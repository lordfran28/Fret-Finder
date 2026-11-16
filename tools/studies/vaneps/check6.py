"""Independent checks for entry6 (the melodic minor in triads): read back from the page's bars, every triad is a close
triad on three adjacent strings in the right inversion, within the hand; going up every note is in A melodic minor
and the roots climb the scale step by step from the lowest triad that fits on the three low strings to the highest that
fits on the neck; coming down every note is in A natural minor, the roots stepping down to A minor; names match notes."""
import sys
sys.path.insert(0, '/home/claude/studies'); sys.path.insert(0, '/home/claude/studies/tango'); sys.path.insert(0, '/home/claude/studies/vaneps')
import entry6 as E

OPENS = [40, 45, 50, 55, 59, 64]                  # grip index 0 = low E
MEL = {9, 11, 0, 2, 4, 6, 8}
NAT = {9, 11, 0, 2, 4, 5, 7}
MEL_ORDER = [9, 11, 0, 2, 4, 6, 8]
NAT_ORDER = [9, 11, 0, 2, 4, 5, 7]
QUAL = {(3, 7): 'm', (4, 7): '', (3, 6): 'dim', (4, 8): 'aug'}
LET = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
probs = []


def P(m): probs.append(m)


def hand_ok(fr):
    fr = [f for f in fr if f > 0]
    return not fr or max(fr) - min(fr) + 1 <= (5 if min(fr) >= 7 else 4)


def fits_anywhere(ms, sets=((0, 1, 2), (1, 2, 3), (2, 3, 4), (3, 4, 5))):
    for st in sets:
        fr = [m - OPENS[i] for m, i in zip(ms, st)]
        if min(fr) >= 0 and max(fr) <= 15 and hand_ok(fr): return True
    return False


def triad_of(ms, inv):
    """root pc and quality from the voicing: inversion 1 has the root on top, 2 in the middle"""
    root = ms[2] if inv == 1 else ms[1]
    others = sorted(((m - root) % 12) for m in ms if m != root)
    return root, QUAL.get(tuple(others))


def name_ok(name, root, q):
    r = LET[name[0]] + (1 if name[1:2] == '#' else -1 if name[1:2] == 'b' else 0)
    rest = name[1:].lstrip('#b')
    return r % 12 == root % 12 and rest == q


def step(sc_order, pc, k):
    return sc_order[(sc_order.index(pc) + k) % 7]


def scale_triad(root_m, sc_order, inv):
    d = sc_order.index(root_m % 12)
    t = root_m + (sc_order[(d + 2) % 7] - sc_order[d]) % 12
    f = root_m + (sc_order[(d + 4) % 7] - sc_order[d]) % 12
    return [t, f, root_m + 12] if inv == 1 else [f, root_m + 12, t + 12]


def prev_root(m, sc_order):
    m -= 1
    while m % 12 not in sc_order: m -= 1
    return m


def next_root(m, sc_order):
    m += 1
    while m % 12 not in sc_order: m += 1
    return m


EXS = {ex['id']: ex for S in E.SECTIONS for ex in S['ex']}
for exid, inv in (('mel-1st', 1), ('mel-2nd', 2)):
    ex = EXS.get(exid)
    if not ex: P(f'{exid}: not on the page'); continue
    chords = []
    for j, B in enumerate(ex['bars']):
        beats = 0
        for it in B['items']:
            if it[0] == 'C':
                chords.append((it[1], it[2], j)); beats += it[3]
                if it[3] != 1.0: P(f'{exid} bar {j + 1}: a triad of {it[3]} beats')
            elif it[0] == 'W': beats += it[1]
        if beats != 4: P(f'{exid} bar {j + 1}: {beats} beats')
    phase, prev = 'up', None
    roots = []
    for k, (name, g, j) in enumerate(chords):
        idx = [i for i, f in enumerate(g) if f >= 0]
        if len(idx) != 3 or idx[2] - idx[0] != 2: P(f'{exid} chord {k + 1}: not three adjacent strings {g}'); continue
        ms = [OPENS[i] + g[i] for i in idx]
        if not (ms[0] < ms[1] < ms[2]) or ms[2] - ms[0] >= 12: P(f'{exid} chord {k + 1}: not a close triad {ms}'); continue
        if max(g) > 15 or not hand_ok([g[i] for i in idx]): P(f'{exid} chord {k + 1}: reach {g}')
        root, q = triad_of(ms, inv)
        if q is None: P(f'{exid} chord {k + 1}: not a triad in this inversion {ms}'); continue
        if not name_ok(name, root, q): P(f'{exid} chord {k + 1}: name {name} for {root % 12}{q}')
        pcs = {m % 12 for m in ms}
        if phase == 'up' and not pcs <= MEL:
            phase = 'down'
            if prev is None: P(f'{exid}: starts coming down')
        if phase == 'up':
            if not pcs <= MEL: P(f'{exid} chord {k + 1}: going up outside the melodic minor')
            if prev is not None and root != next_root(prev, MEL_ORDER): P(f'{exid} chord {k + 1}: going up, the root does not take the next step')
        else:
            if not pcs <= NAT: P(f'{exid} chord {k + 1}: coming down outside the natural minor {sorted(pcs)}')
            if prev is None: pass
            elif roots and roots[-1][1] == 'up':
                if root != prev_root(prev, NAT_ORDER): P(f'{exid} chord {k + 1}: the turn does not step down')
                top = prev
            elif root != prev_root(prev, NAT_ORDER): P(f'{exid} chord {k + 1}: coming down, the root does not take the next step')
        roots.append((root, phase)); prev = root
    ups = [r for r, ph in roots if ph == 'up']; downs = [r for r, ph in roots if ph == 'down']
    if not ups or not downs: P(f'{exid}: does not go up and come down'); continue
    # it starts on the lowest triad that fits on the three low strings
    first = chords[0][1]
    if [i for i, f in enumerate(first) if f >= 0] != [0, 1, 2]: P(f'{exid}: does not start on the three low strings')
    below = scale_triad(prev_root(ups[0], MEL_ORDER) - 12, MEL_ORDER, inv)      # the root sits an octave below the voicing's root note
    if fits_anywhere(below, sets=((0, 1, 2),)): P(f'{exid}: a lower triad fits on the low strings')
    # it climbs to the highest that fits
    above = scale_triad(next_root(ups[-1], MEL_ORDER) - 12, MEL_ORDER, inv)
    if fits_anywhere(above): P(f'{exid}: stops before the top of the neck')
    # it ends on the lowest A minor reached going up
    if downs[-1] % 12 != 9: P(f'{exid}: does not end on A minor')
    low_a = min(r for r in ups if r % 12 == 9)
    if downs[-1] != low_a: P(f'{exid}: ends on another A minor ({downs[-1]} vs {low_a})')
    print(exid, len(ups), 'up,', len(downs), 'down')

# the quotes
for exid, want in (('mel-1st', [('D', [2, 0, 0, -1, -1, -1]), ('E', [4, 2, 2, -1, -1, -1])]), ('mel-2nd', [('Bm', [2, 2, 0, -1, -1, -1]), ('Caug', [4, 3, 2, -1, -1, -1])])):
    its = [(it[1], it[2]) for it in EXS[exid]['quote']['items'] if it[0] == 'C']
    if its != want: P(f'{exid}: quote changed')
    for name, g in its:
        ms = [OPENS[i] + f for i, f in enumerate(g) if f >= 0]
        root, q = triad_of(ms, 1 if exid == 'mel-1st' else 2)
        if q is None or not name_ok(name, root, q): P(f'{exid}: quote {name} does not match {ms}')
        if not {m % 12 for m in ms} <= MEL: P(f'{exid}: quote {name} not in A melodic minor')

print('\n'.join(probs) if probs else 'all good')
sys.exit(1 if probs else 0)
