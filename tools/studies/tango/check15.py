"""Checks for entry15 (tango harmony, rebuilt by rule): every progression, line and tritone entry15 made is checked
against Graciano's rule with code of its own, and every grip, string and fret, rhythm and bar length.
python3 -B check15.py"""
import sys, re
sys.path.insert(0, '/home/claude/scripts'); sys.path.insert(0, '/home/claude/studies/tango'); sys.path.insert(0, '/home/claude/studies')
import gtr
import entry15 as E

OPN = {6: 40, 5: 45, 4: 50, 3: 55, 2: 59, 1: 64}
NAT = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
probs = []
def P(m): probs.append(m)
def width(h): return 4 if h >= 7 else 3
def gnotes(g): return sorted(OPN[6 - i] + g[i] for i in range(6) if g[i] >= 0)
def gbass(g): i = next(i for i in range(6) if g[i] >= 0); return 6 - i, OPN[6 - i] + g[i]
def pcs(ms): return {m % 12 for m in ms}
def kpc(name): return (NAT[name[0]] + {'b': -1, '#': 1}.get(name[1:2], 0)) % 12
Q = {'': [0, 4, 7], 'm': [0, 3, 7], '7': [0, 4, 7, 10], 'dim7': [0, 3, 6, 9], 'maj7': [0, 4, 7, 11], 'm7b5': [0, 3, 6, 10], '6': [0, 4, 7, 9],
     'm6': [0, 3, 7, 9], 'm7': [0, 3, 7, 10], 'm(maj7)': [0, 3, 7, 11], 'm#5': [0, 3, 8]}
def chord(r, q): return {(r + x) % 12 for x in Q[q]}


def playable(g, lab):
    fz = [f for f in g if f > 0]
    if fz and max(fz) - min(fz) > width(min(fz)): P(f'{lab}: grip {g} too wide')
    if any(f > 15 for f in g): P(f'{lab}: off the neck {g}')


def group_ok(g, lab):
    ss = [s for s, f in g]
    if len(set(ss)) != len(ss): P(f'{lab}: two notes on one string {g}')
    fz = [f for s, f in g if f > 0]
    if fz and max(fz) - min(fz) > width(min(fz)): P(f'{lab}: too wide {g}')


def chords_ok(L, want, lab):
    """want: [(root pc, quality, bass pc)]"""
    for (ms, g), (r, q, b) in zip(L['chords'], want):
        if gnotes(g) != sorted(ms): P(f'{lab}: grip {g} does not sound {ms}')
        if not pcs(ms) <= chord(r, q) | {b}: P(f'{lab}: {ms} has notes outside its chord ({r}{q})')
        need = {'7': [4, 10], 'maj7': [4, 11], 'm7b5': [3, 6, 10], '6': [4, 9], '': [4], 'm': [3]}.get(q, [])
        if not {(r + x) % 12 for x in need} - {b} <= pcs(ms): P(f'{lab}: {ms} lacks the notes that make it {q or "major"}')
        if min(ms) % 12 != b: P(f'{lab}: the bass of {ms} is not {b}')
        playable(g, lab)


for L in E.LOG:
    lab = f'{L.get("ex")}/{L["device"]}'; c = L['ctx']; d = L['device']
    if d == 'im-ivm':
        k = kpc(c['key'])
        chords_ok(L, [(k, 'm', k), ((k + 2) % 12, 'm7b5', (k + 2) % 12), ((k + 3) % 12, '', (k + 3) % 12), (k, '7', (k + 4) % 12), ((k + 5) % 12, 'm', (k + 5) % 12)], lab)
        bs = [ms[0] for ms, g in L['chords']]
        if [b - bs[0] for b in bs] != [0, 2, 3, 4, 5]: P(f'{lab}: the bass does not climb 1 2 ♭3 3 4: {bs}')
    if d == 'im-v':
        k = kpc(c['key'])
        chords_ok(L, [(k, 'm', k), (k, 'm', (k + 10) % 12), ((k + 9) % 12, 'dim7', (k + 9) % 12), ((k + 8) % 12, '7', (k + 8) % 12), ((k + 7) % 12, '7', (k + 7) % 12)], lab)
        bs = [ms[0] for ms, g in L['chords']]
        if [b - bs[0] for b in bs] != [0, -2, -3, -4, -5]: P(f'{lab}: the bass does not fall 1 ♭7 6 ♭6 5: {bs}')
    if d in ('im-ivm', 'im-v', 'circle'):
        ups = [ms[1:] for ms, g in L['chords']]
        for a, b in zip(ups, ups[1:]):
            if max(abs(x - y) for x, y in zip(a, b)) > 7: P(f'{lab}: an upper voice leaps {a} -> {b}')
    if d == 'grela':
        k = kpc(c['key'])
        want = [(k, 'm'), ((k + 10) % 12, '6'), ((k + 8) % 12, 'maj7'), ((k + 7) % 12, '7')]
        for (ms, g), (r, q) in zip(L['chords'], want):
            if pcs(ms) != chord(r, q): P(f'{lab}: {ms} is not the whole {r}{q}')
            if max(ms) != c['top'] or c['top'] % 12 != (k + 7) % 12: P(f'{lab}: the key’s 5th is not on top {ms}')
            if gnotes(g) != sorted(ms): P(f'{lab}: grip does not sound its notes')
            playable(g, lab)
    if d == 'circle':
        k = kpc(c['key'])
        want = [((k + 5) % 12, 'm'), ((k + 10) % 12, '7'), ((k + 3) % 12, 'maj7'), ((k + 8) % 12, 'maj7'), ((k + 2) % 12, 'm7b5'), ((k + 7) % 12, '7'), (k, 'm')]
        chords_ok(L, [(r, q, r) for r, q in want], lab)
        rs = [r for r, q in want]
        if [(b - a) % 12 for a, b in zip(rs, rs[1:])] != [5, 5, 5, 6, 5, 5]: P(f'{lab}: not the key’s circle of 5ths (one diminished 5th, ♭VI to II)')
    if d == 'tritone-sub':
        (m1, g1), (m2, g2) = L['chords']
        r = gbass(g1)[1] % 12; sr = gbass(g2)[1] % 12
        if (sr - r) % 12 != 6: P(f'{lab}: the substitute is not a tritone away')
        if not {(r + 4) % 12, (r + 10) % 12} <= pcs(m1): P(f'{lab}: the dominant lacks its 3rd or 7th')
        shared = [m for m in m1 if m % 12 in ((r + 4) % 12, (r + 10) % 12)]
        if not set(shared) <= set(m2): P(f'{lab}: the shared notes {shared} do not stay in the substitute {m2}')
        if not pcs(m2) <= chord(sr, '7') | {(sr + 2) % 12}: P(f'{lab}: the substitute has foreign notes')
        for x in shared:
            s1 = [(6 - i, g1[i]) for i in range(6) if g1[i] >= 0 and OPN[6 - i] + g1[i] == x]
            s2 = [(6 - i, g2[i]) for i in range(6) if g2[i] >= 0 and OPN[6 - i] + g2[i] == x]
            if s1 != s2: P(f'{lab}: the shared note {x} changes string')
        playable(g1, lab); playable(g2, lab)
    if d == 'sub-9-11':
        ms, g = L['chords'][0]
        sub = kpc(c['sub']); dom = kpc(c['dom'])
        if (sub - dom) % 12 != 6 or pcs(ms) != {(sub + x) % 12 for x in (0, 4, 10, 2, 6)} or ms[0] % 12 != sub: P(f'{lab}: not the substitute with 9th and ♯11 {ms}')
        if gnotes(g) != sorted(ms): P(f'{lab}: grip'); playable(g, lab)
    if d == 'dim-for-v':
        (m1, g1), (m2, g2) = L['chords']
        r = kpc(c['dom'])
        if not pcs(m2) <= chord((r + 4) % 12, 'dim7') or len(pcs(m2)) < 3 or m2[0] % 12 != (r + 4) % 12: P(f'{lab}: not the diminished on the 3rd {m2}')
        playable(g1, lab); playable(g2, lab)
    if d == 'dim-shapes':
        r = kpc(c['dim'])
        for g, s in zip(L['grips'], (6, 5, 4)):
            if pcs(gnotes(g)) != chord(r, 'dim7') or gbass(g)[0] != s or gbass(g)[1] % 12 != r: P(f'{lab}: shape {g}')
            playable(g, lab)
    if d == 'dim-marcatto':
        r = kpc(c['dom']); dset = chord((r + 4) % 12, 'dim7')
        fr = []
        for g in L['grips']:
            if pcs(gnotes(g)) != dset: P(f'{lab}: {g} is not the dominant’s diminished')
            if gbass(g)[0] != 4: P(f'{lab}: not on the top four strings')
            fr.append(g[2]); playable(g, lab)
        if [b - a for a, b in zip(fr, fr[1:])] != [-3, -3, -3]: P(f'{lab}: not sliding three frets each')
        step = max(gnotes(L['tgrip'])) - max(gnotes(L['grips'][-1]))
        if abs(step) not in (1, 2): P(f'{lab}: the top voice does not step into the tonic ({step})')
    if d == 'cliche':
        k = kpc(c['key']); frm = c['frm']; line = L['line']
        want = [0, -1, -2, -3] if frm == 8 else [0, 1, 2, 1]
        if [x - line[0] for x in line] != want or line[0] % 12 != (k if frm == 8 else (k + 7) % 12): P(f'{lab}: the line {line}')
        holds = sorted(L['hold'])
        if pcs(holds) != ({(k + 3) % 12, (k + 7) % 12} if frm == 8 else {k, (k + 3) % 12}): P(f'{lab}: the held notes {holds}')
        for i, g in enumerate(L['grips']):
            ms = sorted(L['bass'] + holds + [line[i]])
            if gnotes(g) != ms: P(f'{lab}: grip {g} does not sound {ms}')
            playable(g, lab)
        w = c['where']
        if w == 'bass' and not all(m < min(holds) for m in line): P(f'{lab}: the line is not in the bass')
        if w == 'top' and not all(m > max(holds) for m in line): P(f'{lab}: the line is not on top')
        if w == 'inner' and not all(min(holds + L['bass']) < m < max(holds) for m in line): P(f'{lab}: the line is not inside')
        if L['bass'] and L['bass'][0] % 12 != k: P(f'{lab}: the bass is not the root')
        # the held notes stay put, the line keeps one string
        def where(g, m): return [(6 - i, g[i]) for i in range(6) if g[i] >= 0 and OPN[6 - i] + g[i] == m]
        for a, b in zip(L['grips'], L['grips'][1:]):
            for m in holds + L['bass']:
                if where(a, m) != where(b, m): P(f'{lab}: the held {m} moves')
        ls = {(where(g, m) or [(None,)])[0][0] for g, m in zip(L['grips'], line)}
        if len(ls) != 1 or None in ls: P(f'{lab}: the line changes string')
        if 'frag' in L:
            fr_ = L['frag']
            if fr_['durs'] != [0.5, 0.5, 0.25, 0.25, 0.25, 0.25, 0.5, 1.5]: P(f'{lab}: the broken rhythm')
            seqm = [sorted(OPN[s] + f for s, f in x) for x in fr_['steps'] if x]
            if seqm != [[line[0]], holds, [line[0]], [line[1]], [line[2]], [line[3]], holds]: P(f'{lab}: the broken line {seqm}')
    if d == 'cliche-counter':
        k = kpc(c['key']); seq = L['seq']
        lo = [a for a, b, dd in seq if a is not None]; hi = [b for a, b, dd in seq if b is not None]
        if [x - lo[0] for x in lo] != [0, -1, -2, -3] or lo[0] % 12 != k: P(f'{lab}: the bass line')
        if [x - hi[0] for x in hi] != [0, 2, 3, 2, 0] or hi[0] % 12 != k: P(f'{lab}: the upper line {hi}')
        if [dd for a, b, dd in seq] != [0.5, 0.5, 0.5, 0.5, 1, 1]: P(f'{lab}: rhythm')
        got = [sorted(OPN[s] + f for s, f in g) for g in L['steps']]
        if got != [sorted(x for x in (a, b) if x is not None) for a, b, dd in seq]: P(f'{lab}: strings and frets')
        for g in L['steps']: group_ok(g, lab)
    if d == 'cliche-oct':
        k = kpc(c['key']); line = L['line']
        if [x - line[0] for x in line] != [0, -1, -2, -3] or line[0] % 12 != k: P(f'{lab}: the line')
        for g, m in zip(L['steps'], line):
            if sorted(OPN[s] + f for s, f in g) != [m, m + 12]: P(f'{lab}: not an octave {g}')
            group_ok(g, lab)
    if d in ('tritone', 'four-tritones', 'resolutions', 'fingerings', 'application', 'application-chain'):
        r = kpc(c['dom']); dset = {(r + 4) % 12, (r + 10) % 12, (r + 1) % 12, (r + 7) % 12}

        def is_tt(p, own=False):
            return p[1] - p[0] == 6 and pcs(p) <= dset and (not own or pcs(p) == {(r + 4) % 12, (r + 10) % 12})

        def res_ok(t, x, tp):
            dl, dh = x[0] - t[0], x[1] - t[1]
            return dl * dh < 0 and abs(dl) in (1, 2) and abs(dh) in (1, 2) and pcs(x) <= tp
        tname = c.get('tonic') or c.get('target')
        tp = chord(kpc(tname), 'm' if tname.endswith('m') else ('7' if tname.endswith('7') else '')) if tname else set()
    if d == 'tritone':
        t, x = L['pairs']
        if not is_tt(t, own=True): P(f'{lab}: not the dominant’s tritone {t}')
        if not res_ok(t, x, tp): P(f'{lab}: the resolution {t} -> {x}')
    if d in ('four-tritones', 'resolutions', 'fingerings'):
        ts = L['pairs'] if d == 'four-tritones' else L['tritones']
        if not all(is_tt(t) for t in ts) or [t[0] - ts[0][0] for t in ts] != [0, 3, 6, 9]: P(f'{lab}: not four tritones a minor 3rd apart {ts}')
        if d == 'four-tritones' and not is_tt(ts[0], own=True): P(f'{lab}: does not start with the dominant’s own')
        if d != 'four-tritones':
            for t, x in zip(ts, L['res']):
                if not res_ok(t, x, tp): P(f'{lab}: the resolution {t} -> {x}')
    if d in ('tritone', 'four-tritones', 'resolutions', 'application', 'application-chain'):
        seqp = L['pairs'] if d != 'resolutions' else [x for t, rr in zip(L['tritones'], L['res']) for x in (t, rr)]
        for p, g in zip(seqp, L['pos']):
            if sorted(OPN[s] + f for s, f in g) != sorted(p): P(f'{lab}: {g} does not sound {p}')
            group_ok(g, lab)
    if d == 'fingerings':
        ss = c['strings']
        for (a, b), t, x in zip(L['pos'], L['tritones'], L['res']):
            if [s for s, f in a] != ss: P(f'{lab}: the tritone not on strings {ss}')
            if [s for s, f in b] not in (ss, [ss[0] + 1, ss[1]]): P(f'{lab}: the resolution on {b}')
            if sorted(OPN[s] + f for s, f in a) != t or sorted(OPN[s] + f for s, f in b) != x: P(f'{lab}: frets do not sound the notes')
            fz = [f for s, f in a + b]
            if min(fz) < 1 or max(fz) - min(fz) > width(min(fz)): P(f'{lab}: the shape is too wide {a} {b}')
    if d == 'application':
        ps = L['pairs']
        if not is_tt(ps[0], own=True) or not all(is_tt(p) for p in ps[:3]) or [p[0] - ps[0][0] for p in ps[:3]] != [0, 3, 6]: P(f'{lab}: the tritones {ps[:3]}')
        if not res_ok(ps[2], ps[3], tp): P(f'{lab}: the last does not resolve {ps[2]} -> {ps[3]}')
    if d == 'application-chain':
        t1, t2, x = L['pairs']
        r2 = kpc(c['dom2'])
        if not is_tt(t1, own=True): P(f'{lab}: the first tritone')
        if [b - a for a, b in zip(t1, t2)] != [-1, -1] or pcs(t2) != {(r2 + 4) % 12, (r2 + 10) % 12}: P(f'{lab}: does not slide into the next dominant’s tritone')
        if not res_ok(t2, x, tp): P(f'{lab}: the last does not resolve')

by = {}
for L in E.LOG: by[L['device']] = by.get(L['device'], 0) + 1
print('harmony checked:', len(E.LOG), by)


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
        q = ex['quote']; qits = q.get('items') or []
        if length(qits) > 2 + 1e-9: P(f'{ex["id"]}: quote {length(qits)} beats')
        for j, b in enumerate(ex['bars']):
            lab = f'{ex["id"]}#{j + 1}'
            for it in b['items']:
                if it[0] == 'K':
                    playable(it[2], lab)
                    p = gtr.check_grip(it[2], it[1])
                    if p: P(f'{lab} {it[1]} {it[2]}: {p}')
                if it[0] in 'RP':
                    for grp in it[1]:
                        grp = grp if isinstance(grp[0], list) else [grp]
                        group_ok([tuple(x) for x in grp], lab)
            if abs(length(b['items']) - 4) > 1e-9: P(f'{lab}: {length(b["items"])} beats')
            nb += 1
print('bars checked:', nb)
if probs:
    print('\n'.join(probs)); sys.exit(1)
print('all good')
