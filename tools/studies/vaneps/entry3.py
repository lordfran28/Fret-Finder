"""Van Eps's super and sub series (book pp. 160–238; PDF 166–244), on his own definition: every triad is a
center; move one of its voices a step up the scale (super) or down (sub) and it becomes another sound, which goes
back to the center. Ours: the triads of E♭ major (I Wonder Who's Kissing Her Now) in first inversion, each one a
bar: the center, the moved voice, the center again, held. Upper voice super, middle voice super, and the two outer
voices in counter motion (closing in, the middle still), as in his Example B. The rhythm is ours; his
long series (every voice, every inversion, twelve keys, major and both minors) is named, not copied."""
import sys
sys.path.insert(0, '/home/claude/studies'); sys.path.insert(0, '/home/claude/studies/tango'); sys.path.insert(0, '/home/claude/studies/vaneps')
import entry2 as E2
import mel as M

EB, EB_N = E2.EB, E2.EB_N
CHECK = []
sys.path.insert(0, '/home/claude/scripts')
import gtr
NAMES12 = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']


def identify(ms):
    """a name the chord parser knows for these notes: the bass as root if it can be, else a slash chord"""
    pcs = {m % 12 for m in ms}; bass = min(ms) % 12
    found = []
    for r in range(12):
        rel = {(p - r) % 12 for p in pcs}
        for q, (req, opt) in gtr.QUAL.items():
            req = set(req); opt = set(opt)
            if req <= rel and rel <= (req | opt | {0}) and (0 in rel or 0 in req or q in ('', 'm', 'aug', 'dim7')):
                found.append((0 if r == bass else 1, len(q), r, q))
    if not found: return None
    k, _, r, q = min(found)
    name = NAMES12[r] + q
    return name if r == bass else name + '/' + NAMES12[bass]


def named(ms, fallback):
    n = identify(ms)
    assert n, ('no name for', ms)
    return n


def scale_notes(lo=40, hi=81): return [m for m in range(lo, hi) if m % 12 in EB]


SC = scale_notes()


def step(m, k): return SC[SC.index(m) + k]


def move(ms, voices):
    """voices: {index: +1 or -1} — each moved a scale step"""
    return [step(m, voices.get(i, 0)) if voices.get(i) else m for i, m in enumerate(ms)]


def place(ms, near):
    pl = E2.placements(ms, adjacent=True) or E2.placements(ms)
    return min(pl, key=lambda p: abs(p[2] - near))[1]


def series(id_, voices, degrees=(0, 1, 2, 3, 4, 5, 6), start_oct=3):
    bars = []
    for d in degrees:
        low = 12 * (start_oct + 1) + E2.low_pc('first', EB, d)
        while low < M.midi('G3'): low += 12
        got = None
        for up in (0, 12):
            c = [x + up for x in E2.voicing('first', EB, d, low)]
            if c[2] > 77: continue
            mv = move(c, voices)
            if (E2.placements(mv) and (E2.placements(c, adjacent=True) or E2.placements(c))):
                got = (c, mv); break
        if not got: continue                 # this triad's moved chord does not fit under one hand on three strings
        c, mv = got
        near = 7
        both = []                            # the center and the moved chord on the same three strings: only the moved voice's finger moves
        for ss, g, a in E2.placements(c):
            fr = [m - E2.OPEN[s_] for m, s_ in zip(mv, ss)]
            if min(fr) < 1 or max(fr) > 15 or max(fr) - min(fr) > (4 if min(fr) >= 7 else 3): continue
            gm_ = [-1] * 6
            for s_, f in zip(ss, fr): gm_[6 - s_] = f
            both.append((abs(a - near) + (0 if ss[0] - ss[2] == 2 else 0.5), g, gm_))
        if not both: continue
        _, gc, gm = min(both, key=lambda x: x[0])
        nm = EB_N[d]
        bars.append(dict(chords=[nm], note='', items=[['C', nm, gc, 1.0, {'roll': 0.004}], ['C', named(mv, nm), gm, 1.0, {'roll': 0.004}],
                                                     ['C', nm, gc, 2.0, {'roll': 0.004}]]))
        CHECK.append((id_, d, c, mv, voices))
    return bars


def T(text, p): return dict(where=f'{E2.BOOK}, p. {p - 6}', text=text, item=None, by='Van Eps', whose='Van Eps’s own', played='')


EX = []
b = series('upper-super', {2: +1})
b[0]['note'] = ('E♭ major, the scale’s triads in first inversion (root on top), one a bar: the triad, the same with its top voice a step up the scale, the triad again. '
                'The moved chord is named for what it sounds as.')
EX.append(dict(id='super-upper', title='Super: the upper voice a step up',
               idea=('Van Eps’s idea: every chord is a center. Move one of its voices a step up or down the scale and it becomes another center, which leads back. '
                     'Super is a voice a step up, sub a step down. He takes every voice of every inversion this way, in all twelve keys, major and both minors.'),
               quote=T('“All chords are centers”: the C major scale’s stations with every voice super and sub from its center; then the series key by key.', 167), bars=b))
b2 = series('middle-super', {1: +1})
b2[0]['note'] = 'The middle voice (the 5th) a step up, then back: the chord turns into another of the key over the same bass.'
EX.append(dict(id='super-middle', title='Super: the middle voice a step up', idea='The same with the middle voice moved a step up the scale.',
               quote=T('Middle voice super, key by key.', 175), bars=b2))
b3 = series('counter', {2: -1, 0: +1})
b3[0]['note'] = ('Both outer voices moved at once, closing in: the bottom a step up, the top a step down, the middle voice still; then back. '
                'Only the triads whose moved chord sits under one hand on three strings: ' + ', '.join(M.dname(b['chords'][0]) for b in b3) + '.')
EX.append(dict(id='counter', title='Super and sub in counter motion', idea='The bottom voice super and the top voice sub together, the middle voice standing still (or the other way, opening out).',
               quote=T('Example B: over C major in first inversion, the root a step up, the 3rd a step down, the 5th normal.', 167), bars=b3))
SECTIONS = E2.SECTIONS + [dict(id='vaneps-super', title='Super and sub', part='Exercises', ex=EX)]
