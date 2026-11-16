"""Checks every change entry11 made to the tune against the rule of its technique (written here separately, not with
entry11's own functions), the guide lines against Graciano's rules, and every bar drawn against the notes it stands for.
Run: python3 -B check11.py"""
import sys
sys.path.insert(0, '/home/claude/studies'); sys.path.insert(0, '/home/claude/studies/tango')
import mel as M
import tune_iw as TU
import entry11 as E

OPEN = {6: 40, 5: 45, 4: 50, 3: 55, 2: 59, 1: 64}
bad = []
EPS = 1e-6


def B(msg): bad.append(msg)


def key(e): return (round(e['t'], 6), e['n'])
def by_t(ev, t): return [e for e in ev if abs(e['t'] - t) < EPS]
def tune_only(ev): return [e for e in ev if e.get('tag') in (None, 'back')]


def chord(t):
    c = None
    for b, chs, notes, w in TU.in_eb(ending=2):
        for name, at in chs:
            tt = (0.0 if b == 0 else 1.0 + 3.0 * (b - 1)) + at
            if tt <= t + EPS: c = name
    return c


def tones(c): return {M.midi(p + '4') % 12 for p in M.tone_pcs(c)}


def scale_at(t):
    """the chord's scale by Graciano's rules (the next different chord decides a dominant's scale)"""
    c = chord(t); nxt = None
    for b, chs, notes, w in TU.in_eb(ending=2):
        for name, at in chs:
            tt = (0.0 if b == 0 else 1.0 + 3.0 * (b - 1)) + at
            if tt > t + EPS and name != c and nxt is None: nxt = name
    r = M.rule_for(c, 'Eb', 'major', nxt)
    return [M.midi(p + '4') % 12 for p in M.scale_pcs(r[1], r[2])]


def step_in_scale(a, b, sc):
    """b is the next note of the scale above (or below) a"""
    ma, mb = M.midi(a), M.midi(b)
    d = 1 if mb > ma else -1
    m = ma + d
    while m % 12 not in sc: m += d
    return m == mb


def pitches(ev): return [e['n'] for e in ev]


# ---------------------------------------------------------------- the tune itself
tune = E.TUNE
if pitches(tune)[:4] != ['Bb3', 'G4', 'Bb4', 'G4']: B('the tune does not start B♭, G, B♭, G')
if abs(tune[-1]['t'] + tune[-1]['d'] - (1 + 3 * 31 + 1)) > EPS: B(f'the tune ends at {tune[-1]["t"] + tune[-1]["d"]}')

# ---------------------------------------------------------------- each change against its rule
counts = {}
for L in E.LOG:
    k, p, bef, aft, ex = L['kind'], L['params'], L['before'], L['after'], L['ex']
    counts[k] = counts.get(k, 0) + 1
    tag = f'{ex} {k} {p}'
    if k in ('displace', 'pattern'):
        if pitches(bef) != pitches(aft): B(f'{tag}: notes changed'); continue
        i = next(j for j, e in enumerate(aft) if abs(e['t'] - p['t0']) < EPS)
        n = len(p['durs'])
        span_b = bef[i + n - 1]['t'] + bef[i + n - 1]['d'] - bef[i]['t']
        span_a = aft[i + n - 1]['t'] + aft[i + n - 1]['d'] - aft[i]['t']
        if abs(span_a - span_b) > EPS: B(f'{tag}: length {span_b} -> {span_a}')
        for j in range(i, i + n - 1):
            if abs(aft[j]['t'] + aft[j]['d'] - aft[j + 1]['t']) > EPS: B(f'{tag}: a gap after {aft[j]}')
        changed = sum(1 for j in range(i, i + n) if abs(aft[j]['d'] - bef[j]['d']) > EPS)
        if changed < 2: B(f'{tag}: only {changed} lengths changed')
        rest_b = [(x['t'], x['d']) for j, x in enumerate(bef) if not (i <= j < i + n)]
        rest_a = [(x['t'], x['d']) for j, x in enumerate(aft) if not (i <= j < i + n)]
        if rest_b != rest_a: B(f'{tag}: notes outside the change moved')
    elif k == 'delay':
        if pitches(bef) != pitches(aft): B(f'{tag}: notes changed'); continue
        later = 0
        for x, y in zip(bef, aft):
            if y['t'] < x['t'] - EPS: B(f'{tag}: {y["n"]} earlier')
            if y['t'] > x['t'] + EPS: later += 1
        for j in range(len(aft) - 1):
            if aft[j]['t'] + aft[j]['d'] > aft[j + 1]['t'] + EPS: B(f'{tag}: {aft[j]["n"]} overlaps the next note')
        gaps = sum(1 for j in range(len(aft) - 1) if aft[j + 1]['t'] - (aft[j]['t'] + aft[j]['d']) > EPS) \
            - sum(1 for j in range(len(bef) - 1) if bef[j + 1]['t'] - (bef[j]['t'] + bef[j]['d']) > EPS)
        if not later or gaps < 1: B(f'{tag}: no note comes in late after a rest')
        for x, y in zip(bef, aft):
            if y['t'] > x['t'] + EPS and abs(y['t'] % 1 - 0.5) > EPS: B(f'{tag}: {y["n"]} not on an off-beat')
    elif k == 'anticipate':
        if pitches(bef) != pitches(aft): B(f'{tag}: notes changed'); continue
        moved = [(x, y) for x, y in zip(bef, aft) if abs(x['t'] - y['t']) > EPS]
        if len(moved) != 1: B(f'{tag}: {len(moved)} notes moved'); continue
        x, y = moved[0]
        if not 0 < x['t'] - y['t'] <= 0.5 + EPS: B(f'{tag}: moved by {x["t"] - y["t"]}')
        if abs(x['t'] + x['d'] - (y['t'] + y['d'])) > EPS: B(f'{tag}: the early note does not hold through')
        if abs(x['t'] % 1) > EPS: B(f'{tag}: the note was not on a beat')
        j = aft.index(y)
        if aft[j - 1]['t'] + aft[j - 1]['d'] > y['t'] + EPS: B(f'{tag}: the note before overlaps')
    elif k == 'edit':
        A = {key(e) for e in aft}; Bf = {key(e) for e in bef}
        if not A < Bf: B(f'{tag}: notes added or moved')
        dropped = [e for e in bef if key(e) not in A]
        if not dropped: B(f'{tag}: nothing left out')
        bars = {E.bar_of(e['t']) for e in dropped}
        for e in aft:
            if E.bar_of(e['t']) in bars and M.midi(e['n']) % 12 not in tones(chord(e['t'])): B(f'{tag}: kept {e["n"]}, not in {chord(e["t"])}')
        for e in bef:
            if E.bar_of(e['t']) in bars and M.midi(e['n']) % 12 not in tones(chord(e['t'])) and key(e) in A: B(f'{tag}: {e["n"]} not a chord note but kept')
        for e in aft:
            x = next(z for z in bef if key(z) == key(e))
            if abs(x['d'] - e['d']) > EPS: B(f'{tag}: {e["n"]} changed length')
    elif k in ('fill_chrom', 'fill_diat'):
        old = [e for e in aft if e.get('tag') != 'fill' or key(e) in {key(z) for z in bef}]
        new = [e for e in aft if e not in old]
        if [key(e) for e in tune_only(old)] != [key(e) for e in tune_only(bef)] and [key(e) for e in old] != [key(e) for e in bef]:
            B(f'{tag}: the notes of the line moved')
        i = next(j for j, e in enumerate(aft) if abs(e['t'] - p['t']) < EPS and e.get('tag') != 'fill')
        a = aft[i]; fills = []
        j = i + 1
        while j < len(aft) and aft[j].get('tag') == 'fill': fills.append(aft[j]); j += 1
        b = aft[j]
        ia = next(z for z in bef if key(z) == key(a)); ib_ = [z for z in bef if key(z) == key(b)]
        if not ib_ or bef.index(ib_[0]) != bef.index(ia) + 1: B(f'{tag}: the fill is not between two neighbouring notes of the line'); continue
        ma, mb = M.midi(a['n']), M.midi(b['n'])
        if abs(mb - ma) < 3: B(f'{tag}: {a["n"]} to {b["n"]} is not a leap of a minor 3rd or more')
        ms = [M.midi(f['n']) for f in fills]
        if k == 'fill_chrom':
            want = list(range(ma + 1, mb)) if mb > ma else list(range(ma - 1, mb, -1))
            if ms != want: B(f'{tag}: fill {ms} is not the semitones between {ma} and {mb}')
        else:
            sc = scale_at(a['t'])
            want = [m for m in (range(ma + 1, mb) if mb > ma else range(ma - 1, mb, -1)) if m % 12 in sc]
            if ms != want: B(f'{tag}: fill {ms} is not the scale between')
        t = a['t'] + a['d']
        for f in fills:
            if abs(f['t'] - t) > EPS: B(f'{tag}: a gap in the fill'); break
            t += f['d']
        if abs(t - b['t']) > EPS: B(f'{tag}: the fill does not reach {b["n"]} on its beat')
        if abs(a['t'] - ia['t']) > EPS or abs(b['t'] - ib_[0]['t']) > EPS: B(f'{tag}: the tune’s notes moved')
        for f in fills:
            n = f['n']; up = mb > ma
            if k == 'fill_chrom' and up and 'b' in n[1:2] and M.midi(n) % 12 not in (3, 8, 10): B(f'{tag}: {n} spelled down on the way up')
            if k == 'fill_chrom' and not up and '#' in n: B(f'{tag}: {n} spelled up on the way down')
    elif k == 'neighbour':
        i = next(j for j, e in enumerate(aft) if abs(e['t'] - p['t']) < EPS)
        x0 = next(z for z in bef if abs(z['t'] - p['t']) < EPS)
        a, m, c = aft[i], aft[i + 1], aft[i + 2]
        if not (a['n'] == c['n'] == x0['n']): B(f'{tag}: not the same note on both sides')
        dd = M.midi(m['n']) - M.midi(x0['n'])
        if dd not in (-1, -2, 1, 2): B(f'{tag}: neighbour {m["n"]} is {dd} semitones away')
        if dd > 0: B(f'{tag}: the neighbour is above (Graciano: usually below; ours all below)')
        if abs(dd) == 2 and M.midi(m['n']) % 12 not in scale_at(m['t']): B(f'{tag}: a whole tone away but not in the scale')
        if abs(a['d'] + m['d'] + c['d'] - x0['d']) > EPS or abs(a['t'] - x0['t']) > EPS: B(f'{tag}: not in the note’s own time')
        if len(aft) != len(bef) + 2: B(f'{tag}: other notes added or lost')
    elif k == 'overshoot':
        i = next(j for j, e in enumerate(aft) if abs(e['t'] - p['t']) < EPS)
        x0 = next(z for z in bef if abs(z['t'] - p['t']) < EPS); pv = bef[bef.index(x0) - 1]
        o, c = aft[i], aft[i + 1]
        if c['n'] != x0['n'] or abs(c['t'] + c['d'] - (x0['t'] + x0['d'])) > EPS: B(f'{tag}: does not come back to {x0["n"]} in its time')
        leap = M.midi(x0['n']) - M.midi(pv['n'])
        if abs(leap) < 3: B(f'{tag}: {pv["n"]} to {x0["n"]} is not a leap')
        if not step_in_scale(x0['n'], o['n'], scale_at(x0['t'])) or (M.midi(o['n']) - M.midi(x0['n'])) * leap <= 0:
            B(f'{tag}: {o["n"]} is not one scale step beyond {x0["n"]}')
        if abs(o['t'] - x0['t']) > EPS: B(f'{tag}: the wider note is not on the written note’s beat')
    elif k == 'octave':
        diff = [(x, y) for x, y in zip(bef, aft) if x != y]
        if len(diff) != 1: B(f'{tag}: {len(diff)} notes changed'); continue
        x, y = diff[0]
        if M.midi(y['n']) - M.midi(x['n']) != 12 or y['n'][:-1] != x['n'][:-1] or x['t'] != y['t'] or x['d'] != y['d']: B(f'{tag}: not the same note an octave up')
    elif k == 'anacrusis':
        new = [e for e in aft if key(e) not in {key(z) for z in bef}]
        tgt = next(z for z in bef if abs(z['t'] - p['t']) < EPS)
        if abs((tgt['t'] - 1) % 3) > EPS: B(f'{tag}: the phrase does not start on a downbeat')
        for f in new:
            sounding = [z for z in bef if z['t'] - EPS < f['t'] < z['t'] + z['d'] - EPS]
            if sounding: B(f'{tag}: {f["n"]} where the tune is still sounding {sounding[0]["n"]}')
            if M.midi(f['n']) % 12 not in scale_at(f['t']): B(f'{tag}: {f["n"]} not in the scale of {chord(f["t"])}')
        seq = [f['n'] for f in new] + [tgt['n']]
        for a, b in zip(seq, seq[1:]):
            if not step_in_scale(a, b, scale_at(new[0]['t'])) or M.midi(b) <= M.midi(a): B(f'{tag}: {a} to {b} is not a step up the scale')
        if abs(new[-1]['t'] + new[-1]['d'] - tgt['t']) > EPS: B(f'{tag}: the pickup does not lead into the downbeat')
    elif k == 'mordent':
        i = next(j for j, e in enumerate(aft) if abs(e['t'] - p['t']) < EPS)
        x0 = next(z for z in bef if abs(z['t'] - p['t']) < EPS)
        a, m, c = aft[i], aft[i + 1], aft[i + 2]
        if not (a['n'] == c['n'] == x0['n']) or a['d'] > 0.25 or m['d'] > 0.25: B(f'{tag}: not a quick note, neighbour, note')
        if not step_in_scale(x0['n'], m['n'], scale_at(x0['t'])) or M.midi(m['n']) > M.midi(x0['n']): B(f'{tag}: {m["n"]} is not the scale note below')
        if abs(a['d'] + m['d'] + c['d'] - x0['d']) > EPS: B(f'{tag}: not in the note’s time')
    elif k.startswith('mark_'):
        f = k[5:]
        for x, y in zip(bef, aft):
            if {kk: v for kk, v in x.items() if kk != f} != {kk: v for kk, v in y.items() if kk != f}: B(f'{tag}: more than the mark changed')
        if len(bef) != len(aft): B(f'{tag}: notes added')
        if f == 'slur':
            for t in p['times']:
                y = by_t(aft, t)[0]; j = aft.index(y); pr = aft[j - 1]
                if abs(M.midi(y['n']) - M.midi(pr['n'])) > 2: B(f'{tag}: slur from {pr["n"]} to {y["n"]} is a leap')
    elif k == 'grela':
        new = [e for e in aft if e.get('tag') == 'guide']
        for g in new:
            c = chord(g['t']); gt = {M.midi(pc + '4') % 12 for pc, d in M.guide_tones(c)}
            if M.midi(g['n']) % 12 not in gt: B(f'{tag}: {g["n"]} is not a guide tone of {c}')
            host = [z for z in bef if z['t'] < g['t'] - EPS < z['t'] + z['d'] - 2 * EPS]
            if not host or host[0]['d'] < 2 - EPS: B(f'{tag}: {g["n"]} not inside a long note of the tune')
            else:
                h = host[0]
                if M.midi(g['n']) >= M.midi(h['n']): B(f'{tag}: {g["n"]} not below {h["n"]}')
                if abs(g['t'] + g['d'] - (h['t'] + h['d'])) > EPS: B(f'{tag}: {g["n"]} does not fill out {h["n"]}’s time')
        if [key(e) for e in aft if e.get('tag') != 'guide'] != [key(e) for e in bef]: B(f'{tag}: the tune’s notes moved')
    else:
        B(f'unknown change {k}')

# the two segments of each rhythmic pattern take the same rhythm
for exid in {L['ex'] for L in E.LOG if L['kind'] == 'pattern'}:
    pats = [L['params']['durs'] for L in E.LOG if L['ex'] == exid and L['kind'] == 'pattern']
    if len(pats) < 2 or any(x != pats[0] for x in pats): B(f'{exid}: the pattern is not the same on both segments')

# ---------------------------------------------------------------- the guide line against the tune
for exid, tw, cw, t0, t1 in E.COUNTERS:
    for c in cw:
        ch = chord(c['t'])
        cad = c is cw[-1]
        gt = {M.midi(pc + '4') % 12 for pc, d in M.guide_tones(ch)}
        if cad:
            if M.midi(c['n']) % 12 != M.midi('Eb4') % 12: B(f'{exid}: the cadence does not end on the key note')
        elif M.midi(c['n']) % 12 not in gt: B(f'{exid}: {c["n"]} is not a guide tone of {ch}')
        for u in tw:                                                     # never above the tune, never doubling its 3rd or 7th
            if u['t'] < c['t'] + c['d'] - EPS and c['t'] < u['t'] + u['d'] - EPS:
                if M.midi(c['n']) >= M.midi(u['n']): B(f'{exid}: {c["n"]} not under the tune’s {u["n"]}')
                deg = M.degree_of(u['n'], chord(u['t'])) if M.is_tone(u['n'], chord(u['t'])) else None
                if deg in ('3', 'b3', '7', 'b7') and M.midi(c['n']) % 12 == M.midi(u['n']) % 12: B(f'{exid}: doubles the tune’s {u["n"]}')
        both = [u for u in tw if abs(u['t'] - c['t']) < EPS]
        if both and not any(abs(tt - c['t']) < EPS for tt, _ in E.CHORDS): B(f'{exid}: {c["n"]} struck with the tune, not at a chord change')
    for u in tw:                                                         # the tune holds: the line moves
        if u['d'] >= 2 - EPS and not any(u['t'] + EPS < c['t'] < u['t'] + u['d'] - EPS for c in cw): B(f'{exid}: nothing moves under the long {u["n"]}')
    for b in range(E.bar_of(t0), E.bar_of(t1 - EPS) + 1):               # the tune moves in quarters: the line holds
        s = E.bar_start(b); us = [u for u in tw if s - EPS <= u['t'] < s + 3 - EPS]
        if len(us) == 3 and sum(1 for c in cw if s - EPS <= c['t'] < s + 3 - EPS) > 1: B(f'{exid}: bar {b}: the line moves against a moving tune')

# ---------------------------------------------------------------- the bars drawn against the notes
for exid, sel, bars, b0, b1 in E.SHOWN:
    got = []
    for k, Bb in enumerate(bars):
        b = b0 + k; t = E.bar_start(b)
        for it in Bb['items']:
            if it[0] == 'W': t += it[1]; continue
            names = it[3][1:].split('|')[0].split(',')
            for (s, f), d, nm in zip(it[1], it[2], names):
                got.append((round(t, 5), OPEN[s] + f, nm)); t += d
        if abs(t - E.bar_start(b) - E.bar_len(b)) > 1e-5: B(f'{exid}: bar {b} lasts {t - E.bar_start(b)}')
    want = [(round(e['t'], 5), M.midi(e['n']), M.disp(e['n'])) for e in sel]
    if len(got) != len(want) or any(abs(a[0] - b[0]) > 1e-4 or a[1:] != b[1:] for a, b in zip(got, want)):
        B(f'{exid}: the bars do not sound the notes'); print(got[:6], want[:6])
    for Bb in bars:
        for it in Bb['items']:
            if it[0] == 'R':
                frs = [f for s, f in it[1] if f > 0]
                for (s1, f1), (s2, f2) in zip(it[1], it[1][1:]):
                    pass
                ss = [s for s, f in it[1]]
                ext = it[4] if len(it) > 4 else {}
for exid, tw, cw, t0, t1 in E.COUNTERS:
    bars = next(x['bars'] for x in E.EXS['contracanto'] if x['id'] == exid)
    pbars = [Bb for Bb in bars if Bb['items'] and Bb['items'][0][0] == 'P']
    got = []
    for k, Bb in enumerate(pbars):
        t = E.bar_start(E.bar_of(t0) + k)
        it = Bb['items'][0]
        for g, d in zip(it[1], it[2]):
            for s, f in g: got.append((round(t, 5), OPEN[s] + f))
            t += d
    want = sorted([(round(e['t'], 5), M.midi(e['n'])) for e in tw + cw])
    if len(got) != len(want) or any(abs(a[0] - b[0]) > 1e-4 or a[1] != b[1] for a, b in zip(sorted(got), want)): B(f'{exid}: the two-line bars do not sound the two lines')

# slurs on one string
for exid, sel, bars, b0, b1 in E.SHOWN:
    flat = []
    for Bb in bars:
        for it in Bb['items']:
            if it[0] == 'R': flat += [(tuple(sf), sel_e) for sf, sel_e in zip(it[1], range(len(it[1])))]
    pos = []
    for Bb in bars:
        for it in Bb['items']:
            if it[0] == 'R': pos += [tuple(x) for x in it[1]]
    for j, e in enumerate(sel):
        if e.get('slur') and pos[j][0] != pos[j - 1][0]: B(f'{exid}: the slur into {e["n"]} changes string')

print('\n'.join(bad) if bad else f'entry11: every change follows its rule ({", ".join(f"{k} {v}" for k, v in sorted(counts.items()))}); '
      f'the guide lines are guide tones under the tune, moving where it holds; every bar sounds its notes')
