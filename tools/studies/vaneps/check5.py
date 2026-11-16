"""Independent checks for entry5 (Van Eps's chromatics). The expected notes are worked out here from the exercise's
own definition (key note, kind of triad, inversion, interval, bass), not taken from entry5's records, and compared
with what the page shows: chord names, grips, two-voice steps and their labels, the hand."""
import sys, re
sys.path.insert(0, '/home/claude/studies'); sys.path.insert(0, '/home/claude/studies/tango'); sys.path.insert(0, '/home/claude/studies/vaneps')
sys.path.insert(0, '/home/claude/scripts')
import entry5 as E
import gtr

OPENS = {6: 40, 5: 45, 4: 50, 3: 55, 2: 59, 1: 64}
LET = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
probs = []


def P(msg): probs.append(msg)


def midi_of(name):
    m = re.fullmatch(r'([A-G])([♭♯]?)(\d)', name)
    return 12 * (int(m.group(3)) + 1) + LET[m.group(1)] + {'♭': -1, '♯': 1, '': 0}[m.group(2)]


def pc_of(nm):
    m = re.fullmatch(r'([A-G])([♭♯]*)', nm)
    if not m: return None
    return (LET[m.group(1)] + m.group(2).count('♯') - m.group(2).count('♭')) % 12


def hand_ok(frets):
    fr = [f for f in frets if f > 0]
    if not fr: return True
    return max(fr) - min(fr) + 1 <= (5 if min(fr) >= 7 else 4)


def ex_by_id():
    out = {}
    for S in E.SECTIONS:
        for ex in S['ex']: out[ex['id']] = ex
    return out


EXS = ex_by_id()

# ------------------------------------------------------------------ chromatic triads over a pedal
TRI = {'chrom-maj-1st': (7, False, 1), 'chrom-maj-2nd': (7, False, 2), 'chrom-maj-root': (7, False, 0),
       'chrom-min-1st': (9, True, 1), 'chrom-min-2nd': (9, True, 2), 'chrom-min-root': (9, True, 0)}
assert {c['id'] for c in E.CHECK_TRI} == set(TRI), 'triad exercises'
n_ch = 0
for exid, (kpc, minor, inv) in TRI.items():
    ex = EXS.get(exid)
    if not ex: P(f'{exid}: not on the page'); continue
    bars = ex['bars']
    if len(bars) not in (13, 25): P(f'{exid}: {len(bars)} bars, not one or two octaves')
    prev = None
    for k, B in enumerate(bars):
        its = B['items']
        if len(its) != 1 or its[0][0] != 'C' or its[0][3] != 4.0: P(f'{exid} bar {k + 1}: not one chord of four beats'); continue
        _, name, grip, beats = its[0][:4]
        n_ch += 1
        if B['chords'] != [name]: P(f'{exid} bar {k + 1}: chord list {B["chords"]} vs {name}')
        notes = sorted((OPENS[6 - i] + f, 6 - i, f) for i, f in enumerate(grip) if f >= 0)
        if len(notes) != 4: P(f'{exid} bar {k + 1}: {len(notes)} notes'); continue
        ped, tri = notes[0], notes[1:]
        if ped[0] % 12 != kpc: P(f'{exid} bar {k + 1}: the bass is not the pedal')
        if any(f > 15 for _, _, f in notes): P(f'{exid} bar {k + 1}: above the 15th fret')
        ss = [s for _, s, _ in tri]
        if ss != sorted(ss, reverse=True) or ss[0] - ss[2] != 2: P(f'{exid} bar {k + 1}: triad not on three adjacent strings {ss}')
        if ped[1] <= ss[0]: P(f'{exid} bar {k + 1}: pedal not on a thicker string')
        if not hand_ok([f for _, _, f in notes]): P(f'{exid} bar {k + 1}: stretch {grip}')
        # the triad: the right kind and inversion
        m = [x for x, _, _ in tri]
        if m[2] - m[0] >= 12: P(f'{exid} bar {k + 1}: not a close triad')
        third = 3 if minor else 4
        want = {0: (third, 7), 1: (7 - third, 12 - third), 2: (5, 5 + third)}[inv]
        if (m[1] - m[0], m[2] - m[0]) != want: P(f'{exid} bar {k + 1}: wrong kind or inversion {m}')
        root = {0: m[0], 1: m[2] - 12, 2: m[1] - 12}[inv]
        if k == 0 and root % 12 != kpc: P(f'{exid}: does not start on the key’s own triad')
        if prev is not None and [a - b for a, b in zip(m, prev)] != [1, 1, 1]: P(f'{exid} bar {k + 1}: not a half step above the last')
        prev = m
        if k == len(bars) - 1 and (len(bars) - 1) % 12: P(f'{exid}: does not end on the key note')
        # the name
        try:
            r, q, bass = gtr.parse(name)
        except Exception as e:
            P(f'{exid} bar {k + 1}: name {name}: {e}'); continue
        if r != root % 12 or q != ('m' if minor else ''): P(f'{exid} bar {k + 1}: name {name} for root {root % 12}')
        if (bass if bass is not None else r) != kpc: P(f'{exid} bar {k + 1}: name {name} has the wrong bass')
        if gtr.chord_pcs(name) != {x % 12 for x, _, _ in notes}: P(f'{exid} bar {k + 1}: {name} does not match its notes')

# ------------------------------------------------------------------ the quotes of Van Eps's first two chords
for exid in TRI:
    q = EXS[exid]['quote']
    for it in q.get('items') or []:
        if it[0] != 'C': continue
        name, grip = it[1], it[2]
        if gtr.chord_pcs(name) != {(OPENS[6 - i] + f) % 12 for i, f in enumerate(grip) if f >= 0}:
            P(f'{exid}: quote {name} {grip} doesn’t match')
        r, qq, bass = gtr.parse(name)
        low = min(OPENS[6 - i] + f for i, f in enumerate(grip) if f >= 0)
        if low % 12 != (bass if bass is not None else r): P(f'{exid}: quote {name}: bass is not the lowest note')

# ------------------------------------------------------------------ chromatic scales in parallel intervals
PAR = {'par-oct': (12, 'E♭3'), 'par-10maj': (16, 'F2'), 'par-10min': (15, 'A2'), 'par-12': (19, 'F2'),
       'par-13maj': (21, 'F2'), 'par-13min': (20, 'A2'), 'par-15': (24, 'F2')}
assert {c['id'] for c in E.CHECK_PAR} == set(PAR), 'interval exercises'


def page_steps(ex, hold_want):
    steps, labels = [], []
    for j, B in enumerate(ex['bars']):
        if len(B['items']) != 1 or B['items'][0][0] != 'P': P(f'{ex["id"]} bar {j + 1}: not one two-voice item'); continue
        it = B['items'][0]
        if len(it) < 5 or it[4] != {'hold': hold_want}: P(f'{ex["id"]} bar {j + 1}: the sound is not told which notes ring')
        if abs(sum(it[2]) - 4) > 1e-9: P(f'{ex["id"]} bar {j + 1}: {sum(it[2])} beats')
        lab = it[3]
        if not lab.startswith('='): P(f'{ex["id"]} bar {j + 1}: no note names')
        names = lab[1:].split('|')[0].split(',')
        if len(names) != len(it[1]): P(f'{ex["id"]} bar {j + 1}: {len(names)} names for {len(it[1])} steps')
        for g, d, nm in zip(it[1], it[2], names):
            steps.append((g, d)); labels.append(nm)
    return steps, labels


def check_label(exid, i, g, nm):
    parts = nm.split('+')
    ms = sorted(OPENS[s] + f for s, f in g)
    if len(parts) != len(ms): P(f'{exid} step {i + 1}: label {nm} for {len(ms)} notes'); return
    for p_, m in zip(parts, ms):
        if pc_of(p_) != m % 12: P(f'{exid} step {i + 1}: label {p_} is not {m}')


for exid, (iv, start) in PAR.items():
    ex = EXS.get(exid)
    if not ex: P(f'{exid}: not on the page'); continue
    steps, labels = page_steps(ex, [])
    lo0 = midi_of(start)
    if len(steps) != 13: P(f'{exid}: {len(steps)} steps, not an octave of half steps')
    last_pos = None
    for k, ((g, d), nm) in enumerate(zip(steps, labels)):
        if len(g) != 2: P(f'{exid} step {k + 1}: not two notes'); continue
        (sa, fa), (sb, fb) = sorted(g, key=lambda x: -x[0])          # thicker string first
        lo, up = OPENS[sa] + fa, OPENS[sb] + fb
        if sa == sb: P(f'{exid} step {k + 1}: one string')
        if lo != lo0 + k: P(f'{exid} step {k + 1}: lower voice {lo}, wants {lo0 + k}')
        if up - lo != iv: P(f'{exid} step {k + 1}: {up - lo} apart, wants {iv}')
        if not hand_ok([fa, fb]) or max(fa, fb) > 15 or min(fa, fb) < 0: P(f'{exid} step {k + 1}: stretch {g}')
        pos = min([f for f in (fa, fb) if f > 0], default=None)
        if pos is not None and last_pos is not None and abs(pos - last_pos) > 5: P(f'{exid} step {k + 1}: the hand jumps {last_pos}→{pos}')
        if pos is not None: last_pos = pos
        if d != (4.0 if k == 12 else 1.0): P(f'{exid} step {k + 1}: length {d}')
        check_label(exid, k, g, nm)

# ------------------------------------------------------------------ the 10th to the 3rd over a held bass
HELD = {'held-maj-low': 'F2', 'held-maj-high': 'G3'}
assert {c['id'] for c in E.CHECK_HELD} == set(HELD), 'held exercises'
for exid, bass in HELD.items():
    ex = EXS.get(exid)
    if not ex: P(f'{exid}: not on the page'); continue
    b = midi_of(bass)
    want = [b + i for i in range(16, 3, -1)] + [b + i for i in range(4, 17)]
    rec = next(c for c in E.CHECK_HELD if c['id'] == exid)
    bs = rec['bass_at'][0]
    steps, labels = page_steps(ex, [bs])
    if len(steps) != 26: P(f'{exid}: {len(steps)} steps'); continue
    bass_pos, line_pos = set(), []
    for k, ((g, d), nm) in enumerate(zip(steps, labels)):
        i = k % 13
        bass_here = [x for x in g if x[0] == bs]
        rest = [x for x in g if x[0] != bs]
        if (i % 4 == 0) != bool(bass_here): P(f'{exid} step {k + 1}: the bass is struck at the wrong place')
        for s, f in bass_here:
            bass_pos.add((s, f))
            if OPENS[s] + f != b: P(f'{exid} step {k + 1}: bass {OPENS[s] + f} not {b}')
        if len(rest) != 1: P(f'{exid} step {k + 1}: {len(rest)} line notes'); continue
        s, f = rest[0]
        if OPENS[s] + f != want[k]: P(f'{exid} step {k + 1}: line {OPENS[s] + f}, wants {want[k]}')
        if s >= bs: P(f'{exid} step {k + 1}: line on a string not above the bass')
        line_pos.append((s, f))
        if d != (4.0 if i == 12 else 1.0): P(f'{exid} step {k + 1}: length {d}')
        check_label(exid, k, g, nm)
    if len(bass_pos) != 1: P(f'{exid}: the bass moves {bass_pos}')
    else:
        (s0, bf), = bass_pos
        fr = [f for _, f in line_pos if f > 0] + ([bf] if bf > 0 else [])
        if not hand_ok(fr): P(f'{exid}: the line leaves the hand that holds the bass ({min(fr)}–{max(fr)})')
        if bf > 0 and any(f == bf for _, f in line_pos) and bf != min(fr): P(f'{exid}: a line note on the bass’s fret not under the first finger')

print('triad chords checked:', n_ch, '· interval and held exercises:', len(PAR) + len(HELD))
print('\n'.join(probs) if probs else 'all good')
sys.exit(1 if probs else 0)
