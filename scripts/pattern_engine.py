"""Build compact Orca tracks, execute the actual terminal VM, and render its events."""
from pathlib import Path
import array
import json
import os
import subprocess
import course_audio as audio

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / 'work'
WORK.mkdir(exist_ok=True)
SOURCE = Path(os.environ.get('ORCA_SOURCE', str(Path.home() / 'orca-src')))
TRACE = WORK / 'trace-orca-notes'
DIGITS = '0123456789abcdefghijklmnopqrstuvwxyz'

def compile_trace():
    paths = [ROOT / 'scripts/trace_orca_notes.c'] + [SOURCE / f for f in ['sim.c', 'field.c', 'gbuffer.c', 'vmio.c']]
    if not TRACE.exists() or any(p.stat().st_mtime > TRACE.stat().st_mtime for p in paths):
        subprocess.run(['cc', '-std=c11', '-O2', '-I' + str(SOURCE), *map(str, paths), '-o', str(TRACE)], check=True)

def track(notes='CDEG', step=4, octave=5, velocity=6, gate=1, channel=0, label='LEAD', field='note'):
    assert 1 <= len(notes) <= 35 and 1 <= step <= 35
    return dict(notes=notes, step=step, octave=octave, velocity=velocity, gate=gate, channel=channel, label=label, field=field)

def grid(tracks):
    blocks = []
    for t in tracks:
        width = max(18, len(t['notes']) + 10)
        rows = [list('.' * width) for _ in range(3)]
        target = 6 if t['field'] == 'note' else 7
        clock = target - 2
        rows[0][clock - 1:clock + 2] = list(DIGITS[t['step']] + 'C' + DIGITS[len(t['notes'])])
        rows[1][2:4] = list('D' + DIGITS[t['step']])
        rows[1][target - 2:target + 1] = list('0' + DIGITS[len(t['notes'])] + 'T')
        rows[1][target + 1:target + 1 + len(t['notes'])] = list(t['notes'])
        current_note = t['notes'][0] if t['field'] == 'note' else 'C'
        rows[2][3:9] = list(':' + DIGITS[t['channel']] + DIGITS[t['octave']] + current_note + DIGITS[t['velocity']] + DIGITS[t['gate']])
        blocks.append(['#' + t['label']] + [''.join(r) for r in rows] + ['.'])
    width = max(len(r) for block in blocks for r in block)
    return '\n'.join(r.ljust(width, '.') for block in blocks for r in block) + '\n'

def save_pattern(filename, tracks):
    path = ROOT / 'outputs/patterns' / filename
    path.write_text(grid(tracks))
    return path

def trace(path, frames):
    compile_trace()
    result = subprocess.run([str(TRACE), str(path), str(frames)], check=True, capture_output=True, text=True)
    return [tuple(map(int, line.split())) for line in result.stdout.splitlines()]

def expected_events(tracks, frames):
    events = []
    semitones = [0, 2, 4, 5, 7, 9, 11]
    for tick in range(frames):
        for t in tracks:
            if tick % t['step']: continue
            value = t['notes'][(tick // t['step']) % len(t['notes'])]
            note = value if t['field'] == 'note' else 'C'
            velocity = t['velocity'] if t['field'] == 'note' else DIGITS.index(value.lower()) if value != '.' else 127
            if not note.isalpha() or velocity == 0: continue
            letter = note.upper()
            degree = ord(letter) - ord('C') if letter > 'B' else ord(letter) - ord('A') + 5
            midi = t['octave'] * 12 + degree // 7 * 12 + semitones[degree % 7] + int(note.islower())
            events.append((tick, min(midi, 127), t['channel'], min(velocity * 8 - 1, 127), t['gate']))
    return events

def verify(path, tracks, frames):
    actual = trace(path, frames)
    expected = expected_events(tracks, frames)
    assert actual == expected, f'VM mismatch in {path.name}: {actual[:8]} != {expected[:8]}'
    assert actual, f'No notes in {path}'
    return actual

def midi_events(events, bpm=90, repeat=1, cycle_frames=16):
    seconds_per_frame = 60 / bpm / 4
    result = []
    # Voice ownership is by channel and key. Current arrangements keep registers apart.
    for cycle in range(repeat):
        for tick, note, channel, velocity, duration in events:
            start = (cycle * cycle_frames + tick) * seconds_per_frame
            result += [(start, 'on', note, velocity, channel), (start + duration * seconds_per_frame, 'off', note, 0, channel)]
    return result

def render_pattern(path, tracks, frames, audio_name, loop=False):
    events = verify(path, tracks, frames)
    duration = frames * 60 / 90 / 4
    if loop:
        pcm, report = audio.render_pcm(midi_events(events, repeat=3, cycle_frames=frames), duration * 3 + 2)
        sample_frames = round(duration * audio.rate)
        # Extract the last complete cycle after two cycles of effect and release pre-roll.
        pcm = pcm[2 * sample_frames * 4:3 * sample_frames * 4]
        values = array.array('h'); values.frombytes(pcm)
        jump = max(abs(values[-2] - values[0]), abs(values[-1] - values[1])) / 32768
        report.update(duration=sample_frames/audio.rate, frames=sample_frames, boundary_jump=jump, pre_roll_cycles=2)
        assert jump < .04, (path.name, 'loop boundary', jump)
    else:
        pcm, report = audio.render_pcm(midi_events(events, cycle_frames=frames), duration + 1.5)
    target = ROOT / 'outputs/audio' / audio_name
    audio.save_pcm(target, pcm)
    report.update(pattern=path.name, midi_events=len(events), cycle_frames=frames)
    return report
