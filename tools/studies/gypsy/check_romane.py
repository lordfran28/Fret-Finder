"""Independent checks for romane.py (L'Esprit Manouche, part A of chapters 1–4, moved into It Had to Be You's B♭ minor).
Their diagrams are written out again here as note names on strings, as read from the book (pp. 9–34), so a misread
fret in romane.py shows up as a wrong pitch; ours must be theirs moved up the given number of frets on the same
strings; every note must belong to the chord or scale it is over; the bars must play the numbers up and back down in
the stated rhythm; note names must match the notes; the song's chords named in the text must be in your page's chart."""
import sys, re, json
sys.path.insert(0, '/home/claude/studies'); sys.path.insert(0, '/home/claude/studies/gypsy'); sys.path.insert(0, '/home/claude/scripts')
import romane as R
import gtr

probs = []
def P(m): probs.append(m)
OPENS = [40, 45, 50, 55, 59, 64]
LET = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
def pc(n): return (LET[n[0]] + n.count('♯') - n.count('♭')) % 12
def nm(n):
    m = re.fullmatch(r'([A-G])([♯♭]?)(\d)', n)
    return 12 * (int(m.group(3)) + 1) + LET[m.group(1)] + (m.group(2) == '♯') - (m.group(2) == '♭')

# their diagrams: note/string, in the order of their numbers
BOOK = {
    'am':   'A2/5 C3/5 E3/4 A3/3 C4/2 E4/1 A4/1 E4/2 C4/3 A3/4 E3/5 C3/6 A2/6 C3/6 E3/5 A3/4 C4/4 E4/3 A4/2 C5/1 E5/1',
    'dm':   'D3/4 F3/4 A3/3 D4/2 F4/1 A4/1 F4/2 D4/3 A3/4 F3/5 D3/5 F3/5 A3/4 D4/3 F4/3 A4/2 D5/1 A4/2 F4/3 D4/4 A3/5 F3/6 D3/6',
    'dim':  'F2/6 A♭2/6 B2/5 D3/5 F3/4 A♭3/4 B3/3 D4/3 F4/2 A♭4/2 B4/1 D5/1',
    'dim7': 'A2/6 C♯3/5 E3/5 G3/4 B♭3/4 C♯4/3 E4/3 G4/2 B♭4/2 C♯5/1 E5/1',
    'maj1': 'B♭2/5 D3/5 F3/4 B♭3/3 D4/2 F4/2 B♭4/1 F4/2 D4/3 B♭3/4 F3/5 D3/5 B♭2/6 D3/6 F3/5 B♭3/4 D4/4 F4/3 B♭4/2 D5/1 F5/1',
    'maj2': 'E2/6 G♯2/6 B2/6 E3/5 G♯3/4 B3/3 E4/2 G♯4/1 B4/1',
    'hm':   'A2/6 B2/6 C3/6 D3/5 E3/5 F3/5 G♯3/4 A3/4 B3/3 C4/3 D4/3 E4/2 F4/2 G♯4/1 A4/1',
    'hm2':  'A2/6 B2/6 C3/6 D3/5 E3/5 F3/5 G♯3/4 A3/4 B3/4 C4/4 D4/3 E4/3 F4/3 G♯4/2 A4/2 B4/1 C5/1 D5/1',
    'm6a':  'A2/6 C3/6 E3/5 F♯3/4 A3/4 C4/3 E4/2 F♯4/2 A4/1 C5/1',
    'm6b':  'E3/6 F♯3/6 A3/5 C4/5 E4/4 F♯4/3 A4/3 C5/2 E5/1 F♯5/1',
    'm9a':  'A2/6 B2/6 C3/6 E3/5 A3/4 B3/4 C4/4 E4/3 A4/2 B4/2 C5/2 E5/1',
    'm9b':  'A2/5 B2/5 C3/5 E3/4 A3/3 B3/3 C4/3 E4/2 A4/1',
    'sp1':  'C5/1 B4/1 A4/1 G4/2 F♯4/2 E4/2',
    'sp2':  'B4/1 A4/1 G4/1 F♯4/2 E4/2 D4/2',
    'chrom': 'E2/6 F2/6 F♯2/6 G2/6 G♯2/6 A2/5 A♯2/5 B2/5 C3/5 C♯3/5 D3/4 D♯3/4 E3/4 F3/4 F♯3/4 G3/3 G♯3/3 A3/3 A♯3/3 '
             'B3/2 C4/2 C♯4/2 D4/2 D♯4/2 E4/1 F4/1 F♯4/1 G4/1 G♯4/1',
}
THEIR_CHORD = {'am': 'Am', 'dm': 'Dm', 'dim': 'Fdim7', 'dim7': 'A7b9', 'maj1': 'Bb', 'maj2': 'E', 'm6a': 'Am6', 'm6b': 'Am6',
               'm9a': 'Am(add9)', 'm9b': 'Am(add9)'}
SCALES = {'hm': {9, 11, 0, 2, 4, 5, 8}, 'hm2': {9, 11, 0, 2, 4, 5, 8}, 'sp1': {9, 11, 0, 2, 4, 6, 7}, 'sp2': {7, 9, 11, 0, 2, 4, 6}}
OUR_CHORD = {'am': 'Bbm', 'dm': 'Ebm', 'dim': 'Gbdim7', 'dim7': 'Bb7b9', 'maj1': 'Cb', 'maj2': 'F', 'hm': 'Bbm', 'hm2': 'Bbm',
             'm6a': 'Bbm6', 'm6b': 'Bbm6', 'm9a': 'Bbm(add9)', 'm9b': 'Bbm(add9)', 'sp1': 'Bbm6/9', 'sp2': 'Ab6/9', 'chrom': None}
UP = {k: (0 if k == 'chrom' else 1) for k in BOOK}
# the songs' chords each exercise's text names, and the bars it names them in
SONG_CLAIMS = [('Bbm7', [5, 6, 7, 11, 12, 13, 21, 22, 23, 28]), ('Ebm9', [15, 32]), ('F7b9', [10, 27]), ('Bb9', [3, 4, 19, 20]),
               ('Cb9', [2, 18, 26]), ('F7', [10, 11, 12, 27])]

for key, txt in BOOK.items():
    want = []
    for tok in txt.split():
        n, s = tok.split('/'); s = int(s)
        f = nm(n) - OPENS[6 - s]
        if not 0 <= f <= 15: P(f'{key}: {tok} is not on its string in the first 15 frets')
        want.append((s, f))
    if list(R.THEIRS[key]) != want:
        k = next((i for i, (a, b) in enumerate(zip(R.THEIRS[key], want)) if a != b), min(len(want), len(R.THEIRS[key])))
        P(f'{key}: their diagram differs from the book at number {k + 1}')
    # their notes fit their chord or scale
    if key in THEIR_CHORD and any(nm(t.split('/')[0]) % 12 not in gtr.chord_pcs(THEIR_CHORD[key]) for t in txt.split()): P(f'{key}: a note of theirs outside {THEIR_CHORD[key]}')
    if key in SCALES and any(nm(t.split('/')[0]) % 12 not in SCALES[key] for t in txt.split()): P(f'{key}: a note of theirs outside the scale')
    # ours: theirs moved up on the same strings
    ours = R.ours(key)
    if ours != [(s, f + UP[key]) for s, f in want]: P(f'{key}: ours is not theirs moved up {UP[key]} fret(s)')
    if key != 'chrom' and any(f < 1 or f > 16 for s, f in ours): P(f'{key}: ours has an open string or a fret above the 16th')
    oc = OUR_CHORD[key]
    pcs = (gtr.chord_pcs(oc) if key not in SCALES else {(x + 1) % 12 for x in SCALES[key]}) if oc else set()
    if oc and any((OPENS[6 - s] + f) % 12 not in pcs for s, f in ours): P(f'{key}: a note of ours outside {oc}')
    # a whole-diagram move keeps every interval
    a = [OPENS[6 - s] + f for s, f in ours]; b = [nm(t.split('/')[0]) for t in txt.split()]
    if [x - y for x, y in zip(a, b)] != [UP[key]] * len(b): P(f'{key}: an interval changed')

EXS = {ex['id']: ex for S in R.SECTIONS for ex in S['ex']}
if set(EXS) != set(BOOK): P(f'exercises {sorted(EXS)}')


def runs(ex):
    notes, durs, names, chords = [], [], [], []
    for B in ex['bars']:
        if abs(sum(sum(it[2]) if it[0] == 'R' else it[3] for it in B['items']) - 4) > 1e-9: P(f'{ex["id"]}: a bar is not four beats')
        for it in B['items']:
            if it[0] == 'R':
                notes += [tuple(x) for x in it[1]]; durs += it[2]; names += it[3][1:].split('|')[0].split(',')
                chords.append(tuple(B['chords']))
    return notes, durs, names, chords


for key, ex in EXS.items():
    ours = R.ours(key) if key != 'chrom' else R.THEIRS['chrom']
    notes, durs, names, chords = runs(ex)
    if [pc(n) for n in names] != [(OPENS[6 - s] + f) % 12 for s, f in notes]: P(f'{key}: a note name does not match its note')
    oc = OUR_CHORD[key]
    if oc and set(chords) != {(oc,)}: P(f'{key}: the bars are over {set(chords)}, not {oc}')
    if key in ('sp1', 'sp2'):
        if notes != ours * 8 or any(abs(d - 1 / 3) > 1e-9 for d in durs): P(f'{key}: not the six notes eight times in triplets')
        cs = [it for B in ex['bars'] for it in B['items'] if it[0] == 'C']
        for c in cs:
            g = c[2]
            if c[1] != oc or {(OPENS[i] + x) % 12 for i, x in enumerate(g) if x >= 0} != gtr.chord_pcs(oc) or (OPENS[0] + g[0]) % 12 != gtr.parse(oc)[0]:
                P(f'{key}: the chord is not {oc} with its root on the low E string')
            if g != [x + 1 for x in R.GRIP_THEIRS[key]]: P(f'{key}: the chord is not theirs a fret up')
        continue
    want = ours + ours[-2::-1]
    if key == 'chrom':
        if notes != want + want: P('chrom: not up and down twice (eighths, then triplets)')
        n = len(want)
        if durs[:n - 1] != [0.5] * (n - 1) or any(abs(d - 1 / 3) > 1e-9 for d in durs[n:-1]): P('chrom: rhythm')
        if any(any(c in x for c in '♭') for x in names[:len(ours)]) or any('♯' in x for x in names[len(ours):n]): P('chrom: sharps up, flats down')
        continue
    if notes != want: P(f'{key}: not up the numbers and back down')
    if durs[:-1] != [0.5] * (len(durs) - 1): P(f'{key}: not eighths')
    if key not in ('chrom',) and any('♯' in x for x in names): P(f'{key}: a sharp in B♭ minor')

# quotes: their first notes, unmoved
for key, ex in EXS.items():
    q = ex['quote']['items'][0]
    n = len(q[1])
    if [tuple(x) for x in q[1]] != R.THEIRS[key][:n] or not 3 <= n <= 4 or sum(q[2]) > 2: P(f'{key}: the quote is not their first beat or two')
    if [pc(x) for x in q[3][1:].split('|')[0].split(',')] != [(OPENS[6 - s] + f) % 12 for s, f in q[1]]: P(f'{key}: the quote’s names')

# fingers: on each string the frets rise with the fingers
for key, fs in R.FING.items():
    seq = R.ours(key) if key != 'chrom' else R.THEIRS['chrom']
    if len(fs) != len(seq): P(f'{key}: {len(fs)} fingers for {len(seq)} notes'); continue
    for (s1, f1), (s2, f2), a, b in zip(seq, seq[1:], fs, fs[1:]):
        if s1 == s2 and f2 > f1 and b and a and b < a: P(f'{key}: fingers go backwards on string {s1}')
        if s1 == s2 and a and b and b > a and f2 - f1 < b - a - 1: P(f'{key}: fingers {a}, {b} crowded on {f1}, {f2}')
    if key == 'chrom' and any((f == 0) != (x == 0) or (f and x != f) for (s, f), x in zip(seq, fs)): P('chrom: not a finger per fret')

# the song: the chords and bars the text names
h = open('/home/claude/fret-finder/songs/it-had-to-be-you/index.html').read()
i = h.find('"chorus": [')
chorus, _ = json.JSONDecoder().raw_decode(h[i + len('"chorus": '):])
where = {}
for b in chorus:
    for sg in b['segs']:
        nmz = sg['c'].replace('♭', 'b').replace('♯', '#')
        where.setdefault(nmz, set()).add(int(b['lab']))
for c, bars in SONG_CLAIMS:
    if c == 'F7':
        got = set().union(*[where.get(x, set()) for x in ('F7b9', 'F7#5')])
    else:
        got = where.get(c, set())
    if set(bars) != got: P(f'song: {c} is in bars {sorted(got)}, the text says {bars}')
# every 'CHORD ... bars N–M' the text names must match the song
DISP = {'Bbm7': 'B♭m7', 'Ebm9': 'E♭m9', 'F7b9': 'F7♭9', 'Bb9': 'B♭9', 'Cb9': 'C♭9', 'F7': 'F7 '}
def expand(t):
    out = set()
    for part in re.split(r',\s*|\s+and\s+', t):
        part = part.strip()
        if not part: continue
        a, _, b = part.partition('–')
        out |= set(range(int(a), int(b or a) + 1))
    return out
claimed = 0
for ex in EXS.values():
    txt = ex['idea'] + ' ' + ' '.join(B['note'] for B in ex['bars'])
    for c, bars in SONG_CLAIMS:
        for m in re.finditer(re.escape(DISP[c]), txt):
            mm = re.match(r'[^.;]{0,40}?bars? ([\d–]+(?:(?:,\s*| and )[\d–]+)*)', txt[m.end():])
            if mm:
                claimed += 1
                if not expand(mm.group(1)) <= set(bars): P(f'{ex["id"]}: the text puts {DISP[c]} in bars {mm.group(1)}; the song has it in {bars}')
if claimed < 6: P(f'only {claimed} of the song claims found in the text')
print('exercises checked:', len(EXS))
print('\n'.join(probs) if probs else 'all good')
sys.exit(1 if probs else 0)
