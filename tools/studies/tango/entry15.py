"""Tango harmony, rebuilt by rule: Graciano, Método de guitarra tango, ch. 5 ("Giros armónicos"), pp. 41–49 of the owner's
copy: reharmonizing with the key's own chords, the circle of 5ths, tritone substitutes, diminished chords for the
dominant, the line cliché (from the octave and from the 5th) and the tritone with its resolutions.

Nothing of Graciano's is kept beyond the opening beat or two of each example (the quotes). Every progression of ours
is made by a function that applies his rule to a key and a place in the owner's songs: Очи чёрные (A minor; its own
arrangement already has the line cliché in bars 42–43 and F7–E7 in bar 51), I Wonder Who's Kissing Her Now (E♭ and its
F minor), Я вас любил (G and its E minor, whose pre-chorus walks E minor, E minor (maj7), E minor 7, E minor 6).
Chords are voiced by entry14's search (the bass line the rule's, the upper voices moving least); each function logs
what it made (LOG) and check15.py checks it against the rule with its own code.
"""
import sys
sys.path.insert(0, '/home/claude/studies'); sys.path.insert(0, '/home/claude/studies/tango')
import mel as M
from entry import K, st, ACC
from kit_study import place_lines
import entry14 as C14

OPEN = M.OPEN
sym, pname, dn, nd, ordn, STR, gpos, width = C14.sym, C14.pname, C14.dn, C14.nd, C14.ordn, C14.STR, C14.gpos, C14.width
spell, tone_name, voice_chords, grips_all, gnotes, up, nn = C14.spell, C14.tone_name, C14.voice_chords, C14.grips_all, C14.gnotes, C14.up, C14.nn
OCHI, IW, YVL = C14.OCHI, C14.IW, C14.YVL
OWN = 'Graciano’s own'
LOG = []
EXS = {}


def where(p): return f'Método de guitarra tango, p. {p}'
def ex(sec, id, title, idea, quote, bars): EXS.setdefault(sec, []).append(dict(id=id, title=title, idea=idea, quote=quote, bars=bars))
def bar(chords, items, note=''): return dict(chords=chords, items=items, note=note)
def Q(page, text, items): return dict(where=where(page), text=text, items=items, whose=OWN, played='')
def T(page, text): return dict(where=where(page), text=text, item=None, by='Graciano')


def deg(key, steps, semis):
    n = M.pc_name(up(key + '4', steps, semis))
    return C14.ENH.get(n, n)


C14.QUAL.update({'m7b5': [0, 3, 6, 10], '6': [0, 4, 7, 9], 'm6': [0, 3, 7, 9], 'm7': [0, 3, 7, 10], 'm(maj7)': [0, 3, 7, 11], 'm#5': [0, 3, 8]})
QWORD = {'': '', 'm': ' minor', '7': '7', 'dim7': '°7', 'maj7': 'maj7', 'm7b5': 'm7♭5', '6': '6', 'm6': 'm6', 'm7': 'm7', 'm(maj7)': 'm(maj7)', 'm#5': 'm♯5'}


def split_name(name):
    base, _, bass = name.partition('/')
    r = base[:2] if len(base) > 1 and base[1] in 'b#' else base[:1]
    return r, base[len(r):], bass


def pn(name):
    """a chord's name in prose"""
    r, q, b = split_name(sym(name))
    return M.dname(r) + QWORD[q] + ('/' + M.dname(b) if b else '')


pname = pn


def bass_near(pcx, prev, span=7):
    return min((m for m in range(prev - span, prev + span + 1) if m % 12 == pcx), key=lambda m: (abs(m - prev), m))


NEED = {'': [0, 4, 7], 'm': [0, 3, 7], '7': [4, 10], 'maj7': [4, 11], 'dim7': [], 'm7b5': [3, 6, 10], '6': [4, 9], 'm6': [3, 9],
        'm7': [3, 10], 'm(maj7)': [3, 11], 'm#5': [3, 8]}


def chord_spec(name, bass_m):
    """(pitch classes, bass, the notes the upper voices must keep): a 7th or 6th chord its 3rd and 7th (6th), a triad all
    of it, a diminished 7th any three; never the note the bass already gives"""
    r, q, b = split_name(sym(name))
    rp = M.midi(r + '4') % 12
    pcs = [(rp + x) % 12 for x in C14.QUAL[q]]
    need = [(rp + x) % 12 for x in NEED[q] if (rp + x) % 12 != bass_m % 12]
    return (pcs, bass_m, need)


def voiced(names, basses, near, first_grip=None, bass_strings=(6, 5)):
    opn = any(b in (40, 45, 50) for b in basses)            # an open bass string in the line: open strings allowed
    return voice_chords([chord_spec(n, b) for n, b in zip(names, basses)], near, first_grip=first_grip, bass_strings=bass_strings, allow_open=opn)


IVS = {0: (0, 0), 1: (1, 1), 2: (1, 2), 3: (2, 3), 4: (2, 4), 5: (3, 5), 6: (3, 6), 7: (4, 7), 8: (5, 8), 9: (5, 9), 10: (6, 10), 11: (6, 11)}


def tn(m, name):
    """a note named from the chord's root: its own interval (the 9th of E7 is F♯), C♭ and F♭ written B and E"""
    r, q, b = split_name(sym(name))
    if b and M.midi(b + '4') % 12 == m % 12: return M.dname(b)
    rp = M.midi(r + '4') % 12
    n = M.pc_name(C14.tr_safe(r + '4', *IVS[(m - rp) % 12]))
    if (m - rp) % 12 == 9 and q in ('dim7',): n = M.pc_name(C14.tr_safe(r + '4', 6, 9))
    return M.dname(C14.ENH.get(n, n))


def say_chords(names, vs):
    out = []
    for k, (n, (ms, g)) in enumerate(zip(names, vs)):
        if k and n == names[k - 1]: continue
        out.append(f'{pname(n)}: ' + ', '.join(tn(m, n) for m in ms))
    return '; '.join(out)


def strokes(names, vs, durs, how=None):
    its = []
    for k, (n, (ms, g), d) in enumerate(zip(names, vs, durs)):
        h = how[k] if how else [(d, 'A')]
        its.append(K(sym(n), g, h))
    return its


# ================================================================ the key's own chords (pp. 41–42)
def im_ivm(key, near):
    """p. 41: where a minor tonic goes to the minor chord on its 4th degree, climb to it by step through the natural minor's
    chords: Im, IIm7♭5, ♭III, then the 4th's dominant over its 3rd, and IVm; the bass climbs 1, 2, ♭3, 3, 4."""
    names = [key + 'm', deg(key, 1, 2) + 'm7b5', deg(key, 2, 3), deg(key, 0, 0) + '/' + deg(key, 2, 4), deg(key, 3, 5) + 'm']
    names[3] = deg(key, 0, 0) + '7/' + deg(key, 2, 4)
    k = M.midi(key + '4') % 12
    b0 = next(m for m in range(40, 52) if m % 12 == k)
    basses = [b0, b0 + 2, b0 + 3, b0 + 4, b0 + 5]
    vs = voiced(names, basses, near)
    LOG.append(dict(device='im-ivm', ctx=dict(key=key), names=names, chords=vs))
    return names, vs


def im_v(key, near):
    """p. 42: a still minor tonic set moving by a falling bass: Im, Im over its minor 7th, the diminished 7th on the 6th
    (a passing chord, standing for the dominant with ♭9), then ♭VI7, which cadences on V7; the bass 1, ♭7, 6, ♭6, 5."""
    names = [key + 'm', key + 'm/' + deg(key, 6, 10), deg(key, 5, 9) + 'dim7', deg(key, 5, 8) + '7', deg(key, 4, 7) + '7']
    k = M.midi(key + '4') % 12
    b0 = next(m for m in range(45, 57) if m % 12 == k)
    basses = [b0, b0 - 2, b0 - 3, b0 - 4, b0 - 5]
    vs = voiced(names, basses, near)
    LOG.append(dict(device='im-v', ctx=dict(key=key), names=names, chords=vs))
    return names, vs


def grela(key, near, top_string=1):
    """p. 42, Roberto Grela's way, from the Andalusian cadence: the tonic's root alone, then Im, ♭VII6, ♭VImaj7, V7, with the
    key's 5th held on top all the way (a pedal in the soprano)."""
    k = M.midi(key + '4') % 12
    five = next(m for m in range(59, 72) if m % 12 == (k + 7) % 12)
    names = [key + 'm', deg(key, 6, 10) + '6', deg(key, 5, 8) + 'maj7', deg(key, 4, 7) + '7']
    out = []
    for n in names:
        pcs = C14.pcs_of(n)
        best = None
        for g in C14_grips_with_top(pcs, five, near):
            c = abs(gpos(g) - (gpos(out[-1][1]) if out else near))
            if best is None or c < best[0]: best = (c, g)
        assert best, n
        out.append((sorted(gnotes(best[1])), best[1]))
    LOG.append(dict(device='grela', ctx=dict(key=key, top=five), names=names, chords=out))
    return names, out, five


def C14_grips_with_top(pcs, top, near, n=4):
    """grips of four or five notes of the chord (all its notes there), its highest note `top`, the bass on a low string"""
    from itertools import combinations, product
    found = []
    others = [p for p in pcs]
    for k in (3, 4):
        for lows in combinations(range(top - 22, top), k):
            if {m % 12 for m in lows} | {top % 12} != set(pcs): continue
            if len({m for m in lows}) != k: continue
            ms = sorted(lows) + [top]
            for g in grips_all(ms, allow_open=True, maxf=12, bass_strings=(6, 5, 4)):
                found.append(g)
    return found


# ================================================================ the circle of 5ths (pp. 42–43)
def circle(key, near):
    """pp. 42–43: in a minor key, run the circle of 5ths from the minor IV at twice the speed, the chords of the key:
    IVm, ♭VII7, ♭IIImaj7, ♭VImaj7, IIm7♭5, V7, Im. Each chord a 5th below the last, two to a bar."""
    names = [deg(key, 3, 5) + 'm', deg(key, 6, 10) + '7', deg(key, 2, 3) + 'maj7', deg(key, 5, 8) + 'maj7', deg(key, 1, 2) + 'm7b5', deg(key, 4, 7) + '7', key + 'm']
    roots = [C14.chord_pcs(n)[1] for n in names]
    basses = []
    for r in roots:
        if not basses: basses.append(next(m for m in range(43, 55) if m % 12 == r)); continue
        basses.append(min((m for m in range(40, 56) if m % 12 == r), key=lambda m: abs(m - basses[-1])))
    vs = voiced(names, basses, near)
    LOG.append(dict(device='circle', ctx=dict(key=key), names=names, chords=vs))
    return names, vs


# ================================================================ tritone substitutes (pp. 43–44)
def tritone_sub(dom, near, first_grip=None):
    """p. 43: a dominant (primary or secondary, minor or major key) can be replaced by the dominant 7th an augmented 4th
    away: the two share their 3rd and 7th, swapped. Here the second way: the dominant two beats, the substitute two,
    the shared notes held where they are, the bass moving a tritone."""
    r = C14.chord_pcs(dom)[1]
    sub = deg(dom[:-1], 4, 6) + '7'                         # a diminished 5th up: B♭7 for E7
    b0 = next(m for m in range(40, 52) if m % 12 == r)
    if first_grip: v1 = (sorted(gnotes(first_grip)), first_grip)
    else: v1 = voiced([dom], [b0], near)[0]
    shared = [m for m in v1[0][1:] if m % 12 in ((r + 4) % 12, (r + 10) % 12)]
    sr = (r + 6) % 12
    best = None
    for sb in range(40, 56):
        if sb % 12 != sr or sb >= min(shared): continue
        for extra in [None] + [m for m in range(sb + 3, max(shared) + 8) if m % 12 in ((sr + 7) % 12, (sr + 2) % 12) and m not in shared]:
            ms = sorted([sb] + shared + ([extra] if extra else []))
            for g in grips_all(ms, allow_open=True, maxf=12, bass_strings=(6, 5)):
                keep = all(any(g[6 - s_] == f for s_, f in [(s0, v1[1][6 - s0]) for s0 in range(1, 7) if v1[1][6 - s0] >= 0 and OPEN[s0] + v1[1][6 - s0] == m]) for m in shared)
                c = abs(gpos(g) - gpos(v1[1])) + (0 if keep else 3) + (0 if extra else 1)
                if best is None or c < best[0]: best = (c, (ms, g))
    assert best, dom
    vs = [v1, best[1]]
    LOG.append(dict(device='tritone-sub', ctx=dict(dom=dom, sub=sub), names=[dom, sub], chords=vs))
    return sub, vs


def sub_9_11(dom, near):
    """p. 44: the substitute coloured with its 9th and its ♯11: root, 3rd, 7th, 9th, ♯11."""
    sub = deg(dom[:-1], 4, 6)
    r = M.midi(sub + '4') % 12
    want = {r, (r + 4) % 12, (r + 10) % 12, (r + 2) % 12, (r + 6) % 12}
    best = None
    for b in range(40, 52):
        if b % 12 != r: continue
        from itertools import combinations
        for ups in combinations(range(b + 3, b + 24), 4):
            if {m % 12 for m in ups} | {r} != want: continue
            for g in grips_all([b] + list(ups), allow_open=False, maxf=12, bass_strings=(6, 5)):
                c = abs(gpos(g) - near)
                if best is None or c < best[0]: best = (c, [b] + list(ups), g)
    assert best, dom
    LOG.append(dict(device='sub-9-11', ctx=dict(dom=dom, sub=sub + '7'), chords=[(best[1], best[2])]))
    return sub + '7', best[1], best[2]


# ================================================================ diminished chords for the dominant (p. 44)
def dim_for_v(dom, near, first_grip=None):
    """p. 44: the dominant (primary or secondary) replaced by the diminished 7th on its 3rd: the dominant with ♭9, its
    root left out."""
    r = C14.chord_pcs(dom)[1]
    d3 = deg(dom[:-1], 2, 4) + 'dim7'
    b0 = next(m for m in range(40, 52) if m % 12 == r)
    vs = voiced([dom, d3], [b0, bass_near((r + 4) % 12, b0)], near, first_grip=first_grip)
    LOG.append(dict(device='dim-for-v', ctx=dict(dom=dom, dim=d3), names=[dom, d3], chords=vs))
    return d3, vs


def dim_shapes(dname):
    """p. 44, the diminished grips most used in tango: the root on the 6th string (all six), on the 5th, on the 4th"""
    r = C14.chord_pcs(dname)[1]
    out = []
    for s, shape in ((6, [0, 1, 2, 0, 2, 0]), (5, [-1, 0, 1, -1, 1, -1]), (4, [-1, -1, 0, 1, 0, 1])):
        f = next(f for f in range(2, 14) if (OPEN[s] + f) % 12 == r)
        if s == 5: g = [-1, f, f + 1, f - 1, f + 1, -1]                # root on the A string: R, ♭5, ♭♭7 (6), ♭3
        else: g = [x + f if x >= 0 else -1 for x in shape]
        out.append((s, g))
    LOG.append(dict(device='dim-shapes', ctx=dict(dim=dname), grips=[g for s, g in out]))
    return out


def dim_marcatto(dom, tgrip):
    """p. 44: in place of the dominant, a marcatto 4 with four different diminished 7ths: the one on its 3rd and the same
    chord a minor 3rd apart, here the shape with its root on the D string sliding down three frets at a time; Graciano:
    mind how the last resolves, above all the top voice. The start is chosen so the last top note steps (a semitone or a
    tone) into the top note of the chord that follows."""
    r = C14.chord_pcs(dom)[1]
    d = (r + 4) % 12
    shape = [-1, -1, 0, 1, 0, 1]                        # root on the D string: R, ♭5, ♭♭7, ♭3
    top_t = max(gnotes(tgrip))
    best = None
    for f0 in range(3, 16):
        if (OPEN[4] + f0 - d) % 3 != 0: continue                 # any of the four: the same chord
        frets = [f0 - 3 * k for k in range(4)]
        if min(frets) < 0 or max(frets) > 13: continue
        grips = [[x + f if x >= 0 else -1 for x in shape] for f in frets]
        last_top = max(gnotes(grips[-1]))
        step = top_t - last_top
        if abs(step) in (1, 2):
            c = abs(frets[-1] - gpos(tgrip))
            if best is None or c < best[0]: best = (c, grips)
    assert best, dom
    LOG.append(dict(device='dim-marcatto', ctx=dict(dom=dom), grips=best[1], tgrip=tgrip))
    return best[1]


# ================================================================ the line cliché (pp. 44–47)
def cliche_voicings(key, frm, where_line, near):
    """pp. 44–46: on a minor chord that stays one or two bars, one voice moves while the others hold. From the octave the
    root falls by semitones (root, major 7th, minor 7th, 6th); from the 5th it climbs a semitone and back (5, ♯5, 6, ♯5).
    The moving voice can be in the bass, on top or inside; the other two notes of the chord hold."""
    k = M.midi(key + '4') % 12
    third, fifth = (k + 3) % 12, (k + 7) % 12
    if frm == 8: line_pcs = [k, (k + 11) % 12, (k + 10) % 12, (k + 9) % 12]; holds = [third, fifth]
    else: line_pcs = [fifth, (k + 8) % 12, (k + 9) % 12, (k + 8) % 12]; holds = [k, third]
    best = None
    from itertools import product
    def try_one(line, hold, bass_extra):
        nonlocal best
        gs = []

        for m in line:
            ms = sorted(bass_extra + list(hold) + [m])
            cand = grips_all(ms, allow_open=True, maxf=12, bass_strings=(6, 5, 4))
            if not cand: break
            gs.append(cand)
        else:
            # the held notes keep their strings: pick one grip per step with the holds on the same strings, the line on one string
            for g0 in gs[0]:
                seq = [g0]
                for i, cands in enumerate(gs[1:]):
                    prev = seq[-1]
                    ls = held_strings(prev, [line[i]])[0]                      # the moving voice stays on its string
                    same = [g for g in cands if all(g[6 - s] == prev[6 - s] for s in held_strings(prev, hold + bass_extra))
                            and held_strings(g, [line[i + 1]]) == [ls]]
                    if not same: break
                    seq.append(min(same, key=lambda g: abs(gpos(g) - gpos(prev))))
                else:
                    c = abs(gpos(g0) - near) + 0.5 * sum(1 for g in seq for f in g if f == 0)
                    if best is None or c < best[0]: best = (c, line, hold, bass_extra, seq)

    for lo in range(40, 70):
        if lo % 12 != line_pcs[0]: continue
        line = [lo]
        for p in line_pcs[1:]: line.append(min((m for m in range(line[-1] - 3, line[-1] + 3) if m % 12 == p), key=lambda m: abs(m - line[-1])))
        for hold in product(*[[m for m in range(40, 78) if m % 12 == h] for h in holds]):
            hold = sorted(hold)
            ok = True
            if where_line == 'bass': ok = all(x > max(line) for x in hold) and hold[-1] - line[0] <= 16
            elif where_line == 'top': ok = all(x < min(line) for x in hold) and line[0] - hold[0] <= 16
            else: ok = hold[0] < min(line) and hold[1] > max(line)
            if not ok: continue
            bass_opts = [[]] if where_line == 'bass' else [[rb] for rb in range(40, min(hold + line)) if rb % 12 == k]   # the tonic below, as his
            for bass_extra in bass_opts:
                try_one(line, hold, bass_extra)
    assert best, (key, frm, where_line)
    c, line, hold, bass_extra, seq = best
    names = [key + 'm', key + 'm(maj7)', key + 'm7', key + 'm6'] if frm == 8 else [key + 'm', key + 'm#5', key + 'm6', key + 'm#5']
    LOG.append(dict(device='cliche', ctx=dict(key=key, frm=frm, where=where_line), line=line, hold=list(hold), bass=bass_extra, grips=seq, names=names))
    return names, line, hold, bass_extra, seq


def held_strings(g, notes):
    out = []
    for i in range(6):
        if g[i] >= 0 and OPEN[6 - i] + g[i] in notes: out.append(6 - i)
    return out


# ================================================================ the tritone (pp. 47–49)
def tritone_pair(dom, octave_low):
    """the dominant's tritone, its 3rd below its 7th"""
    r = C14.chord_pcs(dom)[1]
    third = next(m for m in range(octave_low, octave_low + 12) if m % 12 == (r + 4) % 12)
    return [third, third + 6]


def resolve(pair, tonic_pcs):
    """p. 48: a tritone resolving into the tonic chord: its two notes move in contrary motion, each by a semitone (or a
    tone where no chord note is a semitone away), onto notes of the chord"""
    lo, hi = pair
    best = None
    for dl in (-2, -1, 1, 2):
        for dh in (-2, -1, 1, 2):
            if dl * dh > 0: continue
            a, b = lo + dl, hi + dh
            if a % 12 in tonic_pcs and b % 12 in tonic_pcs and a < b:
                c = abs(dl) + abs(dh)
                if best is None or c < best[0]: best = (c, [a, b])
    return best[1] if best else None


def four_tritones(dom, octave_low=55):
    """p. 47–48: the tritone, and the ones a minor 3rd, two and three minor 3rds above it (each a dominant's heart)"""
    t = tritone_pair(dom, octave_low)
    return [[t[0] + 3 * k, t[1] + 3 * k] for k in range(4)]


def on_strings(pairs, ss, near=6, alt=None):
    """two-note shapes on a pair of strings; alt: {index: other strings} where a shape needs them"""
    out = []
    for i, p in enumerate(pairs):
        sl, sh = (alt or {}).get(i, ss)
        fr = [p[0] - OPEN[sl], p[1] - OPEN[sh]]
        if min(fr) < 0 or max(fr) > 15: return None
        out.append([(sl, fr[0]), (sh, fr[1])])
    return out


# ================================================================ the exercises
def grip_txt(g):
    fz = [f for f in g if f > 0]
    if not fz or (0 in g and max(fz) <= 4): return 'in open position'
    return f'at the {ordn(min(fz))} fret'


def prog_bars(song, where_txt, names, vs, first_beats, land_note):
    """the first four chords a beat each, the last two beats and a rest"""
    its = [K(sym(n), g, [(1, 'A')]) for n, (ms, g) in zip(names[:first_beats], vs[:first_beats])]
    last = [K(sym(names[first_beats]), vs[first_beats][1], [(2, 'A'), (2, '-')])]
    return [bar([sym(n) for n in names[:first_beats]], its, f'{song}, {where_txt}: ' + say_chords(names[:first_beats], vs[:first_beats]) + '.'),
            bar([sym(names[first_beats])], last, land_note + ' ' + say_chords(names[first_beats:first_beats + 1], vs[first_beats:first_beats + 1]) + '.')]


def gq(notes, near=3):
    return C14.grip_of([M.midi(n) for n in notes], near=near, allow_open=True)


# ---------------- the key's own chords
names, vs = im_ivm('A', 5); LOG[-1]['ex'] = 'im-ivm'
b1 = prog_bars(OCHI, 'from A minor to D minor, as its verses go (bars 13–15 of your arrangement)', names, vs, 4, 'Into D minor.')
names, vs = im_ivm('E', 3); LOG[-1]['ex'] = 'im-ivm'
b2 = prog_bars(YVL, 'its pre-chorus, from E minor to A minor (bars 25–27)', names, vs, 4, 'Into A minor.')
ex('diatonica', 'im-ivm', 'From the minor tonic to its 4th degree',
   ('Where a minor tonic goes to the minor chord on its 4th degree (with or without the 4th’s own dominant between), climb to it by step through the natural minor’s chords: '
    'I, II (half-diminished), ♭III, then the 4th’s dominant over its 3rd, and the minor IV. The bass climbs 1, 2, ♭3, 3, 4.'),
   Q(41, 'Conexión del Im al IVm, in C minor: C minor, D half-diminished, E♭, C over E, into F minor. Played here: his first two chords.',
     [K('Cm', gq(['C3', 'G3', 'C4', 'Eb4']), [(1, 'A')]), K('Dm7b5', gq(['D3', 'Ab3', 'C4', 'F4']), [(1, 'A')])]), b1 + b2)

names, vs = im_v('A', 3); LOG[-1]['ex'] = 'im-v'
b1 = prog_bars(OCHI, 'A minor before E7 (your arrangement has A minor over G in bar 13 and F7–E7 in bar 51)', names, vs, 4, 'Into E7.')
names, vs = im_v('F', 7); LOG[-1]['ex'] = 'im-v'
b2 = prog_bars(IW, 'its F minor before C7 (bars 9–10)', names, vs, 4, 'Into C7.')
ex('diatonica', 'im-v', 'From the minor tonic to the dominant',
   ('A still minor tonic set moving by a falling bass: the tonic, the tonic over its minor 7th, a passing diminished 7th on the 6th (standing for the dominant with ♭9), '
    'then the ♭VI7 that leads to the dominant. The bass falls 1, ♭7, 6, ♭6, 5.'),
   Q(42, 'Conexión del Im al V7: C minor, C minor over B♭, A°7, A♭7, into G7. Played here: his first two chords.',
     [K('Cm', gq(['C3', 'G3', 'C4', 'Eb4']), [(1, 'A')]), K('Cm/Bb', gq(['Bb2', 'G3', 'Bb3', 'Eb4']), [(1, 'A')])]), b1 + b2)


def grela_bars(song, where_txt, key, near):
    names, out, five = grela(key, near)
    LOG[-1]['ex'] = 'grela'
    k = M.midi(key + '4') % 12
    bnote = min(m for m in out[0][0])
    bs = [s_ for s_ in (6, 5, 4) if 0 <= bnote - OPEN[s_] <= 12][0]
    first = [['R', [[bs, bnote - OPEN[bs]]], [1], f'={nd(spell(bnote, key, "minor"))}|the bass']]
    first += [K(sym(n), g, [(1, 'A')]) for n, (ms, g) in zip(names[:3], out[:3])]
    return [bar([sym(n) for n in names[:3]], first,
                f'{song}, {where_txt}: the bass alone, then ' + '; '.join(f'{pn(n)} (' + ', '.join(tone_name(m, n) for m in ms) + ')' for n, (ms, g) in zip(names[:3], out[:3]))
                + f', {nd(spell(five, key, "minor"))} on top all the way.'),
            bar([sym(names[3])], [K(sym(names[3]), out[3][1], [(2, 'A'), (2, '-')])], f'{pn(names[3])} (' + ', '.join(tone_name(m, names[3]) for m in out[3][0]) + '), the same note on top.')]


ex('diatonica', 'grela', 'Roberto Grela’s way: a pedal on top',
   ('The same idea as Roberto Grela played it, a relative of the Andalusian cadence: the tonic, the ♭VII6, the ♭VImaj7, the dominant, '
    'with the dominant’s root (the key’s 5th) held on top all the way.'),
   Q(42, 'Grela: C in the bass, then C minor, B♭6, A♭maj7, into G7, G on top throughout. Played here: the bass and his first chord.',
     [['R', [[5, 3]], [1], '=C|his notes'], K('Cm', gq(['G3', 'C4', 'Eb4', 'G4']), [(1, 'A')])]),
   grela_bars(OCHI, 'in A minor', 'A', 5) + grela_bars(IW, 'in its F minor', 'F', 8))


def circle_bars(song, where_txt, key, near, plan):
    names, vs = circle(key, near)
    LOG[-1]['ex'] = 'circle'
    out = []
    for i in range(0, 6, 2):
        out.append(bar([sym(names[i]), sym(names[i + 1])], [K(sym(names[i]), vs[i][1], [(1, 'A'), (1, 'A')]), K(sym(names[i + 1]), vs[i + 1][1], [(1, 'A'), (1, 'A')])],
                       (f'{song}, {where_txt}: over {plan}, the circle at twice the speed. ' if i == 0 else '') + say_chords(names[i:i + 2], vs[i:i + 2]) + '.'))
    out.append(bar([sym(names[6])], [K(sym(names[6]), vs[6][1], [(2, 'A'), (2, '-')])], say_chords(names[6:], vs[6:]) + '.'))
    return out


ex('diatonica', 'circulo-1', 'The circle of 5ths',
   ('Where the harmony goes IVm, Im, V7, Im (a bar each), run the circle of 5ths from the minor IV at twice the speed, through the chords of the key: '
    'IVm, ♭VII7, ♭IIImaj7, ♭VImaj7, IIm7♭5, V7, Im. The functions still fall where they did: a tonic chord on the strong beat for Im, and the dominant a little later, after its own II.'),
   Q(42, 'In C minor, over F minor, C minor, G7, C minor: F minor, B♭7; E♭maj7, A♭maj7; D half-diminished, G7; C minor. He gives the names; the grips are ours. Played here: the first bar.',
     [K('Fm', [1, 3, 3, 1, 1, 1], [(1, 'A')]), K('Bb7', [6, 8, 6, 7, 6, 6], [(1, 'A')])]),
   circle_bars(OCHI, 'its second half', 'A', 5, 'D minor, A minor, E7, A minor'))
ex('diatonica', 'circulo-2', 'The circle in place of V, I, V, I',
   ('The second case: where the harmony goes V7, Im, V7, Im, the same circle takes it to the relative major (the ♭III falls where Im was, '
    'with its own II and V before it), and the second half of the phrase turns back to the minor.'),
   T(43, 'Over G7, C minor, G7, C minor: F minor, B♭7; E♭maj7, A♭maj7; D half-diminished, G7; C minor. Chord names only.'),
   circle_bars(YVL, 'in E minor, the key of its pre-chorus', 'E', 4, 'B7, E minor, B7, E minor'))


# ---------------- tritone substitutes
def sub_bars(song, where_txt, dom, tonic, tgrip, near, first_grip=None):
    sub, vs = tritone_sub(dom, near, first_grip)
    LOG[-1]['ex'] = 'sustituto-tritonal'
    (m1, g1), (m2, g2) = vs
    common = sorted({m for m in m1[1:]} & {m for m in m2[1:]})
    keep = (' The ' + ' and '.join(tone_name(m, dom) for m in common) + ' stay where they are: the dominant’s 3rd and 7th are the substitute’s 7th and 3rd.') if common else ''
    sr = C14.chord_pcs(sub)[1]
    ksub = sym(sub)[:-1] + '9' if any(m % 12 == (sr + 2) % 12 for m in m2) else sym(sub)      # its 9th in the shape: so named
    return [bar([sym(dom), ksub], [K(sym(dom), g1, [(2, 'A')]), K(ksub, g2, [(2, 'A')])],
                f'{song}, {where_txt}: {pn(dom)} two beats, then its substitute {pn(sub)}. ' + say_chords([dom, sub], vs) + '.' + keep),
            bar([sym(tonic)], [K(sym(tonic), tgrip, [(2, 'A'), (2, '-')])], f'Into {pn(tonic)}: the substitute’s root falls a semitone to the tonic.')]


ex('tritonal', 'sustituto-tritonal', 'The tritone substitute',
   ('A dominant, primary or secondary, in minor or major, can be replaced by the dominant 7th an augmented 4th away: the two share their 3rd and 7th, swapped. '
    'Either in its place (the original left out), or after it, two beats each, the substitute second, so the tension rises before it rests.'),
   Q(43, 'G7, then its substitute D♭7. Played here: the G7.', [K('G7', [3, 5, 3, 4, 3, -1], [(2, 'A')])]),
   sub_bars(OCHI, 'E7 into A minor', 'E7', 'Am', C14.GR['ochi']['Am'], 5)
   + sub_bars(IW, 'C7 into F minor (bars 8–9)', 'C7', 'Fm', C14.GR['iw']['Fm'], 8, first_grip=C14.GR['iw']['C7'])
   + sub_bars(IW, 'B♭7 into E♭ (bars 16–17)', 'Bb7', 'Eb', C14.GR['iw']['Eb'], 6, first_grip=C14.GR['iw']['Bb7']))


def sub911_bars(song, where_txt, dom, tonic, tgrip, near):
    sub, ms, g = sub_9_11(dom, near)
    LOG[-1]['ex'] = 'sustituto-9-11'
    rn = sym(sub)[:-1]; r = M.midi(rn + '4') % 12
    wd = {0: 'root', 4: '3rd', 10: '7th', 2: '9th', 6: '♯11th'}
    sp = {0: (0, 0), 4: (2, 4), 10: (6, 10), 2: (1, 2), 6: (3, 6)}
    nm = lambda m: M.disp(C14.ENH.get(M.pc_name(C14.tr_safe(rn + '4', *sp[(m - r) % 12])), M.pc_name(C14.tr_safe(rn + '4', *sp[(m - r) % 12]))) + '4')
    return [bar([sym(sub)[:-1] + '7#11'], [K(sym(sub)[:-1] + '7#11', g, [(2, 'A')]), K(sym(tonic), tgrip, [(2, 'A')])],
                f'{song}, {where_txt}: in place of {pn(dom)}, {pn(sub)} with its 9th and ♯11th: ' + ', '.join(f'{nm(m)} ({wd[(m - r) % 12]})' for m in ms)
                + f', {grip_txt(g)}; then {pn(tonic)}.')]


ex('tritonal', 'sustituto-9-11', 'The substitute with its 9th and ♯11',
   'Graciano: it is very common to colour the substitute with its 9th and its ♯11.',
   Q(44, 'D♭7(9,♯11): D♭, F, B, E♭, G. Played here: that chord.', [K('Db7', gq(['Db3', 'F3', 'B3', 'Eb4', 'G4'], near=4), [(2, 'A')])]),
   sub911_bars(OCHI, 'E7 into A minor', 'E7', 'Am', C14.GR['ochi']['Am'], 6) + sub911_bars(IW, 'C7 into F minor', 'C7', 'Fm', C14.GR['iw']['Fm'], 3))


# ---------------- diminished chords for the dominant
def dimv_bars(song, where_txt, dom, tonic, tgrip, near, first_grip=None):
    d3, vs = dim_for_v(dom, near, first_grip)
    LOG[-1]['ex'] = 'disminuido-por-dominante'
    return [bar([sym(dom), sym(d3)], [K(sym(dom), vs[0][1], [(2, 'A')]), K(sym(d3), vs[1][1], [(2, 'A')])],
                f'{song}, {where_txt}: {pn(dom)}, then the diminished 7th on its 3rd, {pn(d3)}. ' + say_chords([dom, d3], vs) + '.'),
            bar([sym(tonic)], [K(sym(tonic), tgrip, [(2, 'A'), (2, '-')])], f'Into {pn(tonic)}.')]


ex('disminuidos', 'disminuido-por-dominante', 'A diminished chord for the dominant',
   ('A tango sound from the very start: the dominant, primary or secondary, replaced by the diminished 7th on its 3rd (the dominant with ♭9, its root left out). '
    'Being symmetrical, the same chord comes back every minor 3rd along the neck.'),
   Q(44, 'G7, then B°7. Played here: both, a beat each.', [K('G7', gq(['G2', 'D3', 'F3', 'B3', 'D4']), [(1, 'A')]), K('Bdim7', gq(['B2', 'F3', 'Ab3', 'D4']), [(1, 'A')])]),
   dimv_bars(OCHI, 'E7 into A minor', 'E7', 'Am', C14.GR['ochi']['Am'], 5)
   + dimv_bars(IW, 'B♭7 into E♭ (bars 16–17)', 'Bb7', 'Eb', C14.GR['iw']['Eb'], 6, first_grip=C14.GR['iw']['Bb7']))


def shapes_bar(song, dname):
    sh = dim_shapes(dname)
    LOG[-1]['ex'] = 'disminuido-graficos'
    return bar([sym(dname)] * 3, [K(sym(dname), g, [(1, 'A')]) for s_, g in sh] + [['W', 1]],
               f'{song}’s {pn(dname)} three ways: ' + '; '.join(f'the root on the {STR[s_]} ({grip_txt(g)})' for s_, g in sh) + '.')


ex('disminuidos', 'disminuido-graficos', 'The three diminished grips',
   'The diminished shapes most used in tango: the root on the 6th string (all six strings), on the 5th, and on the 4th.',
   T(44, 'Tónica en 6ta., en 5ta., en 4ta.: three grip diagrams.'),
   [shapes_bar(OCHI, 'G#dim7'), shapes_bar(IW, 'Ddim7')])


def dmarc_bars(song, where_txt, dom, tonic, tgrip):
    gs = dim_marcatto(dom, tgrip)
    LOG[-1]['ex'] = 'disminuido-marcatto'
    d = sym(deg(dom[:-1], 2, 4) + 'dim7')
    tops = [max(gnotes(g)) for g in gs] + [max(gnotes(tgrip))]
    names = []
    for g in gs:
        root = OPEN[4] + g[2]
        names.append(sym(M.pc_name(spell(root, 'C', 'major')) + 'dim7'))
    return [bar(names, [K(n, g, st(1, 'A', ACC if i % 2 == 0 else 0)) for i, (n, g) in enumerate(zip(names, gs))],
                f'{song}, {where_txt}: in place of {pn(dom)}, ' + ', '.join(pn(n) for n in names) + ' on the top four strings, the shape three frets lower each time (' +
                ', '.join(ordn(g[2]) for g in gs if g[2]) + ' fret' + (', then open strings' if gs[-1][2] == 0 else '') + '). The top voice: ' + ', '.join(nd(spell(t, 'C', 'major')) for t in tops[:-1]) + f', then {nd(spell(tops[-1], "C", "major"))} in {pn(tonic)}.'),
            bar([sym(tonic)], [K(sym(tonic), tgrip, [(2, 'A'), (2, '-')])], f'{pn(tonic)}, {grip_txt(tgrip)}.')]


ex('disminuidos', 'disminuido-marcatto', 'Marcatto 4 on four diminished chords',
   ('In place of the dominant, a marcatto 4 with four different diminished chords (the same chord a minor 3rd apart); '
    'Graciano: mind how the last one resolves, above all the top voice.'),
   T(44, 'Al reemplazar al dominante, podemos realizar un marcatto 4 con cuatro acordes disminuidos diferentes: the idea in words.'),
   dmarc_bars(OCHI, 'E7 into A minor', 'E7', 'Am', [-1, 0, 2, 2, 1, 0]) + dmarc_bars(IW, 'B♭7 into E♭', 'Bb7', 'Eb', C14.GR['iw']['Eb']))


# ---------------- the line cliché
CL_CTX = {'A': (OCHI, 'its A minor, where your arrangement already has it (bars 42–43: A minor, A minor (maj7), A minor 7, A minor 6)'),
          'E': (YVL, 'its pre-chorus in E minor, where the song itself walks E minor, E minor (maj7), E minor 7, E minor 6 (bars 25–26)'),
          'F': (IW, 'its F minor (bar 9)')}
WH = {'bass': 'in the bass', 'top': 'on top', 'inner': 'in an inner voice'}
CL_SHORT = {'A': (OCHI, 'its A minor'), 'E': (YVL, 'its E minor'), 'F': (IW, 'its F minor')}
_said = set()


def ctx_txt(key):
    """the long place the first time a song comes up in this part, the short one after"""
    if key in _said: return CL_SHORT[key]
    _said.add(key); return CL_CTX[key]


def cliche_bars(key, frm, wl, near=5, how='hold'):
    names, line, hold, bass_extra, seq = cliche_voicings(key, frm, wl, near)
    LOG[-1]['ex'] = f'cliche-{frm}-{wl}-{how}'
    LOG[-1]['ctx']['how'] = how
    song, wtxt = ctx_txt(key)
    ls = held_strings(seq[0], [line[0]])[0]
    txt = (f'{song}, {wtxt}: the line ' + ', '.join(tn(m, key + 'm') if i == 0 else tn(m, names[i]) for i, m in enumerate(line)) + f' {WH[wl]}, on the {STR[ls]} (' +
           ', '.join(ordn(g[6 - ls]) for g in seq) + ' fret), ' + ' and '.join(tn(m, key + 'm') for m in hold) + ' held' +
           (f', {tn(bass_extra[0], key + "m")} in the bass' if bass_extra else '') + '.')
    if how == 'hold':
        return [bar([sym(n) for n in names[:2]], [K(sym(names[0]), seq[0], [(2, 'A')]), K(sym(names[1]), seq[1], [(2, 'A')])], txt),
                bar([sym(n) for n in names[2:]], [K(sym(names[2]), seq[2], [(2, 'A')]), K(sym(names[3]), seq[3], [(2, 'A')])])]
    if how == 'marcatto':
        return [bar([sym(n) for n in names], [K(sym(n), g, st(1, 'A', ACC if i % 2 == 0 else 0)) for i, (n, g) in enumerate(zip(names, seq))], txt + ' Short strokes, accents on 1 and 3.')]
    if how == 'arpeggio':                                       # the line's note, then the two others: eighth, eighth, quarter
        bars_ = []
        for half in (0, 2):
            its = []
            for i in (half, half + 1):
                g = seq[i]
                strs = sorted([6 - j for j in range(6) if g[j] >= 0], reverse=True)
                lsx = held_strings(g, [line[i]])[0]
                others = [s_ for s_ in strs if s_ != lsx and OPEN[s_] + g[6 - s_] in hold]
                its.append(K(sym(names[i]), g, [(0.5, [lsx]), (0.5, [others[0]]), (1, [others[1]])]))
            bars_.append(bar([sym(names[half]), sym(names[half + 1])], its, txt + ' Broken: the line’s note, then the two held notes, eighth, eighth, quarter.' if half == 0 else ''))
        return bars_
    raise ValueError(how)


ex('cliche8', 'cliche-8va-bajo', 'The line from the octave, in the bass',
   ('On a minor chord that stays (most often I or IVm, sometimes IIm in a major key): its root falls by semitones, root, major 7th, minor 7th, 6th, while the chord holds, '
    'over one bar or two. Here the line in the bass.'),
   Q(45, 'Línea desde la 8va., al bajo, on D minor: D, C♯, C, B under F and A. Played here: the first chord.', [K('Dm', gq(['D3', 'F3', 'A3']), [(2, 'A')])]),
   cliche_bars('A', 8, 'bass') + cliche_bars('E', 8, 'bass'))
ex('cliche8', 'cliche-8va-soprano', 'The line from the octave, on top', 'The same line on top.',
   Q(45, 'A la soprano: D, C♯, C, B on top of D minor. Played here: the first chord.', [K('Dm', gq(['D3', 'F4', 'A4', 'D5'], near=6), [(2, 'A')])]),
   cliche_bars('A', 8, 'top') + cliche_bars('E', 8, 'top'))
ex('cliche8', 'cliche-8va-interna', 'The line from the octave, inside', 'The same line in an inner voice.',
   Q(45, 'A la voz interna: D, C♯, C, B under F and A, D in the bass. Played here: the first chord.', [K('Dm', gq(['D3', 'D4', 'F4', 'A4'], near=5), [(2, 'A')])]),
   cliche_bars('A', 8, 'inner') + cliche_bars('F', 8, 'inner', near=7))
ex('cliche8', 'cliche-8va-marcatto', 'The line in the bass, as marcatto 4',
   'Most often the line goes in the bass, on the A or D string, played as a marcatto 4 or broken into an arpeggio.',
   Q(45, 'Marcatto 4: the bass-line chords, four short strokes. Played here: the first.', [K('Dm', gq(['D3', 'F3', 'A3']), st(1, 'A'))]),
   cliche_bars('A', 8, 'bass', how='marcatto') + cliche_bars('F', 8, 'bass', near=7, how='marcatto'))
ex('cliche8', 'cliche-8va-arpegio', 'The line in the bass, arpeggiated',
   'The chord broken: the line’s note, then the other two, eighth, eighth, quarter. Graciano: of all the ways, this is the one most played.',
   Q(45, 'Arpegio: D, F, A, then the same with C♯, C, B. Played here: the first beat and a half.', [['P', [[[5, 5]], [[4, 3]]], [0.5, 0.5], '=D,F|his notes']]),
   cliche_bars('A', 8, 'bass', how='arpeggio') + cliche_bars('E', 8, 'bass', how='arpeggio'))


def frag8(key, near=5):
    """p. 46: the line broken up: the bass and the chord, then the line in sixteenths after a short rest, the chord held"""
    names, line, hold, bx, seq = cliche_voicings(key, 8, 'bass', near)
    LOG[-1]['ex'] = 'cliche-8va-fragmentada'; LOG[-1]['ctx']['how'] = 'fragmented'
    g0 = seq[0]
    ls = held_strings(g0, [line[0]])[0]
    hs = held_strings(g0, hold)
    hp = [(s_, g0[6 - s_]) for s_ in hs]
    lf = [g[6 - ls] for g in seq]
    steps = [[(ls, lf[0])], hp, None, [(ls, lf[0])], [(ls, lf[1])], [(ls, lf[2])], [(ls, lf[3])], hp]
    durs = [0.5, 0.5, 0.25, 0.25, 0.25, 0.25, 0.5, 1.5]
    its = [['P', [list(map(list, x)) for x in steps[:2]], durs[:2], '=' + tn(line[0], key + 'm') + ',' + '+'.join(tn(m, key + 'm') for m in hold) + '|the line'],
           ['W', 0.25],
           ['P', [list(map(list, x)) for x in steps[3:]], durs[3:], '=' + ','.join(tn(m, key + 'm') for m in line) + ',' + '+'.join(tn(m, key + 'm') for m in hold) + '|the line']]
    LOG[-1]['frag'] = dict(steps=steps, durs=durs)
    song, wtxt = ctx_txt(key)
    return [bar([sym(key + 'm')], its, f'{song}, {wtxt}: {tn(line[0], key + "m")}, then ' + ' and '.join(tn(m, key + 'm') for m in hold) + '; a sixteenth rest, '
                + ', '.join(tn(m, key + 'm') for m in line[:3]) + f' in sixteenths, {tn(line[3], key + "m")}, and the two notes held to the end of the bar, the line on the {STR[ls]}.')]


def counter8(key, near=5):
    """p. 46: the line in the bass in quarters, and above it a melody from the chord's root up by step to its 3rd and back:
    root on the “and” of 1, 2nd and 3rd in eighths, 2nd, root"""
    k = M.midi(key + '4') % 12
    names, line, hold, bx, seq = cliche_voicings(key, 8, 'bass', near)
    LOG.pop()
    lo = line
    sc = [0, 2, 3]
    top0 = next(m for m in range(lo[0] + 12, lo[0] + 24) if m % 12 == k)
    tops = [top0, top0 + 2, top0 + 3, top0 + 2, top0]
    seqx = [(lo[0], None, 0.5), (None, tops[0], 0.5), (lo[1], tops[1], 0.5), (None, tops[2], 0.5), (lo[2], tops[3], 1), (lo[3], tops[4], 1)]
    steps = place_lines(seqx, lo_strings=(6, 5, 4), up_strings=(1, 2, 3, 4), maxf=12, prefer=near)
    LOG.append(dict(device='cliche-counter', ex='cliche-8va-contrapunto', ctx=dict(key=key), seq=seqx, steps=[[tuple(p) for p in g] for g, d in steps]))
    song, wtxt = ctx_txt(key)
    names_ = ['+'.join(tn(m, key + 'm') for m in (a, b) if m is not None) for a, b, d in seqx]
    return [bar([sym(key + 'm')], [['P', [g for g, d in steps], [d for g, d in steps], '=' + ','.join(names_) + '|two lines']],
                f'{song}, {wtxt}: the line ' + ', '.join(tn(m, key + 'm') for m in lo) + ' in the bass, a quarter each; above it ' + ', '.join(tn(m, key + 'm') for m in tops) + '.')]


def oct8(key, near=5):
    """p. 46: the line alone, in octaves"""
    k = M.midi(key + '4') % 12
    best = None
    for pair in ((6, 4), (5, 3), (4, 2)):
        for lo0 in range(40, 64):
            if lo0 % 12 != k: continue
            line = [lo0, lo0 - 1, lo0 - 2, lo0 - 3]
            fr = [(m - OPEN[pair[0]], m + 12 - OPEN[pair[1]]) for m in line]
            if not all(1 <= a <= 12 and 1 <= b <= 12 for a, b in fr): continue
            c = abs(fr[0][0] - near)
            if best is None or c < best[0]: best = (c, pair, line, fr)
    c, pair, line, fr = best
    steps = [[(pair[0], a), (pair[1], b)] for a, b in fr]
    LOG.append(dict(device='cliche-oct', ex='cliche-8va-octavas', ctx=dict(key=key), line=line, steps=steps))
    song, wtxt = ctx_txt(key)
    return [bar([sym(key + 'm')], [['P', [list(map(list, g)) for g in steps], [1] * 4, '=' + ','.join(tn(m, key + 'm') + '+' + tn(m, key + 'm') for m in line) + '|octaves']],
                f'{song}, {wtxt}: ' + ', '.join(tn(m, key + 'm') for m in line) + f' in octaves on the {STR[pair[0]]} and {STR[pair[1]]} (' + ', '.join(f'{ordn(a)} and {ordn(b)}' for a, b in fr) + ' fret).')]


ex('cliche8', 'cliche-8va-fragmentada', 'The line broken up',
   'Rhythmically broken: the bass and the chord, then the whole line in sixteenths after a short rest, the chord held to the end of the bar.',
   Q(46, 'Rítmicamente fragmentada, on D minor: D, then F and A. Played here: the first beat.', [['P', [[[5, 5]], [[4, 3], [3, 2]]], [0.5, 0.5], '=D,F+A|his notes']]),
   frag8('A') + frag8('E'))
ex('cliche8', 'cliche-8va-contrapunto', 'The line against a counter-line',
   'In counterpoint: the line in the bass in quarters, and above it a melody that climbs from the chord’s root by step to its 3rd and falls back.',
   Q(46, 'Contrapuntísticamente, on D minor: D in the bass, then D above it on the “and”. Played here: the first beat.', [['P', [[[5, 5]], [[3, 7]]], [0.5, 0.5], '=D,D|his notes']]),
   counter8('A') + counter8('F', near=7))
ex('cliche8', 'cliche-8va-octavas', 'The line in octaves', 'The line alone, in octaves.',
   Q(46, 'Como octavados: D in octaves. Played here: the first.', [['P', [[[5, 5], [3, 7]]], [1], '=D+D|his notes']]),
   oct8('A') + oct8('F', near=6))

ex('cliche5', 'cliche-5ta-bajo', 'The line from the 5th, in the bass',
   'The other line climbs from the minor chord’s 5th by a semitone, again, and comes back: 5, ♯5, 6, ♯5. Here in the bass.',
   Q(46, 'Línea desde la 5ta., al bajo: on D minor, A under F and D. Played here: the first chord.', [K('Dm', gq(['A2', 'F3', 'D4']), [(2, 'A')])]),
   cliche_bars('A', 5, 'bass') + cliche_bars('F', 5, 'bass', near=7))
ex('cliche5', 'cliche-5ta-soprano', 'The line from the 5th, on top', 'The same line on top.',
   Q(46, 'A la soprano: A on top of D and F. Played here: the first chord.', [K('Dm', gq(['D3', 'D4', 'F4', 'A4'], near=5), [(2, 'A')])]),
   cliche_bars('A', 5, 'top') + cliche_bars('E', 5, 'top'))
ex('cliche5', 'cliche-5ta-interna', 'The line from the 5th, inside', 'The same line in an inner voice: Graciano’s usual place for it, on the D string.',
   Q(46, 'A la voz interna: A between D and F. Played here: the first chord.', [K('Dm', gq(['D3', 'A3', 'F4']), [(2, 'A')])]),
   cliche_bars('A', 5, 'inner') + cliche_bars('F', 5, 'inner', near=7))
ex('cliche5', 'cliche-5ta-marcatto', 'The line from the 5th, inside, as marcatto 4', 'For this line the middle voice is the usual place, in a marcatto 4.',
   Q(47, 'Marcatto 4 with the inner voice. Played here: the first stroke.', [K('Dm', gq(['D3', 'A3', 'F4']), st(1, 'A'))]),
   cliche_bars('A', 5, 'inner', how='marcatto') + cliche_bars('F', 5, 'inner', near=7, how='marcatto'))
ex('cliche5', 'cliche-5ta-arpegio', 'The line from the 5th, arpeggiated', 'Broken: the line’s note, then the other two (Graciano’s most frequent way).',
   Q(47, 'Arpegio: D, A, F. Played here: the first beat and a half.', [['P', [[[4, 0]], [[3, 2]]], [0.5, 0.5], '=D,A|his notes']]),
   cliche_bars('A', 5, 'inner', how='arpeggio') + cliche_bars('E', 5, 'inner', how='arpeggio'))


# ---------------- the tritone
TONIC = {'Fm': {5, 8, 0}, 'Eb': {3, 7, 10}, 'G': {7, 11, 2}, 'Am': {9, 0, 4}, 'Bb7': {10, 2, 5, 8}}


def place_pairs(pairs, near, options=((4, 3), (3, 2), (5, 4), (4, 2), (2, 1), (5, 3))):
    """each pair of notes on two strings within the hand, the hand moving least: [[(s, f), (s, f)], ...]"""
    from itertools import product
    cands = []
    for p in pairs:
        cs = []
        for sl, sh in options:
            a, b = p[0] - OPEN[sl], p[1] - OPEN[sh]
            if 1 <= a <= 13 and 1 <= b <= 13 and abs(a - b) <= 3: cs.append([(sl, a), (sh, b)])
        assert cs, p
        cands.append(cs)
    best = None
    prev = {None: (0.0, [])}
    for cs in cands:
        nxt = {}
        for key, (c0, path) in prev.items():
            for c in cs:
                pos = (c[0][1] + c[1][1]) / 2
                cc = c0 + (abs(pos - near) * 0.5 if key is None else abs(pos - key)) + 0.2 * (c[0][0] - 3)
                k2 = pos
                if k2 not in nxt or nxt[k2][0] > cc: nxt[k2] = (cc, path + [c])
        prev = nxt
    return min(prev.values(), key=lambda v: v[0])[1]


def pnames(pairs, chord):
    return ['+'.join(tn(m, chord) for m in p) for p in pairs]


def tri_basic_bars(song, where_txt, dom, tonic, dgrip, tgrip, octave_low):
    t = tritone_pair(dom, octave_low); r = resolve(t, TONIC[tonic])
    pos = place_pairs([t, r], gpos(dgrip))
    LOG.append(dict(device='tritone', ex='tritono-basico', ctx=dict(dom=dom, tonic=tonic), pairs=[t, r], pos=pos))
    return [bar([sym(dom), sym(tonic)], [K(sym(dom), dgrip, [(1, 'A')]), ['P', [list(map(list, x)) for x in pos], [1, 1], '=' + pnames([t], dom)[0] + ',' + pnames([r], tonic)[0] + '|the tritone'],
                                          K(sym(tonic), tgrip, [(1, 'A')])],
                f'{song}, {where_txt}: {pn(dom)}’s tritone, its 3rd and 7th ({pnames([t], dom)[0].replace("+", " with ")}), into {pnames([r], tonic)[0].replace("+", " with ")} of {pn(tonic)}: '
                + ', then '.join(f'the {STR[x[0][0]]} and {STR[x[1][0]]} at the {ordn(x[0][1])} and {ordn(x[1][1])} fret' for x in pos) + '.')]


def four_bars(song, where_txt, dom, dgrip, octave_low):
    ts = four_tritones(dom, octave_low)
    pos = place_pairs(ts, gpos(dgrip))
    LOG.append(dict(device='four-tritones', ex='tritono-reemplazos', ctx=dict(dom=dom), pairs=ts, pos=pos))
    return [bar([sym(dom)], [['P', [list(map(list, x)) for x in pos], [1] * 4, '=' + ','.join(pnames(ts, dom)) + '|the tritones']],
                f'{song}, {where_txt}: over {pn(dom)}, its tritone and the three a minor 3rd apart: ' + ', '.join(n.replace('+', ' with ') for n in pnames(ts, dom))
                + ' (the hearts of ' + ', '.join(pn(sym(deg(dom[:-1], st_, se) + '7')) for st_, se in ((0, 0), (2, 3), (4, 6), (6, 9))) + ').')]


def res_bars(song, where_txt, dom, tonic, dgrip, octave_low):
    ts = four_tritones(dom, octave_low)
    rs = [resolve(t, TONIC[tonic]) for t in ts]
    seq = [x for t, r in zip(ts, rs) for x in (t, r)]
    pos = place_pairs(seq, gpos(dgrip))
    LOG.append(dict(device='resolutions', ex='tritono-resoluciones', ctx=dict(dom=dom, tonic=tonic), tritones=ts, res=rs, pos=pos))
    nm = [pnames([x], dom if i % 2 == 0 else tonic)[0] for i, x in enumerate(seq)]
    chs = [sym(dom), sym(tonic)] * 2
    return [bar(chs, [['P', [list(map(list, x)) for x in pos[:4]], [1] * 4, '=' + ','.join(nm[:4]) + '|the tritones']],
                f'{song}, {where_txt}: each tritone of {pn(dom)} into {pn(tonic)}, the two notes moving in contrary motion by a semitone or a tone: '
                + '; '.join(f'{nm[i].replace("+", " with ")} to {nm[i + 1].replace("+", " with ")}' for i in (0, 2)) + '.'),
            bar(chs, [['P', [list(map(list, x)) for x in pos[4:]], [1] * 4, '=' + ','.join(nm[4:]) + '|the tritones']],
                '; '.join(f'{nm[i].replace("+", " with ")} to {nm[i + 1].replace("+", " with ")}' for i in (4, 6)) + '.')]


def fing_bars(song, dom, tonic, ss, octave_low, near):
    """p. 48: the four tritones and their resolutions in one pair of strings, to know by heart; on the G and B strings
    (tuned a major 3rd apart) a resolution that would stretch the hand too far takes the D string for its lower note"""
    third = (C14.chord_pcs(dom)[1] + 4) % 12
    found = None
    for x0 in range(45, 72):                                 # the four, a minor 3rd apart, wherever they fit on these strings
        if (x0 - third) % 3: continue
        ts = [[x0 + 3 * k, x0 + 3 * k + 6] for k in range(4)]
        rs = [resolve(t, TONIC[tonic]) for t in ts]
        out = []
        for t, r in zip(ts, rs):
            a = on_strings([t], ss); b = on_strings([r], ss)
            fz = [f for s_, f in (a[0] + b[0] if a and b else [])]
            if a and b and min(fz) >= 1 and max(fz) - min(fz) <= width(min(fz)):
                out.append((a[0], b[0], False)); continue
            b2 = on_strings([r], (ss[0] + 1, ss[1]))
            fz = [f for s_, f in (a[0] + b2[0] if a and b2 else [])]
            if a and b2 and min(fz) >= 1 and max(fz) - min(fz) <= width(min(fz)):
                out.append((a[0], b2[0], True)); continue
            break
        else:
            c = (0 if x0 % 12 == third else 2) + max(f for a_, b_, m in out for s_, f in a_ + b_) / 10
            if found is None or c < found[0]: found = (c, ts, rs, out)
    assert found, (dom, ss)
    c, ts, rs, out = found
    LOG.append(dict(device='fingerings', ex='tritono-cuerdas-' + ''.join(map(str, ss)), ctx=dict(dom=dom, tonic=tonic, strings=list(ss)), tritones=ts, res=rs,
                    pos=[(list(a), list(b)) for a, b, moved in out]))
    nm = []
    for t, r in zip(ts, rs): nm += [pnames([t], dom)[0], pnames([r], tonic)[0]]
    steps = [x for a, b, moved in out for x in (a, b)]
    moved = [i for i, (a, b, m) in enumerate(out) if m]
    return [bar([sym(dom), sym(tonic)] * 2, [['P', [list(map(list, x)) for x in steps[:4]], [1] * 4, '=' + ','.join(nm[:4]) + '|the tritones']],
                f'{song}: over {pn(dom)} into {pn(tonic)}, on the {STR[ss[0]]} and {STR[ss[1]]}: ' + '; '.join(
                    f'{nm[2 * i].replace("+", " with ")} ({ordn(a[0][1])}, {ordn(a[1][1])}) to {nm[2 * i + 1].replace("+", " with ")} ({ordn(b[0][1])}, {ordn(b[1][1])})'
                    for i, (a, b, m) in enumerate(out[:2])) + '.'),
            bar([sym(dom), sym(tonic)] * 2, [['P', [list(map(list, x)) for x in steps[4:]], [1] * 4, '=' + ','.join(nm[4:]) + '|the tritones']],
                '; '.join(f'{nm[2 * i].replace("+", " with ")} ({ordn(a[0][1])}, {ordn(a[1][1])}) to {nm[2 * i + 1].replace("+", " with ")} ({ordn(b[0][1])}, {ordn(b[1][1])}'
                          + (f', its lower note on the {STR[b[0][0]]}' if m else '') + ')' for i, (a, b, m) in enumerate(out[2:], start=2)) + '.')]


GI = C14.GR['iw']
ex('tritono', 'tritono-basico', 'The tritone and where it goes',
   ('One of tango’s great resources, for V7 to Im above all (and as much for V7 to I in a major key): the tritone between the key’s 4th and 7th degrees, '
    'the heart of the dominant (its 3rd and 7th), resolving by step into the tonic.'),
   Q(47, 'Posibilidad básica: over E7 the tritone G♯ with D, resolving to A with C over A minor. Played here: both.', [['P', [[[4, 6], [3, 7]], [[4, 7], [3, 5]]], [1, 1], '=G♯+D,A+C|his notes']]),
   tri_basic_bars(IW, 'C7 into F minor (bars 8–9)', 'C7', 'Fm', GI['C7'], GI['Fm'], 52) + tri_basic_bars(IW, 'B♭7 into E♭ (bars 16–17)', 'Bb7', 'Eb', GI['Bb7'], GI['Eb'], 50)
   + tri_basic_bars(YVL, 'D7 into G', 'D7', 'G', [-1, 5, 4, 5, 3, -1], [3, 5, 5, 4, 3, 3], 54))
ex('tritono', 'tritono-reemplazos', 'Four tritones for one',
   'The tritone can be replaced by the one a minor 3rd higher, and that one again: four in all, each a dominant’s heart.',
   Q(48, 'Over E7: G♯ with D; reemplazos B with F, D with G♯, F with B. Played here: the first two.', [['P', [[[4, 6], [3, 7]], [[4, 9], [3, 10]]], [1, 1], '=G♯+D,B+F|his notes']]),
   four_bars(IW, 'its C7 (bar 8, the voice holding “how”)', 'C7', GI['C7'], 52) + four_bars(IW, 'its B♭7 (bars 15–16)', 'Bb7', GI['Bb7'], 50))
ex('tritono', 'tritono-resoluciones', 'Four tritones, four resolutions',
   'Each of the four resolves into the tonic chord: its two notes move in contrary motion, each by a semitone (or a tone), onto notes of the chord.',
   Q(48, 'Cuatro posibles resoluciones, in A minor. Played here: the first tritone and its resolution.', [['P', [[[4, 6], [3, 7]], [[4, 7], [3, 5]]], [1, 1], '=G♯+D,A+C|his notes']]),
   res_bars(IW, 'C7 into F minor', 'C7', 'Fm', GI['C7'], 52) + res_bars(IW, 'B♭7 into E♭', 'Bb7', 'Eb', GI['Bb7'], 50))
ex('tritono', 'tritono-cuerdas-4-3', 'The four on the D and G strings',
   ('On the guitar Graciano plays them on the 4th and 3rd strings: the tritone and its resolution in four fingerings to learn by heart, so the resource is ready under the hand. '
    'He recommends taking a dominant, finding its tritone, the four replacements on the same strings, and then the resolutions.'),
   T(48, 'Posibilidad 1–4, en 4ta. y 3er. cuerda: four diagrams of the tritone and its resolution.'),
   fing_bars(IW, 'C7', 'Fm', (4, 3), 52, 7))
ex('tritono', 'tritono-cuerdas-3-2', 'The four on the G and B strings',
   ('On the 3rd and 2nd strings, tuned a major 3rd apart, the shapes change; where a resolution would need too wide a hand, Graciano plays its lower note on the D string, '
    'the same notes.'),
   T(48, 'Posibilidad 1–4, en 3er. y 2da. cuerda; for the third, the resolution on the 2nd and 4th strings. His diagrams are in A minor, Очи чёрные’s key, so on its E7 these are his positions too.'),
   fing_bars(OCHI, 'E7', 'Am', (3, 2), 55, 5))


# ---------------- the tritone in use (p. 49)
def app_bars(exid, title_place, dom, target, dgrip, tgrip, octave_low, chain_dom=None):
    """p. 49: find the tritone in the dominant, replace it, find the resolution. Over the dominant: a stroke, then its
    tritone and the replacements a minor 3rd up; the last one moves by step into the chord that follows. With chain_dom:
    a dominant's tritone slides down a semitone, both notes, into the next dominant's, which then resolves."""
    if chain_dom is None:
        ts = four_tritones(dom, octave_low)[:3]
        tp = TONIC.get(target) or set(C14.pcs_of(target))
        r = resolve(ts[-1], tp)
        pairs = ts + [r]
        pos = place_pairs(pairs, gpos(dgrip))
        LOG.append(dict(device='application', ex=exid, ctx=dict(dom=dom, target=target), pairs=pairs, pos=pos))
        nm = pnames(ts, dom) + pnames([r], target)
        return [bar([sym(dom)], [K(sym(dom), dgrip, [(1, 'A')]), ['P', [list(map(list, x)) for x in pos[:3]], [1, 1, 1], '=' + ','.join(nm[:3]) + '|the tritones']],
                    f'{IW}, {title_place}: {pn(dom)}, then its tritone and two replacements: ' + ', '.join(n.replace('+', ' with ') for n in nm[:3]) + '.'),
                bar([sym(target)], [['P', [list(map(list, pos[3]))], [1], '=' + nm[3] + '|the tritones'], K(sym(target), tgrip, [(2, 'A'), (1, '-')])],
                    f'The last one into {pn(target)}: {nm[2].replace("+", " with ")} to {nm[3].replace("+", " with ")}; then the chord.')]
    t1 = tritone_pair(dom, octave_low)
    t2 = [t1[0] - 1, t1[1] - 1]
    r = resolve(t2, TONIC[target])
    pairs = [t1, t2, r]
    pos = place_pairs(pairs, gpos(dgrip))
    LOG.append(dict(device='application-chain', ex=exid, ctx=dict(dom=dom, dom2=chain_dom, target=target), pairs=pairs, pos=pos))
    nm = pnames([t1], dom) + pnames([t2], chain_dom) + pnames([r], target)
    g2 = GI[chain_dom]
    return [bar([sym(dom), sym(chain_dom)], [K(sym(dom), dgrip, [(1, 'A')]), ['P', [list(map(list, x)) for x in pos[:2]], [1, 1], '=' + ','.join(nm[:2]) + '|the tritones'],
                                            K(sym(chain_dom), g2, [(1, 'A')])],
                f'{IW}, {title_place}: {pn(dom)}’s tritone ({nm[0].replace("+", " with ")}) slides down a semitone, both notes, into {pn(chain_dom)}’s ({nm[1].replace("+", " with ")}).'),
            bar([sym(target)], [['P', [list(map(list, pos[2]))], [1], '=' + nm[2] + '|the tritones'], K(sym(target), tgrip, [(2, 'A'), (1, '-')])],
                f'Then into {pn(target)}: {nm[1].replace("+", " with ")} to {nm[2].replace("+", " with ")}.')]


ex('aplicacion', 'aplicacion-menor', 'In a minor key',
   'Graciano’s examples of use. For major and minor the shapes on the guitar are the same: find the tritone in the dominant, replace it, find the resolution. In a minor key: the dominant into a minor chord.',
   Q(49, 'Tonalidad menor: A minor, F7, E7, then over E7 its tritone and the other one, each resolving into A minor. Played here: his stroke and the first tritone after it.',
     [K('E7', [0, 2, 0, 1, 0, 0], [(1, 'A')]), ['P', [[[4, 6], [3, 7]]], [1], '=G♯+D|his notes']]),
   app_bars('aplicacion-menor', 'bars 8–9, C7 into F minor, where the voice holds “how”', 'C7', 'Fm', GI['C7'], GI['Fm'], 52))
ex('aplicacion', 'aplicacion-mayor', 'In a major key',
   'The same in a major key: the dominant into the key’s major chord.',
   Q(49, 'Tonalidad mayor: C, A♭7, G7, then over G7 its tritones, resolving into C. Played here: his stroke and the first tritone after it.',
     [K('G7', [3, 5, 3, 4, 3, 3], [(1, 'A')]), ['P', [[[4, 3], [3, 4]]], [1], '=F+B|his notes']]),
   app_bars('aplicacion-mayor', 'bars 16–17, B♭7 into E♭', 'Bb7', 'Eb', GI['Bb7'], GI['Eb'], 50))
ex('aplicacion', 'aplicacion-secundario', 'On a secondary dominant',
   'The same on a secondary dominant: the dominant of another of the key’s chords.',
   Q(49, 'C, D♯7, E7 (V of the VIm), the tritones over E7, into A minor. Played here: his stroke and the first tritone after it.',
     [K('E7', [0, 2, 0, 1, 0, 0], [(1, 'A')]), ['P', [[[4, 6], [3, 7]]], [1], '=G♯+D|his notes']]),
   app_bars('aplicacion-secundario', 'bars 14–15, F7 (the dominant of B♭7) into B♭7, where the voice holds “sighs”', 'F7', 'Bb7', [-1, 8, 7, 8, 6, -1], GI['Bb7'], 55))
ex('aplicacion', 'aplicacion-cadena', 'Through a chain of dominants',
   'Secondary dominants in a row, each with its tritone: here one tritone slides down a semitone into the next dominant’s, which resolves into the tonic.',
   Q(49, 'C, D7, G7, C, C7, F, G7, C, A7, D minor, A♭7, G7, C, G7, C: secondary dominants each with its tritone. Played here: two beats of it.',
     [['P', [[[4, 4], [3, 5]], [[4, 5], [3, 4]]], [1, 1], '=F♯+C,G+B|his notes']]),
   app_bars('aplicacion-cadena', 'bars 14–17, F7, B♭7, E♭', 'F7', 'Eb', [-1, 8, 7, 8, 6, -1], GI['Eb'], 55, chain_dom='Bb7'))


def _labels():
    for sec in EXS.values():
        for e in sec:
            for it in e['quote'].get('items') or []:
                if it[0] in 'PR' and isinstance(it[3], str) and '|' not in it[3]: it[3] += '|his notes'


_labels()
SECTIONS = [dict(id='diatonica', title='Reharmonizing with the key’s chords', part='Exercises', ex=EXS['diatonica']),
            dict(id='tritonal', title='Tritone substitutes', part='Exercises', ex=EXS['tritonal']),
            dict(id='disminuidos', title='Diminished chords for the dominant', part='Exercises', ex=EXS['disminuidos']),
            dict(id='cliche8', title='The line cliché from the octave', part='Exercises', ex=EXS['cliche8']),
            dict(id='cliche5', title='The line cliché from the 5th', part='Exercises', ex=EXS['cliche5']),
            dict(id='tritono', title='The tritone', part='Exercises', ex=EXS['tritono']),
            dict(id='aplicacion', title='The tritone in use', part='Exercises', ex=EXS['aplicacion'])]

from quotes import trim as _trim_quotes   # quotes stay a beat or two
_trim_quotes(SECTIONS)
