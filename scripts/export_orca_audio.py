"""Export a note-only Orca patch to the same SoundFont used by the lessons."""
from pathlib import Path
import argparse
import array
import json
from pattern_engine import trace, midi_events
import course_audio as audio

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pattern',type=Path)
    parser.add_argument('--bars',type=int,required=True)
    parser.add_argument('--bpm',type=float,default=90)
    parser.add_argument('--loop',action='store_true')
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    if not 1<=args.bars<=64 or not 20<=args.bpm<=300:parser.error('Use 1-64 bars and 20-300 BPM')
    frames=args.bars*16
    cycles=3 if args.loop else 1
    actual=trace(args.pattern,frames*cycles)
    first=[e for e in actual if e[0]<frames]
    if not first:parser.error('The selected interval contains no MIDI notes')
    if args.loop:
        for cycle in range(1,cycles):
            current=[(e[0]-cycle*frames,*e[1:]) for e in actual if cycle*frames<=e[0]<(cycle+1)*frames]
            if current!=first:parser.error('The MIDI event sequence does not repeat at the requested bar length')
    seconds=frames*60/args.bpm/4
    release=max(e[4] for e in first)*60/args.bpm/4+2
    events=midi_events(first,bpm=args.bpm,repeat=cycles,cycle_frames=frames)
    pcm,report=audio.render_pcm(events,cycles*seconds+release)
    if args.loop:
        count=round(seconds*audio.rate)
        pcm=pcm[(cycles-1)*count*4:cycles*count*4]
        values=array.array('h');values.frombytes(pcm)
        jump=max(abs(values[-2]-values[0]),abs(values[-1]-values[1]))/32768
        if jump>=.04:parser.error(f'Large loop waveform boundary ({jump:.4f}); revise the patch or loop interval')
        report.update(frames=count,duration=count/audio.rate,boundary_jump=jump)
    audio.save_pcm(args.output,pcm)
    report.update(pattern=args.pattern.name,bars=args.bars,bpm=args.bpm,loop=args.loop,soundfont=audio.p['soundfont'],program=audio.p['program'],midi_events=len(first))
    args.output.with_suffix('.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
