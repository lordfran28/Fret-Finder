"""Helpers for the Exercises entries (Fret Finder studies): notes, string/fret placement, two-line steps, checks.
Two-line material is written as one P item per bar whose steps hold one note (one voice moving) or two (both voices
struck); the study template draws one diagram per item with the steps numbered."""
import re
OPEN = [40, 45, 50, 55, 59, 64]                 # strings 6..1
PC = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
NM = ['C', 'D♭', 'D', 'E♭', 'E', 'F', 'G♭', 'G', 'A♭', 'A', 'B♭', 'B']


def N(name):
    """'Bb2', 'C#4', 'D♭3' -> midi."""
    m = re.fullmatch(r'([A-G])([#b♯♭]*)(-?\d)', name.strip())
    if not m: raise ValueError(name)
    p = PC[m.group(1)] + sum(1 if c in '#♯' else -1 for c in m.group(2))
    return 12 * (int(m.group(3)) + 1) + p


def nn(m): return f"{NM[m % 12]}{m // 12 - 1}"


def place(midi, lo, hi, strings=(6, 5, 4, 3, 2, 1)):
    """The first string (in the given order) where midi falls between frets lo and hi."""
    for s in strings:
        f = midi - OPEN[6 - s]
        if lo <= f <= hi: return [s, f]
    raise ValueError(f'{nn(midi)} not playable on {strings} frets {lo}-{hi}')


def SF(s, f): return [s, f]


def two_lines(steps, beat=0.5, over=''):
    """steps: list of groups, each a list of [s, f] (one or two notes), each lasting `beat` (or (group, dur))."""
    groups, durs = [], []
    for st in steps:
        if isinstance(st, tuple): g, d = st
        else: g, d = st, beat
        groups.append([list(x) for x in g]); durs.append(d)
    return ['P', groups, durs, over]


def check_item(it, label=''):
    """Playability: no string twice in a step; the frets a hand covers within one item; lower voice below upper."""
    probs = []
    if it[0] == 'P':
        frets = [f for g in it[1] for s, f in g if f > 0]
        for g in it[1]:
            ss = [s for s, f in g]
            if len(set(ss)) != len(ss): probs.append(f'{label}: two notes on one string {g}')
            if len(g) == 2:
                a, b = sorted(g, key=lambda x: -x[0])          # lower string number = higher string
                if OPEN[6 - a[0]] + a[1] >= OPEN[6 - b[0]] + b[1]: probs.append(f'{label}: voices cross {g}')
        if frets:
            lo, hi = min(frets), max(frets)
            if hi - lo + 1 > (5 if lo >= 7 else 4): probs.append(f'{label}: stretch {lo}-{hi}')
    return probs


def place_lines(seq, lo_strings=(6, 5, 4, 3), up_strings=(1, 2, 3), maxf=12, prefer=5, open_cost=0.4):
    """Finger two voices together. seq: list of (lower midi or None, upper midi or None, beats). Each voice keeps
    its place while it rests or holds; both are never on one string; the hand (index finger at fret h) covers frets
    h..h+3 below the 7th fret and h..h+4 from it up, and it moves only as far as the notes make it; the path that
    moves the hand least (then prefers string changes to shifts, and fewer open strings) wins. Returns two_lines steps."""
    def cands(m, strings):
        if m is None: return [None]
        out = [(s, m - OPEN[6 - s]) for s in strings if 0 <= m - OPEN[6 - s] <= maxf]
        if not out: raise ValueError(f'{nn(m)} not on strings {strings}')
        return out

    def hand(L, U, h):
        fr = [p[1] for p in (L, U) if p and p[1] > 0]
        if not fr: return h
        for w in (3, 4):                                  # four frets, or five from the 7th fret up
            lo_, hi_ = max(fr) - w, min(fr)
            if w == 4: lo_ = max(lo_, 7)
            if lo_ <= hi_: return min(max(h, lo_), hi_)
        return None

    states = {(None, None, prefer): (0.0, [])}
    last = [None, None]
    for lo, up, d in seq:
        new = {}
        for (L0, U0, h0), (cost, path) in states.items():
            for Lc in cands(lo, lo_strings):
                for Uc in cands(up, up_strings):
                    L = Lc if lo is not None else L0
                    U = Uc if up is not None else U0
                    if L and U and L[0] <= U[0]: continue        # the lower voice on a thicker string
                    h = hand(L, U, h0)
                    if h is None: continue
                    c = cost + abs(h - h0) * 1.0
                    for P, P0, m, k in ((L, L0, lo, 0), (U, U0, up, 1)):
                        if m is None or P0 is None: continue
                        if P[0] != P0[0]: c += 0.15
                        if last[k] == m and P != P0: c += 3.0       # a repeated note stays where it was
                    c += sum((open_cost if p[1] == 0 else 0) for p in (Lc, Uc) if p) + 0.03 * abs(h - prefer)
                    key = (L, U, h)
                    if key not in new or new[key][0] > c:
                        new[key] = (c, path + [(Lc if lo is not None else None, Uc if up is not None else None, d, h)])
        if not new: raise ValueError(f'no fingering at step {len(path)} ({nn(lo) if lo else "-"}, {nn(up) if up else "-"})')
        states = new
        if lo is not None: last[0] = lo
        if up is not None: last[1] = up
    best = min(states.values(), key=lambda v: v[0])
    return [([list(p) for p in (L, U) if p], d) for L, U, d, h in best[1]]


def hands(steps):
    """The hand positions a fingering needs, step by step (for the notes), and the largest shift."""
    out, h, shifts = [], None, []
    for g, d in steps:
        fr = [f for s, f in g if f > 0]
        if fr:
            out.append((min(fr), max(fr)))
    return out


def shape(midis, near=5, maxf=12, allow_open=True):
    """Every note of a chord on its own string, lowest note on the thickest string used; the frets within four
    (five from the 7th fret up). The shape closest to fret `near`, with the fewest open strings, wins.
    Returns [[s, f], ...] in the order of midis given."""
    import itertools
    order = sorted(range(len(midis)), key=lambda i: midis[i])
    best = None
    for strings in itertools.combinations((6, 5, 4, 3, 2, 1), len(midis)):     # thick to thin
        pos = []
        for i, s in zip(order, strings):
            f = midis[i] - OPEN[6 - s]
            if f < 0 or f > maxf or (f == 0 and not allow_open): break
            pos.append((i, s, f))
        else:
            fr = [f for _, _, f in pos if f > 0]
            if fr and max(fr) - min(fr) + 1 > (5 if min(fr) >= 7 else 4): continue
            c = (abs((min(fr) if fr else near) - near) + 0.5 * sum(1 for _, _, f in pos if f == 0) + 0.2 * (max(fr) - min(fr) if fr else 0))
            if best is None or c < best[0]: best = (c, pos)
    if best is None: raise ValueError('no shape for ' + ','.join(nn(m) for m in midis))
    out = [None] * len(midis)
    for i, s, f in best[1]: out[i] = [s, f]
    return out
