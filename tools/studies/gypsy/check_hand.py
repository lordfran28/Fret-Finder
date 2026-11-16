"""Independent checks for hand.py (Wrembel's right-hand warm-up). The strokes are compared with a table transcribed
from Wrembel's pages 9–13, not with hand.py's rule; the chord order is read from your Очи чёрные page on the shelf;
every note is read back from the page's items."""
import sys, re, json
sys.path.insert(0, '/home/claude/studies'); sys.path.insert(0, '/home/claude/studies/gypsy'); sys.path.insert(0, '/home/claude/scripts')
import hand as H
import gtr

WREMBEL = {1: 'D', 2: 'DU', 3: 'DUD', 4: 'DUDU', 5: 'DUDUD', 6: 'DUDDUD', 7: 'DUDUDUD', 8: 'DUDUDUDU', 9: 'DUDDUDDUD'}   # as marked on pp. 9–12
OPENS = [40, 45, 50, 55, 59, 64]
probs = []


def P(m): probs.append(m)


# the chart: your Очи чёрные page, its plain chart, each chord's two bars once
h = open('/home/claude/fret-finder/songs/ochi-chyornye/index.html').read()
m = re.search(r'"title": "The plain chart".*?"chords": (\[\[.*?\]\]), "tab"', h, flags=re.S)
plain = [b[0]['c'] for b in json.loads(m.group(1))]
pairs = plain[0::2]
if plain[1::2] != pairs: P('the plain chart does not change every two bars')
if H.CHART != pairs: P(f'chart {H.CHART} is not the song’s {pairs}')

for n, want in WREMBEL.items():
    if ''.join(H.strokes(n)) != want: P(f'strokes for {n}: {"".join(H.strokes(n))}, Wrembel marks {want}')

PLANS = {f'div-{n}': [n] * 4 for n in range(1, 10)}
PLANS.update({'pivot-5': [5, 1, 5, 2, 5, 3, 5, 4], 'loop-23': [2, 3, 2, 3], 'loop-24': [2, 4, 2, 4], 'loop-25': [2, 5, 2, 5]})
EXS = {ex['id']: ex for S in H.SECTIONS for ex in S['ex']}
if set(EXS) != set(PLANS): P(f'exercises {sorted(EXS)}')
for exid, plan in PLANS.items():
    ex = EXS.get(exid)
    if not ex: continue
    if len(ex['bars']) != len(pairs): P(f'{exid}: {len(ex["bars"])} bars for {len(pairs)} changes')
    for j, (B, chord) in enumerate(zip(ex['bars'], pairs)):
        its = B['items']
        if len(its) != 1 or its[0][0] != 'K': P(f'{exid} bar {j + 1}: not one rhythm item'); continue
        _, name, grip, hits = its[0]
        if name != chord or B['chords'] != [chord]: P(f'{exid} bar {j + 1}: {name} where the song has {chord}')
        strs = [i for i, f in enumerate(grip) if f >= 0]
        if len(strs) != 1 or grip[strs[0]] != 0: P(f'{exid} bar {j + 1}: not one open string {grip}'); continue
        s = 6 - strs[0]
        root = gtr.parse(chord)[0]
        if OPENS[strs[0]] % 12 != root: P(f'{exid} bar {j + 1}: the open string is not {chord}’s root')
        # the hits: each beat divided as planned, the strokes as Wrembel marks them
        k = 0
        for bt, n in enumerate(plan):
            seq = hits[k:k + n]; k += n
            if len(seq) != n: P(f'{exid} bar {j + 1} beat {bt + 1}: {len(seq)} notes'); break
            for i, x in enumerate(seq):
                if abs(x[0] - 1 / n) > 1e-9: P(f'{exid} bar {j + 1} beat {bt + 1}: uneven notes')
                if x[1] != [s]: P(f'{exid} bar {j + 1} beat {bt + 1}: on string {x[1]}')
                v = x[2] if len(x) > 2 else 0
                stroke = WREMBEL[n][i]
                if i == 0 and not v > 0.05: P(f'{exid} bar {j + 1} beat {bt + 1}: the beat is not marked')
                if i > 0 and (v > 0) != (stroke == 'D'): P(f'{exid} bar {j + 1} beat {bt + 1} note {i + 1}: the sound has {"down" if v > 0 else "up"}, Wrembel {stroke}')
        rest = hits[k:]
        last = j == len(pairs) - 1
        if not last and rest: P(f'{exid} bar {j + 1}: {len(rest)} notes too many')
        if last:
            needs = WREMBEL[plan[-1]][-1] == 'U' and exid != 'pivot-5'
            if needs and (len(rest) != 1 or rest[0][0] != 1.0 or rest[0][1] != [s] or not rest[0][2] > 0.05): P(f'{exid}: does not close on a downstroke')
            if not needs and rest: P(f'{exid}: an extra note at the end')
        beats = sum(x[0] for x in hits)
        want = len(plan) + (1 if last and rest else 0)
        if abs(beats - want) > 1e-6: P(f'{exid} bar {j + 1}: {beats} beats')

print('exercises checked:', len(PLANS), '· chart:', ' '.join(pairs))
print('\n'.join(probs) if probs else 'all good')
sys.exit(1 if probs else 0)
