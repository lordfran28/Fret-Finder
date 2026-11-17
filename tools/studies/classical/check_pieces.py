"""Independent check of the Sor pages: every bar's notes, turned back into pitches from their string and fret, must be
exactly the source's notes (Mutopia, parsed again here; held duplicates merged) at the same onsets, in playing order;
one note per string at a time; frets within the stated limit; each bar's length right. python3 check_pieces.py PART"""
import sys
sys.path.insert(0, '/home/claude/studies/classical'); sys.path.insert(0, '/home/claude/studies')
from fractions import Fraction as Fr
import lyparse as L, check_sor as CS, sor as SR, pieces as PC

OPEN = [40, 45, 50, 55, 59, 64]
part = sys.argv[1]
probs = []
for k in SR.PARTS[part]:
    S = SR.STUDIES[k]
    P = L.parse(CS.M + CS.T[k])
    sh = S.get('shift', 0)
    want = {}
    for t, du, ms, v in P['notes']:
        want.setdefault(Fr(t) * 4, set()).add(ms + sh)
    bars, _ = PC.piece_bars(CS.M + CS.T[k], k, fixes=S.get('fixes', ()), maxf=S.get('maxf', 12), shift=sh)
    fixed = {(Fr(ft), w, r) for ft, w, r in S.get('fixes', ())}
    for ft, w, r in fixed:
        if ft in want and w in want[ft]: want[ft].discard(w); want[ft].add(r)
    got, t = {}, Fr(0)
    n_, d_ = P['time']; bl = Fr(n_, d_) * 4
    for B in bars:
        t0 = t
        for it in B['items']:
            if it[0] == 'W': t += Fr(it[1]).limit_denominator(96); continue
            for g, d in zip(it[1], it[2]):
                strs = [s for s, f in g]
                if len(strs) != len(set(strs)): probs.append(f'{B["label"]}: two notes on one string')
                if any(not 0 <= f <= S.get('maxf', 12) for s, f in g): probs.append(f'{B["label"]}: fret out of range')
                if g: got.setdefault(t, set()).update(OPEN[6 - s] + f for s, f in g)
                t += Fr(d).limit_denominator(96)
        if abs((t - t0) - Fr(B['beats']).limit_denominator(96)) > Fr(1, 96): probs.append(f'{B["label"]}: bar length')
    if got != want:
        ks = sorted(set(got) | set(want))
        bad = [x for x in ks if got.get(x) != want.get(x)]
        probs.append(f'{k}: {len(bad)} onsets differ from the source, first at beat {bad[0]}: {sorted(got.get(bad[0], []))} vs {sorted(want.get(bad[0], []))}')
    lo = min(m for s in want.values() for m in s)
    if lo < 40: probs.append(f'{k}: a note below the low E ({lo})')
    print(k, 'bars', len(bars), 'onsets', len(want), 'range', lo, max(m for s in want.values() for m in s))
print('\n'.join(probs) if probs else 'all good')
sys.exit(1 if probs else 0)
