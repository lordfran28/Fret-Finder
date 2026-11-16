import sys
sys.path.insert(0, '/home/claude/studies'); sys.path.insert(0, '/home/claude/studies/tango'); sys.path.insert(0, '/home/claude/studies/vaneps')
import entry3 as E
probs = []
for id_, d, c, mv, voices in E.CHECK:
    tri = {E.EB[d % 7], E.EB[(d + 2) % 7], E.EB[(d + 4) % 7]}
    if {m % 12 for m in c} != tri or c[2] % 12 != E.EB[d] or max(c) - min(c) >= 12: probs.append(f'{id_} {d}: center is not the first-inversion triad')
    for i, m in enumerate(mv):
        k = voices.get(i, 0)
        idx = E.SC.index(c[i])
        if m != E.SC[idx + k]: probs.append(f'{id_} {d}: voice {i} not moved a scale step {k}')
for S in E.SECTIONS[-1:]:
    for e in S['ex']:
        for j, b in enumerate(e['bars']):
            g0, g1 = b['items'][0][2], b['items'][1][2]
            if [i for i in range(6) if g0[i] >= 0] != [i for i in range(6) if g1[i] >= 0] or sum(1 for i in range(6) if g0[i] != g1[i]) != len(next(x for x in E.CHECK if x[0] == {'super-upper': 'upper-super', 'super-middle': 'middle-super', 'counter': 'counter'}[e['id']])[4]):
                probs.append(f'{e["id"]} bar {j + 1}: the moved chord is not the same grip with only the moved voices changed')
            for it in b['items']:
                fr = [x for x in it[2] if x > 0]
                if max(fr) - min(fr) > (4 if min(fr) >= 7 else 3): probs.append(f'{e["id"]} bar {j + 1}: stretch')
                ms = sorted(E.E2.OPEN[6 - i] + it[2][i] for i in range(6) if it[2][i] >= 0)
            if abs(sum(it[3] for it in b['items']) - 4) > 1e-9: probs.append('beats')
print('cells checked:', len(E.CHECK)); print('\n'.join(probs) if probs else 'all good'); sys.exit(1 if probs else 0)
