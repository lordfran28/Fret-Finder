"""Carcassi, Método completo Op. 59, first part: the right-hand arpeggios (pp. 14–16 of the owner's Melos copy).
Each arpeggio is a fixed order of thumb and fingers over two chords; Carcassi's own bar (public domain) is shown,
then the same arpeggio, note for note in the same order and rhythm, on G and C major 7 from Я вас любил (bars 8–9)."""
import sys
sys.path.insert(0, '/home/claude/studies')
from fractions import Fraction as Fr

# grips, strings 6..1 (index 0 = low E)
C_ = [-1, 3, 2, 0, 1, 0]          # Carcassi's C
G7 = [3, 2, 0, 0, 0, 1]           # Carcassi's G7
G = [3, 2, 0, 0, 0, 3]            # Я вас любил, bar 8
CM7 = [-1, 3, 2, 0, 0, 0]         # bar 9: C major 7 (the tune holds B)

# the strings each role uses on each chord: B1 = the root low down, B2 = the thumb's second string (4th string for
# four-finger arpeggios), B3 = the open G string (the thumb's second note in three-finger arpeggios), BB = the 5th string
ROLES = {'C': dict(B1=5, B2=4, B3=3, W1=4, W2=3), 'G7': dict(B1=6, B2=4, B3=3, W1=5, W2=4),
         'G': dict(B1=6, B2=4, B3=3, W1=5, W2=4), 'Cmaj7': dict(B1=5, B2=4, B3=3, W1=4, W2=3)}
T3 = Fr(1, 3); S = Fr(1, 4)


def beats(spec, chord):
    """spec: list of groups; each group a list of (length, [roles]); roles 'B1','B2','B3','BB', or a string number"""
    R = ROLES[chord]; hits = []
    for grp in spec:
        for d, roles in grp:
            hits.append([float(d), [R[r] if isinstance(r, str) else r for r in roles]])
    return hits


def bar(spec_bar, chord, grip):
    return ['K', chord, grip, beats(spec_bar, chord)]


# one bar of each arpeggio (four beats), as Carcassi writes it; 'alt' = the thumb's notes alternate per beat
def trip(b, x, y): return [(T3, [b]), (T3, [x]), (T3, [y])]
def six(b, *xs): return [(S, [b])] + [(S, [x]) for x in xs]
def alt(f, a, b):
    """four beats, the thumb on a, b, a, b"""
    return [f(a, 0), f(b, 1), f(a, 2), f(b, 3)]

A = {}
A[1] = dict(name='Thumb, index, middle', how='Triplets: the thumb, then the index on the B string and the middle on the high E. The thumb takes the bass on the beat and the open G on the next beat.',
            spec=lambda: alt(lambda b, k: trip(b, 2, 1), 'B1', 'B3'))
A[2] = dict(name='Thumb, middle, index', how='The same triplets with the fingers reversed: middle on the high E first, then index on the B string.',
            spec=lambda: alt(lambda b, k: trip(b, 1, 2), 'B1', 'B3'))
A[3] = dict(name='Thumb, index, middle, index', how='Sixteenths, four to a beat: thumb, index (B string), middle (high E), index.',
            spec=lambda: alt(lambda b, k: six(b, 2, 1, 2), 'B1', 'B3'))
A[4] = dict(name='Thumb, middle, index, middle', how='Sixteenths: thumb, middle (high E), index (B string), middle.',
            spec=lambda: alt(lambda b, k: six(b, 1, 2, 1), 'B1', 'B3'))
A[5] = dict(name='Four fingers: index, ring / index, middle', how='Triplets with the fourth finger: thumb, index (G string), ring (high E); then thumb, index, middle (B string). The thumb alternates between the bass and the D string.',
            spec=lambda: [trip('B1', 3, 1), trip('B2', 3, 2), trip('B1', 3, 1), trip('B2', 3, 2)])
A[6] = dict(name='Ring, index / middle, index', how='Triplets: thumb, ring (high E), index (G string); then thumb, middle (B string), index.',
            spec=lambda: [trip('B1', 1, 3), trip('B2', 2, 3), trip('B1', 1, 3), trip('B2', 2, 3)])
A[7] = dict(name='Up and down the chord', how='The bass held for two beats under triplet eighths that climb and fall: thumb, index, middle, ring, middle, index (G, B, E strings and back).',
            spec=lambda: [[(T3, ['B1']), (T3, [3]), (T3, [2])], [(T3, [1]), (T3, [2]), (T3, [3])], [(T3, ['B2']), (T3, [3]), (T3, [2])], [(T3, [1]), (T3, [2]), (T3, [3])]])
A[8] = dict(name='Middle, index, ring, index, middle', how='Two beats to a figure: thumb, middle, index, then ring, index, middle.',
            spec=lambda: [[(T3, ['B1']), (T3, [2]), (T3, [3])], [(T3, [1]), (T3, [3]), (T3, [2])], [(T3, ['B2']), (T3, [2]), (T3, [3])], [(T3, [1]), (T3, [3]), (T3, [2])]])
A[9] = dict(name='Thumb, index, middle, ring', how='Sixteenths, the chord straight up: thumb, index (G string), middle (B), ring (high E); the thumb alternates bass and D string.',
            spec=lambda: alt(lambda b, k: six(b, 3, 2, 1), 'B1', 'B2'))
A[10] = dict(name='Thumb, index, ring, middle', how='Sixteenths: thumb, index (G string), ring (high E), middle (B string).',
             spec=lambda: alt(lambda b, k: six(b, 3, 1, 2), 'B1', 'B2'))
A[11] = dict(name='Index between every finger', how='Two beats to a figure in sixteenths over a held bass: thumb, index, middle, index, ring, index, middle, index; the index always on the G string.',
             spec=lambda: [[(S, ['B1']), (S, [3]), (S, [2]), (S, [3])], [(S, [1]), (S, [3]), (S, [2]), (S, [3])]] * 2)
A[13] = dict(name='The thumb slides', how='Sixteenths: the thumb plays the bass and slides straight on to the next string, then index, middle, ring, middle, index, and the thumb on the D string.',
             spec=lambda: [[(S, ['B1']), (S, ['W1']), (S, [3]), (S, [2])], [(S, [1]), (S, [2]), (S, [3]), (S, ['B2'])]] * 2)
A[15] = dict(name='Two strings at once', how='Triplets: the thumb on the beat walking up the chord’s lower notes, then index and middle together on the B and high E strings, twice.',
             spec=lambda: [[(T3, ['B1']), (T3, [2, 1]), (T3, [2, 1])], [(T3, ['W1']), (T3, [2, 1]), (T3, [2, 1])], [(T3, ['W2']), (T3, [2, 1]), (T3, [2, 1])], [(T3, ['B1']), (T3, [2, 1]), (T3, [2, 1])]])
A[21] = dict(name='Three strings at once', how='Sixteenths: the thumb on the beat, then index, middle and ring together on the top three strings three times.',
             spec=lambda: alt(lambda b, k: [(S, [b]), (S, [3, 2, 1]), (S, [3, 2, 1]), (S, [3, 2, 1])], 'B1', 'B2'))



def quote_bar(k):
    return bar(A[k]['spec'](), 'C', C_)


EX = []
for k, a in A.items():
    sp = a['spec']()
    EX.append(dict(
        id=f'arp-{k}', title=f'Arpeggio {k}: {a["name"]}',
        idea=a['how'] + ' Repeat each many times in a row, as Carcassi asks, holding the whole chord down while you play it.',
        quote=dict(where=f'Carcassi, Método completo Op. 59, first part, p. {14 if k <= 6 else 15 if k <= 14 else 16}, No. {k}',
                   text='His first bar, on C major; the second is the same on G7.', item=quote_bar(k), whose='Carcassi’s own', played='Played here: that bar.'),
        bars=[dict(chords=['G'], note='On G, as Я вас любил has it in bar 8: the bass on the low E string, 3rd fret.', items=[bar(sp, 'G', G)]),
              dict(chords=['Cmaj7'], note='On C major 7, bar 9 (the tune holds B): the bass on the A string, 3rd fret; the B string open.', items=[bar(sp, 'Cmaj7', CM7)])]))
SECTIONS = [dict(id='arpeggios', title='Right-hand arpeggios', part='Exercises', ex=EX)]
