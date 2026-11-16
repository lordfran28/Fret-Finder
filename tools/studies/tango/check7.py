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

# ours in the application exercises: the device applied to the song's own chords, checked by the rule
ROOT = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}


def pc_root(c):
    r = ROOT[c[0]] + (-1 if c[1:2] == 'b' else 1 if c[1:2] == '#' else 0)
    return r % 12


def tones(c):
    name = c.split('/')[0]; q = name[2:] if name[1:2] in ('b', '#') else name[1:]
    iv = {'': (0, 4, 7), 'm7': (0, 3, 7, 10), '7': (0, 4, 7, 10), 'maj7': (0, 4, 7, 11)}[q]
    return {(pc_root(c) + i) % 12 for i in iv}


def dominant(c): return c.split('/')[0].endswith('7') and 'maj7' not in c and 'm7' not in c


rule_pairs = 0
for id_, bars in E.OURS.items():
    seq = []             # (chord over it, kind, notes)
    for songbar, chords, ev in bars:
        t, ci, left = 0, 0, chords[0][1]
        for e in ev:
            while left <= 1e-9: ci += 1; left = chords[ci][1]
            over = chords[ci][0]
            seq.append((over, e[0], e[2] if e[0] == 'N' else None))
            left -= e[1]
        if abs(sum(e[1] for e in ev) - 4) > 1e-9: probs.append(f'{id_} bar {songbar}: not 4 beats')
    prev = None
    for over, kind, notes in seq:
        if kind != 'N': continue
        ps = sorted(E.midi(n) for n in notes); pcs = {p % 12 for p in ps}; rule_pairs += 1
        if dominant(over):
            r = pc_root(over); dim = {(r + i) % 12 for i in (1, 4, 7, 10)}
            if ps[1] - ps[0] != 6 or not pcs <= dim: probs.append(f'{id_}: {notes} over {over} is not one of its tritones')
        elif not pcs <= tones(over): probs.append(f'{id_}: {notes} over {over} is not in the chord')
        if prev is not None:
            pover, pps = prev
            same_dim = dominant(over) and over == pover
            if not same_dim and {p % 12 for p in pps} != pcs:
                moves = sorted(abs(b - a) for a, b in zip(pps, ps))
                if not (all(1 <= m <= 2 for m in moves) and 1 in moves): probs.append(f'{id_}: {pps} to {ps} is not a step resolution')
        prev = (over, ps)
print('pairs checked by the rule:', rule_pairs)


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
