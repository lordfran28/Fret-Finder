"""Vals, the tango waltz: Graciano, Método de guitarra tango, ch. 20, pp. 171–174 of the owner's copy.
His examples are in A (major and minor); ours are the same figures in G, on Я вас любил (in 3/4), with the song's own
grips (barre chords around the 3rd and 5th fret), as Graciano asks: move them to other keys and try them on a piece you know."""
import sys
sys.path.insert(0, '/home/claude/studies'); sys.path.insert(0, '/home/claude/studies/tango')
from kit_study import OPEN, N
from entry import K, ACC

YV = {'G': [3, 5, 5, 4, 3, 3], 'Cmaj7': [-1, 3, 5, 4, 5, 3], 'Cm': [-1, 3, 5, 5, 4, 3], 'D7': [-1, 5, 7, 5, 7, 5]}   # the song's own grips
SEQ = ['G', 'Cmaj7', 'Cm', 'D7']
NOTE = ('On the chords of Я вас любил’s first phrase (bars 8–14 of your arrangement): G, C major 7, C minor, D7, a bar each, with the song’s own grips: '
        'G as a barre at the 3rd fret, C major 7 and C minor from the A string at the 3rd, D7 from the A string at the 5th. The chord strokes take the D, G and B strings.')
CH = [4, 3, 2]                         # the chord: three notes in the middle, as Graciano writes it (A, C, E over the bass)


def bass(g): return [[6 - i for i in range(6) if g[i] >= 0][0]]


def basico(c, g): return K(c, g, [(1, bass(g)), (0.5, CH), (0.5, '-'), (0.5, CH), (0.5, '-')])
def var1(c, g): return K(c, g, [(0.5, bass(g)), (0.5, CH[1:], -0.15), (0.5, CH), (0.5, '-'), (0.5, CH), (0.5, '-')])
def var2(c, g): return K(c, g, [(1, bass(g)), (2, CH)])
def var3(c, g): return K(c, g, [(0.5, 'A', ACC), (0.5, 'A', -0.1), (0.5, 'A'), (0.5, 'A', ACC), (0.5, 'A', -0.1), (0.5, 'A')])


def ours(fn): return [dict(chords=[c], note='', items=[fn(c, YV[c])]) for c in SEQ]


def where(p): return f'Método de guitarra tango, p. {p}'


OWN = dict(whose='Graciano’s own', played='Played here: that bar.')
AM = [5, -1, 7, 5, 5, -1]               # his A minor: A under A, C, E
A = [5, -1, 7, 6, 5, -1]                # A major: A under A, C#, E
A7 = [5, -1, 5, 6, 5, -1]               # A7: A under G, C#, E

EX_R = []
EX_R.append(dict(
    id='vals-basico', title='Vals, the basic rhythm',
    idea=('Bass, chord, chord. With a pick, three down-strokes; with the fingers, thumb, then the hand twice, downward, plucked together or strummed. The chords short.'),
    quote=dict(where=where(171), text='Básico, written out on A minor: the low A, then A, C, E twice, short.', item=basico('Am', AM), **OWN),
    bars=ours(basico)))
EX_R[-1]['bars'][0]['note'] = NOTE
EX_R.append(dict(
    id='vals-var1', title='Vals with a stroke on the “and” of 1',
    idea=('The bass as an eighth and a light stroke on the “and”: an up-stroke of the pick, or i-m-a upward, or the middle finger alone. Mixed in with the basic, to taste; not bar after bar.'),
    quote=dict(where=where(172), text='Variación 1 on A minor: A, then C and E on the “and”, then the chord twice.', item=var1('Am', AM), **OWN),
    bars=[dict(chords=['G'], note='Twice the basic, twice the variation: G, C major 7, then C minor and D7 with the stroke on the “and”.', items=[basico('G', YV['G'])]),
          dict(chords=['Cmaj7'], note='', items=[basico('Cmaj7', YV['Cmaj7'])]),
          dict(chords=['Cm'], note='', items=[var1('Cm', YV['Cm'])]), dict(chords=['D7'], note='', items=[var1('D7', YV['D7'])])]))
EX_R.append(dict(
    id='vals-var2', title='Vals, bass and a long chord',
    idea='The bass, then the chord held two beats. Calm: for the cadence of a phrase, or to start a new section more relaxed.',
    quote=dict(where=where(172), text='Variación 2 on A minor.', item=var2('Am', AM), **OWN),
    bars=ours(var2)))
EX_R.append(dict(
    id='vals-var3', title='Vals in six eighths, accented in three',
    idea=('The opposite of the calm one: six eighths, accented on the 1st and 4th, the 6/8 felt over the 3/4. Taken from the Peruvian vals. With a pick, down and up, the accent every three eighths; '
          'with the fingers, strummed.'),
    quote=dict(where=where(172), text='Variación 3, in slashes; played on A minor.', item=var3('Am', AM), **OWN),
    bars=ours(var3)))
Eb7, D7c, Gc = [-1, 6, 5, 6, 4, -1], [-1, 5, 4, 5, 3, -1], YV['G']
F7, E7 = [-1, 8, 7, 8, 6, -1], [-1, 7, 6, 7, 5, -1]      # his notes: F, A, E♭, F and E, G♯, D, E


def fin(n, c1, g1, c2, g2):
    """the two closing formulas on the bVI7-V7 cadence (dotted quarter, eighth, quarter; or eighth, quarter, eighth, quarter)"""
    if n == 1: r = [(1.5, 'A'), (0.5, 'A'), (1, 'A')]
    else: r = [(0.5, 'A'), (1, 'A'), (0.5, 'A'), (1, 'A')]
    return [K(c1, g1, r)], [K(c2, g2, r)]


def tail(I, gI, V, gV):
    return [dict(chords=[I, V], note='', items=[K(I, gI, [(1, 'A'), (1, '-')]), K(V, gV, [(1, 'A')])]),
            dict(chords=[I], note='', items=[K(I, gI, [(1, 'A'), (2, '-')])])]


for n in (1, 2):
    a, b = fin(n, 'Eb7', Eb7, 'D7', D7c)
    qa, qb = fin(n, 'F7', F7, 'E7', E7)
    EX_R.append(dict(
        id=f'vals-final-{n}', title=f'Vals, to end the song ({"first" if n == 1 else "second"} way)',
        idea=(('Two closing formulas, both from the Peruvian vals, on the cadence ♭VI7 to V7, then the tonic, the dominant and the tonic again, short. Pick one, never both; all down-strokes (or the thumb). '
               'Legato as written, or with a little staccato by easing the left hand. The first: dotted quarter, eighth, quarter.') if n == 1 else
              'The second brings back the 6/8 over the 3/4: eighth, quarter, eighth, quarter.'),
        quote=dict(where=where(173), text=f'Para final, the {"first" if n == 1 else "second"} formula on F7 and E7 (in A minor). Played here: those two bars.', items=qa + qb, **OWN),
        bars=[dict(chords=['Eb7'], note=('The same in G, the key of Я вас любил: E♭7 (the ♭VI7) and D7, root on the A string at the 6th and 5th fret, the same shape a fret apart; then G, D7, G. '
                                         'The cadence is Graciano’s, put in place of the song’s own last bars.') if n == 1 else '', items=a),
              dict(chords=['D7'], note='', items=b)] + tail('G', Gc, 'D7', YV['D7'])))

# ---------- bordoneos in the vals ----------
def S(s, name): f = N(name) - OPEN[6 - s]; assert 0 <= f <= 12, (s, name); return [s, f]


def R(notes, durs, over): return ['R', [S(s, n) for s, n in notes], durs, over]


def bord(c, g, walk, c2, g2, up):
    """bar 1: bass, chord, two eighths of the walk; bar 2: the new bass, then the chord held"""
    return [dict(chords=[c], note='', items=[K(c, g, [(1, bass(g)), (1, CH)]), R(walk, [0.5, 0.5], c2)]),
            dict(chords=[c2], note='', items=[K(c2, g2, [(1, bass(g2)), (2, up)])])]


def bq(g, c, walk):
    return [K(c, g, [(1, bass(g)), (1, CH)]), R(walk, [0.5, 0.5], c)]


EX_B = []
EX_B.append(dict(
    id='vals-tercera-menor', title='The bass to the 3rd, minor',
    idea='From the root up the scale to the minor 3rd: root, chord, then two eighths (root, 2nd) into the 3rd on the next downbeat, the chord held over it.',
    quote=dict(where=where(173), text='1, on A minor: A, the chord, A, B; then C. Played here: the first bar.', items=bq(AM, 'Am', [(6, 'A2'), (6, 'B2')]), **OWN),
    bars=bord('Cm', YV['Cm'], [(5, 'C3'), (5, 'D3')], 'Cm/Eb', [-1, 6, 5, 5, 4, -1], [4, 3, 2])))
EX_B[-1]['bars'][0]['note'] = 'On Я вас любил’s C minor (bar 11): C, the chord, C, D up the A string (3rd, 5th fret), into E♭ (6th fret) under G, C, E♭.'
EX_B.append(dict(
    id='vals-tercera-mayor', title='The bass to the 3rd, major',
    idea='On a major chord the walk goes root, 2nd, then a semitone more (the minor 3rd as a passing note) into the major 3rd.',
    quote=dict(where=where(173), text='2, on A major: A, the chord, B, C; then C♯. Played here: the first bar.', items=bq(A, 'A', [(6, 'B2'), (6, 'C3')]), **OWN),
    bars=bord('G', YV['G'], [(6, 'A2'), (6, 'Bb2')], 'G/B', [7, -1, 5, 7, 8, -1], [4, 3, 2])))
EX_B[-1]['bars'][0]['note'] = 'On G (bar 8): G, the chord, A, B♭ up the low E string (5th, 6th fret), into B (7th) under G, D, G.'
EX_B.append(dict(
    id='vals-tercera-dominante', title='The bass to the 3rd, dominant 7',
    idea='The same on a dominant 7 chord: root, 2nd, ♭3 into the major 3rd.',
    quote=dict(where=where(173), text='3, on A7: A, the chord, B, C; then C♯. Played here: the first bar.', items=bq(A7, 'A7', [(6, 'B2'), (6, 'C3')]), **OWN),
    bars=bord('D7', YV['D7'], [(5, 'E3'), (5, 'F3')], 'D7/F#', [-1, 9, -1, 7, 10, 8], [3, 2, 1])))
EX_B[-1]['bars'][0]['note'] = 'On D7 (bars 13–14): D, the chord, E, F up the A string (7th, 8th fret), into F♯ (9th) under D, A, C.'
EX_B.append(dict(
    id='vals-septima', title='The bass down to the 7th of the dominant',
    idea='From the root down by semitones to the 7th: root, chord, root, a semitone below; the 7th on the next downbeat.',
    quote=dict(where=where(173), text='4, on A7: A, the chord, A, A♭; then G. Played here: the first bar.', items=bq(A7, 'A7', [(6, 'A2'), (6, 'Ab2')]), **OWN),
    bars=bord('D7', YV['D7'], [(5, 'D3'), (5, 'Db3')], 'D7/C', [-1, 3, 4, 2, 3, -1], [4, 3, 2])))
EX_B[-1]['bars'][0]['note'] = 'On D7: D, the chord, D, D♭ down the A string (5th, 4th fret), into C (3rd) under F♯, A, D.'


def lean(c, g, notes, durs, rest):
    return [dict(chords=[], note='', items=[['W', rest], R(notes, durs, c)]),
            dict(chords=[c], note='', items=[K(c, g, [(1, bass(g)), (0.5, CH), (0.5, '-'), (0.5, CH), (0.5, '-')])])]


EX_B.append(dict(
    id='vals-apoyatura', title='Leaning into the bass by a semitone',
    idea='A single eighth a semitone below the coming bass, on the “and” of 3. Works into any chord, major, minor or dominant.',
    quote=dict(where=where(173), text='5, into A: G♯ on the last eighth. Played here: that eighth and the bar it leads into.',
               items=[['W', 2.5], R([(6, 'G#2')], [0.5], 'A7'), K('A7', A7, [(1, [6]), (0.5, CH), (0.5, '-'), (0.5, CH), (0.5, '-')])], whose='Graciano’s own', played=''),
    bars=lean('G', YV['G'], [(6, 'F#2')], [0.5], 2.5) + lean('D7', YV['D7'], [(5, 'C#3')], [0.5], 2.5)))
EX_B[-1]['bars'][0]['note'] = 'Into G: F♯ on the low E string (2nd fret); into D7: C♯ on the A string (4th fret).'
EX_B.append(dict(
    id='vals-apoyatura-doble', title='Leaning into the bass by two semitones',
    idea='Two sixteenths climbing by semitones into the coming bass, on the last eighth.',
    quote=dict(where=where(174), text='6, into A: G, G♯. Played here: those and the bar they lead into.',
               items=[['W', 2.5], R([(6, 'G2'), (6, 'G#2')], [0.25, 0.25], 'A7'), K('A7', A7, [(1, [6]), (0.5, CH), (0.5, '-'), (0.5, CH), (0.5, '-')])], whose='Graciano’s own', played=''),
    bars=lean('G', YV['G'], [(6, 'F2'), (6, 'F#2')], [0.25, 0.25], 2.5) + lean('Cmaj7', YV['Cmaj7'], [(5, 'Bb2'), (5, 'B2')], [0.25, 0.25], 2.5)))
EX_B[-1]['bars'][0]['note'] = 'Into G: F, F♯ (low E string, 1st and 2nd fret); into C major 7: B♭, B (A string, 1st and 2nd).'

E8 = [0.5] * 6
EX_B.append(dict(
    id='vals-pedal', title='The bass arpeggio under a pedal',
    idea='Six eighths: the bass climbs the chord (root, 3rd, 5th) on the beats, the 3rd an octave up repeated between, like a pedal.',
    quote=dict(where=where(174), text='7, on A major: A, C♯, C♯, C♯, E, C♯. Played here: that bar.',
               items=[R([(6, 'A2'), (3, 'C#4'), (5, 'C#3'), (3, 'C#4'), (5, 'E3'), (3, 'C#4')], E8, 'A')], **OWN),
    bars=[dict(chords=['G'], note='On G: G, B, D on the low strings (low E 3rd fret, A string 2nd, A string 5th), the B on the G string (4th fret) between.',
               items=[R([(6, 'G2'), (3, 'B3'), (5, 'B2'), (3, 'B3'), (5, 'D3'), (3, 'B3')], E8, 'G')]),
          dict(chords=['Cm'], note='Minor, on C minor: C, E♭, G below (A string 3rd and 6th fret, D string 5th), the E♭ on the B string (4th fret) between.',
               items=[R([(5, 'C3'), (2, 'Eb4'), (5, 'Eb3'), (2, 'Eb4'), (4, 'G3'), (2, 'Eb4')], E8, 'Cm')])]))
EX_B.append(dict(
    id='vals-decimas', title='The bass climbing under the 3rd',
    idea='Six eighths: the bass climbs the scale from the root (root, 2nd, 3rd), the 3rd an octave up repeated over it, starting a 10th above the root.',
    quote=dict(where=where(174), text='8, por décimas, on A major: A, C♯, B, C♯, C♯, C♯. Played here: that bar.',
               items=[R([(6, 'A2'), (3, 'C#4'), (6, 'B2'), (3, 'C#4'), (5, 'C#3'), (3, 'C#4')], E8, 'A')], **OWN),
    bars=[dict(chords=['G'], note='On G: G, A, B in the bass (low E 3rd and 5th fret, A string 2nd), B on the G string (4th fret) over it.',
               items=[R([(6, 'G2'), (3, 'B3'), (6, 'A2'), (3, 'B3'), (5, 'B2'), (3, 'B3')], E8, 'G')]),
          dict(chords=['Cm'], note='Minor, on C minor: C, D, E♭ up the A string (3rd, 5th, 6th fret), E♭ on the B string (4th) over it.',
               items=[R([(5, 'C3'), (2, 'Eb4'), (5, 'D3'), (2, 'Eb4'), (5, 'Eb3'), (2, 'Eb4')], E8, 'Cm')])]))
EX_B.append(dict(
    id='vals-final-bajo', title='The last bass notes of a vals',
    idea='To end: the chord climbed in quarters in the bass, root, 3rd, 5th, then the root an octave up, alone, and two beats of silence.',
    quote=dict(where=where(174), text='Rellenos, 1, para final, in A major: A, C♯, E, then A.', items=[R([(6, 'A2'), (5, 'C#3'), (5, 'E3')], [1, 1, 1], 'A')], **OWN),
    bars=[dict(chords=['G'], note='On G, the end of Я вас любил: G, B, D (low E 3rd fret, A string 2nd and 5th), then G on the D string (5th fret).', items=[R([(6, 'G2'), (5, 'B2'), (5, 'D3')], [1, 1, 1], 'G')]),
          dict(chords=['G'], note='', items=[R([(4, 'G3')], [1], 'G'), ['W', 2]]),
          dict(chords=['Cm'], note='The minor way, on C minor: C, E♭, G, then C.', items=[R([(5, 'C3'), (5, 'Eb3'), (4, 'G3')], [1, 1, 1], 'Cm')]),
          dict(chords=['Cm'], note='', items=[R([(3, 'C4')], [1], 'Cm'), ['W', 2]])]))

for _e in EX_B: _e['quote']['played'] = ''          # these quotes say in their text what is played

SECTIONS = [dict(id='vals-ritmos', title='Vals rhythms', part='Exercises', ex=EX_R),
            dict(id='vals-bordoneos', title='Vals bass phrases', part='Exercises', ex=EX_B)]

from quotes import trim as _trim_quotes   # quotes stay a beat or two
_trim_quotes(SECTIONS)
