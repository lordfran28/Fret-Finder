"""Tango, the bass: Graciano's bordoneos (Método de guitarra tango, ch. 2, pp. 21–25 of the owner's copy).
A bordoneo is a phrase on the three bass strings. Each opens with Graciano's own figure (its first beat or two),
then the same figure where Очи чёрные needs it, inside the sincopado of chapter 1, closed grips around the 5th fret.
Graciano's examples are in A minor and its relatives, the key of Очи чёрные, so where his figure leads to E7 or
A minor, ours is the same notes; to D minor it is his figure moved to D, as his preface asks (move them to other keys)."""
import sys
sys.path.insert(0, '/home/claude/studies'); sys.path.insert(0, '/home/claude/studies/tango')
from kit_study import OPEN, N, nn
from entry import K, st, G4, ACC, SINC, sincopado

S16 = 0.25


def on(s, name):
    f = N(name) - OPEN[6 - s]
    assert 0 <= f <= 12, (s, name, f)
    return [s, f]


def run(notes, durs, over):
    """notes: [(string, 'D3'), ...] on the bass strings"""
    return ['R', [on(s, n) for s, n in notes], list(durs), over]


def where(p): return f'Método de guitarra tango, p. {p}'


OWN = dict(whose='Graciano’s own')
PL = 'Played here: his figure and the bar it leads into (his chords are ours, as he writes them in slashes or plain notes).'
E7o = [0, -1, 6, 7, 5, -1]          # E7 with the open low E as its bass (E2, G#3, D4, E4)
G = dict(G4, **{'E7o': E7o, 'E7/D': [-1, 5, 6, 7, 5, -1], 'Am/G': [3, -1, -1, 5, 5, 5], 'Dm/C': [-1, 3, 3, 2, 3, -1]})

SINC3 = SINC                         # bass, chord, bass, chord: three beats; the 4th is free for the bordoneo


def lead(c, fig_items, rest=0.0):
    """a bar of sincopado on c whose 4th beat holds a bordoneo (after `rest` beats of silence)"""
    its = [K(c, G[c], SINC3)]
    if rest: its.append(['W', rest])
    return its + fig_items


# targets on Очи чёрные: into A minor on the low E string (A2, 5th fret), into E7 and D minor on the A string
APP = {
    'doble-asc': dict(rest=0.5, Am=[(6, 'G2'), (6, 'G#2')], E7=[(5, 'D3'), (5, 'D#3')], Dm=[(5, 'C3'), (5, 'C#3')]),
    'doble-desc': dict(rest=0.5, Am=[(6, 'B2'), (6, 'Bb2')], E7=[(5, 'F#3'), (5, 'F3')], Dm=[(5, 'E3'), (5, 'Eb3')]),
    'triple': dict(rest=0.25, Am=[(6, 'F#2'), (6, 'G2'), (6, 'G#2')], E7=[(5, 'C#3'), (5, 'D3'), (5, 'D#3')], Dm=[(5, 'B2'), (5, 'C3'), (5, 'C#3')]),
    'cuadruple': dict(rest=0.0, Am=[(6, 'F2'), (6, 'F#2'), (6, 'G2'), (6, 'G#2')], E7=[(5, 'C3'), (5, 'C#3'), (5, 'D3'), (5, 'D#3')],
                      Dm=[(5, 'Bb2'), (5, 'B2'), (5, 'C3'), (5, 'C#3')]),
}
SEQ = ['Am', 'Dm', 'Am', 'E7', 'Am']          # Очи чёрные, from the turn: A minor, D minor, A minor, E7, A minor


def app_bars(kind):
    a = APP[kind]; out = []
    for i, c in enumerate(SEQ):
        if i + 1 < len(SEQ):
            nx = SEQ[i + 1]; notes = a[nx]
            out.append(dict(chords=[c], note='', items=lead(c, [run(notes, [S16] * len(notes), nx)], a['rest'])))
        else:
            out.append(dict(chords=[c], note='', items=[sincopado(c, G[c])]))
    return out


def app_quote(kind, notes, s, target, grip):
    """his figure on the 4th beat, then the bar it leads into (bass, chord, bass, chord)"""
    a = APP[kind]
    return [['W', 3 + a['rest']], run(notes, [S16] * len(notes), target), K(target, grip, SINC + [(1, '-')])]


A7 = [5, -1, 5, 6, 5, -1]
EX_A = []
EX_A.append(dict(
    id='apoyatura-doble-asc', title='Two notes up into the bass',
    idea=('The simplest bordoneo: two sixteenths climbing a semitone at a time into the next chord’s bass, from a whole tone below, on the A string or the low E string. '
          'On the A string a finger for each fret; on the low E Graciano slides the index alone, fret to fret.'),
    quote=dict(where=where(21), text='Como apoyatura doble, ascendente, on the A string: D, D♯ into E7, then a bar of E7 (fingers 1, 2, 3).',
               items=app_quote('doble-asc', [(5, 'D3'), (5, 'D#3')], 5, 'E7', G['E7']), **OWN, played=PL),
    bars=app_bars('doble-asc')))
EX_A[-1]['bars'][0]['note'] = ('On Очи чёрные after the turn: A minor, D minor, A minor, E7, A minor, a bar of sincopado each, the 4th beat free. '
                               'Into D minor: C, C♯ up the A string (3rd, 4th fret) to D; into A minor: G, G♯ up the low E (3rd, 4th) to A; into E7: D, D♯ up the A string (5th, 6th) to E.')
EX_A.append(dict(
    id='apoyatura-doble-desc', title='Two notes down into the bass',
    idea='The same from a whole tone above, falling by semitones; on the A string the ring finger slides down, on the low E the fingers go 3, 2, 1.',
    quote=dict(where=where(21), text='Descendente, on the A string: F♯, F into E7 (the ring finger each time).',
               items=app_quote('doble-desc', [(5, 'F#3'), (5, 'F3')], 5, 'E7', G['E7']), **OWN, played=PL),
    bars=app_bars('doble-desc')))
EX_A[-1]['bars'][0]['note'] = 'Into D minor: E, E♭ down the A string (7th, 6th fret); into A minor: B, B♭ down the low E (7th, 6th); into E7: F♯, F (9th, 8th).'
EX_A.append(dict(
    id='apoyatura-triple', title='Three notes up into the bass',
    idea='Three sixteenths from a minor 3rd below, after a sixteenth rest.',
    quote=dict(where=where(22), text='Como apoyatura triple, on the A string: C♯, D, D♯ into E7 (fingers 1, 2, 3, then 3 again).',
               items=app_quote('triple', [(5, 'C#3'), (5, 'D3'), (5, 'D#3')], 5, 'E7', G['E7']), **OWN, played=PL),
    bars=app_bars('triple')))
EX_A[-1]['bars'][0]['note'] = 'Into D minor: B, C, C♯ up the A string (2nd–4th fret); into A minor: F♯, G, G♯ up the low E (2nd–4th); into E7: C♯, D, D♯ (4th–6th).'
EX_A.append(dict(
    id='apoyatura-cuadruple', title='Four notes up into the bass',
    idea=('Four sixteenths from a major 3rd below, filling the whole 4th beat. Graciano’s note: one finger sliding along the neck is very common here; '
          'its small margin of error gives the tango more expression.'),
    quote=dict(where=where(22), text='Como apoyatura cuádruple, on the low E string: F, F♯, G, G♯ into A7, the index alone.',
               items=app_quote('cuadruple', [(6, 'F2'), (6, 'F#2'), (6, 'G2'), (6, 'G#2')], 6, 'A7', A7), **OWN, played=PL),
    bars=app_bars('cuadruple')))
EX_A[-1]['bars'][0]['note'] = 'Into D minor: B♭, B, C, C♯ (A string, 1st–4th fret); into A minor: F, F♯, G, G♯ (low E, 1st–4th); into E7: C, C♯, D, D♯ (A string, 3rd–6th).'

# ---------- as a melodic phrase ----------
TO_V = [(6, 'A2'), (6, 'G#2'), (6, 'A2'), (6, 'B2'), (5, 'C3'), (5, 'D3'), (5, 'D#3')]
TO_I = [(5, 'E3'), (4, 'G3'), (5, 'F3'), (5, 'E3'), (5, 'D3'), (6, 'C3'), (6, 'B2')]
TO_I_D = [(4, 'A3'), (3, 'C4'), (4, 'Bb3'), (4, 'A3'), (4, 'G3'), (5, 'F3'), (5, 'E3')]     # the same into D minor, one string higher


def half_bar(c, grip):
    """bass and chord on the first half, then a sixteenth rest: the phrase fills the rest of the bar"""
    return K(c, grip, flat2([(0.5, 'B')], st(1, 'C'), [(0.5, '-'), (0.25, '-')]))


def flat2(*p):
    out = []
    for x in p: out += x
    return out


EX_F = []
EX_F.append(dict(
    id='frase-a-la-dominante', title='A phrase up to the dominant',
    idea=('A whole bass phrase in place of a single approach: in a minor key, from the tonic, a turn round it (down a semitone and back), then up the scale to the dominant, '
          'the last step a semitone. Two beats of sixteenths. Graciano’s fingers: 2, 1, 2, 4 on the low E string (5th position), then 1, 2, 3 on the A string, the 3rd sliding into E.'),
    quote=dict(where=where(23), text='Como frase melódica, para ir al dominante en tonalidad menor: into E7. Played here: its first beat, the turn round A.',
               items=[['W', 2.25], run(TO_V[:3], [S16] * 3, 'Am')], **OWN, played=''),
    bars=[dict(chords=['Am'], note='Очи чёрные’s A minor before E7: bass and chord, then the phrase from A up to E, as Graciano has it, since his example is in your key.',
               items=[half_bar('Am', G['Am']), run(TO_V, [S16] * 7, 'Am')]),
          dict(chords=['E7'], note='', items=[sincopado('E7', G['E7'])])]))
EX_F.append(dict(
    id='frase-a-la-tonica', title='A phrase down to the tonic',
    idea=('From the dominant’s root, a turn above it (up to the ♭7 of the key, down a step), then down the scale to the tonic. All in the 5th position: '
          'fingers 3, 1, 4, 3, 1, 4, 3, then 1 on the A.'),
    quote=dict(where=where(23), text='Para ir a la tónica en tonalidad menor: E, G, F, E… into A. Played here: its first beat.',
               items=[['W', 2.25], run(TO_I[:3], [S16] * 3, 'E7')], **OWN, played=''),
    bars=[dict(chords=['E7'], note='Очи чёрные’s E7 before A minor: the phrase from E down to A, Graciano’s own notes, since the song is in his key.',
               items=[half_bar('E7', G['E7']), run(TO_I, [S16] * 7, 'E7')]),
          dict(chords=['Am'], note='', items=[sincopado('Am', G['Am'])]),
          dict(chords=['A7'], note='Then moved to D minor, for the song’s turn into D minor, over A7 (its dominant) at the 5th fret: the same shape and fingers one string higher, A on the D string (7th fret), the C on the G string (5th), down to E on the A string (7th) and into D (5th).',
               items=[half_bar('A7', G['A7']), run(TO_I_D, [S16] * 7, 'A7')]),
          dict(chords=['Dm'], note='', items=[sincopado('Dm', G['Dm'])])]))

CLOSE = [(5, 'F3'), (5, 'E3'), (5, 'D3'), (5, 'C3'), (6, 'B2'), (6, 'A2'), (6, 'G#2')]
EX_F.append(dict(
    id='frase-final', title='A phrase to end the song',
    idea=('The end of a tango in a minor key: over the last E7, a chord, then the bass falls from F (the ♭9) down the harmonic minor scale to G♯, '
          'and the last bar is three short chords, tonic, dominant, tonic, and a rest. Fingers 4, 4, 2, 1, 4, 2, 1, the hand around the 4th fret.'),
    quote=dict(where=where(23), text='Como frase para cerrar la obra, en tonalidad menor: the E7 stroke and the F. Played here: those, the first beat and a half.',
               items=[K('E7', G['E7'], [(0.5, 'A')]), run(CLOSE[:1], [1.0], 'E7')], **OWN, played=''),
    bars=[dict(chords=['E7'], note='The last four bars of Очи чёрные (E7, E7, A minor, A minor) closed the way Graciano closes his A minor example: a bar of sincopado on E7, then the phrase, then the three chords.',
               items=[sincopado('E7', G['E7'])]),
          dict(chords=['E7'], note='', items=[K('E7', G['E7'], [(0.5, 'A')]), run(CLOSE, [1.0, S16, S16, 0.5, 0.5, 0.5, 0.5], 'E7')]),
          dict(chords=['Am', 'E7', 'Am'], note='', items=[K('Am', G['Am'], [(0.5, 'A', ACC), (0.5, '-')]), K('E7', G['E7'], [(0.5, 'A'), (0.5, '-')]),
                                                           K('Am', G['Am'], [(0.5, 'A', ACC), (1.5, '-')])])]))

LEV = [(5, 'B2'), (5, 'C3'), (5, 'C#3'), (5, 'D3'), (5, 'D#3')]
LEV_D = [(5, 'A2'), (5, 'Bb2'), (5, 'B2'), (5, 'C3'), (5, 'C#3')]
LEV_A = [(6, 'E2'), (6, 'F2'), (6, 'F#2'), (6, 'G2'), (6, 'G#2')]
EX_F.append(dict(
    id='levare', title='A pick-up into the first bar',
    idea=('The levare: on the “and” of 3 the 5th below the coming chord’s root, then four sixteenths climbing by semitones into it. For the start of the song or of a section, '
          'into the tonic (major or minor) or into a dominant.'),
    quote=dict(where=where(24), text='Como levare: B, then C, C♯, D, D♯ into E7 (fingers 1, 1, 2, 3, 3: the index slides, then the ring finger).',
               items=[['W', 2.5], run(LEV, [0.5] + [S16] * 4, 'E7'), K('E7', G['E7'], SINC + [(1, '-')])], **OWN, played='Played here: his pick-up and the bar it leads into.'),
    bars=[dict(chords=[], note='Into the start of Очи чёрные’s second half, D minor: A (the open A string), then B♭, B, C, C♯ up the A string to D.',
                items=[['W', 2.5], run(LEV_D, [0.5] + [S16] * 4, 'Dm')]),
          dict(chords=['Dm'], note='', items=[sincopado('Dm', G['Dm'])]),
          dict(chords=[], note='Into A minor: the open low E, then F, F♯, G, G♯ up the low E string to A.',
               items=[['W', 2.5], run(LEV_A, [0.5] + [S16] * 4, 'Am')]),
          dict(chords=['Am'], note='', items=[sincopado('Am', G['Am'])])]))

# ---------- the bass to the 3rd, to the 7th ----------
def inv_bar(c, grip, notes, c2, grip2, upper):
    """bass, chord; two sixteenths and an eighth walking to the new bass; the chord over it (Graciano's rhythm)"""
    return [K(c, grip, [(0.5, 'B'), (1, 'C')]), run(notes, [S16, S16, 0.5], c2), K(c2, grip2, [(1.5, upper)])]


INV3 = [('Dm', G['Dm'], [(5, 'Eb3'), (5, 'E3'), (5, 'F3')], 'Dm/F', G['Dm/F'], [4, 3, 2]),
        ('Am', G['Am'], [(6, 'Bb2'), (6, 'B2'), (6, 'C3')], 'Am/C', G['Am/C'], [4, 3, 2]),
        ('E7', E7o, [(6, 'F#2'), (6, 'G2'), (6, 'G#2')], 'E7/G#', G['E7/G#'], [4, 3, 2])]
INV7 = [('Dm', G['Dm'], [(5, 'C#3'), (5, 'C3')], 'Dm/C', G['Dm/C'], [4, 3, 2]),
        ('Am', G['Am'], [(6, 'Ab2'), (6, 'G2')], 'Am/G', G['Am/G'], [3, 2, 1]),
        ('E7', G['E7'], [(5, 'D#3'), (5, 'D3')], 'E7/D', G['E7/D'], [4, 3, 2])]
EX_I = []
qA, qA3 = [5, 7, 7, 6, -1, -1], [9, -1, 7, 9, -1, -1]            # his notes: A under E, A, C#; then C# under A and E
EX_I.append(dict(
    id='bajo-a-la-tercera', title='The bass walks up to the 3rd',
    idea=('Turn the chord to its 3rd in the bass on a weak beat: from the root, two sixteenths and an eighth climbing to the 3rd, then the chord again over the new bass. '
          'A major or dominant chord climbs a tone and two semitones (fingers 1, 2, 3); a minor chord two semitones and a tone (fingers 1, 2, 2).'),
    quote=dict(where=where(24), text='Como inversión de bajos a la 3era., on the low E string: A major, the bass A, then B, C, C♯; the chord over C♯.',
               items=[K('A', qA, [(0.5, 'B'), (1, 'C')]), run([(6, 'B2'), (6, 'C3'), (6, 'C#3')], [S16, S16, 0.5], 'A'), K('A/C#', qA3, [(1.5, [4, 3])])], **OWN, played='Played here: that bar.'),
    bars=[dict(chords=[c, c2], note='', items=inv_bar(c, g, n, c2, g2, up)) for c, g, n, c2, g2, up in INV3]))
EX_I[-1]['bars'][0]['note'] = ('On Очи чёрные’s three chords. D minor: D, then E♭, E, F up the A string (5th to 8th fret), the chord over F. '
                               'A minor: A, then B♭, B, C up the low E (5th to 8th). E7, from the open low E: F♯, G, G♯ (2nd to 4th fret).')
EX_I.append(dict(
    id='bajo-a-la-septima', title='The bass walks down to the 7th',
    idea=('Turn a dominant or minor chord to its 7th in the bass: from the root, down by semitones (a sixteenth on the root, a sixteenth, then the 7th as an eighth), the chord over it. '
          'Fingers 3, 2, 2. Graciano advises against doing this to a major 7 chord as a bordoneo.'),
    quote=dict(where=where(25), text='Como inversión de bajos a la 7ma., on the A string: E7, the bass E, then E, D♯, D; the chord over D.',
               items=[K('E7', G['E7'], [(0.5, 'B'), (1, 'C')]), run([(5, 'E3'), (5, 'D#3'), (5, 'D3')], [S16, S16, 0.5], 'E7/D'), K('E7/D', [-1, 5, 6, 4, 5, -1], [(1.5, [4, 3, 2])])],
               **OWN, played='Played here: that bar.'),
    bars=[dict(chords=[c, c2], note='', items=[K(c, g, [(0.5, 'B'), (1, 'C')]), run([(n[0][0], nn(OPEN[6 - n[0][0]] + g[6 - n[0][0]]))] + n, [S16, S16, 0.5], c2), K(c2, g2, [(1.5, up)])])
          for c, g, n, c2, g2, up in INV7]))
EX_I[-1]['bars'][0]['note'] = ('D minor: D, C♯, C down the A string (5th to 3rd fret), the chord over C. A minor: A, A♭, G down the low E (5th to 3rd), the chord on the top strings. '
                               'E7: E, D♯, D down the A string (7th to 5th), as Graciano has it.')

SECTIONS = [dict(id='apoyaturas', title='Leaning into the bass', part='Exercises', ex=EX_A),
            dict(id='frases', title='Bass phrases', part='Exercises', ex=EX_F),
            dict(id='inversiones', title='The bass to the 3rd and the 7th', part='Exercises', ex=EX_I)]
