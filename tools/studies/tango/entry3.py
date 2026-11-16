"""Milonga, the right hand and the bass: Graciano, Método de guitarra tango, ch. 19, pp. 159–163 of the owner's copy.
The milonga is in 2/4. Each rhythm opens with Graciano's own bar (on A minor, his key and the key of Очи чёрные), then
the same strokes on Очи чёрные's chords (D minor, A minor, E7, A minor), closed grips at the 5th fret.
Every stroke is a down-stroke; the short silence between chord and bass (his comma) is the left hand easing off."""
import sys
sys.path.insert(0, '/home/claude/studies'); sys.path.insert(0, '/home/claude/studies/tango')
from kit_study import OPEN, N
from entry import K, arr, G4

GM = {'Dm': [-1, 5, 7, 7, 6, 5],      # D3 under A3 D4 F4 A4
      'Am': [5, -1, 7, 5, 5, 5],      # A2 under A3 C4 E4 A4: Graciano's own notes on p. 159
      'E7': [-1, 7, 9, 7, 9, 7]}      # E3 under B3 D4 G#4 B4
HI = {'Dm': [-1, -1, 0, 10, 10, 10],  # F4 A4 D5 at the 10th, the open D below
      'Am': [-1, 0, -1, 9, 10, 8],    # E4 A4 C5 at the 8th–10th, the open A below: his notes on p. 160
      'E7': [0, -1, -1, 7, 9, 7]}     # D4 G#4 B4 at the 7th–9th, the open low E below
SEQ = ['Dm', 'Am', 'E7', 'Am']
NOTE = 'On Очи чёрные’s chords, D minor, A minor, E7, A minor, a bar of 2/4 each.'
POS = ('The grips: D minor as a barre at the 5th fret, root on the A string; A minor with its root on the low E at the 5th fret, the A string muted, the chord on the top four strings; '
       'E7 as a barre at the 7th fret, root on the A string.')


def U(g):
    s = [6 - i for i in range(6) if g[i] >= 0]
    return s[1:]


def B(g):
    return [[6 - i for i in range(6) if g[i] >= 0][0]]


def basic(c, g=None, drag=None):
    g = g or GM[c]
    hits = [(0.5, U(g)), (0.25, '-'), (0.25, B(g)), (0.25, U(g)), (0.25, '-')]
    if drag: return [K(c, g, hits), arr(GM[drag], drag)]
    return [K(c, g, hits + [(0.5, B(g))])]


def octava(c, drag=None):
    g, h = GM[c], HI[c]
    hs = [6 - i for i in range(6) if h[i] > 0]          # the fretted notes of the upper chord, low to high
    first = [K(c, g, [(0.5, U(g)), (0.25, '-')])]
    up = [(0.25, hs[:1]), (0.25, hs[1:]), (0.25, '-')]
    if drag: return first + [K(c, h, up), arr(GM[drag], drag)]
    return first + [K(c, h, up + [(0.5, [6 - i for i in range(6) if h[i] == 0])])]


def contra(c):
    g = GM[c]
    return [K(c, g, [(0.25, '-'), (0.25, U(g)), (0.25, '-'), (0.25, B(g)), (0.5, U(g)), (0.5, '-')])]


def candombe(c):
    g = GM[c]
    return [K(c, g, [(0.25, B(g)), (0.25, U(g)), (0.25, '-'), (0.25, B(g)), (0.5, U(g)), (0.5, U(g))])]


def candombe_st(c):
    g = GM[c]
    return [K(c, g, [(0.25, U(g)), (0.25, U(g)), (0.25, '-'), (0.25, U(g)), (0.25, U(g)), (0.25, '-'), (0.25, U(g)), (0.25, '-')])]


def pesante(c, g):
    return K(c, g, [(0.75, 'A'), (0.25, '-')])


def bars_of(fn, drag=False):
    out = []
    for i, c in enumerate(SEQ):
        nxt = SEQ[i + 1] if drag and i + 1 < len(SEQ) else None
        its = fn(c, drag=nxt) if drag else fn(c)
        out.append(dict(chords=[c], note='', items=its))
    return out


def where(p): return f'Método de guitarra tango, p. {p}'


OWN = dict(whose='Graciano’s own', played='Played here: that bar.')
EX = []
EX.append(dict(
    id='milonga-basico', title='Milonga, the basic rhythm',
    idea=('Chord and bass, chord and bass, in the milonga’s 3+1+2+2 sixteenths: the chord a dotted eighth, the bass a sixteenth, then chord and bass as eighths. '
          'Every stroke a down-stroke of the pick (or the thumb). Between each chord and the bass after it, a small silence made by easing the left hand off the strings.'),
    quote=dict(where=where(159), text='Básico, written out on A minor: A, C, E, A over the low A.', items=basic('Am'), **OWN),
    bars=bars_of(basic)))
EX[-1]['bars'][0]['note'] = NOTE + ' ' + POS
EX.append(dict(
    id='milonga-arrastre', title='Milonga with the arrastre',
    idea='The same, with the last eighth a drag: touch the bass string three frets below, muffled, and slide into the next downbeat’s bass.',
    quote=dict(where=where(159), text='Variación 1, básico con arrastre: the last eighth an x with a slide line. On his A minor.', items=basic('Am', drag='Dm'), **OWN),
    bars=bars_of(basic, drag=True)))
EX[-1]['bars'][0]['note'] = NOTE + ' The drag goes into D on the A string, A on the low E, E on the A string.'
EX.append(dict(
    id='milonga-octava', title='Milonga with a change of octave',
    idea=('From the piano: the chord, then a higher inversion of it, its lowest note first on the sixteenth and the rest of it on the eighth, and a deep bass to end the bar.'),
    quote=dict(where=where(160), text='Variación 2, sobre Am: A, C, E, A; then E; then A and C above it; then the low A.', items=octava('Am'), **OWN),
    bars=bars_of(octava)))
EX[-1]['bars'][0]['note'] = (NOTE + ' The upper chords: F, A, D across the 10th fret over the open D (D minor); E, A, C at the 8th–10th over the open A (A minor, Graciano’s own notes); '
                             'D, G♯, B at the 7th–9th over the open low E (E7).')
EX.append(dict(
    id='milonga-octava-arrastre', title='Milonga, the change of octave with the arrastre',
    idea='The change of octave with the last eighth a drag into the next bass.',
    quote=dict(where=where(160), text='Variación 3, as written in slashes, on A minor.', items=octava('Am', drag='Dm'), **OWN),
    bars=bars_of(octava, drag=True)))
EX.append(dict(
    id='milonga-contratiempo', title='Milonga off the beat',
    idea=('A sixteenth rest, the chord on the next sixteenth, the bass, then the chord on 2 and a rest. Only for a bar here and there: repeated, it loses its effect and unsettles the time.'),
    quote=dict(where=where(160), text='Contratiempo, in slashes; played on A minor.', items=contra('Am'), **OWN),
    bars=[dict(chords=['Dm'], note='The basic rhythm on D minor and E7, off the beat on the A minor bars, as Graciano advises: never two bars running.', items=basic('Dm')),
          dict(chords=['Am'], note='', items=contra('Am')), dict(chords=['E7'], note='', items=basic('E7')), dict(chords=['Am'], note='', items=contra('Am'))]))
EX.append(dict(
    id='milonga-candombe', title='Milonga-candombe',
    idea=('The rhythm of the milonga-candombes (Oro y plata, Azabache, Papá Baltasar): bass, chord, bass in a syncopated first beat, then two eighths of chord. '
          'Then the same with the chord only, very short.'),
    quote=dict(where=where(161), text='Candombe, sobre E7: E, the chord G♯, D, E, E again, then the chord twice.', items=candombe('E7'), **OWN),
    bars=bars_of(candombe) + bars_of(candombe_st)))
EX[-1]['bars'][0]['note'] = NOTE + ' First with the bass, then four bars of the chord alone.'
EX.append(dict(
    id='milonga-pesante', title='Pesante in milonga',
    idea='In 2/4 the pesante is a chord on each beat, two quarters to the bar. For the cadences.',
    quote=dict(where=where(161), text='Pesante en milonga: two quarter-note chords. Played on A minor.', items=[pesante('Am', GM['Am']), pesante('Am', GM['Am'])], **OWN),
    bars=[dict(chords=['Am'], note='Two bars of the basic rhythm on A minor, then the cadence of Очи чёрные in pesante: D minor, D minor over F; E7, E7 over G♯; A minor.', items=basic('Am')),
          dict(chords=['Am'], note='', items=octava('Am')),
          dict(chords=['Dm', 'Dm/F'], note='', items=[pesante('Dm', G4['Dm']), pesante('Dm/F', G4['Dm/F'])]),
          dict(chords=['E7', 'E7/G#'], note='', items=[pesante('E7', G4['E7']), pesante('E7/G#', G4['E7/G#'])]),
          dict(chords=['Am'], note='', items=[K('Am', G4['Am'], [(0.5, 'A'), (1.5, '-')])])]))

# ---------- milongueo ----------
def S(s, name): f = N(name) - OPEN[6 - s]; assert 0 <= f <= 12, (s, name); return [s, f]


def milongueo(c, notes):
    """eight sixteenths: the bass on the 1st, 4th and 7th (3+3+2), the chord's notes between"""
    return ['R', [S(s, n) for s, n in notes], [0.25] * 8, c]


MIL = {
    'Am': [(6, 'A2'), (3, 'C4'), (4, 'A3'), (5, 'F3'), (3, 'C4'), (4, 'A3'), (5, 'E3'), (3, 'C4')],       # 1, b6, 5 under C and A: his own
    'E7': [(6, 'E2'), (2, 'B3'), (3, 'G#3'), (4, 'F3'), (2, 'B3'), (3, 'G#3'), (4, 'E3'), (2, 'B3')],     # 1, b2, 1 under B and G#: his own
    'Dm': [(5, 'D3'), (2, 'F4'), (3, 'D4'), (6, 'Bb2'), (2, 'F4'), (3, 'D4'), (6, 'A2'), (2, 'F4')],     # the same rule on D minor: 1, b6, 5 under F and D
}
EX.append(dict(
    id='milongueo', title='Milongueo',
    idea=('From the payadores: a bass in 3+3+2 (on the 1st, 4th and 7th sixteenth) with the chord’s notes filling every sixteenth between, an unbroken run of sixteenths. '
          'On a minor chord the bass goes root, ♭6, 5; on the dominant root, ♭2, root. For a phrase or a section, not the whole song. Practise it slowly, then faster, keeping the time.'),
    quote=dict(where=where(161), text='Milongueo on A minor: A in the bass, C and A above, F in the bass, C and A, E in the bass, C. Played here: his first bar.',
               items=[milongueo('Am', MIL['Am'])], whose='Graciano’s own', played=''),
    bars=[dict(chords=[c], note='', items=[milongueo(c, MIL[c])]) for c in SEQ]))
EX[-1]['bars'][0]['note'] = ('On D minor the same rule: D, then F and D above, B♭ in the bass (low E string, 6th fret), F and D, A (5th fret), F. '
                             'The A minor and E7 bars are Graciano’s own, since his example is in the song’s key; the E7 bar is in open position.')

SECTIONS = [dict(id='milonga', title='Milonga', part='Exercises', ex=EX)]

from quotes import trim as _trim_quotes   # quotes stay a beat or two
_trim_quotes(SECTIONS)
