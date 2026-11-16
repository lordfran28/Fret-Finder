"""Independent checks for manouche.py (Wrembel's accompanist's chords): every grip read back from the page's items is the
chord it is named (all its required tones, nothing outside it, the right bass), playable by the rules written out
again here, the same grip wherever the chord comes back; each exercise does what Wrembel's rule says; and the song
bars are the ones on your Очи чёрные and Я вас любил pages."""
import sys, re, json
sys.path.insert(0, '/home/claude/studies'); sys.path.insert(0, '/home/claude/studies/gypsy'); sys.path.insert(0, '/home/claude/scripts')
import manouche as C
import gtr

OPENS = [40, 45, 50, 55, 59, 64]
probs = []


def P(m): probs.append(m)


def notes(g): return [OPENS[i] + f for i, f in enumerate(g) if f >= 0]


def playable(g):
    fr = [(i, f) for i, f in enumerate(g) if f > 0]
    if any(f == 0 for f in g): return 'an open string'
    lo, hi = min(f for _, f in fr), max(f for _, f in fr)
    if hi - lo + 1 > (5 if lo >= 7 else 4): return f'stretch {lo}-{hi}'
    # fingers: a first-finger barre across every string between its outer notes counts once
    at = [i for i, f in fr if f == lo]
    n = len(fr)
    if len(at) > 1 and all(g[i] >= lo for i in range(min(at), max(at) + 1)): n -= len(at) - 1
    if n > 4: return f'{n} fingers'
    b = next(i for i, f in enumerate(g) if f >= 0)
    if g[b] > min(f for i, f in fr if i != b) + 2: return 'the bass is out of reach'
    return None


def is_chord(name, g):
    root, q, bass = gtr.parse(name)
    req, opt = gtr.QUAL[q]
    pcs = {m % 12 for m in notes(g)}
    allowed = {(root + i) % 12 for i in req | opt} | ({bass} if bass is not None else set())
    need = {(root + i) % 12 for i in req} | ({bass} if bass is not None else set())
    if q != 'dim7': need |= {root}
    low = min(notes(g)) % 12
    if not need <= pcs: return f'missing {sorted(need - pcs)}'
    if not pcs <= allowed: return f'foreign {sorted(pcs - allowed)}'
    if low != (bass if bass is not None else root): return 'wrong bass'
    return None


EXS = {ex['id']: ex for ex in C.SECTION['ex']}
seen = {}
items = {}
for exid, ex in EXS.items():
    seq = []
    for j, B in enumerate(ex['bars']):
        beats = 0
        for it in B['items']:
            if it[0] != 'K': P(f'{exid} bar {j + 1}: not a chord'); continue
            name, g, hits = it[1], it[2], it[3]
            beats += sum(h[0] for h in hits)
            e = is_chord(name, g)
            if e: P(f'{exid} bar {j + 1} {name} {g}: {e}')
            e = playable(g)
            if e: P(f'{exid} bar {j + 1} {name} {g}: {e}')
            if name in seen and seen[name] != g: P(f'{name} gripped two ways: {seen[name]} and {g}')
            seen.setdefault(name, g)
            seq.append((name, g))
        if abs(beats - 4) > 1e-9: P(f'{exid} bar {j + 1}: {beats} beats')
        # la pompe: beats 1 and 3 squashed (half a beat, then silence), 2 and 4 whipped (a quarter of a beat, lighter)
        flat = [h for it in B['items'] for h in it[3]]
        want_p = []
        for k in range(4):
            want_p += [(0.5, True, 0), (0.5, False, 0)] if k % 2 == 0 else [(0.25, True, -0.05), (0.75, False, 0)]
        got = [(h[0], h[1] != '-', h[2] if len(h) > 2 else 0) for h in flat]
        if len(got) != len(want_p) or any(abs(a[0] - b[0]) > 1e-9 or a[1] != b[1] or abs(a[2] - b[2]) > 1e-9 for a, b in zip(got, want_p)):
            P(f'{exid} bar {j + 1}: not la pompe')
        if B['chords'] != [it[1] for it in B['items']]: P(f'{exid} bar {j + 1}: chord list')
    items[exid] = seq

# the songs' own bars
oh = open('/home/claude/fret-finder/songs/ochi-chyornye/index.html').read()
m = re.search(r'"title": "The plain chart".*?"chords": (\[\[.*?\]\]), "tab"', oh, flags=re.S)
ochi = [b[0]['c'] for b in json.loads(m.group(1))]
yh = open('/home/claude/fret-finder/songs/ya-vas-lyubil/index.html').read()
yvl = {}
for mm in re.finditer(r'"bars":\[\{', yh):
    j = mm.start() + len('"bars":'); depth = 0
    for k in range(j, len(yh)):
        if yh[k] == '[': depth += 1
        elif yh[k] == ']':
            depth -= 1
            if depth == 0: break
    try:
        for b in json.loads(yh[j:k + 1]):
            if isinstance(b.get('n'), int) and isinstance(b.get('c'), list): yvl.setdefault(b['n'], b['c'])
    except Exception: pass


def base(n):
    r, q, b = gtr.parse(n)
    return r, ('m' if q.startswith('m') and not q.startswith('maj') else '' if q not in ('dim7', 'm7b5') else q)


if ochi[6:12] != ['Am', 'Am', 'Dm', 'Dm', 'Am', 'Am']: P(f'Очи bars 7–12 are {ochi[6:12]}')
if 'E7' not in ochi or ochi[ochi.index('E7') + 2] != 'Am': P('Очи: E7 does not go to Am')
if [yvl.get(8), yvl.get(9)] != [['G'], ['Cmaj7']]: P(f'Я вас любил bars 8–9: {yvl.get(8)}, {yvl.get(9)}')
if [yvl.get(11), yvl.get(12)] != [['Cm'], ['Dsus4']]: P(f'Я вас любил bars 11–12: {yvl.get(11)}, {yvl.get(12)}')
if [yvl.get(15), yvl.get(16), yvl.get(17)] != [['G', 'A7/C#'], ['D7'], ['G']]: P(f'Я вас любил bars 15–17: {yvl.get(15)}, {yvl.get(16)}, {yvl.get(17)}')
if 'D7' not in yvl.get(14, []) or yvl.get(15, [''])[0] != 'G': P('Я вас любил: D7 does not go to G')

# each rule
nm = lambda exid: [n for n, g in items[exid]]
want = {'w-maj69': ['G6/9', 'C6/9'], 'w-min6': ['Am6', 'Am6/9', 'Dm6', 'Dm6/9', 'Am6', 'Am6/9'],
        'w-7min': ['E7', 'Am6', 'E7#9', 'Am6', 'E7b9', 'Am6', 'E7b13', 'Am6'],
        'w-7maj': ['D9', 'G6/9', 'D13', 'G6/9', 'D13b9', 'G6/9', 'D7b5', 'G6/9', 'D9b5', 'G6/9'],
        'w-m7b5': ['Am6', 'F#m7b5', 'Am6', 'F#m7b5', 'Dm6', 'Bm7b5', 'Dm6', 'Bm7b5'],
        'w-dim': ['Abdim7', 'Am6', 'Bdim7', 'Am6', 'Ddim7', 'Am6'], 'w-pass': ['Cm6', 'C#dim7', 'Dsus4'],
        'w-cl-min': ['Am', 'Am(maj7)', 'Am7', 'Am6'], 'w-cl-maj': ['G6/9', 'Am6', 'Bbm6', 'Gmaj7/B', 'C6/9'],
        'w-march': ['E9', 'A13', 'D9', 'G6/9'], 'w-march-song': ['G6/9', 'A13', 'D9', 'G6/9']}
for exid, w in want.items():
    if exid not in items: P(f'{exid} missing'); continue
    if nm(exid) != w: P(f'{exid}: {nm(exid)}')
# majors as 6/9, minors as minor 6 (never minor 7 except in the cliché), sevenths by where they go
for exid, seq in items.items():
    for n, g in seq:
        r, q, b = gtr.parse(n)
        if q in ('', 'maj7', '6') and exid not in ('w-cl-min',) and not (q == 'maj7' and b is not None and (b - r) % 12 == 4):
            P(f'{exid}: {n} is not a 6/9 (nor a major 7 over its 3rd)')
        if q == 'm7' and exid != 'w-cl-min': P(f'{exid}: a minor 7')
for exid in ('w-7min', 'w-7maj'):
    s = items[exid]
    for (a, _), (b, _) in zip(s[0::2], s[1::2]):
        ra = gtr.parse(a)[0]; rb, qb, _ = gtr.parse(b)
        if (rb - ra) % 12 != 5: P(f'{exid}: {a} does not resolve a 5th down to {b}')
        if exid == 'w-7min' and not qb.startswith('m'): P(f'{exid}: {b} is not minor')
        if exid == 'w-7maj' and qb.startswith('m'): P(f'{exid}: {b} is not major')
# minor 7♭5 = minor 6 over its 6th
s = items['w-m7b5']
for (a, ga), (b, gb) in zip(s[0::2], s[1::2]):
    if gtr.chord_pcs(a) - {0} and {m % 12 for m in notes(gb)} - {m for m in gtr.chord_pcs(a)}: P(f'w-m7b5: {b} has notes outside {a}')
    ra, qa, _ = gtr.parse(a); rb = gtr.parse(b)[0]
    if (rb - ra) % 12 != 9: P(f'w-m7b5: {b} is not on {a}’s 6th')
# diminished for E7♭9: a half step above E, then minor 3rds, one shape moved three frets each time
s = [(n, g) for n, g in items['w-dim'] if 'dim' in n]
e7b9 = {4, 8, 11, 2, 5}
for k, (n, g) in enumerate(s):
    if not {m % 12 for m in notes(g)} <= e7b9: P(f'w-dim: {n} is not inside E7♭9')
    if k and [f - 3 if f > 0 else f for f in g] != s[k - 1][1]: P(f'w-dim: {n} is not the last grip three frets up')
if s and gtr.parse(s[0][0])[0] not in (5, 8, 11, 2): P('w-dim: the first diminished chord is not a half step above E or a minor 3rd from it')
# passing diminished: the bass climbs by half steps
bs = [min(notes(g)) for n, g in items['w-pass']]
if [b - bs[0] for b in bs] != [0, 1, 2]: P(f'w-pass: bass {bs}')
# minor cliché: one string falls a half step each chord, the rest held
s = [g for n, g in items['w-cl-min']]
for a, b in zip(s, s[1:]):
    d = [(i, y - x) for i, (x, y) in enumerate(zip(a, b)) if x != y]
    if len(d) != 1 or d[0][1] != -1: P(f'w-cl-min: {a} → {b}')
# major cliché: the bass climbs G, A, B♭, B, C
bs = [min(notes(g)) % 12 for n, g in items['w-cl-maj']]
if bs != [7, 9, 10, 11, 0]: P(f'w-cl-maj: bass {bs}')
# the march: each 7th chord a 5th above the next chord
s = items['w-march']
for (a, _), (b, _) in zip(s, s[1:]):
    if (gtr.parse(b)[0] - gtr.parse(a)[0]) % 12 != 5: P(f'w-march: {a} to {b} is not a 5th down')

print('grips checked:', sum(len(v) for v in items.values()), '· chords:', len(seen))
print('\n'.join(probs) if probs else 'all good')
sys.exit(1 if probs else 0)
