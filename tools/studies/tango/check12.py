"""Checks entry12 (Graciano ch. 8, the guitar alone) with its own code: every bar sounds the tune exactly, the fingering
can be played (one string per sounding note, the hand's stretch, four fingers, the tune on top on the first three
strings), and each part follows its rule: plain chords with the root lowest and the 3rd (and a dominant's 7th) heard;
the bass on root, 3rd and 5th, the 2nd passing, the 7th on dominants going down to the next chord's 3rd; every dressed
chord what its bar says it is. Run: python3 -B check12.py"""
import sys
sys.path.insert(0, '/home/claude/studies'); sys.path.insert(0, '/home/claude/studies/tango')
import mel as M
import entry12 as E

OPEN = {6: 40, 5: 45, 4: 50, 3: 55, 2: 59, 1: 64}
EPS = 1e-6
bad = []
def B(m): bad.append(m)
def pcs(names): return {M.midi(n + '4') % 12 for n in names}
ROOT = {'Eb': 'Eb', 'G': 'G', 'Ab': 'Ab', 'C7': 'C', 'Fm': 'F', 'F7': 'F', 'Bb7': 'Bb', 'F': 'F'}
TONES = {'Eb': ['Eb', 'G', 'Bb'], 'G': ['G', 'B', 'D'], 'Ab': ['Ab', 'C', 'Eb'], 'C7': ['C', 'E', 'G', 'Bb'], 'Fm': ['F', 'Ab', 'C'],
         'F7': ['F', 'A', 'C', 'Eb'], 'Bb7': ['Bb', 'D', 'F', 'Ab'], 'F': ['F', 'A', 'C']}
DOM = {'C7', 'F7', 'Bb7'}


def pc(n): return M.midi(n) % 12


def tune_bar(b):
    s, L = E.bs(b), E.bl(b)
    return [(round(e['t'] - s, 6), e['n'], round(e['d'], 6)) for e in E.TUNE if s - EPS <= e['t'] < s + L - EPS]


def playable(tag, evs, pos, carried):
    allev = carried[0] + evs; allpos = carried[1] + pos
    for e, (s, f) in zip(allev, allpos):
        if OPEN[s] + f != M.midi(e['n']): B(f'{tag}: {e["n"]} is not string {s} fret {f}')
    for i in range(len(allev)):
        for j in range(i + 1, len(allev)):
            a, b_ = allev[i], allev[j]
            if a['t'] < b_['t'] + b_['d'] - EPS and b_['t'] < a['t'] + a['d'] - EPS and allpos[i][0] == allpos[j][0]:
                B(f'{tag}: {a["n"]} and {b_["n"]} sound together on string {allpos[i][0]}')
    for t in sorted({e['t'] for e in evs}):
        now = [(e, p) for e, p in zip(allev, allpos) if e['t'] - EPS <= t < e['t'] + e['d'] - EPS]
        fr = [p[1] for e, p in now if p[1] > 0]
        if fr:
            lo, hi = min(fr), max(fr)
            if hi - lo > (4 if lo >= 7 else 3): B(f'{tag} at {t}: frets {lo}–{hi} are too wide')
            fingers = len(fr)
            if fingers > 4:
                at_lo = sum(1 for f in fr if f == lo)
                if at_lo < 2 or fingers - at_lo + 1 > 4: B(f'{tag} at {t}: more than four fingers')
        mel = [(e, p) for e, p in now if e['role'] == 'mel']
        for e, p in mel:
            if p[0] > 3: B(f'{tag} at {t}: the tune is on string {p[0]}')
            for o, q in now:
                if o['role'] != 'mel' and M.midi(o['n']) >= M.midi(e['n']): B(f'{tag} at {t}: {o["n"]} is not under the tune’s {e["n"]}')


def chord_heard(tag, name, acc, mel_now, need_tones=('3', '7')):
    tones = TONES[name]
    have = {pc(n) for n in acc} | {pc(n) for n in mel_now}
    for n in acc:
        if pc(n) not in pcs(tones): B(f'{tag}: {n} is not in {name}')
    if '3' in need_tones and M.midi(tones[1] + '4') % 12 not in have: B(f'{tag}: {name} without its 3rd')
    if '7' in need_tones and name in DOM and M.midi(tones[3] + '4') % 12 not in have: B(f'{tag}: {name} without its 7th')


def lowest(ns): return min(ns, key=M.midi)


def mel_sounding(evs, t0, t1, carried):
    return [e['n'] for e in carried[0] + evs if e['role'] == 'mel' and e['t'] < t1 - EPS and e['t'] + e['d'] > t0 + EPS]


DIM = {'Adim7': ('F7', ['A', 'C', 'Eb', 'Gb'], 'Gb'), 'Ddim7': ('Bb7', ['D', 'F', 'Ab', 'Cb'], 'Cb')}
SUBS = {'B7': ('F7', ['B', 'D#', 'F#', 'A'])}
M7B5 = {'Dm7b5': ('Fm', ['D', 'F', 'Ab', 'C'])}


def check_dressed(tag, b, evs, segs, soli, carried, nxt_root):
    for k, (t, d, name, bass, kind) in enumerate(segs):
        acc = [e['n'] for e in evs if e['role'] == 'acc' and e.get('tag') != 'soli' and abs(e['t'] - t) < EPS]
        if not acc: B(f'{tag} bar {b}: no chord at {t}'); continue
        lo = lowest(acc)
        mnow = mel_sounding(evs, t, t + d, carried)
        printed = E.chords_in(b)
        here = [c for tt, c in printed if tt <= t + EPS][-1]
        if kind in ('basic', 'bass'):
            if name != here: B(f'{tag} bar {b}: {name} is not the printed {here}')
            if pc(lo) != pc(ROOT[name] + '4'): B(f'{tag} bar {b}: {name} has {lo} at the bottom, not its root')
            if kind == 'basic': chord_heard(f'{tag} bar {b}', name, acc, mnow)
            if kind == 'bass' and len(acc) != 1: B(f'{tag} bar {b}: more than the bass under the two parts')
        elif kind in ('inv1', 'inv2', 'cadential'):
            want = TONES[name][1] if kind == 'inv1' else TONES[name][2]
            if pc(lo) != pc(want + '4'): B(f'{tag} bar {b}: {name} {kind} has {lo} at the bottom, not {want}')
            chord_heard(f'{tag} bar {b}', name, acc, mnow, need_tones=('3',) if kind == 'inv1' else ())
            if kind == 'inv1' and name != here and not (name == 'F' and here in ('F', 'Fm')): B(f'{tag} bar {b}: {name} is not the printed {here}')
            if kind == 'cadential':
                if name != 'Eb' or here != 'Bb7': B(f'{tag} bar {b}: the cadence is not E♭ over B♭ on the B♭7 bar')
                nxt = segs[k + 1] if k + 1 < len(segs) else None
                if not nxt or nxt[2] != 'Bb7' or pc(lowest([e['n'] for e in evs if e['role'] == 'acc' and abs(e['t'] - nxt[0]) < EPS])) != pc('Bb4'):
                    B(f'{tag} bar {b}: the 6/4 does not go to B♭7 on the same bass')
                if nxt_root != 'Eb': B(f'{tag} bar {b}: the cadence does not go home to E♭')
        elif kind == 'dim':
            dom, notes, b9 = DIM[name]
            if here != dom: B(f'{tag} bar {b}: {name} stands for {dom}, but the bar is {here}')
            if pc(notes[0] + '4') != pc(TONES[dom][1] + '4'): B(f'{tag} bar {b}: {name} is not on the 3rd of {dom}')
            for n in acc:
                if pc(n) not in pcs(notes): B(f'{tag} bar {b}: {n} not in {name}')
            for n in mnow:
                if pc(n) not in pcs(notes): B(f'{tag} bar {b}: the tune’s {n} is not in {name}')
            if pc(b9 + '4') not in {pc(n) for n in acc + mnow}: B(f'{tag} bar {b}: {name} without its flat 9th')
            if len({pc(n) for n in acc + mnow}) < 3: B(f'{tag} bar {b}: {name} too thin to hear')
        elif kind == 'tritone':
            dom, notes = SUBS[name]
            if here != dom: B(f'{tag} bar {b}: {name} for {dom}, but the bar is {here}')
            if (pc(notes[0] + '4') - pc(ROOT[dom] + '4')) % 12 != 6: B(f'{tag} bar {b}: {name} is not a tritone from {dom}')
            if (pc(notes[0] + '4') - pc(nxt_root + '4')) % 12 != 1: B(f'{tag} bar {b}: {name} does not fall a semitone to the next chord')
            for n in acc:
                if pc(n) not in pcs(notes): B(f'{tag} bar {b}: {n} not in {name}')
            for n in mnow:
                iv = (pc(n) - pc(notes[0] + '4')) % 12
                if iv not in (0, 4, 7, 10, 2, 6): B(f'{tag} bar {b}: the tune’s {n} over {name} is not a chord note, 9th or raised 11th')
            if pc(lo) != pc(notes[0] + '4'): B(f'{tag} bar {b}: {name} without its root at the bottom')
        elif kind == 'm7b5':
            minor, notes = M7B5[name]
            if here != minor: B(f'{tag} bar {b}: {name} replaces {minor}, but the bar is {here}')
            if (pc(ROOT[minor] + '4') - pc(notes[0] + '4')) % 12 != 3: B(f'{tag} bar {b}: {name} is not a minor 3rd under {minor}')
            for n in acc + mnow:
                if pc(n) not in pcs(notes): B(f'{tag} bar {b}: {n} not in {name}')
            if pc(lo) != pc(notes[0] + '4'): B(f'{tag} bar {b}: {name} without D at the bottom')
        else:
            B(f'{tag} bar {b}: unknown device {kind}')
    for t, d, how in (soli or []):
        voice = [e for e in evs if e.get('tag') == 'soli']
        mel = [e for e in evs if e['role'] == 'mel' and t - EPS <= e['t'] < t + d - EPS]
        if len(voice) != len(mel): B(f'{tag} bar {b}: the second part does not follow every note'); continue
        here = [c for tt, c in E.chords_in(b) if tt <= t + EPS][-1]
        nxt = {'C7': 'F7', 'F7': 'Bb7'}[here]
        r = M.rule_for(here, 'Eb', 'major', nxt)
        sc = [M.midi(p + '4') % 12 for p in M.scale_pcs(r[1], r[2])]
        for m, v in zip(sorted(mel, key=lambda e: e['t']), sorted(voice, key=lambda e: e['t'])):
            if abs(m['t'] - v['t']) > EPS or abs(m['d'] - v['d']) > EPS: B(f'{tag} bar {b}: the second part is not in rhythm with the tune')
            between = [x for x in range(M.midi(v['n']) + 1, M.midi(m['n'])) if x % 12 in sc]
            if pc(v['n']) not in sc or len(between) != 1 or not 3 <= M.midi(m['n']) - M.midi(v['n']) <= 4:
                B(f'{tag} bar {b}: {v["n"]} is not a 3rd under {m["n"]} in {M.disp(r[1] + "4")} {r[2]}')


BASS_OK = []
ARR = []
for exid, kind, data in E.SHOWN:
    carried = ([], [])
    prev_bass = None
    for k, (b, evs, pos, segs) in enumerate(data):
        tag = f'{exid} bar {b}'
        # the tune exactly as written
        got = sorted((round(e['t'], 6), e['n'], round(e['d'], 6)) for e in evs if e['role'] == 'mel')
        if got != tune_bar(b): B(f'{tag}: the tune is not as written')
        playable(tag, evs, pos, carried)
        L = E.bl(b)
        nc = ([dict(e, t=e['t'] - L) for e, p in zip(carried[0] + evs, carried[1] + pos) if e['t'] + e['d'] > L + EPS],
              [p for e, p in zip(carried[0] + evs, carried[1] + pos) if e['t'] + e['d'] > L + EPS])
        what = kind if kind != 'etude' else segs[0]
        S_ = segs if kind != 'etude' else (segs[1] if len(segs) > 1 else None)
        acc = [e for e in evs if e['role'] == 'acc']
        if what == 'mel':
            if acc: B(f'{tag}: notes other than the tune')
            if exid == 'arriba': ARR.extend(p[0] for p in pos)
        elif what == 'chord':
            for i, (t, name) in enumerate(S_):
                t1 = S_[i + 1][0] if i + 1 < len(S_) else L
                ch = [e['n'] for e in acc if abs(e['t'] - t) < EPS]
                if not ch: B(f'{tag}: no chord at {t}'); continue
                if any(abs(e['d'] - (t1 - t)) > EPS for e in acc if abs(e['t'] - t) < EPS): B(f'{tag}: the chord is not held to the next chord')
                if pc(lowest(ch)) != pc(ROOT[name] + '4'): B(f'{tag}: {name} with {lowest(ch)} at the bottom')
                chord_heard(tag, name, ch, mel_sounding(evs, t, t1, carried))
            if any(not any(abs(e['t'] - t) < EPS for t, _ in S_) for e in acc): B(f'{tag}: a chord note off the chord changes')
        elif what == 'bass':
            for e in sorted(acc, key=lambda e: e['t']):
                name = [c for tt, c in E.chords_in(b) if tt <= e['t'] + EPS][-1]
                deg = (pc(e['n']) - pc(ROOT[name] + '4')) % 12
                third = (pc(TONES[name][1] + '4') - pc(ROOT[name] + '4')) % 12
                ok = deg in (0, third, 7) or (deg == 10 and name in DOM)
                if deg == 2:                                          # the 2nd, passing by step
                    nxt_e = next((x for x in sorted(acc, key=lambda x: x['t']) if x['t'] > e['t'] + EPS), None)
                    if prev_bass and nxt_e is None and k + 1 < len(data):
                        nb = [x for x in data[k + 1][1] if x['role'] == 'acc']
                        nxt_e = min(nb, key=lambda x: x['t']) if nb else None
                    ok = bool(prev_bass and nxt_e and abs(M.midi(prev_bass) - M.midi(e['n'])) <= 2 and abs(M.midi(nxt_e['n']) - M.midi(e['n'])) <= 2
                              and (M.midi(prev_bass) - M.midi(e['n'])) * (M.midi(nxt_e['n']) - M.midi(e['n'])) < 0)
                if not ok: B(f'{tag}: bass {e["n"]} over {name} is not root, 3rd, 5th, a passing 2nd or a dominant’s 7th')
                if e['d'] not in (1.0, 2.0, 3.0): B(f'{tag}: bass {e["n"]} is not a quarter, half or dotted half')
                if name in DOM and deg == 10:
                    BASS_OK.append((exid, b, e['t'], e['n'], name))
                prev_bass = e['n']
        elif what in ('dressed',):
            segs3, soli, _ = S_
            nxt_bar = b + 1
            nxt_root = ROOT[E.chords_in(nxt_bar)[0][1]] if nxt_bar <= 32 and E.chords_in(nxt_bar) else 'Eb'
            if segs3: check_dressed(exid, b, evs, segs3, soli, carried, nxt_root)
        # notes held from before the bar line keep their strings
        carried = nc
        if acc and what != 'bass': prev_bass = None

share = sum(1 for x in ARR if x in (1, 2)) / max(1, len(ARR))
if share < 0.75: B(f'arriba: only {share:.0%} of the tune on the 1st and 2nd strings')
# every dominant's 7th in the bass goes down a step to the next chord's 3rd
for exid, kind, data in E.SHOWN:
    seq = []                                       # the lowest accompanying note at each place one is struck, whatever the texture
    for b, evs, pos, segs in data:
        acc = [e for e in evs if e['role'] == 'acc' and e.get('tag') != 'soli']
        for t in sorted({e['t'] for e in acc}):
            seq.append((b, t, lowest([e['n'] for e in acc if abs(e['t'] - t) < EPS])))
    for x, (b, t, n) in enumerate(seq):
        if any(ex_ == exid and bb == b and abs(tt - t) < EPS and nn == n for ex_, bb, tt, nn, ch_ in BASS_OK):
            if x + 1 >= len(seq): B(f'{exid}: the 7th {n} in bar {b} does not resolve'); continue
            nb, nt, nn = seq[x + 1]
            ch = [c for tt, c in E.chords_in(nb) if tt <= nt + EPS][-1]
            if pc(nn) != pc(TONES[ch][1] + '4') or not 1 <= M.midi(n) - M.midi(nn) <= 2:
                B(f'{exid}: the 7th {n} in bar {b} goes to {nn}, not down a step to the 3rd of {ch}')

print('\n'.join(bad) if bad else f'entry12: the tune exact in every bar, every bar playable, chords, bass lines and dressed chords as their rules say '
      f'({sum(len(d) for _, _, d in E.SHOWN)} bars, {len(BASS_OK)} dominant 7ths in the bass, all resolved; the tune alone {share:.0%} on the 1st and 2nd strings)')
