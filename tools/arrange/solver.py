"""Find guitar grips that carry a given voicing: the bass and the top exact, as many inner voices as fit.
frets are listed low E..high E (index 0 = 6th string); -1 = not played."""
import itertools
OPEN = [40, 45, 50, 55, 59, 64]
NM = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
def nm(p): return NM[p % 12] + str(p // 12 - 1)
def midi(s):
    s = s.strip(); i = 2 if len(s) > 1 and s[1] in 'b#' else 1
    pc = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}[s[0]] + (1 if s[1:i] == '#' else -1 if s[1:i] == 'b' else 0)
    return pc + 12 * (int(s[i:]) + 1)
def sounding(f): return [OPEN[j] + f[j] for j in range(6) if f[j] >= 0]
def playable(f, maxspan=None):
    fr = [(j, x) for j, x in enumerate(f) if x > 0]
    if not fr: return True
    lo = min(x for _, x in fr); hi = max(x for _, x in fr)
    span = hi - lo
    lim = maxspan if maxspan is not None else (3 if lo < 5 else 4)   # 4 frets below the 5th fret, 5 from the 7th up (span = hi-lo)
    if span > lim: return False
    # fingers: notes at the lowest fret on several strings can be one barre if no open string lies between them
    at_lo = [j for j, x in fr if x == lo]
    n = len(fr)
    if len(at_lo) > 1:
        a, b = min(at_lo), max(at_lo)
        if not any(f[k] == 0 for k in range(a, b + 1)): n -= len(at_lo) - 1
    return n <= 4
def search(pcs, bass, top, inner=(), prev=None, lo=0, hi=12, need=None, open_ok=False, maxspan=None, nmax=5):
    """pcs: allowed pitch classes; bass, top: midi (exact); inner: wanted midi notes; returns grips ranked"""
    pcs = set(p % 12 for p in pcs)
    choices = []
    for j in range(6):
        opts = [-1]
        for x in range(lo if lo > 0 else 0, hi + 1):
            if x == 0 and not open_ok: continue
            if x > 0 and x < lo: continue
            if (OPEN[j] + x) % 12 in pcs: opts.append(x)
        if 0 not in opts and open_ok and (OPEN[j]) % 12 in pcs: opts.append(0)
        choices.append(opts)
    res = []
    for f in itertools.product(*choices):
        s = sounding(f)
        if len(s) < 3 or len(s) > nmax: continue
        if min(s) != bass or max(s) != top: continue
        if not playable(f, maxspan): continue
        if need and not set(need) <= set(p % 12 for p in s): continue
        if len(set(s)) < len(s): continue
        hit = sum(1 for p in inner if p in s)
        pcm = len(set(p % 12 for p in s) & pcs)
        mv = 0
        if prev:
            mv = sum(abs(a - b) for a, b in zip(f, prev) if a > 0 and b > 0) + 1.5 * sum(1 for a, b in zip(f, prev) if (a >= 0) != (b >= 0))
        fr = [x for x in f if x > 0]
        pos = abs(sum(fr) / len(fr) - 5.5) if fr else 3
        score = hit * 3 + pcm * 1.5 - mv * 0.35 - pos * 0.25 + len(s) * 0.3
        res.append((score, list(f)))
    res.sort(key=lambda r: -r[0])
    return res
def show(f): return '[' + ','.join(str(x) if x >= 0 else 'x' for x in f) + '] ' + ' '.join(nm(p) for p in sounding(f))
if __name__ == '__main__':
    import sys
    for sc, f in search([10, 2, 5], midi('Bb2'), midi('D4'), [midi('F3'), midi('Bb3')])[:6]: print(round(sc, 1), show(f))
