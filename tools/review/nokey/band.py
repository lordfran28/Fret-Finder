# python3 band.py SLUG INSTR SEMI OFF BAR:BEAT0-BEAT1 ... : the band's pitch classes (page key) in those beats, strongest first
import sys, numpy as np, librosa
sys.path.insert(0, '/home/claude/cp'); import cplib, rpage
slug, inst, semi, off = sys.argv[1], sys.argv[2], int(sys.argv[3]), float(sys.argv[4])
S = cplib.Song(slug); bars = S.T['bars']; starts = [float(b['start']) for b in bars] + [float(bars[-1]['start']) + 3]
lab = {b['label']: i for i, b in enumerate(bars)}
y, sr = librosa.load(inst, sr=22050, mono=True)
N = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'G#', 'A', 'Bb', 'B']
for spec in sys.argv[5:]:
    b, r = spec.split(':'); a, z = map(float, r.split('-'))
    i = lab[b]; nb = rpage.bar_beats(bars[i]['items']) or 4; L = starts[i + 1] - starts[i]
    t0 = starts[i] + (a - 1) / nb * L + off; t1 = starts[i] + (z - 1) / nb * L + off
    seg = y[int(t0 * sr):int(t1 * sr)]
    C = librosa.feature.chroma_cqt(y=seg, sr=sr, hop_length=512).mean(1); C = np.roll(C, -semi); C /= C.max()
    o = np.argsort(-C)
    print('bar %s beats %g-%g: ' % (b, a, z) + ' '.join('%s %.2f' % (N[k], C[k]) for k in o[:7]))
