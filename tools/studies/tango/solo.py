"""Fingering for the guitar alone (Graciano ch. 8): the tune on the top strings with chords, a bass line or other
voices under it, every note held for its written length. A bar is a list of events dict(t, n, d, role) with role
'mel' (the tune), 'acc' (a chord note, a bass note, a second voice). The fingering keeps, at every moment:
- every note that sounds on its own string;
- the tune on top, on the 1st, 2nd or 3rd string;
- the fretted notes within the hand: four frets below the 7th fret, five from it up, open strings free;
- at most four fingers, a barre (two or more notes on the lowest fret of the moment) counting as one.
Bars are fingered one after another, keeping the dozen best ways so far (a beam), the hand moving as little as it can."""
import sys
sys.path.insert(0, '/home/claude/studies/tango')
import mel as M

OPEN = {6: 40, 5: 45, 4: 50, 3: 55, 2: 59, 1: 64}
EPS = 1e-6


def span_ok(frets):
    fr = [f for f in frets if f > 0]
    if not fr: return True
    lo, hi = min(fr), max(fr)
    return hi - lo <= (4 if lo >= 7 else 3)


def fingers_ok(pos):
    fr = [(s, f) for s, f in pos if f > 0]
    if len(fr) <= 4: return True
    lo = min(f for s, f in fr)
    at_lo = [s for s, f in fr if f == lo]
    return len(fr) - len(at_lo) + 1 <= 4 and len(at_lo) >= 2


def overlap(a, b): return a['t'] < b['t'] + b['d'] - EPS and b['t'] < a['t'] + a['d'] - EPS


def moments(evs):
    return sorted({round(e['t'], 6) for e in evs})


def sounding(evs, t): return [e for e in evs if e['t'] - EPS <= t < e['t'] + e['d'] - EPS]


def check_bar(evs, pos):
    """problems with one placement (pos: list of (s, f) parallel to evs)"""
    probs = []
    P = {id(e): p for e, p in zip(evs, pos)}
    for i, a in enumerate(evs):
        for b in evs[i + 1:]:
            if overlap(a, b) and P[id(a)][0] == P[id(b)][0]: probs.append(f'{a["n"]} and {b["n"]} on one string')
    for t in moments(evs):
        snd = sounding(evs, t)
        ps = [P[id(e)] for e in snd]
        if not span_ok([f for s, f in ps]): probs.append(f'stretch at {t}: {ps}')
        if not fingers_ok(ps): probs.append(f'more than four fingers at {t}: {ps}')
        mels = [e for e in snd if e['role'] == 'mel']
        for m in mels:
            if any(M.midi(o['n']) >= M.midi(m['n']) for o in snd if o['role'] != 'mel'): probs.append(f'the tune is not on top at {t}')
            if P[id(m)][0] > 3: probs.append(f'the tune off the top strings at {t}')
    for e, (s, f) in zip(evs, pos):
        if OPEN[s] + f != M.midi(e['n']): probs.append(f'{e["n"]} is not string {s} fret {f}')
    return probs


def candidates(e, h, mel_strings):
    out = []
    strings = mel_strings if e['role'] == 'mel' else (6, 5, 4, 3, 2, 1)
    top = h + (4 if h >= 7 else 3)
    for s in strings:
        f = M.midi(e['n']) - OPEN[s]
        if f == 0 or (h <= f <= top and f <= 15): out.append((s, f))
    return out


def solve_bar(evs, carried, h_prev, mel_strings=(1, 2, 3), k=6):
    """the k best placements of a bar's events, given notes still sounding from before (carried: [(event, pos)]).
    The hand may move inside the bar; at every moment the notes sounding must fit it."""
    order = sorted(range(len(evs)), key=lambda i: (evs[i]['t'], -M.midi(evs[i]['n'])))
    cands = []
    for i in order:
        e = evs[i]
        strings = mel_strings if e['role'] == 'mel' else (6, 5, 4, 3, 2, 1)
        cands.append([(s, M.midi(e['n']) - OPEN[s]) for s in strings if 0 <= M.midi(e['n']) - OPEN[s] <= 15])
    found = []
    pre = [(ce, cp_) for ce, cp_ in carried]

    def hand_at(t, placed):
        fr = [p[1] for e, p in placed if e['t'] - EPS <= t < e['t'] + e['d'] - EPS and p[1] > 0]
        return min(fr) if fr else None

    def rec(j, placed):
        if j == len(order):
            allev = [e for e, p in placed]; allpos = [p for e, p in placed]
            if check_bar(allev, allpos): return
            cost, last = 0.0, h_prev
            for t in moments(allev):
                h = hand_at(t, placed)
                if h is None: continue
                if last: cost += abs(h - last)
                cost += 0.08 * h
                last = h
            for e, (s, f) in placed[len(pre):]:
                if f == 0: cost += 0.35
                if e['role'] == 'mel' and s == 3: cost += 0.25
                if e['role'] == 'acc' and s in (1, 2): cost += 0.1
                if f > 12: cost += 0.5
            pos = [None] * len(evs)
            for (e, p), i in zip(placed[len(pre):], order): pos[i] = p
            found.append((round(cost, 4), last, pos))
            return
        e = evs[order[j]]
        for p in cands[j]:
            ok = True
            snd = [(o, q) for o, q in placed if overlap(e, o)]
            for o, q in snd:
                if q[0] == p[0]: ok = False; break
            if not ok: continue
            now = [q for o, q in placed if o['t'] - EPS <= e['t'] < o['t'] + o['d'] - EPS] + [p]
            if not span_ok([f for s, f in now]) or not fingers_ok(now): continue
            if e['role'] == 'mel' and any(M.midi(o['n']) >= M.midi(e['n']) for o, q in placed if o['role'] != 'mel' and o['t'] - EPS <= e['t'] < o['t'] + o['d'] - EPS): continue
            rec(j + 1, placed + [(e, p)])
    rec(0, pre)
    found.sort(key=lambda x: x[0])
    seen, out = set(), []
    for c, h, pos in found:
        key = tuple(pos)
        if key in seen: continue
        seen.add(key); out.append((c, h, pos))
        if len(out) >= k: break
    return out


def arrange(bars, beam=10, mel_strings=(1, 2, 3)):
    """bars: [[event, ...], ...] with times inside each bar from 0; an event longer than its bar carries into the next.
    Returns positions per bar."""
    states = [(0.0, None, [], [])]           # cost, hand, positions so far, carried [(event with time shifted, pos)]
    for bi, evs in enumerate(bars):
        L = bar_len_of(bi, bars)
        new = []
        for cost, h, path, carried in states:
            opts = solve_bar(evs, carried, h, mel_strings)
            for c, hh, pos in opts:
                nc = []
                for e, p in zip(evs, pos):
                    if e['t'] + e['d'] > L + EPS: nc.append((dict(e, t=e['t'] - L), p))
                for e, p in carried:
                    if e['t'] + e['d'] > L + EPS: nc.append((dict(e, t=e['t'] - L), p))
                new.append((cost + c, hh, path + [pos], nc))
        assert new, f'bar {bi}: nothing fits {[(e["n"], e["t"], e["d"], e["role"]) for e in evs]}'
        new.sort(key=lambda x: x[0])
        states = new[:beam]
    return states[0][2]


LENS = {}


def bar_len_of(bi, bars): return LENS.get(id(bars), [3.0] * len(bars))[bi]


# ---------------------------------------------------------------- choosing chord notes under the tune
def voicings(names, bass, size, top, low=40, spread=19, need=()):
    """sets of spelled notes: `bass` (a pitch-class name) lowest, then size-1 more of `names`, all under midi `top`,
    within `spread` semitones of the bass; `need`: names that must be there"""
    from itertools import combinations
    out = []
    others = [n for n in names if n != bass]
    for ob in range(1, 5):
        b = bass + str(ob)
        try: mb = M.midi(b)
        except AssertionError: continue
        if not (low <= mb < top): continue
        for k in range(size - 1, size):
            for combo in combinations(others + ([bass] if size > len(others) + 1 else []), k):
                # each name at the octave(s) above the bass, under top
                def opts(n):
                    r = []
                    for o in range(1, 6):
                        x = n + str(o)
                        if mb < M.midi(x) < top and M.midi(x) - mb <= spread: r.append(x)
                    return r
                from itertools import product
                for pick in product(*[opts(n) for n in combo]):
                    ms = [mb] + [M.midi(x) for x in pick]
                    if len(set(ms)) != len(ms): continue
                    have = {bass} | set(combo)
                    if any(nd not in have for nd in need): continue
                    out.append([b] + sorted(pick, key=M.midi))
    out.sort(key=lambda v: (M.midi(v[-1]) - M.midi(v[0]), -M.midi(v[0])))
    return out


def arrange_alts(bars, lens, beam=10, mel_strings=(1, 2, 3), per_state=3):
    """bars: [[alternative events, ...], ...]: the beam tries every alternative of each bar.
    Returns (chosen alternative index, positions) per bar."""
    states = [(0.0, None, [], [])]
    for bi, alts in enumerate(bars):
        L = lens[bi]
        new = []
        for cost, h, path, carried in states:
            for ai, evs in enumerate(alts):
                for c, hh, pos in solve_bar(evs, carried, h, mel_strings, k=per_state):
                    nc = [(dict(e, t=e['t'] - L), p) for e, p in zip(evs, pos) if e['t'] + e['d'] > L + EPS]
                    nc += [(dict(e, t=e['t'] - L), p) for e, p in carried if e['t'] + e['d'] > L + EPS]
                    new.append((cost + c + 0.05 * ai, hh, path + [(ai, pos)], nc))
        assert new, f'bar {bi}: nothing fits'
        new.sort(key=lambda x: x[0])
        states = new[:beam]
    return states[0][2]
