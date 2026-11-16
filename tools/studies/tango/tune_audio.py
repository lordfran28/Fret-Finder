"""The chorus tune in E♭ with each chord's root under it, as a sound file to check the transcription by ear."""
import sys
sys.path.insert(0, '/home/claude/studies'); sys.path.insert(0, '/home/claude/studies/tango')
import study_page as SP
import kit_study as K
import mel as M
import tune_iw as T

SP.BPM = 112
BASS = {'Eb': 'Eb3', 'G': 'G2', 'Ab': 'Ab2', 'C7': 'C3', 'Fm': 'F2', 'F7': 'F2', 'Bb7': 'Bb2', 'F': 'F2'}


def bass_of(ch):
    for k in sorted(BASS, key=len, reverse=True):
        if ch == k or (ch.startswith(k) and ch[len(k):] in ('', '7', 'm', 'm7')): return BASS[k]
    raise KeyError(ch)


def bars_for(ending):
    out = []
    held = None
    for b, chs, notes, w in T.in_eb(ending=ending, octave=0):
        seq = []; x = 0
        ch_at = {at: c for c, at in chs}
        for n, d in notes:
            # split a note at a chord change inside it (bar 26 changes on beat 3, where a note starts, so none here)
            lo = M.midi(bass_of(ch_at[x])) if x in ch_at else None
            up = None if n == 'r' else M.midi(n.rstrip('~'))
            if n != 'r' and held == n.rstrip('~') and x == 0 and prev_tie: up = None      # a tied note is not struck again
            if lo is None and up is None:
                seq[-1] = (seq[-1][0], seq[-1][1], seq[-1][2] + d) if seq else (None, None, d)
            else:
                seq.append((lo, up, d))
            x += d
        prev_tie_now = notes[-1][0].endswith('~')
        held = notes[-1][0].rstrip('~')
        globals()['prev_tie'] = prev_tie_now
        steps = []
        for lo, up, d in seq:                      # for the ear only: any string that sounds the note
            g = []
            if lo is not None: g.append(K.place(lo, 0, 12, (6, 5, 4)))
            if up is not None: g.append(K.place(up, 1, 12, (1, 2, 3, 4)))
            steps.append((g, d))
        it = K.two_lines(steps, over='')
        out.append(dict(label=f'{"e" if ending == 2 else ""}{b}', items=[it], beats=sum(d for _, d in notes), chords=[c for c, _ in chs]))
    return out


prev_tie = False
bars = bars_for(1)
prev_tie = False
bars += [B for B in bars_for(2) if B['label'] in ('e30', 'e31', 'e32')]
starts, spb = SP.times(bars)
print(SP.render(bars, starts, spb, '/home/claude/studies/tango/out_tune/iwonder-chorus-tune.mp3'), 's')
