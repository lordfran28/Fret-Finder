"""Juan Serrano, Flamenco Guitar: Basic Techniques (Mel Bay), the rasgueado (book pp. 21–29; PDF = book + 1): the thumb
resting on the low E string, the fingers closed; the index flicks out across the strings and back, then the little
finger (s), the ring (a) and the middle (m) in turn, every stroke a downstroke unless marked; slowly at first, each
finger on its own beat. His preparatory study, three exercises and five studies, on A and E7 (study 5 on barre
chords), are written out with every stroke and finger. Ours: the same strokes, the same fingers in the same order and
rhythm, on the chords of Очи чёрные as your chart has them (E7, Am, Dm, two bars each; the open grips, and barre grips
for study 5). check_ras.py checks every stroke. His bars are described and his first beat quoted; nothing else is
copied."""
import sys
sys.path.insert(0, '/home/claude/studies')

BOOK = 'Flamenco Guitar: Basic Techniques'
OPEN_G = {'Am': [-1, 0, 2, 2, 1, 0], 'Dm': [-1, -1, 0, 2, 3, 1], 'E7': [0, 2, 0, 1, 0, 0], 'A': [-1, 0, 2, 2, 2, 0]}   # Очи's open grips (and his A)
BARRE_G = {'Am': [5, 7, 7, 5, 5, 5], 'Dm': [-1, 5, 7, 7, 6, 5], 'E7': [-1, 7, 9, 7, 9, 7]}                          # barre grips, nothing open
CHART = ['E7', 'E7', 'Am', 'Am', 'E7', 'E7', 'Am', 'Am', 'Dm', 'Dm', 'Am', 'Am', 'E7', 'E7', 'Am', 'Am']   # your Очи чёрные
CHANGES = CHART[0::2]
CHECK = []

# strokes: (beats, finger, 'D' or 'U') or (beats, None, '-') for a rest
def isam(): return [(0.25, f, 'D') for f in 'isam']
def i_(d=1.0): return [(d, 'i', 'D')]
def du(n): return sum(([(0.5, 'i', 'D'), (0.5, 'i', 'U')] for _ in range(n)), [])
def rest(d=1.0): return [(d, None, '-')]
def plain(d=1.0): return [(d, None, 'D')]          # a downstroke he leaves unlettered


def item(chord, strokes, grips):
    """a rhythm item: every stroke strums every string the grip sounds, low to high (down) or high to low (up)"""
    g = grips[chord]
    strs = [6 - i for i, f in enumerate(g) if f >= 0]
    hits, ups, marks = [], [], []
    for k, (d, f, way) in enumerate(strokes):
        if way == '-': hits.append([d, '-']); marks.append(''); continue
        hits.append([d, sorted(strs, reverse=True), 0.06 if k == 0 else 0])
        marks.append((f or '') + ('↓' if way == 'D' else '↑'))
        if way == 'U': ups.append(k)
    return ['K', chord, g, hits, {'up': ups, 'marks': marks}]


def bar(exid, chords_strokes, grips=OPEN_G, note=''):
    """one bar: [(chord, strokes), ...] (the chord can change inside the bar)"""
    its = [item(c, s, grips) for c, s in chords_strokes]
    CHECK.append((exid, [(c, list(s), grips[c]) for c, s in chords_strokes]))
    return dict(chords=[c for c, _ in chords_strokes], note=note, items=its)


def say(strokes):
    out = []
    for d, f, w in strokes:
        if w == '-': out.append('rest'); continue
        out.append((f or '') + ('↓' if w == 'D' else '↑'))
    return ' '.join(out)


def T(text, p): return dict(where=f'{BOOK}, p. {p}', text=text, item=None, by='Serrano')


EX = []
# the preparatory study: each finger a beat
pre = [(1.0, 'i', 'D'), (1.0, 's', 'D'), (1.0, 'a', 'D'), (1.0, 'm', 'D')]
b = [bar('prep', [(c, pre)]) for c in CHANGES] + [bar('prep', [('Am', i_() + rest(3))])]
b[0]['note'] = ('One stroke to a beat, each finger by itself: i, s, a, m, all downstrokes; then the index again. On each change of Очи чёрные, a bar, '
                'and the index alone to end. ↓ is a downstroke (from the low string to the high), ↑ an upstroke.')
EX.append(dict(id='prep', title='Preparatory study: one finger to a beat',
               idea=('Serrano: the rasgueado is the sound of flamenco, rain, a double drumbeat, castanets. The thumb rests on the low E string and the fingers close into the palm. '
                     'The index flicks out across the strings and comes back; then the little finger, the ring and the middle, each in turn, and all three close again before the index '
                     'starts once more. Practise slowly, each finger on its own beat, until each moves without the others.'),
               quote=T('one stroke a beat on A: index, little, ring, middle, then the index again.', 23), bars=b))

# exercise 1 (3/4): i s a m, then i, then a rest
P1 = isam() + i_() + rest()
b = [bar('ex1', [(c, P1)]) for c in CHART[:8]]
b[0]['note'] = f'Three beats: {say(P1)}. Every stroke down. Through the first eight bars of Очи чёрные.'
EX.append(dict(id='ex1', title='Exercise 1: four strokes and the index',
               idea='The four fingers on one beat, i s a m as sixteenths, then the index alone, then a beat’s rest. In three.',
               quote=dict(where=f'{BOOK}, p. 24', text='on A: the four strokes on the first beat, the index on the second.', items=[item('A', isam(), OPEN_G)],
                          whose='Serrano’s own', played='Played here: his first beat, on A.'), bars=b))

# exercise 2 (4/4): i s a m i s a m, then i, then a rest
P2 = isam() + isam() + i_() + rest()
b = [bar('ex2', [(c, P2)]) for c in CHANGES]
b[0]['note'] = f'Four beats: {say(P2)}. A bar on each change of Очи чёрные.'
EX.append(dict(id='ex2', title='Exercise 2: twice round, in four',
               idea='The same, twice round: eight strokes, then the index, then a rest. In four.',
               quote=T('the same on A, in four.', 24), bars=b))

# exercise 3 (3/4): three beats of i s a m, then the index alone
P3a, P3b = isam() * 3, i_() + rest(2)
b = []
for k, c in enumerate(CHART):
    b.append(bar('ex3', [(c, P3a if k % 2 == 0 else P3b)]))
b[0]['note'] = f'Bar one: {say(P3a)}; bar two: {say(P3b)}. Each chord of Очи чёрные has two bars: the strokes, then the index on its own.'
EX.append(dict(id='ex3', title='Exercise 3: three beats of strokes',
               idea='Three beats of i s a m without a break, then the index alone on the next downbeat.',
               quote=T('three beats of the four strokes on A, then the index on the next bar.', 24), bars=b))

# study 1 (3/4): i s a m, i, a downstroke; every fourth bar the chord arrives with one stroke
S1, ARR = isam() + i_() + plain(), plain() + rest(2)
b = [bar('st1', [(c, ARR if k % 4 == 3 else S1)]) for k, c in enumerate(CHART)]
b[0]['note'] = (f'Three bars of {say(S1)}, then a bar with a single stroke and two beats’ rest. Serrano puts that bar where the chord changes; '
                'here it closes each four-bar phrase of Очи чёрные, on A minor.')
EX.append(dict(id='st1', title='Study 1', idea='The strokes of exercise 1 with a third downstroke instead of the rest, and a single stroke to close each phrase.',
               quote=T('A and E7, four bars each; the fourth bar a single stroke.', 25), bars=b))


def antic(k):
    """the chord on the last beat of every fourth bar: the next bar's chord, as he anticipates it"""
    return CHART[k + 1] if k + 1 < len(CHART) else CHART[k]


# study 2 (3/4): i s a m i s a m i | three strokes | again | two strokes and the next chord on the third beat
S2a, S2b = isam() + isam() + i_(), plain() * 3
b = []
for k, c in enumerate(CHART):
    if k % 4 in (0, 2): b.append(bar('st2', [(c, S2a)]))
    elif k % 4 == 1: b.append(bar('st2', [(c, S2b)]))
    else: b.append(bar('st2', [(c, plain() * 2), (antic(k), plain())] if antic(k) != c else [(c, S2b)]))
b.append(bar('st2', [('Am', plain() + rest(2))]))
b[0]['note'] = (f'Bars one and three: {say(S2a)}; bar two: three downstrokes; bar four: two downstrokes and the next chord on the third beat, '
                'arriving early as Serrano has it. Through Очи чёрные, and a last stroke on A minor.')
EX.append(dict(id='st2', title='Study 2', idea='Eight strokes and the index, then plain downstrokes; the next chord comes in on the last beat.',
               quote=T('the change to E7 comes on the third beat of the fourth bar.', 25), bars=b))

# study 3 (3/4): i s a m i s a m, then index down-up | index down-up x3 | again | down-up x2 and the next chord down-up
S3a, S3b = isam() + isam() + du(1), du(3)
b = []
for k, c in enumerate(CHART):
    if k % 4 in (0, 2): b.append(bar('st3', [(c, S3a)]))
    elif k % 4 == 1: b.append(bar('st3', [(c, S3b)]))
    else: b.append(bar('st3', [(c, du(2)), (antic(k), du(1))] if antic(k) != c else [(c, S3b)]))
b.append(bar('st3', [('Am', plain() + rest(2))]))
b[0]['note'] = (f'Bars one and three: {say(S3a)}; bar two: the index down and up in eighths, {say(S3b)}; bar four the same with the next chord on the third beat. '
                'The index goes up as well as down: up from the high string.')
EX.append(dict(id='st3', title='Study 3: the index up and down', idea='The index now strums up as well as down, in eighths, between the four-finger strokes.',
               quote=T('eighths of the index, down and up, after the four strokes.', 25), bars=b))

# study 4 (3/4): three beats of i s a m | index down-up x3 | again | down-up x2 and the next chord
S4a, S4b = isam() * 3, du(3)
b = []
for k, c in enumerate(CHART):
    if k % 4 in (0, 2): b.append(bar('st4', [(c, S4a)]))
    elif k % 4 == 1: b.append(bar('st4', [(c, S4b)]))
    else: b.append(bar('st4', [(c, du(2)), (antic(k), du(1))] if antic(k) != c else [(c, S4b)]))
b.append(bar('st4', [('Am', plain() + rest(2))]))
b[0]['note'] = f'Bars one and three: {say(S4a)}; bar two: {say(S4b)}; bar four the same with the next chord on the third beat.'
EX.append(dict(id='st4', title='Study 4', idea='Whole bars of the four strokes, answered by whole bars of the index down and up.',
               quote=T('three beats of the four strokes, then a bar of eighths down and up.', 26), bars=b))

# study 5 (3/4) on barre chords: i s a m i s a m, index down-up; the last chord before home: three beats of i s a m
S5, S5e = isam() + isam() + du(1), isam() * 3
b = [bar('st5', [(c, S5)], BARRE_G) for c in CHANGES[:6]]
b.append(bar('st5', [('E7', S5e)], OPEN_G))
b.append(bar('st5', [('Am', i_() + rest(2))], OPEN_G))
b[0]['note'] = (f'Each bar: {say(S5)}, on barre chords (nothing open): E7 at the 7th fret (root on the A string), A minor at the 5th (root on the low E), '
                f'D minor at the 5th (root on the A string). Then the open E7 for three beats of the four strokes, and the open A minor with the index.')
EX.append(dict(id='st5', title='Study 5: on barre chords',
               idea='The same strokes on barre chords moving up and down the neck; the barre damps the strings as the hand leaves each chord.',
               quote=T('barre chords up the neck: F♯, B minor, G♯, C♯ minor, D, then A, E7 and A.', 26), bars=b))

SECTIONS = [dict(id='rasgueado', title='Rasgueado', part='Exercises', ex=EX)]
