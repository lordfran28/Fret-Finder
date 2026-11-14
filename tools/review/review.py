"""The night review of one song page: python3 tools/review/review.py SLUG [--voice] [--sound] [--kf]

Reads the arrangement from the page's own data (DATA.tracks[].bars[].items) and reports, bar by bar:
  grips   every grip's notes against its chord name; one grip per chord; the same diagram twice in a row;
          jumps across the neck when the same chord sits near the hand (unless the jump buys a lower bass)
  voice   (--voice) the singer's track: the locked "With ...'s voice" track opened with the singer key, the guitar
          taken out, the sung notes tracked; any guitar note a half step or a minor 9th from a held sung note;
          every page line that says what he sings, next to what the track says he sings
  sound   (--sound) the guitar track against the diagrams: pitch classes the track plays that the diagram
          doesn't have, and diagram notes the track doesn't play

Needs the arranging kit (/home/claude/kit, /home/claude/scripts) and, for --voice, the singer key in the
scratchpad; neither is in this repository."""
import sys, re, json, os, subprocess, collections
sys.path.insert(0, '/home/claude/kit'); sys.path.insert(0, '/home/claude/scripts')
import numpy as np
import checks  # noqa: F401  (adds the chord qualities the pages use)
import gtr, theory as T

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SP = '/tmp/claude-0/-home-claude/32eff81e-a259-5caa-a171-2530c104e7b0/scratchpad/'
NM = ['C', 'D♭', 'D', 'E♭', 'E', 'F', 'G♭', 'G', 'A♭', 'A', 'B♭', 'B']


def nn(m): return f"{NM[m % 12]}{m // 12 - 1}"


def beats_of(it):
    k = it[0]
    if k == 'K': return sum(h[0] for h in it[3])
    if k in ('C', 'T'): return it[3]
    if k in ('R', 'P', 'Y'): return sum(it[2] if k != 'Y' else it[3])
    if k == 'W': return it[1]
    return 0


def item_notes(it):
    """(midi list, grip or None) the item plays."""
    k = it[0]
    if k in ('K', 'C', 'T'): return gtr.notes(it[2]), it[2]
    if k == 'R': return [gtr.OPEN[6 - s] + f for s, f in it[1]], None
    if k == 'P': return [gtr.OPEN[6 - s] + f for pr in it[1] for s, f in pr], None
    if k in ('X', 'H'): return [gtr.OPEN[6 - s] + f for s, f in it[1]], None
    if k == 'Y': return [gtr.OPEN[6 - s] + f for tri in it[2] for s, f in enumerate(tri[:0])], None
    return [], None


def pos(f):
    fz = [x for x in f if x > 0]
    return sum(fz) / len(fz) if fz else 0.0


def load(slug):
    s = open(f'{ROOT}/songs/{slug}/index.html', encoding='utf-8').read()
    m = re.search(r'const DATA = (\{.*?\});\n', s, re.S)
    if not m: raise SystemExit(f'{slug}: no DATA (an older page)')
    return json.loads(m.group(1)), s


def spans(track):
    """every item with its seconds: (bar label, item, t0, t1)"""
    bars = track['bars']; out = []
    starts = [b.get('start') for b in bars]
    for i, b in enumerate(bars):
        nb = sum(beats_of(it) for it in b['items']) or 4
        t0 = starts[i]
        t1 = starts[i + 1] if i + 1 < len(bars) and starts[i + 1] is not None else None
        if t0 is None: continue
        if t1 is None:
            prev = [(starts[j + 1] - starts[j]) / (sum(beats_of(it) for it in bars[j]['items']) or 4) for j in range(max(0, i - 4), i) if starts[j] is not None and starts[j + 1] is not None]
            t1 = t0 + nb * (float(np.median(prev)) if prev else 0.5)
        spb = (t1 - t0) / nb; x = 0.0
        for it in b['items']:
            bt = beats_of(it)
            out.append((b['label'], it, t0 + x * spb, t0 + (x + bt) * spb if bt else t1)); x += bt
    return out


def grips_report(D):
    rep = []
    for tr in D['tracks']:
        sp = spans(tr); used = collections.defaultdict(list); prev = None; prevlab = None
        for lab, it, t0, t1 in sp:
            if it[0] not in ('K', 'C', 'T'): continue
            name, g = it[1], it[2]
            try: p = gtr.check_grip(g, name, 5 if min([x for x in g if x > 0] or [0]) >= 7 else 4)
            except Exception as e: p = [f'chord name not read ({e})']
            if p: rep.append((tr['key'], lab, 'grip', f"{T.disp(name)} {gtr_str(g)}: " + '; '.join(p)))
            used[name].append((lab, tuple(g)))
            if prev is not None and tuple(g) == tuple(prev[1]) and name == prev[0] and lab != prevlab:
                pass  # a grip that keeps going: the page draws it once
            if prev is not None:
                jump = abs(pos(g) - pos(prev[1]))
                if jump >= 5:
                    near = [f for f in T.find_grips(name, lo=max(1, int(pos(prev[1])) - 3), hi=int(pos(prev[1])) + 4, maxspan=4, min_notes=4, max_notes=6)
                            if 0 not in f and abs(pos(f) - pos(prev[1])) <= 3 and min(gtr.notes(f)) <= min(gtr.notes(g))
                            and gtr.notes(f)[0] % 12 == gtr.notes(g)[0] % 12]
                    if near:
                        best = min(near, key=lambda f: abs(pos(f) - pos(prev[1])))
                        rep.append((tr['key'], lab, 'jump', f"{T.disp(prev[0])} at fret {pos(prev[1]):.0f} → {T.disp(name)} at fret {pos(g):.0f}; the same chord sits at {gtr_str(best)} (fret {pos(best):.0f}), same bass"))
            prev = (name, g); prevlab = lab
        for name, L in used.items():
            gs = collections.Counter(g for _, g in L)
            if len(gs) > 1:
                rep.append((tr['key'], L[0][0], 'one grip', f"{T.disp(name)} has {len(gs)} grips: " + ', '.join(f"{gtr_str(g)} ×{c}" for g, c in gs.most_common())))
    return rep


def gtr_str(g): return ''.join('x' if x < 0 else (str(x) if x < 10 else f'({x})') for x in g)


# ---------------- the singer
def unlock(src, out):
    subprocess.run(['node', SP + 'unlock.mjs', src, out], check=True, capture_output=True)


def read_wav(path, sr=22050):
    r = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-ac', '1', '-ar', str(sr), '-f', 'f32le', '-'], capture_output=True, check=True)
    return np.frombuffer(r.stdout, dtype=np.float32).astype(np.float64)


def versions(tr):
    if tr.get('versions'): return tr['versions']
    return [v for v in ((tr.get('main_label', ''), tr.get('audio')), (tr.get('alt_label', ''), tr.get('audio_alt'))) if v[1]]


def is_guitar(v): return not v[1].endswith('.locked') and (re.search(r'guitar', v[1]) or re.search(r'^guitar alone', v[0], re.I))


def voice_of(slug, tr, work):
    vs = versions(tr)
    lk = [v for v in vs if re.search(r'voice|guide|sing|dean|perry|with ', v[1] + ' ' + v[0], re.I) and not is_guitar(v)]
    gt = [v for v in vs if is_guitar(v)]
    if not lk or not gt: return None, 'no singer track and guitar-alone track to compare'
    d = f'{ROOT}/songs/{slug}/'
    sep = work + tr['key'] + '-voc.wav'          # a voice separated from the locked track, when the track has more than guitar and voice
    if os.path.exists(sep):
        read_wav(sep).astype(np.float32).tofile(work + 'v.f32')
        subprocess.run(['python3', '/home/claude/lafa/work/f0p.py', work + 'v.f32', work + 'v_'], check=True, capture_output=True)
        return (0.0, 1.0), None
    mixp = work + 'mix.mp3'
    if lk[0][1].endswith('.locked'): unlock(d + lk[0][1], mixp)
    else: mixp = d + lk[0][1]
    mix = read_wav(mixp); g = read_wav(d + gt[0][1])
    if mixp.startswith(work): os.remove(mixp)
    n = min(len(mix), len(g)); mix, g = mix[:n], g[:n]
    a = float(np.dot(mix, g) / np.dot(g, g))
    v = mix - a * g
    left = float(np.sqrt(np.mean(v ** 2)) / np.sqrt(np.mean(mix ** 2)))
    v.astype(np.float32).tofile(work + 'v.f32')
    subprocess.run(['python3', '/home/claude/lafa/work/f0p.py', work + 'v.f32', work + 'v_'], check=True, capture_output=True)
    return (a, left), None


def sung_segments(work):
    f0 = np.load(work + 'v_f0.npy'); pk = np.load(work + 'v_pk.npy'); E = np.load(work + 'v_E.npy'); tt = np.load(work + 'v_t.npy')
    from scipy.ndimage import median_filter
    vm = median_filter(69 + 12 * np.log2(np.maximum(f0, 1) / 440), size=9)
    voiced = (pk > 0.35) & (E > np.percentile(E, 45)) & (f0 > 60)
    out = []; cur = None
    for i in np.where(voiced)[0]:
        if cur and i == cur[1] + 1 and abs(vm[i] - np.median(vm[cur[0]:i])) < 0.6: cur[1] = i; continue
        if cur and cur[1] - cur[0] > 16: out.append(cur)
        cur = [i, i]
    seg = [(tt[a], tt[b], float(np.median(vm[a:b + 1]))) for a, b in out]
    off = float(np.median([p - round(p) for _, _, p in seg])) if seg else 0.0
    return [(a, b, int(round(p - off))) for a, b, p in seg], off


def voice_report(D, html, slug):
    rep = []; work = SP + 'night/rv_' + slug + '/'; os.makedirs(work, exist_ok=True)
    for tr in D['tracks']:
        info, why = voice_of(slug, tr, work)
        if why: rep.append((tr['key'], '-', 'voice', why)); continue
        seg, off = sung_segments(work)
        rep.append((tr['key'], '-', 'voice', f"singer tuning {off:+.2f} semitones; guitar taken out at ×{info[0]:.3f}, {info[1]:.0%} of the track left as voice; {len(seg)} held notes"))
        sp = spans(tr); bybar = collections.defaultdict(float); ex = collections.defaultdict(list)
        sung_in = collections.defaultdict(collections.Counter)
        for lab, it, t0, t1 in sp:
            for a, b, q in seg:
                ov = min(b, t1) - max(a, t0)
                if ov <= 0: continue
                sung_in[lab][NM[q % 12]] += ov
                if it[0] not in ('K', 'C', 'T'): continue
                for m in set(item_notes(it)[0]):
                    d = m - q
                    if abs(d) in (1, 13) and ov > 0.12:
                        bybar[lab] += ov; ex[lab].append((round(ov, 2), f"{T.disp(it[1])}: {nn(m)} against sung {nn(q)}"))
        for lab, w in bybar.items():
            if w > 0.3: rep.append((tr['key'], lab, 'rub', f"{w:.1f} s: " + '; '.join(x for _, x in sorted(ex[lab], reverse=True)[:3])))
        # page lines that say what he sings
        for b in tr['bars']:
            texts = [b.get('note') or ''] + [str(o.get('lab', '')) for it in b['items'] if isinstance(it[-1], dict) for o in [it[-1]]]
            for tx in texts:
                for sent in re.split(r'(?<=[.;:])\s', tx):
                    if re.search(r'\bsings?\b|\bsung\b|\bmelody\b|\bvoice\b', sent) and re.search(r'\b[A-G][♭♯b#]?\b', sent):
                        top = ', '.join(f"{k} {v:.1f}s" for k, v in sung_in[b['label']].most_common(4))
                        rep.append((tr['key'], b['label'], 'says', f"“{sent.strip()[:150]}” · track: {top or 'no held note'}"))
    return rep


# ---------------- the sound
def sound_report(D, slug):
    rep = []
    for tr in D['tracks']:
        gt = [v for v in versions(tr) if is_guitar(v)]
        if not gt: continue
        x = read_wav(f'{ROOT}/songs/{slug}/{gt[0][1]}', 22050)
        from scipy.signal import stft
        f, t, Z = stft(x, fs=22050, nperseg=8192, noverlap=8192 - 512, boundary=None, padded=False)
        M = np.abs(Z)
        midi = 69 + 12 * np.log2(np.maximum(f, 1) / 440)
        band = (f > 70) & (f < 1400)
        pcmap = np.zeros((12, len(f)))
        for i in np.where(band)[0]:
            r = round(midi[i])
            if abs(midi[i] - r) < 0.3: pcmap[r % 12, i] = 1.0
        C = pcmap @ (M ** 1.0)
        # what the diagram would sound like through the same lens: each note with its harmonics
        def expected(ns):
            e = np.zeros(len(f))
            for m in ns:
                f0 = 440 * 2 ** ((m - 69) / 12)
                for h in range(1, 7):
                    i = int(round(h * f0 / (f[1] - f[0])))
                    if i < len(f): e[i] += 0.6 ** (h - 1)
            return pcmap @ e
        for lab, it, t0, t1 in spans(tr):
            if it[0] not in ('K', 'C', 'T') or t1 - t0 < 0.6: continue
            s = (t >= t0 + min(0.3, 0.3 * (t1 - t0))) & (t < t0 + 0.9 * (t1 - t0))   # past the last chord's release
            if not s.any(): continue
            c = C[:, s].mean(1); c = c / (c.max() + 1e-9)
            e = expected(gtr.notes(it[2])); e = e / (e.max() + 1e-9)
            want = {m % 12 for m in gtr.notes(it[2])}
            extra = [NM[p] for p in range(12) if p not in want and c[p] > 0.4 and c[p] - e[p] > 0.3]
            missing = [NM[p] for p in want if c[p] < 0.08]
            if extra or missing:
                rep.append((tr['key'], lab, 'sound', f"{T.disp(it[1])} {gtr_str(it[2])} at {t0:.1f}s: track has {', '.join(extra) or '-'} not in the diagram; diagram's {', '.join(missing) or '-'} not heard"))
    return rep


if __name__ == '__main__':
    slug = sys.argv[1]
    D, html = load(slug)
    rep = grips_report(D)
    if '--voice' in sys.argv: rep += voice_report(D, html, slug)
    if '--sound' in sys.argv: rep += sound_report(D, slug)
    if '--kf' in sys.argv: rep += kf_report(slug, '--voice' in sys.argv)
    print(f'== {slug}: {sum(len(t["bars"]) for t in D["tracks"])} bars in {len(D["tracks"])} track(s)')
    for k, lab, kind, msg in rep: print(f'[{kind:8s}] {k:>5s} {lab:>9s}  {msg}', flush=True)


# ---------------- Key Finder: the same song's piano page
KF = '/home/claude/key-finder/songs/'


def kf_load(slug):
    h = open(KF + slug + '/index.html', encoding='utf-8').read()
    return json.loads(re.search(r'<script id="kf-data"[^>]*>(.*?)</script>', h, re.S).group(1))


def kf_name(c):
    c = c.replace('♭', 'b').replace('♯', '#').replace('ø7', 'm7b5').replace('ø', 'm7b5').replace('°7', 'dim7').replace('°', 'dim').replace('Δ', 'maj')
    return c


def kf_report(slug, voice=True):
    rep = []
    try: d = kf_load(slug)
    except FileNotFoundError: return [('kf', '-', 'kf', 'not on Key Finder')]
    segs = {}; seq = []
    for b in d['bars']:
        for s in b['segs']:
            segs[s['id']] = (b['n'], s); seq.append(s['id'])
    shapes = collections.defaultdict(set)
    for sid in seq:
        lab, s = segs[sid]
        nm = kf_name(s['c'])
        try: allowed = T.pcs_of(nm)
        except Exception as e: rep.append(('kf', lab, 'name', f"{s['c']}: not read ({e})")); continue
        ks = s['lh'] + s['rh']
        bad = [nn(k) for k in ks if k % 12 not in allowed]
        if bad: rep.append(('kf', lab, 'shape', f"{s['c']}: {', '.join(bad)} not in the chord"))
        shapes[s['c']].add((tuple(s['lh']), tuple(s['rh'])))
    for c, v in shapes.items():
        if len(v) > 1: rep.append(('kf', '-', 'one shape', f"{c} has {len(v)} shapes"))
    if not voice: return rep
    work = SP + 'night/kv_' + slug + '/'; os.makedirs(work, exist_ok=True)
    lk = [f for f in os.listdir(KF + slug) if f.endswith('.mp3.locked')]
    pn = [f for f in os.listdir(KF + slug) if f.endswith('-piano.mp3')]
    if not lk or not pn: return rep + [('kf', '-', 'voice', 'no singer track')]
    unlock(KF + slug + '/' + lk[0], work + 'mix.mp3'); mix = read_wav(work + 'mix.mp3'); os.remove(work + 'mix.mp3')
    p = read_wav(KF + slug + '/' + pn[0]); n = min(len(mix), len(p)); mix, p = mix[:n], p[:n]
    a = float(np.dot(mix, p) / np.dot(p, p)); v = mix - a * p
    left = float(np.sqrt(np.mean(v ** 2)) / np.sqrt(np.mean(mix ** 2)))
    v.astype(np.float32).tofile(work + 'v.f32')
    subprocess.run(['python3', '/home/claude/lafa/work/f0p.py', work + 'v.f32', work + 'v_'], check=True, capture_output=True)
    seg, off = sung_segments(work)
    rep.append(('kf', '-', 'voice', f"piano taken out at ×{a:.3f}, {left:.0%} left as voice; tuning {off:+.2f}; {len(seg)} held notes"))
    bybar = collections.defaultdict(float); ex = collections.defaultdict(list)
    for t0, k, hand, t1, sid in d['events']:
        lab, s = segs.get(sid, ('?', {'c': '?'}))
        for a0, b0, q in seg:
            ov = min(b0, t1) - max(a0, t0)
            if ov > 0.12 and abs(k - q) in (1, 13):
                bybar[lab] += ov; ex[lab].append((round(ov, 2), f"{s['c']}: {nn(k)} against sung {nn(q)}"))
    for lab, w in bybar.items():
        if w > 0.3: rep.append(('kf', lab, 'rub', f"{w:.1f} s: " + '; '.join(x for _, x in sorted(ex[lab], reverse=True)[:3])))
    return rep
