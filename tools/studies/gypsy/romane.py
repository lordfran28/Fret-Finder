"""Romane and Derek Sébastian, L'Esprit Manouche (Mel Bay), part A of chapters 1–4 (book pp. 9–34; PDF = book + 1):
fingerboard diagrams of arpeggios and scales, each played up the numbers and back down, in eighths, alternate strokes.

Theirs are in A minor (the key of their tune for these chapters) and its chords. Ours are the same diagrams, every note
on the same string, moved up one fret into B♭ minor, the minor side of your It Had to Be You (in D♭): their Am, Dm, E7,
B♭7 and the dim7 of E7 become B♭m, E♭m, F7, C♭7 and the dim7 of F7, which are the song's B♭m7, E♭m9, F7♭9, C♭9.
Moving a whole diagram along the neck keeps every interval, string and finger, so ours is the same exercise; where
theirs uses an open string, ours has that note at the 1st fret. The chromatic scale (exercise 14) is the same in every
key and is about the open strings, so it stays where it is. check_romane.py checks every note."""
import sys
sys.path.insert(0, '/home/claude/studies'); sys.path.insert(0, '/home/claude/studies/gypsy')

BOOK = 'L’Esprit Manouche'
OPENS = [40, 45, 50, 55, 59, 64]
SHIFT = 1


def midi(s, f): return OPENS[6 - s] + f


# Their diagrams as read from the book: (string, fret) in the order of their numbers; 1 = the high E string.
THEIRS = {
    'am':   [(5, 0), (5, 3), (4, 2), (3, 2), (2, 1), (1, 0), (1, 5), (2, 5), (3, 5), (4, 7), (5, 7), (6, 8), (6, 5), (6, 8), (5, 7),
             (4, 7), (4, 10), (3, 9), (2, 10), (1, 8), (1, 12)],
    'dm':   [(4, 0), (4, 3), (3, 2), (2, 3), (1, 1), (1, 5), (2, 6), (3, 7), (4, 7), (5, 8), (5, 5), (5, 8), (4, 7), (3, 7), (3, 10),
             (2, 10), (1, 10), (2, 10), (3, 10), (4, 12), (5, 12), (6, 13), (6, 10)],
    'dim':  [(6, 1), (6, 4), (5, 2), (5, 5), (4, 3), (4, 6), (3, 4), (3, 7), (2, 6), (2, 9), (1, 7), (1, 10)],
    'dim7': [(6, 5), (5, 4), (5, 7), (4, 5), (4, 8), (3, 6), (3, 9), (2, 8), (2, 11), (1, 9), (1, 12)],
    'maj1': [(5, 1), (5, 5), (4, 3), (3, 3), (2, 3), (2, 6), (1, 6), (2, 6), (3, 7), (4, 8), (5, 8), (5, 5), (6, 6), (6, 10), (5, 8),
             (4, 8), (4, 12), (3, 10), (2, 11), (1, 10), (1, 13)],
    'maj2': [(6, 0), (6, 4), (6, 7), (5, 7), (4, 6), (3, 4), (2, 5), (1, 4), (1, 7)],
    'hm':   [(6, 5), (6, 7), (6, 8), (5, 5), (5, 7), (5, 8), (4, 6), (4, 7), (3, 4), (3, 5), (3, 7), (2, 5), (2, 6), (1, 4), (1, 5)],
    'hm2':  [(6, 5), (6, 7), (6, 8), (5, 5), (5, 7), (5, 8), (4, 6), (4, 7), (4, 9), (4, 10), (3, 7), (3, 9), (3, 10), (2, 9), (2, 10),
             (1, 7), (1, 8), (1, 10)],
    'm6a':  [(6, 5), (6, 8), (5, 7), (4, 4), (4, 7), (3, 5), (2, 5), (2, 7), (1, 5), (1, 8)],
    'm6b':  [(6, 12), (6, 14), (5, 12), (5, 15), (4, 14), (3, 11), (3, 14), (2, 13), (1, 12), (1, 14)],
    'm9a':  [(6, 5), (6, 7), (6, 8), (5, 7), (4, 7), (4, 9), (4, 10), (3, 9), (2, 10), (2, 12), (2, 13), (1, 12)],
    'm9b':  [(5, 0), (5, 2), (5, 3), (4, 2), (3, 2), (3, 4), (3, 5), (2, 5), (1, 5)],
    'sp1':  [(1, 8), (1, 7), (1, 5), (2, 8), (2, 7), (2, 5)],
    'sp2':  [(1, 7), (1, 5), (1, 3), (2, 7), (2, 5), (2, 3)],
    'chrom': [(s, f) for s, top in ((6, 4), (5, 4), (4, 4), (3, 3), (2, 4), (1, 4)) for f in range(top + 1)],
}
# their left-hand fingers where the diagram gives them (i index, m middle, a ring, au little) -> 1 2 3 4
FING = {
    'dim':  [1, 4] * 6,
    'dim7': [2] + [1, 4] * 5,
    'hm':   [1, 3, 4, 1, 3, 4, 1, 2, 1, 2, 4, 2, 3, 1, 2],
    'hm2':  [1, 3, 4, 1, 3, 4, 1, 1, 3, 4, 1, 3, 4, 1, 2, 1, 2, 4],
    'm6a':  [1, 4, 3, 1, 3, 1, 1, 3, 1, 4],
    'm6b':  [1, 3, 1, 4, 3, 1, 3, 2, 1, 3],
    'm9a':  [1, 3, 4, 1, 1, 3, 4, 1, 2, 3, 4, 3],
    'sp1':  [4, 3, 1, 4, 3, 1],
    'sp2':  [4, 2, 1, 4, 2, 1],
    'chrom': [0, 1, 2, 3, 4] * 3 + [0, 1, 2, 3] + [0, 1, 2, 3, 4] * 2,
}
GRIP_THEIRS = {'sp1': [5, 7, 7, 5, 7, 7], 'sp2': [3, 5, 5, 4, 5, 5]}     # the chord each speed exercise sits in

# how ours is named, and the spellings of its notes
OURS = {   # id: (chord, shift, spelling of the pitch classes)
    'am':   ('Bbm', 1, {10: 'B♭', 1: 'D♭', 5: 'F'}),
    'dm':   ('Ebm', 1, {3: 'E♭', 6: 'G♭', 10: 'B♭'}),
    'dim':  ('Gbdim7', 1, {6: 'G♭', 9: 'A', 0: 'C', 3: 'E♭'}),
    'dim7': ('Bb7b9', 1, {10: 'B♭', 2: 'D', 5: 'F', 8: 'A♭', 11: 'C♭'}),
    'maj1': ('Cb', 1, {11: 'C♭', 3: 'E♭', 6: 'G♭'}),
    'maj2': ('F', 1, {5: 'F', 9: 'A', 0: 'C'}),
    'hm':   ('Bbm', 1, {10: 'B♭', 0: 'C', 1: 'D♭', 3: 'E♭', 5: 'F', 6: 'G♭', 9: 'A'}),
    'hm2':  ('Bbm', 1, {10: 'B♭', 0: 'C', 1: 'D♭', 3: 'E♭', 5: 'F', 6: 'G♭', 9: 'A'}),
    'm6a':  ('Bbm6', 1, {10: 'B♭', 1: 'D♭', 5: 'F', 7: 'G'}),
    'm6b':  ('Bbm6', 1, {10: 'B♭', 1: 'D♭', 5: 'F', 7: 'G'}),
    'm9a':  ('Bbm(add9)', 1, {10: 'B♭', 0: 'C', 1: 'D♭', 5: 'F'}),
    'm9b':  ('Bbm(add9)', 1, {10: 'B♭', 0: 'C', 1: 'D♭', 5: 'F'}),
    'sp1':  ('Bbm6/9', 1, {1: 'D♭', 0: 'C', 10: 'B♭', 8: 'A♭', 7: 'G', 5: 'F'}),
    'sp2':  ('Ab6/9', 1, {0: 'C', 10: 'B♭', 8: 'A♭', 7: 'G', 5: 'F', 3: 'E♭'}),
    'chrom': (None, 0, None),
}
THEIR_NAMES = {   # A minor's spellings for the quotes
    0: 'C', 1: 'C♯', 2: 'D', 3: 'D♯', 4: 'E', 5: 'F', 6: 'F♯', 7: 'G', 8: 'G♯', 9: 'A', 10: 'B♭', 11: 'B'}
SHARP = ['C', 'C♯', 'D', 'D♯', 'E', 'F', 'F♯', 'G', 'G♯', 'A', 'A♯', 'B']
FLAT = ['C', 'D♭', 'D', 'E♭', 'E', 'F', 'G♭', 'G', 'A♭', 'A', 'B♭', 'B']


def ours(key):
    sh = OURS[key][1]
    return [(s, f + sh) for s, f in THEIRS[key]]


def up_down(seq):
    """up the numbers and back down, the top note once"""
    return list(seq) + list(seq[-2::-1])


def bars_of(notes, names, what, chord, per_bar=8, d=0.5, vel=None):
    """eighths, eight to a bar; the last note held to the end of its bar"""
    out = []
    for i in range(0, len(notes), per_bar):
        ns, nm = notes[i:i + per_bar], names[i:i + per_bar]
        durs = [d] * len(ns)
        if i + per_bar >= len(notes):
            durs[-1] = 4 - d * (len(ns) - 1)
        it = ['R', [list(x) for x in ns], durs, '=' + ','.join(nm) + '|' + what]
        if vel: it.append({'vel': vel[i:i + per_bar]})
        out.append(dict(chords=[chord] if chord else [], note='', items=[it]))
    return out


def name_of(key, s, f, down=False):
    m = midi(s, f)
    sp = OURS[key][2]
    if sp is None: return (FLAT if down else SHARP)[m % 12]
    return sp[m % 12]


def T(text, p, notes=None, durs=None, names=None, played='Played here: its first notes.'):
    q = dict(where=f'{BOOK}, p. {p}', text=text, whose='The original', played=played)
    if notes:
        q['items'] = [['R', [list(x) for x in notes], durs or [0.5] * len(notes), '=' + ','.join(names) + '|their first notes']]
    return q


def quote(key, n, text, p, names=None):
    ns = THEIRS[key][:n]
    return T(text, p, ns, names=names or [THEIR_NAMES[midi(s, f) % 12] for s, f in ns])


def fingers_txt(key):
    w = {0: 'open', 1: 'index', 2: 'middle', 3: 'ring', 4: 'little'}
    fs = FING[key]
    out, cur = [], None
    for (s, f), x in zip(ours(key), fs):
        if s != cur: out.append([s, []]); cur = s
        out[-1][1].append(str(x) if x else 'open')
    STR = {6: 'low E', 5: 'A', 4: 'D', 3: 'G', 2: 'B', 1: 'high E'}
    return '; '.join(f'{STR[s]} {"-".join(xs)}' for s, xs in out)


def run_ex(key, what):
    seq = ours(key)
    full = up_down(seq)
    k = len(seq)
    names = [name_of(key, s, f, down=i >= k) for i, (s, f) in enumerate(full)]
    return bars_of(full, names, what, OURS[key][0])


SONG = 'It Had to Be You'
EX = []

# ---------------------------------------------------------------- chapter 1: minor triads in many forms; the dim7
b = run_ex('am', 'B♭ minor across the neck')
b[0]['note'] = ('B♭, D♭ and F from the B♭ at the 1st fret of the A string to the F at the 13th fret of the high E string, '
                'then back down: up through the first position, down through the 6th, up through the 8th, '
                'the hand moving up the neck at each turn. Then the same numbers backwards. Eighths, alternate strokes, and sing the notes as you play them.')
EX.append(dict(id='am', title='B♭ minor in many forms',
               idea=('The minor triad all over the neck as one line: up the chord’s notes in one position, down them in the next one up, up again in the next, '
                     'so you see the chord everywhere at once. Ours is their A minor diagram one fret higher: B♭ minor, the B♭m7 of your bars 5–7, 11–13, 21–23 and 28.'),
               quote=quote('am', 4, 'their A minor diagram starts on the open A string: A, C, E, A.', 9),
               bars=b))
b = run_ex('dm', 'E♭ minor across the neck')
b[0]['note'] = ('E♭, G♭ and B♭ from the E♭ at the 1st fret of the D string up to the B♭ at the 6th fret of the high E string, down through the 6th position, '
                'up through the 8th to the E♭ at the 11th fret, and down through the 11th position to the E♭ at the 11th fret of the low E string; then back.')
EX.append(dict(id='dm', title='E♭ minor in many forms',
               idea='The same idea on the minor chord a fourth up: their D minor, ours E♭ minor, the E♭m9 of your bars 15 and 32.',
               quote=quote('dm', 4, 'their D minor diagram starts on the open D string: D, F, A, D.', 9),
               bars=b))
b = run_ex('dim', 'the diminished seventh, two notes a string')
b[0]['note'] = ('G♭, A, C, E♭: a minor third apart all the way up, from the 2nd fret of the low E string to the 11th fret of the high E string. '
                'Two notes on each string, index then little finger, the hand moving up a fret for each string and two frets from the G to the B string. '
                f'Fingers: {fingers_txt("dim")}.')
EX.append(dict(id='dim', title='The diminished seventh, two notes a string',
               idea=('Nothing but minor thirds, so the diagram is almost a scale: two notes a string, the same shape on every string. '
                     'Ours is theirs a fret higher: G♭°7, the same four notes as A°7, C°7 and E♭°7, which is your F7♭9 without its F (bars 10 and 27) and A♭7♭9 without its A♭.'),
               quote=quote('dim', 4, 'theirs is F°7 (or A♭°7, B°7, D°7), from the F at the 1st fret: F, A♭, B, D.', 10, names=['F', 'A♭', 'B', 'D']),
               bars=b))
b = run_ex('dim7', 'B♭7: its root, then the diminished seventh')
b[0]['note'] = ('The root B♭ at the 6th fret of the low E string with the middle finger, then D, F, A♭, C♭ two notes a string, index and little finger, up to the 13th fret. '
                f'Fingers: {fingers_txt("dim7")}. Over any seventh chord with its root on the low E string; one fret up, theirs is over A7.')
EX.append(dict(id='dim7', title='B♭7: the diminished seventh from its root',
               idea=('Learn it by heart: over a seventh chord with its root on the low E string, play the root and then the diminished seventh built on its 3rd; '
                     'together they make the 7♭9 chord. Ours is on B♭7, your B♭9 of bars 3–4 and 19–20, one fret above their A7.'),
               quote=quote('dim7', 3, 'theirs is on A7, from the A at the 5th fret: A, C♯, E.', 10),
               bars=b))

# ---------------------------------------------------------------- chapter 2: major triads; the harmonic minor scale
b = run_ex('maj1', 'C♭ major across the neck')
b[0]['note'] = ('C♭, E♭ and G♭ from the 2nd fret of the A string up to the C♭ at the 7th fret of the high E string, down to the C♭ at the 7th fret of the low E string, '
                'then up through the 9th position to the G♭ at the 14th fret; then back.')
EX.append(dict(id='maj1', title='C♭ major in many forms',
               idea=('The major triad all over the neck the same way, up and down and up, the hand moving up at each turn. '
                     'Theirs is B♭ major; ours is a fret higher, C♭ major, the chord of your C♭9 (bars 2, 18 and 26).'),
               quote=quote('maj1', 4, 'their B♭ major starts at the 1st fret of the A string: B♭, D, F, B♭.', 17),
               bars=b))
b = run_ex('maj2', 'F major on a diagonal')
b[0]['note'] = 'F, A and C up from the 1st fret of the low E string to the 8th fret of the high E string on a diagonal, three notes on the low E string; then back.'
EX.append(dict(id='maj2', title='F major on a diagonal',
               idea=('The major triad on a diagonal: three notes on the lowest string, then one or two a string climbing across. '
                     'Theirs is E major, from the open low E string; ours is F, the chord of your F7 (bars 10–12 and 27), from the 1st fret.'),
               quote=quote('maj2', 3, 'their E major starts on the open low E string: E, G♯, B.', 17),
               bars=b))
b = run_ex('hm', 'B♭ harmonic minor, in position')
b[0]['note'] = ('B♭ harmonic minor (B♭ C D♭ E♭ F G♭ A) over two octaves in one position: index at the 6th fret, reaching back to the 5th on the G and high E strings and up to the 7th on the D string. '
                f'Fingers: {fingers_txt("hm")}. The E♭ on the A string has no number in their diagram, but it is the scale’s next note.')
EX.append(dict(id='hm', title='B♭ harmonic minor, in position',
               idea=('The scale gypsy players use in a minor key, which you must know two ways: in one position, and reaching over. '
                     'Ours is B♭ harmonic minor, a fret above their A harmonic minor: the scale for your C half-diminished and F7♭9 in bar 10, going to B♭ minor in bar 11.'),
               quote=quote('hm', 4, 'theirs is A harmonic minor at the 5th fret: A, B, C, D.', 18),
               bars=b))
b = run_ex('hm2', 'B♭ harmonic minor, reaching over')
b[0]['note'] = ('The same scale over two octaves and a fourth, from the B♭ at the 6th fret of the low E string to the E♭ at the 11th fret of the high E string; '
                f'from the D string on, the hand moves up the neck as the scale climbs. Fingers: {fingers_txt("hm2")}.')
EX.append(dict(id='hm2', title='B♭ harmonic minor, reaching over',
               idea='The second way: the hand moves up as the scale climbs, so it reaches higher with the same few fingers.',
               quote=quote('hm2', 4, 'theirs is A harmonic minor from the 5th fret: A, B, C, D, the same start.', 18),
               bars=b))

# ---------------------------------------------------------------- chapter 3: the minor triad with a 6th and with a 9th
b = run_ex('m6a', 'B♭ minor 6, from the root')
b[0]['note'] = f'B♭, D♭, F and G (the 6th) from the B♭ at the 6th fret of the low E string, over two octaves and a third; then back. Fingers: {fingers_txt("m6a")}.'
EX.append(dict(id='m6a', title='B♭ minor 6, from the root',
               idea=('The minor chord coloured with the major 6th, a colour gypsy players love in a minor key. Two positions: the first starts on the root, the second on the 5th. '
                     'Ours is B♭m6, a fret above their Am6.'),
               quote=quote('m6a', 3, 'theirs is Am6 at the 5th fret: A, C, E.', 25),
               bars=b))
b = run_ex('m6b', 'B♭ minor 6, from the 5th')
b[0]['note'] = f'F, G, B♭, D♭ from the F at the 13th fret of the low E string, up to the G at the 15th fret of the high E string; then back. Fingers: {fingers_txt("m6b")}.'
EX.append(dict(id='m6b', title='B♭ minor 6, from the 5th',
               idea='The second position, high on the neck, starting on the chord’s 5th.',
               quote=quote('m6b', 3, 'theirs is Am6 at the 12th fret: E, F♯, A.', 25),
               bars=b))
b = run_ex('m9a', 'B♭ minor with the 9th, at the 6th fret')
b[0]['note'] = f'B♭, C (the 9th), D♭ and F from the 6th fret of the low E string up to the F at the 13th fret of the high E string; then back. Fingers: {fingers_txt("m9a")}.'
EX.append(dict(id='m9a', title='B♭ minor with the 9th, from the 6th fret',
               idea=('The minor chord coloured with the major 2nd (the 9th) instead of the 6th. Two positions, both from the root: one at the 6th fret, one at the bottom of the neck. '
                     'Ours is B♭ minor with the 9th, a fret above their A minor with the 9th.'),
               quote=quote('m9a', 3, 'theirs is at the 5th fret: A, B, C.', 26),
               bars=b))
b = run_ex('m9b', 'B♭ minor with the 9th, at the 1st fret')
b[0]['note'] = ('From the B♭ at the 1st fret of the A string up to the B♭ at the 6th fret of the high E string; then back. Theirs starts on the open A string; '
                'ours takes that note at the 1st fret with the index, then the index moves to the 3rd fret (the middle finger takes the D♭ at the 4th).')
EX.append(dict(id='m9b', title='B♭ minor with the 9th, from the 1st fret',
               idea='The second position, low on the neck.',
               quote=quote('m9b', 3, 'theirs starts on the open A string: A, B, C.', 26),
               bars=b))

# ---------------------------------------------------------------- chapter 4: speed
def speed_bars(key, chord, grip, what):
    seq = ours(key)
    names = [name_of(key, s, f) for s, f in seq]
    out = [dict(chords=[chord], note='', items=[['C', chord, grip, 4.0, {'roll': 0.02}]])]
    for _ in range(4):
        notes = seq * 2
        out.append(dict(chords=[chord], note='', items=[['R', [list(x) for x in notes], [1 / 3] * 12, '=' + ','.join(names * 2) + '|' + what]]))
    out.append(dict(chords=[chord], note='', items=[['C', chord, grip, 4.0, {'roll': 0.02}]]))
    return out


G1 = [f + 1 for f in GRIP_THEIRS['sp1']]
G2 = [f + 1 for f in GRIP_THEIRS['sp2']]
b = speed_bars('sp1', 'Bbm6/9', G1, 'six notes on two strings')
b[0]['note'] = ('First the chord, B♭m6/9 with the root on the low E string at the 6th fret (the thumb takes it). Then six notes on the top two strings, D♭ C B♭ on the high E string, '
                f'A♭ G F on the B string, in triplets, twelve to a bar, over and over; then the chord again. Fingers: {fingers_txt("sp1")} (little, ring, index).')
EX.append(dict(id='sp1', title='Speed on two strings: B♭ minor 6/9',
               idea=('For speed and for the two hands together: six notes on two strings inside a chord’s shape, round and round in triplets with a metronome, faster each day, '
                     'while you see the chord under them. Ours is a fret above theirs, over B♭m6/9.'),
               quote=quote('sp1', 3, 'theirs is in Am6/9 at the 5th fret, from the C at the 8th fret of the high E string: C, B, A.', 33),
               bars=b))
b = speed_bars('sp2', 'Ab6/9', G2, 'six notes on two strings')
b[0]['note'] = ('A♭6/9 with the root at the 4th fret of the low E string, then C B♭ A♭ on the high E string and G F E♭ on the B string, two frets apart, in triplets; then the chord. '
                f'Fingers: {fingers_txt("sp2")} (little, middle, index).')
EX.append(dict(id='sp2', title='Speed on two strings: A♭ 6/9',
               idea=('The same on the major chord a step below: theirs is G6/9 under A minor, ours A♭6/9 under B♭ minor. '
                     'The song’s A♭ chords are sevenths (A♭7, A♭13), so this one is practice for the hands rather than a sound from the song.'),
               quote=quote('sp2', 3, 'theirs is in G6/9 at the 3rd fret, from the B at the 7th fret of the high E string: B, A, G.', 33),
               bars=b))
seq = THEIRS['chrom']
full = up_down(seq)
names = [name_of('chrom', s, f, down=i >= len(seq)) for i, (s, f) in enumerate(full)]
b = bars_of(full, names, 'the chromatic scale with open strings', None)
trip = []
for i in range(0, len(full), 12):
    ns, nm = full[i:i + 12], names[i:i + 12]
    durs = [1 / 3] * len(ns)
    if i + 12 >= len(full): durs[-1] = 4 - (len(ns) - 1) / 3
    trip.append(dict(chords=[], note='', items=[['R', [list(x) for x in ns], durs, '=' + ','.join(nm) + '|the same in triplets']]))
trip[0]['note'] = 'The same scale in triplets, twelve notes to a bar.'
b[0]['note'] = ('Every note from the open low E string to the G♯ at the 4th fret of the high E string, one finger for each fret (index on the 1st, little on the 4th) and the open strings between; '
                'on the G string stop at the 3rd fret, because the next note, B, is the open B string. Up in eighths and back down; then the same in triplets.')
EX.append(dict(id='chrom', title='The chromatic scale with open strings',
               idea=('Django used the open strings in his chromatic runs: they roll fast and clean. The chromatic scale is the same in every key, so this one is exactly theirs; '
                     'the open strings are the point of it.'),
               quote=quote('chrom', 4, 'theirs is the whole scale in the first position, from the open low E string: E, F, F♯, G.', 34),
               bars=b + trip))

SECTIONS = [
    dict(id='rom-1', title='Minor triads and the diminished seventh', part='Exercises', ex=EX[0:4]),
    dict(id='rom-2', title='Major triads and the harmonic minor scale', part='Exercises', ex=EX[4:8]),
    dict(id='rom-3', title='The minor triad with a 6th or a 9th', part='Exercises', ex=EX[8:12]),
    dict(id='rom-4', title='Speed', part='Exercises', ex=EX[12:15]),
]
