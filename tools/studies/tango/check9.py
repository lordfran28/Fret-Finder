"""Checks for entry9 (tango melody): every note of ours against the rule it stands for (his scale for the chord, his
chromatic devices, the blue notes, the guide-tone rules), the beats in every bar, the grips, and the length of every
quote (a beat or two)."""
import sys
sys.path.insert(0, '/home/claude/studies/tango'); sys.path.insert(0, '/home/claude/studies')
import entry9 as E
import mel as M
from quotes import _beats

probs, n_seg = [], 0
THREE = {'mayor-dentro', 'vecina'}          # Я вас любил is in 3/4


def bad(ex_, b, msg): probs.append(f'{ex_} bar {b + 1}: {msg}')


def tone(n, c): return M.is_tone(n, c)


def semis(a, b): return M.midi(b) - M.midi(a)


def guide_ok(n, c, cadence=False):
    if M.pc(n) in {M.pc(p + '4') for p, _ in M.guide_tones(c)}: return True
    return cadence and M.degree_of(n, c) == '1'


segs = {}
for ex_, bi, s in E.LINES: segs.setdefault(ex_, []).append((bi, s))

for ex_, L in segs.items():
    prev = None
    for k, (bi, s) in enumerate(L):
        n_seg += 1
        t, c, ns = s['chk'].get('type'), s['chord'], s['notes']
        if t == 'scale':
            root, kind = s['chk']['root'], s['chk']['kind']
            for n in ns:
                if not M.in_scale(n, root, kind): bad(ex_, bi, f'{n} not in {root} {kind} over {c}')
            if s['chk'].get('start_tone') and not tone(ns[0], c): bad(ex_, bi, f'{ns[0]} does not start {c} on a chord note')
            sc = M.scale_notes(root, kind, 'C1', 'C8')
            idx = [sc.index(n) if n in sc else None for n in ns]
            for a, b, x, y in zip(ns, ns[1:], idx, idx[1:]):
                if x is None or y is None or abs(x - y) != 1: bad(ex_, bi, f'{a}→{b} is not a step of {root} {kind}')
        elif t == 'chromatic-scale':
            pos = s['chk']['pos']
            for j, n in enumerate(ns):
                if M.in_scale(n, 'Eb', 'major'): continue
                # a chromatic note: on the same string as a scale note a semitone away, between scale notes or leading into one
                nbrs = [(ns[x], pos[x]) for x in (j - 1, j + 1) if 0 <= x < len(ns)]
                if not any(p[0] == pos[j][0] and abs(semis(n, m)) == 1 for m, p in nbrs): bad(ex_, bi, f'{n}: not a chromatic step on its string')
            for a, b in zip(ns, ns[1:]):
                if abs(semis(a, b)) > 3: bad(ex_, bi, f'{a}→{b} leaps')
        elif t == 'arp':
            pos, kinds = s['chk']['pos'], s['chk']['kinds']
            for j, (n, kd) in enumerate(zip(ns, kinds)):
                if kd == 'tone' and not tone(n, c): bad(ex_, bi, f'{n} not in {c}')
                if kd == 'fill':
                    if tone(n, c): bad(ex_, bi, f'{n} marked a fill but is a chord note')
                    if not (0 < j < len(ns) - 1 and pos[j - 1][0] == pos[j][0] == pos[j + 1][0] and semis(ns[j - 1], n) == 1 and semis(n, ns[j + 1]) == 1):
                        bad(ex_, bi, f'{n}: a fill must sit a semitone between two notes on its string')
        elif t == 'neighbour':
            T = ns[0]
            if not tone(T, c): bad(ex_, bi, f'target {T} not in {c}')
            want = [0, 1, 0, -1, 0]
            if [semis(T, n) for n in ns] != want: bad(ex_, bi, f'{ns} is not target, semitone above, target, semitone below, target')
        elif t == 'passing':
            if not (tone(ns[0], c) and tone(ns[-1], c)): bad(ex_, bi, f'{ns[0]} or {ns[-1]} not in {c}')
            st = {semis(a, b) for a, b in zip(ns, ns[1:])}
            if st not in ({-1}, {1}): bad(ex_, bi, f'{ns} is not semitones one way')
        elif t == 'combo':
            T, Y = s['chk']['target'], s['chk']['top']
            if [semis(T, n) for n in ns[:5]] != [0, 1, 0, -1, 0]: bad(ex_, bi, 'the neighbour figure is wrong')
            rest_ = ns[5:]
            if rest_[0] != Y or rest_[-1] != T or {semis(a, b) for a, b in zip(rest_, rest_[1:])} not in ({-1}, {1}): bad(ex_, bi, 'the passing notes are wrong')
            if not (tone(T, c) and tone(Y, c)): bad(ex_, bi, f'{T} or {Y} not in {c}')
        elif t == 'link':
            a = s['chk']['arp']
            for n in ns[:a + 1]:
                if not tone(n, c): bad(ex_, bi, f'{n} not in {c}')
            run_ = ns[a:] + [s['chk']['target']]
            if {semis(x, y) for x, y in zip(run_, run_[1:])} not in ({-1}, {1}): bad(ex_, bi, 'the link is not semitones one way')
            nxt = L[k + 1][1]
            if nxt['notes'][0] != s['chk']['target'] or not tone(nxt['notes'][0], s['chk']['next_chord']) or nxt['chord'] != s['chk']['next_chord']:
                bad(ex_, bi, 'the link does not land on the next chord')
        elif t == 'land':
            if not tone(ns[0], c): bad(ex_, bi, f'{ns[0]} not in {c}')
        elif t in ('chrom-a', 'chrom-b'):
            g = [ns[i:i + 4] for i in range(0, len(ns), 4)]
            shape_ = [0, -1, 0, 1] if t == 'chrom-a' else [0, -1, -2, -3]
            step = 2 if t == 'chrom-a' else -2
            for j, grp in enumerate(g):
                if [semis(grp[0], n) for n in grp] != shape_: bad(ex_, bi, f'group {grp} is not the pattern')
                if j and semis(g[j - 1][0], grp[0]) != step: bad(ex_, bi, f'group {grp} does not start a whole tone on')
            land = s['chk']['next_target']
            # a: the next group's first note; b: the descent's next semitone
            ok_land = semis(g[-1][0], land) == step if t == 'chrom-a' else semis(ns[-1], land) == -1
            if not ok_land or not tone(land, s['chk']['next_chord']): bad(ex_, bi, f'it does not land on {land}')
            if not tone(ns[0], c): bad(ex_, bi, f'{ns[0]} not in {c}')
        elif t == 'blue7':
            r = M.chord_parse(c)[0]
            cells = [ns[i:i + 3] for i in range(0, 9, 3)]
            for j, cell in enumerate(cells):
                if [M.degree_of(cell[0], c), semis(cell[0], cell[1]), semis(cell[1], cell[2])] != ['b7', 1, 1] or M.pc(cell[2]) != M.pc(r + '4'):
                    bad(ex_, bi, f'{cell} is not 7th, major 7th, root')
                if j and semis(cells[j - 1][0], cell[0]) != 12: bad(ex_, bi, 'the cells do not climb by octaves')
        elif t == 'blue4':
            r = s['chk']['root']
            sharp4 = [j for j, n in enumerate(ns) if (M.pc(n) - M.pc(r + '4')) % 12 == 6]
            if not sharp4: bad(ex_, bi, 'no raised 4th')
            for j in sharp4:
                nb = [ns[x] for x in (j - 1, j + 1) if 0 <= x < len(ns)]
                if not any(abs(semis(ns[j], m)) == 1 for m in nb): bad(ex_, bi, 'the raised 4th is not between the 4th and 5th')
        elif t == 'cluster':
            a, b = ns
            if M.degree_of(b, c) != '1' or semis(a, b) != 1: bad(ex_, bi, 'the cluster is not the major 7th and root')
        elif t == 'picardy':
            g = s['chk']['grip']
            ms = sorted(M.OPEN[6 - i] + g[i] for i in range(6) if g[i] >= 0)
            key = s['chk']['key']
            if (ms[-1] - M.midi(key + '4')) % 12 != 4: bad(ex_, bi, 'the top note is not the major 3rd')
            if {m % 12 for m in ms} != {M.pc(key + '4'), (M.pc(key + '4') + 4) % 12, (M.pc(key + '4') + 7) % 12}: bad(ex_, bi, 'not a major chord')
        elif t == 'guide':
            for n in ns:
                if not guide_ok(n, c, s['chk'].get('cadence')): bad(ex_, bi, f'{n} is not a guide tone of {c}')
        elif t == 'adorno':
            rule = M.rule_for(c, 'Eb', 'major', 'Bb7' if c == 'F7' else None) if c != 'Eb' or True else None
            for gt in s['chk']['guides']:
                if gt not in ns or not guide_ok(gt, c): bad(ex_, bi, f'guide tone {gt} missing over {c}')
            for j, n in enumerate(ns):
                if tone(n, c): continue
                if not M.in_scale(n, rule[1], rule[2]): bad(ex_, bi, f'{n} not in the scale over {c}')
                if j + 1 >= len(ns) or abs(semis(n, ns[j + 1])) > 2: bad(ex_, bi, f'{n} does not move by step to the next note')
        elif t == 'suspension':
            held, res = ns
            if prev is None or prev['notes'][-1] != held: bad(ex_, bi, 'the suspension is not held over')
            if tone(held, c) or not guide_ok(res, c) or abs(semis(held, res)) > 2: bad(ex_, bi, f'{held}→{res} is not a suspension resolving to a guide tone')
        elif t == 'anticipation':
            a, b = ns
            nxt = L[k + 1][1]
            if not guide_ok(a, c) or b != nxt['notes'][0] or not guide_ok(b, s['chk']['next_chord']): bad(ex_, bi, 'not an anticipation of the next guide tone')
        elif t == 'top':
            g = s['chk']['grip']
            ms = [(M.OPEN[6 - i] + g[i]) for i in range(6) if g[i] >= 0]
            if max(ms) != M.midi(ns[0]): bad(ex_, bi, f'{ns[0]} is not on top of {g}')
            if any(not M.is_tone(M.mk(0, 0, 4)[:0] + 'C4', c) and False for _ in ms): pass
            pcs = {M.pc(p + '4') for p in M.tone_pcs(c)}
            if any(m % 12 not in pcs for m in ms): bad(ex_, bi, f'{g} has a note outside {c}')
            if not guide_ok(ns[0], c): bad(ex_, bi, f'{ns[0]} is not a guide tone of {c}')
        else:
            bad(ex_, bi, f'unknown check {t}')
        # guide lines: no leap where the chord changes
        if t in ('guide', 'adorno', 'suspension', 'anticipation') and prev is not None and prev['chord'] != c:
            if abs(semis(prev['notes'][-1], ns[0])) > 2: bad(ex_, bi, f'leap at the change {prev["chord"]}→{c}: {prev["notes"][-1]}→{ns[0]}')
        prev = s
print('segments checked:', n_seg)


def span_ok(fr):
    fz = [f for f in fr if f > 0]
    if not fz: return True
    lo, hi = min(fz), max(fz)
    return hi - lo <= (4 if lo >= 7 else 3)


n_bars = 0
for S in E.SECTIONS:
    for ex_ in S['ex']:
        q = ex_['quote']
        if _beats(q.get('items') or []) > 2 + 1e-9: probs.append(f'{ex_["id"]}: quote too long')
        for j, b in enumerate(ex_['bars']):
            n_bars += 1
            L = 0.0
            for it in b['items']:
                if it[0] == 'K':
                    L += sum(h[0] for h in it[3])
                    if not span_ok(it[2]): probs.append(f'{ex_["id"]} bar {j + 1}: grip stretch {it[2]}')
                    for h in it[3]:
                        if isinstance(h[1], list) and any(it[2][6 - s_] < 0 for s_ in h[1]): probs.append(f'{ex_["id"]} bar {j + 1}: struck string not in grip')
                elif it[0] in ('R', 'P'):
                    L += sum(it[2])
                    if it[0] == 'R':
                        for (s_, f), nm in zip(it[1], it[3][1:].split('|')[0].split(',')):
                            if not 0 <= f <= 15: probs.append(f'{ex_["id"]} bar {j + 1}: fret {f}')
                elif it[0] == 'W': L += it[1]
            want = 3 if ex_['id'] in THREE else 4
            if abs(L - want) > 1e-6: probs.append(f'{ex_["id"]} bar {j + 1}: {L} beats, not {want}')
print('bars checked:', n_bars)
print('\n'.join(probs) if probs else 'all good')
sys.exit(1 if probs else 0)
