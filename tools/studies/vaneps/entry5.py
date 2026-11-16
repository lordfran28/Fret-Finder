"""Van Eps's chromatics (book pp. 138–157; PDF 144–163 of the owner's copy).

1. Chromatic triads over a pedal (pp. 141–148): one bass note held as a pedal; a close triad of one kind and one
   inversion climbs a half step a bar over it, all three voices together, the string set changing as it climbs, the
   pedal moving to another string or octave only when the triad leaves its reach. He does it over G, two octaves, in
   major and minor, each inversion. Ours: major over G (Я вас любил's key note, and his own pedal), minor over A (Очи
   чёрные's), from the key's own triad over its key note up to the same an octave higher (two octaves where the neck and
   the hand allow). Over F (Moonglow) root-position triads can't climb an octave within the hand, so F is not used. The hand
   never stretches beyond four frets (five from the 7th fret), so our pedal moves where his reaches long.
2. Chromatic scales in parallel intervals (p. 157): two voices a fixed interval apart (octave, major and minor 10th,
   12th, major and minor 13th, two octaves) moving up a half step at a time together, across the string sets.
3. The 10th to the 3rd (p. 149): a bass note held; above it a line comes down by half steps from a 10th above it to a
   3rd above it, then climbs back; in major (major 10th to major 3rd) and minor (minor 10th to minor 3rd). Ours: the
   major form over F (bass on the low E string) and over G (bass on the A string); with the bass held the hand cannot
   move, and the minor form doesn't fit one hand anywhere on the neck, so it is described only.
Every chord, interval and fingering is made by rule here and checked by check5.py. His pages are described and his
first two chords quoted where they could be read with certainty; nothing else of his is copied."""
import sys
sys.path.insert(0, '/home/claude/studies'); sys.path.insert(0, '/home/claude/studies/tango'); sys.path.insert(0, '/home/claude/studies/vaneps')
import entry4 as E4
from kit_study import OPEN, nn, place_lines, two_lines

BOOK = E4.E3.E2.BOOK
MAXF = 15
SETS = {4: (6, 5, 4), 3: (5, 4, 3), 2: (4, 3, 2), 1: (3, 2, 1)}         # Van Eps's n/3, thick string first
STRN = {6: 'low E', 5: 'A', 4: 'D', 3: 'G', 2: 'B', 1: 'high E'}
MAJ_N = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
MIN_N = ['Cm', 'C#m', 'Dm', 'Ebm', 'Em', 'Fm', 'F#m', 'Gm', 'G#m', 'Am', 'Bbm', 'Bm']
PED_N = {5: 'F', 9: 'A', 3: 'Eb', 7: 'G'}
INV_W = {0: 'root position', 1: 'first inversion', 2: 'second inversion'}
CHECK_TRI, CHECK_PAR, CHECK_HELD = [], [], []


def T(text, p, **kw): return dict(where=f'{BOOK}, p. {p}', text=text, item=None, by='Van Eps', whose='Van Eps’s own', played='', **kw)


def ordn(n): return f'{n}{"th" if 10 <= n % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")}'


def fits(frets):
    """the fretted notes within one hand: four frets, five from the 7th fret up (open strings are free)"""
    fr = [f for f in frets if f > 0]
    if not fr: return True
    lo, hi = min(fr), max(fr)
    return hi - lo + 1 <= (5 if lo >= 7 else 4)


# ----------------------------------------------------------------------------------- 1. chromatic triads over a pedal
def voicing(root, minor, inv):
    """close triad; root = midi of its root in root position; inv 1: 3rd at the bottom, 2: 5th at the bottom"""
    t, f = root + (3 if minor else 4), root + 7
    return [root, t, f] if inv == 0 else [t, f, root + 12] if inv == 1 else [f, root + 12, t + 12]


def placements(tri, ped_pc):
    """the triad on one set of three adjacent strings, the pedal (its pitch class, any octave, below the triad) on a
    thicker string, all four within the hand"""
    out = []
    for n, ss in SETS.items():
        fr = [m - OPEN[6 - s] for m, s in zip(tri, ss)]
        if min(fr) < 0 or max(fr) > MAXF: continue
        for ps in range(6, ss[0], -1):
            for pf in range(0, MAXF + 1):
                pm = OPEN[6 - ps] + pf
                if pm % 12 != ped_pc or pm >= tri[0]: continue
                if not fits(fr + [pf]): continue
                g = [-1] * 6; g[6 - ps] = pf
                for s, f in zip(ss, fr): g[6 - s] = f
                out.append(dict(set=n, ped=(ps, pf), pm=pm, grip=g, tri=list(tri)))
    return out


def centre(p):
    fr = [f for f in p['grip'] if f > 0]
    return sum(fr) / len(fr) if fr else None


def opens(p): return sum(1 for i, f in enumerate(p['grip']) if f == 0 and 6 - i != p['ped'][0])


def trans(a, b):
    ca, cb = centre(a), centre(b)
    c = abs(ca - cb) if ca is not None and cb is not None else 0
    c += 0.6 * (a['set'] != b['set']) + 1.5 * (a['ped'] != b['ped']) + 1.0 * (a['pm'] != b['pm']) + 0.3 * opens(b)
    return c


def tri_path(tris, ped_pc):
    layers = [placements(t, ped_pc) for t in tris]
    if any(not L for L in layers): return None
    best = [(0.05 * (centre(p) or 0) + 0.3 * opens(p), [p]) for p in layers[0]]
    for L in layers[1:]:
        best = [min(((c + trans(pth[-1], p), pth + [p]) for c, pth in best), key=lambda x: x[0]) for p in L]
    return min(best, key=lambda x: x[0])[1]


def chromatic_triads(key_pc, minor, inv):
    """from the key's own triad over the key note, as low as it goes, a half step a bar: two octaves if the neck and
    the hand allow, else one"""
    for n in (25, 13):
        for r in range(28, 70):
            if r % 12 != key_pc: continue
            tris = [voicing(r + k, minor, inv) for k in range(n)]
            p = tri_path(tris, key_pc)
            if p: return r, p
    raise ValueError('no path')


def tri_name(root_pc, minor, ped_pc):
    nm = (MIN_N if minor else MAJ_N)[root_pc % 12]
    return nm if root_pc % 12 == ped_pc else nm + '/' + PED_N[ped_pc]


def disp(nm): return nm.replace('b', '♭').replace('#', '♯')


def tri_bars(exid, key_pc, minor, inv):
    r, path = chromatic_triads(key_pc, minor, inv)
    bars, prev = [], None
    rec = []
    for k, p in enumerate(path):
        nm = tri_name(r + k, minor, key_pc)
        rec.append(dict(name=nm, grip=p['grip'], tri=p['tri'], pm=p['pm'], set=p['set'], ped=p['ped']))
        note = []
        if prev is not None:
            if p['ped'] != prev['ped']:
                ps, pf = p['ped']
                oc = ', an octave higher' if p['pm'] > prev['pm'] else ', an octave lower' if p['pm'] < prev['pm'] else ''
                note.append(f'The bass {disp(PED_N[key_pc])} moves to the open {STRN[ps]} string{oc}.' if pf == 0 else
                            f'The bass {disp(PED_N[key_pc])} moves to the {STRN[ps]} string, {ordn(pf)} fret{oc}.')
            if p['set'] != prev['set']:
                ss = SETS[p['set']]
                note.append(f'The triad moves to the {STRN[ss[0]]}, {STRN[ss[1]]} and {STRN[ss[2]]} strings ({p["set"]}/3).')
        bars.append(dict(chords=[nm], note=' '.join(note), items=[['C', nm, p['grip'], 4.0, {'roll': 0.004}]]))
        prev = p
    CHECK_TRI.append(dict(id=exid, key_pc=key_pc, minor=minor, inv=inv, root=r, chords=rec))
    return bars, path


def first_note(path, key_pc, minor, inv, song):
    p0 = path[0]; ps, pf = p0['ped']; ss = SETS[p0['set']]
    n = len(path)
    key = disp(PED_N[key_pc]) + (' minor' if minor else ' major')
    span = 'two octaves' if n == 25 else 'an octave'
    return (f'{song}: {key} in {INV_W[inv]}, over {PED_N[key_pc]} on the {STRN[ps]} string ({"open" if pf == 0 else ordn(pf) + " fret"}), '
            f'the triad on the {STRN[ss[0]]}, {STRN[ss[1]]} and {STRN[ss[2]]} strings; then a half step a bar for {span}, '
            f'back to {disp(PED_N[key_pc])}{"m" if minor else ""}. Each chord is named as the triad over the {PED_N[key_pc]}. One chord a bar; let each ring its full four beats.')


EX_T = []
SONG = {7: 'The key note of Я вас любил, G', 9: 'The key note of Очи чёрные, A'}
G = dict(roll=0.004)
for exid, title, key_pc, minor, inv, quote, idea in [
    ('chrom-maj-1st', 'Major triads, first inversion, over a pedal', 7, False, 1,
     dict(where=f'{BOOK}, p. 141', text='over G on the low E string, G major with its 3rd at the bottom on the A, D and G strings (the D and G open), then the same shape a half step higher, which he names G11♭9♯5.',
          items=[['C', 'G', [3, 2, 0, 0, -1, -1], 1.0, G], ['C', 'G#/G', [3, 3, 1, 1, -1, -1], 1.0, G], ['W', 2]], whose='Van Eps’s own', played='Played here: those two.'),
     'Van Eps holds one bass note, a pedal, and moves a triad up over it a half step at a time, all three voices together: one kind of triad, one inversion, the same shape all the way, '
     'only its place on the neck and its string set changing. Every bar is a new sound over the same bass, and he names each one as a chord on the pedal (B♭ major over G is G minor 7). '
     'He runs it two octaves over G, the whole neck, in each inversion, major and minor; “chromatics, chromatics, and more chromatics”, he writes.'),
    ('chrom-maj-2nd', 'Major triads, second inversion, over a pedal', 7, False, 2,
     T('The same climb over G with each triad in second inversion (its 5th at the bottom); the pages after give each line again with every chord on the other string sets.', 141),
     'The same with each triad in second inversion: the 5th at the bottom, the root in the middle, the 3rd on top.'),
    ('chrom-maj-root', 'Major triads, root position, over a pedal', 7, False, 0,
     dict(where=f'{BOOK}, p. 141', text='over the same G, C major in root position on the A, D and G strings (the G open), then C♯ major, the same shape a fret higher.',
          items=[['C', 'C/G', [3, 3, 2, 0, -1, -1], 1.0, G], ['C', 'C#/G', [3, 4, 3, 1, -1, -1], 1.0, G], ['W', 2]], whose='Van Eps’s own', played='Played here: those two.'),
     'The same with each triad in root position. Van Eps starts each line on the lowest triad that fits over his G; ours start on the key’s own chord.'),
    ('chrom-min-1st', 'Minor triads, first inversion, over a pedal', 9, True, 1,
     dict(where=f'{BOOK}, p. 145', text='over G on the low E string, G minor with its 3rd at the bottom on the A, D and G strings (the D and G open), then G♯ minor, a fret higher.',
          items=[['C', 'Gm', [3, 1, 0, 0, -1, -1], 1.0, G], ['C', 'G#m/G', [3, 2, 1, 1, -1, -1], 1.0, G], ['W', 2]], whose='Van Eps’s own', played='Played here: those two.'),
     'The same with minor triads: Van Eps gives every inversion again in minor over the same G.'),
    ('chrom-min-2nd', 'Minor triads, second inversion, over a pedal', 9, True, 2,
     T('Minor triads in second inversion climbing over G, two octaves; the next pages give each on the other string sets.', 145),
     'Minor triads in second inversion: the 5th at the bottom.'),
    ('chrom-min-root', 'Minor triads, root position, over a pedal', 9, True, 0,
     T('Minor triads in root position climbing over G, two octaves.', 145),
     'Minor triads in root position.')]:
    b, path = tri_bars(exid, key_pc, minor, inv)
    b[0]['note'] = first_note(path, key_pc, minor, inv, SONG[key_pc]) + (' ' + b[0]['note'] if b[0]['note'] else '')
    EX_T.append(dict(id=exid, title=title, idea=idea, quote=quote, bars=b))


# ------------------------------------------------------------------------- spelling of a chromatic line in a key
SCALES = {5: [5, 7, 9, 10, 0, 2, 4], 3: [3, 5, 7, 8, 10, 0, 2], 9: [9, 11, 0, 2, 4, 5, 7, 8], 7: [7, 9, 11, 0, 2, 4, 6]}   # F, E♭, G major; A minor with G♯
KEYNM = {5: {5: 'F', 7: 'G', 9: 'A', 10: 'B♭', 0: 'C', 2: 'D', 4: 'E'},
         3: {3: 'E♭', 5: 'F', 7: 'G', 8: 'A♭', 10: 'B♭', 0: 'C', 2: 'D'},
         9: {9: 'A', 11: 'B', 0: 'C', 2: 'D', 4: 'E', 5: 'F', 7: 'G', 8: 'G♯'},
         7: {7: 'G', 9: 'A', 11: 'B', 0: 'C', 2: 'D', 4: 'E', 6: 'F♯'}}


def _norm(n):
    for a, b in (('♭♯', ''), ('♯♭', '')): n = n.replace(a, b)
    return n


def spell(pc, key, up):
    """a note of a chromatic line: the key's own name if it is in the key; else the note below raised (going up) or
    the note above lowered (going down), a natural if either way gives one"""
    names = KEYNM[key]
    if pc in names: return names[pc]
    sh = _norm(names[(pc - 1) % 12] + '♯') if (pc - 1) % 12 in names else None
    fl = _norm(names[(pc + 1) % 12] + '♭') if (pc + 1) % 12 in names else None
    nat = [x for x in (sh, fl) if x and len(x) == 1]
    if nat: return nat[0]
    return (sh or fl) if up else (fl or sh)


# --------------------------------------------------------------------------- 2. chromatic scales in parallel intervals
INTS = [('oct', 'Octaves', 12, 3, 'E♭3', 'I Wonder Who’s Kissing Her Now’s key note, E♭'),
        ('10maj', 'Major 10ths', 16, 5, 'F2', 'Moonglow’s key note, F'),
        ('10min', 'Minor 10ths', 15, 9, 'A2', 'The key note of Очи чёрные, A'),
        ('12', '12ths', 19, 5, 'F2', 'Moonglow’s key note, F'),
        ('13maj', 'Major 13ths', 21, 5, 'F2', 'Moonglow’s key note, F'),
        ('13min', 'Minor 13ths', 20, 9, 'A2', 'The key note of Очи чёрные, A'),
        ('15', 'Two octaves (15ths)', 24, 5, 'F2', 'Moonglow’s key note, F')]
from kit_study import N
IV_W = {12: 'an octave', 16: 'a major 10th', 15: 'a minor 10th', 19: 'a 12th', 21: 'a major 13th', 20: 'a minor 13th', 24: 'two octaves'}


def chunks(steps, sizes):
    out, i = [], 0
    for n in sizes:
        out.append(steps[i:i + n]); i += n
    assert i == len(steps)
    return out


def par_bars(exid, iv, key, start):
    lo0 = N(start)
    seq = [(lo0 + k, lo0 + k + iv, 4.0 if k == 12 else 1.0) for k in range(13)]
    pl = place_lines(seq, lo_strings=(6, 5, 4, 3), up_strings=(5, 4, 3, 2, 1), maxf=MAXF, prefer=1, open_cost=1.0)
    CHECK_PAR.append(dict(id=exid, iv=iv, seq=seq, steps=pl))
    bars = []
    for ch, part in zip(chunks(pl, [4, 4, 4, 1]), chunks(seq, [4, 4, 4, 1])):
        lab = '=' + ','.join(f'{spell(a % 12, key, True)}+{spell(b % 12, key, True)}' for a, b, d in part) + '|' + IV_W[iv] + ' apart'
        bars.append(dict(chords=[], note='', items=[two_lines(ch, over=lab) + [{'hold': []}]]))
    return bars, pl


def strings_text(pl):
    pairs = []
    for g, d in pl:
        ss = tuple(sorted((s for s, f in g), reverse=True))
        if not pairs or pairs[-1] != ss: pairs.append(ss)
    return '; '.join(f'{STRN[a]} and {STRN[b]}' for a, b in pairs)


EX_P = []
for code, title, iv, key, start, song in INTS:
    b, pl = par_bars('par-' + code, iv, key, start)
    b[0]['note'] = (f'{song}: two voices {IV_W[iv]} apart, both struck together, climbing a half step a beat for an octave. '
                    f'The pair moves across the strings as it climbs, the hand moving as little as it can; the strings, in order: {strings_text(pl)}.')
    idea = ('Van Eps’s chromatic scale in two voices: the two keep the same distance and move up together a half step at a time.'
            if code == 'oct' else f'The same climb in {title.lower().split(" (")[0]}.')
    q = (T('octaves, major and minor 10ths, 12ths, major and minor 13ths and two octaves, each climbing by half steps, the strings marked as the pair crosses them; '
           'under the two octaves he writes “walk on the fingers”: one finger after another along the string.', 157) if code == 'oct' else T(f'his line in {title.lower().split(" (")[0]}.', 157))
    EX_P.append(dict(id='par-' + code, title=f'Chromatic scale in {title.lower()}', idea=idea, quote=q, bars=b))


# ------------------------------------------------------------------------------- 3. the 10th to the 3rd over a held bass
def held_fingering(bass_m, line, bass_strings=(6, 5, 4)):
    """The bass stays down the whole time, so the hand can't move: one position (four frets, five from the 7th fret
    up) holds the bass and every note of the line, or the line uses an open string. A line note on the bass's own fret
    is allowed only when the bass is under the first finger (a partial barre). Fewest string changes, then fewest open
    strings, then the lowest position. Returns ((bass string, fret), (h, width), [(s, f) per line note]) or None."""
    best = None
    for bs in bass_strings:
        bf = bass_m - OPEN[6 - bs]
        if not 0 <= bf <= MAXF: continue
        for h in range(1, MAXF - 1):
            w = 5 if h >= 7 else 4
            if bf > 0 and not (h <= bf <= h + w - 1): continue
            layers = []
            for m in line:
                c = []
                for s in range(bs - 1, 0, -1):
                    f = m - OPEN[6 - s]
                    if f == 0 or (h <= f <= h + w - 1 and not (bf > 0 and f == bf and bf != h)): c.append((s, f))
                if not c: break
                layers.append(c)
            else:
                st = [(0.3 * (p[1] == 0), [p]) for p in layers[0]]
                for L in layers[1:]:
                    st = [min(((c + (q[-1][0] != p[0]) + 0.3 * (p[1] == 0), q + [p]) for c, q in st), key=lambda x: x[0]) for p in L]
                c, path = min(st, key=lambda x: x[0])
                c += 0.02 * h + 0.5 * (bs != 6)
                if best is None or c < best[0]: best = (c, (bs, bf), (h, w), path)
    return best[1:] if best else None


def held_bars(exid, key, bass):
    b = N(bass)
    down = [b + i for i in range(16, 3, -1)]                   # the major 10th down to the major 3rd: 13 notes
    up = [b + i for i in range(4, 17)]
    fg = held_fingering(b, down + up)
    if fg is None: raise ValueError(f'{exid}: no one-hand fingering')
    (bs, bf), (h, w), path = fg
    seq, steps = [], []
    for line, pth in ((down, path[:13]), (up, path[13:])):
        for i, (m, p) in enumerate(zip(line, pth)):
            d = 4.0 if i == 12 else 1.0
            seq.append((b if i % 4 == 0 else None, m, d))
            steps.append(([[bs, bf], list(p)] if i % 4 == 0 else [list(p)], d))
    CHECK_HELD.append(dict(id=exid, bass=b, bass_at=(bs, bf), hand=(h, w), seq=seq, steps=steps))
    bars = []
    for half, up_ in ((0, False), (1, True)):
        part_seq = seq[13 * half:13 * half + 13]; part_st = steps[13 * half:13 * half + 13]
        for ch, ps in zip(chunks(part_st, [4, 4, 4, 1]), chunks(part_seq, [4, 4, 4, 1])):
            names = []
            for lo_, upm, d in ps:
                u = spell(upm % 12, key, up_)
                names.append(f'{spell(lo_ % 12, key, up_)}+{u}' if lo_ is not None else u)
            lab = '=' + ','.join(names) + '|' + ('down by half steps' if not up_ else 'up by half steps')
            bars.append(dict(chords=[], note='', items=[two_lines(ch, over=lab) + [{'hold': [bs]}]]))
    return bars, (bs, bf), (h, w)


EX_H = []
for exid, title, key, bass, song in [
        ('held-maj-low', 'The 10th to the 3rd and back, bass on the low E string', 5, 'F2', 'Moonglow’s key note, F'),
        ('held-maj-high', 'The 10th to the 3rd and back, bass on the A string', 7, 'G3', 'The key note of Я вас любил, G')]:
    b, (bs, bf), (h, w) = held_bars(exid, key, bass)
    b[0]['note'] = (f'{song}, held on the {STRN[bs]} string ({ordn(bf)} fret, first finger) and struck again each bar: above it the line comes down by half steps '
                    f'from the major 10th to the major 3rd, then climbs back. The hand stays at the {ordn(h)} fret the whole time; '
                    + ('where the line needs the 1st fret, lay the first finger across as a small barre without lifting the bass.' if bf == h == 1 else
                       'where the line meets the bass’s fret, lay the first finger across as a small barre without lifting the bass.' if bf == h else 'keep the bass finger down.'))
    b[4]['note'] = 'And back up, from the 3rd to the 10th.'
    if exid == 'held-maj-low':
        idea = ('Van Eps holds a bass note and moves a line above it by half steps, from a 10th above it down to a 3rd above it, then from the 3rd back up to the 10th: '
                'every interval in turn against the same bass, in several fingerings. He gives the same in minor (from the minor 10th to the minor 3rd), which only fits '
                'with the long reaches he warns of, wider than the hand here, so it is left out.')
        q = T('seven fingerings of the major form, the bass on the low E string in the first five and on the A string in the last two; then the minor forms.', 149)
    else:
        idea = 'The same with the bass on the A string, higher up.'
        q = T('his last two major forms have the bass on the A string.', 149)
    EX_H.append(dict(id=exid, title=title, idea=idea, quote=q, bars=b))

SECTIONS = E4.SECTIONS + [dict(id='vaneps-chrom-triads', title='Chromatic triads over a pedal', part='Exercises', ex=EX_T),
                          dict(id='vaneps-chrom-lines', title='Chromatic lines in two voices', part='Exercises', ex=EX_P + EX_H)]
