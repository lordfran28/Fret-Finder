# python3 vc.py SLUG STEM [SEMI OFF] : Rod's line from a vocal stem against the page: the page's 'sings' claims and the guitar's rubs
import sys, json, os, numpy as np, librosa
sys.path.insert(0, '/home/claude/cp')
import cplib
slug, stem = sys.argv[1], sys.argv[2]
S = cplib.Song(slug)
T = S.T; bars = T['bars']; starts = [float(b['start']) for b in bars]
cache = '/tmp/night/%s_f0.npz' % slug
if not os.path.exists(cache):
    y, sr = librosa.load(stem, sr=22050, mono=True)
    f0, vf, vp = librosa.pyin(y, fmin=70, fmax=700, sr=sr, hop_length=256, frame_length=2048)
    np.savez(cache, f0=f0, vp=vp)
d = np.load(cache); f0 = d['f0']; vp = d['vp']; dt = 256 / 22050
m = 12 * np.log2(np.where(f0 > 0, f0, np.nan) / 440) + 69
# the page's claims: (t0, t1, midi) from bar 'mel'
claims = []
for b, s0 in zip(bars, starts):
    pass
D = S.D
form_bars = {fb['n']: fb for p in D['form'] for fb in p['bars']}
bt = lambda i: (starts[i + 1] - starts[i]) / (cplib.rpage.bar_beats(bars[i]['items']) or 4) if i + 1 < len(starts) else 0.6
for i, b in enumerate(bars):
    fb = form_bars.get(b['label'], {})
    for x in (fb.get('mel') or b.get('mel') or []):
        pass
# reuse cplib.show's reading of the sung notes
import io, contextlib, re
buf = io.StringIO()
with contextlib.redirect_stdout(buf): cplib.show(slug)
N = {'C':0,'C#':1,'D':2,'D#':3,'E':4,'F':5,'F#':6,'G':7,'G#':8,'A':9,'A#':10,'B':11}
lab2i = {b['label']: i for i, b in enumerate(bars)}
cur = None
for line in buf.getvalue().splitlines():
    mm = re.match(r'^(\S+)\s{2,}', line)
    if mm and mm.group(1) in lab2i: cur = lab2i[mm.group(1)]; continue
    if 'sings:' in line and cur is not None:
        for nm, oc, a, z in re.findall(r'([A-G]#?)(\d)@([\d.]+)-([\d.]+)', line):
            p = N[nm] + 12 * (int(oc) + 1); beat = bt(cur)
            claims.append((starts[cur] + (float(a) - 1) * beat, starts[cur] + (float(z) - 1) * beat, p, bars[cur]['label']))
def sung(t0, t1, semi, off):
    a, z = int((t0 + off) / dt), int((t1 + off) / dt); g = m[a:z]; g = g[~np.isnan(g)]
    if len(g) < 0.4 * max(1, z - a): return None
    return float(np.median(g)) - semi
if len(sys.argv) > 3: semi, off = float(sys.argv[3]), float(sys.argv[4])
else:
    best = None
    for semi in range(-12, 13):
        for off in np.arange(-8.0, 8.01, 0.1):
            ok = n = 0
            for t0, t1, p, _ in claims:
                if t1 - t0 < 0.5: continue
                s = sung(t0, t1, semi, off)
                if s is None: continue
                n += 1; ok += (round(s) - p) % 12 == 0
            if n and (best is None or ok / n > best[0]): best = (ok / n, semi, off, n)
    print('best fit: %.2f of %d held notes agree at semi %d, offset %.1f s' % (best[0], best[3], best[1], best[2])); semi, off = best[1], best[2]
# claims that the track contradicts
print('page says vs track (held >= 0.5 s):')
bad = 0
for t0, t1, p, lab in claims:
    if t1 - t0 < 0.5: continue
    s = sung(t0, t1, semi, off)
    if s is None: continue
    if (round(s) - p) % 12 != 0:
        bad += 1; print('  bar %-4s %6.2fs page %-4s sung %-4s (%+.0f c)' % (lab, t0, cplib.nm(p) if hasattr(cplib,'nm') else p, cplib.nm(int(round(s))) if hasattr(cplib,'nm') else s, 100 * (s - round(s))))
print(' ', bad, 'disagree')
# the sung line as held segments (>= 0.5 s, steady), put in the page's octave by the claims' median octave
seg = []; i = 0; mm_ = m.copy()
n = len(mm_)
while i < n:
    if np.isnan(mm_[i]): i += 1; continue
    j = i; base = mm_[i]
    while j < n and not np.isnan(mm_[j]) and abs(mm_[j] - np.nanmedian(mm_[i:j + 1])) < 0.6: j += 1
    if (j - i) * dt >= 0.5: seg.append((i * dt - off, j * dt - off, float(np.median(mm_[i:j])) - semi))
    i = max(j, i + 1)
vo = np.median([s[2] for s in seg])
shift = 12 * round((np.median([p for _, _, p, _ in claims]) - vo) / 12) if claims else 0
seg = [(a, z, p + shift) for a, z, p in seg]
print('held sung notes', len(seg), 'octave shift to the page', shift)
# rubs against the guitar, with ring time
import copy
T2 = copy.deepcopy(S.T)
for b in T2['bars']:
    for it in b['items']:
        if it[0] == 'K': it[3] = [h[:2] for h in it[3]]
ev = sorted(S.events(T2), key=lambda e: e['t']); last = {}
for e in ev:
    q = last.get(e['s'])
    if q is not None: q['end'] = min(q.get('end') or 1e9, e['t'])
    last[e['s']] = e
G = [(e['t'], min(e.get('end') or 1e9, e['t'] + 4.0), cplib.OPEN[e['s']] + e['f']) for e in ev]
out = []
for a0, a1, vp_ in seg:
    v = int(round(vp_))
    for g0, g1, gp in G:
        ov = min(a1, g1) - max(a0, g0)
        if ov >= 0.5 and abs(gp - v) in (1, 13):
            bi = max(k for k, s in enumerate(starts) if s <= max(a0, g0) + 1e-6)
            out.append((bars[bi]['label'], round(max(a0, g0), 2), cplib.nm(v), cplib.nm(gp), round(ov, 2), round(100 * (vp_ - v))))
print('rubs (overlap >= 0.5 s):', len(out))
for r in sorted(set(out), key=lambda z: z[1]): print('   bar %-4s %7.2fs sung %-4s guitar %-4s %.2fs (%+d c)' % r)
json.dump({'semi': semi, 'off': off, 'seg': seg}, open('/tmp/night/%s_voice.json' % slug, 'w'))
