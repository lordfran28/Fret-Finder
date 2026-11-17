"""Independent checks for concepts2.py: Wyble's figures read again from the book's own music (vector glyphs, vecread.py)
and compared with the transcription; ours must be his first events moved by one fixed interval (so every shape and
every step is his), starting on the two chord tones the text names; the strings and frets must give exactly those
pitches, one note per string, inside one hand position at a time; the bars Moonglow's page gives for each chord."""
import sys, re, json
sys.path.insert(0, '/home/claude/studies'); sys.path.insert(0, '/home/claude/studies/wyble'); sys.path.insert(0, '/home/claude/scripts')
import concepts2 as C
import vecread as V
import gtr

probs = []
def P(m): probs.append(m)
OPEN = [40, 45, 50, 55, 59, 64]
LET = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
def wm(n):
    m = re.fullmatch(r'([A-G])([♯♭]?)(\d)', n)
    return 12 * (int(m.group(3)) + 1) + LET[m.group(1)] + (m.group(2) == '♯') - (m.group(2) == '♭')

# 1. the transcription against the book
for key, (page, sysno) in C.WHERE.items():
    row = V.spell(V.read(page))[sysno - 1]
    book = [sorted(wm(n) for n in ns) for bar in row for x, ns in bar]
    mine = [sorted(wm(x) for x in ev.split('+')) for ev in C.HIS[key].split()]
    if book != mine:
        k = next((i for i, (a, b) in enumerate(zip(book, mine)) if a != b), min(len(book), len(mine)))
        P(f'{key}: differs from the book at event {k + 1}: {book[k] if k < len(book) else None} vs {mine[k] if k < len(mine) else None}')
# 2. ours = his moved by one interval, starting on the named chord's two tones
NM = {'C': 0, 'D♭': 1, 'D': 2, 'E♭': 3, 'E': 4, 'F': 5, 'F♯': 6, 'G♭': 6, 'G': 7, 'A♭': 8, 'A': 9, 'B♭': 10, 'B': 11, 'C♭': 11, 'G♯': 8}
EXS = {e['id']: e for e in C.EX}
IDS = {'P1U': 'c-8-1-up', 'P1D': 'c-8-1-down', 'P2U': 'c-8-2-up', 'P2D': 'c-8-2-down', 'E9': 'c-9', 'E10U': 'c-10-up', 'E10D': 'c-10-down', 'E12': 'c-12', 'E19': 'c-19'}
h = open('/home/claude/fret-finder/songs/moonglow/index.html').read()
i = h.find('"chords": [{"name"')
mg, _ = json.JSONDecoder().raw_decode(h[i + len('"chords": '):])
MG = {c['name']: c['note'] for c in mg}
for key, (ch, tr, n, what, d, per) in C.OURS.items():
    his = [sorted(wm(x) for x in ev.split('+')) for ev in C.HIS[key].split()][:n]
    ex = EXS[IDS[key]]
    got, durs, lens = [], [], []
    for B in ex['bars']:
        L = 0
        for it in B['items']:
            for g, du in zip(it[1], it[2]):
                ss = [s for s, f in g]
                if len(ss) != len(set(ss)): P(f'{key}: two notes on a string')
                fr = [f for s, f in g if f > 0]
                got.append(sorted(OPEN[6 - s] + f for s, f in g)); durs.append(du); L += du
            fr = [f for g in it[1] for s, f in g if f > 0]
        lens.append(round(L, 6))
    shifts = {g[j] - (hh[j] - 12) for g, hh in zip(got, his) for j in range(len(g))} if len(got) == len(his) and all(len(a) == len(b) for a, b in zip(got, his)) else None
    if shifts != {tr}: P(f'{key}: ours is not his moved by one interval ({shifts})')
    # his rhythm, from the page: pattern 1 and 2 in quarters (4/4), exercise 9 in triplet eighths (4/4), exercise 10 in eighths (3/4)
    RD, RB = {'P1U': 1, 'P1D': 1, 'P2U': 1, 'P2D': 1, 'E9': 1 / 3, 'E10U': 0.5, 'E10D': 0.5, 'E12': [0.5] * 6 + [1], 'E19': [0.5] * 6 + [1]}[key], {'E10U': 3, 'E10D': 3}.get(key, 4)
    RDS = [RD] * len(durs) if not isinstance(RD, list) else (RD * len(durs))[:len(durs)]
    if any(abs(x - y) > 1e-9 for x, y in zip(durs, RDS)) or len(got) != n: P(f'{key}: rhythm')
    if any(abs(L - RB) > 1e-6 for L in lens): P(f'{key}: bar lengths {lens}')
    names = re.findall(r'([A-G][♯♭]?) and ([A-G][♯♭]?)', what)[0]
    if {NM[x] for x in names} != {got[0][0] % 12, got[0][-1] % 12}: P(f'{key}: does not start on {names}')
    if not {NM[x] for x in names} <= gtr.chord_pcs(ch): P(f'{key}: {names} are not in {ch}')
    if ex['bars'][0]['chords'] != [ch]: P(f'{key}: the chord shown')
    # the bar the text names must carry that chord on Moonglow's page
    txt = ex['bars'][0]['note']
    mb = re.search(r'\(bar (\d+)\)', txt)
    if mb and mb.group(1) not in re.findall(r'\d+', MG.get(ch, '')): P(f'{key}: Moonglow has no {ch} in bar {mb.group(1)}')
    # the hand: the frets of each bar's notes within one position where they are played together, and nearby from one to the next
    for B in ex['bars']:
        for it in B['items']:
            for g in it[1]:
                fr = [f for s, f in g if f > 0]
                if fr and max(fr) - min(fr) + 1 > (5 if min(fr) >= 7 else 4): P(f'{key}: a stretch {g}')
# 3. the quote is his first shape, at its own pitch
for key, e_id in IDS.items():
    q = EXS[e_id]['quote']['item']
    his0 = sorted(wm(x) - 12 for x in C.HIS[key].split()[0].split('+'))
    if sorted(OPEN[6 - s] + f for s, f in q[1][0]) != his0 or len(q[1]) != 1: P(f'{key}: the quote')
# 4. the book's own sequence rule holds through every printed bar (a missed accidental would break it)
RULE = {'E12': (7, 1), 'E19': (7, -2), 'E10U': (6, 2), 'E10D': (6, -2), 'E9': (3, 2), 'P1U': (2, 2), 'P1D': (2, -2), 'P2U': (2, 2), 'P2D': (2, -2)}
for key, (size, step) in RULE.items():
    e = [sorted(wm(x) for x in ev.split('+')) for ev in C.HIS[key].split()]
    if any([m + step for m in e[i - size]] != e[i] for i in range(size, len(e))): P(f'{key}: the printed figure does not repeat {step:+d} every {size}')
print('exercises checked:', len(C.OURS))
print('\n'.join(probs) if probs else 'all good')
sys.exit(1 if probs else 0)
