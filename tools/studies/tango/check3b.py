"""Checks for entry3b (milonga, second part): the milongueo basses follow Graciano's degrees and steps, the fills are
10ths or 6ths moving by step from the right chord notes, the chromatic fill, the cluster and the ♭VI7, every bar's
beats, every grip's stretch, every quote a beat or two."""
import sys
sys.path.insert(0, '/home/claude/studies/tango'); sys.path.insert(0, '/home/claude/studies')
import entry3b as E
import mel as M
from quotes import _beats
probs = []
def semis(a, b): return M.midi(b) - M.midi(a)
def deg(n, chord): return M.degree_of(n, chord)
SCALE = {'Cm7': ('Eb', 'major'), 'G7': ('C', 'harmonic minor'), 'Eb': ('Eb', 'major'), 'Bb7': ('Eb', 'major')}
def step(a, b, root, kind):
    sc = M.scale_notes(root, kind, 'C1', 'C7')
    return a in sc and b in sc and abs(sc.index(a) - sc.index(b)) == 1
def rel(n, chord):                     # semitones above the chord's root, 0..11
    r = M.chord_parse(chord)[0]
    return (M.pc(n) - M.pc(r + '4')) % 12
for r in E.RULES:
    k = r[0]
    if k in ('bass', 'milongueo', 'milongueo-aø', 'milongueo-vi'):
        chord, ns, why = r[1], r[2], r[3]
        bass = ns if k == 'bass' else [ns[0], ns[3], ns[6]]
        want = {'minor 1 b6 5': [0, 8, 7], 'dominant 1 b2 1': [0, 1, 0], 'major 1 6 5': [0, 9, 7], 'major dominant 1 2 1': [0, 2, 0]}
        if why in want:
            if [rel(n, chord) for n in bass] != want[why]: probs.append(f'{chord} {why}: {bass}')
        else:
            root, kind = {'minor step down': ('C', 'natural minor'), 'dominant melodic up': ('C', 'melodic minor'),
                          'major step down': ('Eb', 'major'), 'major dominant up': ('Eb', 'major')}[why]
            kind = 'major' if kind == 'natural minor' else kind
            root = 'Eb' if why == 'minor step down' else root          # C natural minor = E♭ major's notes
            for a, b in zip(bass, bass[1:]):
                if not step(a, b, root, kind): probs.append(f'{chord} {why}: {a}→{b} not a step')
            d = [semis(a, b) for a, b in zip(bass, bass[1:])]
            if ('down' in why) != all(x < 0 for x in d) or ('up' in why) != all(x > 0 for x in d): probs.append(f'{chord} {why}: wrong way')
        if k != 'bass':
            ups = [ns[1], ns[2], ns[4], ns[5], ns[7]]
            for u in ups:
                if k == 'milongueo' and not M.is_tone(u, chord): probs.append(f'{chord}: {u} not in the chord')
            if k == 'milongueo-aø' and {M.pc(ns[3]), M.pc(ns[4]), M.pc(ns[5])} != {M.pc('A4'), M.pc('Eb4'), M.pc('C4')}: probs.append('the A half-diminished is wrong')
            if k == 'milongueo-vi' and {M.pc(ns[3]), M.pc(ns[4]), M.pc(ns[5])} != {M.pc('C4'), M.pc('G4'), M.pc('Eb4')}: probs.append('the C minor 7 is wrong')
            if any(M.midi(u) <= M.midi(b) for u in ups for b in bass): probs.append(f'{chord}: a filling note under the bass')
    elif k in ('cbass1', 'cbass2', 'cgtr'):
        chord, ns = r[1], r[2]
        degs = [deg(n, chord) for n in ns]
        if None in degs: probs.append(f'{k} {chord}: a note outside the chord')
        if k == 'cbass1' and (len({M.midi(n) for n in ns[:3]}) != 1 or degs[0] != '1' or degs[3] != '5' or M.midi(ns[3]) > M.midi(ns[0])): probs.append(f'{k} {chord}')
        if k == 'cbass2' and (degs[:3] != ['1', degs[1], '5'] or degs[1] not in ('3', 'b3') or degs[3] != '5' or M.midi(ns[3]) > M.midi(ns[0])): probs.append(f'{k} {chord}')
        if k == 'cgtr' and (degs[0] != '1' or sorted(M.midi(n) for n in ns) != [M.midi(n) for n in ns]): probs.append(f'{k} {chord}')
    elif k in ('decimas-v-i', 'decimas-i-v', 'sextas-v-i', 'sextas-i-v'):
        chords, pairs = r[1], r[2]
        iv = (15, 16) if k.startswith('decimas') else (8, 9)
        for lo, hi in pairs:
            if semis(lo, hi) not in iv: probs.append(f'{k}: {lo}-{hi} is not a {"10th" if iv[0] == 15 else "6th"}')
        for lo, hi in pairs[:-1]:
            for n in (lo, hi):
                ok = M.in_scale(n, 'C', 'harmonic minor') if chords[0] == 'G7' else M.in_scale(n, 'Eb', 'major')
                if k == 'sextas-v-i': ok = ok or M.in_scale(n, 'C', 'melodic minor')
                if not ok: probs.append(f'{k}: {n} is outside the scale over {chords[0]}')
        first, last = pairs[0], pairs[-1]
        for n in first:
            if not M.is_tone(n, chords[0]) and deg(n, chords[0]) is None and not (chords[0] == 'G7' and M.pc(n) == M.pc('Ab4')): probs.append(f'{k}: {n} does not start on {chords[0]}')
        for n in last:
            if not M.is_tone(n, chords[1]): probs.append(f'{k}: {n} does not land on {chords[1]}')
        lows = [p[0] for p in pairs]
        for a, b in zip(lows, lows[1:]):
            if a == b: continue
            ch = chords[0] if b != last[0] else chords[1]
            root, kind = SCALE[chords[0]]
            if k.startswith('sextas-v') : root, kind = 'C', 'melodic minor'
            if not (step(a, b, root, kind) or step(a, b, 'C', 'harmonic minor') or step(a, b, 'Eb', 'major')): probs.append(f'{k}: {a}→{b} not a step')
    elif k == 'cromatico':
        ns = r[2]
        if not (M.is_tone(ns[0], 'Cm7') and M.is_tone(ns[0], 'G7')): probs.append('cromatico: the first note is not shared')
        if [semis(ns[0], n) for n in ns[:3]] != [0, -1, 0]: probs.append('cromatico: not the lower semitone turn')
        if deg(ns[3], 'Cm7') != 'b7' or [semis(a, b) for a, b in zip(ns[3:6], ns[4:6])] != [-1, -1] or deg(ns[6], 'G7') != 'b7': probs.append('cromatico: the fall is wrong')
    elif k == 'cluster':
        g = r[2]; ms = sorted(M.OPEN[6 - i] + g[i] for i in range(6) if g[i] >= 0)
        if ms[-1] - ms[-2] != 1 or ms[-1] % 12 != M.pc('G4') or any(m % 12 == M.pc('F4') for m in ms): probs.append('cluster wrong')
    elif k == 'bvi7':
        if (M.pc('Ab4') - M.pc('G4')) % 12 != 1: probs.append('bvi7')
    else:
        probs.append(f'unchecked {k}')


def span_ok(fr):
    fz = [f for f in fr if f > 0]
    return not fz or max(fz) - min(fz) <= (4 if min(fz) >= 7 else 3)


n_bars = 0
for S in E.SECTIONS[1:]:
    for ex in S['ex']:
        if _beats(ex['quote'].get('items') or []) > 2 + 1e-9: probs.append(f'{ex["id"]}: quote too long')
        want = 4 if ex['id'].startswith('contemporanea') else 2
        for j, b in enumerate(ex['bars']):
            n_bars += 1
            L = 0
            for it in b['items']:
                if it[0] == 'K':
                    L += sum(h[0] for h in it[3])
                    if not span_ok(it[2]): probs.append(f'{ex["id"]} bar {j + 1}: stretch {it[2]}')
                elif it[0] in ('R', 'P'): L += sum(it[2])
                elif it[0] == 'W': L += it[1]
            if abs(L - want) > 1e-6: probs.append(f'{ex["id"]} bar {j + 1}: {L} beats')
print('rules checked:', len(E.RULES), ' bars checked:', n_bars)
print('\n'.join(probs) if probs else 'all good')
sys.exit(1 if probs else 0)
