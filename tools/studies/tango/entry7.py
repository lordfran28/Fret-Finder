"""Tango harmony: Graciano, Método de guitarra tango, ch. 5 ("Giros armónicos"), pp. 41–49 of the owner's copy.
Reharmonizing with diatonic chords, the circle of 5ths, tritone substitutes, diminished chords for the dominant,
the line cliché (from the octave and from the 5th), and the tritone interval with its four resolutions.

Same method as entries 5 and 6: Graciano's notes kept as data (sounding pitch) and moved whole by one interval:
his C minor and D minor examples into A minor (Очи чёрные), his A minor and C major tritone examples a minor 3rd up
into C minor and E♭ (I Wonder Who's Kissing Her Now). Where he gives only chord names, ours are grips on the same
chords moved. check7.py proves the moves and the stretches.
"""
import sys
sys.path.insert(0, '/home/claude/studies'); sys.path.insert(0, '/home/claude/studies/tango')
import importlib.util as _ilu
_sp = _ilu.spec_from_file_location('cad6', '/home/claude/studies/tango/entry6.py'); E6 = _ilu.module_from_spec(_sp); _sp.loader.exec_module(E6)
from entry import K, st, ACC
Cad, place, tr, tr_name, midi, disp, nd, split = E6.Cad, E6.place, E6.tr, E6.tr_name, E6.midi, E6.disp, E6.nd, E6.split
E6.MOVES.clear()
MOVES = E6.MOVES
DOWN_m3, DOWN_P4, UP_m3 = (-2, -3), (-3, -5), (2, 3)


def bar(chords, items, note=''): return dict(chords=chords, items=items, note=note)
def where(p): return f'Método de guitarra tango, p. {p}'


OWN = 'Graciano’s own'
EXS = {}


def ex(sec, id, title, idea, quote, bars):
    EXS.setdefault(sec, []).append(dict(id=id, title=title, idea=idea, quote=quote, bars=bars))


def names(c): return ', '.join(nd(e[3]) for e in c.ev if e[0] == 'K')


def T(text, w):
    """a quote in words only (his diagrams, his chord names): no sound"""
    return dict(where=where(w), text=text, item=None, by='Graciano')


# ================================================================ diatonic reharmonization (pp. 41–43)
H1 = Cad([('K', 1, ['C3', 'G3', 'C4', 'Eb4'], 'Cm'), ('K', 1, ['D3', 'Ab3', 'C4', 'F4'], 'Dm7b5'), ('K', 1, ['Eb3', 'Bb3', 'Eb4', 'G4'], 'Eb'),
          ('K', 1, ['E3', 'G3', 'C4', 'G4'], 'C/E'), ('K', 1, ['F3', 'C4', 'F4', 'Ab4'], 'Fm'), ('W', 3)])
O1 = H1.moved(DOWN_m3); a1, b1 = split(O1, 4)
ex('diatonica', 'im-ivm', 'From the minor tonic to its 4th degree',
   ('Where a minor tonic goes to the minor chord on its 4th degree (with or without the 4th’s dominant between), climb by step through the natural minor’s chords: '
    'I, II (half-diminished), ♭III, then the 4th’s dominant over its 3rd, and the minor IV. The bass climbs too.'),
   dict(where=where(41), text='Conexión del Im al IVm: in C minor, over the bar before F minor, C minor, D half-diminished, E♭, C over E, into F minor. Played here: the first two chords.',
        items=Cad(H1.ev[:2]).items(4), whose=OWN, played=''),
   [bar(['Am', 'Bm7b5', 'C', 'A/C#'], a1.items(5, k_opts={i: dict(allow_open=True) for i in range(4)}),
        'Очи чёрные goes from A minor to D minor (bars 8–9 of the chorus in four): his chords a minor 3rd lower, ' + names(a1) + '; the bass A, B, C, C♯.'),
    bar(['Dm'], b1.items(5), 'Into D minor.')])

H2 = Cad([('K', 1, ['C3', 'G3', 'C4', 'Eb4'], 'Cm'), ('K', 1, ['Bb2', 'G3', 'Bb3', 'Eb4'], 'Cm/Bb'), ('K', 1, ['A2', 'Gb3', 'C4', 'Eb4'], 'Adim7'),
          ('K', 1, ['Ab2', 'Eb3', 'Gb3', 'C4', 'Eb4'], 'Ab7'), ('K', 1, ['G2', 'D3', 'F3', 'B3', 'D4'], 'G7'), ('W', 3)])
O2 = H2.moved(DOWN_m3); a2, b2 = split(O2, 4)
ex('diatonica', 'im-v7', 'From the minor tonic to the dominant',
   ('A still minor tonic set moving by a falling bass: the tonic, the tonic over its minor 7th, a passing diminished (or the 7th degree’s dominant with ♭9), '
    'then the ♭VI7 that cadences on the dominant. The bass falls by semitones from the root to the dominant.'),
   dict(where=where(42), text='Conexión del Im al V7: C minor, C minor over B♭ (his has no C in it), A°7, A♭7, into G7. Played here: the first two chords.',
        items=Cad(H2.ev[:2]).items(5, k_opts={0: dict(allow_open=True), 1: dict(allow_open=True)}), whose=OWN, played=''),
   [bar(['Am', 'Am/G', 'F#dim7', 'F7'], a2.items(3, k_opts={i: dict(allow_open=True, bass=6) for i in range(4)}),
        'Очи чёрные’s A minor before E7: ' + names(a2) + ', the bass A, G, F♯, F down the low E string (as his, without the root in the second chord).'),
    bar(['E7'], b2.items(1, k_opts={0: dict(allow_open=True, bass=6)}), 'E7 in open position.')])

H3 = Cad([('N', 1, ['C3']), ('K', 1, ['G3', 'C4', 'Eb4', 'G4'], 'Cm'), ('K', 1, ['F3', 'Bb3', 'D4', 'G4'], 'Bb6'), ('K', 1, ['Eb3', 'Ab3', 'C4', 'G4'], 'Abmaj7'),
          ('K', 1, ['G2', 'D3', 'F3', 'B3', 'D4', 'G4'], 'G7'), ('W', 3)])
O3 = H3.moved(DOWN_m3); a3, b3 = split(O3, 4)
ex('diatonica', 'grela', 'Roberto Grela’s way: a pedal on top',
   ('The same idea as Roberto Grela played it, a relative of the Andalusian cadence: the tonic, the ♭VII6, the ♭VImaj7, the dominant, '
    'with the dominant’s root held on top all the way (in C minor, a G).'),
   dict(where=where(42), text='C in the bass, then C minor (G, C, E♭, G), B♭6 (F, B♭, D, G), A♭maj7 (E♭, A♭, C, G), into G7 (G, D, F, B, D, G). Played here: the bass and the first chord.',
        items=Cad(H3.ev[:2]).items(5), whose=OWN, played=''),
   [bar(['Am', 'G6', 'Fmaj7'], a3.items(3, fix={1: [4, 3, 2, 1], 2: [5, 4, 3, 1], 3: [5, 4, 3, 1]},
                                         k_opts={i: dict(allow_open=True) for i in range(1, 4)}),
        'In A minor the held note is E, the open top string: A in the bass, then A minor (E, A, C, E), G6 (D, G, B, E), Fmaj7 (C, F, A, E), each with the open E on top.'),
    bar(['E7'], b3.items(1, k_opts={0: dict(allow_open=True)}), 'Into E7 in open position, the E still on top.')])

GQ = {'Fm': [1, 3, 3, 1, 1, 1], 'Bb7': [6, 8, 6, 7, 6, 6], 'Ebmaj7': [-1, 6, 8, 7, 8, -1], 'Abmaj7': [4, -1, 5, 5, 4, -1], 'Dm7b5': [-1, 5, 6, 5, 6, -1],
      'G7': [3, -1, 3, 4, 3, -1], 'Cm': [-1, 3, 5, 5, 4, -1]}
GC = {'Dm': [-1, 5, 7, 7, 6, -1], 'G7': [3, -1, 3, 4, 3, -1], 'Cmaj7': [-1, 3, 5, 4, 5, -1], 'Fmaj7': [1, -1, 2, 2, 1, -1], 'Bm7b5': [-1, 2, 3, 2, 3, -1],
      'E7': [0, -1, 0, 1, 0, -1], 'Am': [-1, 0, 2, 2, 1, 0]}
HC = Cad([('KN', 2, 'Fm'), ('KN', 2, 'Bb7'), ('KN', 2, 'Ebmaj7'), ('KN', 2, 'Abmaj7'), ('KN', 2, 'Dm7b5'), ('KN', 2, 'G7'), ('KN', 4, 'Cm')])
OC = HC.moved(DOWN_m3)
cb = [split(OC, 4)[0]]; rest_ = split(OC, 4)[1]
cb.append(split(rest_, 4)[0]); rest_ = split(rest_, 4)[1]
cb.append(split(rest_, 4)[0]); cb.append(split(rest_, 4)[1])
CIRCLE_NOTE = 'D minor, G7, Cmaj7, Fmaj7, B half-diminished, E7, A minor: the bass D, G, C, F, B, E, A, each a 5th below the last. All in the first five frets.'
ex('diatonica', 'circulo-1', 'The circle of 5ths',
   ('Where the harmony goes IVm, Im, V7, Im, run the circle of 5ths from the minor IV at twice the speed, the chords of the key: '
    'IVm, ♭VII7, ♭IIImaj7, ♭VImaj7, IIm7♭5, V7, Im. The functions still fall where they did; the dominant comes a little later, after its own II.'),
   dict(where=where(42), text='In C minor, over F minor, C minor, G7, C minor: F minor, B♭7; E♭maj7, A♭maj7; D half-diminished, G7; C minor. He gives the chord names; the grips are ours. Played here: the first bar.',
        items=Cad([('KN', 1, e[2]) for e in HC.ev[:2]]).items(5, grips=GQ), whose=OWN, played=''),
   [bar([e[2] for e in c.ev], c.items(3, grips=GC), CIRCLE_NOTE if j == 0 else '') for j, c in enumerate(cb)])
EXS['diatonica'][-1]['bars'][0]['note'] = 'Очи чёрные’s second half (D minor, A minor, E7, A minor) with the circle in its place: ' + CIRCLE_NOTE
# ================================================================ tritone substitutes (pp. 43–44)
H4 = Cad([('K', 2, ['G2', 'D3', 'F3', 'B3', 'D4'], 'G7'), ('K', 2, ['Db3', 'F3', 'B3', 'Eb4'], 'Db7'), ('K', 4, ['C3', 'G3', 'C4', 'Eb4'], 'Cm')])
O4 = H4.moved(DOWN_m3); a4, b4 = split(O4, 4)
ex('tritonal', 'sustituto-tritonal', 'The tritone substitute',
   ('A dominant, primary or secondary, in minor or major, can be replaced by the dominant an augmented 4th away: the two share their 3rd and 7th, swapped. '
    'Either in its place (the original left out), or after it, two beats each: the substitute second, so the tension rises before it rests. '
    '(His D♭7 keeps the G7’s B; the print leaves the natural off it.)'),
   dict(where=where(43), text='G7 (G, D, F, B, D), then its substitute D♭7 (D♭, F, B, E♭, the 9th on top). Played here: the G7.',
        items=[K('G7', [3, 5, 3, 4, 3, -1], [(2, 'A')])], whose=OWN, played=''),
   [bar(['E7', 'Bb7'], a4.items(1, fix={1: [5, 4, 3, 2]}, k_opts={0: dict(allow_open=True), 1: dict(allow_open=True)}),
        'Очи чёрные’s E7, then its substitute B♭7, his notes a minor 3rd lower: E7 in open position (E, B, D, G♯, B), then B♭, D, A♭, C in the first position: the open D and the note at the G string’s 1st fret (G♯ in E7, the same note as A♭ in B♭7) do not move.'),
    bar(['Am'], b4.items(2, k_opts={0: dict(allow_open=True)}), 'Into A minor: the B♭ falls a semitone to A.')])
H5 = Cad([('K', 4, ['Db3', 'F3', 'B3', 'Eb4', 'G4'], 'Db7#11')])
O5 = H5.moved(DOWN_m3)
ex('tritonal', 'sustituto-11', 'The substitute with its 9th and ♯11',
   'Graciano: it is very common to colour the substitute with its 9th and its ♯11.',
   dict(where=where(44), text='D♭7(9,♯11): D♭, F, B, E♭, G. Played here: that chord.', items=Cad([('K', 2) + tuple(H5.ev[0][2:])]).items(6), whose=OWN, played=''),
   [bar(['Bb7#11'], O5.items(6), 'B♭7 with 9th and ♯11, his chord a minor 3rd lower: B♭, D, A♭, C, E from the low E string, at the 5th and 6th fret.')])

# ================================================================ diminished chords for the dominant (p. 44)
H6 = Cad([('K', 2, ['G2', 'D3', 'F3', 'B3', 'D4'], 'G7'), ('K', 2, ['B2', 'F3', 'Ab3', 'D4'], 'Bdim7')])
O6 = H6.moved(DOWN_m3)
ex('disminuidos', 'disminuido-por-dominante', 'A diminished chord for the dominant',
   ('A tango sound from the very start: the dominant, primary or secondary, replaced by the diminished 7th on its 3rd (the dominant with ♭9, its root left out). '
    'Being symmetrical, it can move a minor 3rd at a time along the neck and stay the same chord: B°7, D°7, F°7, A♭°7.'),
   dict(where=where(44), text='G7 (G, D, F, B, D), then B°7 (B, F, A♭, D). Played here: both.', items=Cad([(e[0], 1) + tuple(e[2:]) for e in H6.ev]).items(3), whose=OWN, played=''),
   [bar(['E7', 'G#dim7'], O6.items(1, k_opts={0: dict(allow_open=True)}) + [],
        'Очи чёрные’s E7 and the diminished on its 3rd, G♯°7 (G♯, D, F, B), his chords a minor 3rd lower.'),
    bar(['Am'], [K('Am', [-1, 0, 2, 2, 1, 0], [(2, 'A'), (2, '-')])], 'Into A minor.')])
DIMG = [('G#dim7', [4, 5, 6, 4, 6, 4], 'root on the low E string (4th fret)'), ('G#dim7', [-1, 11, 12, 10, 12, -1], 'root on the A string (11th fret)'),
        ('G#dim7', [-1, -1, 6, 7, 6, 7], 'root on the D string (6th fret)')]
ex('disminuidos', 'disminuido-graficos', 'The three diminished grips',
   'The diminished shapes most used in tango: with the root on the 6th string (all six strings, a barre), on the 5th string, and on the 4th.',
   T('Tónica en 6ta., en 5ta., en 4ta.: three grip diagrams, no pitches given.', 44),
   [bar(['G#dim7'] * 3, [K(n, g, [(1, 'A')]) for n, g, w in DIMG] + [['W', 1]], 'G♯°7 three ways: ' + '; '.join(w for n, g, w in DIMG) + '.')])
MARC_DIM = [('Bdim7', [-1, -1, 9, 10, 9, 10]), ('G#dim7', [-1, -1, 6, 7, 6, 7]), ('Fdim7', [-1, -1, 3, 4, 3, 4]), ('Ddim7', [-1, -1, 0, 1, 0, 1])]
ex('disminuidos', 'disminuido-marcatto', 'Marcatto 4 on four diminished chords',
   ('In place of the dominant, a marcatto 4 with four different diminished chords (the same chord a minor 3rd apart); '
    'Graciano: mind how the last one resolves, above all the top voice.'),
   T('Al reemplazar al dominante, podemos realizar un marcatto 4 con cuatro acordes disminuidos diferentes: the idea in words; the bar is ours.', 44),
   [bar([n for n, g in MARC_DIM], [K(n, g, st(1, 'A', ACC if i % 2 == 0 else 0)) for i, (n, g) in enumerate(MARC_DIM)],
        'In place of Очи чёрные’s E7: B°7, G♯°7, F°7, D°7 on the top four strings, the shape sliding down three frets each time (9th, 6th, 3rd fret, then open). '
        'The top voice falls D, B, G♯, F, and F falls a semitone to A minor’s E.'),
    bar(['Am'], [K('Am', [-1, 0, 2, 2, 1, 0], [(2, 'A'), (2, '-')])], 'A minor in open position, E on top.')])

# ================================================================ the line cliché (pp. 44–47)
def four(vs, name4, dur=1, how=''):
    return [('K', dur, v, n, how) for v, n in zip(vs, name4)]


LC8 = ['Dm', 'Dm(maj7)', 'Dm7', 'Dm6']
LC5 = ['Dm', 'Dm#5', 'Dm6', 'Dm#5']
V8 = {'bajo': [['D3', 'F3', 'A3'], ['C#3', 'F3', 'A3'], ['C3', 'F3', 'A3'], ['B2', 'F3', 'A3']],
      'soprano': [['D3', 'F4', 'A4', 'D5'], ['D3', 'F4', 'A4', 'C#5'], ['D3', 'F4', 'A4', 'C5'], ['D3', 'F4', 'A4', 'B4']],
      'interna': [['D3', 'D4', 'F4', 'A4'], ['D3', 'C#4', 'F4', 'A4'], ['D3', 'C4', 'F4', 'A4'], ['D3', 'B3', 'F4', 'A4']]}
V5 = {'bajo': [['A2', 'F3', 'D4'], ['A#2', 'F3', 'D4'], ['B2', 'F3', 'D4'], ['A#2', 'F3', 'D4']],
      'soprano': [['D3', 'D4', 'F4', 'A4'], ['D3', 'D4', 'F4', 'A#4'], ['D3', 'D4', 'F4', 'B4'], ['D3', 'D4', 'F4', 'A#4']],
      'interna': [['D3', 'A3', 'F4'], ['D3', 'A#3', 'F4'], ['D3', 'B3', 'F4'], ['D3', 'A#3', 'F4']]}
NAMES_A8 = ['Am', 'Am(maj7)', 'Am7', 'Am6']
NAMES_A5 = ['Am', 'Am#5', 'Am6', 'Am#5']
FIX8 = {'bajo': {i: [6, 5, 4] for i in range(4)}, 'soprano': {i: [6, 3, 2, 1] for i in range(4)}, 'interna': {i: [6, 4, 3, 2] for i in range(4)}}
FIX5 = {'bajo': {i: [6, 5, 3] for i in range(4)}, 'soprano': {i: [5, 3, 2, 1] for i in range(4)}, 'interna': {i: [5, 4, 2] for i in range(4)}}
WHERE_TXT = {'bajo': 'in the bass', 'soprano': 'on top', 'interna': 'in an inner voice'}
for k, page in (('bajo', 45), ('soprano', 45), ('interna', 45)):
    h = Cad(four(V8[k], LC8)); o = h.moved(DOWN_P4)
    o = Cad([(e[0], e[1], e[2], NAMES_A8[i], e[4]) for i, e in enumerate(o.ev)])
    ex('cliche8', 'cliche-8va-' + k, 'The line from the octave, ' + WHERE_TXT[k],
       ('On a minor chord (most often I or IVm, sometimes IIm in a major key): its root falls by semitones, root, major 7th, minor 7th, 6th, while the chord stays, '
        'one bar to two. Here the line ' + WHERE_TXT[k] + '.') if k == 'bajo' else 'The same line ' + WHERE_TXT[k] + '.',
       dict(where=where(page), text='Línea desde la 8va., ' + {'bajo': 'al bajo', 'soprano': 'a la soprano', 'interna': 'a la voz interna'}[k] + ', on D minor: D, C♯, C, B under F and A' if k == 'bajo' else
            ('Línea desde la 8va., a la soprano: D, C♯, C, B on top of D minor' if k == 'soprano' else 'a la voz interna: D, C♯, C, B under F and A, D in the bass') + '. Played here: the first chord.',
            items=Cad(h.ev[:1]).items(5, fix={0: {'bajo': [5, 4, 3], 'soprano': [4, 3, 2, 1], 'interna': [4, 3, 2, 1]}[k]}, k_opts={0: dict(allow_open=True)}), whose=OWN, played=''),
       [bar(NAMES_A8, o.items(5, fix=FIX8[k], k_opts={i: dict(allow_open=True) for i in range(4)}),
            'On Очи чёрные’s A minor, his chords a 4th lower: ' + {'bajo': 'A, G♯, G, F♯ on the low E string (5th to 2nd fret) under C and E (A string 3rd fret, D string 2nd).',
                                                                   'soprano': 'A, G♯, G, F♯ on the top string (5th to 2nd fret) over C and E (G and B strings, 5th fret), the low A under them.',
                                                                   'interna': 'A, G♯, G, F♯ on the D string (7th to 4th fret) under C and E (G and B strings, 5th fret), the low A below.'}[k])])
# the bass line as marcatto 4, arpeggio, broken up, against a counter-line, in octaves
hm = Cad(four(V8['bajo'], LC8, 1, 's'))
hm = Cad([(e[0], e[1], e[2], e[3], 's>' if i % 2 == 0 else 's') for i, e in enumerate(hm.ev)]); om = hm.moved(DOWN_P4)
om = Cad([(e[0], e[1], e[2], NAMES_A8[i], e[4]) for i, e in enumerate(om.ev)])
ex('cliche8', 'cliche-8va-marcatto', 'The line in the bass, as marcatto 4',
   'Most often the line goes in the bass, on the A or D string, played as a marcatto 4 or broken into an arpeggio.',
   dict(where=where(45), text='Marcatto 4: the bass-line chords, four short strokes. Played here: the first.', items=Cad(hm.ev[:1]).items(5, fix={0: [5, 4, 3]}), whose=OWN, played=''),
   [bar(NAMES_A8, om.items(5, fix=FIX8['bajo']), 'Short strokes, accents on 1 and 3.')])
HA = Cad([('N', 0.5, [b]) if False else ('N', 0.5, [b]) for b in []])
arp_ev = []
for b in ['D3', 'C#3', 'C3', 'B2']:
    arp_ev += [('N', 0.5, [b]), ('N', 0.5, ['F3']), ('N', 1, ['A3'])]
HA = Cad(arp_ev); OA = HA.moved(DOWN_P4); oa1, oa2 = split(OA, 4)
FXA = {0: [6], 1: [5], 2: [4], 3: [6], 4: [5], 5: [4]}
ex('cliche8', 'cliche-8va-arpegio', 'The line in the bass, arpeggiated',
   'The chord broken: the line’s note, then the other two, eighth, eighth, quarter. Graciano: of all the ways this is the most played.',
   dict(where=where(45), text='Arpegio: D, F, A; C♯, F, A; C, F, A; B, F, A. Played here: the first beat and a half.', items=Cad(HA.ev[:2]).items(5, fix={0: [5], 1: [4]}), whose=OWN, played=''),
   [bar(['Am', 'Am(maj7)'], oa1.items(4, fix=FXA), 'A, C, E; G♯, C, E: the line on the low E string, C on the A string (3rd fret), E on the D string (2nd).'),
    bar(['Am7', 'Am6'], oa2.items(3, fix=FXA), 'G, C, E; F♯, C, E.')])
HF = Cad([('N', 0.5, ['D3']), ('N', 0.5, ['F3', 'A3']), ('W', 0.25), ('N', 0.25, ['D3']), ('N', 0.25, ['C#3']), ('N', 0.25, ['C3']), ('N', 0.5, ['B2']), ('N', 1.5, ['F3', 'A3'])])
OF = HF.moved(DOWN_P4)
ex('cliche8', 'cliche-8va-fragmentada', 'The line broken up',
   'Rhythmically broken: the bass and the chord, then the whole line in sixteenths after a short rest, the chord held to the end of the bar.',
   dict(where=where(46), text='Rítmicamente fragmentada: D; F and A; a sixteenth rest, D, C♯, C; B; F and A held. Played here: the first beat.', items=Cad(HF.ev[:2]).items(5, fix={0: [5], 1: [4, 3]}), whose=OWN, played=''),
   [bar(['Am'], OF.items(4, fix={0: [6], 1: [5, 4], 3: [6], 4: [6], 5: [6], 6: [6], 7: [5, 4]}), 'A; C and E; then A, G♯, G down the low E string, F♯, and C with E held.')])
HCP = Cad([('N', 0.5, ['D3']), ('N', 0.5, ['D4']), ('N', 0.5, ['C#3', 'E4']), ('N', 0.5, ['F4']), ('N', 1, ['C3', 'E4']), ('N', 1, ['B2', 'D4'])])
OCP = HCP.moved(DOWN_P4)
ex('cliche8', 'cliche-8va-contrapunto', 'The line against a counter-line',
   'In counterpoint: the line in the bass in quarters, and above it a melody that climbs and falls back (in his, D, E, F, E, D).',
   dict(where=where(46), text='Contrapuntísticamente, on D minor: D in the bass, then D, E, F, E, D above C♯, C, B. Played here: the first beat.', items=Cad(HCP.ev[:2]).items(5, fix={0: [5], 1: [3]}), whose=OWN, played=''),
   [bar(['Am'], OCP.items(4, fix={0: [6], 1: [3], 2: [6, 3], 3: [2], 4: [6, 3], 5: [6, 3]}), 'A in the bass; A, B, C, B, A above (G string, B string) over G♯, G, F♯ on the low E string.')])
HO = Cad([('N', 1, ['D3', 'D4']), ('N', 1, ['C#3', 'C#4']), ('N', 1, ['C3', 'C4']), ('N', 1, ['B2', 'B3'])])
OO = HO.moved(DOWN_P4)
ex('cliche8', 'cliche-8va-octavas', 'The line in octaves',
   'The line alone, in octaves.',
   dict(where=where(46), text='Como octavados: D, C♯, C, B in octaves. Played here: the first.', items=Cad(HO.ev[:1]).items(5, fix={0: [5, 3]}), whose=OWN, played=''),
   [bar(['Am'], OO.items(4, fix={i: [6, 4] for i in range(4)}), 'A, G♯, G, F♯ in octaves on the low E and D strings (5th and 7th fret, then down a fret at a time).')])

for k, page in (('bajo', 46), ('soprano', 46), ('interna', 46)):
    h = Cad(four(V5[k], LC5)); o = h.moved(DOWN_P4)
    o = Cad([(e[0], e[1], e[2], NAMES_A5[i], e[4]) for i, e in enumerate(o.ev)])
    ex('cliche5', 'cliche-5ta-' + k, 'The line from the 5th, ' + WHERE_TXT[k],
       ('The other line climbs from the minor chord’s 5th by semitones and comes back: 5, ♯5, 6, ♯5. Here ' + WHERE_TXT[k] + '.') if k == 'bajo' else 'The same line ' + WHERE_TXT[k] + '.',
       dict(where=where(page), text='Línea desde la 5ta., ' + {'bajo': 'al bajo: A, A♯, B, A♯ under F and D', 'soprano': 'a la soprano: A, A♯, B, A♯ on top of D, F', 'interna': 'a la voz interna: A, A♯, B, A♯ between D and F'}[k] + '. Played here: the first chord.',
            items=Cad(h.ev[:1]).items(3, fix={0: {'bajo': [5, 4, 2], 'soprano': [4, 3, 2, 1], 'interna': [4, 3, 1]}[k]}, k_opts={0: dict(allow_open=True)}), whose=OWN, played=''),
       [bar(NAMES_A5, o.items(2, fix=FIX5[k], k_opts={i: dict(allow_open=True) for i in range(4)}),
            'On Очи чёрные’s A minor, a 4th lower: ' + {'bajo': 'E, F, F♯, F on the low E string (open, 1st, 2nd, 1st fret) under C and A.',
                                                        'soprano': 'E, F, F♯, F on the top string (open, 1st, 2nd, 1st) over A and C, the open A below.',
                                                        'interna': 'E, F, F♯, F on the D string (2nd, 3rd, 4th, 3rd fret) between the open A and C.'}[k])])
h5m = Cad([(e[0], e[1], e[2], e[3], 's>' if i % 2 == 0 else 's') for i, e in enumerate(four(V5['interna'], LC5))]); o5m = h5m.moved(DOWN_P4)
o5m = Cad([(e[0], e[1], e[2], NAMES_A5[i], e[4]) for i, e in enumerate(o5m.ev)])
ex('cliche5', 'cliche-5ta-marcatto', 'The line from the 5th, inside, as marcatto 4',
   'For this line the middle voice is the usual place, on the D string, in a marcatto 4.',
   dict(where=where(47), text='Marcatto 4 with the inner voice. Played here: the first stroke.', items=Cad(h5m.ev[:1]).items(3, fix={0: [4, 3, 1]}, k_opts={0: dict(allow_open=True)}), whose=OWN, played=''),
   [bar(NAMES_A5, o5m.items(2, fix=FIX5['interna'], k_opts={i: dict(allow_open=True) for i in range(4)}), 'Short strokes, accents on 1 and 3.')])
arp5 = []
for m in ['A3', 'A#3', 'B3', 'A#3']:
    arp5 += [('N', 0.5, ['D3']), ('N', 0.5, [m]), ('N', 1, ['F4'])]
HA5 = Cad(arp5); OA5 = HA5.moved(DOWN_P4); o51, o52 = split(OA5, 4)
FXA5 = {0: [5], 1: [4], 2: [2], 3: [5], 4: [4], 5: [2]}
ex('cliche5', 'cliche-5ta-arpegio', 'The line from the 5th, arpeggiated',
   'Broken: the root, the line’s note, the 3rd above.',
   dict(where=where(47), text='Arpegio: D, A, F; D, A♯, F; D, B, F; D, A♯, F. Played here: the first beat and a half.', items=Cad(HA5.ev[:2]).items(3, fix={0: [4], 1: [3]}), whose=OWN, played=''),
   [bar(['Am', 'Am#5'], o51.items(2, fix=FXA5, n_opts={0: {}}), 'A (open A string), E, C; A, F, C: the line on the D string, C on the B string (1st fret).'),
    bar(['Am6', 'Am#5'], o52.items(2, fix=FXA5), 'A, F♯, C; A, F, C.')])
HF5 = Cad([('N', 0.5, ['D3']), ('N', 0.5, ['A3', 'F4']), ('W', 0.5), ('N', 0.25, ['A3']), ('N', 0.25, ['A#3']), ('N', 1, ['B3']), ('N', 1, ['A2'])])
OF5 = HF5.moved(DOWN_P4)
ex('cliche5', 'cliche-5ta-fragmentada', 'The line from the 5th, broken up',
   'Rhythmically broken: the root and the chord, a rest, the line in two quick notes and a held one, then the low 5th.',
   dict(where=where(47), text='Rítmicamente fragmentada: D; A and F; an eighth rest; A, A♯; B; then the low A. Played here: the first beat.', items=Cad(HF5.ev[:2]).items(3, fix={0: [4], 1: [3, 1]}), whose=OWN, played=''),
   [bar(['Am'], OF5.items(2, fix={0: [5], 1: [4, 2], 3: [4], 4: [4], 5: [4], 6: [6]}), 'A (open); E and C; a rest; E, F on the D string; F♯; then the open low E.')])

# ================================================================ the tritone (pp. 47–49), a minor 3rd up: C minor and E♭
TRI = [['G#3', 'D4'], ['B3', 'F4'], ['D4', 'G#4'], ['F4', 'B4']]
RES = [['A3', 'C4'], ['C4', 'E4'], ['C4', 'A4'], ['E4', 'C5']]
HT1 = Cad([('N', 1, TRI[0]), ('N', 1, RES[0]), ('W', 2)]); OT1 = HT1.moved(UP_m3)
ex('tritono', 'tritono-basico', 'The tritone and where it goes',
   ('One of tango’s great resources, for V7 to Im above all (and as much for V7 to I in major): the tritone between the key’s 4th and 7th degrees, '
    'the heart of the dominant, resolving by semitone into the tonic. In A minor, G♯ and D into A and C.'),
   dict(where=where(47), text='Posibilidad básica: over E7 the tritone G♯ with D, resolving to A with C over A minor. Played here: both.', items=Cad(HT1.ev[:2]).items(6), whose=OWN, played=''),
   [bar(['G7', 'Cm'], OT1.items(9, fix={0: [4, 3], 1: [4, 3]}),
        'I Wonder Who’s Kissing Her Now goes from G7 to C minor (bars 6–7): G7’s tritone, B with F, into C with E♭, his notes a minor 3rd up. On the D and G strings, 9th and 10th fret.')])
HT2 = Cad([('N', 1, TRI[0]), ('N', 1, TRI[1]), ('N', 1, TRI[2]), ('N', 1, TRI[3])]); OT2 = HT2.moved(UP_m3)
ex('tritono', 'tritono-reemplazos', 'Four tritones for one',
   'The tritone can be replaced by the one a minor 3rd higher, and that one again: four in all, each a dominant’s heart (here of E7, G7, B♭7, D♭7 in his A minor).',
   dict(where=where(48), text='Over E7: G♯ with D; reemplazos B with F, D with G♯, F with B. Played here: the first two.', items=Cad(HT2.ev[:2]).items(6), whose=OWN, played=''),
   [bar(['G7'], OT2.items(9, fix={0: [4, 3], 1: [4, 3], 2: [3, 2], 3: [3, 2]}),
        'Over G7: B with F, D with A♭, F with B, A♭ with D. The first two on the D and G strings (9th–10th, 12th–13th fret), the last two on the G and B strings (10th–12th, 13th–15th).')])
ev3 = []
for t, r in zip(TRI, RES): ev3 += [('N', 1, t), ('N', 1, r)]
HT3 = Cad(ev3); OT3 = HT3.moved(UP_m3); t3a, t3b = split(OT3, 4)
ex('tritono', 'tritono-resoluciones', 'Four tritones, four resolutions',
   ('Each of the four resolves into the tonic chord by semitone: G♯/D to A/C, B/F to C/E, D/G♯ to C/A, F/B to E/C (in his A minor): '
    'every note a step from a note of the chord it goes to.'),
   dict(where=where(48), text='Cuatro posibles resoluciones, in A minor. Played here: the first tritone and its resolution.', items=Cad(HT3.ev[:2]).items(6), whose=OWN, played=''),
   [bar(['G7', 'Cm', 'G7', 'Cm'], t3a.items(9, fix={0: [4, 3], 1: [4, 3], 2: [4, 3], 3: [4, 3]}),
        'Into C minor: B/F to C/E♭, D/A♭ to E♭/G.'),
    bar(['G7', 'Cm', 'G7', 'Cm'], t3b.items(11), 'F/B to E♭/C, A♭/D to G/E♭, higher up.')])

# the fingerings: his diagrams are positions in A minor, so they go on Очи чёрные's E7 and A minor as they are
ev43 = []
for t, r in zip(TRI, RES): ev43 += [('N', 1, t), ('N', 1, r)]
H43 = Cad(ev43); O43 = H43.moved((0, 0)); f43a, f43b = split(O43, 4)
F43 = {'a': {0: [4, 3], 1: [4, 3], 2: [4, 3], 3: [4, 3]}, 'b': {0: [4, 3], 1: [4, 3]}}
ex('tritono', 'tritono-cuerdas-4-3', 'The four on the D and G strings',
   ('On the guitar Graciano plays them on the 4th and 3rd strings: the tritone (his black dots) and its resolution (grey) in four fingerings to learn by heart, '
    'so the resource is ready under the hand. His diagrams are in A minor, Очи чёрные’s key, so these are his positions, over its E7 and A minor.'),
   T('Posibilidad 1–4, en 4ta. y 3er. cuerda: four diagrams of the tritone and its resolution (G♯/D, B/F, D/G♯, F/B and where each goes).', 48),
   [bar(['E7', 'Am', 'E7', 'Am'], f43a.items(7, fix=F43['a']), 'G♯/D (D string 6th, G string 7th) to A/C (7th, 5th); B/F (9th, 10th) to C/E (10th, 9th).'),
    bar(['E7', 'Am', 'E7', 'Am'], Cad(f43b.ev[:2]).items(12, fix=F43['b']) + Cad(f43b.ev[2:]).moved((-7, -12)).items(3, fix=F43['b']),
        'D/G♯ (12th, 13th) to C/A (10th, 14th); F/B an octave lower, where the neck allows (3rd, 4th) to E/C (2nd, 5th).')])
MOVES.pop()        # that octave is the neck's, not a change of key
F32a = {0: [3, 2], 1: [3, 2], 2: [3, 2], 3: [3, 2]}
ex('tritono', 'tritono-cuerdas-3-2', 'The four on the G and B strings',
   ('On the 3rd and 2nd strings, tuned a major 3rd apart, the shapes change. In his third the resolution’s lower note would need too wide a hand, '
    'so it moves to the D string, the same notes.'),
   T('Posibilidad 1–4, en 3er. y 2da. cuerda; for the third, the resolution on the 2nd and 4th strings.', 48),
   [bar(['E7', 'Am', 'E7', 'Am'], f43a.items(3, fix=F32a), 'G♯/D (G string 1st, B string 3rd) to A/C (2nd, 1st); B/F (4th, 6th) to C/E (5th, 5th).'),
    bar(['E7', 'Am', 'E7', 'Am'], f43b.items(10, fix={0: [3, 2], 1: [4, 2], 2: [3, 2], 3: [3, 2]}),
        'D/G♯ (7th, 9th) to C on the D string (10th) with A on the B string (10th), as his; F/B (10th, 12th) to E/C (9th, 13th).')])

# examples of application (p. 49). His four examples are quoted (their first beat or two); ours apply the same
# device to I Wonder Who's Kissing Her Now's own dominants: over each dominant its tritone (3rd and 7th) and the
# replacements a minor 3rd up, each pair moving by step into the next chord. check7.py checks every pair by that rule.
def slashes(seq):
    return [('KN', d, n) for n, d in seq]


AP_END_MIN = [('KN', 1, 'E7'), ('N', 1, ['G#3', 'D4']), ('N', 1, ['A3', 'C4']), ('N', 1, ['F3', 'B3']),
              ('N', 1, ['E3', 'C4']), ('N', 1, ['A2']), ('K', 1, ['A3', 'C4', 'E4', 'A4'], 'Am'), ('W', 1)]
HP1 = Cad(slashes([('Am', 1), ('Am', 1), ('Am', 1), ('F7', 1), ('E7', 1), ('E7', 1), ('E7', 1), ('E7', 1)]) + AP_END_MIN)
HP2 = Cad(slashes([('C', 1), ('C', 1), ('C', 1), ('Ab7', 1), ('G7', 1), ('G7', 1), ('G7', 1), ('G7', 1)]) +
          [('KN', 1, 'G7'), ('N', 1, ['F3', 'B3']), ('N', 1, ['E3', 'C4']), ('N', 1, ['G#3', 'D4']),
           ('N', 1, ['G3', 'E4']), ('N', 1, ['C3']), ('K', 1, ['E3', 'G3', 'C4', 'E4'], 'C'), ('W', 1)])
HP3 = Cad(slashes([('C', 1), ('C', 1), ('C', 1), ('D#7', 1), ('E7', 1), ('E7', 1), ('E7', 1), ('E7', 1)]) + AP_END_MIN)
HP4 = Cad(slashes([('C', 1), ('C', 1), ('C', 1), ('C', 1), ('D7', 1), ('D7', 1), ('D7', 1)]) + [('N', 1, ['F#3', 'C4']),
          ('N', 1, ['G3', 'B3']), ('N', 1, ['G2']), ('K', 1, ['F3', 'B3', 'D4'], 'G7'), ('N', 1, ['F3', 'B3']),
          ('N', 1, ['E3', 'C4']), ('N', 1, ['C3']), ('K', 1, ['E3', 'G3', 'C4', 'E4'], 'C7'), ('N', 1, ['E3', 'Bb3']),
          ('N', 1, ['F3', 'A3']), ('N', 1, ['G3', 'C#4']), ('N', 1, ['A3', 'C4']), ('KN', 1, 'G7'),
          ('KN', 1, 'C'), ('N', 1, ['G3', 'C#4']), ('N', 1, ['F3', 'D4']), ('N', 1, ['Bb3', 'E4']),
          ('N', 1, ['A3', 'F4']), ('KN', 1, 'Ab7'), ('KN', 1, 'G7'), ('N', 1, ['F3', 'B3']),
          ('N', 1, ['E3', 'C4']), ('N', 1, ['F4', 'B4']), ('N', 1, ['E4', 'C5']), ('W', 1)])
GQ2 = {'Am': [5, 7, 7, 5, 5, 5], 'F7': [1, 3, 1, 2, 1, 1], 'E7': [0, 2, 0, 1, 0, 0], 'C': [-1, 3, 2, 0, 1, 0], 'Ab7': [4, 6, 4, 5, 4, 4],
       'G7': [3, 5, 3, 4, 3, 3], 'D#7': [-1, 6, 5, 6, 4, -1], 'D7': [-1, 5, 4, 5, 3, -1]}
GI = {'Eb': [-1, 6, 8, 8, 8, 6], 'Bb7': [6, 8, 6, 7, 6, 6], 'Cm7': [8, 10, 8, 8, 8, 8], 'G7': [-1, 10, 12, 10, 12, 10],
      'Abmaj7': [-1, 11, 13, 12, 13, 11], 'C7': [8, 10, 8, 9, 8, 8], 'Fm7': [-1, 8, 10, 8, 9, 8], 'F7': [-1, 8, 10, 8, 10, 8],
      'Ab7': [-1, 11, 13, 11, 13, 11], 'G7/D': [-1, 5, 5, 4, 6, -1]}     # the song page's own grips
OURS = {}          # id: [(song bar, [(chord, beats)], events)]: what check7.py checks by the rule


def kn(*cs): return [('KN', 1, c) for c in cs]


OURS['aplicacion-menor'] = [
    (7, [('Abmaj7', 2), ('C7', 2)], kn('Abmaj7', 'Abmaj7', 'C7', 'C7')),
    (8, [('C7', 4)], kn('C7') + [('N', 1, ['E3', 'Bb3']), ('N', 1, ['G3', 'Db4']), ('N', 1, ['Bb3', 'E4'])]),
    (9, [('Fm7', 4)], [('N', 1, ['Ab3', 'F4'])] + kn('Fm7', 'Fm7') + [('W', 1)])]
OURS['aplicacion-mayor'] = [
    (14, [('F7', 4)], kn('F7') + [('N', 1, ['A3', 'Eb4']), ('N', 1, ['C4', 'Gb4']), ('N', 1, ['Eb4', 'A4'])]),
    (15, [('F7', 2), ('Bb7', 2)], kn('F7') + [('N', 1, ['A3', 'Eb4']), ('N', 1, ['Ab3', 'D4'])] + kn('Bb7')),
    (16, [('Bb7', 4)], [('KN', 2, 'Bb7'), ('N', 1, ['Ab3', 'D4']), ('N', 1, ['D4', 'Ab4'])]),
    (17, [('Eb', 4)], [('N', 1, ['Eb4', 'G4']), ('KN', 2, 'Eb'), ('W', 1)])]
OURS['aplicacion-secundario'] = [
    (3, [('Eb', 4)], kn('Eb', 'Eb', 'Eb', 'Eb')),
    (4, [('Eb', 2), ('G7/D', 2)], kn('Eb', 'Eb', 'G7/D') + [('N', 1, ['B3', 'F4'])]),
    (5, [('Cm7', 4)], [('N', 1, ['C4', 'Eb4']), ('KN', 2, 'Cm7'), ('W', 1)])]
OURS['aplicacion-cadena'] = [
    (21, [('Eb', 2), ('G7', 2)], kn('Eb', 'Eb', 'G7') + [('N', 1, ['B3', 'F4'])]),
    (22, [('Ab7', 4)], [('N', 1, ['C4', 'Gb4'])] + kn('Ab7', 'Ab7') + [('N', 1, ['Gb3', 'C4'])]),
    (23, [('G7', 2), ('C7', 2)], [('N', 1, ['F3', 'B3'])] + kn('G7') + [('N', 1, ['E3', 'Bb3']), ('N', 1, ['G3', 'Db4'])]),
    (24, [('Fm7', 4)], [('N', 1, ['Ab3', 'C4']), ('KN', 2, 'Fm7'), ('W', 1)])]
NEAR = {'aplicacion-menor': 7, 'aplicacion-mayor': 6, 'aplicacion-secundario': 5, 'aplicacion-cadena': 9}
NOTES = {
    'aplicacion-menor': ['Bars 7–9 of I Wonder Who’s Kissing Her Now: C7 resolving to F minor.', 'Bar 8, where the voice holds: C7, then its tritone E with B♭, and the two replacements a minor 3rd up, G with D♭ and B♭ with E.',
                         'Into F minor: B♭ falls a step to A♭, E rises a semitone to F; then the chord.'],
    'aplicacion-mayor': ['Bars 14–17: F7, B♭7, E♭. Over F7 (bar 14, where the voice holds) its tritone A with E♭ and the replacements C with G♭, E♭ with A.',
                         'F7’s tritone A/E♭ slides a semitone down, both notes, into B♭7’s A♭/D.', 'B♭7 (the voice holds), its tritone low, then high.',
                         'Into E♭: A♭ falls to G, D rises to E♭.'],
    'aplicacion-secundario': ['Bars 3–5: E♭, then G7 over D (the dominant of C minor, the song’s VIm), into C minor 7.', 'G7’s tritone, B with F, on its last beat.',
                              'Into C minor: B rises to C, F falls to E♭.'],
    'aplicacion-cadena': ['Bars 21–24, the song’s chain: E♭, G7, A♭7, G7, C7, F minor. Each dominant’s tritone moves by semitones into the next one.',
                          'G7’s B/F rises to A♭7’s C/G♭; then A♭7’s tritone again, an octave lower.',
                          'Down a semitone into G7’s F/B (the voice holds), then C7’s E/B♭, and its replacement G/D♭.',
                          'Into F minor: G rises to A♭, D♭ falls to C.']}
DESC = {
    'aplicacion-menor': ('Graciano’s examples of use. For major and minor alike the shapes on the guitar are the same: find the tritone in the dominant, '
                         'replace it, find the resolution. In a minor key: the dominant resolving into a minor chord.'),
    'aplicacion-mayor': 'The same in a major key: the dominant into the key’s major chord, here with the dominant before it (V of V) leading in by its own tritone.',
    'aplicacion-secundario': 'The same on a secondary dominant: the dominant of another of the key’s chords (in E♭, G7 into C minor).',
    'aplicacion-cadena': 'Secondary dominants in a row, resolving to major or minor chords: each with its tritone, sometimes its replacement a minor 3rd up after it.'}


def ours_bars(id_):
    out = []
    for n, (songbar, chords, ev) in enumerate(OURS[id_]):
        out.append(bar([c for c, _ in chords], Cad(ev).items(NEAR[id_], grips=GI), NOTES[id_][n] if n < len(NOTES[id_]) else ''))
    return out


APP = [
    ('aplicacion-menor', 'In a minor key', HP1, 'Tonalidad menor: A minor, F7, E7, then over E7 its tritone and the other one, each resolving into A minor'),
    ('aplicacion-mayor', 'In a major key', HP2, 'Tonalidad mayor: C, A♭7, G7, then over G7 its tritones, resolving into C'),
    ('aplicacion-secundario', 'On a secondary dominant', HP3, 'C, D♯7, E7 (V of the VIm), the tritones over E7, into A minor'),
    ('aplicacion-cadena', 'Through a chain of dominants', HP4, 'C, D7, G7, C, C7, F, G7, C, A7, D minor, A♭7, G7, C, G7, C: secondary dominants each with its tritone'),
]
for id_, title, h, txt in APP:
    ex('aplicacion', id_, title, DESC[id_],
       dict(where=where(49), text=txt + '. Played here: ' + ('his stroke and the first tritone after it.' if id_ != 'aplicacion-cadena' else 'his second bar’s last beat and the next.'),
            items=(Cad(h.ev[8:10]).items(2, grips=GQ2) if id_ != 'aplicacion-cadena' else Cad(h.ev[7:9]).items(4)), whose=OWN, played=''),
       ours_bars(id_))

SECTIONS = [dict(id='diatonica', title='Reharmonizing with the key’s chords', part='Exercises', ex=EXS['diatonica']),
            dict(id='tritonal', title='Tritone substitutes', part='Exercises', ex=EXS['tritonal']),
            dict(id='disminuidos', title='Diminished chords for the dominant', part='Exercises', ex=EXS['disminuidos']),
            dict(id='cliche8', title='The line cliché from the octave', part='Exercises', ex=EXS['cliche8']),
            dict(id='cliche5', title='The line cliché from the 5th', part='Exercises', ex=EXS['cliche5']),
            dict(id='tritono', title='The tritone', part='Exercises', ex=EXS['tritono']),
            dict(id='aplicacion', title='The tritone in use', part='Exercises', ex=EXS['aplicacion'])]


def _labels():
    for sid, sec in EXS.items():
        for e in sec:
            for it in (e['quote'].get('items') or []):
                if it[0] == 'P' and '|' not in it[3]: it[3] += '|his notes'
            for b in e['bars']:
                for it in b['items']:
                    if it[0] == 'P' and '|' not in it[3]:
                        if b['chords'] and len(set(b['chords'])) == 1: it[3] += '|over ' + nd(b['chords'][0])
                        else: it[3] += '|the tritones' if sid in ('tritono', 'aplicacion') else '|the line'


_labels()
