import base64,json,sys
from pathlib import Path
import course_audio as audio
out=audio.ASSETS
bank={key:audio.p[key] for key in ['id','label','preset_name','bpm','velocity','gate_frames']}
bank['samples']={}
reports={}
for label,midi in {'C':60,'D':62,'E':64,'G':67}.items():
    filename=f'course-synth-{label}{midi}.wav'
    events=[(0,'on',midi,63),(audio.gate/audio.rate,'off',midi,0)]
    reports[label]=audio.render(events,1.8,filename)
    bank['samples'][label]=base64.b64encode((out/filename).read_bytes()).decode()
for slug,notes in [('ascending',[60,62,64,67]),('descending',[67,64,62,60])]:
    events=[]
    for i,note in enumerate(notes*2):
        start=i*60/audio.p['bpm']
        events.extend([(start,'on',note,63),(start+audio.gate/audio.rate,'off',note,0)])
    reports[slug]=audio.render(events,6.8,f'lesson-02-{slug}.wav')
(out/'melody-sounds.js').write_text("'use strict';\nwindow.OrcaMelodyAudio=Object.freeze("+json.dumps(bank,ensure_ascii=False,separators=(',',':'))+");\n")
(out/'lesson-02-audio.json').write_text(json.dumps({'profile':'course-sound.json','renders':reports},ensure_ascii=False,indent=2)+'\n')
print(json.dumps(reports,ensure_ascii=False,indent=2))
