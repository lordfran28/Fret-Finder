# python3 rv.py SLUG [TRACKFILE] : grips vs names, one grip per chord, root/3rd struck, rubs vs the VF line, the track vs the diagrams
import sys, copy, collections, numpy as np
sys.path.insert(0, '/home/claude/cp'); sys.path.insert(0, '/home/claude/vfm')
import cplib, ff, rpage
slug = sys.argv[1]
S = cplib.Song(slug); T = copy.deepcopy(S.T)
for b in T['bars']:
    for it in b['items']:
        if it[0] == 'K': it[3] = [h[:2] for h in it[3]]
OPEN = {6: 40, 5: 45, 4: 50, 3: 55, 2: 59, 1: 64}   # string number (6 = low E)
N = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
def gnotes(f):   # f: list low E .. high E
    return {6 - i: OPEN[6 - i] + v for i, v in enumerate(f) if v is not None and v >= 0}
grips = collections.defaultdict(set); probs = []
starts = [float(b['start']) for b in T['bars']]
segs = []   # (t0, t1, name, grip pcs, struck pcs, label)
for bi, b in enumerate(T['bars']):
    nb = rpage.bar_beats(b['items']) or 4
    L = (starts[bi + 1] - starts[bi]) if bi + 1 < len(starts) else 2.5
    q = 0.0
    for it in b['items']:
        k = it[0]
        if k in ('K', 'C'):
            name, f = it[1], it[2]
            dur = sum(h[0] for h in it[3]) if k == 'K' else it[3]
            gn = gnotes(f); gp = {m % 12 for m in gn.values()}
            pcs, R = ff.name_pcs(name)
            grips[name].add(tuple(f))
            bad = sorted({N[p] for p in gp - pcs})
            if bad: probs.append('bar %s %s %s: notes not in the name: %s' % (b['label'], name, f, bad))
            if R is not None:
                third = {(R + 3) % 12, (R + 4) % 12} & pcs
                if 'sus' not in name and third and not (third & gp): probs.append('bar %s %s %s: no 3rd in the grip' % (b['label'], name, f))
                struck = set()
                if k == 'K':
                    for h in it[3]:
                        for s in h[1]:
                            if s in gn: struck.add(gn[s] % 12)
                else: struck = gp
                if 'sus' not in name and third and (third & gp) and not (third & struck): probs.append('bar %s %s: the pattern never sounds the 3rd' % (b['label'], name))
                if R in gp and R not in struck and '/' not in name: probs.append('bar %s %s: the pattern never sounds the root' % (b['label'], name))
            segs.append((starts[bi] + q / nb * L, starts[bi] + (q + dur) / nb * L, name, gp, b['label']))
            q += dur
        elif k == 'R': q += sum(it[2])
        elif k == 'X': q += it[2]
        elif k == 'W': q += it[1]
        elif k == 'P': q += sum(it[2]) if isinstance(it[2], list) else it[2]
        elif k == 'T': q += it[3]
print('grip problems:', len(probs)); [print('  ', p) for p in probs]
multi = {n: g for n, g in grips.items() if len(g) > 1}
print('chords with more than one grip:', {n: [''.join('x' if v < 0 else str(v) for v in f) for f in g] for n, g in multi.items()})
# rubs vs the VF line
V = S.voice()
if V:
    ev = sorted(S.events(T), key=lambda e: e['t']); last = {}
    for e in ev:
        p = last.get(e['s'])
        if p is not None: p['end'] = min(p.get('end') or 1e9, e['t'])
        last[e['s']] = e
    G = [(e['t'], min(e.get('end') or 1e9, e['t'] + 4.0), cplib.OPEN[e['s']] + e['f']) for e in ev]
    out = set()
    for a0, a1, vp in V:
        if a1 - a0 < 0.5: continue
        for g0, g1, gp in G:
            ov = min(a1, g1) - max(a0, g0)
            if ov >= 0.5 and abs(gp - vp) in (1, 13):
                bi = max(i for i, s in enumerate(starts) if s <= max(a0, g0) + 1e-6)
                out.add((T['bars'][bi]['label'], round(max(a0, g0), 2), cplib.nm(vp), cplib.nm(gp), round(ov, 2), 'above' if gp > vp and gp - vp < 12 else ''))
    print('rubs vs the sung line (held >= 0.5 s, overlap >= 0.5 s):', len(out))
    for r in sorted(out, key=lambda z: z[1]): print('   bar %-4s %7.2fs sung %-4s guitar %-4s %.2fs %s' % r)
else: print('no sung line on disk')
# the track vs the diagrams: chroma per chord segment
trk = sys.argv[2] if len(sys.argv) > 2 else None
if trk:
    import librosa
    y, sr = librosa.load(trk, sr=22050, mono=True)
    C = librosa.feature.chroma_cqt(y=y, sr=sr, hop_length=512); hop = 512 / sr
    low = []
    for t0, t1, name, gp, lab in segs:
        if t1 - t0 < 0.4: continue
        c = C[:, int(t0 / hop) + 2:int(t1 / hop)].mean(1); c = c / (c.max() + 1e-9)
        inside = sum(c[p] for p in gp) / (c.sum() + 1e-9)
        out_ = [N[p] for p in range(12) if p not in gp and c[p] > 0.75]
        if out_ or inside < 0.55: low.append((lab, name, round(float(inside), 2), out_))
    print('segments where the track has strong notes the diagram lacks:', len(low))
    for x in low: print('  ', x)
