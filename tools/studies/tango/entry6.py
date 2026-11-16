"""Tango cadences: Graciano, Método de guitarra tango, ch. 4 ("Cadencial"), pp. 35–39 of the owner's copy.
The moment that links two sections, or leads to the end of a section or of the piece.

As in entry5, every cadence is kept twice: Graciano's own notes (sounding pitch) and ours, made by moving his whole
by one interval (letters and semitones together). Where he gives only chord names (slashes), ours are grips on
the same chords moved. Strings and frets are found by `place` (one note per string, the hand's stretch kept,
nearest the position asked for); check6.py proves the notes are his, moved, and the grips playable.
"""
import sys
from itertools import combinations
sys.path.insert(0, '/home/claude/studies'); sys.path.insert(0, '/home/claude/studies/tango')
from kit_study import OPEN
from entry import K, st, sincopado, G4, ACC
import importlib.util as _ilu
_sp = _ilu.spec_from_file_location('fills5', '/home/claude/studies/tango/entry5.py'); F5 = _ilu.module_from_spec(_sp); _sp.loader.exec_module(F5)
tr, midi, disp = F5.tr, F5.midi, F5.disp

DOWN_P4, UP_m3, UP_M3, SAME = (-3, -5), (2, 3), (2, 4), (0, 0)
MOVES = []


def tr_name(name, iv):
    """a chord name moved: its root and any bass, spelled by the same interval"""
    def one(r):
        n = tr(r + '4', *iv)
        return n[:-1]
    import re
    m = re.match(r'^([A-G][b#]?)(.*?)(?:/([A-G][b#]?))?$', name)
    out = one(m.group(1)) + m.group(2)
    if m.group(3): out += '/' + one(m.group(3))
    return out


def place(names, near, strings=None, bass=None, allow_open=False, gap_cost=1.0):
    """strings for the notes (lowest note on the lowest string): one note per string, the stretch kept
    (four frets below the 7th, five from it up), the hand nearest `near`."""
    ps = sorted(midi(n) for n in names)
    if strings:
        fr = [p - OPEN[6 - s] for p, s in zip(ps, sorted(strings, reverse=True))]
        assert all(0 <= f <= 15 for f in fr), (names, strings, fr)
        return sorted(strings, reverse=True), fr
    best = None
    for combo in combinations([6, 5, 4, 3, 2, 1], len(ps)):
        fr = [p - OPEN[6 - s] for p, s in zip(ps, combo)]
        if any(f < 0 or f > 15 for f in fr): continue
        if bass and combo[0] != bass: continue
        fz = [f for f in fr if f > 0]
        if fz:
            lo, hi = min(fz), max(fz)
            if hi - lo > (4 if lo >= 7 else 3): continue
            c = (lo + hi) / 2
        else:
            c = 0
        opens = sum(1 for f in fr if f == 0)
        if opens and not allow_open: continue
        cost = abs(c - near) + gap_cost * (combo[0] - combo[-1] + 1 - len(combo))
        if best is None or cost < best[0]: best = (cost, list(combo), fr)
    assert best, ('no place for', names, near)
    return best[1], best[2]


class Cad:
    """events: ('K', beats, notes, name, how) a chord struck ('s' short, '>' accented), ('N', beats, notes) one or two
    notes, ('W', beats) silence, ('KN', beats, name) a chord he gives by name only (slashes)."""

    def __init__(self, ev): self.ev = ev

    def moved(self, iv):
        out = []
        for e in self.ev:
            if e[0] == 'K': out.append(('K', e[1], [tr(n, *iv) for n in e[2]], tr_name(e[3], iv), e[4] if len(e) > 4 else ''))
            elif e[0] == 'N': out.append(('N', e[1], [tr(n, *iv) for n in e[2]]))
            elif e[0] == 'KN': out.append(('KN', e[1], tr_name(e[2], iv)))
            else: out.append(e)
        c = Cad(out); MOVES.append((self, c, iv[1])); return c

    def beats(self): return sum(e[1] for e in self.ev)

    def items(self, near, fix=None, label='', grips=None, k_opts=None, n_opts=None):
        """fix: {event index: strings}; grips: {name: grip} for chords given by name only"""
        fix = fix or {}; k_opts = k_opts or {}; n_opts = n_opts or {}
        out, steps, durs, names = [], [], [], []
        pos = near

        def flush():
            if steps:
                out.append(['P', [list(map(list, s)) for s in steps], list(durs), '=' + ','.join(names) + ('|' + label if label else '')])
                steps.clear(); durs.clear(); names.clear()
        for i, e in enumerate(self.ev):
            if e[0] == 'W':
                flush(); out.append(['W', e[1]]); continue
            if e[0] == 'KN':
                flush(); g = grips[e[2]]; out.append(K(e[2], g, [(e[1], 'A')])); continue
            if e[0] == 'K':
                flush()
                ss, fr = place(e[2], pos, fix.get(i), **k_opts.get(i, {}))
                g = [-1] * 6
                for s, f in zip(ss, fr): g[6 - s] = f
                how = e[4] if len(e) > 4 else ''
                v = ACC if '>' in how else 0
                hits = st(e[1], 'A', v) if 's' in how else [(e[1], 'A', v)]
                out.append(K(e[3], g, hits))
                fz = [f for f in fr if f > 0]; pos = sum(fz) / len(fz) if fz else pos
                continue
            ss, fr = place(e[2], pos, fix.get(i), allow_open=True, gap_cost=0.2, **n_opts.get(i, {}))
            steps.append([(s, f) for s, f in zip(ss, fr)]); durs.append(e[1])
            names.append('+'.join(disp(n) for n in sorted(e[2], key=midi)))
            fz = [f for f in fr if f > 0]; pos = sum(fz) / len(fz) if fz else pos
        flush()
        return out


def bar(chords, items, note=''): return dict(chords=chords, items=items, note=note)


def nd(name):
    """a chord name as the page writes it"""
    return name.replace('dim7', '°7').replace('b', '♭').replace('#', '♯').replace('°7', '°7')


def where(p): return f'Método de guitarra tango, p. {p}'


OWN = 'Graciano’s own'
EXS = {}


def ex(sec, id, title, idea, quote, bars):
    EXS.setdefault(sec, []).append(dict(id=id, title=title, idea=idea, quote=quote, bars=bars))


def split(c, at):
    """a cadence's events cut into bars at the given beat"""
    a, b, t = [], [], 0.0
    for e in c.ev:
        (a if t < at - 1e-9 else b).append(e); t += e[1]
    return Cad(a), Cad(b)


# ================================================================ between two sections (pp. 35–37)
DM = ['D3', 'A3', 'D4', 'F4']; DMAJ = ['D3', 'A3', 'D4', 'F#4']


def link(chord, cname, line, land):
    return Cad([('K', 1, chord, cname), ('N', 1, ['A3']), ('N', 1, line[0]), ('N', 1, line[1]), ('N', 2, land), ('W', 2)])


H = {
    '1a': link(DM, 'Dm', [['G#3', 'Bb3'], ['G3', 'C#4']], ['F3', 'D4']),
    '1b': link(DM, 'Dm', [['B2', 'G#3'], ['C#3', 'G3']], ['D3', 'F3']),
    '2a': link(DM, 'Dm', [['G#3', 'Bb3'], ['G3', 'C#4']], ['F#3', 'D4']),
    '2b': link(DM, 'Dm', [['B2', 'G#3'], ['C#3', 'G3']], ['D3', 'F#3']),
    '3a': link(DMAJ, 'D', [['G#3', 'B3'], ['G3', 'C#4']], ['F3', 'D4']),
    '3b': link(DMAJ, 'D', [['B2', 'G#3'], ['C#3', 'G3']], ['D3', 'F3']),
}
LINK_TXT = {
    '1a': ('minor-to-minor', 'Section A in a minor key, section B in a minor key', 35,
           'D minor; then A; G♯ with B♭; G with C♯; into D minor’s F with D. The lower voice falls by semitones (A, G♯, G, F) while the upper climbs (B♭, C♯, D)'),
    '1b': ('minor-to-minor-2', 'Section A minor, section B minor (second way)', 35,
           'the same with the voices turned over: B below G♯, then C♯ below G, into D with F. The lower voice climbs (B, C♯, D), the upper falls (G♯, G, F)'),
    '2a': ('minor-to-major', 'Section A in a minor key, section B in the major', 35,
           'into D major: the same line, landing on F♯ with D'),
    '2b': ('minor-to-major-2', 'Minor to major (second way)', 36, 'the voices turned over, landing on D with F♯'),
    '3a': ('major-to-minor', 'Section A in a major key, section B in the minor', 36,
           'from D major: A; G♯ with B; G with C♯; into D minor’s F with D'),
    '3b': ('major-to-minor-2', 'Major to minor (second way)', 36, 'B below G♯, C♯ below G, into D with F'),
}
# strings for the line and the landing: the 'a' ways at the 5th fret, the 'b' ways from the open A minor or A
LINK_FIX = {'1a': ({1: [5], 2: [5, 4], 3: [5, 4]}, {0: [5, 3]}), '2a': ({1: [5], 2: [5, 4], 3: [5, 4]}, {0: [5, 3]}),
            '3a': ({1: [5], 2: [5, 4], 3: [5, 4]}, {0: [5, 3]}),
            '1b': ({1: [4], 2: [6, 4], 3: [6, 4]}, {0: [6, 5]}), '2b': ({1: [4], 2: [6, 4], 3: [6, 4]}, {0: [6, 5]}),
            '3b': ({1: [4], 2: [6, 4], 3: [6, 4]}, {0: [6, 5]})}
for k, c in H.items():
    id_, title, page, txt = LINK_TXT[k]
    o = c.moved(DOWN_P4)
    first, second = split(o, 4)
    land_name = {'1': 'Am', '2': 'A', '3': 'Am'}[k[0]]
    start_name = {'1': 'Am', '2': 'Am', '3': 'A'}[k[0]]
    q = Cad(c.ev[:2])
    idea = ('The cadence moment that links two sections falls in the 4th bar of a phrase (in his example D minor, A7, A7, D minor). '
            'Over the tonic’s last bar: the chord, then a two-voice line through the dominant’s notes in contrary motion, into the first chord of the next section.') if k == '1a' else \
        'The other voicing: the two voices change places.' if k[1] == 'b' else \
        {'2': 'When the next section is in the major key of the same name: the same line, the last note of the upper voice raised.',
         '3': 'From a major section into a minor one.'}[k[0]]
    ex('entre', 'cadencia-' + id_, title, idea,
       dict(where=where(page), text=f'Posibles cadenciales, {k[0]}: {txt}. Played here: the chord and the A after it.', items=q.items(5, label='his notes'), whose=OWN, played=''),
       [bar([start_name], first.items(5 if k[1] == 'a' else 1, label='the line', fix=LINK_FIX[k][0], k_opts={0: dict(allow_open=k[1] == 'b')}),
            ('In A minor, Очи чёрные’s key, his notes a 4th lower: ' + (('A minor' if k[0] != '3' else 'A major') + (' at the 5th fret (A on the low E string, then E, A, ' if k[1] == 'a' else ' in open position (the open A, then E, A, ') + ('C' if k[0] != '3' else 'C♯') + '); ') +
             'then E; ' + ', then '.join(' with '.join(disp(n) for n in sorted(e[2], key=midi)) for e in first.ev[2:4]) + '.')),
        bar([land_name], second.items(4, label='the next section', fix=LINK_FIX[k][1]), f'Into {"A minor" if land_name == "Am" else "A major"}: ' + ' with '.join(disp(n) for n in sorted(second.ev[0][2], key=midi)) + '.')])

# 4: bVI7 - V7 (slashes)
H4 = Cad([('KN', 2, 'Dm'), ('KN', 1, 'Bb7'), ('KN', 1, 'A7'), ('KN', 2, 'Dm'), ('W', 2)])
G4Q = {'Dm': [-1, 5, 7, 7, 6, -1], 'Bb7': [6, 8, 6, 7, 6, 6], 'A7': [5, -1, 5, 6, 5, -1]}
O4 = H4.moved(DOWN_P4)
GO = {'Am': G4['Am'], 'F7': [-1, 8, 7, 8, 6, -1], 'E7': G4['E7'], 'A': [5, -1, 7, 6, 5, -1]}
q4, _ = split(H4, 4)
o4a, o4b = split(O4, 4)
ex('entre', 'cadencia-bVI7-V7', 'The ♭VI7 before the dominant',
   'The dominant reached through the 7th chord on the minor key’s 6th degree, a semitone above it; then the tonic, minor or major.',
   dict(where=where(36), text='Cadencia ♭VI7–V7: D minor (two beats), B♭7, A7; then D minor or D. He writes slashes; the grips are ours. Played here: that bar.',
        items=q4.items(5, grips=G4Q), whose=OWN, played=''),
   [bar(['Am', 'F7', 'E7'], [K('Am', GO['Am'], [(1, 'A'), (1, 'A')]), K('F7', GO['F7'], [(1, 'A')]), K('E7', GO['E7'], [(1, 'A')])],
        'In A minor: A minor, F7, E7. F7 is the E7 grip one fret higher (F, A, E♭, F from the A string at the 8th fret), so the hand slides down a fret into E7.'),
    bar(['Am'], [K('Am', GO['Am'], [(2, 'A')]), ['W', 2]], 'Into A minor (or A major).')])

# 5: chords over the tonic in the bass, the open string
H5 = Cad([('K', 1, DM, 'Dm'), ('K', 1, ['D3', 'F4', 'A4', 'C5'], 'F/D'), ('K', 1, ['D3', 'E4', 'G#4', 'B4'], 'E/D'), ('K', 1, ['D3', 'Eb4', 'G4', 'Bb4'], 'Eb/D'),
          ('K', 2, ['D3', 'D4', 'F4', 'A4'], 'Dm'), ('W', 2)])
O5 = H5.moved(DOWN_P4)
o5a, o5b = split(O5, 4)
FX5 = {0: [5, 4, 3, 2], 1: [5, 3, 2, 1], 2: [5, 3, 2, 1], 3: [5, 3, 2, 1]}
ex('entre', 'cadencia-pedal', 'Triads over the tonic in the bass',
   ('Over the tonic held in the bass, major triads falling by semitones from the minor key’s 3rd degree: on D, F, then E, then E♭, into D minor or D major. '
    'Graciano: choose a key where the bass can be an open string, with the triad above it.'),
   dict(where=where(36), text='Cadencia ♭III–III–♭II sobre bajo pedal de tónica: D minor, F over D, E over D, E♭ over D; then D minor. On the open D string. Played here: the first two chords.',
        items=Cad(H5.ev[:2]).items(2, fix={0: [4, 3, 2, 1], 1: [4, 3, 2, 1]}, k_opts={0: dict(allow_open=True), 1: dict(allow_open=True)}), whose=OWN, played=''),
   [bar(['Am', 'C/A', 'B/A', 'Bb/A'], o5a.items(3, fix=FX5, k_opts={i: dict(allow_open=True) for i in range(4)}),
        'In A minor the open A string is the bass: A minor (open), then C, B and B♭ on the top three strings at the 5th, 4th and 3rd fret, the same shape sliding down.'),
    bar(['Am'], o5b.items(2, fix={0: [5, 3, 2, 1]}, k_opts={0: dict(allow_open=True)}), 'A minor over the open A: A, C, E on the top three strings (2nd, 1st fret and open).')])

# 6: from the major tonic to the dominant of its relative minor
H6 = {
    'a': Cad([('K', 1, ['C3', 'E3', 'G3', 'C4'], 'C', 's'), ('K', 1, ['C3', 'E3', 'G3', 'C4'], 'C', 's'), ('K', 1, ['B2', 'F3', 'Ab3', 'D4'], 'Bdim7', 's'),
              ('K', 1, ['A2', 'Gb3', 'C4', 'Eb4'], 'Adim7'), ('K', 2, ['G#2', 'E3', 'B3', 'E4'], 'E7'), ('W', 2)]),
    'b': Cad([('K', 1, ['C3', 'E3', 'G3', 'C4'], 'C', 's'), ('K', 1, ['C3', 'E3', 'G3', 'C4'], 'C', 's'), ('K', 1, ['D3', 'Ab3', 'B3', 'F4'], 'Ddim7', 's'),
              ('K', 1, ['D#3', 'A3', 'C4', 'F#4'], 'D#dim7', 's'), ('K', 2, ['E3', 'B3', 'D4', 'G#4'], 'E7'), ('W', 2)]),
    'c': Cad([('K', 1, ['C3', 'E3', 'G3', 'C4'], 'C'), ('K', 1, ['C3', 'E3', 'G3', 'C4'], 'C'), ('K', 1, ['D3', 'F#3', 'C4', 'D4'], 'D7'),
              ('K', 1, ['Eb3', 'G3', 'Db4', 'Eb4'], 'Eb7'), ('K', 2, ['E3', 'G#3', 'D4', 'E4'], 'E7'), ('W', 2)]),
    'd': Cad([('K', 1, ['C3', 'G3', 'B3', 'E4'], 'Cmaj7'), ('K', 1, ['G2', 'G3', 'B3', 'E4'], 'Cmaj7/G'), ('K', 1, ['A2', 'Eb3', 'A3', 'C4', 'F#4'], 'Adim7'),
              ('K', 1, ['Bb2', 'E3', 'Bb3', 'Db4', 'G4'], 'Bbdim7'), ('K', 2, ['B2', 'E3', 'B3', 'D4', 'G#4'], 'E7/B'), ('W', 2)]),
}
H6_TXT = {
    'a': (36, 'C, C, B°7, A°7, E7 (his E7 has no D: G♯, E, B, E): the bass falls C, B, A, G♯', 'the bass falls by step from the tonic to the dominant’s 3rd, through two diminished chords'),
    'b': (37, 'C, C, D°7, D♯°7, E7: the bass climbs C, D, D♯, E', 'the bass climbs by semitones through two diminished chords to the dominant'),
    'c': (37, 'C, C, D7, E♭7, E7: the same climb with three dominant 7ths of one shape', 'the bass climbs through two dominant 7ths of the same shape, a semitone apart'),
    'd': (37, 'Cmaj7, then over G, A°7, B♭°7, E7 over B: the bass G, A, B♭, B', 'from the major 7th over its 5th, the bass climbs by semitones to the dominant’s 5th'),
}
for k, c in H6.items():
    o = c.moved(UP_m3)
    a, b = split(o, 4)
    page, htxt, how = H6_TXT[k]
    ex('entre', 'cadencia-I-V7-VIm-' + k, 'From the major tonic to the dominant of its relative minor' + ('' if k == 'a' else f' ({"second third fourth".split()["bcd".index(k)]} way)'),
       ('In a major key, from the tonic to the dominant of its 6th degree (the relative minor), ' + how + '.') if k == 'a' else how[0].upper() + how[1:] + '.',
       dict(where=where(page), text=f'Cadencia del I al V7/VIm: {htxt}. Played here: the first two chords.', items=Cad(c.ev[:2]).items(2, k_opts={0: dict(allow_open=True), 1: dict(allow_open=True)}), whose=OWN, played=''),
       [bar([e[3] for e in a.ev if e[0] == 'K'], a.items(5, fix={'d': {0: [5, 4, 3, 2], 1: [6, 4, 3, 2]}}.get(k)),
            ('I Wonder Who’s Kissing Her Now goes from E♭ to G7 and C minor (bars 5–7): his cadence a minor 3rd up, from E♭ to the dominant of C minor: ' if k == 'a' else 'The same, a minor 3rd up: ')
            + ', '.join(nd(e[3]) for e in a.ev if e[0] == 'K') + '.'),
        bar([b.ev[0][3]], b.items(5, fix={0: [6, 5, 4, 3, 2]} if k == 'd' else None), 'The dominant of C minor' + (' (as in his, without its 7th: B, G, D, G)' if k == 'a' else '') + '.')])

# 7: from the minor tonic to the dominant, barres sliding down
H7 = Cad([('K', 1, ['A2', 'E3', 'A3', 'C4', 'E4', 'A4'], 'Am', '>'), ('K', 1, ['A2', 'E3', 'A3', 'C4', 'E4', 'A4'], 'Am', 's'),
          ('K', 1, ['G2', 'D3', 'F3', 'B3', 'D4', 'G4'], 'G7', 's'), ('K', 1, ['F2', 'C3', 'Eb3', 'A3', 'C4', 'F4'], 'F7', 's'),
          ('K', 2, ['E2', 'B2', 'D3', 'G#3', 'B3', 'E4'], 'E7'), ('W', 2)])
O7 = H7.moved(SAME)
a7, b7 = split(O7, 4)
KO7 = {i: dict(allow_open=True) for i in range(6)}
ex('entre', 'cadencia-Im-V7', 'From the minor tonic down to the dominant',
   'Whole barres sliding down the neck from the minor tonic to the dominant: the bass falls A, G, F, E, the chords between dominant 7ths on the key’s 7th and 6th degrees.',
   dict(where=where(37), text='Cadencia del Im al V7: A minor (accented), A minor, G7, F7, E7, full six-string chords. Played here: the two A minors.',
        items=Cad(H7.ev[:2]).items(5), whose=OWN, played=''),
   [bar(['Am', 'G7', 'F7'], a7.items(4, k_opts=KO7),
        'Очи чёрные is in his key, so these are Graciano’s own chords: A minor as a barre at the 5th fret, G7 at the 3rd, F7 at the 1st, the bass on the low E string.'),
    bar(['E7'], b7.items(1, k_opts=KO7), 'E7 in open position.')])

# ================================================================ into the end (pp. 37–39)
HB1 = Cad([('K', 1, ['A2', 'E3', 'G3', 'C#4', 'E4', 'A4'], 'A7'), ('K', 1, ['Bb2', 'E3', 'Bb3', 'Db4', 'G4', 'Bb4'], 'Bbdim7'),
           ('K', 1, ['B2', 'F3', 'B3', 'D4', 'G#4', 'B4'], 'Bdim7'), ('K', 1, ['C#3', 'G3', 'C#4', 'E4', 'A#4', 'C#5'], 'C#dim7'),
           ('K', 1, ['D3', 'A3', 'D4', 'F4', 'A4', 'D5'], 'Dm'), ('K', 1, ['A2', 'E3', 'G3', 'C#4', 'E4', 'A4'], 'A7'), ('K', 1, ['D3', 'A3', 'D4', 'F4', 'A4', 'D5'], 'Dm'), ('W', 1)])
OB1 = HB1.moved(DOWN_P4)
b1a, b1b = split(OB1, 4)
KB = {i: dict(allow_open=True, bass=6) for i in range(8)}
ex('final', 'final-disminuidos', 'Chromatic diminished chords',
   ('When the cadence leads to the end of a section or of the piece it comes in the 3rd bar of the phrase (D minor, A7, A7, then D minor, A7, D minor). '
    'Here: the dominant, then diminished 7th chords climbing by semitones, the bass on the low E string, into the tonic. Graciano: it works in major and in minor.'),
   dict(where=where(37), text='Cadencia con disminuidos cromáticos: A7, B♭°7, B°7, C♯°7, then D minor, A7, D minor; the bass on the 6th string, every chord on all six strings. Played here: A7 and B♭°7.',
        items=Cad(HB1.ev[:2]).items(6, k_opts=KB), whose=OWN, played=''),
   [bar(['E7', 'Fdim7', 'F#dim7', 'G#dim7'], b1a.items(1, k_opts=KB),
        'In A minor, his chords a 4th lower: E7 in open position, then the diminished shape at the 1st, 2nd and 4th fret (F, F♯, G♯ in the bass), into A minor at the 5th.'),
    bar(['Am', 'E7', 'Am'], b1b.items(5, k_opts=KB), 'A minor, E7, A minor to end.')])

HB2 = Cad([('K', 1, ['C3', 'E3', 'Bb3', 'C4'], 'C7'), ('K', 1, ['Db3', 'G3', 'Bb3', 'Db4'], 'Dbdim7'), ('K', 1, ['D3', 'F3', 'B3', 'D4'], 'G7/D'),
           ('K', 1, ['E3', 'G3', 'C4', 'E4'], 'C7/E'), ('N', 1, ['F3', 'F4']), ('W', 3)])
OB2 = HB2.moved(UP_M3)
b2a, b2b = split(OB2, 4)
KB5 = {i: dict(bass=5) for i in range(4)}
ex('final', 'final-V7-bVIdim', 'The bass climbs to the leading note',
   ('From the dominant 7th, through the diminished chord on the minor key’s 6th degree, the dominant of the dominant over its 5th, and the dominant over its 3rd: '
    'the bass on the A string climbs by semitones to the leading note, then the tonic. Major or minor.'),
   dict(where=where(38), text='Cadencia V7–♭VIdim–V/V–V/I, in F minor: C7, D♭°7, G7 over D, C7 over E (his has no B♭ in it: E, G, C, E), into F minor. Played here: C7 and D♭°7.',
        items=Cad(HB2.ev[:2]).items(3, k_opts=KB5), whose=OWN, played=''),
   [bar(['E7', 'Fdim7', 'B7/F#', 'E7/G#'], b2a.items(8, k_opts=KB5),
        'In A minor, a major 3rd above his: E7, F°7, B7 over F♯, E7 over G♯ (as his, without its 7th), the bass E, F, F♯, G♯ up the A string from the 7th fret.'),
    bar(['Am'], b2b.items(11), 'Into A minor: A on the A string at the 12th fret with its octave on the B string.')])

HB3 = Cad([('K', 0.5, ['C3', 'E3', 'Bb3', 'C4'], 'C7'), ('N', 1, ['C3']), ('N', 0.25, ['B2']), ('N', 0.25, ['C3']),
           ('N', 0.5, ['C#3']), ('N', 0.5, ['D3']), ('N', 0.5, ['D#3']), ('N', 0.5, ['E3']), ('N', 1, ['F3']), ('W', 3)])
OB3 = HB3.moved(UP_M3)
b3a, b3b = split(OB3, 4)
FX3 = {0: [4, 3, 2, 1], 1: [4], 2: [4], 3: [4], 4: [4], 5: [4], 6: [4], 7: [4]}
ex('final', 'final-decariana', 'The decariana',
   ('A line from the old guard, set down by Julio De Caro and played to this day: from the dominant’s root (the key’s 5th) up by semitones to the tonic, '
    'the first note turned round its lower neighbour. Major or minor.'),
   dict(where=where(38), text='Decariana: C7 (an eighth), C; B, C; C♯, D, D♯, E into F or F minor. Played here: the chord and the C.',
        items=Cad(HB3.ev[:2]).items(2), whose=OWN, played=''),
   [bar(['E7'], b3a.items(2, fix=FX3, k_opts={0: dict(allow_open=True)}),
        'In A minor: E7 (E on the D string at the 2nd fret, G♯, D, the open E), then E; D♯, E; F, F♯, G, G♯, all up the D string from the 1st fret.'),
    bar(['Am'], b3b.items(7, fix={0: [4]}), 'Into A (A minor or major): A on the D string, 7th fret.')])

# doble decariana: his, and his rule for the minor (the tonic's bass a minor 3rd: A becomes A♭; the last chord F minor)
def dd(land, last):
    return Cad([('N', 0.5, ['C3']), ('N', 0.5, ['C4']), ('N', 0.5, ['C3']), ('N', 0.25, ['B3']), ('N', 0.25, ['C4']),
                ('N', 0.5, ['B2', 'C#4']), ('N', 0.5, ['D4']), ('N', 0.5, ['Bb2', 'D#4']), ('N', 0.5, ['E4']),
                ('N', 1, [land, 'F4']), ('K', 1, ['C3', 'E3', 'Bb3', 'C4'], 'C7'), ('K', 1, last[0], last[1], 's'), ('W', 1)])


HB4 = dd('A2', (['F2', 'C3', 'F3', 'A3', 'C4', 'F4'], 'F'))
HB4m = dd('Ab2', (['F2', 'C3', 'F3', 'Ab3', 'C4', 'F4'], 'Fm'))
OB4 = HB4m.moved(UP_M3)
b4a, b4b = split(OB4, 4)
FX4 = {0: [5], 1: [2], 2: [5], 3: [2], 4: [2], 5: [5, 2], 6: [2], 7: [5, 2], 8: [2], 9: [6, 2]}
ex('final', 'final-doble-decariana', 'The double decariana',
   ('Graciano’s name for it: the decariana high up, and below it a second line falling by semitones from the dominant’s root, a rich counterpoint. '
    'His note: in a minor key the tonic’s bass goes to the minor 3rd.'),
   dict(where=where(38), text='Doble línea decariana: over C7, C, C, B, B♭ in the bass (quarters) under C; B, C; C♯, D, D♯, E above; into F over A, then C7 and F. Played here: its first beat.',
        items=Cad(HB4.ev[:2]).items(2, fix={0: [5], 1: [2]}), whose=OWN, played=''),
   [bar(['E7'], b4a.items(6, fix=FX4),
        'In A minor (his rule for the minor applied): the bass E, E, D♯, D on the A string (7th, 7th, 6th, 5th fret), the line E; D♯, E; F, F♯, G, G♯ on the B string from the 4th fret.'),
    bar(['Am/C', 'E7', 'Am'], b4b.items(8, fix={0: [6, 2], 1: [5, 4, 3, 2]}),
        'Into A over C (low E string, 8th fret, with A on the B string), then E7 and A minor, short.')])

HB5 = Cad([('N', 0.5, ['C3', 'C4']), ('N', 0.5, ['C4']), ('N', 0.5, ['C#3', 'C#4']), ('N', 0.5, ['C#4']), ('N', 0.5, ['D3', 'D4']), ('N', 0.5, ['D4']),
           ('N', 0.5, ['E3', 'E4']), ('N', 0.5, ['E4']), ('N', 1, ['F3', 'F4']), ('W', 3)])
OB5 = HB5.moved(UP_M3)
b5a, b5b = split(OB5, 4)
FX5b = {0: [4, 2], 1: [2], 2: [4, 2], 3: [2], 4: [4, 2], 5: [2], 6: [4, 2], 7: [2]}
ex('final', 'final-octavas', 'The line in octaves',
   'The dominant’s root climbing to the tonic in octaves, C, C♯, D, E, F in his: the octave on each beat, its top note again on the “and”. Major or minor.',
   dict(where=where(38), text='Por octavas: C, C♯, D, E in octaves (the low notes short), each top note repeated, into F. Played here: the first beat.',
        items=Cad(HB5.ev[:2]).items(4, fix={0: [5, 3], 1: [3]}), whose=OWN, played=''),
   [bar(['E7'], b5a.items(3, fix=FX5b), 'In A minor: E, F, F♯, G♯ in octaves on the D and B strings (2nd and 5th fret, then 3rd and 6th, 4th and 7th, 6th and 9th).'),
    bar(['Am'], b5b.items(8, fix={0: [4, 2]}), 'Into A: the octave at the 7th and 10th fret.')])

HB6 = Cad([('N', 0.5, ['C3', 'C4']), ('N', 0.25, ['B3']), ('N', 0.25, ['C4']), ('N', 0.5, ['C#3', 'C#4']), ('N', 0.25, ['C4']), ('N', 0.25, ['C#4']),
           ('N', 0.5, ['D3', 'D4']), ('N', 0.25, ['C#4']), ('N', 0.25, ['D4']), ('N', 0.5, ['E3', 'E4']), ('N', 0.25, ['D#4']), ('N', 0.25, ['E4']),
           ('N', 1, ['F3', 'F4']), ('W', 3)])
OB6 = HB6.moved(UP_M3)
b6a, b6b = split(OB6, 4)
FX6 = {i: ([4, 2] if i % 3 == 0 else [2]) for i in range(12)}
ex('final', 'final-octavas-adorno', 'The octaves, decorated',
   ('The same octaves, each one decorated: the octave, then its top note’s lower neighbour a semitone down, and the note again, in sixteenths. '
    '(His print leaves the sharp off the C♯ and D groups’ neighbours after a natural; the pattern is the same in every group.)'),
   dict(where=where(39), text='Por octavas con embellecimiento: C in octaves, B, C; C♯ in octaves, C, C♯; D, C♯, D; E, D♯, E; into F. Played here: the first beat.',
        items=Cad(HB6.ev[:3]).items(4, fix={0: [5, 3], 1: [3], 2: [3]}), whose=OWN, played=''),
   [bar(['E7'], b6a.items(3, fix=FX6), 'In A minor: E, F, F♯, G♯ in octaves on the D and B strings, each top note with its neighbour below on the B string.'),
    bar(['Am'], b6b.items(8, fix={0: [4, 2]}), 'Into A at the 7th and 10th fret.')])



def _labels():
    """every line says what it is: Graciano's in the quotes, ours the line over the bar's chord"""
    for sec in EXS.values():
        for e in sec:
            for it in e['quote']['items']:
                if it[0] == 'P' and '|' not in it[3]: it[3] += '|his notes'
            for b in e['bars']:
                for it in b['items']:
                    if it[0] == 'P' and '|' not in it[3]: it[3] += '|over ' + nd(b['chords'][0]) if b['chords'] else '|the line'


_labels()

SECTIONS = [dict(id='entre', title='Between two sections', part='Exercises', ex=EXS['entre']),
            dict(id='final', title='Into the end', part='Exercises', ex=EXS['final'])]

from quotes import trim as _trim_quotes   # quotes stay a beat or two
_trim_quotes(SECTIONS)
