"""Checks for entry5 (tango fills): every fill is Graciano's, moved whole; every grip and run is playable."""
import sys
sys.path.insert(0, '/home/claude/scripts'); sys.path.insert(0, '/home/claude/studies/tango'); sys.path.insert(0, '/home/claude/studies')
import gtr
import entry5 as E
from kit_study import OPEN

probs = []
# 1. his fills moved whole: the same values, the same flags, every note by the same interval
for his, ours, se in E.MOVES:
    assert [d for d, _ in his.ev] == [d for d, _ in ours.ev], 'rhythm changed'
    assert his.flags == ours.flags
    for (d, a), (_, b) in zip(his.ev, ours.ev):
        assert len(a) == len(b)
        for x, y in zip(a, b):
            if E.midi(y) - E.midi(x) != se: probs.append(f'not moved whole: {x} -> {y} ({se})')
print('fills moved whole:', len(E.MOVES))


def bass_of(g):
    i = next(i for i in range(6) if g[i] >= 0)
    return 6 - i, g[i], OPEN[i] + g[i]


def chk_k(it, lab):
    name, g, hits = it[1], it[2], it[3]
    fr = [f for f in g if f > 0]
    if fr:
        lo, hi = min(fr), max(fr)
        if hi - lo > (4 if lo >= 7 else 3): probs.append(f'{lab} {name} {g}: stretch {lo}-{hi}')
    for h in hits:
        if isinstance(h[1], list):
            for s in h[1]:
                if g[6 - s] < 0: probs.append(f'{lab} {name}: string {s} struck but not in grip {g}')
    nm = name.replace('♭', 'b').replace('♯', '#')
    p = gtr.check_grip(g, nm)
    if p: probs.append(f'{lab} {name} {g}: {p}')


def chk_run(it, lab):
    if it[0] == 'R':
        for s, f in it[1]:
            if not 0 <= f <= 15: probs.append(f'{lab}: fret {f}')
    else:
        prev = None
        for grp in it[1]:
            ss = [s for s, f in grp]
            if len(set(ss)) != len(ss): probs.append(f'{lab}: two notes on one string {grp}')
            fr = [f for s, f in grp if f > 0]
            if fr and max(fr) - min(fr) > 3: probs.append(f'{lab}: two-note shape too wide {grp}')
            if prev and fr and max(abs(a - b) for a, b in zip(sorted(fr), sorted(prev))) > 3: probs.append(f'{lab}: shape jumps {prev} -> {fr}')
            prev = fr or prev


bars, n = [], 0
for S in E.SECTIONS:
    for ex in S['ex']:
        q = ex['quote']
        qits = q.get('items') or ([q['item']] if q.get('item') else [])
        L = 0
        for it in qits:
            if it[0] == 'K': chk_k(it, ex['id'] + ' quote'); L += sum(h[0] for h in it[3])
            elif it[0] in 'RP': chk_run(it, ex['id'] + ' quote'); L += sum(it[2])
            elif it[0] == 'W': L += it[1]
        if qits and L > 4: probs.append(f'{ex["id"]} quote {L} beats')
        for j, b in enumerate(ex['bars']):
            lab = f'{ex["id"]}#{j + 1}'
            L = 0
            for it in b['items']:
                if it[0] == 'K': chk_k(it, lab); L += sum(h[0] for h in it[3])
                elif it[0] in 'RP': chk_run(it, lab); L += sum(it[2])
                elif it[0] == 'W': L += it[1]
            if abs(L - 4) > 1e-9: probs.append(f'{lab}: {L} beats')
            n += 1
        # 2. the arrastre lands on the next bar's bass; a run's last note steps onto the next chord
        for j, b in enumerate(ex['bars'][:-1]):
            its = b['items']; nxt = next((x for x in ex['bars'][j + 1]['items'] if x[0] == 'K'), None)
            if not nxt: continue
            s, f, m = bass_of(nxt[2])
            last = its[-1]
            if last[0] == 'R' and len(last) > 4 and last[4].get('vel', [0])[0] == E.GHOST and len(last[1]) == 3:      # the drag
                if not (last[1][-1][0] == s and last[1][-1][1] == f - 1): probs.append(f'{ex["id"]}: drag misses the bass {last[1]} -> {s}/{f}')
print('bars checked:', n)

# 3. the music: targets are chord tones; the scale fills step onto the next root; the x where Graciano puts it
CT = {'E7': {4, 8, 11, 2}, 'Am': {9, 0, 4, 7},          # A minor's 7th: his sixths into C minor's 5th land on B♭ and G
       'Dm': {2, 5, 9}, 'Eb': {3, 7, 10}, 'Bb7': {10, 2, 5, 8}}
for S in E.SECTIONS:
    for ex in S['ex']:
        for b in ex['bars']:
            for it in b['items']:
                if it[0] == 'P':
                    tgt = [OPEN[6 - s] + f for s, f in it[1][-1]]
                    c = b['chords'][0]
                    if not {m % 12 for m in tgt} <= CT[c]: probs.append(f'{ex["id"]}: target {tgt} not in {c}')
# sizes: sixths 8 or 9 semitones, thirds 3 or 4, tenths 15 or 16, each fill one size throughout (as his)
for his, ours, se in E.MOVES:
    sz = {E.midi(ns[1]) - E.midi(ns[0]) for d, ns in ours.ev if len(ns) == 2}
    if sz and not (sz <= {8, 9} or sz <= {3, 4} or sz <= {15, 16}): probs.append(f'odd sizes {sz}')
# the x: Graciano's dead note is the dominant's bass (going to V) or a semitone under the tonic's bass (going to I)
for S in E.SECTIONS:
    for ex in S['ex']:
        if not ex['id'].startswith('octavas'): continue
        r = next(x for x in ex['bars'][0]['items'] if x[0] == 'R'); s, f = r[1][-1]; xm = OPEN[6 - s] + f
        k = next(x for x in ex['bars'][1]['items'] if x[0] == 'K'); bs, bf, bm = bass_of(k[2])
        want = 0 if 'tonica-dominante' in ex['id'] else -1
        if (xm - bm) % 12 != want % 12: probs.append(f'{ex["id"]}: x {xm} vs bass {bm}')
if probs:
    print('\n'.join(probs)); sys.exit(1)
print('all good')
