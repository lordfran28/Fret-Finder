"""Independent checks for solo.py (Debarre, Daussat and Roux's soloing techniques on Очи чёрные): the chords against your
Очи чёрные page, the tune against Hermann's tune as the Очи чёрные page's source has it (read here from its note names),
every note's pitch, string and stroke, and each technique's rule written out again here."""
import sys, re, json
sys.path.insert(0, '/home/claude/studies'); sys.path.insert(0, '/home/claude/studies/gypsy'); sys.path.insert(0, '/home/claude/scripts'); sys.path.insert(0, '/home/claude/oci')
import solo as S
import gtr
import music as OCI

probs = []
def P(m): probs.append(m)
OPENS = [40, 45, 50, 55, 59, 64]
LET = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
def pc(name): return (LET[name[0]] + name.count('♯') + name.count('#') - name.count('♭')) % 12
def midi(s, f): return OPENS[6 - s] + f
def note_midi(n):
    m = re.fullmatch(r'([A-G])(#?)(\d)', n)
    return 12 * (int(m.group(3)) + 1) + LET[m.group(1)] + (1 if m.group(2) else 0)

h = open('/home/claude/fret-finder/songs/ochi-chyornye/index.html').read()
m = re.search(r'"title": "The plain chart".*?"chords": (\[\[.*?\]\]), "tab"', h, flags=re.S)
chart = [b[0]['c'] for b in json.loads(m.group(1))]
changes = chart[0::2]
EXS = {ex['id']: ex for ex in S.SECTIONS[0]['ex']}
want_ids = {'damp', 'triplet', 'sweep', 'roll-acc', 'roll-chords', 'roll-tune', 'chrom', 'harm-art', 'harm-nat', 'octaves'}
if set(EXS) != want_ids: P(f'exercises {sorted(EXS)}')


def labels(it): return it[3][1:].split('|')[0].split(',')


def chord_ok(name, notes_midi):
    return {x % 12 for x in notes_midi} <= gtr.chord_pcs(name)


# rest strokes and sweeping: a note on every string of a root-on-the-low-E grip
for exid, order, arrows in (('damp', [6, 5, 4, 3, 2, 1], '↓' * 6), ('sweep', [6, 5, 4, 3, 2, 1, 2, 3, 4], '↓' * 6 + '↑' * 3)):
    ex = EXS[exid]
    if [B['chords'][0] for B in ex['bars']] != changes: P(f'{exid}: chords')
    for k, B in enumerate(ex['bars']):
        r = B['items'][0]; c = B['chords'][0]
        if [x[0] for x in r[1]] != order: P(f'{exid} bar {k + 1}: strings {[x[0] for x in r[1]]}')
        ms = [midi(*x) for x in r[1]]
        if not chord_ok(c, ms) or min(ms) % 12 != gtr.parse(c)[0] or r[1][0][0] != 6: P(f'{exid} bar {k + 1}: not {c} from the low E string')
        if any(abs(d - 1 / 3) > 1e-9 for d in r[2]): P(f'{exid} bar {k + 1}: not triplets')
        if ''.join(l[-1] for l in labels(r)) != arrows: P(f'{exid} bar {k + 1}: strokes')
        if [pc(l[:-1]) for l in labels(r)] != [x % 12 for x in ms]: P(f'{exid} bar {k + 1}: names')
        if exid == 'damp':
            ch = B['items'][1]
            if ch[0] != 'C' or ch[1] != c or ch[3] != 2.0 or [ch[2][6 - s] for s in order] != [x[1] for x in r[1]]: P(f'{exid} bar {k + 1}: the rolled chord is not the same grip')

# the triplet stroke: A harmonic minor, A4 down to A2 and back, in the 5th position, down-up-down
hm = [x for x in range(45, 70) if x % 12 in {9, 11, 0, 2, 4, 5, 8}]
line = hm[::-1] + hm
got, arrows, frets, durs = [], [], [], []
for B in EXS['triplet']['bars']:
    for it in B['items']:
        if it[0] != 'R': continue
        got += [midi(*x) for x in it[1]]; arrows += [l[-1] for l in labels(it)]; frets += [x[1] for x in it[1]]; durs += it[2]
if got != line: P('triplet: not A harmonic minor down two octaves and back')
if ''.join(arrows) != '↓↑↓' * (len(line) // 3): P('triplet: strokes')
if any(not 4 <= f <= 8 for f in frets): P('triplet: outside the 5th position')
if any(abs(d - 1 / 3) > 1e-9 for d in durs): P('triplet: not triplets')

# rolling: one note faster and faster
for k, (B, s) in enumerate(zip(EXS['roll-acc']['bars'], (6, 5, 4))):
    r = B['items'][0]
    if r[1] != [[s, 0]] * 16: P(f'roll-acc bar {k + 1}: not the open string 16 times')
    if OPENS[6 - s] % 12 != gtr.parse(B['chords'][0])[0]: P(f'roll-acc bar {k + 1}: not the chord’s root')
    d = r[2]
    if abs(sum(d) - 4) > 1e-9 or abs(d[0] - 0.5) > 1e-9: P('roll-acc: length')
    ratios = [b / a for a, b in zip(d[:-2], d[1:-1])]
    if max(ratios) - min(ratios) > 1e-6 or not all(x < 1 for x in ratios): P('roll-acc: not evenly faster')
    if ''.join(l[-1] for l in labels(r)) != '↓↑' * 8: P('roll-acc: strokes')
if [B['chords'][0] for B in EXS['roll-acc']['bars']] != ['E7', 'Am', 'Dm']: P('roll-acc: chords')
# rolling on chords: the first eight bars, the gypsy page's grips, six strokes a beat down and up
GY = {'E7': [-1, 7, 6, 7, 5, -1], 'Am6': [5, -1, 4, 5, 5, -1], 'Dm6': [-1, 5, 7, 4, 6, -1]}
for k, B in enumerate(EXS['roll-chords']['bars']):
    it = B['items'][0]; c = it[1]
    if c.rstrip('6') != chart[k] and c != chart[k]: P(f'roll-chords bar {k + 1}: {c} for {chart[k]}')
    if it[2] != GY.get(c): P(f'roll-chords bar {k + 1}: not the gypsy page’s grip')
    if not chord_ok(c, [OPENS[i] + f for i, f in enumerate(it[2]) if f >= 0]): P(f'roll-chords bar {k + 1}: grip')
    if len(it[3]) != 18 or any(abs(x[0] - 1 / 6) > 1e-9 for x in it[3]): P(f'roll-chords bar {k + 1}: not six a beat')
    if it[4]['up'] != list(range(1, 18, 2)) or ''.join(it[4]['marks']) != '↓↑' * 9: P(f'roll-chords bar {k + 1}: strokes')
# rolling the tune: Hermann's tune an octave above the voice, every note rolled
tune = [(note_midi(n), d) for n, d in OCI.PICKUP] + [(n, d) for bar in OCI.TUNE for n, d in bar]
want, last = [], None
for n, d in tune:
    if n == 'r': want.append(None); continue
    if n == '~': want.append(last + 12); continue
    if isinstance(n, str): n = note_midi(n)
    last = n; want.append(n + 12)
got = []
for k, B in enumerate(EXS['roll-tune']['bars']):
    for it in B['items']:
        if it[0] == 'R':
            if it[4].get('trem') != 6: P(f'roll-tune bar {k + 1}: not rolled')
            got += [midi(*x) for x in it[1]]
            if any(x[1] == 0 or x[0] > 4 for x in it[1]): P(f'roll-tune bar {k + 1}: open string or below the D string')
            if [pc(l) for l in labels(it)] != [midi(*x) % 12 for x in it[1]]: P(f'roll-tune bar {k + 1}: names')
        elif it[0] == 'W': got.append(None)
    if k and B['chords'] != [chart[k - 1]]: P(f'roll-tune bar {k + 1}: chord {B["chords"]}')
if got != want: P('roll-tune: not the tune an octave up')

# chromatics: E2 to A3 by half steps, first position, down and up, then A minor
it0, it1, ch = EXS['chrom']['bars'][0]['items'][0], EXS['chrom']['bars'][1]['items'][0], EXS['chrom']['bars'][1]['items'][1]
ms = [midi(*x) for x in it0[1] + it1[1]]
if ms != list(range(40, 58)): P('chrom: not E to A by half steps')
if any(not 0 <= x[1] <= 4 for x in it0[1] + it1[1]): P('chrom: outside the first position')
if ''.join(l[-1] for l in labels(it0) + labels(it1)) != '↓↑' * 9: P('chrom: strokes')
if ch[0] != 'C' or ch[1] != 'Am' or not chord_ok('Am', [OPENS[i] + f for i, f in enumerate(ch[2]) if f >= 0]): P('chrom: the end')

# harmonics
for k, B in enumerate(EXS['harm-art']['bars']):
    for it, c in zip(B['items'], B['chords']):
        if it[4].get('harm') is not True: P('harm-art: not marked as harmonics')
        g = GY.get(c)
        if g is None or it[1] != [[6 - i, f] for i, f in enumerate(g) if f >= 0]: P(f'harm-art bar {k + 1}: not {c}’s grip')
        if [pc(l) for l in labels(it)] != [(midi(*x) + 12) % 12 for x in it[1]]: P('harm-art: names')
if [c.rstrip('6') for B in EXS['harm-art']['bars'] for c in B['chords']] != changes: P('harm-art: chords')
for k, B in enumerate(EXS['harm-nat']['bars']):
    it, ch = B['items']; c = B['chords'][0]
    if it[4].get('harm') != 'nat' or any(x[1] != 12 for x in it[1]): P('harm-nat: not 12th-fret natural harmonics')
    want_s = sorted(s for s in range(1, 7) if OPENS[6 - s] % 12 in gtr.chord_pcs(c) and not (c == 'Dm' and s in (6, 1)) and not (c == 'Am' and s == 4))
    if sorted(x[0] for x in it[1]) != want_s and sorted(x[0] for x in it[1]) != [s for s in want_s]: P(f'harm-nat bar {k + 1}: strings {sorted(x[0] for x in it[1])} vs {want_s}')
    if any(OPENS[6 - x[0]] % 12 not in gtr.chord_pcs(c) for x in it[1]): P(f'harm-nat bar {k + 1}: a harmonic outside {c}')
    if not chord_ok(c, [OPENS[i] + f for i, f in enumerate(ch[2]) if f >= 0]): P('harm-nat: chord')

# octaves: the tune where it is sung, doubled an octave up, one string between
want = [(n if not isinstance(n, str) else n) for n in want]
got = []
for k, B in enumerate(EXS['octaves']['bars']):
    for it in B['items']:
        if it[0] == 'P':
            for g in it[1]:
                (s1, f1), (s2, f2) = sorted(g, key=lambda x: -x[0])
                if s1 - s2 != 2 or min(f1, f2) < 1: P(f'octaves bar {k + 1}: not one string between, or open')
                if midi(s2, f2) - midi(s1, f1) != 12: P(f'octaves bar {k + 1}: not an octave')
                got.append(midi(s1, f1) + 12)
        elif it[0] == 'W': got.append('w')
tied = [w for w in want]
if [x for x in got if x != 'w'] != [x for x, (n, d) in zip(want, tune) if x is not None and n != '~']: P('octaves: not the tune')
print('exercises checked:', len(EXS))
print('\n'.join(probs) if probs else 'all good')
sys.exit(1 if probs else 0)
