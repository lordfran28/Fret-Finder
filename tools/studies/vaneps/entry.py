"""George Van Eps, Harmonic Mechanisms for Guitar vol. 1: the scale in first-inversion triads (root on top),
three voices on three adjacent strings, full range, up and back (book p. 29, 'Scale in first inversion triads taken
thru the descending cycle of fifths'). His book gives every key; ours is the key of your Moonglow (F major), with our
own choice of string sets and positions, worked out so the hand moves as little as it can."""
import sys
sys.path.insert(0, '/home/claude/studies')
from kit_study import OPEN, nn, N

BOOK = 'Harmonic Mechanisms for Guitar, vol. 1'
SETS = {4: (6, 5, 4), 3: (5, 4, 3), 2: (4, 3, 2), 1: (3, 2, 1)}        # Van Eps's n/3: the n-th set of three strings
F_MAJ = [5, 7, 9, 10, 0, 2, 4]                                           # F G A Bb C D E
NAMES = ['F', 'Gm', 'Am', 'Bb', 'C', 'Dm', 'Edim']


def triad(deg, octave_root):
    """first inversion: 3rd, 5th, root above (the root on top); returns three midi notes low to high"""
    sc = F_MAJ
    r = sc[deg % 7] + 12 * (octave_root + 1)
    third = sc[(deg + 2) % 7]; fifth = sc[(deg + 4) % 7]
    t = third + 12 * (octave_root - 1)
    while t >= r: t -= 12
    while t < r - 12: t += 12
    f = fifth + 12 * (octave_root - 1)
    while f <= t: f += 12
    while f >= r: f -= 12
    return [t, f, r]


def placements(midis):
    out = []
    for n, ss in SETS.items():
        fr = [m - OPEN[6 - s] for m, s in zip(midis, ss)]
        if min(fr) < 0 or max(fr) > 15: continue
        pos = [f for f in fr if f > 0]
        if pos and max(pos) - min(pos) + 1 > (5 if min(pos) >= 7 else 4): continue
        g = [-1] * 6
        for s, f in zip(ss, fr): g[6 - s] = f
        out.append((n, g, sum(fr) / 3))
    return out


def path(chords):
    """least movement: a placement for each triad, the hand moving as little as possible, set changes cost a little"""
    best = {}
    for i, ms in enumerate(chords):
        pl = placements(ms)
        assert pl, [nn(m) for m in ms]
        new = {}
        for n, g, a in pl:
            if i == 0:
                new[n] = (a * 0.05, [(n, g)], a); continue
            cands = [(c + abs(a - pa) + (0.6 if n != pn else 0), p, pa) for pn, (c, p, pa) in best.items()]
            c, p, _ = min(cands)
            new[n] = (c, p + [(n, g)], a)
        best = new
    return min(best.values())[1]


# the scale from the lowest first-inversion triad on the low strings (D minor: F, A, D) up to the top of the neck, and back
seq, deg, octv = [], 5, 3               # D minor, root D3
while True:
    t = triad(deg, octv)
    if t[2] > N('F5'): break
    seq.append((NAMES[deg % 7], t))
    deg += 1
    if deg % 7 == 5 and False: pass
    if F_MAJ[deg % 7] < F_MAJ[(deg - 1) % 7]: octv += 1
up = path([m for _, m in seq])
names = [n for n, _ in seq]


def bars_from(names_, grips, per_bar=4):
    out = []
    for i in range(0, len(grips), per_bar):
        chunk = list(zip(names_[i:i + per_bar], grips[i:i + per_bar]))
        items = [['C', nm, g, 1.0, {'roll': 0.004}] for nm, (n, g) in chunk]
        if len(chunk) < per_bar: items.append(['W', per_bar - len(chunk)])
        out.append(dict(chords=[nm for nm, _ in chunk], note='', items=items))
    return out


down = list(reversed(up))[1:]
b = bars_from(names, up) + bars_from(list(reversed(names))[1:], down)
sets_used = []
for n, g in up:
    if not sets_used or sets_used[-1] != n: sets_used.append(n)
b[0]['note'] = ('Moonglow’s key, F major: each triad with its root on top (the 3rd at the bottom), one to a beat, from D minor on the three low strings up the scale to the top of the neck, then back down. '
                f'The string sets change as the scale climbs: {", ".join(f"{n}/3" for n in sets_used)} (Van Eps’s names: 4/3 is the low E, A and D strings, 1/3 the G, B and high E). '
                'Alternate two fingers where you can, as he advises, rather than hopping on one.')
EX = [dict(
    id='triads-1st', title='The scale in first-inversion triads',
    idea=('Van Eps: three voices on three adjacent strings, the scale’s own triads one after another, the root on top. The same three notes in every position up the neck; '
          'the shapes repeat each octave, so the whole neck becomes one map of the key. Name each triad as you play it.'),
    quote=dict(where=f'{BOOK}, p. 29', text='his first key, C major, begins on the lowest strings with D minor (F, A, D) and E minor (G, B, E).',
               items=[['C', 'Dm', [1, 0, 0, -1, -1, -1], 1.0, {'roll': 0.004}], ['C', 'Em', [3, 2, 2, -1, -1, -1], 1.0, {'roll': 0.004}], ['W', 2]],
               whose='Van Eps’s own', played='Played here: those two.'),
    bars=b)]
SECTIONS = [dict(id='vaneps', title='Three-voice triads', part='Exercises', ex=EX)]
