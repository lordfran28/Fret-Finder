# python3 vline2.py SLUG A B STEP SEMI : pitch from the cached pyin (record time), minus SEMI
import numpy as np, sys
slug=sys.argv[1]; a, b, st, semi = map(float, sys.argv[2:6])
d = np.load('/tmp/night/%s_f0.npz' % slug); f0 = d['f0']; dt = 256 / 22050
m = 12 * np.log2(np.where(f0 > 0, f0, np.nan) / 440) + 69 - semi
N = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
t = a; out = []
while t < b - 1e-6:
    s = m[int(t / dt):int((t + st) / dt)]; g = s[~np.isnan(s)]
    if len(g) > 0.4 * len(s): x = np.median(g); out.append('%6.2f %s%d%+03.0f' % (t, N[int(round(x)) % 12], int(round(x)) // 12 - 1, 100 * (x - round(x))))
    else: out.append('%6.2f   .     ' % t)
    t += st
for i in range(0, len(out), 8): print(' | '.join(out[i:i + 8]))
