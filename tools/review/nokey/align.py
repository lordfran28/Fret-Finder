# python3 align.py GUITAR RECORD : semitone shift (record - page) and time offset (record = page + off), by chroma
import sys, numpy as np, librosa
g, sr = librosa.load(sys.argv[1], sr=22050, mono=True); r, _ = librosa.load(sys.argv[2], sr=22050, mono=True)
h = 2048
G = librosa.feature.chroma_cqt(y=g, sr=sr, hop_length=h); R = librosa.feature.chroma_cqt(y=r, sr=sr, hop_length=h)
G = (G - G.mean(1, keepdims=True)); R = (R - R.mean(1, keepdims=True))
dt = h / sr; best = []
for semi in range(12):
    Rr = np.roll(R, -semi, axis=0)
    for lag in range(-int(10 / dt), int(10 / dt)):
        a = max(0, lag); b = max(0, -lag); n = min(G.shape[1] - b, Rr.shape[1] - a)
        c = float((G[:, b:b + n] * Rr[:, a:a + n]).sum() / n)
        best.append((c, semi, lag * dt))
best.sort(reverse=True); print([(round(c, 3), s, round(o, 2)) for c, s, o in best[:6]])
# windows: offset per 30 s
c0, semi, off = best[0]; Rr = np.roll(R, -semi, axis=0)
for w0 in range(0, int(G.shape[1] * dt) - 20, 20):
    i0 = int(w0 / dt); i1 = int((w0 + 20) / dt); res = []
    for lag in range(int((off - 3) / dt), int((off + 3) / dt)):
        if i0 + lag < 0 or i1 + lag > Rr.shape[1]: continue
        res.append(((G[:, i0:i1] * Rr[:, i0 + lag:i1 + lag]).sum(), lag * dt))
    if res: print(w0, round(max(res)[1], 2))
