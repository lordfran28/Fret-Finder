"""Tango fills (rellenos): Graciano, Método de guitarra tango, ch. 3, pp. 27–33 of the owner's copy.
A relleno is a phrase where the tune holds a note or stops, mostly on the top three strings.

Every fill is written twice in data: Graciano's own notes (sounding pitch, in his C minor / C major, on G7 and C),
and ours, made from his by one fixed transposition (letters and semitones together, so the spelling follows),
into Очи чёрные (A minor: E7, A minor, D minor) or I Wonder Who's Kissing Her Now (E♭ major: B♭7, E♭).
The rhythm is his, value for value; only the strings and frets are ours. check5.py proves both.
"""
import sys
sys.path.insert(0, '/home/claude/studies'); sys.path.insert(0, '/home/claude/studies/tango')
from kit_study import OPEN
from entry import K, st, arr, G4, sincopado, marcatto4, GHOST, ACC

# ---------------------------------------------------------------- spelled notes
LET = 'CDEFGAB'; LPC = [0, 2, 4, 5, 7, 9, 11]


def parse(n):
    L, rest = n[0], n[1:]
    acc = 0
    while rest and rest[0] in 'b#':
        acc += 1 if rest[0] == '#' else -1; rest = rest[1:]
    return LET.index(L), acc, int(rest)


def midi(n):
    i, a, o = parse(n)
    return 12 * (o + 1) + LPC[i] + a


def tr(n, steps, semis):
    """transpose a spelled note by an interval given as letter steps and semitones (C->A: -2, -3)"""
    i, a, o = parse(n)
    j = i + steps; o2 = o + j // 7; j %= 7
    target = midi(n) + semis
    acc = target - (12 * (o2 + 1) + LPC[j])
    if acc in (2, -2):                     # a double sharp or flat is written as the plain note it sounds
        j2 = next(k for k in range(7) if (LPC[k] - target) % 12 == 0)
        return LET[j2] + str((target - LPC[j2]) // 12 - 1)
    assert acc in (-1, 0, 1), (n, steps, semis)
    if (LET[j], acc) in (('C', -1), ('F', -1), ('E', 1), ('B', 1)):     # C♭, F♭, E♯, B♯ are written as B, E, F, C
        j2 = next(k for k in range(7) if (LPC[k] - target) % 12 == 0)
        return LET[j2] + str((target - LPC[j2]) // 12 - 1)
    return LET[j] + {-1: 'b', 0: '', 1: '#'}[acc] + str(o2)


def disp(n):
    i, a, o = parse(n)
    return LET[i] + {-1: '♭', 0: '', 1: '♯'}[a]


def on(s, n):
    f = midi(n) - OPEN[6 - s]
    assert 0 <= f <= 15, (s, n, f)
    return [s, f]


# intervals between Graciano's keys and ours
DOWN_m3, UP_M6, UP_m3, UP_M3, UP_M2 = (-2, -3), (5, 9), (2, 3), (2, 4), (1, 2)

# ---------------------------------------------------------------- grips
# Очи чёрные (the tango entries' grips: bass and three notes, around the 5th fret)
OC = dict(Am=G4['Am'], E7=G4['E7'], Dm=G4['Dm'],
          E7o=[0, -1, 2, 1, 3, -1],        # E7 over the open low E (E2 E3 G#3 D4)
          AmL=[5, 7, 7, 5, -1, -1])        # A minor as Graciano voices his landing chord: bass, then 5th, root, 3rd (A2 E3 A3 C4)
# I Wonder Who's Kissing Her Now, its arrangement's grips
IW = dict(Bb7=[6, 8, 6, 7, 6, 6],          # barre at the 6th fret, root on the low E string
          Eb=[-1, 6, 8, 8, 8, 6],          # barre at the 6th fret, root on the A string
          EbL=[-1, 6, 8, 8, 8, -1],        # the same without the top string: bass, 5th, root, 3rd, like his landing chord
          Bb7_7=[-1, -1, 6, 7, 6, 6],      # B♭7 over A♭, the D string lowest (A♭3 D4 F4 B♭4)
          Bb7_1=[-1, -1, 8, 10, 9, 10],    # B♭7, the D string lowest (B♭3 F4 A♭4 D5)
          Bb7_3=[-1, -1, 12, 13, 11, 13])  # B♭7 over D, the D string lowest (D4 A♭4 B♭4 F5)
# Graciano's key, for the quotes (he writes slashes; the grips are ours)
GQ = dict(G7=[3, -1, 3, 4, 3, -1], Cm=[-1, 3, 5, 5, 4, -1], C=[-1, 3, 5, 5, 5, -1],
          G7_7=[-1, -1, 3, 4, 3, 3], G7_1=[-1, -1, 5, 7, 6, 7], G7_3=[-1, -1, 9, 10, 8, 10])

LAND = [(0.5, 'B'), (1, 'C'), (0.5, 'B'), (1, 'C'), (1, '-')]       # his landing bar: bass, chord, bass, chord, rest
TWO = [(1, 'A'), (1, '-'), (1, 'A'), (1, '-')]                     # a stroke on 1 and on 3
FOUR = [(1, 'A')] * 4                                              # four quarter strokes (his four slashes)


def where(p): return f'Método de guitarra tango, p. {p}'


OWN = 'Graciano’s own'


# ---------------------------------------------------------------- one fill, his and ours
class Fill:
    """events: [(beats, [notes])], [] a rest. kind 'R' (one note at a time) or 'P' (two at a time).
    flags per event: 'g' a ghost (the slide's first touch, or his x-note), 's' short."""

    def __init__(self, events, flags=None):
        self.ev = events
        self.flags = flags or [''] * len(events)

    def moved(self, iv, octave=0):
        st_, se = iv
        ev = [(d, [tr(n, st_ + 7 * octave, se + 12 * octave) for n in ns]) for d, ns in self.ev]
        out = Fill(ev, list(self.flags))
        MOVES.append((self, out, se + 12 * octave))
        return out

    def items(self, strings, names_over=None):
        """strings: one entry per sounding event (an int, or a list for two notes). Leading and trailing rests become waits."""
        out, cur, k = [], None, 0
        notes, durs, names, vel, short = [], [], [], [], []
        kind = 'P' if any(len(ns) == 2 for d, ns in self.ev) else 'R'

        def flush():
            if notes:
                it = [kind, list(notes), list(durs), '=' + ','.join(names)]
                if kind == 'R' and (any(vel) or any(short)): it.append(dict(vel=list(vel), short=list(short)))
                out.append(it)
                notes.clear(); durs.clear(); names.clear(); vel.clear(); short.clear()

        for (d, ns), fl in zip(self.ev, self.flags):
            if not ns:
                if notes and kind == 'R':          # a rest inside a run is held over by the note before it
                    durs[-1] += d; continue
                flush(); out.append(['W', d]); continue
            ss = strings[k]; k += 1
            ss = ss if isinstance(ss, list) else [ss]
            assert len(ss) == len(ns)
            pos = [on(s, n) for s, n in zip(ss, ns)]
            notes.append(pos if kind == 'P' else pos[0]); durs.append(d)
            nm = '+'.join(disp(n) for n in ns)
            names.append(('x ' + nm) if 'x' in fl else nm)
            vel.append(GHOST if ('g' in fl or 'x' in fl) else 0); short.append(1 if ('s' in fl or 'x' in fl) else 0)
        flush()
        assert k == len(strings), (k, len(strings))
        return out

    def beats(self): return sum(d for d, ns in self.ev)


def R16(*names, rest=0.25):
    ev = ([(rest, [])] if rest else []) + [(0.25, [n]) for n in names]
    return Fill(ev)


EXS = {}
MOVES = []          # (his, ours, semitones): what check5.py proves


def ex(sec, id, title, idea, quote, bars):
    EXS.setdefault(sec, []).append(dict(id=id, title=title, idea=idea, quote=quote, bars=bars))


def bar(chords, items, note=''): return dict(chords=chords, items=items, note=note)


# ================================================================ scale fills (p. 27–28)
H_DESC_MIN = R16('G4', 'Bb4', 'Ab4', 'G4', 'F4', 'Eb4', 'D4')
H_DESC_MAJ = R16('G4', 'B4', 'A4', 'G4', 'F4', 'E4', 'D4')
H_ASC_MIN = R16('G3', 'A3', 'B3', 'C4', 'D4', 'Eb4', 'F4')
H_ASC_MAJ = R16('G3', 'A3', 'B3', 'C4', 'D4', 'E4', 'F4')


def first_beat(f, strings, n=3):
    """his fill's first beat (a sixteenth rest and three notes, or four notes)"""
    g = Fill(f.ev[:n + (1 if not f.ev[0][1] else 0)])
    return g.items(strings)


ex('escalar', 'relleno-escalar-desc-menor', 'Down the scale into the tonic (minor)',
   ('Over the dominant, after two strokes, a sixteenth rest and seven sixteenths: the 5th of the key, up a minor 3rd to the key’s 7th (the natural minor’s, not the leading note), '
    'then straight down the scale to the 2nd, landing on the tonic chord. Graciano: this fill is one of the bass phrases of chapter 2, raised; in A minor it is the bass phrase down to the tonic (on Tango: the bass) an octave higher.'),
   dict(where=where(27), text='Relleno escalar descendente, en tonalidad menor: on G7, two strokes, then G, B♭, A♭, G, F, E♭, D into C minor (the bass C, then G, C, E♭ above it). Played here: the two strokes and his first three notes.',
        items=[K('G7', GQ['G7'], [(1, 'A'), (1, 'A')])] + first_beat(H_DESC_MIN, [1, 1, 1]), whose=OWN, played=''),
   [bar(['E7'], [K('E7', OC['E7'], [(1, 'A'), (1, 'A')])] + H_DESC_MIN.moved(DOWN_m3).items([2, 2, 2, 2, 3, 3, 3]),
        'Очи чёрные’s E7 into A minor, a minor 3rd below his key: E, G, F, E, D, C, B. E on the B string at the 5th fret, G at the 8th (little finger), F at the 6th, E at the 5th; '
        'then D, C, B on the G string at the 7th, 5th and 4th. The strokes are the E7 from the A string at the 7th fret.'),
    bar(['Am'], [K('Am', OC['AmL'], LAND)], 'A minor voiced as Graciano voices his landing chord: A on the low E string (5th fret), then E, A, C above it.')])

ex('escalar', 'relleno-escalar-desc-mayor', 'Down the scale into the tonic (major)',
   'The same in a major key: from the 5th up a major 3rd to the 7th, then down the scale to the 2nd and onto the tonic.',
   dict(where=where(27), text='En tonalidad mayor: on G7, two strokes, then G, B, A, G, F, E, D into C. Played here: the strokes and his first three notes.',
        items=[K('G7', GQ['G7'], [(1, 'A'), (1, 'A')])] + first_beat(H_DESC_MAJ, [1, 1, 1]), whose=OWN, played=''),
   [bar(['Bb7'], [K('Bb7', IW['Bb7'], [(1, 'A'), (1, 'A')])] + H_DESC_MAJ.moved(UP_m3).items([2, 1, 1, 2, 2, 2, 3]),
        'I Wonder Who’s Kissing Her Now, its B♭7 into E♭ (the intro into the chorus), a minor 3rd above his key: B♭, D, C, B♭, A♭, G, F. '
        'In the 8th position: B♭ on the B string (11th fret), D and C on the top string (10th, 8th), B♭, A♭, G on the B string (11th, 9th, 8th), F on the G string (10th). '
        'The strokes are the song’s B♭7, a barre at the 6th fret.'),
    bar(['Eb'], [K('Eb', IW['EbL'], LAND)], 'E♭ as his landing chord: E♭ on the A string (6th fret), then B♭, E♭, G.')])

ex('escalar', 'relleno-escalar-asc-menor', 'Up the scale into the dominant (minor)',
   ('From the tonic to the dominant: a sixteenth rest and seven sixteenths climbing from the 5th of the key to the 4th above it, the 6th and 7th raised (the melodic minor going up), '
    'so that the dominant’s root falls on the next downbeat. Graciano leaves the first half of the bar empty; here it holds two strokes of the chord, as in his fills going down.'),
   dict(where=where(27), text='Ascendente, en tonalidad menor: G, A, B, C, D, E♭, F into G7. Played here: the sixteenth rest and G, A, B.',
        items=first_beat(H_ASC_MIN, [4, 4, 4]), whose=OWN, played=''),
   [bar(['Am'], [K('Am', OC['Am'], [(1, 'A'), (1, 'A')])] + H_ASC_MIN.moved(UP_M6).items([3, 2, 2, 2, 1, 1, 1]),
        'Очи чёрные’s A minor into E7: E, F♯, G♯, A, B, C, D, all in the 7th position: E on the G string (9th fret), F♯, G♯, A on the B string (7th, 9th, 10th), B, C, D on the top string (7th, 8th, 10th).'),
    bar(['E7'], [K('E7', OC['E7'], FOUR)], 'E7, four strokes, as his four slashes.')])

ex('escalar', 'relleno-escalar-asc-mayor', 'Up the scale into the dominant (major)',
   'The same in a major key: up the major scale from the 5th to the 4th above, into the dominant.',
   dict(where=where(28), text='En tonalidad mayor: G, A, B, C, D, E, F into G7. Played here: the sixteenth rest and G, A, B.',
        items=first_beat(H_ASC_MAJ, [4, 4, 4]), whose=OWN, played=''),
   [bar(['Eb'], [K('Eb', IW['Eb'], [(1, 'A'), (1, 'A')])] + H_ASC_MAJ.moved(UP_m3).items([4, 4, 3, 3, 3, 2, 2]),
        'I Wonder Who’s Kissing Her Now, E♭ into B♭7: B♭, C, D, E♭, F, G, A♭ in the 7th position: B♭ and C on the D string (8th, 10th fret), D, E♭, F on the G string (7th, 8th, 10th), G and A♭ on the B string (8th, 9th).'),
    bar(['Bb7'], [K('Bb7', IW['Bb7'], FOUR)], 'B♭7, four strokes.')])

# ================================================================ pattern fills (p. 28)
H_PAT_MIN = Fill([(0.25, [n]) for n in ['C4', 'B3', 'C4', 'D4', 'Eb4', 'D4', 'Eb4', 'F4']])
H_PAT_MAJ = Fill([(0.25, [n]) for n in ['C4', 'B3', 'C4', 'D4', 'E4', 'D4', 'E4', 'F4']])
ex('patron', 'relleno-patron-menor', 'A pattern into the dominant (minor)',
   ('Graciano’s pattern fill: each group of four sixteenths is a note, the note a step below, the note again, a step up; the next group starts a step higher. '
    'Two beats of it lead into the dominant. He advises studying many such patterns from a book of them.'),
   dict(where=where(28), text='Relleno en patrón, en tonalidad menor: C, B, C, D, then E♭, D, E♭, F into G7 (eighth, quarter, eighth, quarter, rest). Played here: his first beat.',
        items=Fill(H_PAT_MIN.ev[:4]).items([3, 3, 3, 3]), whose=OWN, played=''),
   [bar(['Am'], [K('Am', OC['Am'], [(1, 'A'), (1, 'A')])] + H_PAT_MIN.moved(UP_M6).items([2, 2, 2, 1, 1, 1, 1, 1]),
        'Очи чёрные’s A minor into E7: A, G♯, A, B, then C, B, C, D, in the 7th position: A, G♯, A on the B string (10th, 9th, 10th fret), the rest on the top string (7th, 8th, 7th, 8th, 10th).'),
    bar(['E7'], [sincopado('E7', OC['E7'])], 'E7 in his landing rhythm, eighth, quarter, eighth, quarter, rest: the sincopado of chapter 1.')])
ex('patron', 'relleno-patron-mayor', 'A pattern into the dominant (major)',
   'The same pattern in a major key.',
   dict(where=where(28), text='En tonalidad mayor: C, B, C, D, then E, D, E, F into G7. Played here: his first beat.',
        items=Fill(H_PAT_MAJ.ev[:4]).items([3, 3, 3, 3]), whose=OWN, played=''),
   [bar(['Eb'], [K('Eb', IW['Eb'], [(1, 'A'), (1, 'A')])] + H_PAT_MAJ.moved(UP_m3).items([3, 3, 3, 3, 2, 3, 2, 2]),
        'I Wonder Who’s Kissing Her Now, E♭ into B♭7: E♭, D, E♭, F on the G string (8th, 7th, 8th, 10th fret), then G (B string, 8th), F (G string, 10th), G, A♭ (B string, 8th, 9th).'),
    bar(['Bb7'], [sincopado('Bb7', IW['Bb7'])], 'B♭7, sincopado.')])

# ================================================================ campanitas (p. 28)
# his: stroke; slide into G (D string, 5th fret); G (B string, 8th), short; slide into G (G string, 12th); G (top string, 15th), short; stroke
H_CAMP1 = Fill([(0.125, ['F3']), (0.5, ['G3']), (0.375, ['G4']), (0.125, ['F4']), (0.5, ['G4']), (1, ['G5'])], ['g', '', 's', 'g', '', 's'])
H_CAMP2 = Fill([(0.125, ['F4']), (0.5, ['G4']), (0.5, ['G5']), (0.5, ['G4']), (0.25, ['G5']), (0.25, ['G4']), (0.5, ['G5'])], ['g', '', 's', '', '', '', ''])


def camp_slide_fix(f):
    """our slides start two frets below (his slide lines give no start): the ghost is a whole tone under the target"""
    ev = list(f.ev)
    for i, fl in enumerate(f.flags):
        if fl == 'g':
            tgt = ev[i + 1][1][0]
            ev[i] = (ev[i][0], [tr(tgt, -1, -2)])
    return Fill(ev, f.flags)


H_CAMP1 = camp_slide_fix(H_CAMP1); H_CAMP2 = camp_slide_fix(H_CAMP2)
ex('campanitas', 'campanitas-1', 'Campanitas',
   ('“Little bells”, from Carlos Di Sarli’s piano, taken to the guitar by Ubaldo De Lío: over the dominant, its root in octaves, each struck alone, climbing the neck, '
    'the same note twice on two strings so it rings like a bell, the top one short. Then the chord, and the tonic, minor or major.'),
   dict(where=where(28), text='Campanitas en 8vas: on G7, a stroke, then G slid into on the D string, G on the B string, G slid into on the G string, G on the top string (15th fret), a stroke; then C minor or C. Played here: his first two beats.',
        items=[K('G7', GQ['G7'], [(0.375, 'A')])] + Fill(H_CAMP1.ev[:5], H_CAMP1.flags[:5]).items([4, 4, 2, 3, 3]), whose=OWN, played=''),
   [bar(['E7'], [K('E7', OC['E7'], [(0.375, 'A')])] + H_CAMP1.moved(DOWN_m3).items([5, 5, 2, 3, 3, 1]) + [K('E7', OC['E7'], [(1, 'A')])],
        'Очи чёрные’s E7 into A minor, his bells a minor 3rd lower: E slid into on the A string (5th to 7th fret; his is on the D string, where E would sit at the 2nd fret with no room to slide), '
        'E on the B string (5th), short; E slid into on the G string (7th to 9th); E on the top string (12th), short; the E7 again.'),
    bar(['Am'], [sincopado('Am', OC['Am'])], 'A minor, sincopado (his slashes: eighth, quarter, eighth, quarter, rest).')])
ex('campanitas', 'campanitas-2', 'Campanitas between two strings',
   'The second way: the octave rocking between the G string and the top string, the last three as sixteenth, sixteenth, eighth.',
   dict(where=where(28), text='The second example: a stroke, G slid into on the G string (12th fret), G on the top string (15th), short, G on the G string; then G, G, G between the two strings; a rest. Played here: his first two beats.',
        items=[K('G7', GQ['G7'], [(0.375, 'A')])] + Fill(H_CAMP2.ev[:4], H_CAMP2.flags[:4]).items([3, 3, 1, 3]), whose=OWN, played=''),
   [bar(['E7'], [K('E7', OC['E7'], [(0.375, 'A')])] + H_CAMP2.moved(DOWN_m3).items([3, 3, 1, 3, 1, 3, 1]) + [['W', 1]],
        'On E7: E slid into on the G string (7th to 9th fret), E on the top string (12th), short, back to the G string, then top, G string, top. The hand stays at the 9th–12th fret.'),
    bar(['Am'], [sincopado('Am', OC['Am'])], 'A minor, sincopado.')])

# ================================================================ tenths (p. 29)
TENTH_SF = [0.5, 0.5, 0.5, 2]
TENTH_FR = [1, 0.25, 0.25, 2]
H_DEC_MAJ = [['C3', 'E4'], ['D3', 'F4'], ['D#3', 'F#4'], ['E3', 'G4']]
H_DEC_MIN = [['C3', 'Eb4'], ['Db3', 'F4'], ['D3', 'F#4'], ['Eb3', 'G4']]


def dec(pairs, durs): return Fill([(0.5, [])] + [(d, p) for d, p in zip(durs, pairs)])


def pairs_on(s_lo, s_hi): return [[s_lo, s_hi]] * 4


ex('decimas', 'decimas-mayor', 'Tenths over a major chord',
   ('From Francisco De Caro’s left hand at the piano (his brother Julio’s sextet, the mid-1920s): a note and its tenth, moving together. Over a major chord, from the root and 3rd '
    'the lower voice climbs a tone and two semitones to the 3rd, the upper voice a semitone and two semitones to the 5th. Plain eighths, the last held. Graciano: on the A and B strings as here, '
    'or on the low E and G strings, or on the D and top strings.'),
   dict(where=where(29), text='Rellenos en décimas, sin fraseo, sobre acorde mayor: C with E, D with F, D♯ with F♯, E with G (held), on the A and B strings. Played here: his first beat and a half.',
        items=Fill(dec(H_DEC_MAJ, TENTH_SF).ev[:3]).items([[5, 2], [5, 2]]), whose=OWN, played=''),
   [bar(['Eb'], [sincopado('Eb', IW['Eb'])], 'I Wonder Who’s Kissing Her Now, its E♭ where the voice rests (the 3rd bar of the chorus): a bar of the chord, then the tenths.'),
    bar(['Eb'], dec(H_DEC_MAJ, TENTH_SF).moved(UP_m3).items(pairs_on(5, 2)),
        'E♭ with G, F with A♭, F♯ with A, G with B♭: the A string at the 6th, 8th, 9th, 10th fret, the B string two frets higher, then one.')])
ex('decimas', 'decimas-mayor-fraseada', 'Tenths over a dominant, phrased',
   'Phrased: the first tenth a quarter, the two between quick sixteenths. Graciano: the same goes on a dominant chord.',
   dict(where=where(29), text='Fraseada, sobre acorde mayor: C with E as a quarter, D with F and D♯ with F♯ as sixteenths, E with G held. Played here: the eighth rest and the first tenth.',
        items=Fill(dec(H_DEC_MAJ, TENTH_FR).ev[:2]).items([[5, 2]]), whose=OWN, played=''),
   [bar(['E7'], [sincopado('E7', OC['E7'])], 'Очи чёрные’s E7 (his note: the same applies to the dominant chord).'),
    bar(['E7'], dec(H_DEC_MAJ, TENTH_FR).moved(UP_M3).items(pairs_on(5, 2)),
        'E with G♯, F♯ with A, G with A♯, G♯ with B: the A string at the 7th, 9th, 10th, 11th fret, the B string at the 9th, 10th, 11th, 12th.')])
ex('decimas', 'decimas-menor', 'Tenths over a minor chord',
   ('Over a minor chord, from the root and minor 3rd: the lower voice climbs by semitones to the 3rd, the upper voice a tone and two semitones to the 5th.'),
   dict(where=where(29), text='Sin fraseo, sobre acorde menor: C with E♭, D♭ with F, D with F♯, E♭ with G. Played here: his first beat and a half.',
        items=Fill(dec(H_DEC_MIN, TENTH_SF).ev[:3]).items([[5, 2], [5, 2]]), whose=OWN, played=''),
   [bar(['Dm'], [sincopado('Dm', OC['Dm'])], 'Очи чёрные’s D minor and A minor, a bar of each chord, then its tenths.'),
    bar(['Dm'], dec(H_DEC_MIN, TENTH_SF).moved(UP_M2).items(pairs_on(5, 2)),
        'D minor on the A and B strings: D with F, E♭ with G, E with G♯, F with A (A string 5th to 8th fret).'),
    bar(['Am'], [sincopado('Am', OC['Am'])]),
    bar(['Am'], dec(H_DEC_MIN, TENTH_SF).moved(DOWN_m3).items(pairs_on(6, 3)),
        'A minor on the low E and G strings, the other pair Graciano names: A with C, B♭ with D, B with D♯, C with E (low E string 5th to 8th fret, G string 5th to 9th).')])
ex('decimas', 'decimas-menor-fraseada', 'Tenths over a minor chord, phrased',
   'The minor tenths in the phrased rhythm.',
   dict(where=where(29), text='Fraseada, sobre acorde menor: C with E♭ as a quarter, then the two sixteenths, E♭ with G held. Played here: the eighth rest and the first tenth.',
        items=Fill(dec(H_DEC_MIN, TENTH_FR).ev[:2]).items([[5, 2]]), whose=OWN, played=''),
   [bar(['Am'], [sincopado('Am', OC['Am'])], 'Очи чёрные’s A minor, then its tenths on the third pair of strings, the D and top strings.'),
    bar(['Am'], dec(H_DEC_MIN, TENTH_FR).moved(UP_M6).items(pairs_on(4, 1)),
        'A with C, B♭ with D, B with D♯, C with E: the D string at the 7th to 10th fret, the top string at the 8th, 10th, 11th, 12th.')])

# ================================================================ octaves (p. 30)


def octs(*names, x):
    ev = [(0.5, [])] + [(0.5, [n]) for n in names] + [(0.5, [x])]
    return Fill(ev, [''] * (len(names) + 1) + ['x'])


H_OCT_TD_MIN = octs('C4', 'C5', 'Bb3', 'Bb4', 'Ab3', 'Ab4', x='G2')
H_OCT_DT_MIN = octs('G3', 'G4', 'A3', 'A4', 'B3', 'B4', x='B2')
H_OCT_TD_MAJ = octs('C4', 'C5', 'B3', 'B4', 'A3', 'A4', x='G2')
H_OCT_DT_MAJ = octs('G3', 'G4', 'A3', 'A4', 'B3', 'B4', x='B2')
OCT_IDEA = ('Broken octaves in eighths, the lower note first, stepping down (or up) the scale, and an x on the last eighth: a muted, dead touch of the bass string '
            'where the next chord’s bass is, the hand already there. The next bar: a stroke on 1 and on 3.')
ex('octavas', 'octavas-tonica-dominante-menor', 'Octaves from the tonic to the dominant (minor)',
   OCT_IDEA + ' From the tonic down: the root, the 7th and the 6th of the key, into the dominant.',
   dict(where=where(30), text='Rellenos en 8vas., en tonalidad menor, de tónica a dominante: C, B♭, A♭ in octaves, then the x on G, into G7. Played here: the eighth rest and the first octave.',
        items=Fill(H_OCT_TD_MIN.ev[:3]).items([3, 1]), whose=OWN, played=''),
   [bar(['Am'], H_OCT_TD_MIN.moved(DOWN_m3).items([4, 2, 4, 2, 4, 2, 6]),
        'Очи чёрные’s A minor into E7: A, G, F in octaves on the D and B strings (7th and 10th fret, 5th and 8th, 3rd and 6th), the x on the open low E.'),
    bar(['E7'], [K('E7', OC['E7o'], TWO)], 'E7 over the open low E, near where the octaves end (E on the D string, 2nd fret; G♯, 1st; D on the B string, 3rd).')])
ex('octavas', 'octavas-dominante-tonica-menor', 'Octaves from the dominant to the tonic (minor)',
   OCT_IDEA + ' From the dominant up: its root, then the 6th and 7th of the key raised, into the tonic; the x a semitone under the tonic’s bass.',
   dict(where=where(30), text='De dominante a tónica, en menor: G, A, B in octaves, the x on B, into C minor. Played here: the eighth rest and the first octave.',
        items=Fill(H_OCT_DT_MIN.ev[:3]).items([4, 2]), whose=OWN, played=''),
   [bar(['E7'], H_OCT_DT_MIN.moved(DOWN_m3).items([4, 2, 4, 2, 4, 2, 6]),
        'Очи чёрные’s E7 into A minor: E, F♯, G♯ in octaves on the D and B strings (2nd and 5th fret, 4th and 7th, 6th and 9th), the x on G♯, low E string 4th fret, a fret under A.'),
    bar(['Am'], [K('Am', OC['Am'], TWO)], 'A minor, the bass on the low E string at the 5th fret.')])
ex('octavas', 'octavas-tonica-dominante-mayor', 'Octaves from the tonic to the dominant (major)',
   OCT_IDEA + ' In a major key, from the tonic down the scale to the dominant.',
   dict(where=where(30), text='En tonalidad mayor, de tónica a dominante: C, B, A in octaves, the x on G, into G7. Played here: the eighth rest and the first octave.',
        items=Fill(H_OCT_TD_MAJ.ev[:3]).items([3, 1]), whose=OWN, played=''),
   [bar(['Eb'], H_OCT_TD_MAJ.moved(UP_m3).items([3, 1, 3, 1, 3, 1, 6]),
        'I Wonder Who’s Kissing Her Now, E♭ into B♭7: E♭, D, C in octaves on the G and top strings (8th and 11th fret, 7th and 10th, 5th and 8th), the x on B♭, low E string 6th fret, where the B♭7 barre goes.'),
    bar(['Bb7'], [K('Bb7', IW['Bb7'], TWO)], 'B♭7, the barre at the 6th fret.')])
ex('octavas', 'octavas-dominante-tonica-mayor', 'Octaves from the dominant to the tonic (major)',
   OCT_IDEA + ' In a major key, from the dominant up to the tonic.',
   dict(where=where(30), text='En tonalidad mayor, de dominante a tónica: G, A, B in octaves, the x on B, into C. Played here: the eighth rest and the first octave.',
        items=Fill(H_OCT_DT_MAJ.ev[:3]).items([4, 2]), whose=OWN, played=''),
   [bar(['Bb7'], H_OCT_DT_MAJ.moved(UP_m3).items([3, 1, 3, 1, 3, 1, 5]),
        'B♭7 into E♭: B♭, C, D in octaves on the G and top strings (3rd and 6th fret, 5th and 8th, 7th and 10th), the x on D, A string 5th fret, a fret under E♭.'),
    bar(['Eb'], [K('Eb', IW['Eb'], TWO)], 'E♭, the barre at the 6th fret.')])

# ================================================================ sixths and thirds (pp. 30–32)


def dyads(pairs):
    return Fill([(0.5, [])] + [(d, p) for d, p in zip([1, 0.5, 1], pairs)] + [(1, [])])


SIX = [  # id, title, chord, his pairs, page, interval to ours, strings, text
    ('sextas-dominante-fundamental', 'Sixths into the root (dominant)', 'dom', [['A3', 'F4'], ['Bb3', 'F#4'], ['B3', 'G4']], 30, DOWN_m3, (4, 2),
     'buscando la fundamental: on G7, A with F, B♭ with F♯, B with G', 'E7: F♯ with D, G with D♯, G♯ with E, on the D and B strings (4th and 3rd fret, 5th and 4th, 6th and 5th). E on top, the root.'),
    ('sextas-dominante-tercera', 'Sixths into the 3rd (dominant)', 'dom', [['C4', 'A4'], ['C#4', 'A#4'], ['D4', 'B4']], 31, DOWN_m3, (4, 2),
     'buscando la tercera: on G7, C with A, C♯ with A♯, D with B', 'E7: A with F♯, A♯ with G, B with G♯, on the D and B strings at the 7th, 8th, 9th fret. G♯ on top, the 3rd.'),
    ('sextas-dominante-quinta', 'Sixths into the 5th (dominant)', 'dom', [['Eb3', 'C4'], ['E3', 'C#4'], ['F3', 'D4']], 31, UP_M6, (3, 1),
     'buscando la quinta: on G7, E♭ with C, E with C♯, F with D', 'E7: C with A, C♯ with A♯, D with B, on the G and top strings at the 5th, 6th, 7th fret. B on top, the 5th.'),
    ('sextas-menor-fundamental', 'Sixths into the root (minor)', 'min', [['Db4', 'Bb4'], ['D4', 'B4'], ['Eb4', 'C5']], 31, DOWN_m3, (3, 1),
     'buscando la fundamental: on C minor, D♭ with B♭, D with B, E♭ with C', 'A minor: B♭ with G, B with G♯, C with A, on the G and top strings at the 3rd, 4th, 5th fret. A on top, the root.'),
    ('sextas-menor-tercera', 'Sixths into the 3rd (minor)', 'min', [['F3', 'C#4'], ['F#3', 'D4'], ['G3', 'Eb4']], 31, UP_M6, (3, 1),
     'buscando la tercera: on C minor, F with C♯, F♯ with D, G with E♭', 'A minor: D with A♯, D♯ with B, E with C, on the G string (7th, 8th, 9th fret) and the top string (6th, 7th, 8th). C on top, the 3rd.'),
    ('sextas-menor-quinta', 'Sixths into the 5th (minor)', 'min', [['Ab3', 'F4'], ['A3', 'F#4'], ['Bb3', 'G4']], 31, DOWN_m3, (4, 2),
     'buscando la quinta: on C minor, A♭ with F, A with F♯, B♭ with G', 'A minor: F with D, F♯ with D♯, G with E, on the D and B strings at the 3rd, 4th, 5th fret. E on top, the 5th, with G under it (the minor 7th, as his B♭ is in C minor).'),
]
THI = [
    ('terceras-dominante-tercera', 'Thirds into the 3rd (dominant)', 'dom', [['F3', 'A3'], ['Gb3', 'Bb3'], ['G3', 'B3']], 31, UP_M6, (3, 2),
     'buscando la tercera, on G7: F with A, G♭ with B♭, G with B', 'E7: D with F♯, E♭ with G, E with G♯, on the G and B strings at the 7th, 8th, 9th fret. G♯ on top, the 3rd.'),
    ('terceras-dominante-quinta', 'Thirds into the 5th (dominant)', 'dom', [['A3', 'C4'], ['Bb3', 'Db4'], ['B3', 'D4']], 32, UP_M6, (2, 1),
     'buscando la quinta: on G7, A with C, B♭ with D♭, B with D', 'E7: F♯ with A, G with B♭, G♯ with B, on the B string (7th, 8th, 9th fret) and the top string (5th, 6th, 7th). B on top, the 5th.'),
    ('terceras-dominante-septima', 'Thirds into the 7th (dominant only)', 'dom', [['C4', 'Eb4'], ['C#4', 'E4'], ['D4', 'F4']], 32, UP_M6, (2, 1),
     'buscando la séptima (solo en acorde de dominante): on G7, C with E♭, C♯ with E, D with F', 'E7: A with C, A♯ with C♯, B with D, on the B string (10th, 11th, 12th fret) and the top string (8th, 9th, 10th). D on top, the 7th.'),
    ('terceras-menor-tercera', 'Thirds into the 3rd (minor)', 'min', [['A#3', 'C#4'], ['B3', 'D4'], ['C4', 'Eb4']], 32, UP_M6, (2, 1),
     'buscando la tercera: on C minor, A♯ with C♯, B with D, C with E♭', 'A minor: G with A♯, G♯ with B, A with C, on the B string (8th, 9th, 10th fret) and the top string (6th, 7th, 8th). C on top, the 3rd.'),
    ('terceras-menor-quinta', 'Thirds into the 5th (minor)', 'min', [['Db4', 'F4'], ['D4', 'F#4'], ['Eb4', 'G4']], 32, DOWN_m3, (3, 2),
     'buscando la quinta: on C minor, D♭ with F, D with F♯, E♭ with G', 'A minor: B♭ with D, B with D♯, C with E, on the G and B strings at the 3rd, 4th, 5th fret. E on top, the 5th.'),
]
SIX_IDEA = ('Inside one chord: a sixth slides up by semitones onto two of the chord’s notes, the target on top. Eighth rest, a quarter, an eighth, the target a quarter, a rest; '
            'then the chord goes on. Each sixth keeps the same size as the target’s.')
THI_IDEA = ('The same with thirds. Graciano: it is good to swap, one chord with a fill in thirds, the next with one in sixths.')
HQ_STR = {'sextas-dominante-fundamental': [4, 2], 'sextas-dominante-tercera': [3, 1], 'sextas-dominante-quinta': [4, 2], 'sextas-menor-fundamental': [3, 1],
          'sextas-menor-tercera': [4, 2], 'sextas-menor-quinta': [4, 2], 'terceras-dominante-tercera': [4, 3], 'terceras-dominante-quinta': [3, 2],
          'terceras-dominante-septima': [3, 2], 'terceras-menor-tercera': [3, 2], 'terceras-menor-quinta': [3, 2]}
TGT = {'fundamental': 'root', 'tercera': '3rd', 'quinta': '5th', 'septima': '7th'}
for sec, rows, idea0, word in (('sextas', SIX, SIX_IDEA, 'Rellenos en 6tas.'), ('terceras', THI, THI_IDEA, 'Rellenos en 3eras.')):
    for i, (id_, title, kind, pairs, page, iv, ss, his_txt, our_txt) in enumerate(rows):
        h = dyads(pairs)
        c, g = ('E7', OC['E7']) if kind == 'dom' else ('Am', OC['Am'])
        tgt = TGT[id_.split('-')[-1]]
        idea = idea0 if i == 0 else f'The same over a {"dominant" if kind == "dom" else "minor"} chord, aiming at its {tgt}.'
        head = (word + ' ') if i == 0 else ''
        kind_txt = 'para acorde dominante o mayor' if kind == 'dom' else 'para acorde menor'
        ex(sec, id_, title, idea,
           dict(where=where(page), text=f'{head}{kind_txt.capitalize() if not head else kind_txt}, {his_txt}; then a bar of the chord. Played here: the eighth rest and his first {"sixth" if sec == "sextas" else "third"}.',
                items=Fill(h.ev[:2]).items([HQ_STR[id_]]), whose=OWN, played=''),
           [bar([c], h.moved(iv).items([list(ss)] * 3), f'Очи чёрные’s {"E7" if c == "E7" else "A minor"}. {our_txt}'),
            bar([c], [K(c, g, FOUR)], 'The chord, four strokes.')])

# ================================================================ the marcatto as a fill (pp. 32–33)
ORD = {1: ['7', '1', '3', '1'], 2: ['7', '3', '1', '7'], 3: ['7', '3', '1', '3'], 4: ['7', '1', '7', '3']}
NAME = {'7': 'Bb7/Ab', '1': 'Bb7', '3': 'Bb7/D'}
HNAME = {'7': 'G7/F', '1': 'G7', '3': 'G7/B'}


def marc_bar(order):
    its = []
    for j, k in enumerate(ORD[order]):
        g = IW['Bb7_' + k]
        if j < 3: its.append(K(NAME[k], g, st(1, 'A')))
        else: its += [K(NAME[k], g, [(0.5, 'A')]), arr(IW['Eb'], 'Eb')]
    return its


for o in (1, 2, 3, 4):
    q = [K(HNAME[k], GQ['G7_' + k], st(1, 'A')) for k in ORD[o][:2]]
    ex('marcatto', f'marcatto-relleno-{o}', f'The marcatto in inversions, order {o}',
       ('The pianists’ marcatto jumps by octaves; on the guitar that does little, so Graciano keeps the idea and moves through the dominant’s inversions instead, the D string always lowest: '
        'its 7th, its root or its 3rd in the bass. Four short chords, then a slide into the tonic’s first beat.') if o == 1 else '',
       dict(where=where(32 if o < 3 else 33), text=f'Rellenos del marcatto 4, orden {o}: on G7, with the D string lowest, ' +
            ', '.join({'7': 'F in the bass', '1': 'G', '3': 'B'}[k] for k in ORD[o]) + '; the slide into C minor or C. Played here: his first two chords.',
            items=q, whose=OWN, played=''),
       [bar(['Bb7/Ab', 'Bb7', 'Bb7/D'], marc_bar(o),
            ('I Wonder Who’s Kissing Her Now, B♭7 into E♭, the D string lowest: A♭ under D, F, B♭ at the 6th–7th fret; B♭ under F, A♭, D at the 8th–10th; '
             'D under A♭, B♭, F at the 11th–13th. ' if o == 1 else '') + 'This order: ' + ', '.join({'7': 'A♭ in the bass', '1': 'B♭', '3': 'D'}[k] for k in ORD[o]) +
            '. The slide goes up the A string from the 3rd fret into E♭ at the 6th.'),
        bar(['Eb'], [sincopado('Eb', IW['Eb'])], 'E♭, sincopado, his slashes.')])

# ================================================================ étude: Очи чёрные with fills
CH = ['E7', 'E7', 'Am', 'Am', 'E7', 'E7', 'Am', 'Am', 'Dm', 'Dm', 'Am', 'Am', 'E7', 'E7', 'Am', 'Am']


def etude():
    b = []
    E7, Am, Dm = OC['E7'], OC['Am'], OC['Dm']
    b.append(bar(['E7'], [marcatto4('E7', E7)], 'Очи чёрные’s sixteen bars, a fill in every second bar of each chord, from this page: the scale down (bar 2), the pattern (4), octaves (6 and 12), '
                 'sixths (8), tenths (10), campanitas (14). The other bars keep the rhythms of chapter 1.'))
    b.append(bar(['E7'], [K('E7', E7, [(1, 'A'), (1, 'A')])] + H_DESC_MIN.moved(DOWN_m3).items([2, 2, 2, 2, 3, 3, 3]), 'Down the scale into A minor.'))
    b.append(bar(['Am'], [K('Am', OC['AmL'], LAND)]))
    b.append(bar(['Am'], [K('Am', Am, [(1, 'A'), (1, 'A')])] + H_PAT_MIN.moved(UP_M6).items([2, 2, 2, 1, 1, 1, 1, 1]), 'The pattern into E7.'))
    b.append(bar(['E7'], [sincopado('E7', E7)]))
    b.append(bar(['E7'], H_OCT_DT_MIN.moved(DOWN_m3).items([4, 2, 4, 2, 4, 2, 6]), 'Octaves up into A minor.'))
    b.append(bar(['Am'], [K('Am', Am, TWO)]))
    b.append(bar(['Am'], dyads(SIX[3][3]).moved(DOWN_m3).items([[3, 1]] * 3), 'Sixths into A minor’s root.'))
    b.append(bar(['Dm'], [sincopado('Dm', Dm)]))
    b.append(bar(['Dm'], dec(H_DEC_MIN, TENTH_SF).moved(UP_M2).items(pairs_on(5, 2)), 'Tenths over D minor.'))
    b.append(bar(['Am'], [sincopado('Am', Am)]))
    b.append(bar(['Am'], H_OCT_TD_MIN.moved(DOWN_m3).items([4, 2, 4, 2, 4, 2, 6]), 'Octaves down into E7.'))
    b.append(bar(['E7'], [K('E7', OC['E7o'], TWO)], 'E7 over the open low E, where the octaves left the hand.'))
    b.append(bar(['E7'], [K('E7', E7, [(0.375, 'A')])] + H_CAMP1.moved(DOWN_m3).items([5, 5, 2, 3, 3, 1]) + [K('E7', E7, [(1, 'A')])], 'Campanitas into A minor.'))
    b.append(bar(['Am'], [sincopado('Am', Am)]))
    b.append(bar(['Am'], [K('Am', Am, [(0.5, 'A', ACC), (3.5, '-')])], 'One short chord, accented.'))
    return b


ETUDES = [dict(id='etude-ochi-rellenos', title='Очи чёрные with fills', idea='', quote=dict(where='', text='', item=None), bars=etude())]



def _label_runs():
    """each run or pair of lines says what it is played over: ours the bar's chord, Graciano's 'his notes'"""
    def lab(its, text):
        for it in its:
            if it[0] in 'RP' and isinstance(it[3], str) and it[3].startswith('=') and '|' not in it[3]:
                it[3] += '|' + text
    for sec in EXS.values():
        for e in sec:
            q = e['quote']
            lab(q.get('items') or [], 'his notes')
            for b in e['bars']:
                if b['chords']: lab(b['items'], 'over ' + b['chords'][0].replace('b', '♭').replace('#', '♯'))
    for b in ETUDES[0]['bars']:
        lab(b['items'], 'over ' + b['chords'][0].replace('b', '♭').replace('#', '♯'))


_label_runs()

SECTIONS = [dict(id='escalar', title='Scale fills', part='Exercises', ex=EXS['escalar']),
            dict(id='patron', title='Pattern fills', part='Exercises', ex=EXS['patron']),
            dict(id='campanitas', title='Campanitas', part='Exercises', ex=EXS['campanitas']),
            dict(id='decimas', title='Tenths', part='Exercises', ex=EXS['decimas']),
            dict(id='octavas', title='Octaves', part='Exercises', ex=EXS['octavas']),
            dict(id='sextas', title='Sixths', part='Exercises', ex=EXS['sextas']),
            dict(id='terceras', title='Thirds', part='Exercises', ex=EXS['terceras']),
            dict(id='marcatto', title='The marcatto as a fill', part='Exercises', ex=EXS['marcatto']),
            dict(id='etudes', title='Études', part='Études', ex=ETUDES)]

