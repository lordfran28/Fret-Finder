import sys
sys.path.insert(0, '/home/claude/studies'); sys.path.insert(0, '/home/claude/studies/tango'); sys.path.insert(0, '/home/claude/studies/vaneps')
import entry4 as E
from kit_study import check_item
probs = []
for var, held, out in E.CHECK:
    who, way, steps = E.VARS[var]
    for (lo, up), n in zip(out, steps):
        if lo % 12 not in E.E3.EB or up % 12 not in E.E3.EB: probs.append(f'{var}: outside E♭ major'); continue
        if E.SC.index(up) - E.SC.index(lo) != n: probs.append(f'{var}: {lo}-{up} is not {n} scale steps')
    fixed = [lo for lo, up in out] if var in ('3-6-up', '6-3-down') else [up for lo, up in out]
    if len(set(fixed)) != 1: probs.append(f'{var}: the held voice moves')
for S in E.SECTIONS[-1:]:
    for e in S['ex']:
        for j, b in enumerate(e['bars']):
            for it in b['items']: probs += check_item(it, f'{e["id"]} bar {j + 1}')
            if abs(sum(sum(it[2]) for it in b['items']) - 4) > 1e-9: probs.append('beats')
print('stations checked:', len(E.CHECK)); print('\n'.join(probs) if probs else 'all good'); sys.exit(1 if probs else 0)
