"""Check every guitar recording in assets/guitar: a good note starts at once and its harmonics stand well above the noise
(h1, h2: dB of the harmonics in 0.05-0.35 s and 0.35-0.8 s after the note starts; a star marks a late start).
A note under about 3 dB in h1 is dead or broken: replace it from its neighbour on the same string."""
import sys, json, os, numpy as np, librosa
sys.path.insert(0, '/home/claude/tools'); import render
man = render._man; SR = 44100
res = {}
for s in range(6, 0, -1):
    for k in sorted(man[str(s)], key=int):
        m = int(k); y = render.sample(s, m)
        f0 = 440 * 2 ** ((m - 69) / 12)
        fr = int(0.02 * SR); n = min(len(y), int(2.0 * SR))
        e = np.array([np.sqrt(np.mean(y[i:i + fr] ** 2)) + 1e-9 for i in range(0, n - fr, fr)])
        on = int(np.argmax(20 * np.log10(e / e.max()) > -10)) * 0.02
        out = []
        for a0, a1 in ((0.05, 0.35), (0.35, 0.8)):
            seg = y[int((on + a0) * SR):int((on + a1) * SR)]
            if len(seg) < 1024: out.append(-120); continue
            S = np.abs(np.fft.rfft(seg * np.hanning(len(seg)))) ** 2 / len(seg); f = np.fft.rfftfreq(len(seg), 1 / SR)
            h = sum(S[(f > k * f0 * 0.985) & (f < k * f0 * 1.015)].sum() for k in range(1, 10))
            out.append(10 * np.log10(h + 1e-15))
        res['%d/%d' % (s, m)] = dict(on=round(on, 2), h1=round(out[0], 1), h2=round(out[1], 1))
json.dump(res, open('scores2.json', 'w'))
for s in range(6, 0, -1):
    print('string', s, ' '.join('%s:%.0f/%.0f%s' % (librosa.midi_to_note(int(k.split('/')[1])), v['h1'], v['h2'], '*' if v['on'] > 0.08 else '') for k, v in res.items() if k.startswith('%d/' % s)))
