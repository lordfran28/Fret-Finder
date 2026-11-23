# python3 altg.py SLUG SEMI OFF : for every chord with several grips, where each grip is used, and whether the main grip
# (the most used) would put a note a half step or minor 9th from what is sung there (sung pitch per 0.1 s, held >= 0.5 s)
import sys, copy, collections, numpy as np
sys.path.insert(0, '/home/claude/cp'); import cplib, rpage
slug = sys.argv[1]; semi = float(sys.argv[2]); off = float(sys.argv[3])
S = cplib.Song(slug); T = S.T; starts = [float(b['start']) for b in T['bars']] + [float(T['bars'][-1]['start']) + 3]
d = np.load('/tmp/night/%s_f0.npz' % slug); f0 = d['f0']; dt = 256 / 22050
m = 12 * np.log2(np.where(f0 > 0, f0, np.nan) / 440) + 69 - semi
OPEN = [40, 45, 50, 55, 59, 64]
use = collections.defaultdict(list)
for bi, b in enumerate(T['bars']):
    nb = rpage.bar_beats(b['items']) or 4; L = starts[bi + 1] - starts[bi]; q = 0
    for it in b['items']:
        if it[0] == 'K':
            dur = sum(h[0] for h in it[3]); use[it[1]].append((tuple(it[2]), b['label'], starts[bi] + q / nb * L, starts[bi] + (q + dur) / nb * L)); q += dur
        elif it[0] == 'C': use[it[1]].append((tuple(it[2]), b['label'], starts[bi] + q / nb * L, starts[bi] + (q + it[3]) / nb * L)); q += it[3]
        elif it[0] == 'R': q += sum(it[2])
        elif it[0] in ('X',): q += it[2]
        elif it[0] == 'W': q += it[1]
def sungheld(t0, t1):
    out = []; t = t0
    while t < t1:
        g = m[int((t + off) / dt):int((t + off + 0.1) / dt)]; g = g[~np.isnan(g)]
        out.append(int(round(np.median(g))) if len(g) > 4 else None); t += 0.1
    # runs of the same pitch >= 0.5 s
    res = []; i = 0
    while i < len(out):
        j = i
        while j < len(out) and out[j] == out[i]: j += 1
        if out[i] is not None and (j - i) >= 5: res.append(out[i])
        i = j
    return res
for name, L in use.items():
    gs = collections.Counter(g for g, *_ in L)
    if len(gs) < 2: continue
    main = gs.most_common(1)[0][0]
    fs = lambda g: ''.join('x' if v < 0 else (str(v) if v < 10 else '(%d)' % v) for v in g)
    print(name, {fs(g): n for g, n in gs.items()}, 'main', fs(main))
    for g, lab, t0, t1 in L:
        if g == main: continue
        notes = [OPEN[i] + v for i, v in enumerate(main) if v >= 0]
        sh = sungheld(t0, t1)
        rub = sorted({cplib.nm(n) + '/' + cplib.nm(s) for n in notes for s in sh if abs(n - s) in (1, 13)})
        print('   bar %-4s %s instead: sung held %s; main grip would rub: %s' % (lab, fs(g), [cplib.nm(s) for s in sh], rub or 'no'))
