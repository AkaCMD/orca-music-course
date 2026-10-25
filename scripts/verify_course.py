"""Validate lesson links, terminal MIDI behavior, and PCM loop metadata."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote,urlsplit
import array,json,subprocess,sys,wave
from build_full_course import VARIANTS
from pattern_engine import ROOT,trace,verify
O=ROOT/'outputs'
class Document(HTMLParser):
    def __init__(self):super().__init__();self.links=[];self.ids=set();self.answers=[];self.current_quiz=None;self.quizzes=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.add(a['id'])
        for key in ('href','src','data-calm','data-battle'):
            if a.get(key):self.links.append(a[key])
        if 'data-quiz' in a:self.quizzes.append(a)
    def handle_endtag(self,tag):pass

def main():
    lessons=sorted((O/'lessons').glob('*.html'))
    assert len(lessons)==12,len(lessons)
    assert len(list((O/'reference').glob('*.html')))==13
    docs={f:Document() for f in O.rglob('*.html')}
    for path,doc in docs.items():doc.feed(path.read_text())
    for path,doc in docs.items():
        for link in doc.links:
            parsed=urlsplit(link)
            if parsed.scheme or parsed.netloc:continue
            target=(path.parent/unquote(parsed.path)).resolve() if parsed.path else path.resolve()
            assert target.exists(),f'{path.relative_to(ROOT)}: missing {link}'
            if parsed.fragment and target.suffix=='.html':
                target_doc=docs.get(target)
                assert target_doc is not None and parsed.fragment in target_doc.ids,(path,link)
    assert all(docs[p].quizzes for p in lessons)
    checked=0
    for n,variants in VARIANTS.items():
        for slug,tracks,frames,_ in variants:
            verify(O/'patterns'/f'{n:02d}-{slug}.orca',tracks,frames*2);checked+=1
    basics=[('01-pulse.orca',4,[60]*8),('02-density.orca',2,[60]*16),('03-four-note-melody.orca',4,[60,62,64,67]*2),('04-descending-melody.orca',4,[67,64,62,60]*2)]
    for filename,step,notes in basics:
        events=trace(O/'patterns'/filename,32)
        assert [e[0] for e in events]==list(range(0,32,step))
        assert [e[1] for e in events]==notes
        checked+=1
    manifest=json.loads((O/'manifests/course.json').read_text());wave_count=0
    for lesson in manifest['lessons']:
        for variant in lesson['variants']:
            with wave.open(str(O/'audio'/variant['audio']),'rb') as wav:
                assert (wav.getnchannels(),wav.getsampwidth(),wav.getframerate())==(2,2,48000)
                assert wav.getnframes()==variant['report']['frames']
                values=array.array('h');values.frombytes(wav.readframes(wav.getnframes()))
            peak=max(abs(min(values)),abs(max(values)))/32768
            assert 0<peak<.98
            if variant['loop']:
                assert len(values)//2==variant['frames']*8000
                jump=max(abs(values[-2]-values[0]),abs(values[-1]-values[1]))/32768
                assert jump<.04
            wave_count+=1
    assert json.loads((O/'projects/final-cue/score.json').read_text())['sample_frames']==1024000
    for script in (O/'assets').glob('*.js'):
        subprocess.run(['node','--check',str(script)],check=True,capture_output=True)
    print(json.dumps({'lessons':len(lessons),'reference_pages':13,'html_pages':len(docs),'terminal_patterns_checked':checked,'new_audio_previews_checked':wave_count,'local_links':'pass','javascript_syntax':'pass'},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
