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
A[12] = dict(name='Thumb on the first and seventh', how='Sixteenths, two beats to a figure: the thumb on the bass, then middle (B string), index (G), ring (high E), middle, index; the thumb again on the D string; index. The bass rings for a beat and a half.',
             spec=lambda: [[(S, ['B1']), (S, [2]), (S, [3]), (S, [1])], [(S, [2]), (S, [3]), (S, ['B2']), (S, [3])]] * 2)
A[14] = dict(name='The index on the D string', how='Sixteenths over a bass held for two beats: middle on the G string, index on the D string, middle, ring on the B string, middle, index, middle; then the same from the high E string.',
             spec=lambda: [[(S, ['B1']), (S, [3]), (S, [4]), (S, [3])], [(S, [2]), (S, [3]), (S, [4]), (S, [3])], [(S, [1]), (S, [3]), (S, [4]), (S, [3])], [(S, [2]), (S, [3]), (S, [4]), (S, [3])]])
A[16] = dict(name='Index with the thumb, then ring, middle', how='Triplets, four fingers: the thumb and the index (G string) together on the beat, then ring (high E), middle (B string). The thumb alternates the bass and the D string.',
             spec=lambda: alt(lambda b, k: [(T3, [b, 3]), (T3, [1]), (T3, [2])], 'B1', 'B2'))
A[17] = dict(name='Up one beat, down the next', how='Triplets: thumb and index together, middle, ring; then thumb and ring together, middle, index. The thumb alternates the bass and the D string.',
             spec=lambda: [[(T3, ['B1', 3]), (T3, [2]), (T3, [1])], [(T3, ['B2', 1]), (T3, [2]), (T3, [3])]] * 2)
A[18] = dict(name='The thumb slides', how='The thumb slides across the A, D and G strings in triplets, a note each, while the ring, middle, index and middle fingers take the high E string on the beats.',
             spec=lambda: [[(T3, [5, 1]), (T3, [4]), (T3, [3])]] * 4)
A[19] = dict(name='Index with the thumb, then middle, ring, middle', how='Sixteenths: thumb and index (G string) together on the beat, then middle (B), ring (high E), middle. The thumb alternates the bass and the D string.',
             spec=lambda: alt(lambda b, k: [(S, [b, 3]), (S, [2]), (S, [1]), (S, [2])], 'B1', 'B2'))
A[20] = dict(name='Ring with the thumb, the thumb inside', how='Sixteenths: thumb (bass) and ring (high E) together on the beat, middle on the G string, the thumb on the D string, index on the G string. The bass on every beat.',
             spec=lambda: [[(S, ['B1', 1]), (S, [3]), (S, [4]), (S, [3])]] * 4)
A[22] = dict(name='Three strings at once, two ways', how=('Index, middle and ring together on the top three strings in sixteenths. On C the thumb plays only the first and seventh of each eight (the bass, then the D string; '
                                                       'in the second half the bass again); on G7 the thumb walks in eighths, G, B, D, B, G, D, B, G, with the chord between every two of its notes. '
                                                       'Ours follows the same pairing: his C bar on C major 7, his G7 bar on G.'),
             spec=lambda: [[(S, ['B1']), (S, [3, 2, 1]), (S, [3, 2, 1]), (S, [3, 2, 1])], [(S, [3, 2, 1]), (S, [3, 2, 1]), (S, ['B2']), (S, [3, 2, 1])],
                           [(S, ['B1']), (S, [3, 2, 1]), (S, [3, 2, 1]), (S, [3, 2, 1])], [(S, [3, 2, 1]), (S, [3, 2, 1]), (S, ['B1']), (S, [3, 2, 1])]],
             spec_g=lambda: [[(S, [6]), (S, [3, 2, 1]), (S, [5]), (S, [3, 2, 1])], [(S, [4]), (S, [3, 2, 1]), (S, [5]), (S, [3, 2, 1])],
                             [(S, [6]), (S, [3, 2, 1]), (S, [4]), (S, [3, 2, 1])], [(S, [5]), (S, [3, 2, 1]), (S, [6]), (S, [3, 2, 1])]])
A[21] = dict(name='Three strings at once', how='Sixteenths: the thumb on the beat, then index, middle and ring together on the top three strings three times.',
             spec=lambda: alt(lambda b, k: [(S, [b]), (S, [3, 2, 1]), (S, [3, 2, 1]), (S, [3, 2, 1])], 'B1', 'B2'))



def quote_bar(k):
    return bar(A[k]['spec'](), 'C', C_)


EX = []
for k, a in sorted(A.items()):
    sp = a['spec']()
    EX.append(dict(
        id=f'arp-{k}', title=f'Arpeggio {k}: {a["name"]}',
        idea=a['how'] + ' Repeat each many times in a row, as Carcassi asks, holding the whole chord down while you play it.',
        quote=dict(where=f'Carcassi, Método completo Op. 59, first part, p. {14 if k <= 6 else 15 if k <= 14 else 16}, No. {k}',
                   text=('His first bar, on C major; on G7, his second bar, the thumb walks instead.' if k == 22 else 'His first bar, on C major; the second is the same on G7.'),
                   item=quote_bar(k), whose='Carcassi’s own', played='Played here: that bar.'),
        bars=[dict(chords=['G'], note='On G, as Я вас любил has it in bar 8: the bass on the low E string, 3rd fret.', items=[bar(a['spec_g']() if 'spec_g' in a else sp, 'G', G)]),
              dict(chords=['Cmaj7'], note='On C major 7, bar 9 (the tune holds B): the bass on the A string, 3rd fret; the B string open.', items=[bar(sp, 'Cmaj7', CM7)])]))
SECTIONS = [dict(id='arpeggios', title='Right-hand arpeggios', part='Exercises', ex=EX)]
