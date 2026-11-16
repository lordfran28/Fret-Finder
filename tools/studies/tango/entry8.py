"""Tango walking bass with chords: Graciano, Método de guitarra tango, ch. 6 ("Bajo caminante combinado con acordes"),
pp. 51–55 of the owner's copy.

Graciano gives this chapter as rules: four rhythms for the chord over a bass in quarters, the chord voicings to use,
and the bass notes as degree formulas for each kind of chord (every 4 beats up or down, every 8 beats up then down,
every 2 beats the root then a chromatic approach), three special cases and the line cliché. Ours apply exactly those
rules to the chords of the owner's songs (I Wonder Who's Kissing Her Now in E♭, Очи чёрные in A minor, and once
I'll Be Seeing You in D♭, the only song of his with the move the first special case needs). Every bass note is built
from his formula for that chord (`deg`), and check8.py checks each one against the rule, the voicings, the beats and
the hand. His own examples are quoted by their first two notes or chords only; his example from a tango by Troilo is
described, not written out.

A bar is built from: the chords with their beats, the bass notes (each a quarter unless given), and the chord strikes
(beat, which chord, how long it rings). Strings and frets come from `place_bar`: the bass on the 6th and 5th strings
(the 4th only where the formula needs it), the chord's notes above it on the 4th to 2nd strings, one note per string,
and every held chord kept under the hand while the bass moves (four frets below the 7th, five from it up).
"""
import sys
from itertools import product, combinations
sys.path.insert(0, '/home/claude/studies'); sys.path.insert(0, '/home/claude/studies/tango')
from entry import K, marcatto4, ACC
import importlib.util as _ilu
_sp = _ilu.spec_from_file_location('fills5_for8', '/home/claude/studies/tango/entry5.py'); F5 = _ilu.module_from_spec(_sp); _sp.loader.exec_module(F5)
tr, midi, disp = F5.tr, F5.midi, F5.disp

OPEN = {6: 40, 5: 45, 4: 50, 3: 55, 2: 59, 1: 64}


def where(p): return f'Método de guitarra tango, p. {p}'


OWN = 'Graciano’s own'

# ---------------------------------------------------------------- degrees and formulas (pp. 53–54)
DEG = {'1': (0, 0), 'b2': (1, 1), '2': (1, 2), 'b3': (2, 3), '3': (2, 4), '4': (3, 5), '11': (3, 5), '#4': (3, 6), '#11': (3, 6),
       'b5': (4, 6), '5': (4, 7), '#5': (4, 8), 'b13': (5, 8), '6': (5, 9), 'bb7': (6, 9), 'b7': (6, 10), '7': (6, 11), '8': (7, 12)}


def deg(root, d):
    """a degree above a root note (with octave), spelled"""
    st, se = DEG[d]
    return tr(root, st, se)


FORM = {
    'asc': {'maj': '1 2 3 5', 'min': '1 2 b3 5', 'dom': '1 2 3 5', 'hd': '1 b2 b3 b5', 'dim': '1 2 b3 11', 'aug': '1 2 3 #11'},
    'desc': {'maj': '8 7 5 3', 'min': '8 b7 5 b3', 'dom': '8 b7 5 3', 'hd': '8 b7 b5 b3', 'dim': '8 7 bb7 b13', 'aug': '8 b7 #5 #4'},
    'eight': {'maj': '1 2 3 5 8 7 5 3', 'min': '1 2 b3 5 8 b7 5 b3', 'dom': '1 2 3 5 8 b7 5 3', 'hd': '1 b2 b3 b5 8 b7 b5 b3',
              'dim': '1 2 b3 4 b5 4 b3 2', 'aug': '1 2 3 #4 #5 #4 3 2'},
    'sp1': {'any': '1 b2 2 b3'}, 'sp2': {'any': '1 5 b5 3'}, 'sp3': {'any': '1 2 b3 3'}, 'cliche': {'any': '1 7 b7 6'},
    'r5': {'any': '1 5 1 5'}, 'arp': {'maj': '1 3 5 3', 'dom': '1 3 5 3', 'min': '1 b3 5 b3'},
    'arp7': {'maj': '1 3 5 7', 'dom': '1 3 5 b7', 'min': '1 b3 5 b7'},
}


def quality(name):
    n = name.split('/')[0]
    q = n[2:] if n[1:2] in ('b', '#') else n[1:]
    if q in ('', 'maj7', '6'): return 'maj'
    if q in ('m', 'm7', 'm6', 'm(maj7)'): return 'min'
    if q in ('7', '9', '7b9'): return 'dom'
    if q in ('m7b5',): return 'hd'
    if q in ('dim7',): return 'dim'
    if q in ('aug', '+'): return 'aug'
    raise ValueError(name)


def root_of(name, octave):
    n = name.split('/')[0]
    r = n[:2] if n[1:2] in ('b', '#') else n[:1]
    return r + str(octave)


def formula(kind, chord, root_note):
    q = 'any' if 'any' in FORM[kind] else quality(chord)
    ds = FORM[kind][q].split()
    if kind == 'desc':      # from the octave down: the degrees counted from the root below
        return [deg(root_note, d) for d in ds]
    if kind == 'eight':     # up from the root, then down from the octave (the diminished and augmented stay inside it)
        return [deg(root_note, d) for d in ds]
    if kind == 'sp2':       # 1, then the 5th below, the flat 5th, the 3rd (all under the root)
        return [root_note] + [tr(deg(root_note, d), -7, -12) for d in ds[1:]]
    if kind == 'r5':        # root and 5th, the 5th below the root here (where the 5th is above, the bar gives its notes)
        f = tr(deg(root_note, '5'), -7, -12)
        return [root_note, f, root_note, f]
    if kind == 'cliche':    # 1, then down by semitones: 7, b7, 6 under the root
        return [root_note] + [tr(deg(root_note, d), -7, -12) for d in ds[1:]]
    return [deg(root_note, d) for d in ds]


# the chord's notes over the bass (p. 52): root, 3rd and 7th for maj7, m7 and 7, the root left to the bass;
# the diminished as on the 5th string (flat 5th, double-flat 7th), the half-diminished complete, the augmented its 3rd and #5
UPPER = {'maj': ['3', '7'], 'min': ['b3', 'b7'], 'dom': ['3', 'b7'], 'hd': ['b3', 'b5', 'b7'], 'dim': ['b5', 'bb7'], 'aug': ['3', '#5']}
UPPER_6 = {'maj': ['3', '6']}          # a plain major chord, where the song's chord is a 6


def upper(chord):
    q = quality(chord)
    n = chord.split('/')[0]
    ds = UPPER_6[q] if (q == 'maj' and n.endswith('6') and not n.endswith('m6')) else UPPER[q]
    return [deg(root_of(chord, 3), d) for d in ds]


# ---------------------------------------------------------------- placing a bar on the neck
def span_ok(frets):
    fz = [f for f in frets if f > 0]
    if not fz: return True
    lo, hi = min(fz), max(fz)
    return hi - lo <= (4 if lo >= 7 else 3)


def chord_options(names, lo_m=55, hi_m=72, strings=(4, 3, 2)):
    """every way to put the chord's upper notes (any octave between G3 and C5) on distinct strings 4–2, low to high"""
    pcs = [midi(n) % 12 for n in names]
    out = []
    for octs in product(*[[m for m in range(lo_m, hi_m + 1) if m % 12 == pc] for pc in pcs]):
        ms = sorted(octs)
        if len(set(ms)) < len(ms) or ms[-1] - ms[0] > 14: continue
        for ss in combinations(strings, len(ms)):          # strings high to low as numbers fall: 4,3,2
            ss = sorted(ss, reverse=True)
            fr = [m - OPEN[s] for m, s in zip(ms, ss)]
            if any(f < 1 or f > 13 for f in fr) or not span_ok(fr): continue
            out.append(list(zip(ss, fr)))
    return out


def bass_options(name, allow4=False):
    """the 6th and 5th strings; the 4th only when asked for, or when the note is too high for the other two"""
    m = midi(name)
    out = [(s, m - OPEN[s]) for s in (6, 5) if 0 <= m - OPEN[s] <= 12]
    if allow4 or not out:
        out += [(4, m - OPEN[4])] if 0 <= m - OPEN[4] <= 12 else []
    return out


def place_bar(bass, chords, strikes, near, allow4=()):
    """bass: [(note, beats)]; chords: [(name, beats, upper notes)]; strikes: [(beat, chord index, rings beats)].
    Returns the bass positions and each chord's positions: everything held fits the hand."""
    t, on = 0.0, []
    for n, d in bass: on.append((t, d)); t += d
    sounding = []          # per bass note: the chords ringing at its onset or struck while it sounds
    for (t0, d) in on:
        s = set()
        for (b, ci, ring) in strikes:
            if b - 1e-9 <= t0 < b + ring - 1e-9 or t0 - 1e-9 <= b < t0 + d - 1e-9: s.add(ci)
        sounding.append(s)
    best = None
    for lo_m, strs in ((55, (4, 3, 2)), (45, (5, 4, 3, 2))):      # lower, with the 5th string, only when nothing else fits
        copts = [chord_options(c[2], lo_m=lo_m, strings=strs) for c in chords]
        best = _search(bass, copts, sounding, near, allow4)
        if best: break
    assert best, ('nothing fits', bass, chords)
    return best[1], best[2]


def _search(bass, copts, sounding, near, allow4):
    best = None
    for cp in product(*copts):
        ccost = sum(abs(sum(f for s, f in p) / len(p) - near) for p in cp)
        if best and ccost >= best[0]: continue
        # bass: dynamic choice of string per note, given the chords sounding with it
        states = {None: (ccost, [])}
        for i, (n, d) in enumerate(bass):
            new = {}
            for opt in bass_options(n, allow4=i in allow4):
                s, f = opt
                ok = True
                for ci in sounding[i]:
                    if s in [x for x, _ in cp[ci]] or not span_ok([f] + [y for _, y in cp[ci]]): ok = False
                if not ok: continue
                for prev, (c0, path) in states.items():
                    c = c0 + (abs(f - prev[1]) if prev and f > 0 and prev[1] > 0 else 0) + 0.3 * abs(f - near) * (f > 0)
                    if opt not in new or c < new[opt][0]: new[opt] = (c, path + [opt])
            states = new
            if not states: break
        if not states: continue
        c, path = min(states.values(), key=lambda x: x[0])
        if best is None or c < best[0]: best = (c, path, cp)
    return best


def build_bar(bass, chords, strikes, near=5, allow4=(), stop=True, label='the bass'):
    """the items of one bar: a stroke (K) wherever the chord is struck, with the bass note under it; the other bass
    notes as a numbered line (R) that stops each note as the next one comes."""
    bpos, cpos = place_bar(bass, chords, strikes, near, allow4)
    t, ons = 0.0, []
    for (n, d), p in zip(bass, bpos): ons.append((t, d, n, p)); t += d
    assert abs(t - 4) < 1e-9, ('bar is not 4 beats', t)
    items, run = [], []

    def flush():
        if run:
            items.append(['R', [list(p) for _, _, _, p in run], [d for _, d, _, _ in run],
                          '=' + ','.join(disp(n) for _, _, n, _ in run) + '|' + label, {'stop': True}])
            run.clear()
    for (t0, d, n, p) in ons:
        hits_here = [(b, ci, ring) for (b, ci, ring) in strikes if t0 - 1e-9 <= b < t0 + d - 1e-9]
        if not hits_here:
            run.append((t0, d, n, p)); continue
        flush()
        (b, ci, ring) = hits_here[0]
        name, _, ups = chords[ci]
        g = [-1] * 6; g[6 - p[0]] = p[1]
        for s, f in cpos[ci]: g[6 - s] = f
        cs = [s for s, f in cpos[ci]]
        rb = root_of(name, 3)[:-1]
        nm = name if disp(n) == disp(rb + '3') else f'{name}/{n[:-1]}'
        if b - t0 < 1e-9:
            hits = [(d, [p[0]] + cs)]
        else:
            hits = [(b - t0, [p[0]]), (t0 + d - b, cs)]
        it = K(nm, g, hits)
        if ring > (t0 + d - b) + 1e-9: it.append({'hold': ring, 'strings': cs})
        items.append(it)
    flush()
    return items


# ---------------------------------------------------------------- a bar from a few words
def walk(chords, bass, strikes, near=5, allow4=(), note=''):
    """chords: [(name, beats)]; bass: [(kind, chord, root note) or (note, beats)]; strikes: [(beat, chord index, rings)]"""
    ch = [(n, b, upper(n)) for n, b in chords]
    notes = []
    for x in bass:
        if len(x) == 3:
            kind, c, r = x
            ns = formula(kind, c, r)
            notes += [(n, 1.0) for n in ns]
            RULES.append((kind, c, r, ns))
        else:
            notes.append(x)
    return dict(chords=[n for n, _ in chords], items=build_bar(notes, ch, strikes, near, allow4), note=note, ch=ch, bass=notes, strikes=strikes)


RULES = []          # (formula, chord, root, notes): what check8.py checks
EXS = {}


def ex(sec, id, title, idea, quote, bars):
    EXS.setdefault(sec, []).append(dict(id=id, title=title, idea=idea, quote=quote, bars=bars))


def T(text, p, items=None):
    d = dict(where=where(p), text=text, whose=OWN, played='', by='Graciano')
    if items: d['items'] = items
    else: d['item'] = None
    return d


def his_line(names, strings=5):
    """his first notes (in C, sounding an octave below his treble clef), a quarter each"""
    pos = []
    for n in names:
        opts = [(s, midi(n) - OPEN[s]) for s in (6, 5, 4) if 0 <= midi(n) - OPEN[s] <= 12]
        pos.append(next(o for o in opts if o[0] == strings) if any(o[0] == strings for o in opts) else opts[0])
    return [['R', [list(p) for p in pos], [1.0] * len(names), '=' + ','.join(disp(n) for n in names) + '|his notes']]


IW = 'I Wonder Who’s Kissing Her Now'
H1 = [(0.5, 0, 3.5)]          # the chord on the "and" of 1, ringing to the end of the bar
SHORT1 = [(0.5, 0, 0.5)]      # the chord on the "and" of 1, an eighth

# ================================================================ rhythms for the chord over a marcatto bass (p. 51)
ex('ritmos', 'ritmo-a', 'Rhythm a: the chord held',
   ('The bass plays four quarters on the low strings (the 6th and 5th, the 4th only when it must); the chord comes in on the “and” of 1 and rings to the end of the bar. '
    'Graciano: for when the bass plays the chord’s root and 5th, or repeats the root.'),
   T('Patrón a: an eighth rest, then the chord held for the rest of the bar, over the bass in quarters.', 51),
   [walk([('Ebmaj7', 4)], [('r5', 'Ebmaj7', 'Eb3')], H1,
         note=f'{IW}, bars 1–2. E♭: the bass E♭, B♭, E♭, B♭ (root and 5th); above it G and D, the chord’s 3rd and 7th, from the “and” of 1.'),
    walk([('Bb7', 4)], [('Bb2', 1), ('F3', 1), ('Bb2', 1), ('F3', 1)], H1,
         note='B♭7: B♭ and F, the 5th above this time; A♭ and D above them.')])
RULES.append(('r5', 'Bb7', 'Bb2', ['Bb2', 'F3', 'Bb2', 'F3']))

ex('ritmos', 'ritmo-b', 'Rhythm b: the chord twice',
   ('The chord on the “and” of 1 and of 3, an eighth each. Graciano: ideal when the bass walks through the chord’s notes; the first chord sits on the root, '
    'the second on another note of the chord (an inversion).'),
   T('Patrón b: an eighth rest and an eighth of the chord, a quarter rest; the same again on beats 3 and 4.', 51),
   [walk([('Cm7', 4)], [('arp', 'Cm7', 'C3')], [(0.5, 0, 0.5), (2.5, 0, 0.5)],
         note=f'{IW}, bars 5–6. C minor 7: the bass C, E♭, G, E♭ through the chord; E♭ and B♭ above it on the “and” of 1 (over C) and of 3 (over G, the chord inverted).'),
    walk([('G7', 4)], [('arp', 'G7', 'G2')], [(0.5, 0, 0.5), (2.5, 0, 0.5)],
         note='G7: G, B, D, B; B and F above.')])

ex('ritmos', 'ritmo-c', 'Rhythm c: the chord once, short',
   'The chord once, an eighth on the “and” of 1, then the bass alone. Graciano: it goes with any bass.',
   T('Patrón c: an eighth rest, an eighth of the chord, then rests to the end of the bar.', 51),
   [walk([('Fm7', 4)], [('asc', 'Fm7', 'F2')], SHORT1, note=f'{IW}, bars 9–10. F minor 7: the bass climbs F, G, A♭, C (his formula for a minor chord); A♭ and E♭ above.'),
    walk([('C7', 4)], [('desc', 'C7', 'C2')], SHORT1, note='C7: the bass falls C, B♭, G, E (his formula down for a dominant), E a semitone under the next bar’s F.')])

ex('ritmos', 'ritmo-d', 'Rhythm d: the chord on the beat',
   ('The chord on beat 1 with the bass. Graciano: to let it ring the whole bar, the bass must play the root and 5th or repeat the root; more often the chord is struck on 1 '
    'and rings for one beat only, which leaves the bass free to walk through the chord.'),
   T('Patrón d: the chord as a half note on beat 1, the bass in four quarters under it.', 51),
   [walk([('F7', 4)], [('F2', 1), ('C3', 1), ('F2', 1), ('C3', 1)], [(0, 0, 4)], note=f'{IW}, bars 11–12. F7 held over the bass F, C, F, C: A and E♭ above.'),
    walk([('F7', 4)], [('arp7', 'F7', 'F2')], [(0, 0, 1)], note='F7 struck on 1 for a beat, then the bass walks F, A, C, E♭ through the chord.')])
RULES.append(('r5', 'F7', 'F2', ['F2', 'C3', 'F2', 'C3']))

# ================================================================ the voices for the chords (pp. 52–53)


def shell(name, beats, form):
    """a whole chord as Graciano gives it: root on the 5th string (root, 3rd, 7th upwards) or on the 6th (root, 7th, 3rd)"""
    q = quality(name)
    rs = next(root_of(name, o) for o in (2, 3) if 0 <= midi(root_of(name, o)) - OPEN[form] <= 12)
    up = {'maj': ['3', '7'], 'min': ['b3', 'b7'], 'dom': ['3', 'b7']}[q]
    if form == 5: notes = [rs, deg(rs, up[0]), deg(rs, up[1])]
    else: notes = [rs, deg(rs, up[1]), tr(deg(rs, up[0]), 7, 12)]
    g = [-1] * 6
    for n, s_ in zip(notes, [form, 4, 3]): g[6 - s_] = midi(n) - OPEN[s_]
    assert span_ok(g), (name, form, g)
    return K(name, g, [(beats, [form, 4, 3])]), notes


SH = []
VOX = [(['Cm7'], [6]), (['G7'], [6]), (['Abmaj7', 'C7'], [6, 5]), (['C7'], [5]), (['Fm7'], [6]), (['C7'], [5]), (['F7'], [6]), (['F7'], [6])]
vox_bars = []
for n, (cs, forms) in enumerate(VOX):
    its = []
    for c, f in zip(cs, forms):
        it, notes = shell(c, 4 / len(cs), f); its.append(it); SH.append((c, f, notes))
    vox_bars.append(dict(chords=cs, items=its, note=''))
vox_bars[0]['note'] = (f'{IW}, bars 5–12, every chord as three notes. Root on the 6th string: root, 7th, 3rd (C minor 7, G7, A♭maj7, F minor 7, F7). '
                       'Root on the 5th string: root, 3rd, 7th (C7). The hand stays between the 1st and 8th fret.')
ex('voces', 'voces-tres', 'Three notes: root, 3rd, 7th',
   'Graciano prefers chords in three parts for major 7, dominant 7 and minor 7: the root, the 3rd and the 7th. With the root on the 5th string they go root, 3rd, 7th upwards; on the 6th string root, 7th, 3rd.',
   T('Voces para los acordes: C major 7, C7 and C minor 7 in three notes, from the 5th string and from the 6th. Played here: his C major 7 both ways.', 52,
     [K('Cmaj7', [-1, 3, 2, 4, -1, -1], [(1, 'A')]), K('Cmaj7', [8, -1, 9, 9, -1, -1], [(1, 'A')])]),
   vox_bars)

DIM6 = [4, -1, 3, 4, -1, -1]          # G#2 F3 B3: root, double-flat 7th, flat 3rd (the 6th string)
DIM5 = [-1, 2, 3, 1, -1, -1]          # B2 F3 G#3: the same chord from B on the 5th string: root, flat 5th, double-flat 7th
AM7_6 = [5, -1, 5, 5, -1, -1]         # A2 G3 C4
ex('voces', 'voces-disminuido', 'The diminished chord in three notes',
   ('Diminished chords in three notes: with the root on the 5th string, the root, flat 5th and double-flat 7th; on the 6th string, the root, double-flat 7th and minor 3rd. '
    'A diminished 7th is the same chord from any of its four notes, so both shapes fit one chord.'),
   T('Disminuidos: C°7 as C, G♭, B𝄫 from the 5th string and C, B𝄫, E♭ from the 6th. Played here: both.', 52,
     [K('Cdim7', [-1, 3, 4, 2, -1, -1], [(1, 'A')]), K('Cdim7', [8, -1, 7, 8, -1, -1], [(1, 'A')])]),
   [dict(chords=['G#dim7', 'G#dim7/B'], items=[K('G#dim7', DIM6, [(2, 'A')]), K('G#dim7/B', DIM5, [(2, 'A')])],
         note='Очи чёрные’s E7 as G♯°7, the diminished on its 3rd (from Tango: harmony): G♯, F, B from the 6th string (4th fret); then the same chord from B on the 5th string, B, F, G♯ (2nd fret).'),
    dict(chords=['Am7'], items=[K('Am7', AM7_6, [(4, 'A')])], note='Into A minor 7, root on the 6th string: A, G, C.')])

HD6 = [1, 2, 1, 1, -1, -1]            # F2 B2(C♭) E♭3 A♭3
HD5 = [-1, 8, 9, 8, 9, -1]            # F3 B3(C♭) E♭4 A♭4
ex('voces', 'voces-semidisminuido', 'The half-diminished chord complete',
   'Graciano plays the half-diminished (minor 7 with flat 5th) complete, four notes, from the 5th string or the 6th.',
   T('Medio disminuidos: C minor 7 flat 5 complete, from the 5th string and from the 6th. Played here: both.', 52,
     [K('Cm7b5', [-1, 3, 4, 3, 4, -1], [(1, 'A')]), K('Cm7b5', [8, -1, 8, 8, 7, -1], [(1, 'A')])]),
   [dict(chords=['Fm7b5'], items=[K('Fm7b5', HD6, [(2, 'A')]), K('Fm7b5', HD5, [(2, 'A')])],
         note=f'{IW}, bar 9, as its own page darkens it (“Darker”: F half-diminished in place of F minor 7): F, C♭ (B on the neck), E♭, A♭ from the 6th string at the 1st fret, then from the 5th string at the 8th.'),
    dict(chords=['C7'], items=[shell('C7', 4, 5)[0]], note='On to C7, root on the 5th string.')])

AUG6 = [6, 5, 4, -1, -1, -1]          # B♭2 D3 F♯3
AUG5 = [-1, 1, 4, 3, 3, -1]           # B♭2 F♯3 B♭3 D4: the root doubled
EBM7_5 = [-1, 6, 5, 7, -1, -1]        # E♭3 G3 D4
ex('voces', 'voces-aumentado', 'The augmented chord',
   ('Augmented chords are rare in a tango’s own harmony, Graciano says, but a fine way to reharmonize a dominant: as a triad, usually with the root doubled when it is on the 5th string.'),
   T('Aumentados: C, E, G♯ with C again on top from the 5th string; C, E, G♯ from the 6th. Played here: both.', 53,
     [K('Caug', [-1, 3, 2, 1, 1, -1], [(1, 'A')]), K('Caug', [8, 7, 6, -1, -1, -1], [(1, 'A')])]),
   [dict(chords=['Bbaug'], items=[K('Bbaug', AUG6, [(2, 'A')]), K('Bbaug', AUG5, [(2, 'A')])],
         note=f'{IW}, bar 16, where the voice holds: B♭7 as B♭ augmented, B♭, D, F♯ from the 6th string (6th fret), then from the 5th string with B♭ doubled (1st–4th fret).'),
    dict(chords=['Ebmaj7'], items=[K('Ebmaj7', EBM7_5, [(4, 'A')])], note='Into E♭ (bar 17), the F♯ rising to G: E♭, G, D from the 5th string.')])

# ================================================================ notes for the marcatto bass (pp. 53–54)
ex('notas', 'cuatro-sube', 'Every 4 beats: up',
   ('When a chord lasts four beats, the bass climbs four of its notes, the formula set by the kind of chord: major and dominant 1, 2, 3, 5; minor 1, 2, ♭3, 5. '
    'The chord above, short, on the “and” of 1.'),
   T('Ritmo armónico cada 4 tiempos, ascenso: major 1 2 3 5, minor 1 2 ♭3 5, dominant 1 2 3 5, half-diminished 1 ♭2 ♭3 ♭5, diminished 1 2 ♭3 11, augmented 1 2 3 ♯11, all from C. Played here: C, D.',
     53, his_line(['C3', 'D3'])),
   [walk([('Fm7', 4)], [('asc', 'Fm7', 'F2')], SHORT1, note=f'{IW}, bars 9–12: F minor 7, F, G, A♭, C.'),
    walk([('C7', 4)], [('asc', 'C7', 'C3')], SHORT1, note='C7: C, D, E, G.'),
    walk([('F7', 4)], [('asc', 'F7', 'F2')], SHORT1, note='F7: F, G, A, C.'),
    walk([('F7', 4)], [('asc', 'F7', 'F2')], [(0.5, 0, 3.5)], note='F7 again, the chord held this time.')])
ex('notas', 'cuatro-baja', 'Every 4 beats: down',
   'Down from the octave: major 8, 7, 5, 3; minor 8, ♭7, 5, ♭3; dominant 8, ♭7, 5, 3.',
   T('Descenso: major 8 7 5 3, minor 8 ♭7 5 ♭3, dominant 8 ♭7 5 3, half-diminished 8 ♭7 ♭5 ♭3, diminished 8 7 𝄫7 ♭13, augmented 8 ♭7 ♯5 ♯4, from C. Played here: C, B.',
     53, his_line(['C4', 'B3'], strings=4)),
   [walk([('Fm7', 4)], [('desc', 'Fm7', 'F2')], SHORT1, note=f'{IW}, bars 9–12 again: F minor 7, F, E♭, C, A♭.'),
    walk([('C7', 4)], [('desc', 'C7', 'C2')], SHORT1, note='C7: C, B♭, G, E.'),
    walk([('F7', 4)], [('desc', 'F7', 'F2')], SHORT1, note='F7: F, E♭, C, A.'),
    walk([('F7', 4)], [('desc', 'F7', 'F2')], [(0.5, 0, 3.5)], note='F7, the chord held.')])
ex('notas', 'cuatro-otros', 'Every 4 beats: the other three kinds',
   ('The formulas for the half-diminished (up 1, ♭2, ♭3, ♭5; down 8, ♭7, ♭5, ♭3), the diminished (up 1, 2, ♭3, 11; down 8, 7, 𝄫7, ♭13) and the augmented '
    '(up 1, 2, 3, ♯11; down 8, ♭7, ♯5, ♯4), on the chords of those kinds from the pages above.'),
   T('The same table, for medio disminuido, disminuido and aumentado (p. 53).', 53),
   [walk([('Fm7b5', 4)], [('asc', 'Fm7b5', 'F2')], SHORT1, note=f'F half-diminished ({IW}, bar 9, darker): up, F, G♭, A♭, C♭ (B on the neck).'),
    walk([('Fm7b5', 4)], [('desc', 'Fm7b5', 'F2')], SHORT1, note='Down: F, E♭, C♭ (B), A♭.'),
    walk([('G#dim7', 4)], [('asc', 'G#dim7', 'G#2')], SHORT1, note='G♯°7 (Очи чёрные’s E7, as above): up, G♯, A♯, B, C♯.'),
    walk([('G#dim7', 4)], [('desc', 'G#dim7', 'G#2')], SHORT1, note='Down: G♯, G (his 7th), F, E.'),
    walk([('Bbaug', 4)], [('asc', 'Bbaug', 'Bb2')], SHORT1, note=f'B♭ augmented ({IW}, bar 16, as above): up, B♭, C, D, E.'),
    walk([('Bbaug', 4)], [('desc', 'Bbaug', 'Bb2')], SHORT1, note='Down: B♭, A♭, F♯, E.')])

OCHI2 = [('Dm7', 'D3'), ('Am7', 'A2'), ('E7', 'E2'), ('Am7', 'A2')]
eight_bars = []
for c, r in OCHI2:
    ns = formula('eight', c, r); RULES.append(('eight', c, r, ns))
    a4 = [i for i in range(4)] if c == 'Dm7' else ()
    for half in (0, 1):
        eight_bars.append(dict(chords=[c], items=build_bar([(n, 1.0) for n in ns[4 * half:4 * half + 4]], [(c, 4, upper(c))], SHORT1, near=6,
                                                           allow4=a4 if half == 1 else ()),
                               note='', ch=[(c, 4, upper(c))], bass=[(n, 1.0) for n in ns[4 * half:4 * half + 4]], strikes=SHORT1))
eight_bars[0]['note'] = ('Очи чёрные’s second half, each chord two bars: D minor 7 (D, E, F, A, then D, C, A, F, the octave on the 4th string, which Graciano allows when it must), '
                         'A minor 7 (A, B, C, E; A, G, E, C), E7 (E, F♯, G♯, B; E, D, B, G♯), A minor 7.')
ex('notas', 'ocho', 'Every 8 beats: up, then down',
   'When a chord lasts eight beats, the two joined: four notes up from the root, then four down from the octave.',
   T('Ritmo armónico cada 8 tiempos, ascenso y descenso combinados: major C, D, E, G, then C, B, G, E. Played here: C, D.', 54, his_line(['C3', 'D3'])),
   eight_bars)

ex('notas', 'dos', 'Every 2 beats: into the next root',
   ('When a chord lasts two beats: its root, then its 5th, flat 5th or sharp 5th, whichever is a semitone from the next chord’s root, as a chromatic approach to it; '
    'the plain 5th when neither is. Where a chord lasts a bar, his four-beat formulas.'),
   T('Ritmo armónico cada 2 tiempos: C then G (1, 5), C then G♭ (1, ♭5), C then G♯ (1, ♯5). Played here: C, G♭.', 54, his_line(['C3', 'Gb2'], strings=6)),
   [walk([('G7', 2), ('C7', 2)], [('G2', 1), ('Db3', 1), ('C3', 1), ('Gb2', 1)], [(0.5, 0, 0.5), (2.5, 1, 0.5)],
         note=f'{IW}, bars 23–26. G7, its root and flat 5th, D♭, a semitone above C; C7, root and flat 5th, G♭, a semitone above F.'),
    walk([('Fm7', 4)], [('asc', 'Fm7', 'F2')], SHORT1, note='F minor 7, a bar: up, F, G, A♭, C.'),
    walk([('Fm7', 2), ('Db9', 2)], [('F2', 1), ('C3', 1), ('Db3', 1), ('Ab2', 1)], [(0.5, 0, 0.5), (2.5, 1, 0.5)],
         note='F minor 7, root and 5th: C is already a semitone under D♭. D♭9, root and 5th: none of the three 5ths is next to C, so the plain one.'),
    walk([('Cm7', 4)], [('C3', 4)], [(0, 0, 4)], note='C minor 7, held.')])
RULES += [('two', 'G7', 'C7', ['G2', 'Db3']), ('two', 'C7', 'Fm7', ['C3', 'Gb2']), ('two', 'Fm7', 'Db9', ['F2', 'C3']), ('two', 'Db9', 'Cm7', ['Db3', 'Ab2'])]

# ================================================================ special cases and the line cliché (pp. 54–55)
ex('especiales', 'especial-1', 'Up by semitones to the 3rd',
   'Graciano’s first special case: 1, ♭2, 2, ♭3, a semitone at a time, into a chord whose root is a major 3rd above.',
   T('Patrón 1 - ♭2 - 2 - ♭3: C, D♭, D, E♭ into E7. Played here: C, D♭.', 54, his_line(['C3', 'Db3'])),
   [walk([('Dbmaj7', 4)], [('sp1', 'Dbmaj7', 'Db3')], H1, near=6,
         note='I’ll Be Seeing You, bars 11–12, where D♭ major 7 goes to F7, a major 3rd up: D♭, D, E♭, E up the A string under the chord held (F and C).'),
    walk([('F7', 4)], [('desc', 'F7', 'F2')], SHORT1, near=6, note='F7: down, F, E♭, C, A.')])
ex('especiales', 'especial-2', 'The 5th, the flat 5th, the 3rd',
   'The second: 1, the 5th below, the flat 5th, the 3rd, into the chord a 4th up (the dominant into its tonic).',
   T('Patrón 1 - 5 - ♭5 - ♯5 (under the notes: 1, 5, ♭5, 3): E, B, B♭, G♯ into A minor. Played here: E, B.', 54, his_line(['E3', 'B2'])),
   [walk([('C7', 4)], [('sp2', 'C7', 'C3')], SHORT1, note=f'{IW}, bars 28–29, where the voice holds: C7 into F minor, C, G, G♭, E, all on the low E and A strings.'),
    walk([('Fm7', 4)], [('asc', 'Fm7', 'F2')], SHORT1, note='F minor 7: up, F, G, A♭, C.')])
ex('especiales', 'especial-3', 'Up from the 2nd by semitones',
   'The third: 1, 2, ♭3, 3, into the chord a 4th up.',
   T('Patrón 1 - 2 - ♭3 - 3: G, A, B♭, B into C. Played here: G, A.', 54, his_line(['G2', 'A2'], strings=6)),
   [walk([('Bb7', 4)], [('sp3', 'Bb7', 'Bb2')], H1, note=f'{IW}, bars 16–17, where the voice holds: B♭7 into E♭, B♭, C, D♭, D, the chord held above.'),
    walk([('Ebmaj7', 4)], [('desc', 'Ebmaj7', 'Eb2')], SHORT1, note='E♭: down, E♭, D, B♭, G, the G the root of the next bar’s G7.')])
ex('especiales', 'cliche-bajo', 'The line cliché in the bass',
   'Under a minor chord the bass falls from the root by semitones, 1, 7, ♭7, 6, the chord held above it.',
   T('Línea cliché al bajo: on C minor, C, B, B♭, A; then A♭ (A♭7) and G (G7). Played here: C, B.', 55, his_line(['C3', 'B2'])),
   [walk([('Cm7', 4)], [('cliche', 'Cm7', 'C3')], H1, note=f'{IW}, bars 26–28: C minor 7, the bass C, B, B♭, A under E♭ and B♭ held.'),
    walk([('Gm7', 2), ('C7', 2)], [('G2', 1), ('Db3', 1), ('C3', 1), ('G2', 1)], [(0.5, 0, 0.5), (2.5, 1, 0.5)],
         note='Gm7 and C7, two beats each: G with its flat 5th, D♭, into C; C with its 5th.'),
    walk([('C7', 4)], [('desc', 'C7', 'C2')], SHORT1, note='C7, a bar: down, C, B♭, G, E, into F minor.')])
RULES += [('two', 'Gm7', 'C7', ['G2', 'Db3']), ('two', 'C7', 'C7', ['C3', 'G2'])]

# ================================================================ the walking bass in an accompaniment (p. 55)
GR = {'Fm7': [-1, 8, 10, 8, 9, 8], 'C7': [8, 10, 8, 9, 8, 8], 'F7': [-1, 8, 10, 8, 10, 8], 'Cm7': [8, 10, 8, 8, 8, 8], 'Eb': [-1, 6, 8, 8, 8, 6]}
et = [dict(chords=['Fm7'], items=[marcatto4('Fm7', GR['Fm7'])], note=''),
      dict(chords=['C7'], items=[marcatto4('C7', GR['C7'])], note=''),
      dict(chords=['F7'], items=[marcatto4('F7', GR['F7'])], note=''),
      walk([('F7', 4)], [('desc', 'F7', 'F2')], SHORT1, near=7, note='Bar 12, the voice holds: F7 walking down, F, E♭, C, A.'),
      dict(chords=['Cm7'], items=[marcatto4('Cm7', GR['Cm7'])], note=''),
      walk([('F7', 4)], [('asc', 'F7', 'F2')], SHORT1, near=4, note='Bar 14, the voice holds: F7 walking up, F, G, A, C.'),
      walk([('F7', 2), ('Bb7', 2)], [('F2', 1), ('B2', 1), ('Bb2', 1), ('F2', 1)], [(0.5, 0, 0.5), (2.5, 1, 0.5)], near=4,
           note='Bar 15, two beats each: F with its flat 5th, C♭ (B on the neck), a semitone above B♭; B♭ with its 5th.'),
      walk([('Bb7', 4)], [('sp3', 'Bb7', 'Bb2')], H1, near=5, note='Bar 16, the voice holds: B♭, C, D♭, D into E♭.'),
      dict(chords=['Eb'], items=[marcatto4('Eb', GR['Eb'])], note='E♭, marcatto.')]
RULES += [('two', 'F7', 'Bb7', ['F2', 'B2']), ('two', 'Bb7', 'Bb7', ['Bb2', 'F2'])]
et[0]['note'] = (f'{IW}, bars 9–17: the marcatto of chapter 1 (four short strokes, the 1st and 3rd accented), and the walking bass with the chord only in the bars '
                 'where the voice holds a note (12, 14, 16), as Graciano advises: a bar or two at a time, among the rhythms, bordoneos and fills.')
ex('aplicacion', 'aplicacion', 'In an accompaniment',
   ('Graciano shows the technique on the first eight bars of Aníbal Troilo’s tango La última curda, the bass resolving each chord as the harmony needs. '
    'It is not for playing alongside a double bass, he says, but a way to suggest one now and then when the guitar is in a duo or accompanies a singer, '
    'only for a bar or two at a time.'),
   T('Aplicación técnica del bajo caminante con acordes: Troilo’s La última curda, its first eight bars (not reproduced here).', 55),
   et)

SECTIONS = [dict(id='ritmos', title='The chord over a marcatto bass', part='Exercises', ex=EXS['ritmos']),
            dict(id='voces', title='The chords’ voices', part='Exercises', ex=EXS['voces']),
            dict(id='notas', title='The notes of the bass', part='Exercises', ex=EXS['notas']),
            dict(id='especiales', title='Special cases', part='Exercises', ex=EXS['especiales']),
            dict(id='aplicacion', title='The walking bass in a song', part='Études', ex=EXS['aplicacion'])]

sys.path.insert(0, '/home/claude/studies/tango')
from quotes import trim as _trim_quotes   # quotes stay a beat or two
_trim_quotes(SECTIONS)
