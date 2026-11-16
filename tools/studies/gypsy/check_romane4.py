"""Independent checks for romane4.py (L'Esprit Manouche, part A of chapters 14, 17, 22 and 23). Their tabs, triads and grips
are written out again here as note names on strings, read from the book (pp. 114, 138, 177–178, 185–186); ours must be
theirs moved whole along the neck on the same strings; the scale, triads and chords must be what the text calls them; the
static top voice must stay put while the bass falls by half steps; rhythm, names and the song's chords and bars named."""
import sys, re, json
sys.path.insert(0, '/home/claude/studies'); sys.path.insert(0, '/home/claude/studies/gypsy'); sys.path.insert(0, '/home/claude/scripts')
import romane4 as R
import gtr

probs = []
def P(m): probs.append(m)
OPENS = [40, 45, 50, 55, 59, 64]
LET = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
def pc(n): return (LET[n[0]] + n.count('♯') - n.count('♭')) % 12
def nm(n):
    m = re.fullmatch(r'([A-G])([♯♭]?)(\d)', n)
    return 12 * (int(m.group(3)) + 1) + LET[m.group(1)] + (m.group(2) == '♯') - (m.group(2) == '♭')
def at(s, f): return OPENS[6 - s] + f

BOOK = {
    'hd48': 'D3/5 D♯3/5 F3/5 F♯3/5 G♯3/4 A3/4 B3/4 C4/4 D4/3 D♯4/3 F4/3 F♯4/3 G♯4/2 A4/2 B4/2 C5/2 D5/1 D♯5/1 F5/1 F♯5/1',
    's70': 'C4/4 E5/1 B3/4 D5/1 A3/4 C5/1 G3/5 B4/2 F3/5 A4/2 E3/5 G4/2 D3/6 F4/3 C3/6 E4/3',
    's71': 'E5/1 D5/2 E5/1 C5/2 E5/1 B4/2 E5/1 A4/3 E5/1 G♯4/3 E5/1 A4/3 E5/1 B4/2 E5/1 C5/2',
    's72': 'F5/1 E5/1 F5/1 D5/2 F5/1 C5/2 F5/1 B4/2 D5/1 C5/2 D5/1 B4/2 D5/1 A4/2 D5/1 G♯4/2',
    's73': 'E5/1 D5/2 E5/1 C5/2 E5/1 B4/2 E5/1 A4/2 E5/1 G♯4/2 D5/1 F4/2 B4/1 E4/2 C5/1 D4/3 B4/1',
}
TRI_BOOK = {'t58a': ['A3 D4 F♯4', 'C4 E4 G4', 'D4 F♯4 A4', 'E4 G4 C5', 'F♯4 A4 D5', 'G4 C5 E5', 'A4 D5 F♯5'],
            't58b': ['E3 G3 C4', 'F♯3 A3 D4', 'G3 C4 E4', 'A3 D4 F♯4', 'C4 E4 G4', 'D4 F♯4 A4']}
GRIP_BOOK = {'v66': [('G6/9', 'G2 D3 G3 B3 E4 A4'), ('Eb9/Bb', 'B♭2 E♭3 G3 D♭4 F4 B♭4'), ('Ab6/9', 'A♭2 E♭3 A♭3 C4 F4 B♭4'),
                     ('D9/A', 'A2 D3 F♯3 C4 E4 A4'), ('G6/9', 'G2 D3 G3 B3 E4 A4')],
             'v67': [('Am9', 'A2 E3 A3 C4 G4 B4'), ('Ab9', 'A♭2 E♭3 A♭3 C4 G♭4 B♭4'), ('G6/9', 'G2 D3 G3 B3 E4 A4')],
             'v69': [('C#m7b5', 'C♯3 B3 E4 G4'), ('F9/C', 'C3 A3 E♭4 G4'), ('G/B', 'B2 G3 D4 G4'), ('Bb13', 'B♭2 A♭3 D4 G4'),
                     ('A7', 'A2 E3 G3 C♯4 G4'), ('Abmaj7', 'A♭2 E♭3 A♭3 C4 G4'), ('Gmaj7', 'G2 D3 G3 B3 F♯4 B4')]}
MOVE = {'hd48': 1, 't58a': 1, 't58b': 1, 'v66': 6, 'v67': 6, 'v69': -1, 's70': 1, 's71': 1, 's72': 1, 's73': 1}
OUR_NAMES = {'v66': ['Db6/9', 'A9/E', 'D6/9', 'Ab9/Eb', 'Db6/9'], 'v67': ['Ebm9', 'D9', 'Db6/9'],
             'v69': ['Cm7b5', 'E9/B', 'Gb/Bb', 'A13', 'Ab7', 'Gmaj7', 'Gbmaj7']}

for key, txt in BOOK.items():
    toks = [t.split('/') for t in txt.split()]
    want = [(int(s), nm(n) - OPENS[6 - int(s)]) for n, s in toks]
    if any(not 0 <= f <= 15 for s, f in want): P(f'{key}: a note of theirs is not on its string')
    if list(R.THEIRS[key]) != want:
        k = next((i for i, (a, b) in enumerate(zip(R.THEIRS[key], want)) if a != b), min(len(want), len(R.THEIRS[key])))
        P(f'{key}: their notes differ from the book at {k + 1}')
    if R.ours(key) != [(s, f + MOVE[key]) for s, f in want]: P(f'{key}: ours is not theirs moved {MOVE[key]:+d}')
    if any(f < 1 or f > 16 for s, f in R.ours(key)): P(f'{key}: an open string or a fret above the 16th')
# the half-diminished scale: half, whole, half, whole … from E♭
ms = [at(*x) for x in R.ours('hd48')]
if [b - a for a, b in zip(ms, ms[1:])] != [1, 2] * 9 + [1] or ms[0] % 12 != 3: P('hd48: not the half-whole scale from E♭')
if {m % 12 for m in ms} != {3, 4, 6, 7, 9, 10, 0, 1}: P('hd48: notes')
# s70: tenths falling down D♭ major; s71: F every other note; s72: G♭ then E♭; s73: F, then the two lines
ms = [at(*x) for x in R.ours('s70')]
DB = {1, 3, 5, 6, 8, 10, 0}
if any(m % 12 not in DB for m in ms) or any(hi - lo not in (15, 16) for lo, hi in zip(ms[0::2], ms[1::2])) or any(b >= a for a, b in zip(ms[0::2], ms[2::2])):
    P('s70: not D♭ major falling in tenths')
BBM = {10, 0, 1, 3, 5, 6, 9}
for key in ('s71', 's72', 's73'):
    if any(at(*x) % 12 not in BBM for x in R.ours(key)): P(f'{key}: a note outside B♭ harmonic minor')
ms = [at(*x) for x in R.ours('s71')]
if set(ms[0::2]) != {77}: P('s71: F5 is not every other note')
ms = [at(*x) for x in R.ours('s72')]
if set(ms[0:8:2]) != {78} or set(ms[8:15:2]) != {75} or ms[15] % 12 != 9: P('s72: not round G♭, then E♭, onto A')
ms = [at(*x) for x in R.ours('s73')]
if set(ms[0:7:2]) != {77} or ms[-1] % 12 != 0: P('s73: the turning F or the end')
# triads
for key, books in TRI_BOOK.items():
    strs = R.TSTR[key]
    for (name, fr), want in zip(R.TRIADS[key], books):
        got = [at(s, f) for s, f in zip(strs, fr)]
        if got != [nm(x) for x in want.split()]: P(f'{key}: their {name} triad at {fr} is not {want}')
        if {g % 12 for g in got} != gtr.chord_pcs(name): P(f'{key}: their {name} is not {name} major')
    names = [n for n, fr in R.TRIADS[key]]
    if names != (['D', 'C'] * 4)[:len(names)] and names != (['C', 'D'] * 4)[:len(names)]: P(f'{key}: not alternating')
    lows = [min(fr) for n, fr in R.TRIADS[key]]
    if lows != sorted(lows): P(f'{key}: not in order up the neck')
EXS = {e['id']: e for S in R.SECTIONS[-4:] for e in S['ex']}
for key in TRI_BOOK:
    ex = EXS[key]
    strs = R.TSTR[key]
    tri = [({'C': 'Db', 'D': 'Eb'}[n], [f + 1 for f in fr]) for n, fr in R.TRIADS[key]]
    path = tri + tri[-2::-1]
    chords = [it for B in ex['bars'] for it in B['items'] if it[0] == 'C']
    if [(c[1], [c[2][6 - s] for s in strs]) for c in chords] != [(n, fr) for n, fr in path] or any(c[3] != 1 for c in chords): P(f'{key}: the chords up and back')
    for c in chords:
        if {(OPENS[i] + f) % 12 for i, f in enumerate(c[2]) if f >= 0} != gtr.chord_pcs(c[1]) or sum(f >= 0 for f in c[2]) != 3: P(f'{key}: {c[1]} grip')
    runs = [x for B in ex['bars'] for it in B['items'] if it[0] == 'R' for x in zip(it[1], it[2])]
    want = []
    for k, (n, fr) in enumerate(path):
        t = [[s, f] for s, f in zip(strs, fr)]
        want += t if k < len(tri) else t[::-1]
    if [list(x[0]) for x in runs] != want or any(abs(x[1] - 1 / 3) > 1e-9 for x in runs): P(f'{key}: the arpeggios')
    if {tuple(B['chords']) for B in ex['bars']} != {('Eb7',)}: P(f'{key}: not over E♭7')
# grips
for key, gs in GRIP_BOOK.items():
    for (tn, notes), (rn, g) in zip(gs, R.VOICINGS[key]):
        if tn != rn or sorted(OPENS[i] + f for i, f in enumerate(g) if f >= 0) != sorted(nm(x) for x in notes.split()): P(f'{key}: their {tn}')
        if {nm(x) % 12 for x in notes.split()} - gtr.chord_pcs(tn.replace('#', '#')): P(f'{key}: their {tn} has a note outside it')
    ours = R.GR[key]
    if list(ours) != list(dict.fromkeys(OUR_NAMES[key])): P(f'{key}: names {list(ours)}')
    for (tn, g), on in zip(R.VOICINGS[key], OUR_NAMES[key]):
        if ours[on] != [f + MOVE[key] if f >= 0 else -1 for f in g]: P(f'{key}: {on} is not their {tn} moved')
        if {(OPENS[i] + f) % 12 for i, f in enumerate(ours[on]) if f >= 0} - gtr.chord_pcs(on): P(f'{key}: {on} has a note outside it')
        r, q, bass = gtr.parse(on)
        low = min(OPENS[i] + f for i, f in enumerate(ours[on]) if f >= 0) % 12
        if low != (bass if bass is not None else r): P(f'{key}: {on} has the wrong bass')
        if max(ours[on]) > 16 or min(f for f in ours[on] if f >= 0) < 1: P(f'{key}: {on} out of reach')
    seq = [B['chords'][0] for B in EXS[key]['bars']]
    for B in EXS[key]['bars']:
        if any(it[0] != 'K' or it[2] != ours[it[1]] for it in B['items']): P(f'{key}: a bar not on its grip')
    want = {'v66': ['Db6/9', 'A9/E', 'D6/9', 'Ab9/Eb'] * 2 + ['Db6/9'], 'v67': ['Ebm9', 'D9', 'Db6/9', 'Db6/9'] * 2, 'v69': OUR_NAMES['v69']}[key]
    if seq != want: P(f'{key}: bars {seq}')
# the static top voice and the falling bass
v = [R.GR['v69'][n] for n in OUR_NAMES['v69']]
if len({g[4] for g in v[:6]}) != 1 or (OPENS[4] + v[0][4]) % 12 != 6: P('v69: the top is not G♭ held')
basses = [min(OPENS[i] + f for i, f in enumerate(g) if f >= 0) for g in v]
if [b - a for a, b in zip(basses, basses[1:])] != [-1] * 6: P('v69: the bass does not fall by half steps')
# rhythm and names
for key in ('hd48', 's70', 's71', 's72', 's73'):
    ex = EXS[key]
    notes, durs, labs, lens = [], [], [], []
    for B in ex['bars']:
        L = 0
        for it in B['items']:
            if it[0] == 'R': notes += [tuple(x) for x in it[1]]; durs += it[2]; labs += it[3][1:].split('|')[0].split(','); L += sum(it[2])
            elif it[0] == 'W': L += it[1]
            elif it[0] == 'C': L += it[3]
        lens.append(L)
    if notes != R.ours(key): P(f'{key}: not the notes in order')
    if [pc(re.sub(r'[↓↑]', '', l)) for l in labs] != [at(*n) % 12 for n in notes]: P(f'{key}: a name')
    want = {'hd48': ([0.5] * 20, [4, 4, 4]), 's70': ([0.5] * 15 + [2.5], [4, 8]), 's71': ([0.5] * 15 + [2], [4, 4, 4]),
            's72': ([0.5] * 15 + [2], [4, 4, 4]), 's73': ([0.5] * 17, [4, 4, 4])}[key]
    if durs != want[0] or lens != want[1]: P(f'{key}: rhythm {durs} {lens}')
    if key != 'hd48' and key != 's70' and ex['bars'][0]['items'][0] != ['W', 0.5]: P(f'{key}: not after an eighth’s rest')
c = [it for it in EXS['s73']['bars'][-1]['items'] if it[0] == 'C'][0]
if c[2] != [-1, -1, -1, 6, 6, 6] or {(OPENS[i] + f) % 12 for i, f in enumerate(c[2]) if f >= 0} != gtr.chord_pcs('Bbm'): P('s73: the last chord')
CH = {'hd48': {('Eb7',)}, 's70': {('Db',)}, 's71': {('Bbm',)}}
for k, w in CH.items():
    if {tuple(B['chords']) for B in EXS[k]['bars']} != w: P(f'{k}: chords')
if [B['chords'] for B in EXS['s72']['bars']] != [['Ebm'], ['Ebm'], ['F7']] or [B['chords'] for B in EXS['s73']['bars']] != [['Bbm'], ['F7'], ['Bbm']]: P('s72/s73: chords')
# the song
h = open('/home/claude/fret-finder/songs/it-had-to-be-you/index.html').read()
i = h.find('"chorus": [')
chorus, _ = json.JSONDecoder().raw_decode(h[i + len('"chorus": '):])
where = {}
for b in chorus:
    for sg in b['segs']: where.setdefault(sg['c'], set()).add(int(b['lab']))
j = h.find('"intro": [')
intro, _ = json.JSONDecoder().raw_decode(h[j + len('"intro": '):])
intro_ch = [sg['c'] for b in intro[:2] for sg in b['segs']]
if intro_ch != ['D♭maj9', 'B♭m7', 'E♭m9', 'A♭7']: P(f'song: the intro is {intro_ch}')
for c, bars in (('E♭9', {5, 6, 7, 8, 13, 14}), ('E♭m9', {15}), ('A♭7', {16}), ('D♭maj7', {17}), ('G♭maj7', {25})):
    if not bars <= where.get(c, set()): P(f'song: {c} is not in bars {sorted(bars)}')
if not ({10, 11, 12} <= where.get('F7♭9', set()) | where.get('F7♯5', set())): P('song: F7 not in bars 10–12')
print('exercises checked:', len(EXS))
print('\n'.join(probs) if probs else 'all good')
sys.exit(1 if probs else 0)
