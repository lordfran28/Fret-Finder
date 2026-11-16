"""Independent checks for romane3.py (L'Esprit Manouche, part A of chapters 10 and 11). Their tabs are written out again
here as note names on strings, read from the book (pp. 81–91); their grips as note names; ours must be theirs moved
whole along the neck on the same strings by the stated number of frets; every note must belong to its key; the cells
must do what the text says (the step above, the half step below, the note); the rhythm, names, stars and the song's
chords and bars named in the text are checked against your page."""
import sys, re, json
sys.path.insert(0, '/home/claude/studies'); sys.path.insert(0, '/home/claude/studies/gypsy'); sys.path.insert(0, '/home/claude/scripts')
import romane3 as R
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
    'd31': 'E4/2 D4/2 C♯4/2 D4/2 A4/1 G4/1 F♯4/1 G4/1',
    'd32': 'A4/2 G4/2 F♯4/2 G4/2 E5/1 D5/1 C♯5/1 D5/1',
    'd33': 'F4/2 E4/2 D♯4/2 E4/2 B4/1 A4/1 G♯4/1 A4/1',
    'd34': 'B4/2 A4/2 G♯4/2 A4/2 F5/1 E5/1 D♯5/1 E5/1',
    'd37': 'F5/1 E5/1 G5/1 F5/1 B♭4/2 A4/2 C5/2 B♭4/2 F4/3 E4/3 G4/3 F4/3 B♭3/4 A3/4 C4/4 B♭3/4 F3/5 E3/5 G3/5 F3/5 B♭2/6 A2/6 C3/6 B♭2/6',
    'd38': 'B♭2/6 C3/6 A2/6 B♭2/6 F3/5 G3/5 E3/5 F3/5 B♭3/4 C4/4 A3/4 B♭3/4 F4/3 G4/3 E4/3 F4/3 B♭4/2 C5/2 A4/2 B♭4/2 F5/1 G5/1 E5/1 F5/1',
    'd39': 'E♭4/2 D4/2 F4/2 E♭4/2 G3/4 B3/3 D4/2 C4/3',
    'd40': 'G4/2 F♯4/2 A♭4/2 G4/2 B3/4 D4/3 F4/2 E♭4/3',
    'b41': ('C3/5 B2/5 D3/5 C3/5 E3/4 D3/5 F3/4 E3/4 G3/4 F3/4 A3/4 G3/4 B3/3 A3/4 C4/3 B3/3 '
            'D4/3 C4/3 E4/2 D4/3 F4/2 E4/2 G4/2 F4/2 A4/1 G4/2 B4/1 A4/1 C5/1 B4/1 D5/1 C5/1'),
}
SCALE42 = 'B2/6 C3/6 D3/6 E3/5 F♯3/5 G3/5 A3/4 B3/4 C4/4 D4/3 E4/3 F♯4/2 G4/2 A4/2 B4/1 C5/1 D5/1'.split()
BOOK['b42'] = ' '.join(SCALE42[i + j] for i in range(14) for j in range(4))
GRIPS = {'v35': [('Am11', 'A2 G3 C4 D4', '5x553x'), ('Adim7', 'A2 F♯3 C4 E♭4', '5x454x'), ('G6', 'G2 G3 B3 E4', '3x545x')],
         'v36': [('Am9', 'A3 C4 G4 B4', 'xCACCx'), ('D7#5', 'D3 C4 F♯4 A♯4', 'AxABBx'), ('Gmaj9', 'G3 B3 F♯4 A4', 'xA9BAx')]}
MOVE = {'d31': -1, 'd32': -1, 'd33': 1, 'd34': 1, 'v35': -1, 'v36': -1, 'd37': -4, 'd38': -4, 'd39': -2, 'd40': -2, 'b41': 1, 'b42': -1}
KEY = {'d31': 'Gb', 'd32': 'Gb', 'd37': 'Gb', 'd38': 'Gb', 'b42': 'Gb', 'b41': 'Db', 'd33': 'Bbm', 'd34': 'Bbm', 'd39': 'Bbm', 'd40': 'Bbm'}
MAJ = [0, 2, 4, 5, 7, 9, 11]
def keyset(k):
    r = gtr.parse(k)[0]
    return {(r + x) % 12 for x in MAJ} | {(r + 6) % 12} if not k.endswith('m') else {(r + x) % 12 for x in (0, 2, 3, 5, 7, 8, 9, 10, 11)} | {(r + 6) % 12, (r + 4) % 12}

for key, txt in BOOK.items():
    toks = [t.split('/') for t in txt.split()]
    want = [(int(s), nm(n) - OPENS[6 - int(s)]) for n, s in toks]
    if any(not 0 <= f <= 15 for s, f in want): P(f'{key}: a note of theirs is not on its string')
    if list(R.THEIRS[key]) != want:
        k = next((i for i, (a, b) in enumerate(zip(R.THEIRS[key], want)) if a != b), min(len(want), len(R.THEIRS[key])))
        P(f'{key}: their notes differ from the book at {k + 1}')
    ours = R.ours(key)
    if ours != [(s, f + MOVE[key]) for s, f in want]: P(f'{key}: ours is not theirs moved {MOVE[key]:+d}')
    if any(f < 1 or f > 16 for s, f in ours): P(f'{key}: an open string or a fret above the 16th')
    ks = keyset(KEY[key])
    if any(at(s, f) % 12 not in ks for s, f in ours): P(f'{key}: a note outside {KEY[key]}')
    nms = R.names(key)
    if [pc(x) for x in nms] != [at(s, f) % 12 for s, f in ours]: P(f'{key}: names')
    if any('♯' in x for x in nms): P(f'{key}: a sharp in a flat key')
# the cells: step above (in the key), the note, half step below, the note (31-34); 37: note, half below, step above, note; 38: note, above, below, note
for key in ('d31', 'd32', 'd33', 'd34'):
    ms = [at(*x) for x in R.ours(key)]
    for g in (ms[:4], ms[4:]):
        if not (g[1] == g[3] and g[1] - g[2] == 1 and g[0] - g[1] in (1, 2)): P(f'{key}: not the cell')
    root = gtr.parse(KEY[key])[0]
    tg = {ms[1] % 12, ms[5] % 12}
    if tg != {root, (root + 7) % 12}: P(f'{key}: the cell does not circle the root and the 5th')
for key, order in (('d37', (0, -1, 'up', 0)), ('d38', (0, 'up', -1, 0))):
    ms = [at(*x) for x in R.ours(key)]
    root = gtr.parse(KEY[key])[0]
    for k in range(6):
        g = ms[4 * k:4 * k + 4]
        if g[0] != g[3] or g[0] % 12 not in (root, (root + 7) % 12): P(f'{key} group {k + 1}: not on the root or 5th')
        lo, up = (g[1], g[2]) if order[1] == -1 else (g[2], g[1])
        if g[0] - lo != 1 or up - g[0] != 2: P(f'{key} group {k + 1}: not a half step below and a whole step above')
    if len({s for s, f in R.ours(key)[0::4]}) != 6: P(f'{key}: not a string each')
# the V arpeggio (39) and the diminished on its 3rd (40) land on the root and the minor 3rd
ms39 = [at(*x) for x in R.ours('d39')]; ms40 = [at(*x) for x in R.ours('d40')]
if {x % 12 for x in ms39[4:7]} != gtr.chord_pcs('F') or ms39[7] % 12 != 10: P('d39: not the F arpeggio onto B♭')
if {x % 12 for x in ms40[4:7]} != {9, 0, 3} or ms40[7] % 12 != 1: P('d40: not the A diminished arpeggio onto D♭')
# 41: each scale note then the one below; 42: fours up the scale
ms = [at(*x) for x in R.ours('b41')]
sc = sorted(set(ms))
if any(sc.index(a) - sc.index(b) != 1 for a, b in zip(ms[0::2], ms[1::2])) or any(sc.index(b) - sc.index(a) != 1 for a, b in zip(ms[0::2], ms[2::2])): P('b41: not the pairs')
ms = [at(*x) for x in R.ours('b42')]
sc = sorted(set(ms))
if len(sc) != 17 or [ms[4 * i:4 * i + 4] for i in range(14)] != [sc[i:i + 4] for i in range(14)]: P('b42: not fours up the scale')
if any(not 6 <= f <= 9 for s, f in R.ours('b42')): P('b42: not in the 6th position')
# voicings
for key, gs in GRIPS.items():
    for (tn, notes, g), (on, og) in zip(gs, R.VOICINGS[key]):
        frets = [-1 if c == 'x' else int(c, 16) for c in g]
        if frets != og or on != tn: P(f'{key}: their {tn}')
        if sorted(nm(n) for n in notes.split()) != sorted(OPENS[i] + f for i, f in enumerate(frets) if f >= 0): P(f'{key}: their {tn} is not {notes}')
        if {nm(n) % 12 for n in notes.split()} - gtr.chord_pcs(tn): P(f'{key}: {tn} has a note outside it')
    GRo = R.GR35 if key == 'v35' else R.GR36
    for (tn, notes, g), name in zip(gs, R.OUR_V[key]):
        frets = [-1 if c == 'x' else int(c, 16) for c in g]
        if GRo[name] != [f + MOVE[key] if f >= 0 else -1 for f in frets]: P(f'{key}: {name} is not their {tn} moved')
        if {(OPENS[i] + f) % 12 for i, f in enumerate(GRo[name]) if f >= 0} - gtr.chord_pcs(name): P(f'{key}: {name} has a note outside it')
    tops = [OPENS[4] + GRo[n][4] for n in R.OUR_V[key]]
    d = [b - a for a, b in zip(tops, tops[1:])]
    if d != ([1, 1] if key == 'v35' else [-1, -1]): P(f'{key}: the top note does not move by half steps as described')
    EX = {e['id']: e for S in R.SECTIONS for e in S['ex']}
    seq = [B['chords'][0] for B in EX[key]['bars']]
    n = R.OUR_V[key]
    if seq != [n[0], n[1], n[2], n[2]] * 2: P(f'{key}: bars {seq}')
    for B in EX[key]['bars']:
        for it in B['items']:
            if it[0] != 'K' or it[2] != GRo[it[1]]: P(f'{key}: a bar not on its grip')
# rhythm and stars
EXS = {e['id']: e for S in R.SECTIONS[-5:] for e in S['ex']}
if set(EXS) != set(MOVE): P(f'exercises {sorted(EXS)}')
for key, ex in EXS.items():
    if key.startswith('v'): continue
    notes, durs, labs, lens = [], [], [], []
    for B in ex['bars']:
        L = 0
        for it in B['items']:
            if it[0] == 'R': notes += [tuple(x) for x in it[1]]; durs += it[2]; labs += it[3][1:].split('|')[0].split(','); L += sum(it[2])
            elif it[0] == 'W': L += it[1]
        lens.append(L)
    if notes[:len(R.ours(key))] != R.ours(key): P(f'{key}: not the notes in order')
    if any(pc(re.sub(r'[*]', '', l)) != at(*n) % 12 for l, n in zip(labs, notes)): P(f'{key}: a name')
    want_len = {'d37': 2, 'd38': 2, 'd31': 8, 'd32': 8, 'd33': 8, 'd34': 8}.get(key, 4)
    if any(abs(L - want_len) > 1e-9 for L in lens): P(f'{key}: bars of {lens}')
    if key in ('d31', 'd32', 'd33', 'd34'):
        if durs != [0.5] * 7 + [2.5] or len(notes) != 8: P(f'{key}: rhythm')
        if [('*' in l) for l in labs[:8]] != [False, True] * 4: P(f'{key}: stars')
    if key in ('d37', 'd38'):
        if durs != [0.5] * 24 or [('*' in l) for l in labs] != [False, False, False, True] * 6: P(f'{key}: rhythm or stars')
    if key in ('d39', 'd40'):
        if durs != [0.5] * 7 + [2] or ex['bars'][0]['items'][0] != ['W', 0.5]: P(f'{key}: rhythm')
    if key == 'b41' and durs != [0.5] * 32: P('b41: rhythm')
    if key == 'b42' and (durs != [0.25] * 55 + [2] or ex['bars'][0]['items'][0] != ['W', 0.25]): P('b42: rhythm')
    if {tuple(B['chords']) for B in ex['bars']} != {(KEY[key],)}: P(f'{key}: chords')
# quotes
for key, ex in EXS.items():
    it = ex['quote']['items'][0]
    if key.startswith('v'):
        if it[0] != 'C' or it[2] != R.VOICINGS[key][0][1]: P(f'{key}: quote')
        continue
    if [tuple(x) for x in it[1]] != R.THEIRS[key][:len(it[1])] or sum(it[2]) > 2: P(f'{key}: quote')
# the song's chords and bars the texts name
h = open('/home/claude/fret-finder/songs/it-had-to-be-you/index.html').read()
i = h.find('"chorus": [')
chorus, _ = json.JSONDecoder().raw_decode(h[i + len('"chorus": '):])
where = {}
for b in chorus:
    for sg in b['segs']: where.setdefault(sg['c'], set()).add(int(b['lab']))
txt = ' '.join(e['idea'] + ' ' + ' '.join(B['note'] for B in e['bars']) for e in EXS.values())
CLAIMS = [('G♭maj7', {25}), ('F7♭9', {10}), ('B♭m7', {11}), ('A♭m7', {24}), ('D♭7', {24})]
for c, bars in CLAIMS:
    if not bars <= where.get(c, set()): P(f'song: {c} is not in bars {sorted(bars)}')
if 'bar 25' not in txt or 'bars 10–11' not in txt or 'bars 24–25' not in txt: P('the song’s bars are not named as checked')
print('exercises checked:', len(EXS))
print('\n'.join(probs) if probs else 'all good')
sys.exit(1 if probs else 0)
