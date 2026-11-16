"""Chord grips by rule, for Wrembel's voicings: every note a tone of the chord, every required tone present, the bass
note the one asked for, no open strings (manouche grips move), the hand within four frets (five from the 7th fret up),
at most four fingers (a first-finger barre counts as one, and only across strings it holds down), nothing on a string
between two barred strings that should stay silent. Among the grips that pass, the one nearest the position asked
for, then the fewest notes doubled, then four notes rather than five or six."""
import sys, itertools
sys.path.insert(0, '/home/claude/scripts')
import gtr

OPENS = [40, 45, 50, 55, 59, 64]                 # grip index 0 = low E string


def fingers(g):
    fr = [(i, f) for i, f in enumerate(g) if f > 0]
    if not fr: return 0
    lo = min(f for _, f in fr)
    at_lo = [i for i, f in fr if f == lo]
    n = len(fr)
    if len(at_lo) >= 2:
        a, b = min(at_lo), max(at_lo)
        if all(g[i] >= lo for i in range(a, b + 1)):        # a barre: every string under it is fretted at or above it
            n -= len(at_lo) - 1
    return n


def hand_ok(g):
    fr = [f for f in g if f > 0]
    return not fr or max(fr) - min(fr) + 1 <= (5 if min(fr) >= 7 else 4)


def grips(name, bass_string=None, maxf=12, sizes=(4, 5), strings=None, root_needed=True):
    """every grip of the chord `name` (gtr names, slash bass allowed) with the bass on `bass_string` (6, 5 or 4), or on
    exactly the strings given (thick to thin); the root must sound unless root_needed is False"""
    root, q, bass = gtr.parse(name)
    req, opt = gtr.QUAL[q]
    allowed = {(root + i) % 12 for i in req | opt} | ({bass} if bass is not None else set())
    need = {(root + i) % 12 for i in req} | ({bass} if bass is not None else set()) | ({root} if root_needed and q != 'dim7' else set())
    low_pc = bass if bass is not None else root
    out = []
    if strings:
        sets = [tuple(6 - s for s in strings)]
    else:
        sets = []
        for bs in ([bass_string] if bass_string else [6, 5, 4]):
            bi = 6 - bs
            for n in sizes:
                sets += [(bi,) + strs for strs in itertools.combinations(range(bi + 1, 6), n - 1)]
    for idx in sets:
        bi = idx[0]
        if True:
            if True:
                choices = []
                for i in idx:
                    c = [f for f in range(1, maxf + 1) if (OPENS[i] + f) % 12 in allowed]
                    if i == bi: c = [f for f in c if (OPENS[i] + f) % 12 == low_pc]
                    choices.append(c)
                for frets in itertools.product(*choices):
                    if max(frets) - min(frets) > 4: continue
                    g = [-1] * 6
                    for i, f in zip(idx, frets): g[i] = f
                    if not hand_ok(g) or fingers(g) > 4: continue
                    if g[bi] > min(f for i, f in enumerate(g) if f > 0 and i != bi) + 2: continue    # the bass finger (or thumb) can't reach far ahead of the hand
                    pcs = [(OPENS[i] + g[i]) % 12 for i in idx]
                    if not need <= set(pcs): continue
                    out.append(g)
    return out


def pos(g):
    """where the hand is: the mean of the fretted notes"""
    fr = [f for f in g if f > 0]
    return sum(fr) / len(fr)


def best(name, near, bass_string=None, prefer_top=None, sizes=(4, 5), strings=None, root_needed=True):
    """the grip nearest fret `near`; ties: fewer doubled notes, four notes, the top note nearest `prefer_top` (midi)"""
    cands = grips(name, bass_string, sizes=sizes, strings=strings, root_needed=root_needed)
    if not cands: raise ValueError(f'no grip for {name} on {bass_string}')
    def cost(g):
        ms = [OPENS[i] + f for i, f in enumerate(g) if f >= 0]
        dbl = len(ms) - len({m % 12 for m in ms})
        c = abs(pos(g) - near) + 0.6 * dbl + 0.3 * (len(ms) - 4)
        if prefer_top is not None: c += 0.15 * abs(max(ms) - prefer_top)
        return c
    return min(cands, key=cost)


def notes(g): return [OPENS[i] + f for i, f in enumerate(g) if f >= 0]


def path(names, strings, near, root_needed=None, fixed=None):
    """a grip for each chord, on the string sets given (one per chord, or one for all), the hand moving as little as it
    can: least total change of position, then of the top note"""
    if not isinstance(strings, list) or len(strings) != len(names): strings = [strings] * len(names)
    root_needed = root_needed or [True] * len(names)
    layers = []
    fixed = fixed or {}
    for n, st, rn in zip(names, strings, root_needed):
        sets = st if isinstance(st, list) else [st]                 # a list of string sets: any of them
        L = [g for x in sets for g in grips(n, strings=x, root_needed=rn)]
        if n in fixed and fixed[n] in L: L = [fixed[n]]             # a chord already gripped elsewhere keeps its grip
        layers.append(L)
    for n, L in zip(names, layers):
        if not L: raise ValueError(f'no grip for {n}')
    def top(g): return max(notes(g))
    def extra(g): return 0.5 * max(0, len(notes(g)) - 4) + 2.0 * (len(notes(g)) - len({m % 12 for m in notes(g)}))
    best_ = [(abs(pos(g) - near) * 1.0 + extra(g), [g]) for g in layers[0]]
    for L in layers[1:]:
        best_ = [min(((c + abs(pos(g) - pos(p[-1])) + 0.15 * abs(top(g) - top(p[-1])) + 0.1 * sum(1 for a, b in zip(g, p[-1]) if a != b) + extra(g), p + [g])
                      for c, p in best_), key=lambda x: x[0]) for g in L]
    out = min(best_, key=lambda x: x[0])[1]
    first = {}
    for k, n in enumerate(names):                       # one grip per chord: a chord that comes back keeps its first grip
        if n in first and first[n] in layers[k]: out[k] = first[n]
        first.setdefault(n, out[k])
    return out
