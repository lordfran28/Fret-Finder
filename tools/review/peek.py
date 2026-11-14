# what the guitar track plays in a bar, note by note (strongest fundamentals), next to the diagram
import sys, json; sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__))); import review as R, numpy as np
from scipy.signal import stft
slug, key = sys.argv[1], sys.argv[2]; labs = sys.argv[3].split(',')
D, _ = R.load(slug); tr = [t for t in D['tracks'] if t['key'] == key][0]
gt = [v for v in R.versions(tr) if R.is_guitar(v)][0]
x = R.read_wav(f'/home/claude/fret-finder/songs/{slug}/{gt[1]}')
f, t, Z = stft(x, fs=22050, nperseg=8192, noverlap=8192 - 512, boundary=None, padded=False); M = np.abs(Z)
midi = 69 + 12 * np.log2(np.maximum(f, 1) / 440)
for lab, it, t0, t1 in R.spans(tr):
    if lab not in labs: continue
    desc = it[1] + ' ' + R.gtr_str(it[2]) + ' ' + str([R.nn(m) for m in R.item_notes(it)[0]]) if it[0] in 'KCT' else it[0] + ' ' + json.dumps(it[1])[:80]
    print(f'{lab} {t0:.2f}-{t1:.2f} {desc}  opts={json.dumps(it[-1])[:120] if isinstance(it[-1], dict) else ""}')
    for a in np.arange(t0, t1 - 0.05, max(0.25, (t1 - t0) / 6)):
        s = (t >= a) & (t < a + 0.25); spec = M[:, s].mean(1); e = {}
        for m in range(38, 84):
            i = np.argmin(abs(midi - m)); e[m] = spec[i - 1:i + 2].max()
        top = sorted(e, key=e.get, reverse=True)[:6]
        print(f'   {a:.2f}', ' '.join(f'{R.nn(m)}{e[m] / e[top[0]]:.1f}' for m in top))
