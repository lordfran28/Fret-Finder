"""Independent checks for romane2.py (L'Esprit Manouche, part A of chapters 5–9). Their tabs and diagrams are written out
again here as note names on strings, as read from the book (pp. 41–75), so a misread fret in romane2.py shows up as a wrong
pitch; ours must be theirs moved whole along the neck by the stated number of frets on the same strings; every note must
belong to the chord or scale it is over; the bars must play the notes in the order and rhythm described; strokes,
names and quotes are checked; the song's chords and bars the text names must match your page."""
import sys, re, json
sys.path.insert(0, '/home/claude/studies'); sys.path.insert(0, '/home/claude/studies/gypsy'); sys.path.insert(0, '/home/claude/scripts')
import romane2 as R
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
    'brk': ('F2/6 G♯2/6 F2/6 G♯2/6 B2/5 G♯2/6 B2/5 D3/5 B2/5 D3/5 F3/4 D3/5 F3/4 G♯3/4 F3/4 G♯3/4 '
            'B3/3 G♯3/4 B3/3 D4/3 B3/3 D4/3 F4/2 D4/3 F4/2 G♯4/2 F4/2 G♯4/2 B4/1 G♯4/2 B4/1 D5/1'),
    'maj7': 'F♯2/6 G2/6 B2/5 D3/5 F♯3/4 G3/4 B3/3 D4/3 F♯4/2 G4/2 B4/1 D5/1 D5/1 B4/1 G4/2 F♯4/2 D4/3 B3/3 G3/4 F♯3/4 D3/5 B2/5 G2/6 F♯2/6',
    'sw1': 'F♯3/4 G3/4 B3/3 D4/2 F♯4/2 D4/2 B3/3 G3/4',
    'sw2': 'G♯3/4 A3/4 C4/3 E4/2 G4/2 E4/2 C4/3 A3/4',
    'c6': 'B2/6 C3/6 D♯3/5 E3/5 F♯3/4 G3/4 B3/3 C4/3 D♯4/2 E4/2 G♯4/1 A4/1',
    'wt1': 'B2/6 C♯3/6 D♯3/5 F3/5 G3/4 A3/4 B3/3 C♯4/3 D♯4/2 F4/2 G4/1 A4/1 B4/1',
    'wt2': 'G2/6 A2/6 B2/6 C♯3/5 D♯3/5 F3/5 G3/4 A3/4 B3/4 C♯4/3 D♯4/3 F4/3 G4/2 A4/2 B4/2 C♯5/1 D♯5/1 F5/1 G5/1',
    'add9': 'G2/6 A2/6 B2/6 D3/5 G3/4 A3/4 B3/4 D4/3 G4/2 A4/2 B4/1 D5/1 E5/1',
    'diat': ('G3/4 B3/3 D4/2 G4/1 A4/1 F♯4/2 C4/3 A3/4 B3/4 D4/3 G4/2 B4/1 C5/1 A4/2 E♭4/3 C4/4 '
             'B3/4 D4/3 G4/2 B4/1 A4/1 F♯4/2 C4/3 A3/4 G3/4'),
    'sus': 'G2/6 D3/5 F3/4 C4/3 D4/2 A4/1 D4/2 C4/3 F3/4 D3/5 G2/6',
    'anat1': 'C3/5 A2/6 D3/5 G2/6 C3/5',
    'anat2': 'F3/6 D3/6 G3/5 C3/6 F3/5',
    'circ': 'E3/6 A3/5 D3/6 G3/5 C3/6 F3/5 B♭2/6 E♭3/5 A♭2/6 D♭3/5 F♯2/6 B2/5 E2/6',
    'trit': 'A2/6 E♭3/5 A3/4 E♭3/5 A3/4 E♭4/3',
    'wtt': 'A3/5 E♭4/4 A4/3 G4/3 C♯4/4 G3/5 F3/5 B3/4 F4/3 E♭4/3 A3/4 E♭3/5 C♯3/5 G3/4 C♯4/3 B3/3 F3/4 B2/5 A2/5',
    'b5': 'G2/6 C♯3/5 F3/4 B3/3 D4/2 G♯4/1 D4/2 B3/3 F3/4 C♯3/5 G2/6',
    'dmsw': 'D4/3 F4/2 A4/1 D5/1 A4/1 F4/2 D4/3 F4/2 A4/1 C♯5/1 A4/1 F4/2 D4/3 F4/2 A4/1 C5/1 A4/1 F4/2',
}
# the move into the song's keys: A minor and C major up a fret, G major down a fret, G7 (C major's V) up a fret; the tritone
# three frets up (A–E♭ to C–G♭, A♭7's 3rd and 7th)
MOVE = {'brk': 1, 'maj7': -1, 'sw1': -1, 'sw2': -1, 'c6': 1, 'wt1': 1, 'wt2': 1, 'add9': -1, 'diat': -1, 'sus': 1,
        'anat1': 1, 'anat2': 1, 'circ': 1, 'trit': 3, 'wtt': 1, 'b5': 1, 'dmsw': 1}
WT = {0, 2, 4, 6, 8, 10}
def pcs(*names): return {pc(x) for x in names}
ALLOW = {'brk': pcs('G♭', 'A', 'C', 'E♭'), 'maj7': pcs('G♭', 'B♭', 'D♭', 'F'), 'sw1': pcs('G♭', 'B♭', 'D♭', 'F'),
         'sw2': pcs('A♭', 'C♭', 'E♭', 'G♭', 'G'), 'c6': pcs('D♭', 'F', 'A♭', 'B♭', 'C', 'E', 'G', 'A'), 'wt1': WT, 'wt2': WT,
         'add9': pcs('G♭', 'A♭', 'B♭', 'D♭', 'E♭'), 'sus': pcs('A♭', 'D♭', 'E♭', 'G♭', 'B♭'),
         'anat1': pcs('D♭', 'B♭', 'E♭', 'A♭'), 'anat2': pcs('G♭', 'E♭', 'A♭', 'D♭'), 'circ': set(range(12)), 'trit': pcs('C', 'G♭'),
         'wtt': WT, 'b5': pcs('A♭', 'C', 'D', 'G♭', 'E♭', 'A'), 'dmsw': pcs('E♭', 'G♭', 'B♭', 'D', 'D♭'),
         'diat': set(range(12))}

for key, txt in BOOK.items():
    toks = [t.split('/') for t in txt.split()]
    want = [(int(s), nm(n) - OPENS[6 - int(s)]) for n, s in toks]
    if any(not 0 <= f <= 15 for s, f in want): P(f'{key}: a note of theirs is not on its string')
    if list(R.THEIRS[key]) != want:
        k = next((i for i, (a, b) in enumerate(zip(R.THEIRS[key], want)) if a != b), min(len(want), len(R.THEIRS[key])))
        P(f'{key}: their notes differ from the book at {k + 1}')
    ours = R.ours(key)
    if ours != [(s, f + MOVE[key]) for s, f in want]: P(f'{key}: ours is not theirs moved {MOVE[key]:+d}')
    if any(f < 1 or f > 16 for s, f in ours): P(f'{key}: ours has an open string or a fret above the 16th')
    if any(at(s, f) % 12 not in ALLOW[key] for s, f in ours): P(f'{key}: a note of ours outside its chord or scale')
# their notes against their chords, for the readings that have a chord
THEIR_ALLOW = {'brk': pcs('F', 'G♯', 'B', 'D'), 'maj7': pcs('G', 'B', 'D', 'F♯'), 'wt1': {(x - 1) % 12 for x in WT}, 'wt2': {(x - 1) % 12 for x in WT},
               'wtt': {(x - 1) % 12 for x in WT}, 'sus': pcs('G', 'C', 'D', 'F', 'A'), 'b5': pcs('G', 'B', 'C♯', 'F', 'D', 'G♯'),
               'c6': pcs('C', 'E', 'G', 'A', 'B', 'D♯', 'F♯', 'G♯'), 'dmsw': pcs('D', 'F', 'A', 'C♯', 'C')}
for key, al in THEIR_ALLOW.items():
    if any(nm(t.split('/')[0]) % 12 not in al for t in BOOK[key].split()): P(f'{key}: a note of theirs outside their chord')
# the diatonic sweeps, half a bar at a time, against their chords (with the 6th the line takes)
DI = ['Gb', 'Abm6', 'Gb/Bb', 'Cbm6', 'Gb', 'Db7']
for k, c in enumerate(DI):
    for s, f in R.ours('diat')[4 * k:4 * k + 4]:
        if at(s, f) % 12 not in gtr.chord_pcs(c): P(f'diat: a note outside {c}')

EXS = {ex['id']: ex for S in R.SECTIONS[len(R.R1.SECTIONS):] for ex in S['ex']}
want_ids = {'brk', 'maj7', 'sw1', 'sw2', 'sw3', 'c6', 'wt1', 'wt2', 'add9', 'diat', 'sus', 'anat', 'circ', 'trit', 'wtt', 'b5', 'dmsw'}
if set(EXS) != want_ids: P(f'exercises {sorted(EXS)}')


def flat(ex):
    notes, durs, labs, bars = [], [], [], []
    for B in ex['bars']:
        L = 0
        for it in B['items']:
            if it[0] == 'R':
                notes += [tuple(x) for x in it[1]]; durs += it[2]; labs += it[3][1:].split('|')[0].split(','); L += sum(it[2])
            elif it[0] == 'W': L += it[1]
        bars.append(L)
    return notes, durs, labs, bars


def up_down(x): return list(x) + list(x[-2::-1])


O = R.ours
EXPECT = {   # id: (notes, durations, bar lengths)
    'brk': (O('brk') + O('brk')[::-1], [0.5] * 64, [4] * 8),
    'maj7': (O('maj7'), [0.5] * 23 + [2.5], [4, 4, 8]),
    'sw1': (O('sw1') * 2, [0.5] * 16, [4, 4]),
    'sw2': (O('sw2') * 2, [0.5] * 16, [4, 4]),
    'sw3': (O('sw1') + O('sw2') + [(s, f + 2) for s, f in O('sw2')] + [(s, f + 5) for s, f in O('sw1')], [0.5] * 32, [4] * 4),
    'c6': (up_down(O('c6')) + [O('c6')[2 * p - 2 + h] for p in (1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1, 2, 3, 4, 5, 6) for h in (0, 1)],
           [0.5] * 22 + [1] + [0.5] * 32, [4] * 7),
    'wt1': (up_down(O('wt1')) * 2, [0.5] * 24 + [3] + [1 / 3] * 24 + [4], [3] * 5 + [4] * 3),
    'wt2': (up_down(O('wt2')) * 2, [0.5] * 36 + [3] + [1 / 3] * 36 + [4], [3] * 7 + [4] * 4),
    'add9': (O('add9'), [0.5] * 12 + [1], [4, 4]),
    'diat': (O('diat'), [0.5] * 24 + [2], [4] * 4),
    'sus': (O('sus'), [0.5] * 10 + [1], [2] * 3),
    'anat': (O('anat1') + O('anat2'), [1] * 4 + [4] + [1] * 4 + [4], [4] * 4),
    'circ': (O('circ'), [1] * 12 + [4], [4] * 4),
    'trit': (up_down(O('trit')), [0.5] * 10 + [3], [4, 4]),
    'wtt': (O('wtt'), [1 / 3] * 18 + [2], [4, 4]),
    'b5': (O('b5'), [0.5] * 10 + [1], [2] * 3),
    'dmsw': (O('dmsw'), [1 / 3] * 18, [2] * 3),
}
MARKS = {'sw1': '↓h↓↓↑↑↑↑p↓↓↓↑↑↑↑'.replace('p↓↓↓', 'ph↓↓'), 'sw2': '↓h↓↓↑↑↑↑ph↓↓↑↑↑↑', 'sw3': '↓h↓↓↑↑↑↑' + 'ph↓↓↑↑↑↑' * 3,
         'sus': '↓' * 6 + '↑' * 5, 'b5': '↓' * 6 + '↑' * 5, 'dmsw': '↓↓↓↓↑↑' * 3, 'diat': '↓↓↓↓↑↑↑↑' * 3, 'wtt': '↓↓↓↑↑↑' * 3}
for key, (n_, d_, b_) in EXPECT.items():
    ex = EXS[key]
    notes, durs, labs, bars = flat(ex)
    if notes != [tuple(x) for x in n_]: P(f'{key}: not the notes in the order described')
    if len(durs) != len(d_) or any(abs(a - b) > 1e-9 for a, b in zip(durs, d_)): P(f'{key}: rhythm')
    if len(bars) != len(b_) or any(abs(a - b) > 1e-9 for a, b in zip(bars, b_)): P(f'{key}: bar lengths {bars}')
    base = [re.sub(r'[↓↑hp*]', '', x) for x in labs]
    if [pc(x) for x in base] != [at(s, f) % 12 for s, f in notes]: P(f'{key}: a name does not match its note')
    if any('♯' in x for x in base): P(f'{key}: a sharp among flat keys')
    if key in MARKS:
        got = ''.join(re.sub(r'[^↓↑hp]', '', x) for x in labs)
        if got != MARKS[key]: P(f'{key}: strokes {got}')
# the hammered and pulled notes sound softer than the struck ones
for key in ('sw1', 'sw2', 'sw3'):
    for B in EXS[key]['bars']:
        it = B['items'][0]
        for l, v in zip(it[3][1:].split('|')[0].split(','), it[4]['vel']):
            if ('h' in l or 'p' in l) != (v < 0): P(f'{key}: a hammer or pull-off not softened')
# the c6 line marks the chord's notes with *
c6labs = flat(EXS['c6'])[2][23:]
if [('*' in x) for x in c6labs] != [False, True] * 16: P('c6: the chord notes are not the starred ones')
# chords over the bars
CH = {'brk': {('Gbdim7',)}, 'maj7': {('Gbmaj7',)}, 'sw1': {('Gbmaj7',)}, 'sw2': {('Abm7',)}, 'c6': {('Db6',)}, 'wt1': {('Ab7#5',)},
      'wt2': {('Ab7#5',)}, 'add9': {('Gbadd9',)}, 'sus': {('Ab7sus4',)}, 'trit': {('Ab7',)}, 'wtt': {('Bb7',)}, 'b5': {('Ab7b5',)}, 'dmsw': {('Ebm',)}}
for key, want in CH.items():
    if {tuple(B['chords']) for B in EXS[key]['bars']} != want: P(f'{key}: chords {[B["chords"] for B in EXS[key]["bars"]]}')
if [B['chords'] for B in EXS['sw3']['bars']] != [['Gbmaj7'], ['Abm7'], ['Bbm7'], ['Cbmaj7']]: P('sw3: chords')
if [B['chords'] for B in EXS['diat']['bars']] != [['Gb', 'Abm6'], ['Gb/Bb', 'Cbm6'], ['Gb', 'Db7'], ['Gb']]: P('diat: chords')
for k, (B, c) in enumerate(zip(EXS['sw3']['bars'], ['Gbmaj7', 'Abm7', 'Bbm7', 'Cbmaj7'])):
    al = gtr.chord_pcs(c) | {(gtr.parse(c)[0] - 1) % 12}
    if any(at(*x) % 12 not in al for x in B['items'][0][1]): P(f'sw3 bar {k + 1}: a note outside {c} and its approach')
# quotes: their own first notes, a beat or two
for key, ex in EXS.items():
    q = ex['quote']
    if not q.get('items'): continue
    it = q['items'][0]
    src = {'anat': 'anat1'}.get(key, key)
    if [tuple(x) for x in it[1]] != R.THEIRS[src][:len(it[1])] or sum(it[2]) > 2 + 1e-9: P(f'{key}: the quote')
    if [pc(x) for x in it[3][1:].split('|')[0].split(',')] != [at(s, f) % 12 for s, f in it[1]]: P(f'{key}: the quote’s names')
# the song: chord names followed by 'bars ...' in the texts must be in those bars of your page
h = open('/home/claude/fret-finder/songs/it-had-to-be-you/index.html').read()
i = h.find('"chorus": [')
chorus, _ = json.JSONDecoder().raw_decode(h[i + len('"chorus": '):])
where = {}
for b in chorus:
    for sg in b['segs']: where.setdefault(sg['c'], set()).add(int(b['lab']))
def expand(t):
    out = set()
    for part in re.split(r',\s*|\s+and\s+', t):
        part = part.strip()
        if part:
            a, _, b = part.partition('–'); out |= set(range(int(a), int(b or a) + 1))
    return out
n_claims = 0
for ex in EXS.values():
    txt = ex['idea'] + ' ' + ' '.join(B['note'] for B in ex['bars'])
    for c in sorted(where, key=len, reverse=True):
        for m in re.finditer(re.escape(c) + r'(?![♭♯0-9a-z])', txt):
            mm = re.match(r'[^.;]{0,40}?bars? ([\d–]+(?:(?:,\s*| and )[\d–]+)*)', txt[m.end():])
            if mm and not re.search(r'[A-G][♭♯]?(?:m|maj|7|9|13|6)', txt[m.end():m.end() + mm.start(1)]):
                n_claims += 1
                if not expand(mm.group(1)) <= where[c]: P(f'{ex["id"]}: the text puts {c} in bars {mm.group(1)}; your page has it in {sorted(where[c])}')
if n_claims < 6: P(f'only {n_claims} song claims found')
print('exercises checked:', len(EXS), '· song claims:', n_claims)
print('\n'.join(probs) if probs else 'all good')
sys.exit(1 if probs else 0)
