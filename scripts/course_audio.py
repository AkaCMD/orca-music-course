"""Render course MIDI events with the installed SoundFont and shared profile."""
from pathlib import Path
import array
import ctypes as c
import ctypes.util
import json
import hashlib
import os
import sys
import wave

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'outputs/assets'
p = json.loads((ASSETS / 'course-sound.json').read_text())
sfpath = Path(os.environ.get('ORCA_SOUNDFONT_DIR', str(Path.home() / '.local/share/soundfonts'))) / p['soundfont']
if p.get('soundfont_sha256') and hashlib.sha256(sfpath.read_bytes()).hexdigest() != p['soundfont_sha256']:
    raise RuntimeError('SoundFont differs from course-sound.json; select the recorded font or update the profile and regenerate the previews')
lib = c.CDLL(ctypes.util.find_library('fluidsynth'))

def bind(name, result, args):
    function = getattr(lib, name)
    function.restype = result
    function.argtypes = args
    return function

P, I = c.c_void_p, c.c_int
new_settings = bind('new_fluid_settings', P, [])
setnum = bind('fluid_settings_setnum', I, [P, c.c_char_p, c.c_double])
setint = bind('fluid_settings_setint', I, [P, c.c_char_p, I])
new_synth = bind('new_fluid_synth', P, [P])
load = bind('fluid_synth_sfload', I, [P, c.c_char_p, I])
select = bind('fluid_synth_program_select', I, [P, I, I, I, I])
getpreset = bind('fluid_synth_get_channel_preset', P, [P, I])
presetname = bind('fluid_preset_get_name', c.c_char_p, [P])
on = bind('fluid_synth_noteon', I, [P, I, I, I])
off = bind('fluid_synth_noteoff', I, [P, I, I])
write16 = bind('fluid_synth_write_s16', I, [P, I, P, I, I, P, I, I])
free_synth = bind('delete_fluid_synth', None, [P])
free_settings = bind('delete_fluid_settings', None, [P])
rate = p['sample_rate']
gate = round(60 / p['bpm'] / 4 * p['gate_frames'] * rate)

def render_pcm(events, seconds):
    """Accept (seconds, on/off, note, velocity[, channel]) tuples."""
    settings = new_settings()
    synth = None
    try:
        for key, value in {'synth.sample-rate': rate, 'synth.gain': p['gain'], **p['settings']}.items():
            setter = setint if key.endswith('.active') else setnum
            assert setter(settings, key.encode(), value) == 0
        synth = new_synth(settings)
        soundfont = load(synth, str(sfpath).encode(), 1)
        assert soundfont > 0, 'SoundFont could not be loaded'
        assert select(synth, 0, soundfont, p['bank'], p['program']) == 0
        assert select(synth, 9, soundfont, 128, 0) == 0
        actual_name = presetname(getpreset(synth, 0)).decode()
        chunks = []
        total_frames = round(seconds * rate)
        def block(count):
            while count > 0:
                size = min(count, 16384)
                buffer = (c.c_short * (size * 2))()
                assert write16(synth, size, buffer, 0, 2, buffer, 1, 2) == 0
                chunks.append(bytes(buffer))
                count -= size
        cursor = 0
        # Releases precede attacks at an identical time, so retriggers survive.
        ordered = sorted(events, key=lambda e: (e[0], e[1] != 'off'))
        for event in ordered:
            when, kind, note, velocity = event[:4]
            channel = event[4] if len(event) > 4 else 0
            target = round(when * rate)
            if target > total_frames:
                raise ValueError('Event outside render duration')
            block(target - cursor)
            cursor = target
            result = on(synth, channel, note, velocity) if kind == 'on' else off(synth, channel, note)
            # One-shot drum voices may already have ended when their note-off arrives.
            if kind == 'on': assert result == 0
        block(total_frames - cursor)
        pcm = b''.join(chunks)
        if sys.byteorder != 'little':
            values = array.array('h'); values.frombytes(pcm); values.byteswap(); pcm = values.tobytes()
        values = array.array('h'); values.frombytes(pcm)
        peak = max(abs(min(values)), abs(max(values))) / 32768
        assert 0 < peak < .98, f'Unexpected peak: {peak}'
        return pcm, {'preset': actual_name, 'peak': peak, 'duration': total_frames / rate, 'sample_rate': rate, 'frames': total_frames}
    finally:
        if synth: free_synth(synth)
        free_settings(settings)

def save_pcm(path, pcm):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), 'wb') as wav:
        wav.setparams((2, 2, rate, 0, 'NONE', 'not compressed'))
        wav.writeframes(pcm)

def render(events, seconds, filename):
    pcm, report = render_pcm(events, seconds)
    save_pcm(ASSETS / filename, pcm)
    return report
