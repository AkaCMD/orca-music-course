from pathlib import Path
import ctypes as c
import ctypes.util, json, wave, struct, hashlib, base64
ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/'outputs/assets'
p=json.loads((ASSETS/'course-sound.json').read_text())
sfpath=Path('/home/cmd/.local/share/soundfonts')/p['soundfont']
lib=c.CDLL(ctypes.util.find_library('fluidsynth'))
def bind(n,rt,args):
    fn=getattr(lib,n);fn.restype=rt;fn.argtypes=args;return fn
P=c.c_void_p; I=c.c_int; F=c.c_float
new_settings=bind('new_fluid_settings',P,[])
setnum=bind('fluid_settings_setnum',I,[P,c.c_char_p,c.c_double])
setint=bind('fluid_settings_setint',I,[P,c.c_char_p,I])
new_synth=bind('new_fluid_synth',P,[P]);load=bind('fluid_synth_sfload',I,[P,c.c_char_p,I])
select=bind('fluid_synth_program_select',I,[P,I,I,I,I])
getpreset=bind('fluid_synth_get_channel_preset',P,[P,I])
presetname=bind('fluid_preset_get_name',c.c_char_p,[P])
on=bind('fluid_synth_noteon',I,[P,I,I,I]);off=bind('fluid_synth_noteoff',I,[P,I,I])
write=bind('fluid_synth_write_float',I,[P,I,P,I,I,P,I,I])
free_synth=bind('delete_fluid_synth',None,[P]);free_settings=bind('delete_fluid_settings',None,[P])
rate=p['sample_rate']; gate=round(60/p['bpm']/4*p['gate_frames']*rate)
def render(events,seconds,filename):
    st=new_settings()
    for key,val in {'synth.sample-rate':rate,'synth.gain':p['gain'],**p['settings']}.items():
        fn=setint if key.endswith('.active') else setnum
        assert fn(st,key.encode(),val)==0
    sy=new_synth(st)
    try:
        sf=load(sy,str(sfpath).encode(),1);assert sf>0
        assert select(sy,0,sf,p['bank'],p['program'])==0
        actual_name=presetname(getpreset(sy,0)).decode()
        total=[]
        def block(n):
            if not n:return
            l=(F*n)();r=(F*n)();assert write(sy,n,l,0,1,r,0,1)==0
            total.extend(zip(l,r))
        cursor=0
        for t,kind,note,vel in sorted(events):
            target=round(t*rate);block(target-cursor);cursor=target
            assert (on(sy,0,note,vel) if kind=='on' else off(sy,0,note))==0
        block(round(seconds*rate)-cursor)
        peak=max(abs(x) for row in total for x in row)
        assert .005<peak<.92,(peak,filename)
        pcm=b''.join(struct.pack('<hh',*(max(-32768,min(32767,round(v*32767))) for v in row)) for row in total)
        with wave.open(str(ASSETS/filename),'wb') as wav:
            wav.setparams((2,2,rate,0,'NONE','not compressed'));wav.writeframes(pcm)
        return {'preset':actual_name,'peak':peak,'duration':seconds}
    finally:free_synth(sy);free_settings(st)
