"""Scales after Segovia's Diatonic Major and Minor Scales (1953): two octaves up and down in eighths, apoyando,
each played seven times with a different pair (or three) of right-hand fingers. Segovia's fingering is his; ours
is worked out here. The keys are those of the owner's songs."""
import sys
sys.path.insert(0, '/home/claude/studies')
from kit_study import N, nn, place_lines, OPEN

SEG = 'Diatonic Major and Minor Scales'
MAJ = [0, 2, 4, 5, 7, 9, 11]
MEL_UP = [0, 2, 3, 5, 7, 9, 11]; NAT_DOWN = [0, 2, 3, 5, 7, 8, 10]
FLAT_KEYS = {'F', 'Bb', 'Eb', 'Ab', 'Db', 'C', 'Gm', 'Cm', 'Dm', 'Fm'}


LET = 'CDEFGAB'; NAT = [0, 2, 4, 5, 7, 9, 11]


def spell(root, deg, midi):
    """the note's name from its scale degree: D minor's 7th going up is C♯, not D♭"""
    li = (LET.index(root[0]) + deg) % 7
    d = (midi - NAT[li]) % 12
    acc = {0: '', 1: '♯', 2: '𝄪', 11: '♭', 10: '𝄫'}[d]
    return LET[li] + acc


def scale(root, kind):
    r = N(root)
    up_steps = MAJ if kind == 'major' else MEL_UP
    dn_steps = MAJ if kind == 'major' else NAT_DOWN
    up = [(r + 12 * o + s, k) for o in range(2) for k, s in enumerate(up_steps)] + [(r + 24, 0)]
    down = [(r + 12 * o + s, k) for o in (1, 0) for k, s in reversed(list(enumerate(dn_steps)))]
    return up + down            # 15 up, 14 down: 29 notes, then the root held to fill the bar


RH = 'Apoyando, seven times through: i–m, m–i, a–m, m–a, i–a, a–i, then i–m–a–m.'
KEYS = [('F2', 'major', 'F major', 'Moonglow'), ('D3', 'minor', 'D minor', 'Moonglow’s relative minor'),
        ('G2', 'major', 'G major', 'Я вас любил'), ('E2', 'minor', 'E minor', 'its relative minor'),
        ('B2', 'major', 'B major', 'Misty'), ('G#2', 'minor', 'G♯ minor', 'its relative minor'),
        ('Eb3', 'major', 'E♭ major', 'the Glinka romance'), ('C3', 'minor', 'C minor', 'its relative minor')]


def scale_bars(root, kind, label):
    ms = scale(root, kind) + [(N(root), 0)]
    steps = place_lines([(m, None, .5) for m, k in ms[:-1]] + [(ms[-1][0], None, 1.5)], lo_strings=(6, 5, 4, 3, 2, 1), maxf=12, open_cost=3.0)
    notes = [g[0] for g, d in steps]
    durs = [d for g, d in steps]
    names = [spell(root, k, m) for m, k in ms]
    bars, i = [], 0
    while i < len(notes):
        k, tot = i, 0
        while k < len(notes) and tot + durs[k] <= 4 + 1e-9: tot += durs[k]; k += 1
        items = [['R', notes[i:k], durs[i:k], '=' + ','.join(names[i:k])]]
        if tot < 4 - 1e-9: items.append(['W', 4 - tot])
        bars.append(items); i = k
    return bars


EX = []
for root, kind, title, song in KEYS:
    bars = scale_bars(root, kind, title)
    up = 'up with the 6th and 7th raised, down without them (melodic minor, as Segovia writes his)' if kind == 'minor' else 'up and down'
    EX.append(dict(
        id='scale-' + title.split()[0].lower().replace('♯', 's').replace('♭', 'b') + '-' + kind, title=(f'{title}, the key of {song}' if kind == 'major' else f'{title}, its relative minor'),
        idea=f'Two octaves {up}, in eighths. {RH}',
        quote=dict(where=f'{SEG}, p. 3, the first scale (C major), and the finger table under it',
                   text='Segovia’s C major starts on C on the A string (3rd fret) with the 2nd finger and D (5th fret) with the 4th, then crosses to the D string. Under the scale he writes seven rows of right-hand fingers: i m, m i, a m, m a, i a, a i, and i m a m. The opening:',
                   item=['R', [[5, 3], [5, 5]], [.5, .5], ''], whose='Segovia’s own', played='Played here: those two notes.') if not EX else dict(where='', text='', item=None),
        bars=[dict(chords=[], note=('Up from the lowest ' + title.split()[0] + '.') if j == 0 else '', items=b) for j, b in enumerate(bars)]))
SECTIONS = [dict(id='scales', title='Scales in the keys of your songs', part='Exercises', ex=EX)]
