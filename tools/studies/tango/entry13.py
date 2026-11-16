"""Tango fills (rellenos), rebuilt by rule: Graciano, Método de guitarra tango, ch. 3, pp. 27–33 of the owner's copy.
A relleno is a phrase put where the tune holds a note or stops, mostly on the top three strings.

Nothing of Graciano's is kept here beyond the opening beat or two of each example (the quotes). Every fill of ours is
made by one function per device, which applies his rule to a chord of one of the owner's songs:
Очи чёрные (A minor: E7, A minor, D minor), I Wonder Who's Kissing Her Now (E♭, with its C7 into F minor, F7 into B♭7)
and Я вас любил (G: D7, G). Each function logs what it made (LOG); check13.py rebuilds the rule with its own code and
checks every note, every rhythm, every string and fret, and the landing.

Two études: Очи чёрные's sixteen bars with a fill in every second bar, and the chorus of I Wonder Who's Kissing Her Now
(the 1909 waltz, tune_iw.py) with fills where the voice holds a note or rests.
"""
import sys
sys.path.insert(0, '/home/claude/studies'); sys.path.insert(0, '/home/claude/studies/tango')
import mel as M
from entry import K, st, arr, G4, GHOST, ACC
import tune_iw as TU

OPEN = M.OPEN                        # string number -> open midi (6: 40 ... 1: 64)
OCHI, IW, YVL = 'Очи чёрные', 'I Wonder Who’s Kissing Her Now', 'Я вас любил'
OWN = 'Graciano’s own'
LOG = []            # every fill we made: dict(ex, device, ctx, ev, pos, land)
EXS = {}


def where(p): return f'Método de guitarra tango, p. {p}'


def ex(sec, id, title, idea, quote, bars):
    EXS.setdefault(sec, []).append(dict(id=id, title=title, idea=idea, quote=quote, bars=bars))


def bar(chords, items, note=''): return dict(chords=chords, items=items, note=note)


# ---------------------------------------------------------------- spelling, scales, chords
SC = {'major': [(0, 0), (1, 2), (2, 4), (3, 5), (4, 7), (5, 9), (6, 11)],
      'natural': [(0, 0), (1, 2), (2, 3), (3, 5), (4, 7), (5, 8), (6, 10)],
      'harmonic': [(0, 0), (1, 2), (2, 3), (3, 5), (4, 7), (5, 8), (6, 11)],
      'melodic': [(0, 0), (1, 2), (2, 3), (3, 5), (4, 7), (5, 9), (6, 11)]}


def scale_list(key, kind):
    out = []
    for o in range(1, 7):
        for a, b in SC[kind]: out.append(M.tr(key + str(o), a, b))
    return sorted(out, key=M.midi)


def steps_from(note, key, kind, n, direction):
    """n notes of the key's scale from `note` (in the scale) by step, up (1) or down (-1)"""
    sl = scale_list(key, kind)
    i = sl.index(note)
    j = i + (n - 1) * direction
    if not 0 <= j < len(sl): raise ValueError('off the scale list')
    return [sl[i + k * direction] for k in range(n)]


def degree(key, kind, d, octave):
    """the scale's d-th degree (1..7) with its letter in `octave`"""
    a, b = SC[kind][d - 1]
    return M.tr(key + str(octave), a, b)


def root(ch): return M.chord_parse(ch)[0]


def tr_safe(n, steps, semis):
    """M.tr, but a double sharp or flat is written as the plain note it sounds (F double sharp as G)"""
    try: return M.tr(n, steps, semis)
    except AssertionError:
        for st_ in (steps + 1, steps - 1):
            try: return M.tr(n, st_, semis)
            except AssertionError: pass
        raise


def fam(ch): return M.FAMILY[M.chord_parse(ch)[1]]


def dn(ch):
    """a chord's name in prose: A minor, B♭7, E♭"""
    r, q, b = M.chord_parse(ch)
    out = M.dname(r) + {'m': ' minor'}.get(q, M.dname(q))
    return out + ('/' + M.dname(b) if b else '')


def nd(n): return M.disp(n)


STR = {6: 'low E string', 5: 'A string', 4: 'D string', 3: 'G string', 2: 'B string', 1: 'top string'}


def ordn(f): return 'open' if f == 0 else f'{f}{"th" if 10 <= f % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(f % 10, "th")}'


def say_run(notes, pos):
    """'E, G, F on the B string (5th, 8th, 6th fret), D, C on the G string (7th, 5th)'"""
    parts, cur = [], None
    for n, (s, f) in zip(notes, pos):
        if cur and cur[0] == s: cur[1].append(nd(n)); cur[2].append(f)
        else:
            cur = [s, [nd(n)], [f]]; parts.append(cur)
    out = []
    for k, (s, ns, fs) in enumerate(parts):
        frets = ', '.join(ordn(f) for f in fs)
        out.append(f'{", ".join(ns)} on the {STR[s]} ({frets}{" fret" if k == 0 else ""})')
    return '; '.join(out)


# ---------------------------------------------------------------- the songs' grips (bass and three notes, as the tango pages)
GR = {
    'ochi': {'Am': G4['Am'], 'E7': G4['E7'], 'Dm': G4['Dm'],
             'Am*': [5, 7, 7, 5, -1, -1],             # A minor as Graciano voices his landing chord: bass, 5th, root, 3rd
             'E7o': [0, -1, 2, 1, 3, -1]},            # E7 over the open low E
    'iw': {'Eb': [-1, 6, 8, 8, 8, -1],                 # the song page's barre at the 6th fret, root on the A string
           'Bb7': [6, -1, 6, 7, 6, -1],                # its B♭7 barre at the 6th, root on the low E string
           'C7': [8, -1, 8, 9, 8, -1], 'Fm': [-1, 8, 10, 10, 9, -1], 'F7': [-1, 8, 7, 8, 6, -1],
           'Ab': [4, -1, 6, 5, 4, -1], 'G': [3, -1, 5, 4, 3, -1], 'F': [-1, 8, 10, 10, 10, -1], 'Eb/Bb': [6, -1, 5, 3, 4, -1],
           'Fm*': [-1, 8, 10, 10, 9, -1], 'Eb*': [-1, 6, 8, 8, 8, -1],
           'C7lo': [-1, 3, 2, 3, 1, -1], 'F7lo': [1, -1, 1, 2, 1, -1], 'Bb7lo': [-1, 1, 3, 1, 3, -1]},     # the same chords lower on the neck
    'yvl': {'G': [3, -1, 5, 4, 3, -1], 'D7': [-1, 5, 4, 5, 3, -1], 'G*': [3, 5, 5, 4, -1, -1]},
}
SONG = {'ochi': OCHI, 'iw': IW, 'yvl': YVL}


def near_grip(song, ch, pos):
    """the song's grip for a chord (or its lower one) nearest a place on the neck"""
    G = GR[song]
    cands = [G[k] for k in (ch, ch + 'lo', ch + 'o') if k in G]
    return min(cands, key=lambda g: abs(gpos(g) - pos))


def gpos(g):
    fr = [f for f in g if f > 0]
    return sum(fr) / len(fr) if fr else 1


def bass_pitch(g):
    i = next(i for i in range(6) if g[i] >= 0)
    return OPEN[6 - i] + g[i], 6 - i, g[i]


LAND = [(0.5, 'B'), (1, 'C'), (0.5, 'B'), (1, 'C'), (1, '-')]       # his landing bar: bass, chord, bass, chord, rest
TWO = [(1, 'A'), (1, '-'), (1, 'A'), (1, '-')]                     # a stroke on 1 and on 3
FOUR = [(1, 'A')] * 4
SINC_L = [(0.5, 'A'), (1, 'A'), (0.5, 'A'), (1, 'A'), (1, '-')]    # his landing for the pattern fill: eighth, quarter, eighth, quarter, rest


# ---------------------------------------------------------------- a fill: events and strings
class Fill:
    """ev: [(beats, [notes], flag)]; flag '' plain, 'g' a ghost (the slide's first touch), 's' short, 'x' a dead note.
    pos: one list of (string, fret) per sounding event."""

    def __init__(self, ev, pos, device, ctx):
        self.ev, self.pos, self.device, self.ctx = ev, pos, device, ctx

    def beats(self): return sum(d for d, _, _ in self.ev)

    def notes(self): return [ns for d, ns, fl in self.ev if ns]

    def items(self, label, lead_rest=True):
        out = []
        kind = 'P' if any(len(ns) >= 2 for d, ns, fl in self.ev) else 'R'
        notes, durs, names, vel, short = [], [], [], [], []
        k = 0

        def flush():
            if notes:
                it = [kind, list(notes), list(durs), '=' + ','.join(names) + '|' + label]
                if kind == 'R' and (any(vel) or any(short)): it.append(dict(vel=list(vel), short=list(short)))
                out.append(it)
                notes.clear(); durs.clear(); names.clear(); vel.clear(); short.clear()
        for d, ns, fl in self.ev:
            if not ns:
                if notes and kind == 'R': durs[-1] += d; continue
                flush(); out.append(['W', d]); continue
            p = self.pos[k]; k += 1
            for (s, f), n in zip(p, ns): assert OPEN[s] + f == M.midi(n), (n, s, f)
            notes.append([list(x) for x in p] if kind == 'P' else list(p[0])); durs.append(d)
            nm = '+'.join(nd(n) for n in ns)
            names.append(('x ' + nm) if fl == 'x' else nm)
            vel.append(GHOST if fl in ('g', 'x') else 0); short.append(1 if fl in ('s', 'x') else 0)
        flush()
        return out

    def log(self, exid, land=None):
        LOG.append(dict(ex=exid, device=self.device, ctx=dict(self.ctx), ev=[(d, list(ns), fl) for d, ns, fl in self.ev],
                        pos=[[tuple(x) for x in p] for p in self.pos], land=land))
        return self


def width(h): return 4 if h >= 7 else 3          # the hand covers h..h+3, from the 7th fret h..h+4


def finger_line(notes, near, strings=(1, 2, 3)):
    """strings and frets for a single line, no open strings: every note inside the hand (index finger at fret h), a shift of
    the hand costs most, then distance from `near`, string changes and long jumps on one string"""
    ms = [M.midi(n) for n in notes]
    layers = []
    for i, m in enumerate(ms):
        cur = {}
        for s in strings:
            f = m - OPEN[s]
            if not 1 <= f <= 15: continue
            for h in range(max(1, f - 4), f + 1):
                if f > h + width(h): continue
                if i == 0:
                    cur[(s, f, h)] = (0.15 * abs(h - near) + 0.01 * f, None); continue
                best = None
                for (s0, f0, h0), (c0, _) in layers[-1].items():
                    c = (c0 + (0 if h == h0 else 2 + 0.3 * abs(h - h0)) + 0.1 * abs(s - s0) + 0.01 * f + 0.15 * abs(h - near)
                         + (0.6 if s == s0 and abs(f - f0) > 2 else 0))
                    if best is None or c < best[0]: best = (c, (s0, f0, h0))
                if best: cur[(s, f, h)] = best
        assert cur, (notes[i], 'cannot be played here')
        layers.append(cur)
    k = min(layers[-1], key=lambda k: layers[-1][k][0])
    cost = layers[-1][k][0]
    path = [k]
    for i in range(len(layers) - 1, 0, -1):
        k = layers[i][k][1]; path.append(k)
    path.reverse()
    return [(s, f) for s, f, h in path], cost


def best_octave(make, near, strings_sets=((1, 2, 3), (1, 2, 3, 4)), octaves=range(2, 7)):
    """make(octave) -> notes or None; the octave whose notes finger best on the given strings near the hand"""
    best = None
    for ss in strings_sets:
        for o in octaves:
            try: ns = make(o)
            except ValueError: continue
            if not ns: continue
            try:
                pos, c = finger_line(ns, near, ss)
            except AssertionError:
                continue
            if any(f > 15 for s, f in pos): continue
            if best is None or c < best[0]: best = (c, ns, pos)
        if best: return best[1], best[2]
    raise ValueError('no octave fits')


# ================================================================ the devices, one function each
def scale_down(dom, ton, mode, near):
    """p. 27: over the dominant, a sixteenth rest and seven sixteenths: its root (the key's 5th), up a 3rd to the key's 7th
    (in minor the natural minor's, not the leading note), then down the key's scale to its 2nd; the tonic falls on the next downbeat."""
    key = root(ton); kind = 'natural' if mode == 'minor' else 'major'

    def make(o):
        first = degree(key, kind, 5, o)
        if M.pc(first) != M.pc(root(dom) + '4'): return None
        sev = degree(key, kind, 7, o)
        if M.midi(sev) < M.midi(first): sev = degree(key, kind, 7, o + 1)
        down = steps_from(sev, key, kind, 6, -1)
        return [first] + down
    ns, pos = best_octave(make, near)
    ev = [(0.25, [], '')] + [(0.25, [n], '') for n in ns]
    return Fill(ev, [[p] for p in pos], 'scale-down', dict(dom=dom, ton=ton, mode=mode, key=key))


def scale_up(ton, dom, mode, near):
    """p. 27–28: a sixteenth rest and seven sixteenths climbing from the key's 5th to the 4th above it (in minor with the
    6th and 7th raised, the melodic minor going up), so the dominant's root falls on the next downbeat."""
    key = root(ton); kind = 'melodic' if mode == 'minor' else 'major'

    def make(o):
        first = degree(key, kind, 5, o)
        return steps_from(first, key, kind, 7, 1)
    ns, pos = best_octave(make, near)
    ev = [(0.25, [], '')] + [(0.25, [n], '') for n in ns]
    return Fill(ev, [[p] for p in pos], 'scale-up', dict(dom=dom, ton=ton, mode=mode, key=key))


def pattern(ton, dom, mode, near):
    """p. 28: groups of four sixteenths, a note, the step below it, the note again, the step above; the next group starts
    a step above the last; from the key's root, two groups into the dominant (in minor the leading note below the root)."""
    key = root(ton); kind = 'harmonic' if mode == 'minor' else 'major'

    def make(o):
        x = degree(key, kind, 1, o)
        out = []
        for g in range(2):
            lo = steps_from(x, key, kind, 2, -1)[1]; hi = steps_from(x, key, kind, 2, 1)[1]
            out += [x, lo, x, hi]
            x = steps_from(hi, key, kind, 2, 1)[1]
        return out
    ns, pos = best_octave(make, near)
    ev = [(0.25, [n], '') for n in ns]
    return Fill(ev, [[p] for p in pos], 'pattern', dict(dom=dom, ton=ton, mode=mode, key=key))


def slide_from(n, semis): return M.tr(n, -1, -2) if semis == 2 else tr_safe(n, -1, -1) if semis == 1 else None


def campanitas(dom, way):
    """p. 28: the dominant's root alone, in octaves, climbing the neck. Way 1: the root, the octave above, the same octave
    again on the next string down (slid into), then the octave above that, short; the strings as his, skipping one up, one
    back, one more up. Way 2: the octave rocking between the G string and the top string."""
    r = root(dom)
    if way == 1:
        best = None
        for a in (4, 5, 6):
            ss = [a, a - 2, a - 1, a - 3]
            for o in range(1, 5):
                ns = [r + str(o), r + str(o + 1), r + str(o + 1), r + str(o + 2)]
                fr = [M.midi(n) - OPEN[s] for n, s in zip(ns, ss)]
                if any(f < 1 or f > 15 for f in fr): continue
                if not all(x < y for x, y in zip(fr, fr[1:])): continue          # climbing the neck
                if fr[0] < 2 or fr[2] < 2: continue                             # room to slide in (from the 1st fret at least)
                c = max(fr)
                if best is None or c < best[0]: best = (c, ns, ss, fr)
        assert best, ('no campanitas for', dom)
        c, ns, ss, fr = best
        f0, f2 = max(1, fr[0] - 2), max(1, fr[2] - 2)                       # each slide from a tone below, or a semitone where the neck ends
        g0 = slide_from(ns[0], fr[0] - f0); g2 = slide_from(ns[2], fr[2] - f2)
        ev = [(0.125, [g0], 'g'), (0.5, [ns[0]], ''), (0.375, [ns[1]], 's'), (0.125, [g2], 'g'), (0.5, [ns[2]], ''), (1.0, [ns[3]], 's')]
        pos = [[(ss[0], f0)], [(ss[0], fr[0])], [(ss[1], fr[1])], [(ss[2], f2)], [(ss[2], fr[2])], [(ss[3], fr[3])]]
        return Fill(ev, pos, 'campanitas-1', dict(dom=dom))
    # way 2: the G string and the top string
    for o in range(2, 6):
        lo, hi = r + str(o), r + str(o + 1)
        f3, f1 = M.midi(lo) - OPEN[3], M.midi(hi) - OPEN[1]
        if 2 <= f3 <= 15 and 1 <= f1 <= 15: break
    else:
        raise AssertionError(('no campanitas 2 for', dom))
    g = slide_from(lo, 2)
    ev = [(0.125, [g], 'g'), (0.5, [lo], ''), (0.5, [hi], 's'), (0.5, [lo], ''), (0.25, [hi], ''), (0.25, [lo], ''), (0.5, [hi], '')]
    pos = [[(3, f3 - 2)], [(3, f3)], [(1, f1)], [(3, f3)], [(1, f1)], [(3, f3)], [(1, f1)]]
    return Fill(ev, pos, 'campanitas-2', dict(dom=dom))


TEN = {'maj': ([(0, 0), (1, 2), (1, 3), (2, 4)], [(2, 4), (3, 5), (3, 6), (4, 7)]),       # 1 2 ♯2 3 under 3 4 ♯4 5
       'min': ([(0, 0), (1, 1), (1, 2), (2, 3)], [(2, 3), (3, 5), (3, 6), (4, 7)])}       # 1 ♭2 2 ♭3 under ♭3 4 ♯4 5
TEN_RHY = {'plain': [0.5, 0.5, 0.5, 2], 'phrased': [1, 0.25, 0.25, 2]}


def tenths(chord, phrased, strings):
    """p. 29: a note and its tenth moving together, from the chord's root and 3rd to its 3rd and 5th: over a major (or
    dominant) chord the lower voice climbs a tone and two semitones, the upper a semitone and two semitones; over a minor
    chord the lower climbs by semitones, the upper a tone and two semitones. Plain eighths, or phrased (a quarter, two
    sixteenths), the last pair held; on the A and B strings, the low E and G, or the D and top strings."""
    q = 'min' if fam(chord) == 'min' else 'maj'
    lo_iv, hi_iv = TEN[q]
    s_lo, s_hi = strings
    r = root(chord)
    for o in range(1, 5):
        base = r + str(o)
        pairs = [[tr_safe(base, a, b), tr_safe(base, c + 7, d + 12)] for (a, b), (c, d) in zip(lo_iv, hi_iv)]
        fr = [(M.midi(x) - OPEN[s_lo], M.midi(y) - OPEN[s_hi]) for x, y in pairs]
        if all(1 <= a <= 15 and 1 <= b <= 15 for a, b in fr): break
    else:
        raise AssertionError(('no tenths for', chord, strings))
    rh = TEN_RHY['phrased' if phrased else 'plain']
    ev = [(0.5, [], '')] + [(d, p, '') for d, p in zip(rh, pairs)]
    pos = [[(s_lo, a), (s_hi, b)] for a, b in fr]
    return Fill(ev, pos, 'tenths', dict(chord=chord, q=q, phrased=phrased, strings=list(strings)))


def octaves(way, ton, dom, mode, land_grip, pair):
    """p. 30: broken octaves in eighths, the lower note first, three steps of the key's scale, then an x: the bass string
    struck dead where the next chord's bass is. From the tonic down (1, 7, 6) to the dominant, the x on the dominant's root;
    from the dominant up (5, 6, 7, in minor the melodic minor's raised 6th and 7th) to the tonic, the x on that 7th, a fret
    under the tonic's bass."""
    key = root(ton)
    if way == 'td': kind, start_deg, direction = ('natural' if mode == 'minor' else 'major'), 1, -1
    else: kind, start_deg, direction = ('melodic' if mode == 'minor' else 'major'), 5, 1
    s_lo, s_hi = pair
    lb, ls, lf = bass_pitch(land_grip)
    for o in range(2, 5):
        first = degree(key, kind, start_deg, o)
        line = steps_from(first, key, kind, 3, direction)
        fr = [(M.midi(n) - OPEN[s_lo], M.midi(n) + 12 - OPEN[s_hi]) for n in line]
        if all(1 <= a <= 15 and 1 <= b <= 15 and 0 <= b - a <= 3 for a, b in fr): break
    else:
        raise AssertionError(('no octaves for', way, ton, pair))
    xm = lb if way == 'td' else lb - 1
    xname = M.tr(line[-1], 0, 0) if way == 'dt' else steps_from(line[-1], key, kind, 2, -1)[1]
    # the x's own octave: the bass's
    while M.midi(xname) > xm: xname = M.tr(xname, -7, -12)
    while M.midi(xname) < xm: xname = M.tr(xname, 7, 12)
    assert M.midi(xname) == xm, (xname, xm)
    ev = [(0.5, [], '')]
    pos = []
    for n, (a, b) in zip(line, fr):
        ev += [(0.5, [n], ''), (0.5, [M.tr(n, 7, 12)], '')]
        pos += [[(s_lo, a)], [(s_hi, b)]]
    ev.append((0.5, [xname], 'x')); pos.append([(ls, xm - OPEN[ls])])
    return Fill(ev, pos, 'octaves-' + way, dict(ton=ton, dom=dom, mode=mode, key=key, pair=list(pair), land_bass=lb))


def chromatic_below(n):
    """the two notes a tone and a semitone below n, spelled as a line climbing into it"""
    two = M.tr(n, -1, -2)
    one = M.tr(two, 0, 1) if M.pc_name(two)[-1:] != '#' else M.tr(n, 0, -1)
    if M.pc_name(one) in ('E#', 'B#'): one = M.tr(n, 0, -1)
    return two, one


INTV = {'sixth': (-5, 'sixth'), 'third': (-2, 'third')}


def dyad_slide(chord, target, interval, near, pairs=((4, 2), (3, 1), (4, 3), (3, 2), (2, 1), (5, 3), (5, 4))):
    """pp. 30–32: inside one chord, two notes a sixth (or a third) apart slide up by semitones, two steps, onto two of its
    notes, the target on top: eighth rest, a quarter, an eighth, the target a quarter, a rest. The lower note of the target
    is the chord's own note a sixth (third) below it (for a minor chord's 5th that is its minor 7th, as in his)."""
    r, q, _ = M.chord_parse(chord)
    tones = {M.pc_name(p): d for p, d in M.chord_tones(chord)}
    if fam(chord) == 'min': tones[M.pc_name(M.tr(r + '4', 6, 10))] = 'b7'
    tdeg = {'root': ['1'], '3rd': ['3', 'b3'], '5th': ['5'], '7th': ['b7']}[target]
    tpc = next(p for p, d in tones.items() if d in tdeg)
    steps = INTV[interval][0]
    best = None
    for o in range(2, 6):
        top = tpc + str(o)
        # the chord's note whose letter lies `steps` letters below
        L = M.LET[(M.LET.index(tpc[0]) + steps) % 7]
        cand = [p for p in tones if p[0] == L]
        assert len(cand) == 1, (chord, target, L, tones)
        lo_pc = cand[0]
        lo = next(lo_pc + str(oo) for oo in range(o, o - 3, -1) if M.midi(lo_pc + str(oo)) < M.midi(top) and M.midi(top) - M.midi(lo_pc + str(oo)) < 12)
        a2, a1 = chromatic_below(lo); b2, b1 = chromatic_below(top)
        seq = [[a2, b2], [a1, b1], [lo, top]]
        for sl, sh in pairs:
            fr = [(M.midi(x) - OPEN[sl], M.midi(y) - OPEN[sh]) for x, y in seq]
            if not all(1 <= a <= 15 and 1 <= b <= 15 for a, b in fr): continue
            if any(abs(a - b) > 3 for a, b in fr): continue
            c = abs((fr[2][0] + fr[2][1]) / 2 - near) + 0.3 * (sl - sh - 1)
            if best is None or c < best[0]: best = (c, seq, [[(sl, a), (sh, b)] for a, b in fr])
    assert best, ('no dyads for', chord, target, interval)
    c, seq, pos = best
    ev = [(0.5, [], ''), (1, seq[0], ''), (0.5, seq[1], ''), (1, seq[2], ''), (1, [], '')]
    return Fill(ev, pos, interval + 's', dict(chord=chord, target=target, interval=interval))


DROP2 = {'7': ['b7', '3', '5', '1'], '1': ['1', '5', 'b7', '3'], '3': ['3', 'b7', '1', '5']}
ORD = {1: ['7', '1', '3', '1'], 2: ['7', '3', '1', '7'], 3: ['7', '3', '1', '3'], 4: ['7', '1', '7', '3']}


def inversions(dom, which):
    """every way to play the dominant 7th on the four top strings, the D string lowest, with its 7th, root or 3rd in the bass
    (the next notes of the chord above it in Graciano's order: 7 3 5 1, 1 5 7 3, 3 7 1 5): [(notes, grip)]"""
    tones = {d: p for p, d in M.chord_tones(dom)}
    out = []
    for o in range(2, 5):
        ns = [tones[DROP2[which][0]] + str(o)]
        for d in DROP2[which][1:]:
            p = tones[d]
            ns.append(next(p + str(oo) for oo in range(1, 7) if M.midi(p + str(oo)) > M.midi(ns[-1])))
        fr = [M.midi(n) - OPEN[s] for n, s in zip(ns, (4, 3, 2, 1))]
        if not all(0 <= f <= 15 for f in fr): continue
        fz = [f for f in fr if f > 0]
        if max(fz) - min(fz) > (4 if min(fz) >= 7 else 3): continue
        out.append((ns, [-1, -1] + fr))
    return out


def marcatto_fill(dom, ton, order, near, land_grip):
    """pp. 32–33: the pianists' marcatto in octaves, on the guitar moved through the dominant's inversions with the D string
    lowest: four short chords in one of his four orders, then a slide into the tonic's bass."""
    from itertools import product
    kinds = sorted(set(ORD[order]))
    opts = {k: inversions(dom, k) for k in kinds}
    best = None
    for pick in product(*[range(len(opts[k])) for k in kinds]):
        ch = {k: opts[k][i] for k, i in zip(kinds, pick)}
        seq = [ch[k] for k in ORD[order]]
        c, last = 0.0, near
        for ns, g in seq:
            p = gpos(g); c += abs(p - last); last = p
            c += sum(1.0 for f in g if f == 0)
        c += abs(gpos(land_grip) - last)
        if best is None or c < best[0]: best = (c, seq)
    chords = [ns for ns, g in best[1]]; grips = [g for ns, g in best[1]]
    f = Fill([(1, ns, 's') for ns in chords], [[(s, g[6 - s]) for s in (4, 3, 2, 1)] for g in grips], 'marcatto', dict(dom=dom, ton=ton, order=order))
    f.grips = grips
    its = []
    names = {'7': '/' + M.pc_name(M.tr(root(dom) + '4', 6, 10)), '1': '', '3': '/' + M.pc_name(M.tr(root(dom) + '4', 2, 4))}
    for j, (k, g) in enumerate(zip(ORD[order], grips)):
        nm = dom + names[k]
        if j < 3: its.append(K(nm, g, st(1, 'A')))
        else: its += [K(nm, g, [(0.5, 'A')]), arr(land_grip, ton)]
    f.k_items = its
    return f


# ================================================================ the contexts: where each fill goes in the songs
CTX = {
    'ochi-V-i': dict(song='ochi', key='A', mode='minor', dom='E7', ton='Am', where='E7 into A minor (bars 2–3)'),
    'ochi-i-V': dict(song='ochi', key='A', mode='minor', dom='E7', ton='Am', where='A minor into E7 (bars 4–5)'),
    'iw-V-i': dict(song='iw', key='F', mode='minor', dom='C7', ton='Fm', where='C7 into F minor (bars 8–9, where the voice holds “how”)'),
    'iw-i-V': dict(song='iw', key='F', mode='minor', dom='C7', ton='Fm', where='F minor into C7 (bars 9–10)'),
    'iw-V-I': dict(song='iw', key='Eb', mode='major', dom='Bb7', ton='Eb', where='B♭7 into E♭ (bars 16–17)'),
    'iw-I-V': dict(song='iw', key='Eb', mode='major', dom='Bb7', ton='Eb', where='E♭ into B♭7 (bars 31–32, where the voice holds “now”)'),
    'iw-V/V': dict(song='iw', key='Bb', mode='major', dom='F7', ton='Bb7', where='F7 into B♭7 (bars 14–15, where the voice holds “sighs”)'),
    'yvl-V-I': dict(song='yvl', key='G', mode='major', dom='D7', ton='G', where='D7 into G'),
    'yvl-I-V': dict(song='yvl', key='G', mode='major', dom='D7', ton='G', where='G into D7'),
}


def grips(c): return GR[CTX[c]['song']]


def star(c, ch):
    g = grips(c)
    return g.get(ch + '*', g[ch])


def label(ch): return 'over ' + dn(ch)


# ================================================================ quotes: his opening beat or two only
GQ = dict(G7=[3, -1, 3, 4, 3, -1], G7_7=[-1, -1, 3, 4, 3, 3], G7_1=[-1, -1, 5, 7, 6, 7])


def qrun(notes, ss, durs, rest=0.0, flags=None):
    pos = [[(s, M.midi(n) - OPEN[s])] for n, s in zip(notes, ss)]
    ev = ([(rest, [], '')] if rest else []) + [(d, [n], (flags[i] if flags else '')) for i, (n, d) in enumerate(zip(notes, durs))]
    return Fill(ev, pos, 'quote', {}).items('his notes')


def qpairs(pairs, ss, durs, rest=0.5):
    pos = [[(s, M.midi(n) - OPEN[s]) for n, s in zip(p, sp)] for p, sp in zip(pairs, ss)]
    ev = [(rest, [], '')] + [(d, p, '') for p, d in zip(pairs, durs)]
    return Fill(ev, pos, 'quote', {}).items('his notes')


def Q(page, text, items): return dict(where=where(page), text=text, items=items, whose=OWN, played='')


# ================================================================ the exercises
def two_bars(c, fill_items, land_items, ch1, ch2, note1, note2=''):
    return [bar([ch1], fill_items, note1), bar([ch2], land_items, note2)]


def sd_bars(exid, c):
    C = CTX[c]; g = grips(c)
    f = scale_down(C['dom'], C['ton'], C['mode'], gpos(g[C['dom']])).log(exid, land=bass_pitch(star(c, C['ton']))[0])
    ns = f.notes(); flat_ns = [n[0] for n in ns]
    its = [K(C['dom'], g[C['dom']], [(1, 'A'), (1, 'A')])] + f.items(label(C['dom']))
    return two_bars(c, its, [K(C['ton'], star(c, C['ton']), LAND)], C['dom'], C['ton'],
                    f'{SONG[C["song"]]}, {C["where"]}: ' + ', '.join(nd(n) for n in flat_ns) + '. ' + say_run(flat_ns, [p[0] for p in f.pos]) + '.',
                    f'{dn(C["ton"])} as his landing chord: the bass, then the 5th, root and 3rd above it.')


def su_bars(exid, c):
    C = CTX[c]; g = grips(c)
    f = scale_up(C['ton'], C['dom'], C['mode'], gpos(g[C['ton']])).log(exid, land=bass_pitch(g[C['dom']])[0])
    flat_ns = [n[0] for n in f.notes()]
    its = [K(C['ton'], g[C['ton']], [(1, 'A'), (1, 'A')])] + f.items(label(C['ton']))
    return two_bars(c, its, [K(C['dom'], g[C['dom']], FOUR)], C['ton'], C['dom'],
                    f'{SONG[C["song"]]}, {C["where"]}: ' + ', '.join(nd(n) for n in flat_ns) + '. ' + say_run(flat_ns, [p[0] for p in f.pos]) + '.',
                    f'{dn(C["dom"])}, four strokes.')


def pt_bars(exid, c):
    C = CTX[c]; g = grips(c)
    f = pattern(C['ton'], C['dom'], C['mode'], gpos(g[C['ton']])).log(exid, land=bass_pitch(g[C['dom']])[0])
    flat_ns = [n[0] for n in f.notes()]
    its = [K(C['ton'], g[C['ton']], [(1, 'A'), (1, 'A')])] + f.items(label(C['ton']))
    return two_bars(c, its, [K(C['dom'], g[C['dom']], SINC_L)], C['ton'], C['dom'],
                    f'{SONG[C["song"]]}, {C["where"]}: ' + ', '.join(nd(n) for n in flat_ns[:4]) + ', then ' + ', '.join(nd(n) for n in flat_ns[4:]) + '. '
                    + say_run(flat_ns, [p[0] for p in f.pos]) + '.',
                    f'{dn(C["dom"])} in his landing rhythm: eighth, quarter, eighth, quarter, rest.')


SECT_NOTE = {}
ex('escalar', 'escalar-desc-menor', 'Down the scale into the tonic (minor)',
   ('Over the dominant, after two strokes: a sixteenth rest and seven sixteenths. Start on the dominant’s root (the key’s 5th), jump up a 3rd to the key’s 7th '
    '(in minor the natural minor’s 7th, not the leading note), then go straight down the key’s scale to its 2nd; the tonic falls on the next downbeat. '
    'Graciano: this is one of the bass phrases of chapter 2, two octaves up.'),
   Q(27, 'Relleno escalar descendente, en tonalidad menor: on G7, two strokes, then his line from G down into C minor. Played here: its first beat.',
     qrun(['G4', 'Bb4', 'Ab4'], [1, 1, 1], [0.25] * 3, rest=0.25)),
   sd_bars('escalar-desc-menor', 'ochi-V-i') + sd_bars('escalar-desc-menor', 'iw-V-i'))
ex('escalar', 'escalar-desc-mayor', 'Down the scale into the tonic (major)',
   'The same in a major key: from the dominant’s root up a 3rd to the key’s 7th, then down the major scale to the 2nd, onto the tonic.',
   Q(27, 'En tonalidad mayor: on G7, two strokes, then the same line in C major. Played here: its first beat.', qrun(['G4', 'B4', 'A4'], [1, 1, 1], [0.25] * 3, rest=0.25)),
   sd_bars('escalar-desc-mayor', 'iw-V-I') + sd_bars('escalar-desc-mayor', 'yvl-V-I'))
ex('escalar', 'escalar-asc-menor', 'Up the scale into the dominant (minor)',
   ('From the tonic to the dominant: a sixteenth rest and seven sixteenths climbing from the key’s 5th to the 4th above it, the 6th and 7th raised '
    '(the melodic minor going up), so the dominant’s root falls on the next downbeat. Graciano leaves the first half of the bar empty; here it holds two strokes of the chord.'),
   Q(27, 'Ascendente, en tonalidad menor: from G up into G7. Played here: the sixteenth rest and his first three notes.', qrun(['G3', 'A3', 'B3'], [4, 4, 4], [0.25] * 3, rest=0.25)),
   su_bars('escalar-asc-menor', 'ochi-i-V') + su_bars('escalar-asc-menor', 'iw-i-V'))
ex('escalar', 'escalar-asc-mayor', 'Up the scale into the dominant (major)',
   'The same in a major key: up the major scale from the 5th to the 4th above, into the dominant.',
   Q(28, 'En tonalidad mayor: from G up into G7. Played here: the sixteenth rest and his first three notes.', qrun(['G3', 'A3', 'B3'], [4, 4, 4], [0.25] * 3, rest=0.25)),
   su_bars('escalar-asc-mayor', 'iw-I-V') + su_bars('escalar-asc-mayor', 'yvl-I-V'))

ex('patron', 'patron-menor', 'A pattern into the dominant (minor)',
   ('Graciano’s pattern fill: four sixteenths to a group, a note, the step below it, the note again, the step above; the next group starts a step above that. '
    'Two groups from the key’s root lead into the dominant (in minor the step below the root is the leading note). He advises working through a book of such patterns.'),
   Q(28, 'Relleno en patrón, en tonalidad menor: two groups from C into G7, then G7 in his landing rhythm. Played here: his first group.', qrun(['C4', 'B3', 'C4', 'D4'], [3, 3, 3, 3], [0.25] * 4)),
   pt_bars('patron-menor', 'ochi-i-V') + pt_bars('patron-menor', 'iw-i-V'))
ex('patron', 'patron-mayor', 'A pattern into the dominant (major)',
   'The same pattern in a major key.',
   Q(28, 'En tonalidad mayor: the same two groups in C major. Played here: his first group.', qrun(['C4', 'B3', 'C4', 'D4'], [3, 3, 3, 3], [0.25] * 4)),
   pt_bars('patron-mayor', 'iw-I-V') + pt_bars('patron-mayor', 'yvl-I-V'))


# ---------------------------------------------------------------- campanitas
def camp_bars(exid, c, way):
    C = CTX[c]; g = grips(c)
    f = campanitas(C['dom'], way).log(exid)
    gd = near_grip(C['song'], C['dom'], f.pos[1][0][1])
    its = [K(C['dom'], gd, [(0.375, 'A')])] + f.items(label(C['dom']))
    its += [K(C['dom'], near_grip(C['song'], C['dom'], f.pos[-1][0][1]), [(1, 'A')])] if way == 1 else [['W', 1]]
    land = [K(C['ton'], g[C['ton']], SINC_L)]
    txt = ', '.join(f'{nd(n)} on the {STR[p[0][0]]} ({ordn(p[0][1])})' for n, p in [(n, p) for (d, ns, fl), p in zip(f.ev, f.pos) for n in ns if fl != 'g'][:4 if way == 1 else 3])
    first = f'{SONG[C["song"]]}, {C["where"]}: ' if way == 1 or c != 'ochi-V-i' else ''
    slides = [(p[0][0], p[0][1], q[0][1]) for (d, ns, fl), p, q in zip(f.ev, f.pos, f.pos[1:]) if fl == 'g']
    sl = '; '.join(f'the slide on the {STR[s_]} from the {ordn(a)} fret to the {ordn(b_)}' for s_, a, b_ in slides)
    return two_bars(c, its, land, C['dom'], C['ton'], first + dn(C['dom']) + f'’s root in octaves: {txt}; {sl}.',
                    f'{dn(C["ton"])} in his slashes’ rhythm: eighth, quarter, eighth, quarter, rest.')


ex('campanitas', 'campanitas-1', 'Campanitas',
   ('“Little bells”, from Carlos Di Sarli’s piano, taken to the guitar by Ubaldo De Lío. Over the dominant, its root alone in octaves, climbing the neck: '
    'the root, the octave above it short, the same note again on the next string down (slid into), then the octave above that, short, ringing like a bell. '
    'His strings skip one up, come back one, and skip one up again. Then the chord, and the tonic, minor or major.'),
   Q(28, 'Campanitas en 8vas: on G7, a stroke, then G four times up the neck on the D, B, G and top strings, a stroke; then C minor or C. Played here: his first two beats.',
     [K('G7', GQ['G7'], [(0.375, 'A')])] + qrun(['F3', 'G3', 'G4', 'F4', 'G4'], [4, 4, 2, 3, 3], [0.125, 0.5, 0.375, 0.125, 0.5], flags=['g', '', 's', 'g', ''])),
   camp_bars('campanitas-1', 'ochi-V-i', 1) + camp_bars('campanitas-1', 'iw-V-i', 1) + camp_bars('campanitas-1', 'iw-V/V', 1))
ex('campanitas', 'campanitas-2', 'Campanitas between two strings',
   'The second way: the octave rocking between the G string and the top string, the last three a sixteenth, a sixteenth and an eighth.',
   Q(28, 'The second example: a stroke, G slid into on the G string, its octave on the top string, short, and back; then three more between the two strings. Played here: his first two beats.',
     [K('G7', GQ['G7'], [(0.375, 'A')])] + qrun(['F4', 'G4', 'G5', 'G4'], [3, 3, 1, 3], [0.125, 0.5, 0.5, 0.5], flags=['g', '', 's', ''])),
   camp_bars('campanitas-2', 'ochi-V-i', 2) + camp_bars('campanitas-2', 'iw-V-I', 2))


# ---------------------------------------------------------------- tenths
def ten_bars(exid, c_song, chord, phrased, strings, where_txt, lead=True):
    g = GR[c_song]
    f = tenths(chord, phrased, strings).log(exid)
    pairs = f.notes()
    out = []
    if lead: out.append(bar([chord], [K(chord, g[chord], SINC_L)], f'{SONG[c_song]}, {where_txt}: a bar of the chord, then its tenths.'))
    out.append(bar([chord], f.items(label(chord)),
                   '; '.join(f'{nd(a)} with {nd(b)}' for a, b in pairs) + f': the {STR[strings[0]]} at the ' + ', '.join(ordn(p[0][1]) for p in f.pos)
                   + f' fret, the {STR[strings[1]]} at the ' + ', '.join(ordn(p[1][1]) for p in f.pos) + '.'))
    return out


ex('decimas', 'decimas-mayor', 'Tenths over a major chord',
   ('From Francisco De Caro’s left hand at the piano, in his brother Julio’s sextet in the mid-1920s: a note and its tenth, moving together. '
    'Over a major chord, from its root and 3rd: the lower voice climbs a tone and two semitones to the 3rd, the upper a semitone and two semitones to the 5th. '
    'An eighth rest, three eighths, the last pair held. Graciano: on the A and B strings, or the low E and G strings, or the D and top strings.'),
   Q(29, 'Rellenos en décimas, sin fraseo, sobre acorde mayor: on C, from C with E to E with G, on the A and B strings. Played here: his first beat and a half.',
     qpairs([['C3', 'E4'], ['D3', 'F4']], [[5, 2], [5, 2]], [0.5, 0.5])),
   ten_bars('decimas-mayor', 'iw', 'Eb', False, (5, 2), 'its E♭ (bars 3–4, where the voice holds “now”)')
   + ten_bars('decimas-mayor', 'yvl', 'G', False, (6, 3), 'its G'))
ex('decimas', 'decimas-dominante-fraseada', 'Tenths over a dominant, phrased',
   'Phrased: the first pair a quarter, the two between it and the last quick sixteenths. Graciano: the same goes on a dominant chord.',
   Q(29, 'Fraseada, sobre acorde mayor: C with E as a quarter, then the two sixteenths, E with G held. Played here: the eighth rest and the first pair.',
     qpairs([['C3', 'E4']], [[5, 2]], [1])),
   ten_bars('decimas-dominante-fraseada', 'ochi', 'E7', True, (5, 2), 'its E7')
   + ten_bars('decimas-dominante-fraseada', 'iw', 'C7', True, (6, 3), 'its C7 (bar 8)'))
ex('decimas', 'decimas-menor', 'Tenths over a minor chord',
   'Over a minor chord, from its root and minor 3rd: the lower voice climbs by semitones to the 3rd, the upper a tone and two semitones to the 5th.',
   Q(29, 'Sin fraseo, sobre acorde menor: on C minor, from C with E♭ to E♭ with G. Played here: his first beat and a half.',
     qpairs([['C3', 'Eb4'], ['Db3', 'F4']], [[5, 2], [5, 2]], [0.5, 0.5])),
   ten_bars('decimas-menor', 'ochi', 'Dm', False, (5, 2), 'its D minor')
   + ten_bars('decimas-menor', 'ochi', 'Am', False, (6, 3), 'its A minor')
   + ten_bars('decimas-menor', 'iw', 'Fm', False, (4, 1), 'its F minor (bar 9)'))
ex('decimas', 'decimas-menor-fraseada', 'Tenths over a minor chord, phrased',
   'The minor tenths in the phrased rhythm.',
   Q(29, 'Fraseada, sobre acorde menor: C with E♭ as a quarter, the two sixteenths, E♭ with G held. Played here: the eighth rest and the first pair.',
     qpairs([['C3', 'Eb4']], [[5, 2]], [1])),
   ten_bars('decimas-menor-fraseada', 'ochi', 'Am', True, (4, 1), 'its A minor')
   + ten_bars('decimas-menor-fraseada', 'iw', 'Fm', True, (5, 2), 'its F minor'))


# ---------------------------------------------------------------- octaves
def oct_bars(exid, c, way):
    C = CTX[c]; g = grips(c)
    src, dst = (C['ton'], C['dom']) if way == 'td' else (C['dom'], C['ton'])
    land = g[dst]
    best = None
    for pair in ((4, 2), (3, 1), (5, 3), (6, 4)):
        try: f = octaves(way, C['ton'], C['dom'], C['mode'], land, pair)
        except AssertionError: continue
        h = sum(p[0][1] for p in f.pos[:-1]) / (len(f.pos) - 1)
        c_ = abs(h - gpos(land))
        if best is None or c_ < best[0]: best = (c_, f)
    f = best[1].log(exid, land=bass_pitch(land)[0])
    line = [ns[0] for d, ns, fl in f.ev if ns and fl != 'x'][::2]
    xs, xf = f.pos[-1][0]
    return two_bars(c, f.items(label(src)), [K(dst, land, TWO)], src, dst,
                    f'{SONG[C["song"]]}, {C["where"]}: ' + ', '.join(nd(n) for n in line) + f' in octaves on the {STR[f.ctx["pair"][0]]} and {STR[f.ctx["pair"][1]]} ('
                    + ', '.join(f'{ordn(a[0][1])} and {ordn(b[0][1])}' for a, b in zip(f.pos[:-1:2], f.pos[1:-1:2])) + f'), the x on the {STR[xs]} ({ordn(xf)}).',
                    f'{dn(dst)}, a stroke on 1 and on 3; its bass is where the x was' + (', a fret higher.' if way == 'dt' else '.'))


OCT_IDEA = ('Broken octaves in eighths, the lower note first, three steps of the key’s scale; on the last eighth an x, the bass string struck dead '
            'where the next chord’s bass is, so the hand is already there. The next bar: a stroke on 1 and on 3.')
ex('octavas', 'octavas-tonica-dominante-menor', 'Octaves from the tonic to the dominant (minor)',
   OCT_IDEA + ' From the tonic down: the root, the 7th and the 6th of the natural minor, the x on the dominant’s root.',
   Q(30, 'Rellenos en 8vas., en tonalidad menor, de tónica a dominante: from C down into G7. Played here: the eighth rest and his first octave.', qrun(['C4', 'C5'], [3, 1], [0.5, 0.5], rest=0.5)),
   oct_bars('octavas-tonica-dominante-menor', 'ochi-i-V', 'td') + oct_bars('octavas-tonica-dominante-menor', 'iw-i-V', 'td'))
ex('octavas', 'octavas-dominante-tonica-menor', 'Octaves from the dominant to the tonic (minor)',
   OCT_IDEA + ' From the dominant up: its root, then the key’s 6th and 7th raised; the x on that 7th, a fret under the tonic’s bass.',
   Q(30, 'De dominante a tónica, en menor: from G up into C minor. Played here: the eighth rest and his first octave.', qrun(['G3', 'G4'], [4, 2], [0.5, 0.5], rest=0.5)),
   oct_bars('octavas-dominante-tonica-menor', 'ochi-V-i', 'dt') + oct_bars('octavas-dominante-tonica-menor', 'iw-V-i', 'dt'))
ex('octavas', 'octavas-tonica-dominante-mayor', 'Octaves from the tonic to the dominant (major)',
   OCT_IDEA + ' In a major key, from the tonic down the scale: root, 7th, 6th, the x on the dominant’s root.',
   Q(30, 'En tonalidad mayor, de tónica a dominante: from C down into G7. Played here: the eighth rest and his first octave.', qrun(['C4', 'C5'], [3, 1], [0.5, 0.5], rest=0.5)),
   oct_bars('octavas-tonica-dominante-mayor', 'iw-I-V', 'td') + oct_bars('octavas-tonica-dominante-mayor', 'yvl-I-V', 'td'))
ex('octavas', 'octavas-dominante-tonica-mayor', 'Octaves from the dominant to the tonic (major)',
   OCT_IDEA + ' In a major key, from the dominant up: 5th, 6th, 7th, the x on the 7th.',
   Q(30, 'En tonalidad mayor, de dominante a tónica: from G up into C. Played here: the eighth rest and his first octave.', qrun(['G3', 'G4'], [4, 2], [0.5, 0.5], rest=0.5)),
   oct_bars('octavas-dominante-tonica-mayor', 'iw-V-I', 'dt') + oct_bars('octavas-dominante-tonica-mayor', 'yvl-V-I', 'dt'))


# ---------------------------------------------------------------- sixths and thirds
def dy_bars(exid, song, chord, target, interval, where_txt):
    g = GR[song]
    f = dyad_slide(chord, target, interval, gpos(g[chord])).log(exid)
    ps = f.notes()
    sl, sh = f.pos[0][0][0], f.pos[0][1][0]
    return [bar([chord], f.items(label(chord)),
                f'{SONG[song]}, {where_txt}: ' + ', then '.join(f'{nd(a)} with {nd(b)}' for a, b in ps) + f', on the {STR[sl]} and {STR[sh]} ('
                + ', '.join(f'{ordn(p[0][1])} and {ordn(p[1][1])}' for p in f.pos) + f'). {nd(ps[-1][1])} on top, the {target}.'),
            bar([chord], [K(chord, g[chord], FOUR)], 'The chord, four strokes.')]


SIX = [  # target, kind, his first pair (quote), his strings, page, his words
    ('root', 'dom', ['A3', 'F4'], [4, 2], 30, 'buscando la fundamental: on G7, three sixths sliding up onto B with G'),
    ('3rd', 'dom', ['C4', 'A4'], [3, 1], 31, 'buscando la tercera: on G7, onto D with B'),
    ('5th', 'dom', ['Eb3', 'C4'], [4, 2], 31, 'buscando la quinta: on G7, onto F with D'),
    ('root', 'min', ['Db4', 'Bb4'], [3, 1], 31, 'buscando la fundamental: on C minor, onto E♭ with C'),
    ('3rd', 'min', ['F3', 'C#4'], [4, 2], 31, 'buscando la tercera: on C minor, onto G with E♭'),
    ('5th', 'min', ['Ab3', 'F4'], [4, 2], 31, 'buscando la quinta: on C minor, onto B♭ with G'),
]
THI = [
    ('3rd', 'dom', ['F3', 'A3'], [4, 3], 31, 'buscando la tercera, on G7: three thirds sliding up onto G with B'),
    ('5th', 'dom', ['A3', 'C4'], [3, 2], 32, 'buscando la quinta: on G7, onto B with D'),
    ('7th', 'dom', ['C4', 'Eb4'], [3, 2], 32, 'buscando la séptima (solo en acorde de dominante): on G7, onto D with F'),
    ('3rd', 'min', ['A#3', 'C#4'], [3, 2], 32, 'buscando la tercera: on C minor, onto C with E♭'),
    ('5th', 'min', ['Db4', 'F4'], [3, 2], 32, 'buscando la quinta: on C minor, onto E♭ with G'),
]
WHERE_DY = {('ochi', 'E7'): 'its E7', ('ochi', 'Am'): 'its A minor', ('iw', 'C7'): 'its C7 (bar 8, the voice holding)', ('iw', 'F7'): 'its F7 (bars 12 and 14, the voice holding)',
            ('iw', 'Fm'): 'its F minor (bar 9)', ('iw', 'Eb'): 'its E♭ (bars 19–20, the voice holding “wine”)', ('yvl', 'G'): 'its G', ('yvl', 'D7'): 'its D7'}
SIX_IDEA = ('Inside one chord: a sixth slides up by semitones onto two of the chord’s notes, the target on top. Eighth rest, a quarter, an eighth, the target a quarter, a rest; '
            'then the chord goes on. The two lower sixths are the same size as the target’s. Graciano: ideal inside one chord, a chromatic sixth into each of its notes.')
THI_IDEA = 'The same with thirds. Graciano: good to swap, one chord with a fill in thirds, the next with one in sixths.'
for sec, rows, idea0, word, interval in (('sextas', SIX, SIX_IDEA, 'Rellenos en 6tas.', 'sixth'), ('terceras', THI, THI_IDEA, 'Rellenos en 3eras.', 'third')):
    for i, (tgt, kind, qp, qs, page, his) in enumerate(rows):
        ctxs = [('ochi', 'E7'), ('iw', 'F7')] if kind == 'dom' else [('ochi', 'Am'), ('iw', 'Fm')]
        if kind == 'dom' and tgt == 'root': ctxs = [('ochi', 'E7'), ('iw', 'C7')]
        if kind == 'dom' and tgt in ('3rd', 'root') and interval == 'sixth': ctxs.append(('iw', 'Eb'))       # “para acorde dominante o mayor”
        id_ = f'{sec}-{"dominante" if kind == "dom" else "menor"}-{tgt}'
        title = f'{"Sixths" if interval == "sixth" else "Thirds"} into the {tgt} ({"dominant" if kind == "dom" else "minor"})'
        idea = idea0 if i == 0 else f'The same over a {"dominant (or major)" if kind == "dom" else "minor"} chord, aiming at its {tgt}.'
        kind_txt = 'para acorde dominante o mayor' if kind == 'dom' else 'para acorde menor'
        bars_ = []
        for song, ch in ctxs: bars_ += dy_bars(id_, song, ch, tgt, interval, WHERE_DY[(song, ch)])
        ex(sec, id_, title, idea,
           Q(page, f'{word + " " if i == 0 else ""}{kind_txt}, {his}; then a bar of the chord. Played here: the eighth rest and his first {interval}.',
             qpairs([qp], [qs], [1])), bars_)


# ---------------------------------------------------------------- the marcatto as a fill
def marc_bars(exid, c, order):
    C = CTX[c]; g = grips(c)
    f = marcatto_fill(C['dom'], C['ton'], order, 7, g[C['ton']]).log(exid, land=bass_pitch(g[C['ton']])[0])
    ws = {'7': 'its 7th', '1': 'its root', '3': 'its 3rd'}
    txt = ', '.join(f'{ws[k]} ({nd(ns[0])}) in the bass' for k, ns in zip(ORD[order], f.notes()))
    return two_bars(c, f.k_items, [K(C['ton'], g[C['ton']], SINC_L)], C['dom'], C['ton'],
                    f'{SONG[C["song"]]}, {C["where"]}: {dn(C["dom"])} on the top four strings, {txt}; the slide goes up the {STR[bass_pitch(g[C["ton"]])[1]]} into {dn(C["ton"])}’s bass.',
                    f'{dn(C["ton"])} in his landing rhythm.')


for o in (1, 2, 3, 4):
    ws = {'7': 'F', '1': 'G', '3': 'B'}
    ex('marcatto', f'marcatto-relleno-{o}', f'The marcatto in inversions, order {o}',
       ('The pianists’ marcatto jumps by octaves; on the guitar that does little, so Graciano keeps the idea and moves through the dominant’s inversions instead, '
        'the D string always lowest: its 7th, its root or its 3rd in the bass. Four short chords, then a slide into the tonic’s first beat.') if o == 1 else
       'The same chords in another of his orders.',
       Q(32 if o < 3 else 33, f'Rellenos del marcatto 4, orden {o}: on G7, the D string lowest, ' + ', '.join(ws[k] for k in ORD[o]) + ' in the bass; the slide into C minor or C. Played here: his first two chords.',
         [K({'7': 'G7/F', '1': 'G7', '3': 'G7/B'}[k], GQ['G7_' + k] if k != '3' else [-1, -1, 9, 10, 8, 10], st(1, 'A')) for k in ORD[o][:2]]),
       marc_bars(f'marcatto-relleno-{o}', 'iw-V-I' if o % 2 else 'ochi-V-i', o))


# ================================================================ études
CH_OCHI = ['E7', 'E7', 'Am', 'Am', 'E7', 'E7', 'Am', 'Am', 'Dm', 'Dm', 'Am', 'Am', 'E7', 'E7', 'Am', 'Am']


def etude_ochi():
    from entry import marcatto4, sincopado
    G = GR['ochi']; b = []
    E7, Am, Dm = G['E7'], G['Am'], G['Dm']
    b.append(bar(['E7'], [marcatto4('E7', E7)], 'Очи чёрные’s sixteen bars, a fill in the second bar of each chord: the scale down (bar 2), the pattern (4), octaves up (6), '
                 'sixths into the root (8), tenths over D minor (10), octaves down (12), campanitas (14). The other bars keep the rhythms of chapter 1.'))
    f = scale_down('E7', 'Am', 'minor', gpos(E7)).log('etude-ochi', land=bass_pitch(G['Am*'])[0])
    b.append(bar(['E7'], [K('E7', E7, [(1, 'A'), (1, 'A')])] + f.items(label('E7')), 'Down the scale into A minor.'))
    b.append(bar(['Am'], [K('Am', G['Am*'], LAND)]))
    f = pattern('Am', 'E7', 'minor', gpos(Am)).log('etude-ochi', land=bass_pitch(E7)[0])
    b.append(bar(['Am'], [K('Am', Am, [(1, 'A'), (1, 'A')])] + f.items(label('Am')), 'The pattern into E7.'))
    b.append(bar(['E7'], [K('E7', E7, SINC_L)]))
    f = octaves('dt', 'Am', 'E7', 'minor', Am, (4, 2)).log('etude-ochi', land=bass_pitch(Am)[0])
    b.append(bar(['E7'], f.items(label('E7')), 'Octaves up into A minor.'))
    b.append(bar(['Am'], [K('Am', Am, TWO)]))
    f = dyad_slide('Am', 'root', 'sixth', gpos(Am)).log('etude-ochi')
    b.append(bar(['Am'], f.items(label('Am')), 'Sixths into A minor’s root.'))
    b.append(bar(['Dm'], [sincopado('Dm', Dm)]))
    f = tenths('Dm', False, (5, 2)).log('etude-ochi')
    b.append(bar(['Dm'], f.items(label('Dm')), 'Tenths over D minor.'))
    b.append(bar(['Am'], [sincopado('Am', Am)]))
    f = octaves('td', 'Am', 'E7', 'minor', G['E7o'], (4, 2)).log('etude-ochi', land=bass_pitch(G['E7o'])[0])
    b.append(bar(['Am'], f.items(label('Am')), 'Octaves down into E7.'))
    b.append(bar(['E7'], [K('E7', G['E7o'], TWO)], 'E7 over the open low E, where the x left the hand.'))
    f = campanitas('E7', 1).log('etude-ochi')
    b.append(bar(['E7'], [K('E7', G['E7o'], [(0.375, 'A')])] + f.items(label('E7')) + [K('E7', E7, [(1, 'A')])], 'Campanitas into A minor.'))
    b.append(bar(['Am'], [sincopado('Am', Am)]))
    b.append(bar(['Am'], [K('Am', Am, [(0.5, 'A', ACC), (3.5, '-')])], 'One short chord, accented.'))
    return b


# I Wonder Who's Kissing Her Now: the chorus, first ending, in 3/4; the vals of Graciano's ch. 20 under the voice, fills where it holds
IWB = {b: (chs, notes, w) for b, chs, notes, w in TU.in_eb(ending=1)}


def vals(c, g, beats=3):
    s = [6 - i for i in range(6) if g[i] >= 0]
    return K(c, g, [(1, [s[0]]), (0.5, s[1:4]), (0.5, '-'), (0.5, s[1:4]), (0.5, '-')][:5 if beats == 3 else 1])


def words(b):
    w = IWB[b][2]
    return f'“{w}”' if w else ''


def etude_iw():
    G = GR['iw']; out = []
    held = {3: 'now', 7: 'how', 12: 'eyes', 14: 'sighs', 19: 'wine', 23: 'mine', 31: 'now'}
    out.append(bar(['Bb7'], [K('Bb7', G['Bb7'], [(1, 'A')])],
                   'The chorus of I Wonder Who’s Kissing Her Now as the 1909 song has it, a waltz, in E♭, with the first ending. Under the voice the vals of Graciano’s chapter 20 '
                   '(bass, chord, chord); where the voice holds a note or rests, a fill from this page, whole, fitted into the bar: tenths under “now”, the scale down under “how”, '
                   'sixths under “eyes” and “wine”, thirds under “sighs”, campanitas under “mine”, the scale up under the last “now”. This bar is the pickup: the voice sings “I”.'))
    b = 1
    while b <= 32:
        chs, notes, w = IWB[b]
        c = chs[0][0]
        g = G[c] if c in G else None
        note = ''
        if b == 3:      # tenths over E♭ from beat 2 of bar 3, the last pair held into bar 4
            f = tenths('Eb', False, (5, 2)).log('etude-iw')
            its = f.items(label('Eb'))
            p_it = its[1]
            n3 = ','.join(p_it[3].split('|')[0][1:].split(',')[:3])
            out.append(bar(['Eb'], [K('Eb', g, [(1, [5])]), ['W', 0.5], ['P', p_it[1][:3], [0.5] * 3, '=' + n3 + '|over E♭']],
                           'The voice holds “now”: tenths over E♭ from the second beat, E♭ with G, F with A♭, F♯ with A ...'))
            last = ','.join(p_it[3].split('|')[0][1:].split(',')[3:])
            out.append(bar(['Eb'], [['P', p_it[1][3:], [2], '=' + last + '|over E♭'], K('Eb', g, [(0.5, [4, 3, 2]), (0.5, '-')])],
                           '... and G with B♭, held, the voice still on “now”; then the chord.'))
            b = 5; continue
        if b == 8:
            f = scale_down('C7', 'Fm', 'minor', gpos(g)).log('etude-iw', land=bass_pitch(G['Fm'])[0])
            out.append(bar(['C7'], [K('C7', g, [(1, [6])])] + f.items(label('C7')), 'The voice holds “how” and rests: the scale down into F minor.'))
            b += 1; continue
        if b == 9:
            out.append(bar(['Fm'], [K('Fm', G['Fm'], LAND[:4])], 'F minor as the fill’s landing, his bass and chord twice.'))
            b += 1; continue
        if b in (12, 14, 19):
            ch = c
            tgt, iv = {12: ('3rd', 'sixth'), 14: ('7th', 'third'), 19: ('3rd', 'sixth')}[b]
            f = dyad_slide(ch, tgt, iv, gpos(g)).log('etude-iw')
            its = f.items(label(ch))
            assert its[0][0] == 'W' and its[-1][0] == 'W'
            gb = near_grip('iw', ch, f.pos[0][0][1])
            s_b = [6 - i for i in range(6) if gb[i] >= 0][0]
            out.append(bar([ch], [K(ch, gb, [(0.5, [s_b])])] + its[1:-1],
                           f'The voice holds “{held[b]}”: the bass, then {iv}s into {dn(ch)}’s {tgt}.'))
            b += 1; continue
        if b == 24:
            f = campanitas('C7', 1).log('etude-iw')
            out.append(bar(['C7'], [K('C7', near_grip('iw', 'C7', f.pos[1][0][1]), [(0.375, 'A')])] + f.items(label('C7')), 'The voice holds “mine” and rests: campanitas on C7, into F minor.'))
            b += 1; continue
        if b == 26:
            out.append(bar(['Fm', 'F'], [K('Fm', G['Fm'], [(1, [5]), (1, [4, 3, 2])]), K('F', G['F'], [(1, [4, 3, 2])])], 'F minor, then F on the third beat.'))
            b += 1; continue
        if b == 27:
            out.append(bar(['Eb/Bb'], [vals('Eb/Bb', G['Eb/Bb'])])); b += 1; continue
        if b == 31:
            f = scale_up('Eb', 'Bb7', 'major', gpos(g)).log('etude-iw', land=bass_pitch(G['Bb7'])[0])
            out.append(bar(['Eb'], [K('Eb', g, [(1, [5])])] + f.items(label('Eb')), 'The voice holds “now”: the scale up into B♭7.'))
            b += 1; continue
        if b == 32:
            out.append(bar(['Bb7'], [K('Bb7', g, [(1, [6]), (0.5, [4, 3, 2]), (0.5, '-'), (0.5, [4, 3, 2]), (0.5, '-')])], 'B♭7; the voice sings “I”, back to the top.'))
            b += 1; continue
        out.append(bar([c], [vals(c, g)], ''))
        b += 1
    for j, B in enumerate(out):                  # the words sung in each bar, so the place is never lost
        w = IWB[j][2]
        if w and j > 0 and not B['note'].startswith('The voice holds'): B['note'] = (f'Sung: “{w.rstrip(",.;")}”. ' + B['note']).strip()
    out.append(bar(['Eb'], [K('Eb', G['Eb'], [(0.5, 'A', ACC), (2.5, '-')])], 'Or end here, on E♭.'))
    return out


ETUDES = [dict(id='etude-ochi-rellenos', title='Очи чёрные with fills', idea='', quote=dict(where='', text='', item=None), bars=etude_ochi()),
          dict(id='etude-iw-rellenos', title='I Wonder Who’s Kissing Her Now with fills', idea='', quote=dict(where='', text='', item=None), bars=etude_iw())]

SECTIONS = [dict(id='escalar', title='Scale fills', part='Exercises', ex=EXS['escalar']),
            dict(id='patron', title='Pattern fills', part='Exercises', ex=EXS['patron']),
            dict(id='campanitas', title='Campanitas', part='Exercises', ex=EXS['campanitas']),
            dict(id='decimas', title='Tenths', part='Exercises', ex=EXS['decimas']),
            dict(id='octavas', title='Octaves', part='Exercises', ex=EXS['octavas']),
            dict(id='sextas', title='Sixths', part='Exercises', ex=EXS['sextas']),
            dict(id='terceras', title='Thirds', part='Exercises', ex=EXS['terceras']),
            dict(id='marcatto', title='The marcatto as a fill', part='Exercises', ex=EXS['marcatto']),
            dict(id='etudes', title='Études', part='Études', ex=ETUDES)]

from quotes import trim as _trim_quotes   # quotes stay a beat or two
_trim_quotes(SECTIONS)
