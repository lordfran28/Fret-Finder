"""Checks for entry10 (tango melodic patterns): every group of ours is the pattern's shape in the scale Graciano's rules
give its chord, each new chord starts on one of its own notes, the groups move a step at a time, the arpeggio parts
are the chord's notes in order and the scale parts steps of the scale, the chromatic cells are built as he builds them,
every bar has its beats and every quote is a beat or two."""
import sys
sys.path.insert(0, '/home/claude/studies/tango'); sys.path.insert(0, '/home/claude/studies')
import entry10 as E
import mel as M
from quotes import _beats

probs, n = [], 0
THREE = {'e9', 'e10', 't1', 't2', 't3', 't4'}


def bad(ex_, b, msg): probs.append(f'{ex_} bar {b + 1}: {msg}')


def sc_of(s):
    r = M.rule_for(s['chord'], s['key'], s['mode'], s['nxt'])
    if (r[1], r[2]) != (s['root'], s['kind']): raise AssertionError(('rule', s['chord'], r, s['root'], s['kind']))
    return M.scale_notes(r[1], r[2], 'C1', 'C8')


by_ex = {}
for ex_, bi, s in E.LINES: by_ex.setdefault(ex_, []).append((bi, s))
for ex_, L in by_ex.items():
    prev = None
    last_anchor = None
    for bi, s in L:
        n += 1
        sc = sc_of(s)
        c, ns = s['chord'], s['notes']
        if s.get('groups') is not None:
            i, flat, durs = 0, [], []
            for gi, (a, shp) in enumerate(s['groups']):
                want = [sc[sc.index(a) + o] for o in shp]
                got = ns[i:i + len(shp)]
                if got != want: bad(ex_, bi, f'group {got} is not {want}')
                if s['durs'][i:i + len(shp)] != list(s['rhythm']): bad(ex_, bi, 'the rhythm is not the pattern’s')
                new_chord = gi == 0 and (prev is None or prev['chord'] != c)
                if new_chord and not M.is_tone(got[0], c): bad(ex_, bi, f'{c} does not start on its own note ({got[0]})')
                if not new_chord and last_anchor is not None and gi + (0 if prev is None else 1) and last_anchor in sc:
                    if sc.index(a) - sc.index(last_anchor) != s['step'] and not (gi == 0 and prev is not None and prev.get('step') != s['step']):
                        bad(ex_, bi, f'the groups do not move a step ({last_anchor}→{a})')
                last_anchor = a; i += len(shp)
            if i != len(ns): bad(ex_, bi, 'notes left over')
        elif s.get('part') == 'arp':
            tones = [x for x in sc + [M.tr(t, 0, 0) for t in []] if False]
            ms = [M.midi(x) for x in ns]
            if not all(M.is_tone(x, c) for x in ns): bad(ex_, bi, f'a note outside {c}')
            d = 1 if ms[1] > ms[0] else -1
            for a, b in zip(ns, ns[1:]):
                between = [m for m in range(min(M.midi(a), M.midi(b)) + 1, max(M.midi(a), M.midi(b))) if any(M.pc(p + '4') == m % 12 for p in M.tone_pcs(c) if M.chord_parse(c)[1] in ('', 'm') or True)]
                tri = {M.pc(p + '4') for p, dg in M.chord_tones(c) if dg in ('1', '3', 'b3', '5')}
                if (M.midi(b) - M.midi(a)) * d <= 0: bad(ex_, bi, 'the arpeggio turns back')
                if any(m % 12 in tri for m in range(min(M.midi(a), M.midi(b)) + 1, max(M.midi(a), M.midi(b)))): bad(ex_, bi, f'{a}→{b} skips a note of the triad')
                if M.pc(a) not in tri or M.pc(b) not in tri: bad(ex_, bi, f'{a} or {b} is not in the triad')
        elif s.get('part') == 'scale':
            idx = [sc.index(x) if x in sc else None for x in ns]
            for a, b, x, y in zip(ns, ns[1:], idx, idx[1:]):
                if x is None or y is None or abs(x - y) != 1: bad(ex_, bi, f'{a}→{b} is not a step of the scale')
            if prev is not None:
                if prev['chord'] != c and not M.is_tone(ns[0], c): bad(ex_, bi, f'{c} does not start on its own note')
                if abs(M.midi(prev['notes'][-1]) - M.midi(ns[0])) > 2: bad(ex_, bi, 'the scale does not go on from the arpeggio')
        elif s.get('cell'):
            names, durs = E.CELLS[s['cell']]
            k = 0
            tones_up = []
            for T in s['targets']:
                if not M.is_tone(T, c): bad(ex_, bi, f'{T} not in {c}')
                above = sc[sc.index(T) + 1]
                want = [{'T': T, 'C': E.below(T), 'D': above}[x] for x in names]
                if ns[k:k + len(names)] != want: bad(ex_, bi, f'{ns[k:k + len(names)]} is not {want}')
                if M.midi(E.below(T)) != M.midi(T) - 1: bad(ex_, bi, 'not a semitone below')
                k += len(names)
            ts = [M.midi(t) for t in s['targets']]
            for a, b in zip(ts, ts[1:]):
                if b <= a or any(M.is_tone(M.mk(0, 0, 4), c) and False for _ in []): bad(ex_, bi, 'targets do not climb')
                if any(any(M.pc(p + '4') == m % 12 for p in M.tone_pcs(c)) for m in range(a + 1, b)): bad(ex_, bi, 'a chord note is skipped')
        else:
            bad(ex_, bi, 'unchecked segment')
        prev = s
print('segments checked:', n)

n_bars = 0
for S in E.SECTIONS:
    for ex_ in S['ex']:
        if _beats(ex_['quote'].get('items') or []) > 2 + 1e-9: probs.append(f'{ex_["id"]}: quote too long')
        for j, b in enumerate(ex_['bars']):
            n_bars += 1
            L = sum(sum(it[2]) for it in b['items'] if it[0] == 'R')
            want = 3 if ex_['id'] in THREE else 4
            if abs(L - want) > 1e-6: probs.append(f'{ex_["id"]} bar {j + 1}: {L} beats')
            for it in b['items']:
                for s_, f in it[1]:
                    if not 1 <= f <= 15: probs.append(f'{ex_["id"]} bar {j + 1}: fret {f}')
print('bars checked:', n_bars)
print('\n'.join(probs) if probs else 'all good')
sys.exit(1 if probs else 0)
