"""Checks for entry8 (tango walking bass): every bass line follows Graciano's formula for its chord, the 2-beat
approach is the right one of the three 5ths, the chord over the bass is the voicing he names, every held chord stays
under the hand while the bass moves, every bar has 4 beats and every quote a beat or two."""
import sys
sys.path.insert(0, '/home/claude/studies/tango'); sys.path.insert(0, '/home/claude/studies')
import entry8 as E
from quotes import _beats

OPEN = E.OPEN
probs = []
PC = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}


def rootpc(c):
    return (PC[c[0]] + (-1 if c[1:2] == 'b' else 1 if c[1:2] == '#' else 0)) % 12


SEMI = {d: E.DEG[d][1] for d in E.DEG}
n_rules = 0
for kind, chord, root, notes in E.RULES:
    n_rules += 1
    ms = [E.midi(n) for n in notes]
    r = E.midi(root) if kind != 'two' else ms[0]
    rel = [m - r for m in ms]
    if kind in ('asc', 'desc', 'eight'):
        want = [SEMI[d] for d in E.FORM[kind][E.quality(chord)].split()]
        if rel != want: probs.append(f'{kind} {chord}: {notes} is not {E.FORM[kind][E.quality(chord)]}')
        if kind == 'asc' and rel != sorted(rel): probs.append(f'asc {chord} not rising')
        if kind == 'desc' and rel != sorted(rel, reverse=True): probs.append(f'desc {chord} not falling')
    elif kind == 'r5':
        if [x % 12 for x in rel] != [0, 7, 0, 7] or rel[0] != rel[2] or rel[1] != rel[3] or abs(rel[1]) not in (5, 7):
            probs.append(f'r5 {chord}: {notes}')
    elif kind in ('arp', 'arp7'):
        q = E.quality(chord); third = 3 if q == 'min' else 4
        want = [0, third, 7, third] if kind == 'arp' else [0, third, 7, 10]
        if rel != want: probs.append(f'{kind} {chord}: {notes}')
    elif kind in ('sp1', 'sp3'):
        want = [0, 1, 2, 3] if kind == 'sp1' else [0, 2, 3, 4]
        if rel != want: probs.append(f'{kind} {chord}: {notes}')
    elif kind == 'sp2':
        if rel != [0, -5, -6, -8]: probs.append(f'sp2 {chord}: {notes}')
    elif kind == 'cliche':
        if rel != [0, -1, -2, -3]: probs.append(f'cliche {chord}: {notes}')
    elif kind == 'two':
        nxt = root                     # for 'two' the third field is the next chord
        here = (ms[1] - ms[0]) % 12
        if here not in (6, 7, 8): probs.append(f'two {chord}: second note is not a 5th')
        npc = rootpc(nxt); x = ms[1] % 12
        adj = lambda p: (p - npc) % 12 in (1, 11)
        options = {k: (ms[0] + k) % 12 for k in (6, 8)}
        if here in (6, 8) and not adj(x): probs.append(f'two {chord}->{nxt}: the altered 5th is not next to {nxt}')
        if here == 7 and not adj(x) and any(adj(p) for p in options.values()): probs.append(f'two {chord}->{nxt}: an altered 5th was the approach')
        if rootpc(chord) != ms[0] % 12: probs.append(f'two {chord}: does not start on its root')
print('bass formulas checked:', n_rules)


def span_ok(fr):
    fz = [f for f in fr if f > 0]
    if not fz: return True
    lo, hi = min(fz), max(fz)
    return hi - lo <= (4 if lo >= 7 else 3)


n_bars = 0
for S in E.SECTIONS:
    for ex in S['ex']:
        q = ex['quote']
        if _beats(q.get('items') or []) > 2 + 1e-9: probs.append(f'{ex["id"]}: quote too long')
        for j, b in enumerate(ex['bars']):
            n_bars += 1
            L = 0.0; held = []      # (until, strings, frets) of chords ringing on
            for it in b['items']:
                if it[0] == 'K':
                    g = it[2]
                    if not span_ok(g): probs.append(f'{ex["id"]} #{j + 1}: stretch {g}')
                    t0 = L
                    for h in it[3]:
                        if h[1] != '-' and isinstance(h[1], list) and any(g[6 - s] < 0 for s in h[1]): probs.append(f'{ex["id"]} #{j + 1}: struck string not in grip')
                        L += h[0]
                    if len(it) > 4: held.append((t0 + (L - t0 - it[3][-1][0]) + it[4]['hold'], it[4]['strings'], {s: g[6 - s] for s in it[4]['strings']}))
                elif it[0] == 'R':
                    for (s, f), d in zip(it[1], it[2]):
                        if not 0 <= f <= 12: probs.append(f'{ex["id"]} #{j + 1}: fret {f}')
                        if s == 4 and any(0 <= (OPEN[s] + f) - OPEN[x] <= 12 for x in (6, 5)) and 'ocho' not in ex['id']:
                            probs.append(f'{ex["id"]} #{j + 1}: 4th string not needed')
                        for until, ss, fr in held:
                            if L < until - 1e-9:
                                if s in ss: probs.append(f'{ex["id"]} #{j + 1}: bass on a held string')
                                if not span_ok([f] + list(fr.values())): probs.append(f'{ex["id"]} #{j + 1}: bass {s}/{f} out of reach of the held chord {fr}')
                        L += d
                elif it[0] == 'W': L += it[1]
            if abs(L - 4) > 1e-9: probs.append(f'{ex["id"]} #{j + 1}: {L} beats')
            # the chord over the bass is the voicing he names
            if 'ch' in b:
                for it in b['items']:
                    if it[0] != 'K': continue
                    name = it[1].split('/')[0]
                    ch = next(c for c in b['ch'] if c[0] == name)
                    ups = {E.midi(n) % 12 for n in ch[2]}
                    struck = set()
                    for h in it[3]:
                        if isinstance(h[1], list): struck |= set(h[1])
                    lowest = max(s for s in range(1, 7) if it[2][6 - s] >= 0)
                    got = {(OPEN[s] + it[2][6 - s]) % 12 for s in struck if s != lowest}
                    if got != ups: probs.append(f'{ex["id"]} #{j + 1}: {it[1]} upper notes {sorted(got)} not {sorted(ups)}')
print('bars checked:', n_bars)
print('\n'.join(probs) if probs else 'all good')
sys.exit(1 if probs else 0)
