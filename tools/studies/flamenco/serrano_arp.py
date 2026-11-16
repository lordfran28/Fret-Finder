"""Juan Serrano, Flamenco Guitar: Basic Techniques, the arpeggio exercises (book pp. 46–48; PDF = book + 1): four right-hand
patterns over chords with the root on the low E string (his E, F, G, A minor, G, F, E: the open E and barres at the
1st, 3rd and 5th fret). Every note tirando (free stroke) except the ring finger, apoyando (rest stroke). Ours: his four
patterns, the same fingers on the same strings in the same rhythm, over Очи чёрные's changes (your chart, one bar each)
with the root on the low E string as his are: E7 open, A minor barred at the 5th fret, D minor at the 10th; then, as he
ends, the bass alone. check_arp.py checks every note."""
import sys
sys.path.insert(0, '/home/claude/studies'); sys.path.insert(0, '/home/claude/studies/flamenco')
import entry as F0

K, BOOK = F0.K, 'Flamenco Guitar: Basic Techniques'
GRIP = {'E7': [0, 2, 0, 1, 0, 0], 'Am': [5, 7, 7, 5, 5, 5], 'Dm': [10, 12, 12, 10, 10, 10]}      # root on the low E string
CHANGES = ['E7', 'Am', 'E7', 'Am', 'Dm', 'Am', 'E7', 'Am']                                       # your Очи чёрные, a bar a change
ACC = {'p': 0.08, 'a': 0.12}                   # the thumb's bass and the ring finger's apoyando a little stronger
CHECK = []


def beats_1():   # p a m i, a beat each, the thumb on the 6th, 5th, 4th string in turn (3/4)
    return [[('p', 6 - b), ('a', 1), ('m', 2), ('i', 3)] for b in range(3)]


def beats_2():   # p i m a m i, six to a beat, the thumb as in no. 1 (3/4)
    return [[('p', 6 - b), ('i', 3), ('m', 2), ('a', 1), ('m', 2), ('i', 3)] for b in range(3)]


def beats_3():   # p i m i, then a i m i three times, the ring finger on the B, high E, B strings (4/4)
    return [[('p', 6), ('i', 4), ('m', 3), ('i', 4)]] + [[('a', s), ('i', 4), ('m', 3), ('i', 4)] for s in (2, 1, 2)]


def beats_4():   # in threes: p i m, then a m i stepping down a string each beat (4/4)
    return [[('p', 6), ('i', 3), ('m', 2)], [('a', 1), ('m', 2), ('i', 3)], [('a', 2), ('m', 3), ('i', 4)], [('a', 3), ('m', 4), ('i', 5)]]


def bar(exid, chord, beats):
    spec = []
    for bt in beats:
        d = 1 / len(bt)
        for f, s in bt: spec.append((d, [s], ACC.get(f, 0)))
    CHECK.append((exid, chord, GRIP[chord], beats))
    names = ' '.join(f for bt in beats for f, s in bt)
    return dict(chords=[chord], note='', items=[K(chord, GRIP[chord], spec)]), names


def run(exid, make):
    bars = []
    for c in CHANGES:
        b, names = bar(exid, c, make())
        bars.append(b)
    n = len(make())
    bars.append(dict(chords=['Am'], note='', items=[K('Am', GRIP['Am'], [(n, [6], ACC['p'])])]))       # the bass alone, as he ends
    CHECK.append((exid, 'Am', GRIP['Am'], [[('p', 6)]]))
    return bars, names


def T(text, p): return dict(where=f'{BOOK}, p. {p}', text=text, item=None, by='Serrano')


STRN = {6: 'low E', 5: 'A', 4: 'D', 3: 'G', 2: 'B', 1: 'high E'}
EX = []
INFO = [
    ('arp-1', 'Serrano no. 1: p a m i', beats_1, 46, 'four to a beat: the thumb, then a, m, i down the top three strings; the thumb on the low E, the A, then the D string, a beat each.'),
    ('arp-2', 'Serrano no. 2: p i m a m i', beats_2, 46, 'six to a beat: the thumb, then i, m, a up the top three strings and m, i back down; the thumb moving as in no. 1.'),
    ('arp-3', 'Serrano no. 3: p i m i, a i m i', beats_3, 46, 'four to a beat, in four: i and m rock between the D and G strings while the ring finger takes the top note, the B, the high E, the B again; the thumb only on the first beat.'),
    ('arp-4', 'Serrano no. 4: p i m, a m i', beats_4, 46, 'three to a beat, in four: after p i m, each beat a m i comes down the strings, starting a string lower each time, down to the A string.')]
for exid, title, make, p, what in INFO:
    b, names = run(exid, make)
    b[0]['note'] = (f'The pattern: {what} On Очи чёрные’s changes, a bar each, with the root on the low E string: E7 open, A minor at the 5th fret, D minor at the 10th; '
                    'then the A alone. Every note tirando except a, apoyando.')
    first = make()[0]
    EX.append(dict(
        id=exid, title=title,
        idea=('Serrano’s arpeggios for the flamenco right hand: the thumb on the bass, the fingers on the top strings, every note a free stroke except the ring finger, which rests on the next string. '
              'He plays each over E, F, G, A minor, G, F and E, moving the barre up and back.' if exid == 'arp-1' else 'The same chords, another pattern.'),
        quote=dict(where=f'{BOOK}, p. {p}', text=f'his first beat on E: {" ".join(f for f, s in first)}.',
                   items=[K('E', [0, 2, 2, 1, 0, 0], [(1 / len(first), [s], ACC.get(f, 0)) for f, s in first])], whose='Serrano’s own', played='Played here: that beat.'),
        bars=b))
SECTION = dict(id='flamenco-serrano', title='Serrano’s arpeggios', part='Exercises', ex=EX, mark='S')
SECTIONS = list(F0.SECTIONS) + [SECTION]
