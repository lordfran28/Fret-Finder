"""Fingering for guitar pieces given as notes (onset, length, midi): every note gets a string and fret.
A beam search over the onsets: notes struck together on different strings, never on a string that is still
ringing a held note (unless nothing else works), the hand (index finger at fret h) covering h..h+3 below the 7th
fret and h..h+4 from it up for every fretted note held at that moment; cost = hand shifts, high frets, string
changes for repeated notes. Open strings are welcome (this is music written for them)."""
from fractions import Fraction as Fr
import itertools
STD = [40, 45, 50, 55, 59, 64]           # strings 6..1


def cands(m, tuning, maxf=12):
    return [(s, m - tuning[6 - s]) for s in (6, 5, 4, 3, 2, 1) if 0 <= m - tuning[6 - s] <= maxf]


def span_ok(frets):
    fr = [f for f in frets if f > 0]
    if not fr: return True, None
    lo, hi = min(fr), max(fr)
    return (hi - lo + 1 <= (5 if lo >= 7 else 4)), (lo, hi)


def hand_for(frets, h, wide=False):
    fr = [f for f in frets if f > 0]
    if not fr: return h
    for w in (3, 4):
        lo_, hi_ = max(fr) - w, min(fr)
        if w == 4 and not wide: lo_ = max(lo_, 7)
        if lo_ <= hi_: return min(max(h, lo_), hi_)
    return None


def dedupe(notes):
    """one note per pitch per onset (voices that share a note head), the longest kept"""
    best = {}
    for t, d, m in notes:
        k = (t, m)
        if k not in best or best[k] < d: best[k] = d
    return sorted((t, d, m) for (t, m), d in best.items())


def finger(notes, tuning=STD, beam=60, maxf=12, prefer=1):
    """notes: list of (onset, dur, midi), one per pitch per onset (see dedupe). Returns dict index -> (string, fret)."""
    idx = sorted(range(len(notes)), key=lambda i: (notes[i][0], notes[i][2]))
    groups = []
    for i in idx:
        if groups and notes[groups[-1][0]][0] == notes[i][0]: groups[-1].append(i)
        else: groups.append([i])
    # state: (cost, h, {note index: (s, f)} of everything placed, ringing list)
    states = [(0.0, prefer, {}, ())]
    for g in groups:
        t = notes[g[0]][0]
        new = []
        for cost, h, pl, ring in states:
            still = tuple(j for j in ring if notes[j][0] + notes[j][1] > t + Fr(1, 64))
            used = {pl[j][0]: j for j in still}
            opts = [cands(notes[i][2], tuning, maxf) for i in g]
            if any(not o for o in opts): raise ValueError(f'note {notes[g[0]][2]} out of range at {t}')
            for combo in itertools.product(*opts):
                ss = [c[0] for c in combo]
                if len(set(ss)) < len(ss): continue
                # the lowest note on the thickest string of the group
                if any(notes[g[a]][2] < notes[g[b]][2] and combo[a][0] < combo[b][0] for a in range(len(g)) for b in range(len(g))): continue
                c = cost; cut = [j for j in still if pl[j][0] in ss]
                c += 6.0 * len(cut)
                held = [pl[j][1] for j in still if j not in cut]
                frets = [f for s, f in combo] + held
                h2 = hand_for(frets, h)
                if h2 is None:
                    # let held notes go if they make the chord impossible
                    h2 = hand_for([f for s, f in combo], h)
                    if h2 is not None: c += 4.0
                if h2 is None:
                    # a five-fret stretch low on the neck, where the music leaves no other way (marked)
                    h2 = hand_for(frets, h, wide=True)
                    if h2 is None: continue
                    c += 8.0
                c += abs(h2 - h) * 1.2
                c += sum(0.1 * f + 0.1 * max(0, f - 5) for s, f in combo)
                for (s, f), i in zip(combo, g):
                    # a note just played on another string, played again: keep its place
                    for j in reversed(list(pl.keys())[-12:]):
                        if notes[j][2] == notes[i][2]:
                            if pl[j] != (s, f): c += 0.8
                            break
                pl2 = dict(pl); [pl2.__setitem__(i, cmb) for i, cmb in zip(g, combo)]
                ring2 = tuple(j for j in still if j not in cut) + tuple(g)
                new.append((c, h2, pl2, ring2))
        if not new: raise ValueError(f'no fingering at onset {t}')
        new.sort(key=lambda x: x[0])
        # keep the best few, distinct by (hand, strings of ringing notes)
        seen = set(); states = []
        for st in new:
            key = (st[1], tuple(sorted((st[2][j] for j in st[3]))))
            if key in seen: continue
            seen.add(key); states.append(st)
            if len(states) >= beam: break
    return states[0][2]
