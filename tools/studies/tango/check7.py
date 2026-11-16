"""Checks for entry7 (tango harmony): every cadence is Graciano's moved whole; every grip and two-note shape playable."""
import sys
sys.path.insert(0, '/home/claude/studies/tango'); sys.path.insert(0, '/home/claude/studies')
import entry7 as E
from kit_study import OPEN
probs = []
for his, ours, se in E.MOVES:
    if [e[0] for e in his.ev] != [e[0] for e in ours.ev] or [e[1] for e in his.ev] != [e[1] for e in ours.ev]:
        probs.append('rhythm or kind changed')
    for a, b in zip(his.ev, ours.ev):
        if a[0] in ('K', 'N'):
            for x, y in zip(a[2], b[2]):
                if E.midi(y) - E.midi(x) != se: probs.append(f'not moved whole: {x}->{y}')
            if a[0] == 'K' and (a[4] if len(a) > 4 else '') != (b[4] if len(b) > 4 else ''): probs.append('articulation changed')
print('cadences moved whole:', len(E.MOVES))


def span_ok(fr):
    fz = [f for f in fr if f > 0]
    if not fz: return True
    lo, hi = min(fz), max(fz)
    return hi - lo <= (4 if lo >= 7 else 3)


n = 0
for S in E.SECTIONS:
    for ex in S['ex']:
        groups = [('quote', ex['quote'].get('items') or [])] + [(f'#{j + 1}', b['items']) for j, b in enumerate(ex['bars'])]
        for lab, its in groups:
            L = 0
            for it in its:
                if it[0] == 'K':
                    if not span_ok(it[2]): probs.append(f'{ex["id"]} {lab}: stretch {it[1]} {it[2]}')
                    for h in it[3]:
                        if isinstance(h[1], list) and any(it[2][6 - s] < 0 for s in h[1]): probs.append(f'{ex["id"]} {lab}: struck string not in grip')
                    L += sum(h[0] for h in it[3])
                elif it[0] == 'P':
                    for g in it[1]:
                        ss = [s for s, f in g]
                        if len(set(ss)) != len(ss): probs.append(f'{ex["id"]} {lab}: two notes on a string')
                        if not span_ok([f for s, f in g]): probs.append(f'{ex["id"]} {lab}: two-note stretch {g}')
                        if any(not 0 <= f <= 15 for s, f in g): probs.append(f'{ex["id"]} {lab}: fret out of range')
                    L += sum(it[2])
                elif it[0] == 'W': L += it[1]
            if lab == 'quote' and L > 4: probs.append(f'{ex["id"]} quote {L}')
            if lab != 'quote' and abs(L - 4) > 1e-9: probs.append(f'{ex["id"]} {lab}: {L} beats')
            n += 1
print('bars checked:', n)
print('\n'.join(probs) if probs else 'all good')
sys.exit(1 if probs else 0)
