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
# qualities some pages use that the kit lacks (17 Nov): minor-major 7th, 7♭9 suspended
for _q, _v in {'mmaj7': ({3, 11}, {0, 7}), '7b9sus4': ({5, 10, 1}, {0, 7}), 'm(maj7)': ({3, 11}, {0, 7}), 'maj7(6)': ({4, 11, 9}, {0, 7}), '6/9sus': ({5, 9, 2}, {0, 7})}.items(): gtr.QUAL.setdefault(_q, _v)
gtr.QUAL.setdefault('(add9)', gtr.QUAL['add9'])      # Cloudy writes G(add9)

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


def ascii_name(c):
    """a chord name as the kit reads it: F♯m(maj9) → F#mmaj9"""
    c = c.replace('♭', 'b').replace('♯', '#').replace('Δ', 'maj').replace('ø7', 'm7b5').replace('°7', 'dim7').replace('°', 'dim')
    return re.sub(r'm\(maj(\d+)\)', r'mmaj\1', c)


def load(slug):
    s = open(f'{ROOT}/songs/{slug}/index.html', encoding='utf-8').read()
    m = re.search(r'const DATA = (\{.*?\});\n', s, re.S)
    if m: return json.loads(m.group(1)), s
    # an older page (Barquito de papel): <script id="data"> with bars[].segs[] (chord, grip f, beats) and bar times t
    m = re.search(r'<script id="data"[^>]*>(.*?)</script>', s, re.S)
    d = json.loads(m.group(1)) if m else None
    if isinstance(d, dict) and not d.get('bars') and isinstance(d.get('sections'), list):
        # the same older form with its bars inside sections (If I Ever Lose This Heaven, 17 Nov)
        d = dict(d, bars=[b for sec in d['sections'] for b in sec.get('bars', []) if b.get('segs')])
    pt = re.search(r'<script id="pt-data"[^>]*>(.*?)</script>', s, re.S)
    if isinstance(d, dict) and not d.get('bars') and pt:
        # It Had to Be You (1 Nov): the playing order in pt-data, even beats from t0, grips written "x43544" or with (10)
        P = json.loads(pt.group(1)); spb = 60.0 / P['bpm']; x = P.get('t0', 0.0); bl = []
        def fr(f):
            if isinstance(f, list): return f
            return [-1 if q == 'x' else int(q.strip('()')) for q in re.findall(r'x|\(\d+\)|\d', f or '')]
        for i, b in enumerate(P['bars']):
            segs = [dict(g, f=fr(g.get('f'))) for g in b['segs']]
            bl.append(dict(n=b.get('sub') or str(i + 1), t=b.get('start', round(x, 3)), segs=segs, badge=b.get('badge')))
            x += sum(g.get('beats', 4) for g in b['segs']) * spb
        d = dict(d, bars=bl)
    if not (isinstance(d, dict) and isinstance(d.get('bars'), list) and d['bars'] and 'segs' in d['bars'][0]):
        raise SystemExit(f'{slug}: no DATA (an older page in a form the review does not read)')
    bars = [dict(label=str(b['n']), start=b.get('t'), note=b.get('badge') or '',
                 items=[['K', ascii_name(g['c']), g['f'], [[g.get('beats', 4), 'a']]] if isinstance(g.get('f'), list) and len(g['f']) == 6 else ['W', g.get('beats', 4)] for g in b['segs']]) for b in d['bars']]
    vers = [(lab, src) for src, lab in re.findall(r'data-src="([^"$]+)"[^>]*>([^<]+)<', s)]
    if not vers and isinstance(d.get('audio'), list):             # Heaven names its tracks in its data: [file, label]
        vers = [(a[1], a[0]) for a in d['audio'] if isinstance(a, list) and len(a) >= 2]
    vers.sort(key=lambda v: 0 if re.search(r'alone', v[0], re.I) else 1)   # the guitar alone first, for taking it out of the singer's track
    return dict(tracks=[dict(key='main', bars=bars, versions=vers, old=True)]), s     # old=True: no picking pattern in the data


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
            name, g = ascii_name(it[1]), it[2]          # 17 Nov: the pages also write °7 and ø7 (I Can't Get Started)
            try: p = gtr.check_grip(g, name, 5 if min([x for x in g if x > 0] or [0]) >= 7 else 4)
            except Exception as e: p = [f'chord name not read ({e})']
            if p: rep.append((tr['key'], lab, 'grip', f"{T.disp(name)} {gtr_str(g)}: " + '; '.join(p)))
            used[name].append((lab, tuple(g)))
            if prev is not None and tuple(g) == tuple(prev[1]) and name == prev[0] and lab != prevlab:
                pass  # a grip that keeps going: the page draws it once
            if prev is not None:
                jump = abs(pos(g) - pos(prev[1]))
                if jump >= 5:
                    try: near = [f for f in T.find_grips(name, lo=max(1, int(pos(prev[1])) - 3), hi=int(pos(prev[1])) + 4, maxspan=4, min_notes=4, max_notes=6)
                            if 0 not in f and abs(pos(f) - pos(prev[1])) <= 3 and min(gtr.notes(f)) <= min(gtr.notes(g))
                            and gtr.notes(f)[0] % 12 == gtr.notes(g)[0] % 12]
                    except ValueError: near = []           # a chord name the grip finder doesn't know
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


def notes_report(D):
    """a bar's note that puts the hand at a fret no grip of the bar is at (Fly Me to the Moon bar 11 said "E minor 7
    at the 7th fret" over the open grip 020000, 15 Nov)"""
    rep = []
    for tr in D['tracks']:
        for b in tr['bars']:
            note = b.get('note') or ''
            gs = [it[2] for it in b['items'] if it[0] in ('K', 'C', 'T')]
            # harmonics and runs put the hand at their own frets (bar 61 of I Can't Get Started: harmonics at the 12th)
            gs += [[f if 6 - s_ == i else -1 for i in range(6)] for it in b['items'] if it[0] in ('H', 'R', 'X') for s_, f in it[1]]
            if not gs or 'open' in note.lower(): continue
            for m in re.finditer(r'at the (\d+)(?:st|nd|rd|th)(?:[–-](\d+)(?:st|nd|rd|th))? fret', note):
                lo = int(m.group(1)); hi = int(m.group(2) or lo)
                if not any(any(lo - 1 <= f <= hi + 1 for f in g if f > 0) for g in gs):
                    rep.append((tr['key'], b['label'], 'note', f"says “{m.group(0)}” but the grips are {', '.join(gtr_str(g) for g in gs)}"))
    return rep


def plays_report(D):
    """from the page's own data: a chord whose hits never sound its root, its 3rd or its 7th. A string struck before
    on the same fret still rings and counts, and a chord held across a run in its own bar (the same grip both sides)
    is taken whole. The 7th is told apart: the agreed rule (14 Nov) lets a pattern leave it out."""
    rep = []
    for tr in D['tracks']:
        if tr.get('old'): continue                     # an older page keeps no picking pattern: --sound checks it
        ringing = {}                                   # string -> fret still sounding
        for b in tr['bars']:
            groups = []                                # [name, grip, sounding strings]
            for it in b['items']:
                if it[0] != 'K':
                    if it[0] in ('C', 'T'): ringing = {6 - i: f for i, f in enumerate(it[2]) if f >= 0}
                    elif it[0] in ('R', 'X', 'H'):
                        ringing.update({s: f for s, f in it[1]})
                        # a run in the bar that breaks the chord it follows plays that chord's notes (Misty, bar 36)
                        if it[0] == 'R' and groups:
                            gg = groups[-1][1]
                            hit = {s for s, f in it[1] if 0 < s < 7 and gg[6 - s] == f}
                            groups[-1][2] |= hit; groups[-1][3] |= hit
                    elif it[0] == 'P':
                        ringing.update({s: f for pr in it[1] for s, f in pr})
                        # a fill in thirds down the chord it follows sounds that chord's notes (Somos novios, 17 Nov)
                        if groups: groups[-1][4] |= {(gtr.OPEN[6 - s] + f) % 12 for pr in it[1] for s, f in pr}; groups[-1][3] |= {0}
                    continue
                g = it[2]; idx = [6 - i for i, f in enumerate(g) if f >= 0]       # strings low to high
                masks = {'a': idx, 'b': idx[:1], 't': idx[1:], 'h': idx[-3:], '-': []}
                struck = {s for h in it[3] for s in (h[1] if isinstance(h[1], list) else masks.get(h[1], []))}
                sounding = {s for s in range(1, 7) if g[6 - s] >= 0 and (s in struck or ringing.get(s) == g[6 - s])}
                if groups and groups[-1][0] == it[1] and groups[-1][1] == g: groups[-1][2] |= sounding; groups[-1][3] |= struck
                elif groups and groups[-1][0] == it[1]:
                    # the same chord on a second grip in the same bar (Misty's B major 9, bass first, then the top):
                    # what either grip sounds counts for the chord
                    groups[-1][4] |= {(gtr.OPEN[6 - s] + g[6 - s]) % 12 for s in sounding}; groups[-1][5] |= set(gtr.pcs(g))
                    groups[-1][3] |= struck
                else: groups.append([it[1], g, set(sounding), set(struck), set(), set()])
                ringing = {s: g[6 - s] for s in sounding} | {s: f for s, f in ringing.items() if g[6 - s] == f}
            for name, g, sounding, struck, more, more_g in groups:
                if not struck: continue
                try:
                    r_, q_, _ = gtr.parse(name); req_ = gtr.QUAL[q_][0]
                except Exception: continue
                pcs_ = {(gtr.OPEN[6 - s] + g[6 - s]) % 12 for s in sounding} | more
                want = [(r_, 'root')] + [((r_ + i) % 12, '3rd') for i in (4, 3) if i in req_][:1] + [((r_ + i) % 12, '7th') for i in (10, 11) if i in req_][:1]
                gp = set(gtr.pcs(g)) | more_g
                lost = [(w, f'{NM[p]} ({w})') for p, w in want if p in gp and p not in pcs_]
                hard = [x for w, x in lost if w != '7th']; soft = [x for w, x in lost if w == '7th']
                if hard: rep.append((tr['key'], b['label'], 'plays', f"{T.disp(name)} {gtr_str(g)}: the pattern never sounds {', '.join(hard + soft)}"))
                elif soft: rep.append((tr['key'], b['label'], 'plays 7', f"{T.disp(name)} {gtr_str(g)}: the pattern never sounds {', '.join(soft)}"))
    return rep


# ---------------- the singer
def tidy(work):
    """the voice and its salience take 100 MB a song; only the pitch tracks are kept (17 Nov: the disk filled)"""
    for f in ('v.f32', 'v_sal.npy'):
        try: os.remove(work + f)
        except FileNotFoundError: pass


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
        subprocess.run(['python3', '/home/claude/lafa/work/f0p.py', work + 'v.f32', work + 'v_'], check=True, capture_output=True); tidy(work)
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
    subprocess.run(['python3', '/home/claude/lafa/work/f0p.py', work + 'v.f32', work + 'v_'], check=True, capture_output=True); tidy(work)
    return (a, left), None


WIDE = set()                                   # (start, end) of sung notes whose pitch swings too far to name


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
    # how far the pitch swings inside each held note: Hvorostovsky's vibrato is a semitone wide, so a note between
    # B and C reads as either (16 Nov); such notes are marked, not trusted
    raw = 69 + 12 * np.log2(np.maximum(f0, 1) / 440)
    def swing(a, b):                               # the spread of the voiced pitch in the 0.6 s around the note
        mid = (tt[a] + tt[b]) / 2; w = voiced & (np.abs(tt - mid) < 0.3)
        x = raw[w]; x = x[np.abs(x - np.median(x)) < 2.5] if len(x) else x
        return float(np.std(x)) if len(x) > 4 else 0.0
    WIDE.clear(); WIDE.update({(round(float(tt[a]), 3), round(float(tt[b]), 3)) for a, b in out if swing(a, b) > 0.6})
    # the singer's tuning: a circular mean over the steady frames (a median of rounded fractions misreads a singer
    # who is a quarter tone flat: Dean's flat B♭ read as A, 14 Nov)
    from scipy.ndimage import uniform_filter1d
    ms = uniform_filter1d(vm, 9); steady = voiced & (np.abs(np.gradient(uniform_filter1d(vm, 15))) < 0.045)
    off = float(np.angle(np.mean(np.exp(2j * np.pi * ms[steady]))) / (2 * np.pi)) if steady.any() else 0.0
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
        rec = any(re.search(r"the record\b|record.s (own )?voice", v[0], re.I) for v in versions(tr) if v[1].endswith('.locked'))
        if info[0] < 0.2 and rec:      # 17 Nov: Cloudy's "With the record's voice" is the record's own singer, no guitar in it
            rep.append((tr['key'], '-', 'voice', f"the singer's track is the record's own voice (×{info[0]:.3f} of the guitar in it), as its name says"))
        elif info[0] < 0.2:
            rep.append((tr['key'], '-', 'voice', f"the singer's track holds almost none of the guitar-alone track (×{info[0]:.3f}): its guitar is another take, so what he hears with the singer is not what the diagrams show"))
        wide = collections.defaultdict(float)
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
                        if (round(float(a), 3), round(float(b), 3)) in WIDE: wide[lab] += ov
        for lab, w in bybar.items():
            if w > 0.3:
                tag = ' · the sung note swings more than a semitone: check by ear' if wide[lab] > 0.6 * w else ''
                rep.append((tr['key'], lab, 'rub', f"{w:.1f} s: " + '; '.join(x for _, x in sorted(ex[lab], reverse=True)[:3]) + tag))
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
            if it[0] == 'R' and t1 > t0:
                # a run, a line or a bass under it: every note of its diagram heard at its own time
                bt = sum(it[2]) or 1; spb = (t1 - t0) / bt; x = 0.0; miss = []
                for (s_, f_), d in zip(it[1], it[2]):
                    on = t0 + x * spb; x += d
                    w = (t >= on + 0.03) & (t < on + max(0.08, min(0.3, 0.8 * d * spb)))
                    if not w.any(): continue
                    c = C[:, w].mean(1); c = c / (c.max() + 1e-9)
                    m = gtr.OPEN[6 - s_] + f_
                    if c[m % 12] < 0.22: miss.append(f"{nn(m)} (string {s_}, fret {f_}) at {on:.1f}s")
                if miss: rep.append((tr['key'], lab, 'sound', f"run over {T.disp(it[3]) if len(it) > 3 and isinstance(it[3], str) else ''}: diagram's {'; '.join(miss[:4])} not heard"))
                continue
            if it[0] not in ('K', 'C', 'T') or t1 - t0 < 0.6: continue
            s = (t >= t0 + min(0.3, 0.3 * (t1 - t0))) & (t < t0 + 0.9 * (t1 - t0))   # past the last chord's release
            if not s.any(): continue
            c = C[:, s].mean(1); c = c / (c.max() + 1e-9)
            e = expected(gtr.notes(it[2])); e = e / (e.max() + 1e-9)
            want = {m % 12 for m in gtr.notes(it[2])}
            # a note "not in the diagram" counts only away from the diagram's own overtones: the open low E's 3rd
            # harmonic is a B an octave and a fifth up, and in It Keeps You Runnin's E13 it rang louder than the E (17 Nov)
            hm = np.ones(len(f), bool)
            for m in set(gtr.notes(it[2])):
                for h in (3, 5, 6):
                    hm &= np.abs(midi - (m + 12 * np.log2(h))) > 0.3
            cx = (pcmap * hm) @ M[:, s].mean(1); cx = cx / (C[:, s].mean(1).max() + 1e-9)
            extra = [NM[p] for p in range(12) if p not in want and c[p] > 0.4 and cx[p] > 0.4 and c[p] - e[p] > 0.3]
            missing = [NM[p] for p in want if c[p] < 0.08]
            # the root and the 3rd, by their own fundamentals (a pitch class can hide in another note's overtones:
            # Barquito's E9 kept E but never played its G♯, 15 Nov)
            try:
                r_, q_, _ = gtr.parse(it[1]); req_ = gtr.QUAL[q_][0]
                third = next(((r_ + i) % 12 for i in (4, 3) if i in req_), None)
            except Exception: r_, third = None, None
            fe = {}
            for m in set(gtr.notes(it[2])):
                fq = 440 * 2 ** ((m - 69) / 12); i = int(round(fq / (f[1] - f[0])))
                fe[m] = float(M[max(0, i - 1):i + 2, s].mean(1).max())
            top = max(fe.values()) if fe else 0
            for p, what in ((r_, 'root'), (third, '3rd')):
                if p is None or top <= 0: continue
                ms = [m for m in fe if m % 12 == p]
                if ms and max(fe[m] for m in ms) < 0.06 * top and NM[p] not in missing: missing.append(f'{NM[p]} ({what})')
            if extra or missing:
                rep.append((tr['key'], lab, 'sound', f"{T.disp(it[1])} {gtr_str(it[2])} at {t0:.1f}s: track has {', '.join(extra) or '-'} not in the diagram; diagram's {', '.join(missing) or '-'} not heard"))
    return rep


def cp_report(html):
    """the compendium's sound: every ▶ plays (string index 0–5 from the low E, a real fret)"""
    m = re.search(r'<script id="cp-data" type="application/json">(.*?)</script>', html, re.S)
    if not m: return []
    C = json.loads(m.group(1)); rep = []
    def walk(x, where):
        if isinstance(x, dict):
            if isinstance(x.get('ev'), list):
                bad = [e for e in x['ev'] if not (isinstance(e, list) and len(e) >= 3 and 0 <= e[1] <= 5 and 0 <= e[2] <= 24)]
                if bad: rep.append(('cp', where, 'cp sound', f"{x.get('where') or x.get('title') or ''}: {len(bad)} notes with no string (e.g. {bad[0][:3]})"))
            for k, v in x.items(): walk(v, where if k != 'replaced' else 'replaced')
        elif isinstance(x, list):
            for v in x: walk(v, where)
    walk(C, '-')
    return rep


# ---------------- Key Finder: the same song's piano page
KF = '/home/claude/key-finder/songs/'


KF_SLUG = {'faure-apres-un-reve': 'apres-un-reve'}      # the same song under another name on Key Finder


def kf_load(slug):
    h = open(KF + KF_SLUG.get(slug, slug) + '/index.html', encoding='utf-8').read()
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
    slug = KF_SLUG.get(slug, slug)
    lk = [f for f in os.listdir(KF + slug) if f.endswith('.mp3.locked')]
    pn = [f for f in os.listdir(KF + slug) if f.endswith('-piano.mp3')]
    if not lk or not pn: return rep + [('kf', '-', 'voice', 'no singer track')]
    unlock(KF + slug + '/' + lk[0], work + 'mix.mp3'); mix = read_wav(work + 'mix.mp3'); os.remove(work + 'mix.mp3')
    p = read_wav(KF + slug + '/' + pn[0]); n = min(len(mix), len(p)); mix, p = mix[:n], p[:n]
    a = float(np.dot(mix, p) / np.dot(p, p)); v = mix - a * p
    left = float(np.sqrt(np.mean(v ** 2)) / np.sqrt(np.mean(mix ** 2)))
    v.astype(np.float32).tofile(work + 'v.f32')
    subprocess.run(['python3', '/home/claude/lafa/work/f0p.py', work + 'v.f32', work + 'v_'], check=True, capture_output=True); tidy(work)
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


if __name__ == '__main__':
    slug = sys.argv[1]
    if '--kf' in sys.argv and not os.path.exists(f'{ROOT}/songs/{slug}/index.html'):
        # a song only on Key Finder (Love Me Tender, White Christmas, ...): its own checks alone
        print(f'== {slug}: on Key Finder only')
        for k, lab, kind, msg in kf_report(slug, '--voice' in sys.argv): print(f'[{kind:8s}] {k:>5s} {lab:>9s}  {msg}', flush=True)
        sys.exit()
    D, html = load(slug)
    rep = grips_report(D) + plays_report(D) + notes_report(D) + cp_report(html)
    if '--voice' in sys.argv: rep += voice_report(D, html, slug)
    if '--sound' in sys.argv: rep += sound_report(D, slug)
    if '--kf' in sys.argv: rep += kf_report(slug, '--voice' in sys.argv)
    print(f'== {slug}: {sum(len(t["bars"]) for t in D["tracks"])} bars in {len(D["tracks"])} track(s)')
    for k, lab, kind, msg in rep: print(f'[{kind:8s}] {k:>5s} {lab:>9s}  {msg}', flush=True)
