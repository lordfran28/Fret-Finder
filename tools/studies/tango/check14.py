"""Checks for entry14 (tango cadences, rebuilt by rule): every cadence entry14 made is checked against Graciano's rule with
code of its own, and every grip, string and fret, rhythm and bar length. python3 -B check14.py"""
import sys, re
sys.path.insert(0, '/home/claude/scripts'); sys.path.insert(0, '/home/claude/studies/tango'); sys.path.insert(0, '/home/claude/studies')
import gtr
import entry14 as E

OPN = {6: 40, 5: 45, 4: 50, 3: 55, 2: 59, 1: 64}
NAT = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
probs = []
def P(m): probs.append(m)


def pitch(n):
    m = re.fullmatch(r'([A-G])([b#]?)(\d)', n); assert m, n
    return 12 * (int(m.group(3)) + 1) + NAT[m.group(1)] + {'b': -1, '#': 1, '': 0}[m.group(2)]


def pcn(name): return (NAT[name[0]] + {'b': -1, '#': 1}.get(name[1:2], 0)) % 12
def width(h): return 4 if h >= 7 else 3
def gnotes(g): return sorted(OPN[6 - i] + g[i] for i in range(6) if g[i] >= 0)
def gbass(g): i = next(i for i in range(6) if g[i] >= 0); return 6 - i, OPN[6 - i] + g[i]


def playable(g, lab):
    fz = [f for f in g if f > 0]
    if fz and max(fz) - min(fz) > width(min(fz)): P(f'{lab}: grip {g} too wide')


def pcs(ms): return {m % 12 for m in ms}


Q = {'': [0, 4, 7], 'm': [0, 3, 7], '7': [0, 4, 7, 10], 'dim7': [0, 3, 6, 9], 'maj7': [0, 4, 7, 11]}
def chord(root, q): return {(root + x) % 12 for x in Q[q]}


def steps_pitches(steps): return [sorted(OPN[s] + f for s, f in g) for g in steps]


def group_ok(g, lab):
    ss = [s for s, f in g]
    if len(set(ss)) != len(ss): P(f'{lab}: two notes on one string {g}')
    fz = [f for s, f in g if f > 0]
    if fz and max(fz) - min(fz) > width(min(fz)): P(f'{lab}: too wide {g}')
    if any(not 0 <= f <= 15 for s, f in g): P(f'{lab}: fret off the neck {g}')


for L in E.LOG:
    lab = f'{L["ex"]}/{L["device"]}'; c = L['ctx']; d = L['device']
    if d == 'link':
        k = pcn(c['key']); lines = L['lines']
        got = steps_pitches(L['steps'])
        want = [sorted(pitch(n) for n in ns) for ns in lines]
        if got != want: P(f'{lab}: the strings and frets do not sound the notes {got} {want}')
        for g in L['steps']: group_ok(g, lab)
        if L['durs'] != [1, 1, 1, 2]: P(f'{lab}: rhythm {L["durs"]}')
        five = pitch(lines[0][0])
        if five % 12 != (k + 7) % 12: P(f'{lab}: does not start on the key’s 5th')
        lo = [sorted(pitch(n) for n in p)[0] for p in lines[1:]]; hi = [sorted(pitch(n) for n in p)[1] for p in lines[1:]]
        third_b = (k + (3 if c['mode_b'] == 'minor' else 4)) % 12
        fall, climb = (lo, hi) if c['way'] == 'a' else (hi, lo)
        if [five - fall[0], fall[0] - fall[1]] != [1, 1] or fall[2] % 12 != third_b or not 0 < fall[1] - fall[2] <= 2: P(f'{lab}: the falling voice {fall} is not 5, ♯4, 4, then the new 3rd')
        six = (k + (8 if (c['way'] == 'a' and c['mode_a'] == 'minor') else 9)) % 12
        if [x % 12 for x in climb] != [six, (k + 11) % 12, k] or not climb[0] < climb[1] < climb[2]: P(f'{lab}: the climbing voice {climb} is not 6, 7, 8')
        if any(a >= b for a, b in zip(lo, hi)): P(f'{lab}: voices cross')
    if d == 'bvi7':
        (t, gt), (b6, g6), (v, gv), (t2, _) = L['chords']
        kk = pcn(c['key'])
        def sev(g, r): return pcs(gnotes(g)) <= chord(r, '7') and {r, (r + 4) % 12, (r + 10) % 12} <= pcs(gnotes(g))
        if gbass(gv)[1] % 12 != (kk + 7) % 12 or not sev(gv, (kk + 7) % 12): P(f'{lab}: the dominant')
        if not sev(g6, (kk + 8) % 12): P(f'{lab}: the ♭VI7 is not a 7th chord a semitone above the dominant')
        if [x - y if y >= 0 else None for x, y in zip(g6, gv)] != [1 if y >= 0 else None for y in gv]: P(f'{lab}: not the same grip a fret higher')
        if not pcs(gnotes(gt)) <= chord(kk, 'm') or gbass(gt)[1] % 12 != kk: P(f'{lab}: the tonic')
    if d == 'pedal':
        kk = pcn(c['key']); names = [n for n, g in L['chords']]; gs = [g for n, g in L['chords']]
        for g in gs:
            s_, b = gbass(g)
            if b != c['bass'] or b % 12 != kk or g[6 - s_] != 0: P(f'{lab}: the bass is not the open tonic {g}')
            playable(g, lab)
        for i, off in enumerate((3, 2, 1)):
            up_ = [OPN[s] + gs[i][6 - s] for s in (3, 2, 1)]
            if pcs(up_) != chord((kk + off) % 12, ''): P(f'{lab}: triad {i + 1} is not the major triad {off} semitones above the tonic')
        for a, b in zip(gs[:2], gs[1:3]):
            if [x - y for x, y in zip(a[3:], b[3:])] != [1, 1, 1]: P(f'{lab}: the shape does not slide down a fret')
        if pcs([OPN[s] + gs[3][6 - s] for s in (3, 2, 1)]) != chord(kk, 'm'): P(f'{lab}: does not end on the minor tonic')
    if d == 'i-v/vi':
        T = pcn(c['key']); w = c['way']
        basses = [ms[0] for ms, g in L['chords']]
        want_b = {'a': [0, 0, -1, -3, -4], 'b': [0, 0, 2, 3, 4], 'c': [0, 0, 2, 3, 4], 'd': [0, 7, 9, 10, 11]}[w]
        if [(b - T) % 12 for b in basses] != [x % 12 for x in want_b]: P(f'{lab}: bass line {basses}')
        steps_ = [b - a for a, b in zip(basses, basses[1:])]
        if w == 'a' and any(s_ > 0 or s_ < -2 for s_ in steps_): P(f'{lab}: the bass does not fall by step')
        if w in 'bc' and any(s_ < 0 or s_ > 2 for s_ in steps_): P(f'{lab}: the bass does not climb by step')
        if w == 'd' and (steps_[0] != -5 or any(s_ < 1 or s_ > 2 for s_ in steps_[1:])): P(f'{lab}: the bass does not drop to the 5th and climb by step')
        want_c = {'a': [(0, ''), (0, ''), (11, 'dim7'), (9, 'dim7'), (4, '')], 'b': [(0, ''), (0, ''), (2, 'dim7'), (3, 'dim7'), (4, '7')],
                  'c': [(0, ''), (0, ''), (2, '7'), (3, '7'), (4, '7')], 'd': [(0, 'maj7'), (0, 'maj7'), (9, 'dim7'), (10, 'dim7'), (4, '7')]}[w]
        for (ms, g), (r, q) in zip(L['chords'], want_c):
            full = chord((T + r) % 12, q)
            if not pcs(ms) <= full: P(f'{lab}: {ms} has notes outside {(T + r) % 12}{q}')
            if q == '7' and not {(T + r + 4) % 12, (T + r + 10) % 12} <= pcs(ms): P(f'{lab}: a 7th chord without its 3rd and 7th')
            if q == 'dim7' and len(pcs(ms) & full) < 3: P(f'{lab}: a diminished chord with fewer than three of its notes')
            if gnotes(g) != sorted(ms): P(f'{lab}: grip {g} does not sound {ms}')
            playable(g, lab)
        ups = [ms[1:] for ms, g in L['chords']]
        for a, b in zip(ups, ups[1:]):
            if max(abs(x - y) for x, y in zip(a, b)) > 5: P(f'{lab}: a voice leaps {a} -> {b}')
        if w == 'c':
            g2, g3, g4 = [g for ms, g in L['chords'][2:5]]
            if not ([x - y if x >= 0 else None for x, y in zip(g3, g2)] == [1 if x >= 0 else None for x in g2] and
                    [x - y if x >= 0 else None for x, y in zip(g4, g3)] == [1 if x >= 0 else None for x in g3]): P(f'{lab}: the three 7ths are not one shape')
    if d == 'im-v':
        kk = pcn(c['key']); gs = L['grips']
        want = [(0, 'm'), (0, 'm'), (10, '7'), (8, '7'), (7, '7')]
        for g, (r, q) in zip(gs, want):
            s_, b = gbass(g)
            if s_ != c['string'] or b % 12 != (kk + r) % 12: P(f'{lab}: bass {b} on string {s_}')
            if pcs(gnotes(g)) != chord((kk + r) % 12, q): P(f'{lab}: {g} is not {(kk + r) % 12}{q}')
            playable(g, lab)
            if sum(1 for f in g if f >= 0) < 5: P(f'{lab}: not a whole barre {g}')
        bs = [gbass(g)[1] for g in gs]
        if [b - a for a, b in zip(bs, bs[1:])] != [0, -2, -2, -1]: P(f'{lab}: the bass does not slide down {bs}')
    if d == 'dims':
        kk = pcn(c['key']); gs = L['grips']
        v = gbass(gs[0])[1]
        if v % 12 != (kk + 7) % 12 or pcs(gnotes(gs[0])) != chord((kk + 7) % 12, '7'): P(f'{lab}: the dominant')
        for g, off in zip(gs[1:4], (1, 2, 4)):
            s_, b = gbass(g)
            if s_ != 6 or b != v + off: P(f'{lab}: diminished bass {b} not {v + off} on the low E string')
            if pcs(gnotes(g)) != chord(b % 12, 'dim7') or sum(1 for f in g if f >= 0) != 6: P(f'{lab}: not a six-string diminished 7th {g}')
            playable(g, lab)
        q = 'm' if c['mode'] == 'minor' else ''
        for g in (gs[4], gs[6]):
            if pcs(gnotes(g)) != chord(kk, q) or gbass(g)[0] != 6: P(f'{lab}: the tonic {g}')
        if gbass(gs[4])[1] - v != 5: P(f'{lab}: the bass does not step from the leading note to the tonic')
    if d == 'bass5':
        kk = pcn(c['key']); chs = L['chords']
        bs = [ms[0] for ms, g in chs]
        v = bs[0]
        if v % 12 != (kk + 7) % 12 or [b - v for b in bs] != [0, 1, 2, 4]: P(f'{lab}: the bass {bs} is not 5, ♭6, 6, 7')
        for ms, g in chs:
            if gbass(g)[0] != 5: P(f'{lab}: the bass is not on the A string {g}')
            if gnotes(g) != sorted(ms): P(f'{lab}: grip {g} does not sound {ms}')
            playable(g, lab)
        want = [chord(v % 12, '7'), chord((v + 1) % 12, 'dim7'), chord((v + 7) % 12, '7'), chord(v % 12, '7')]
        for (ms, g), w_ in zip(chs, want):
            if not pcs(ms) <= w_: P(f'{lab}: {ms} outside its chord')
        if not {(v + 4) % 12, (v + 10) % 12} <= pcs(chs[0][0]): P(f'{lab}: the dominant lacks its 3rd or 7th')
        if L['land'][0] % 12 != kk or L['land'][1] - L['land'][0] != 12 or L['land'][0] - bs[-1] != 1: P(f'{lab}: the landing')
    if d == 'decariana':
        line = [pitch(n) for n in L['line']]; kk = pcn(c['key'])
        if line[0] % 12 != (kk + 7) % 12: P(f'{lab}: does not start on the 5th')
        if [x - line[0] for x in line] != [0, -1, 0, 1, 2, 3, 4, 5]: P(f'{lab}: not the decariana {line}')
        if len({s for s, f in L['pos']}) != 1: P(f'{lab}: not on one string')
        if [OPN[s] + f for s, f in L['pos']] != line: P(f'{lab}: strings and frets do not sound the line')
        if L['durs'] != [1, 0.25, 0.25, 0.5, 0.5, 0.5, 0.5, 1]: P(f'{lab}: rhythm')
    if d == 'doble':
        kk = pcn(c['key']); seq = L['seq']
        ups = [u for lo, u, dd in seq if u is not None]; los = [lo for lo, u, dd in seq if lo is not None]
        if [x - ups[0] for x in ups] != [0, -1, 0, 1, 2, 3, 4, 5]: P(f'{lab}: the high line is not the decariana')
        if ups[0] % 12 != (kk + 7) % 12 or ups[0] - los[0] != 12: P(f'{lab}: the high line does not start an octave above the low')
        third = (kk + (3 if c['mode'] == 'minor' else 4)) % 12
        if [x - los[0] for x in los[:4]] != [0, 0, -1, -2] or los[4] % 12 != third or not 0 < los[3] - los[4] <= 2: P(f'{lab}: the low line {los}')
        if [dd for lo, u, dd in seq] != [0.5, 0.5, 0.5, 0.25, 0.25, 0.5, 0.5, 0.5, 0.5, 1]: P(f'{lab}: rhythm')
        got = steps_pitches(L['steps'])
        want = [sorted(x for x in (lo, u) if x is not None) for lo, u, dd in seq]
        if got != want: P(f'{lab}: strings and frets {got} vs {want}')
        for g in L['steps']: group_ok(g, lab)
    if d.startswith('octaves-end'):
        kk = pcn(c['key']); line = L['line']
        if line[0] % 12 != (kk + 7) % 12 or [x - line[0] for x in line] != [0, 1, 2, 4, 5]: P(f'{lab}: not 5, ♯5, 6, 7, 8')
        dec = d.endswith('dec')
        per = 3 if dec else 2
        for i in range(4):
            g = L['steps'][i * per]
            ms = sorted(OPN[s] + f for s, f in g)
            if ms != [line[i], line[i] + 12]: P(f'{lab}: octave {i} {ms}'); continue
            top = [x for x in g if OPN[x[0]] + x[1] == line[i] + 12][0]
            if dec:
                a, b = L['steps'][i * per + 1], L['steps'][i * per + 2]
                if a != [(top[0], top[1] - 1)] or b != [top]: P(f'{lab}: the decoration {a} {b}')
            elif L['steps'][i * per + 1] != [top]: P(f'{lab}: the repeat')
        want_d = [0.5, 0.25, 0.25] * 4 if dec else [0.5, 0.5] * 4
        if L['durs'] != want_d: P(f'{lab}: rhythm')
        lm = sorted(OPN[s] + f for s, f in L['land'])
        if lm != [line[4], line[4] + 12]: P(f'{lab}: the landing')
        for g in L['steps']: group_ok(g, lab)

by = {}
for L in E.LOG: by[L['device']] = by.get(L['device'], 0) + 1
print('cadences checked:', len(E.LOG), by)


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
                    nm = it[1].replace('♭', 'b').replace('♯', '#').replace('°7', 'dim7').replace(' minor', 'm')
                    p = gtr.check_grip(it[2], nm)
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
