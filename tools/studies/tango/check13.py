"""Checks for entry13 (tango fills, rebuilt by rule). Every fill entry13 made is checked against Graciano's rule with
code of its own (its own note names, scales and intervals), and every string and fret, rhythm, grip and bar length.
python3 -B check13.py"""
import sys, re
sys.path.insert(0, '/home/claude/scripts'); sys.path.insert(0, '/home/claude/studies/tango'); sys.path.insert(0, '/home/claude/studies')
import gtr
import entry13 as E

OPN = {6: 40, 5: 45, 4: 50, 3: 55, 2: 59, 1: 64}
LETTERS = 'CDEFGAB'; NAT = [0, 2, 4, 5, 7, 9, 11]
probs = []


def P(msg): probs.append(msg)


def pitch(n):
    m = re.fullmatch(r'([A-G])([b#]?)(\d)', n)
    assert m, n
    return 12 * (int(m.group(3)) + 1) + NAT[LETTERS.index(m.group(1))] + {'b': -1, '#': 1, '': 0}[m.group(2)]


def letter(n): return LETTERS.index(n[0])


def pcl(name):            # a pitch-class name ('Bb') -> 0..11
    return (NAT[LETTERS.index(name[0])] + {'b': -1, '#': 1, '': 0}[name[1:2] if len(name) > 1 else '']) % 12


KEYS = {'major': [0, 2, 4, 5, 7, 9, 11], 'natural': [0, 2, 3, 5, 7, 8, 10], 'harmonic': [0, 2, 3, 5, 7, 8, 11], 'melodic': [0, 2, 3, 5, 7, 9, 11]}


def scale_pcs(key, kind): return {(pcl(key) + x) % 12 for x in KEYS[kind]}


def deg_pc(key, kind, d): return (pcl(key) + KEYS[kind][d - 1]) % 12


def next_in(scale, m, direction):
    x = m + direction
    while x % 12 not in scale: x += direction
    return x


def chord_root(ch): return re.match(r'[A-G][b#]?', ch).group(0)


def chord_pcs(ch):
    r = pcl(chord_root(ch)); q = ch[len(chord_root(ch)):]
    iv = {'': [0, 4, 7], '7': [0, 4, 7, 10], 'm': [0, 3, 7]}[q]
    return {(r + x) % 12 for x in iv}


def width(h): return 4 if h >= 7 else 3


def windows(frets):
    """how many hand positions a line of fretted notes needs, in order (greedy)"""
    n, lo, hi = 0, None, None
    for f in frets:
        if lo is None: lo = hi = f; n = 1; continue
        a, b = min(lo, f), max(hi, f)
        if b - a <= width(a): lo, hi = a, b
        else: n += 1; lo = hi = f
    return n


def sounding(L): return [(d, ns, fl) for d, ns, fl in L['ev'] if ns]


# ---------------------------------------------------------------- every logged fill
for L in E.LOG:
    tag = f'{L["ex"]}/{L["device"]}'
    snd = sounding(L)
    if len(snd) != len(L['pos']): P(f'{tag}: {len(snd)} notes, {len(L["pos"])} places'); continue
    for (d, ns, fl), ps in zip(snd, L['pos']):
        if len(ns) != len(ps): P(f'{tag}: {ns} on {ps}')
        for n, (s, f) in zip(ns, ps):
            if not 0 <= f <= 15: P(f'{tag}: fret {f}')
            if OPN[s] + f != pitch(n): P(f'{tag}: {n} is not string {s} fret {f}')
        ss = [s for s, f in ps]
        if len(set(ss)) != len(ss): P(f'{tag}: two notes on one string {ps}')
        fz = [f for s, f in ps if f > 0]
        if len(fz) > 1 and max(fz) - min(fz) > width(min(fz)): P(f'{tag}: too wide {ps}')
    rhythm = [d for d, ns, fl in L['ev']]
    ms = [[pitch(n) for n in ns] for d, ns, fl in snd]
    c = L['ctx']; dev = L['device']

    if dev in ('scale-down', 'scale-up', 'pattern'):
        key, mode = c['key'], c['mode']
        line = [m[0] for m in ms]
        frets = [p[0][1] for p in L['pos']]
        if any(f == 0 for f in frets): P(f'{tag}: an open string in a run')
        if windows(frets) > 2: P(f'{tag}: the hand moves {windows(frets) - 1} times')
        if any(p[0][0] > 4 for p in L['pos']): P(f'{tag}: off the top strings {L["pos"]}')
    if dev == 'scale-down':
        kind = 'natural' if mode == 'minor' else 'major'; sc = scale_pcs(key, kind)
        if rhythm != [0.25] * 8 or L['ev'][0][1]: P(f'{tag}: rhythm {rhythm}')
        if line[0] % 12 != deg_pc(key, kind, 5) or line[0] % 12 != pcl(chord_root(c['dom'])): P(f'{tag}: does not start on the dominant’s root')
        if line[1] % 12 != deg_pc(key, kind, 7) or not 3 <= line[1] - line[0] <= 4: P(f'{tag}: the second note is not the key’s 7th a 3rd up')
        for a, b in zip(line[1:], line[2:]):
            if b != next_in(sc, a, -1): P(f'{tag}: {a}->{b} not the next scale step down')
        if line[-1] % 12 != deg_pc(key, kind, 2): P(f'{tag}: does not end on the 2nd')
        if L['land'] % 12 != pcl(key): P(f'{tag}: lands on {L["land"]}, not the tonic')
        ls = [letter(n[0]) for d, n, fl in snd]
        if any((a - b) % 7 != 1 for a, b in zip(ls[1:], ls[2:])): P(f'{tag}: spelling skips a letter')
    if dev == 'scale-up':
        kind = 'melodic' if mode == 'minor' else 'major'; sc = scale_pcs(key, kind)
        if rhythm != [0.25] * 8 or L['ev'][0][1]: P(f'{tag}: rhythm {rhythm}')
        if line[0] % 12 != deg_pc(key, kind, 5): P(f'{tag}: does not start on the key’s 5th')
        for a, b in zip(line, line[1:]):
            if b != next_in(sc, a, 1): P(f'{tag}: {a}->{b} not the next scale step up')
        if line[-1] % 12 != deg_pc(key, kind, 4): P(f'{tag}: does not end on the 4th')
        if L['land'] % 12 != pcl(chord_root(c['dom'])): P(f'{tag}: does not land on the dominant')
    if dev == 'pattern':
        kind = 'harmonic' if mode == 'minor' else 'major'; sc = scale_pcs(key, kind)
        if rhythm != [0.25] * 8: P(f'{tag}: rhythm {rhythm}')
        if line[0] % 12 != pcl(key): P(f'{tag}: does not start on the key’s root')
        for g in (0, 4):
            x, lo, x2, hi = line[g:g + 4]
            if not (x2 == x and lo == next_in(sc, x, -1) and hi == next_in(sc, x, 1)): P(f'{tag}: group {line[g:g + 4]} is not note, step below, note, step above')
        if line[4] != next_in(sc, line[3], 1): P(f'{tag}: the second group does not start a step above the first’s last note')
        if next_in(sc, line[-1], 1) % 12 != pcl(chord_root(c['dom'])): P(f'{tag}: does not lead into the dominant’s root')
        if L['land'] % 12 != pcl(chord_root(c['dom'])): P(f'{tag}: does not land on the dominant')
    if dev == 'campanitas-1':
        r = pcl(chord_root(c['dom']))
        if rhythm != [0.125, 0.5, 0.375, 0.125, 0.5, 1.0]: P(f'{tag}: rhythm {rhythm}')
        flags = [fl for d, ns, fl in L['ev']]
        if flags != ['g', '', 's', 'g', '', 's']: P(f'{tag}: slides and shorts {flags}')
        bells = [m[0] for m, (d, ns, fl) in zip(ms, snd) if fl != 'g']
        if any(b % 12 != r for b in bells) or [b - bells[0] for b in bells] != [0, 12, 12, 24]: P(f'{tag}: not the root in octaves {bells}')
        ss = [p[0][0] for p, (d, ns, fl) in zip(L['pos'], snd) if fl != 'g']
        fr = [p[0][1] for p, (d, ns, fl) in zip(L['pos'], snd) if fl != 'g']
        if [ss[0] - x for x in ss] != [0, 2, 1, 3]: P(f'{tag}: strings {ss} are not his pattern')
        if not all(a < b for a, b in zip(fr, fr[1:])): P(f'{tag}: not climbing the neck {fr}')
        for i in (0, 3):
            (gs, gf), (ts, tf) = L['pos'][i][0], L['pos'][i + 1][0]
            if gs != ts or not 1 <= tf - gf <= 2 or gf < 1: P(f'{tag}: slide {L["pos"][i]} -> {L["pos"][i + 1]}')
    if dev == 'campanitas-2':
        r = pcl(chord_root(c['dom']))
        if rhythm != [0.125, 0.5, 0.5, 0.5, 0.25, 0.25, 0.5]: P(f'{tag}: rhythm {rhythm}')
        bells = [m[0] for m in ms[1:]]
        if any(b % 12 != r for b in bells) or [b - bells[0] for b in bells] != [0, 12, 0, 12, 0, 12]: P(f'{tag}: not rocking octaves {bells}')
        if [p[0][0] for p in L['pos'][1:]] != [3, 1, 3, 1, 3, 1]: P(f'{tag}: not the G and top strings')
    if dev == 'tenths':
        r = pcl(chord_root(c['chord'])); q = c['q']
        want_lo = {'maj': [0, 2, 3, 4], 'min': [0, 1, 2, 3]}[q]; want_hi = {'maj': [4, 5, 6, 7], 'min': [3, 5, 6, 7]}[q]
        if q != ('min' if c['chord'].endswith('m') else 'maj'): P(f'{tag}: wrong quality')
        if [(m[0] - r) % 12 for m in ms] != want_lo or [(m[1] - r) % 12 for m in ms] != want_hi: P(f'{tag}: degrees {[[x % 12 for x in m] for m in ms]}')
        if any(not 15 <= m[1] - m[0] <= 16 for m in ms): P(f'{tag}: not tenths')
        if any(b - a not in (1, 2) for a, b in zip([m[0] for m in ms], [m[0] for m in ms][1:])): P(f'{tag}: the lower voice does not climb by step')
        want_r = [0.5, 1, 0.25, 0.25, 2] if c['phrased'] else [0.5, 0.5, 0.5, 0.5, 2]
        if rhythm != want_r: P(f'{tag}: rhythm {rhythm}')
        pairs = {tuple(s for s, f in p) for p in L['pos']}
        if len(pairs) != 1 or list(pairs)[0] not in ((5, 2), (6, 3), (4, 1)): P(f'{tag}: strings {pairs}')
    if dev.startswith('octaves'):
        key, mode = c['key'], c['mode']; way = dev[-2:]
        kind = ('natural' if mode == 'minor' else 'major') if way == 'td' else ('melodic' if mode == 'minor' else 'major')
        sc = scale_pcs(key, kind)
        if rhythm != [0.5] * 8 or L['ev'][0][1]: P(f'{tag}: rhythm {rhythm}')
        lows, highs = [m[0] for m in ms[0:6:2]], [m[0] for m in ms[1:6:2]]
        if [h - l for l, h in zip(lows, highs)] != [12, 12, 12]: P(f'{tag}: not octaves')
        start = pcl(key) if way == 'td' else deg_pc(key, kind, 5)
        if lows[0] % 12 != start: P(f'{tag}: starts on the wrong degree')
        d = -1 if way == 'td' else 1
        if lows[1] != next_in(sc, lows[0], d) or lows[2] != next_in(sc, lows[1], d): P(f'{tag}: not steps of the scale {lows}')
        x = ms[6][0]
        if L['ev'][-1][2] != 'x': P(f'{tag}: the last note is not dead')
        if way == 'td' and (x % 12 != deg_pc(key, kind, 5) or x != L['land']): P(f'{tag}: the x is not the dominant’s bass')
        if way == 'dt' and (x % 12 != lows[2] % 12 or x != L['land'] - 1): P(f'{tag}: the x is not the 7th a fret under the tonic’s bass')
        if L['pos'][-1][0][0] < 5: P(f'{tag}: the x is not on a bass string')
        ls_ = {p[0][0] for p in L['pos'][0:6:2]}; hs_ = {p[0][0] for p in L['pos'][1:6:2]}
        if len(ls_) != 1 or len(hs_) != 1: P(f'{tag}: the octaves move strings')
    if dev in ('sixths', 'thirds'):
        size = {'sixths': (8, 9), 'thirds': (3, 4)}[dev]
        ivs = [m[1] - m[0] for m in ms]
        if len(set(ivs)) != 1 or ivs[0] not in size: P(f'{tag}: sizes {ivs}')
        for a, b in zip(ms, ms[1:]):
            if b[0] - a[0] != 1 or b[1] - a[1] != 1: P(f'{tag}: not sliding by semitones {ms}')
        r = pcl(chord_root(c['chord'])); minor = c['chord'].endswith('m')
        tdeg = {'root': 0, '3rd': 3 if minor else 4, '5th': 7, '7th': 10}[c['target']]
        if (ms[-1][1] - r) % 12 != tdeg: P(f'{tag}: the top does not land on the {c["target"]}')
        allowed = chord_pcs(c['chord']) | ({(r + 10) % 12} if minor else set())
        if ms[-1][0] % 12 not in allowed: P(f'{tag}: the lower note of the target is not the chord’s')
        if dev == 'sixths' and minor and c['target'] == '5th' and (ms[-1][0] - r) % 12 != 10: P(f'{tag}: his minor-5th case has the 7th under it')
        if rhythm != [0.5, 1, 0.5, 1, 1]: P(f'{tag}: rhythm {rhythm}')
        if len({tuple(s for s, f in p) for p in L['pos']}) != 1: P(f'{tag}: the pair changes strings')
    if dev == 'marcatto':
        dom = c['dom']; r = pcl(chord_root(dom)); want = {(r + x) % 12 for x in (0, 4, 7, 10)}
        order = {1: [10, 0, 4, 0], 2: [10, 4, 0, 10], 3: [10, 4, 0, 4], 4: [10, 0, 10, 4]}[c['order']]
        shape = {10: [10, 4, 7, 0], 0: [0, 7, 10, 4], 4: [4, 10, 0, 7]}
        for m, ps, b in zip(ms, L['pos'], order):
            if {x % 12 for x in m} != want: P(f'{tag}: {m} is not the whole dominant 7th')
            if sorted(m) != m: P(f'{tag}: voices crossed {m}')
            if [(x - r) % 12 for x in m] != shape[b]: P(f'{tag}: not his voicing for that bass {m}')
            if [s for s, f in ps] != [4, 3, 2, 1]: P(f'{tag}: not on the top four strings')
        if rhythm != [1, 1, 1, 1]: P(f'{tag}: rhythm')
        if L['land'] % 12 != pcl(chord_root(c['ton'])): P(f'{tag}: does not slide into the tonic')

n_fills = len(E.LOG)
by = {}
for L in E.LOG: by[L['device']] = by.get(L['device'], 0) + 1
print('fills checked:', n_fills, by)

# ---------------------------------------------------------------- bars, grips, quotes
def chk_k(it, lab):
    name, g, hits = it[1], it[2], it[3]
    fz = [f for f in g if f > 0]
    if fz and max(fz) - min(fz) > width(min(fz)): P(f'{lab} {name} {g}: stretch')
    for h in hits:
        if isinstance(h[1], list):
            for s in h[1]:
                if g[6 - s] < 0: P(f'{lab} {name}: string {s} struck but not in the grip {g}')
    p = gtr.check_grip(g, name.replace('♭', 'b').replace('♯', '#'))
    if p: P(f'{lab} {name} {g}: {p}')


def length(its):
    t = 0.0
    for it in its:
        if it[0] == 'K': t += sum(h[0] for h in it[3])
        elif it[0] in 'RP': t += sum(it[2])
        elif it[0] == 'W': t += it[1]
    return t


nb = 0
for S in E.SECTIONS:
    for ex in S['ex']:
        q = ex['quote']
        qits = q.get('items') or []
        if length(qits) > 2 + 1e-9: P(f'{ex["id"]}: quote {length(qits)} beats')
        for it in qits:
            if it[0] == 'K': chk_k(it, ex['id'] + ' quote')
        for j, b in enumerate(ex['bars']):
            lab = f'{ex["id"]}#{j + 1}'
            for it in b['items']:
                if it[0] == 'K': chk_k(it, lab)
                if it[0] in 'RP':
                    for grp in it[1]:
                        grp = grp if isinstance(grp[0], list) else [grp]
                        for s, f in grp:
                            if not 0 <= f <= 15: P(f'{lab}: fret {f}')
            L_ = length(b['items'])
            want = (3 if j > 0 else 1) if ex['id'] == 'etude-iw-rellenos' else 4
            if ex['id'] == 'etude-iw-rellenos' and j == len(ex['bars']) - 1: want = 3
            if abs(L_ - want) > 1e-9: P(f'{lab}: {L_} beats, not {want}')
            nb += 1
print('bars checked:', nb)

# the IW étude: the fills sit where the voice holds or rests (bars of the 1909 chorus)
import tune_iw as TU
held, tie = {}, False
for b, chs, notes, w in TU.in_eb(ending=1):
    t, onsets = 0.0, []                  # where in the bar the voice starts a new note
    for k, (n, d) in enumerate(notes):
        if n != 'r' and not (k == 0 and tie): onsets.append(t)
        tie = n.endswith('~')
        t += d
    held[b] = onsets
FILL_BARS = {3, 4, 8, 12, 14, 19, 24, 31}
et = next(e for S in E.SECTIONS for e in S['ex'] if e['id'] == 'etude-iw-rellenos')
for j, b in enumerate(et['bars']):
    song_bar = j if j <= 32 else None
    has_fill = any(it[0] in 'RP' for it in b['items'])
    if song_bar is None: continue
    if has_fill and song_bar not in FILL_BARS: P(f'étude IW bar {song_bar}: a fill where it should not be')
    if has_fill and any(t > 0.99 for t in held[song_bar]): P(f'étude IW bar {song_bar}: a fill while the voice sings new words {held[song_bar]}')
for b in FILL_BARS:
    if not any(it[0] in 'RP' for it in et['bars'][b]['items']): P(f'étude IW bar {b}: no fill')

if probs:
    print('\n'.join(probs)); sys.exit(1)
print('all good')
