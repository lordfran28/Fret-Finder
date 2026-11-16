"""Tango cadences, rebuilt by rule: Graciano, Método de guitarra tango, ch. 4 ("Cadencial"), pp. 35–39 of the owner's copy.
The moment that links two sections, or leads to the end of a section or of the piece.

Nothing of Graciano's is kept here beyond the opening beat or two of each example (the quotes). Every cadence of ours is
made by a function that applies his rule to a key and the chords of one of the owner's songs: Очи чёрные (A minor),
I Wonder Who's Kissing Her Now (E♭, its F minor), Я помню чудное мгновенье (E♭, whose third stanza turns to E♭ minor),
Я вас любил (G, its E minor). Each function logs what it made (LOG); check14.py rebuilds the rule with its own code and
checks every note, chord, bass line, rhythm, string and fret.
"""
import sys
from itertools import combinations, product
sys.path.insert(0, '/home/claude/studies'); sys.path.insert(0, '/home/claude/studies/tango')
import mel as M
from entry import K, st, arr, G4, ACC, GHOST
from kit_study import place_lines, shape
import entry13 as F13

OPEN = M.OPEN
tr_safe, dn, nd, ordn, STR, gpos, width = F13.tr_safe, F13.dn, F13.nd, F13.ordn, F13.STR, F13.gpos, F13.width
OCHI, IW, YVL, GLI = 'Очи чёрные', 'I Wonder Who’s Kissing Her Now', 'Я вас любил', 'Я помню чудное мгновенье'
OWN = 'Graciano’s own'
LOG = []
EXS = {}


def where(p): return f'Método de guitarra tango, p. {p}'
def ex(sec, id, title, idea, quote, bars): EXS.setdefault(sec, []).append(dict(id=id, title=title, idea=idea, quote=quote, bars=bars))
def bar(chords, items, note=''): return dict(chords=chords, items=items, note=note)
def Q(page, text, items): return dict(where=where(page), text=text, items=items, whose=OWN, played='')


# ---------------------------------------------------------------- notes and chords
def nn(m, sharp=True):
    """a midi number as a note name (sharps, or flats)"""
    names = (['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'] if sharp else
             ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B'])
    return names[m % 12] + str(m // 12 - 1)


def spell(m, key, mode='major', direction=1):
    """a midi note named for a key: the key's own note by its own name (B♭ in E♭), a natural letter if there is one,
    otherwise a sharp going up and a flat coming down"""
    kind = 'major' if mode == 'major' else 'natural'
    sc = {M.midi(n + '4') % 12: n for n in M.scale_pcs(key, 'major' if mode == 'major' else 'harmonic minor')}
    sc.update({M.midi(n + '4') % 12: n for n in M.scale_pcs(key, 'major' if mode == 'major' else 'melodic minor') if M.midi(n + '4') % 12 not in sc})
    pc = m % 12
    if pc in sc: name = sc[pc]
    else:
        nat = {0: 'C', 2: 'D', 4: 'E', 5: 'F', 7: 'G', 9: 'A', 11: 'B'}
        if pc in nat: name = nat[pc]
        else: name = ['C#', 'D#', 'F#', 'G#', 'A#'][[1, 3, 6, 8, 10].index(pc)] if direction > 0 else ['Db', 'Eb', 'Gb', 'Ab', 'Bb'][[1, 3, 6, 8, 10].index(pc)]
    o = m // 12 - 1
    for oo in (o - 1, o, o + 1):
        try:
            if M.midi(name + str(oo)) == m: return name + str(oo)
        except AssertionError: pass
    raise ValueError((m, name))


def tone_name(m, chord):
    """a note of a chord spelled as the chord spells it (F♯°7: F♯, A, C, E♭)"""
    base = chord.split('/')[0]
    for a, b in ENH.items():
        if base.startswith(a): base = b + base[len(a):]
    r = base[:2] if len(base) > 1 and base[1] in 'b#' else base[:1]
    q = base[len(r):]
    if q in M.QUAL:
        for d in M.QUAL[q]:
            p = tr_safe(r + '4', *M.DEG[d])
            if M.midi(p) % 12 == m % 12: return ENH.get(M.pc_name(p), M.disp(p)).replace('b', '♭').replace('#', '♯')
    bs = chord.split('/')[1] if '/' in chord else None
    if bs and M.midi(bs + '4') % 12 == m % 12: return M.disp(bs + '4')
    return nd(nn(m, sharp=False))


def at(pc_name, near_midi):
    """the note of a pitch-class name nearest a midi number"""
    best = None
    for o in range(0, 8):
        n = pc_name + str(o)
        try: m = M.midi(n)
        except AssertionError: continue
        if best is None or abs(m - near_midi) < abs(best[1] - near_midi): best = (n, m)
    return best[0]


def up(n, steps, semis): return tr_safe(n, steps, semis)


QUAL = {'': [0, 4, 7], 'm': [0, 3, 7], '7': [0, 4, 7, 10], 'dim7': [0, 3, 6, 9], 'maj7': [0, 4, 7, 11]}


def chord_pcs(name):
    """pitch classes of a chord name like 'E7', 'Fdim7', 'Am', 'B7/F#'"""
    base = name.split('/')[0]
    r = base[:2] if len(base) > 1 and base[1] in 'b#' else base[:1]
    q = base[len(r):]
    rp = M.midi(r + '4') % 12
    return [(rp + x) % 12 for x in QUAL[q]], rp


ENH = {'Cb': 'B', 'Fb': 'E', 'E#': 'F', 'B#': 'C'}


def sym(name):
    """a chord symbol as the page reads it (C♭7 as B7): ASCII, 'b' and '#', 'dim7'"""
    for a, b in ENH.items():
        if name.startswith(a): name = b + name[len(a):]
        name = name.replace('/' + a, '/' + b)
    return name


def pname(name):
    """a chord name for the page (C♭7 written as B7, the grip it is)"""
    for a, b in ENH.items():
        if name.startswith(a): name = b + name[len(a):]
        name = name.replace('/' + a, '/' + b)
    return M.dname(name) if 'dim7' in name else dn(name)


# ---------------------------------------------------------------- the songs' grips and placing chords
GR = {'ochi': {'Am': G4['Am'], 'E7': G4['E7'], 'Dm': G4['Dm'], 'Am_o': [-1, 0, 2, 2, 1, 0], 'E7_o': [0, 2, 0, 1, 0, 0]},
      'iw': {'Eb': [-1, 6, 8, 8, 8, -1], 'Bb7': [6, -1, 6, 7, 6, -1], 'C7': [8, -1, 8, 9, 8, -1], 'Fm': [-1, 8, 10, 10, 9, -1],
             'F': [-1, 8, 10, 10, 10, -1], 'G7': [3, -1, 3, 4, 3, -1], 'Cm': [-1, 3, 5, 5, 4, -1]},
      'gli': {'Eb': [-1, 6, 8, 8, 8, -1], 'Ebm': [-1, 6, 8, 8, 7, -1]},
      'yvl': {'Em': [0, 2, 2, 0, 0, 0]}}


def grips_all(midis, allow_open=False, maxf=13, bass_strings=(6, 5, 4, 3), max_gaps=1):
    """every playable way to put these notes on the strings (lowest on one of `bass_strings`)"""
    ms = sorted(midis); out = []
    for combo in combinations((6, 5, 4, 3, 2, 1), len(ms)):
        if combo[0] not in bass_strings: continue
        fr = [m - OPEN[s] for m, s in zip(ms, combo)]
        if any(f < 0 or f > maxf or (f == 0 and not allow_open) for f in fr): continue
        fz = [f for f in fr if f > 0]
        if fz and max(fz) - min(fz) > width(min(fz)): continue
        if (combo[0] - combo[-1] + 1) - len(combo) > max_gaps: continue
        g = [-1] * 6
        for s_, f in zip(combo, fr): g[6 - s_] = f
        out.append(g)
    return out


def grip_of(midis, near=5, allow_open=False, maxf=13, bass_strings=(6, 5, 4, 3)):
    """a grip for exact notes, each on its own string, the lowest on one of `bass_strings`; within the hand, nearest a fret"""
    ms = sorted(midis)
    best = None
    for combo in combinations((6, 5, 4, 3, 2, 1), len(ms)):
        if combo[0] not in bass_strings: continue
        fr = [m - OPEN[s] for m, s in zip(ms, combo)]
        if any(f < 0 or f > maxf or (f == 0 and not allow_open) for f in fr): continue
        fz = [f for f in fr if f > 0]
        if fz and max(fz) - min(fz) > width(min(fz)): continue
        gaps = (combo[0] - combo[-1] + 1) - len(combo)
        c = abs((min(fz) if fz else near) - near) + 0.5 * sum(1 for f in fr if f == 0) + 0.3 * gaps + 0.1 * (max(fz) - min(fz) if fz else 0)
        if best is None or c < best[0]: best = (c, combo, fr)
    if best is None: raise ValueError('no grip for ' + ','.join(nn(m) for m in ms))
    g = [-1] * 6
    for s, f in zip(best[1], best[2]): g[6 - s] = f
    return g


def gnotes(g): return [OPEN[6 - i] + g[i] for i in range(6) if g[i] >= 0]


# ================================================================ between two sections (pp. 35–36)
def link(key_a, mode_a, mode_b, way, near, maxf=12):
    """pp. 35–36: over the last bar of section A (the 4th of its phrase), its tonic chord, then the key's 5th alone, then two
    pairs of notes in contrary motion into the first chord of section B, in the same key, minor or major. One voice falls
    by semitones from the 5th (its sharp 4th, its 4th) to B's 3rd; the other climbs to the root: in way a, above, from
    the 6th (A's own: the minor 6th from a minor key, the major 6th from a major one) to the leading note; in way b, below,
    from the major 6th to the leading note. Each pair a quarter, the landing a half."""
    R = key_a
    fifth = min((up(R + str(o), 4, 7) for o in (2, 3, 4)), key=lambda n: abs(M.midi(n) - 57))   # the key's 5th, alone, where his sits
    f1, f2 = M.tr(fifth, -1, -1), M.tr(fifth, -1, -2)      # its sharp 4th (a semitone down), its 4th
    third_b = up(fifth, -2, -4 if mode_b == 'minor' else -3)
    if way == 'a':
        six = up(fifth, 1, 1 if mode_a == 'minor' else 2)
        seven = up(fifth, 2, 4); root = up(fifth, 3, 5)
        pairs = [[f1, six], [f2, seven], [third_b, root]]
    else:
        six = up(up(fifth, 1, 2), -7, -12)                 # the major 6th, an octave below
        seven = up(six, 1, 2); root = up(seven, 1, 1)
        pairs = [[six, f1], [seven, f2], [root, third_b]]
    tonic = R + ('m' if mode_a == 'minor' else '')
    land = R + ('m' if mode_b == 'minor' else '')
    seq = [(None, M.midi(fifth), 1)] + [(M.midi(a), M.midi(b), 1) for a, b in pairs[:2]] + [(M.midi(pairs[2][0]), M.midi(pairs[2][1]), 2)]
    steps = place_lines([(lo, upn, d) for lo, upn, d in seq], lo_strings=(6, 5, 4, 3), up_strings=(1, 2, 3, 4, 5), maxf=maxf, prefer=near)
    names = [[fifth]] + pairs
    LOG.append(dict(device='link', ctx=dict(key=R, mode_a=mode_a, mode_b=mode_b, way=way), lines=names, steps=[[tuple(p) for p in g] for g, d in steps],
                    durs=[d for g, d in steps]))
    return tonic, land, names, steps


def link_items(tonic, tgrip, names, steps, label):
    its = [K(sym(tonic), tgrip, [(1, 'A')])]
    groups = [g for g, d in steps]; durs = [d for g, d in steps]
    lab = ','.join('+'.join(nd(n) for n in sorted(ns, key=M.midi)) for ns in names)
    its.append(['P', groups[:3], durs[:3], '=' + ','.join(lab.split(',')[:3]) + '|' + label])
    land = ['P', groups[3:], [2], '=' + lab.split(',')[3] + '|' + label]
    return its, land


def link_bars(exid, song, key, mode_a, mode_b, way, tgrip, where_txt, near=5, maxf=12):
    tonic, land, names, steps = link(key, mode_a, mode_b, way, near, maxf)
    LOG[-1]['ex'] = exid
    first, second = link_items(tonic, tgrip, names, steps, 'the line')
    pairs = names[1:]
    say = (f'{song}, {where_txt}: {dn(tonic)}, then {nd(names[0][0])} alone, then ' +
           ', '.join(' with '.join(nd(n) for n in sorted(p, key=M.midi)) for p in pairs[:2]) + '. ')
    pos = [g for g, d in steps]
    say += 'The line: ' + '; '.join(', '.join(f'{nd(n)} on the {STR[s]} ({ordn(f)})' for n, (s, f) in zip(sorted(ns, key=M.midi), sorted(g, key=lambda x: -x[0])))
                                   for ns, g in zip(names, pos)) + '.'
    return [bar([sym(tonic)], first, say),
            bar([sym(land)], [second, ['W', 2]], f'Into {dn(land)}: ' + ' with '.join(nd(n) for n in sorted(pairs[2], key=M.midi)) + ', the first notes of the new section.')]


LINK_IDEA = ('The moment that links two sections comes in the 4th bar of a phrase (in his example D minor, A7, A7, D minor). Over that bar: '
             'the tonic chord, the key’s 5th alone, then two notes at a time in contrary motion into the new section’s first chord. '
             'One voice falls by semitones from the 5th to the new tonic’s 3rd; the other climbs from the 6th through the leading note to the root.')
ex('entre', 'enlace-menor-menor-a', 'Minor section into a minor section',
   LINK_IDEA + ' Here the falling voice is below.',
   Q(35, 'Posibles cadenciales, 1: Sección A en tonalidad menor, sección B en tonalidad menor: on D minor, the chord, then A, then the two lines into D minor. Played here: the chord and the A.',
     [K('Dm', [-1, 5, 7, 7, 6, -1], [(1, 'A')]), ['R', [[3, 2]], [1], '=A|his notes']]),
   link_bars('enlace-menor-menor-a', OCHI, 'A', 'minor', 'minor', 'a', G4['Am'], 'in A minor, the key of all its sections', maxf=8))
ex('entre', 'enlace-menor-menor-b', 'Minor into minor, the voices turned over',
   'The other voicing: the climbing voice below (from the major 6th, the melodic minor’s), the falling voice above.',
   Q(35, 'The second way: the same chord and A, then the climbing voice under the falling one. Played here: the chord and the A.',
     [K('Dm', [-1, 5, 7, 7, 6, -1], [(1, 'A')]), ['R', [[3, 2]], [1], '=A|his notes']]),
   link_bars('enlace-menor-menor-b', OCHI, 'A', 'minor', 'minor', 'b', GR['ochi']['Am_o'], 'in A minor'))
ex('entre', 'enlace-menor-mayor-a', 'Minor section into a major section',
   'When the new section is in the major key of the same name: the same line, the falling voice landing a semitone higher, on the major 3rd.',
   Q(35, 'Sección A en tonalidad menor, sección B en tonalidad mayor: from D minor into D. Played here: the chord and the A.',
     [K('Dm', [-1, 5, 7, 7, 6, -1], [(1, 'A')]), ['R', [[3, 2]], [1], '=A|his notes']]),
   link_bars('enlace-menor-mayor-a', IW, 'F', 'minor', 'major', 'a', GR['iw']['Fm'], 'F minor into F major, the turn the song itself makes in bar 26', near=8))
ex('entre', 'enlace-menor-mayor-b', 'Minor into major, the voices turned over',
   'The same with the climbing voice below.',
   Q(36, 'The second way, into D. Played here: the chord and the A.',
     [K('Dm', [-1, 5, 7, 7, 6, -1], [(1, 'A')]), ['R', [[3, 2]], [1], '=A|his notes']]),
   link_bars('enlace-menor-mayor-b', IW, 'F', 'minor', 'major', 'b', GR['iw']['Fm'], 'F minor into F major', near=8))
ex('entre', 'enlace-mayor-menor-a', 'Major section into a minor section',
   'From a major section into one in the minor of the same name: the climbing voice starts from the major key’s own 6th.',
   Q(36, 'Sección A en tonalidad mayor, sección B en tonalidad menor: from D into D minor. Played here: the chord and the A.',
     [K('D', [-1, 5, 7, 7, 7, -1], [(1, 'A')]), ['R', [[3, 2]], [1], '=A|his notes']]),
   link_bars('enlace-mayor-menor-a', GLI, 'Eb', 'major', 'minor', 'a', GR['gli']['Eb'], 'E♭ into E♭ minor, as the song turns in its third stanza', near=6))
ex('entre', 'enlace-mayor-menor-b', 'Major into minor, the voices turned over',
   'The same with the climbing voice below.',
   Q(36, 'The second way, into D minor. Played here: the chord and the A.',
     [K('D', [-1, 5, 7, 7, 7, -1], [(1, 'A')]), ['R', [[3, 2]], [1], '=A|his notes']]),
   link_bars('enlace-mayor-menor-b', GLI, 'Eb', 'major', 'minor', 'b', GR['gli']['Eb'], 'E♭ into E♭ minor', near=6))


# ================================================================ placing chords: a bass and voices that move least
def voicing_cands(pcs, bass, need, n_up=3, lo_gap=3, span=19, top_max=76):
    """uppers: n_up notes of the chord above the bass (each pitch class once, `need` among them), within `span` of the bass"""
    out = []
    pool = [p for p in set(pcs) if p != bass % 12] if len(set(pcs)) > n_up else list(set(pcs))
    for combo in combinations(sorted(set(pool)), n_up):
        if not set(need) <= set(combo): continue
        opts = []
        for p in combo:
            opts.append([m for m in range(bass + lo_gap, bass + span + 1) if m % 12 == p and m <= top_max])
        for pick in product(*opts):
            ms = sorted(pick)
            if len(set(ms)) < n_up or ms[-1] - bass > span: continue
            out.append(ms)
    return out


def voice_chords(chords, near, n_up=3, allow_open=False, maxf=12, bass_strings=(6, 5), first_grip=None):
    """chords: [(pitch classes, bass midi, needed pitch classes)]: the voicing of each (bass + uppers) and its grip, the
    upper voices moving as little as they can from chord to chord, every chord playable, near the hand"""
    layers = []
    for k, (pcs, bass, need) in enumerate(chords):
        cur = {}
        if k == 0 and first_grip:                                     # the song's own grip to start from
            ms = sorted(gnotes(first_grip)); assert ms[0] == bass, (ms, bass)
            layers.append({(tuple(ms[1:]), tuple(first_grip)): (0.0, None, first_grip)}); continue
        for ups in voicing_cands(pcs, bass, need, n_up):
            ms = [bass] + ups
            for g in grips_all(ms, allow_open=allow_open, maxf=maxf, bass_strings=bass_strings):
                pos = gpos(g)
                key = (tuple(ups), tuple(g))
                gaps = 0.3 * sum(1 for i in range(6) if g[i] < 0 and any(g[j] >= 0 for j in range(i)) and any(g[j] >= 0 for j in range(i + 1, 6)))
                if k == 0:
                    cur[key] = (0.5 * abs(pos - near) + gaps, None, g); continue
                best = None
                for prev, (c0, _, g0) in layers[-1].items():
                    c = c0 + sum(abs(a - b) for a, b in zip(prev[0], ups)) + 0.5 * abs(pos - gpos(g0)) + gaps
                    if best is None or c < best[0]: best = (c, prev, g)
                cur[key] = best
        assert cur, ('no voicing', chords[k])
        layers.append(cur)
    k = min(layers[-1], key=lambda x: layers[-1][x][0])
    path = [k]
    for i in range(len(layers) - 1, 0, -1):
        k = layers[i][k][1]; path.append(k)
    path.reverse()
    return [([chords[i][1]] + list(key[0]), list(key[1])) for i, key in enumerate(path)]


def pcs_of(name):
    p, r = chord_pcs(name)
    return p


def root_pc(name): return chord_pcs(name)[1]


def need_of(name):
    """the notes a voicing must keep: a 7th chord its 3rd and 7th; a triad all three; a diminished 7th any three"""
    p, r = chord_pcs(name)
    base = name.split('/')[0]
    if base.endswith('dim7'): return []
    if base.endswith('maj7'): return [(r + 4) % 12, (r + 11) % 12]
    if base.endswith('7'): return [(r + 4) % 12, (r + 10) % 12]
    return [x for x in p if x != r] if '/' in name else p


def bass_at(pc, lo=40, hi=55):
    """the bass note of a pitch class on the low strings"""
    return next(m for m in range(lo, hi + 1) if m % 12 == pc)


def NM(pc, flats=True): return nn(pc + 48, sharp=not flats)[:-1]


# ================================================================ ♭VI7–V7 (p. 36)
def bvi7(song, key, grips, dom_grip):
    """p. 36: the dominant reached from the 7th chord a semitone above it (the ♭VI7 of a minor key): the tonic two beats,
    ♭VI7, V7, then the tonic, minor or major. Graciano writes slashes; the ♭VI7 here is the dominant's own grip a fret higher."""
    t = key + 'm'
    vr = M.pc_name(up(key + '4', 4, 7)); br = M.pc_name(up(key + '4', 5, 8))
    V, bVI = vr + '7', br + '7'
    g6 = [f + 1 if f >= 0 else -1 for f in dom_grip]
    LOG.append(dict(device='bvi7', ex=None, ctx=dict(key=key), chords=[(t, grips[t]), (bVI, g6), (V, dom_grip), (t, grips[t])]))
    return t, V, bVI, g6


def bvi7_bars(exid, song, key, grips, where_txt):
    t, V, bVI, g6 = bvi7(song, key, grips, grips[key_dom(key)])
    LOG[-1]['ex'] = exid
    gV = grips[key_dom(key)]
    return [bar([sym(t), sym(bVI), sym(V)], [K(sym(t), grips[t], [(1, 'A'), (1, 'A')]), K(sym(bVI), g6, [(1, 'A')]), K(sym(V), gV, [(1, 'A')])],
                f'{song}, {where_txt}: {dn(t)}, {dn(bVI)}, {dn(V)}. {dn(bVI)} is the {dn(V)} grip one fret higher, so the hand slides down a fret into {dn(V)}.'),
            bar([sym(t)], [K(sym(t), grips[t], [(2, 'A'), (2, '-')])], f'Into {dn(t)} (or its major).')]


def key_dom(key): return M.pc_name(up(key + '4', 4, 7)) + '7'


ex('entre', 'cadencia-bVI7-V7', 'The ♭VI7 before the dominant',
   'The dominant reached through the 7th chord on the minor key’s 6th degree, a semitone above it; then the tonic, minor or major.',
   Q(36, 'Cadencia ♭VI7–V7: D minor two beats, B♭7, A7; then D minor or D. Slashes only. Played here: the D minor.',
     [K('Dm', [-1, 5, 7, 7, 6, -1], [(2, 'A')])]),
   bvi7_bars('cadencia-bVI7-V7', OCHI, 'A', GR['ochi'], 'as your arrangement has it in its second verse (bar 51)')
   + bvi7_bars('cadencia-bVI7-V7', IW, 'F', dict(GR['iw'], Fm=GR['iw']['Fm']), 'in its F minor'))


# ================================================================ triads over the tonic in the bass (p. 36)
def pedal(key, bass_open, near=3):
    """p. 36: over the minor tonic held in the bass, major triads on the key's ♭3rd, 2nd and ♭2nd degrees, falling by
    semitones, one shape sliding down; then the tonic. Graciano: pick a key whose tonic is an open string."""
    k = M.midi(key + '4') % 12
    roots = [(k + 3) % 12, (k + 2) % 12, (k + 1) % 12]
    best = None
    for inv in range(3):
        sh = []
        ok = True
        for r in roots:
            tri = [(r + x) % 12 for x in (0, 4, 7)]
            order = tri[inv:] + tri[:inv]
            ms = []
            lo = 55
            for p in order:
                m = next(x for x in range(lo, lo + 13) if x % 12 == p); ms.append(m); lo = m + 1
            fr = [m - OPEN[s] for m, s in zip(ms, (3, 2, 1))]
            if any(f < 1 or f > 12 for f in fr) or max(fr) - min(fr) > 3: ok = False; break
            sh.append((ms, fr))
        if ok:
            c = abs(sum(sh[0][1]) / 3 - near)
            if best is None or c < best[0]: best = (c, sh)
    assert best, key
    sh = best[1]
    tonic = [(k + x) % 12 for x in (0, 3, 7)]
    end = None
    for inv in range(3):
        order = tonic[inv:] + tonic[:inv]
        ms, lo = [], 55
        for p in order:
            m = next(x for x in range(lo, lo + 13) if x % 12 == p); ms.append(m); lo = m + 1
        fr = [m - OPEN[s] for m, s in zip(ms, (3, 2, 1))]
        if all(0 <= f <= 12 for f in fr) and max(fr) - min(f for f in fr if f > 0 or True) <= 4:
            c = sum(abs(a - b) for a, b in zip(ms, sh[-1][0]))
            if end is None or c < end[0]: end = (c, ms, fr)
    names = [M.pc_name(up(key + '4', a, b)) + '/' + key for a, b in ((2, 3), (1, 2), (1, 1))]     # ♭III, II, ♭II spelled from the key
    grips = []
    bs = {40: 6, 45: 5, 50: 4}[bass_open]
    for ms, fr in [(m, f) for m, f in sh] + [(end[1], end[2])]:
        g = [-1] * 6; g[6 - bs] = 0
        for s, f in zip((3, 2, 1), fr): g[6 - s] = f
        grips.append(g)
    LOG.append(dict(device='pedal', ex=None, ctx=dict(key=key, bass=bass_open), chords=[(n, g) for n, g in zip(names + [key + 'm'], grips)]))
    return names, grips


def pedal_bars(exid, song, key, bass_open, where_txt):
    names, grips = pedal(key, bass_open)
    LOG[-1]['ex'] = exid
    bs = {40: 6, 45: 5, 50: 4}[bass_open]
    first = [K(sym(key + 'm'), grips[-1], [(1, 'A')])] + [K(sym(n), g, [(1, 'A')]) for n, g in zip(names, grips[:3])]
    return [bar([sym(key + 'm')] + [pname(n) for n in names], first,
                f'{song}, {where_txt}: the open {STR[bs]} is the bass under {dn(key + "m")}, then ' + ', '.join(pname(n.split('/')[0]) for n in names)
                + ' on the top three strings, the same shape sliding down a fret at a time.'),
            bar([sym(key + 'm')], [K(sym(key + 'm'), grips[-1], [(2, 'A'), (2, '-')])], f'Into {dn(key + "m")} over the open string.')]


ex('entre', 'cadencia-pedal', 'Triads over the tonic in the bass',
   ('Over the minor tonic held in the bass, major triads falling by semitones: on the key’s ♭3rd, its 2nd and its ♭2nd (on D: F, E, E♭), into the tonic, minor or major. '
    'Graciano: choose a key where the bass can be an open string, with the triad above it.'),
   Q(36, 'Cadencia ♭III–III–♭II sobre bajo pedal de tónica: D minor, F over D, E over D, E♭ over D, on the open D string; then D minor. Played here: the first two chords.',
     [K('Dm', [-1, -1, 0, 7, 6, 5], [(1, 'A')]), K('F/D', [-1, -1, 0, 10, 10, 8], [(1, 'A')])]),
   pedal_bars('cadencia-pedal', OCHI, 'A', 45, 'in A minor')
   + pedal_bars('cadencia-pedal', YVL, 'E', 40, 'its E minor (the pre-chorus)'))


# ================================================================ from the major tonic to the dominant of its relative minor (pp. 36–37)
def i_to_v_vi(key, way, near):
    """pp. 36–37, four ways from the major tonic to the dominant of its 6th degree (the relative minor's dominant):
    a: the bass falls by step from the tonic to that dominant's 3rd, through diminished 7ths on the key's 7th and 6th;
    b: the bass climbs by semitones from the 2nd, diminished 7ths on the 2nd and sharp 2nd, to the dominant's root;
    c: the same climb with dominant 7ths of one shape on the 2nd and sharp 2nd;
    d: from the major 7th chord over its 5th, the bass climbs by semitones (6th, ♭7th as diminished 7ths) to the dominant's 5th.
    Two beats of the tonic, a beat each of the two chords between, then the dominant."""
    T = M.midi(key + '4') % 12
    D = (T + 4) % 12                                                   # the relative minor's dominant (G in E♭)
    Dn = M.pc_name(up(key + '4', 2, 4))
    if way == 'a':
        seq = [(key, T), (key, T), (M.pc_name(up(key + '4', 6, 11)) + 'dim7', (T + 11) % 12), (M.pc_name(up(key + '4', 5, 9)) + 'dim7', (T + 9) % 12),
               (Dn, (D + 4) % 12)]
        names = [key, key, seq[2][0], seq[3][0], Dn + '/' + M.pc_name(up(Dn + '4', 2, 4))]
    elif way == 'b':
        seq = [(key, T), (key, T), (M.pc_name(up(key + '4', 1, 2)) + 'dim7', (T + 2) % 12), (M.pc_name(up(key + '4', 1, 3)) + 'dim7', (T + 3) % 12), (Dn + '7', D)]
        names = [s_[0] for s_ in seq]
    elif way == 'c':
        seq = [(key, T), (key, T), (M.pc_name(up(key + '4', 1, 2)) + '7', (T + 2) % 12), (M.pc_name(up(key + '4', 2, 3)) + '7', (T + 3) % 12), (Dn + '7', D)]
        names = [s_[0] for s_ in seq]
    else:
        seq = [(key + 'maj7', T), (key + 'maj7', (T + 7) % 12), (M.pc_name(up(key + '4', 5, 9)) + 'dim7', (T + 9) % 12),
               (M.pc_name(up(key + '4', 6, 10)) + 'dim7', (T + 10) % 12), (Dn + '7', (D + 7) % 12)]
        names = [key + 'maj7', key + 'maj7/' + M.pc_name(up(key + '4', 4, 7)), seq[2][0], seq[3][0], Dn + '7/' + M.pc_name(up(Dn + '4', 4, 7))]
    # the bass: the first on the low strings, then each the nearest note of its pitch class (the line moves by step)
    basses = []
    for k, (nm, bpc) in enumerate(seq):
        if k == 0: b = bass_at(bpc, 43, 55)
        else:
            prev = basses[-1]
            b = min((m for m in range(prev - 6, prev + 7) if m % 12 == bpc), key=lambda m: abs(m - prev))
        basses.append(b)
    chords = []
    for (nm, bpc), b in zip(seq, basses):
        pcs = pcs_of(nm)
        need = need_of(nm)
        if way == 'a' and nm == Dn: need = pcs_of(nm)                    # his last chord: the dominant's triad, without its 7th
        chords.append((pcs, b, need))
    vs = voice_chords(chords, near, first_grip=GR['iw'][key] if way != 'd' and key in GR['iw'] else None)
    LOG.append(dict(device='i-v/vi', ex=None, ctx=dict(key=key, way=way), names=names, chords=[(ms, g) for ms, g in vs]))
    return names, vs


IVV_TXT = {'a': 'the bass falls by step from the tonic to the dominant’s 3rd, through two diminished 7ths',
           'b': 'the bass climbs by semitones through two diminished 7ths to the dominant',
           'c': 'the bass climbs through two dominant 7ths of the same shape, a semitone apart',
           'd': 'from the major 7th over its 5th, the bass climbs by semitones to the dominant’s 5th'}
IVV_Q = {'a': ('C, C, B°7, A°7, E7', [['C3', 'G3', 'C4', 'E4']] * 2), 'b': ('C, C, D°7, D♯°7, E7', [['C3', 'G3', 'C4', 'E4']] * 2),
         'c': ('C, C, D7, E♭7, E7', [['C3', 'G3', 'C4', 'E4']] * 2), 'd': ('Cmaj7, Cmaj7 over G, A°7, B♭°7, E7 over B', [['C3', 'G3', 'B3', 'E4'], ['G2', 'G3', 'B3', 'E4']])}
for w, page in (('a', 36), ('b', 37), ('c', 37), ('d', 37)):
    names, vs = i_to_v_vi('Eb', w, 6)
    LOG[-1]['ex'] = f'cadencia-I-V7-VIm-{w}'
    hows = [st(1, 'A')] * 4 if w in 'ab' else [[(1, 'A')]] * 4
    its = [K(sym(n), g, h) for n, (ms, g), h in zip(names[:4], vs[:4], hows)]
    ms_txt = '; '.join(f'{pname(n)}: ' + ', '.join(tone_name(m, n) for m in ms) for k, (n, (ms, g)) in enumerate(zip(names, vs)) if k == 0 or n != names[k - 1])
    qd = IVV_Q[w]
    ex('entre', f'cadencia-I-V7-VIm-{w}', 'From the major tonic to the dominant of its relative minor' + ('' if w == 'a' else f' ({"second third fourth".split()["bcd".index(w)]} way)'),
       ('In a major key, from the tonic to the dominant of its 6th degree (the relative minor), ' + IVV_TXT[w] + '.') if w == 'a' else IVV_TXT[w][0].upper() + IVV_TXT[w][1:] + '.',
       Q(page, f'Cadencia del I al V7/VIm: {qd[0]}. Played here: the first two chords.',
         [K('Cmaj7' if w == 'd' and i == 0 else 'Cmaj7/G' if w == 'd' else 'C', grip_of([M.midi(n) for n in ns], near=3, allow_open=True), st(1, 'A') if w in 'ab' else [(1, 'A')])
          for i, ns in enumerate(qd[1])]),
       [bar([sym(n) for n in names[:4]], its, f'{IW}, bars 5–6: E♭ goes to G (the dominant of C minor). ' + ms_txt + '.'),
        bar([sym(names[4])], [K(sym(names[4]), vs[4][1], [(2, 'A'), (2, '-')])], 'The dominant of C minor' + (' (as in his, without its 7th).' if w == 'a' else '.'))])


# ================================================================ from the minor tonic down to the dominant (p. 37)
def barre(root_midi, q, string):
    """a whole barre with its root on the low E string (E shape) or the A string (A shape)"""
    f = root_midi - OPEN[string]
    shapes = {(6, 'm'): [0, 2, 2, 0, 0, 0], (6, '7'): [0, 2, 0, 1, 0, 0], (6, ''): [0, 2, 2, 1, 0, 0],
              (5, 'm'): [-1, 0, 2, 2, 1, 0], (5, '7'): [-1, 0, 2, 0, 2, 0], (5, ''): [-1, 0, 2, 2, 2, 0]}
    return [x + f if x >= 0 else -1 for x in shapes[(string, q)]]


def im_to_v(key, string):
    """p. 37: from the minor tonic to the dominant by whole barres sliding down the neck: the bass falls from the root to
    the minor 7th, the minor 6th and the 5th, with dominant 7ths on the 7th and 6th. Tonic (accented), tonic, the two 7ths, all short; the dominant."""
    k = M.midi(key + '4') % 12
    r0 = next(m for m in range(OPEN[string] + 1, OPEN[string] + 13) if m % 12 == k)
    roots = [r0, r0, r0 - 2, r0 - 4, r0 - 5]
    qs = ['m', 'm', '7', '7', '7']
    grips = [barre(r, q, string) for r, q in zip(roots, qs)]
    names = [key + 'm', key + 'm'] + [M.pc_name(up(key + '4', a, b)) + '7' for a, b in ((6, 10), (5, 8), (4, 7))]
    LOG.append(dict(device='im-v', ex=None, ctx=dict(key=key, string=string), names=names, grips=grips))
    return names, grips


def im_v_bars(exid, song, key, string, where_txt):
    names, grips = im_to_v(key, string)
    LOG[-1]['ex'] = exid
    its = [K(sym(names[0]), grips[0], [(1, 'A', ACC)])] + [K(sym(n), g, st(1, 'A')) for n, g in zip(names[1:4], grips[1:4])]
    frets = [min(f for f in g if f >= 0) for g in grips]
    seen = [(n, f) for k, (n, f) in enumerate(zip(names[:4], frets)) if k == 0 or (n, f) != (names[k - 1], frets[k - 1])]
    return [bar([sym(n) for n in names[:4]], its, f'{song}, {where_txt}: ' + ', '.join(f'{pname(n)} as a barre at the {ordn(f)} fret' if f else f'{pname(n)} open'
                                                                                          for n, f in seen) + f', the bass on the {STR[string]}, falling a tone, a tone, a semitone.'),
            bar([sym(names[4])], [K(sym(names[4]), grips[4], [(2, 'A'), (2, '-')])], f'{pname(names[4])}' + (f' at the {ordn(frets[4])} fret.' if frets[4] else ' in open position.'))]


ex('entre', 'cadencia-Im-V7', 'From the minor tonic down to the dominant',
   'Whole barres sliding down the neck from the minor tonic to the dominant: the bass falls from the root to the minor 7th, the minor 6th and the 5th, with dominant 7ths on the key’s 7th and 6th degrees.',
   Q(37, 'Cadencia del Im al V7: A minor (accented), A minor, G7, F7, E7, full six-string chords. Played here: the two A minors.',
     [K('Am', [5, 7, 7, 5, 5, 5], [(1, 'A', ACC)]), K('Am', [5, 7, 7, 5, 5, 5], st(1, 'A'))]),
   im_v_bars('cadencia-Im-V7', IW, 'F', 5, 'its F minor before C7 (bars 9–10)') + im_v_bars('cadencia-Im-V7', GLI, 'Eb', 5, 'the E♭ minor of its third stanza, before B♭7 (bars 28–29)'))


# ================================================================ into the end (pp. 37–39)
END_CTX = {'ochi': dict(song=OCHI, key='A', mode='minor', V='E7', I='Am', where='E7 into A minor, the last bars of each verse'),
           'iw': dict(song=IW, key='Eb', mode='major', V='Bb7', I='Eb', where='B♭7 into E♭, the last two bars of the chorus (30–31)')}
DIM6 = [0, 1, 2, 0, 2, 0]                     # the six-string diminished 7th, its root on the low E string


def dims_ending(c):
    """p. 37: the dominant, then diminished 7ths on the bass a semitone, a tone and a major 3rd above its root (the 6th
    string: the ♭6th, 6th and 7th of the key), into the tonic; then dominant and tonic again. Major or minor."""
    C = END_CTX[c]
    v = M.midi(C['V'][:-1] + '2')
    while v < 40: v += 12
    while v > 51: v -= 12
    V = barre(v, '7', 6)
    names = [C['V']]
    grips = [V]
    for d in (1, 2, 4):
        b = v + d; f = b - 40
        grips.append([f + x for x in DIM6])
        names.append(M.pc_name(up(C['V'][:-1] + '4', {1: 0, 2: 1, 4: 2}[d], d) if d != 1 else up(C['V'][:-1] + '4', 1, 1)) + 'dim7')
    t = v + 5
    I = barre(t, 'm' if C['mode'] == 'minor' else '', 6)
    LOG.append(dict(device='dims', ex=None, ctx=dict(c=c, key=C['key'], mode=C['mode']), names=names + [C['I'], C['V'], C['I']], grips=grips + [I, V, I]))
    return names, grips, I, V


def dims_bars(exid, c):
    C = END_CTX[c]
    names, grips, I, V = dims_ending(c)
    LOG[-1]['ex'] = exid
    fr = [g[0] for g in grips]
    return [bar([sym(n) for n in names], [K(sym(n), g, [(1, 'A')]) for n, g in zip(names, grips)],
                f'{C["song"]}, {C["where"]}: {pname(names[0])}' + (f' (a barre at the {ordn(fr[0])} fret)' if fr[0] else ' in open position') + ', then the diminished shape with its bass on the low E string at the '
                + ', '.join(ordn(f) for f in fr[1:]) + ' fret: ' + ', '.join(pname(n)[:-2] for n in names[1:]) + ' in the bass.'),
            bar([sym(C['I']), sym(C['V']), sym(C['I'])], [K(sym(C['I']), I, [(1, 'A')]), K(sym(C['V']), V, [(1, 'A')]), K(sym(C['I']), I, [(1, 'A'), (1, '-')])],
                f'{pname(C["I"])}, {pname(C["V"])}, {pname(C["I"])} to end, the tonic a barre at the {ordn(I[0])} fret.')]


def bass5_ending(c, near):
    """p. 38: the bass climbs the A string by semitones from the dominant's root to the leading note: the dominant 7th,
    the diminished 7th on the key's ♭6th, the dominant of the dominant over its 5th, the dominant over its 3rd; then the tonic."""
    C = END_CTX[c]
    vr = C['V'][:-1]
    v = M.midi(vr + '2')
    while v < 45: v += 12
    seq = [(C['V'], v), (M.pc_name(up(vr + '4', 1, 1)) + 'dim7', v + 1), (M.pc_name(up(vr + '4', 4, 7)) + '7/' + M.pc_name(up(vr + '4', 1, 2)), v + 2),
           (C['V'] + '/' + M.pc_name(up(vr + '4', 2, 4)), v + 4)]
    chords = []
    for nm, b in seq:
        base = nm.split('/')[0]
        need = need_of(base) if nm == base else [x for x in need_of(base) if x != b % 12] or [(root_pc(base) + 10) % 12]
        chords.append((pcs_of(base), b, need))
    vs = voice_chords(chords, near, bass_strings=(5,))
    t = v + 5
    land = [t, t + 12]
    LOG.append(dict(device='bass5', ex=None, ctx=dict(c=c, key=C['key'], mode=C['mode']), names=[n for n, b in seq], chords=vs, land=land))
    return seq, vs, land


def bass5_bars(exid, c):
    C = END_CTX[c]
    seq, vs, land = bass5_ending(c, 5 if c == 'iw' else 8)
    LOG[-1]['ex'] = exid
    lg = shape(land, near=gpos(vs[-1][1]), maxf=13)
    sp = lambda m: nd(spell(m, C['key'], C['mode'], 1))
    txt = '; '.join(f'{pname(n)}: ' + ', '.join(tone_name(m, n) for m in ms) for (n, b), (ms, g) in zip(seq, vs))
    return [bar([sym(n) for n, b in seq], [K(sym(n), g, [(1, 'A')]) for (n, b), (ms, g) in zip(seq, vs)],
                f'{C["song"]}, {C["where"]}: the bass up the A string, ' + ', '.join(sp(b) for n, b in seq) + '. ' + txt + '.'),
            bar([sym(C['I'])], [['P', [lg], [1], f'={sp(land[0])}+{sp(land[1])}|the tonic'], ['W', 3]],
                f'Into {pname(C["I"])}: its root in octaves on the {STR[lg[0][0]]} and the {STR[lg[1][0]]}.')]


def chrom_up(a, b):
    """the semitones from a up to b (b included), spelled climbing (sharps, or the plain letter)"""
    out = []
    for m in range(M.midi(a) + 1, M.midi(b) + 1):
        out.append(nn(m))
    out[-1] = b
    return out


def decariana(c):
    """p. 38: from the old guard, set down by Julio De Caro: from the dominant's root (the key's 5th) up by semitones to the
    tonic, the first note turned round its lower neighbour. The chord an eighth, the 5th a quarter, the neighbour and the
    5th two sixteenths, then four eighths up to the leading note; the tonic on the next downbeat."""
    C = END_CTX[c]
    tg = GR['ochi' if c == 'ochi' else 'iw'][C['I']]
    land = next(m for m in gnotes(tg) if m % 12 == M.midi(C['key'] + '4') % 12 and m >= 48)
    five = land - 5
    sp = lambda m: spell(m, C['key'], C['mode'])
    line = [sp(five), sp(five - 1), sp(five)] + [sp(m) for m in range(five + 1, land)] + [sp(land)]
    # one string: the landing grip's string for that note
    ls = next(6 - i for i in range(6) if tg[i] >= 0 and OPEN[6 - i] + tg[i] == land)
    pos = [(ls, M.midi(n) - OPEN[ls]) for n in line]
    assert all(0 <= f <= 12 for s, f in pos), pos
    LOG.append(dict(device='decariana', ex=None, ctx=dict(c=c, key=C['key']), line=line, pos=pos, durs=[1, 0.25, 0.25, 0.5, 0.5, 0.5, 0.5, 1]))
    return line, pos, tg


def deca_bars(exid, c):
    C = END_CTX[c]
    line, pos, tg = decariana(c)
    LOG[-1]['ex'] = exid
    vg = GR['ochi' if c == 'ochi' else 'iw'][C['V']]
    r = ['R', [list(p) for p in pos[:-1]], [1, 0.25, 0.25, 0.5, 0.5, 0.5, 0.5], '=' + ','.join(nd(n) for n in line[:-1]) + '|the line']
    return [bar([sym(C['V'])], [K(sym(C['V']), vg, [(0.5, 'A')]), r],
                f'{C["song"]}, {C["where"]}: {pname(C["V"])}, then ' + ', '.join(nd(n) for n in line[:-1]) + f', all on the {STR[pos[0][0]]}, '
                + ', '.join(ordn(f) for s, f in pos[:-1]) + (' fret.' if pos[1][1] else ' (the open string, then up the frets).')),
            bar([sym(C['I'])], [['R', [list(pos[-1])], [1], f'={nd(line[-1])}|the tonic'], K(sym(C['I']), tg, [(1, 'A'), (2, '-')])],
                f'{nd(line[-1])} on the {STR[pos[-1][0]]} ({ordn(pos[-1][1])} fret), the root of the {pname(C["I"])} grip that follows.')]


def doble(c):
    """p. 38: the decariana up high, and below it a second line falling by semitones from the dominant's root to the tonic's
    3rd (in a minor key the minor 3rd: Graciano's note), a rich counterpoint; then the dominant and the tonic."""
    C = END_CTX[c]
    k = M.midi(C['key'] + '4') % 12
    five_lo = next(m for m in range(43, 56) if m % 12 == (k + 7) % 12)
    five_hi = five_lo + 12
    third = (k + (3 if C['mode'] == 'minor' else 4)) % 12
    lows = [five_lo, five_lo, five_lo - 1, five_lo - 2]
    end_lo = max(m for m in range(five_lo - 6, five_lo) if m % 12 == third)
    ups = [five_hi, five_hi - 1, five_hi] + list(range(five_hi + 1, five_hi + 5))
    seq = [(lows[0], None, 0.5), (None, ups[0], 0.5), (lows[1], None, 0.5), (None, ups[1], 0.25), (None, ups[2], 0.25),
           (lows[2], ups[3], 0.5), (None, ups[4], 0.5), (lows[3], ups[5], 0.5), (None, ups[6], 0.5), (end_lo, five_hi + 5, 1)]
    steps = place_lines(seq, lo_strings=(6, 5, 4), up_strings=(1, 2, 3), maxf=12, prefer=6)
    LOG.append(dict(device='doble', ex=None, ctx=dict(c=c, key=C['key'], mode=C['mode']), seq=seq, steps=[[tuple(p) for p in g] for g, d in steps]))
    return seq, steps


def doble_bars(exid, c):
    C = END_CTX[c]
    seq, steps = doble(c)
    LOG[-1]['ex'] = exid
    sp = lambda m: nd(spell(m, C['key'], C['mode'], 1))
    names = ['+'.join(sp(m) for m in (lo, upn) if m is not None) for lo, upn, d in seq]
    g = GR['ochi' if c == 'ochi' else 'iw']
    first = ['P', [s for s, d in steps[:-1]], [d for s, d in steps[:-1]], '=' + ','.join(names[:-1]) + '|the two lines']
    land = ['P', [steps[-1][0]], [1], '=' + names[-1] + '|the two lines']
    up_line = [m for lo, m, d in seq if m is not None]; lo_line = [m for m, u, d in seq if m is not None]
    return [bar([sym(C['V'])], [first],
                f'{C["song"]}, {C["where"]}: the high line ' + ', '.join(sp(m) for m in up_line[:-1]) + '; the low line ' + ', '.join(nd(spell(m, C['key'], C['mode'], -1)) for m in lo_line[:-1]) + '.'),
            bar([sym(C['I']), sym(C['V']), sym(C['I'])], [land, K(sym(C['V']), g[C['V']], [(1, 'A')]), K(sym(C['I']), g[C['I']], st(1, 'A')), ['W', 1]],
                f'Into {pname(C["I"])} over its {"minor " if C["mode"] == "minor" else ""}3rd ({sp(lo_line[-1])} in the bass, {sp(up_line[-1])} on top), then {pname(C["V"])} and {pname(C["I"])}, short.')]


def octaves_end(c, decorated=False):
    """p. 38–39: the dominant's root climbing to the tonic in octaves: the 5th, sharp 5th, 6th and 7th (the major 6th and
    leading note in minor too), the octave on each beat and its top note again on the “and”; decorated: the top note’s
    lower neighbour a semitone down and back in two sixteenths in place of the repeat."""
    C = END_CTX[c]
    k = M.midi(C['key'] + '4') % 12
    tg = GR['ochi' if c == 'ochi' else 'iw'][C['I']]
    best = None
    for pair in ((4, 2), (5, 3), (3, 1), (6, 4)):
        for lo5 in range(40, 64):
            if lo5 % 12 != (k + 7) % 12: continue
            line = [lo5, lo5 + 1, lo5 + 2, lo5 + 4, lo5 + 5]
            fr = [(m - OPEN[pair[0]], m + 12 - OPEN[pair[1]]) for m in line]
            if not all(1 <= a <= 13 and 1 <= b <= 13 and 0 <= b - a <= 3 for a, b in fr): continue
            cst = abs((fr[4][0] + fr[4][1]) / 2 - gpos(tg))
            if best is None or cst < best[0]: best = (cst, pair, line, fr)
    assert best, c
    cst, pair, line, fr = best
    steps, durs = [], []
    for m, (a, b) in zip(line[:4], fr[:4]):
        steps.append([(pair[0], a), (pair[1], b)]); durs.append(0.5)
        if decorated:
            steps += [[(pair[1], b - 1)], [(pair[1], b)]]; durs += [0.25, 0.25]
        else:
            steps.append([(pair[1], b)]); durs.append(0.5)
    LOG.append(dict(device='octaves-end' + ('-dec' if decorated else ''), ex=None, ctx=dict(c=c, key=C['key']), line=line, steps=steps, durs=durs,
                    land=[(pair[0], fr[4][0]), (pair[1], fr[4][1])]))
    return line, steps, durs, [(pair[0], fr[4][0]), (pair[1], fr[4][1])], pair


def oct_end_bars(exid, c, decorated=False):
    C = END_CTX[c]
    line, steps, durs, land, pair = octaves_end(c, decorated)
    LOG[-1]['ex'] = exid
    sp = lambda m: nd(spell(m, C['key'], C['mode'], 1))
    names = []
    for g in steps:
        ms = sorted(OPEN[s] + f for s, f in g)
        names.append('+'.join(sp(m) for m in ms))
    return [bar([sym(C['V'])], [['P', [list(map(list, g)) for g in steps], durs, '=' + ','.join(names) + '|octaves']],
                f'{C["song"]}, {C["where"]}: ' + ', '.join(sp(m) for m in line[:4]) + f' in octaves on the {STR[pair[0]]} and {STR[pair[1]]} ('
                + ', '.join(f'{ordn(g[0][1])} and {ordn(g[1][1])}' for g in steps if len(g) == 2) + ')' + (', each top note with the note a fret below it.' if decorated else '.')),
            bar([sym(C['I'])], [['P', [[list(x) for x in land]], [1], f'={sp(line[4])}+{sp(line[4] + 12)}|octaves'], ['W', 3]],
                f'Into {pname(C["I"])}: the octave at the {ordn(land[0][1])} and {ordn(land[1][1])} fret.')]


PH3 = ('When the cadence leads to the end of a section or of the piece it comes in the 3rd bar of the phrase (in his example D minor, A7, A7, then D minor, A7, D minor). ')
ex('final', 'final-disminuidos', 'Chromatic diminished chords',
   PH3 + 'Here: the dominant, then diminished 7th chords climbing by semitones from it, the bass on the low E string, into the tonic. Graciano: it works in major and in minor.',
   Q(37, 'Cadencia con disminuidos cromáticos: A7, B♭°7, B°7, C♯°7, then D minor, A7, D minor, the bass on the 6th string, every chord on all six strings. Played here: A7 and B♭°7.',
     [K('A7', [5, 7, 5, 6, 5, 5], [(1, 'A')]), K('Bbdim7', [6, 7, 8, 6, 8, 6], [(1, 'A')])]),
   dims_bars('final-disminuidos', 'ochi') + dims_bars('final-disminuidos', 'iw'))
ex('final', 'final-V7-bVIdim', 'The bass climbs to the leading note',
   ('From the dominant 7th, through the diminished 7th on the key’s ♭6th, the dominant of the dominant over its 5th and the dominant over its 3rd: '
    'the bass on the A string climbs by semitones to the leading note, then the tonic. Major or minor.'),
   Q(38, 'Cadencia V7–♭VIdim–V/V–V/I, in F minor: C7, D♭°7, G7 over D, C7 over E, into F minor. Played here: C7 and D♭°7.',
     [K('C7', [-1, 3, 2, 3, 1, -1], [(1, 'A')]), K('Dbdim7', [-1, 4, 5, 3, 2, -1], [(1, 'A')])]),
   bass5_bars('final-V7-bVIdim', 'ochi') + bass5_bars('final-V7-bVIdim', 'iw'))
ex('final', 'final-decariana', 'The decariana',
   ('A line from the old guard, set down by Julio De Caro and played to this day: from the dominant’s root (the key’s 5th) up by semitones to the tonic, '
    'the first note turned round its lower neighbour. Major or minor.'),
   Q(38, 'Decariana: C7 an eighth, then C, a quarter. Played here: those two.',
     [K('C7', [-1, 3, 2, 3, 1, -1], [(0.5, 'A')]), ['R', [[5, 3]], [1], '=C|his notes']]),
   deca_bars('final-decariana', 'ochi') + deca_bars('final-decariana', 'iw'))
ex('final', 'final-doble-decariana', 'The double decariana',
   ('Graciano’s name for it: the decariana up high, and below it a second line falling by semitones from the dominant’s root, a rich counterpoint. '
    'His note: in a minor key the tonic’s bass goes to the minor 3rd.'),
   Q(38, 'Doble línea decariana: over C7, the low C on the beat, the high C on the “and”. Played here: that first beat.',
     [['P', [[[5, 3]], [[2, 1]]], [0.5, 0.5], '=C,C|his notes']]),
   doble_bars('final-doble-decariana', 'ochi') + doble_bars('final-doble-decariana', 'iw'))
ex('final', 'final-octavas', 'The line in octaves',
   'The dominant’s root climbing to the tonic in octaves (5th, sharp 5th, 6th, 7th): the octave on each beat, its top note again on the “and”. Major or minor.',
   Q(38, 'Por octavas: C in octaves, its top note again; then C♯, D, E the same way, into F. Played here: the first beat.',
     [['P', [[[5, 3], [3, 5]], [[3, 5]]], [0.5, 0.5], '=C+C,C|his notes']]),
   oct_end_bars('final-octavas', 'ochi') + oct_end_bars('final-octavas', 'iw'))
ex('final', 'final-octavas-adorno', 'The octaves, decorated',
   'The same octaves, each one decorated: the octave, then its top note’s lower neighbour a semitone down, and the note again, in sixteenths.',
   Q(39, 'Por octavas con embellecimiento: C in octaves, then B, C. Played here: the first beat.',
     [['P', [[[5, 3], [3, 5]], [[3, 4]], [[3, 5]]], [0.5, 0.25, 0.25], '=C+C,B,C|his notes']]),
   oct_end_bars('final-octavas-adorno', 'ochi', True) + oct_end_bars('final-octavas-adorno', 'iw', True))


def _labels():
    for sec in EXS.values():
        for e in sec:
            for it in e['quote'].get('items') or []:
                if it[0] in 'PR' and isinstance(it[3], str) and '|' not in it[3]: it[3] += '|his notes'


_labels()
SECTIONS = [dict(id='entre', title='Between two sections', part='Exercises', ex=EXS['entre']),
            dict(id='final', title='Into the end', part='Exercises', ex=EXS['final'])]

from quotes import trim as _trim_quotes   # quotes stay a beat or two
_trim_quotes(SECTIONS)
