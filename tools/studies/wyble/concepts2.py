"""Wyble & Berman, Concepts for the Classical and Jazz Guitar: Exercises 8, 9 and 10 (book pp. 9–13; PDF pages 11–15).
Each is a mechanical figure of two-note shapes: the top voice moves by half steps while the lower voice alternates two
moves, or a cell of three or six shapes repeats a whole step higher each time. Wyble starts them on the tritone of a
seventh chord (its 3rd and 7th). Ours: the same figure, shape for shape and step for step, started on the 3rd and 7th
(or the pair of chord tones his opening has) of one of Moonglow's chords, for the first bars; the figure then carries on
by its own rule, as his does. His notes are written out below as printed (written pitch, an octave above the sound);
check_concepts2.py reads them again from the book's own music and checks every note of ours against them."""
import sys, re
sys.path.insert(0, '/home/claude/studies')
from kit_study import place_lines, two_lines

W1 = 'Concepts for the Classical and Jazz Guitar'
LET = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
NAMES = ['C', 'D♭', 'D', 'E♭', 'E', 'F', 'G♭', 'G', 'A♭', 'A', 'B♭', 'B']


def wm(n):
    """written pitch name to midi"""
    m = re.fullmatch(r'([A-G])([♯♭]?)(\d)', n)
    return 12 * (int(m.group(3)) + 1) + LET[m.group(1)] + (m.group(2) == '♯') - (m.group(2) == '♭')


# his figures, event by event (a '+' joins notes struck together), written pitch, as printed
HIS = {
    'P1U': 'G♯3+D5 C4+E♭5 B♭3+E5 D4+F5 C4+F♯5 E4+G5 D4+G♯5 F♯4+A5 E4+B♭5 G♯4+B5 F♯4+C6 A♯4+C♯6 A♭4+D6 C5+E♭6 B♭4+E6 D5+F6',
    'P1D': 'D5+F6 B♭4+E6 C5+E♭6 G♯4+D6 B♭4+C♯6 F♯4+C6 G♯4+B5 E4+B♭5 F♯4+A5 D4+G♯5 E4+G5 C4+F♯5 D4+F5 B♭3+E5 C4+E♭5 G♯3+D5',
    'P2U': 'G♯3+D5 G3+E♭5 B♭3+E5 A3+F5 C4+F♯5 B3+G5 D4+G♯5 C♯4+A5 E4+B♭5 E♭4+B5 F♯4+C6 F4+C♯6 G♯4+D6 G4+E♭6 B♭4+E6 A4+F6',
    'P2D': 'A4+F6 B♭4+E6 G4+E♭6 G♯4+D6 F4+C♯6 F♯4+C6 E♭4+B5 E4+B♭5 C♯4+A5 D4+G♯5 B3+G5 C4+F♯5 A3+F5 B♭3+E5 G3+E♭5 G♯3+D5',
    'E9': ('E3+B♭4 G♯3+B4 G3+C5 F♯3+C5 B♭3+C♯5 A3+D5 G♯3+D5 C4+E♭5 B3+E5 B♭3+E5 D4+F5 C♯4+F♯5 '
           'C4+F♯5 E4+G5 E♭4+G♯5 D4+G♯5 F♯4+A5 F4+B♭5 E4+B♭5 G♯4+B5 G4+C6 F♯4+C6 B♭4+C♯6 A4+D6'),
    'E10U': ('C4+F♯5 E4+G5 E♭4+G♯5 B3 C♯4+A4 E♭4 D4+G♯5 F♯4+A5 F4+B♭5 C♯4 E♭4+B4 F4 '
             'E4+B♭5 G♯4+B5 G4+C6 E♭4 F4+C♯5 G4 F♯4+C6 B♭4+C♯6 A4+D6 F4 G4+E♭5 A4'),
    'E10D': ('F♯4+C6 B♭4+C♯6 A4+D6 F4 G4+E♭5 A4 E4+B♭5 G♯4+B5 G4+C6 E♭4 F4+C♯5 G4 '
             'D4+G♯5 F♯4+A5 F4+B♭5 C♯4 E♭4+B4 F4 C4+F♯5 E4+G5 E♭4+G♯5 B3 C♯4+A4 E♭4'),
    'E12': ('E4+C5 G♯4 C4+G♯4 E4 G♯3+E4 C4 F♯3+B♭4 F4+C♯5 A4 C♯4+A4 F4 A3+F4 C♯4 G3+B4 '
            'F♯4+D5 B♭4 D4+B♭4 F♯4 B♭3+F♯4 D4 G♯3+C5'),
    'E19': ('F♯4+C6 A4 E5 F♯5 E5 A4 F♯4+C6 E4+B♭5 G4 D5 E5 D5 G4 E4+B♭5 '
            'D4+G♯5 F4 C5 D5 C5 F4 D4+G♯5 C4+F♯5 E♭4 B♭4 C5 B♭4 E♭4 C4+F♯5'),
    'E16': 'E♭4+C5 F♯3 A3+F♯4 G♯4 C4+A4 B4 E♭4+C5 D5 F♯4+E♭5 F5 A4+F♯5 G♯5 C5+A5',
    'E18': ('F♯3+A4 C4+E♭5 E♭4+C5 B3+D5 F♯4+E♭5 D4+F5 A3+C5 E♭4+F♯5 F♯4+E♭5 D4+F5 A4+F♯5 F4+G♯5 '
            'C4+E♭5 F♯4+A5 A4+F♯5 F4+G♯5 C5+A5 G♯4+B5 E♭4+F♯5 A4+C6 C5+A5 G♯4+B5 E♭5+C6 B4+D6'),
    'E20': ('D4+G♯5 F♯4 C5 D5 C5 F♯4 D4+G♯5 C4+F♯5 E4 B♭4 C5 B♭4 E4 C4+F♯5 B♭3+E5 D4 G♯4 B♭4 G♯4 D4 B♭3+E5'),
}
WHERE = {'P1U': (11, 7), 'P1D': (11, 8), 'P2U': (12, 1), 'P2D': (12, 2), 'E9': (14, 1), 'E10U': (15, 1), 'E10D': (15, 2), 'E12': (25, 1), 'E19': (29, 1), 'E16': (28, 1), 'E18': (28, 6), 'E20': (29, 3)}   # PDF page, system
BOOKP = {'P1U': 9, 'P1D': 9, 'P2U': 10, 'P2D': 10, 'E9': 12, 'E10U': 13, 'E10D': 13, 'E12': 23, 'E19': 27, 'E16': 26, 'E18': 26, 'E20': 27}


def events(key):
    return [sorted(wm(x) for x in ev.split('+')) for ev in HIS[key].split()]


# ours: (his figure, how many events, transposition in semitones, Moonglow's chord, its two tones the figure starts on, beat length, events a bar)
OURS = {
    'P1U': ('G13', 3, 8, 'B and F, the 3rd and 7th', 1.0, 4),
    'P1D': ('Am7', -5, 8, 'A and C, the root and 3rd', 1.0, 4),
    'P2U': ('Db9', -3, 8, 'F and C♭, the 3rd and 7th', 1.0, 4),
    'P2D': ('D9', -3, 8, 'F♯ and D, the 3rd and root', 1.0, 4),
    'E9': ('F9', 5, 12, 'A and E♭, the 3rd and 7th', 1 / 3, 12),
    'E10U': ('E9', 2, 12, 'D and G♯, the 7th and 3rd', 0.5, 6),
    'E10D': ('Eb9', 1, 12, 'G and D♭, the 3rd and 7th', 0.5, 6),
    'E12': ('Db9#5', 1, 14, 'F and D♭, the 3rd and root', [0.5] * 6 + [1.0], 7),
    'E19': ('Eb9', 1, 14, 'G and D♭, the 3rd and 7th', [0.5] * 6 + [1.0], 7),
    'E16': ('Abdim7', -1, 13, 'D and B', [0.5] * 12 + [1.0], 8),
    'E18': ('Abdim7', 2, 12, 'A♭ and B', 1 / 3, 12),
    'E20': ('Eb9', -1, 14, 'D♭ and G, the 7th and 3rd', [0.5] * 6 + [1.0], 7),
}


def ours_events(key):
    ch, tr, n, what, d, per = OURS[key]
    return [[m - 12 + tr for m in ev] for ev in events(key)[:n]]


def bars_of(key):
    ch, tr, n, what, d, per = OURS[key]
    ev = ours_events(key)
    out = []
    for b in range(0, len(ev), per):
        seq = []
        for j, e in enumerate(ev[b:b + per]):
            lo, up = (e[0], e[1]) if len(e) == 2 else ((e[0], None) if e[0] < 55 else (None, e[0]))
            seq.append((lo, up, d[b + j] if isinstance(d, list) and len(d) > per else (d[j] if isinstance(d, list) else d)))
        it = two_lines(place_lines(seq, lo_strings=(6, 5, 4, 3), up_strings=(1, 2, 3, 4), maxf=15), over=ch if b == 0 else '')
        L = sum(x[2] for x in seq)
        full = 3 if key.startswith('E10') else 4
        out.append([it] + ([['W', full - L]] if L < full - 1e-9 else []))      # a rest where his figure ends before the bar does
    return out


def nm(m): return NAMES[m % 12]


def quote(key):
    e = events(key)[0]
    seq = [(e[0] - 12, e[1] - 12, 1.0)]
    return two_lines(place_lines(seq, lo_strings=(6, 5, 4, 3), up_strings=(1, 2, 3, 4), maxf=15))


def ex(key, id_, title, idea, his_text, first_note, more_note):
    ch, tr, n, what, d, per = OURS[key]
    bs = bars_of(key)
    ev = ours_events(key)
    bars = [dict(chords=[ch] if i == 0 else [], note='', items=b) for i, b in enumerate(bs)]
    bars[0]['note'] = first_note.format(ch=ch.replace('b', '♭', 1).replace('#', '♯').replace('dim7', '°7'), what=what, a=nm(ev[0][0]), b=nm(ev[0][-1]))
    if len(bars) > 1: bars[1]['note'] = more_note
    p = BOOKP[key]
    return dict(id=id_, title=title, idea=idea,
                quote=dict(where=f'{W1}, p. {p}', text=his_text, item=quote(key), whose='Wyble’s own', played='Played here: its first shape.'),
                bars=bars)


EX = [
    ex('P1U', 'c-8-1-up', 'Exercise 8, pattern 1, climbing',
       ('Two voices, the top climbing by half steps, the bottom up a major third, then down a whole step, so the pair is a tritone and an octave apart, '
        'then a minor tenth, and so on, one pair to a beat. Wyble starts it on the 3rd and 7th of E7.'),
       'pattern 1 climbing from G♯ with D above (the 3rd and 7th of E7), sixteen pairs in quarter notes, fingered and with strings marked.',
       'From {what} of Moonglow’s {ch} (bar 7): the top up a half step each beat, the bottom up a major third, down a whole step, in turn. '
       'Thumb on the low note, a finger on the high one.',
       'The rule carries on by itself up the neck; Wyble takes it two bars further.'),
    ex('P1D', 'c-8-1-down', 'Exercise 8, pattern 1, falling',
       'The same pattern coming down: the top falling by half steps, the bottom down a major third, then up a whole step.',
       'pattern 1 falling from D with F above, sixteen pairs.',
       'From {what} of Moonglow’s {ch} (bar 6): the top down a half step each beat, the bottom down a major third, up a whole step, in turn.',
       'On down by the same rule.'),
    ex('P2U', 'c-8-2-up', 'Exercise 8, pattern 2, climbing',
       'Pattern 2: the top still climbs by half steps, but the bottom goes down a half step, then up a minor third: the pair is a tritone and an octave apart, then a minor 13th.',
       'pattern 2 climbing from G♯ with D above, sixteen pairs.',
       'From {what} of Moonglow’s {ch} (bar 2): the top up a half step each beat, the bottom down a half step, up a minor third, in turn.',
       'Up the neck by the same rule.'),
    ex('P2D', 'c-8-2-down', 'Exercise 8, pattern 2, falling',
       'Pattern 2 coming down: the top falls by half steps, the bottom goes up a half step, then down a minor third.',
       'pattern 2 falling from A with F above, sixteen pairs.',
       'From {what} of Moonglow’s {ch} (bar 22): the top down a half step each beat, the bottom up a half step, down a minor third, in turn.',
       'On down by the same rule.'),
    ex('E9', 'c-9', 'Exercise 9: sets of three in triplets',
       ('A set of three shapes, the tritone and two neighbours, played as a triplet; the next set is the same a whole step higher, and so on. '
        'Wyble starts on the 3rd and 7th of C7.'),
       'sets of three placed in triplets, from E with B♭ above (the 3rd and 7th of C7), twenty-four shapes over two bars.',
       'From {what} of the F9 that opens Moonglow’s bridge, four sets a bar, each a whole step above the last.',
       ''),
    ex('E10U', 'c-10-up', 'Exercise 10, climbing',
       ('A bar of six eighths in 3/4: three two-note shapes, a single bass note, a shape, a single note; the next bar is the same a whole step higher. '
        'Wyble starts it on C and F♯, the 7th and 3rd of D7.'),
       'in 3/4, from C with F♯ above, four bars, each a whole step higher.',
       'From {what} of Moonglow’s {ch} (bar 21): the six-note bar, then the same a whole step up.',
       'A whole step higher, as the rule goes on.'),
    ex('E10D', 'c-10-down', 'Exercise 10, falling',
       'The same bar coming down a whole step at a time.',
       'falling from F♯ with C above, four bars.',
       'From {what} of Moonglow’s {ch} (bar 1): the bar, then the same a whole step down.',
       'A whole step lower.'),
]
EX += [
    ex('E12', 'c-12', 'Exercise 12: the augmented triad, falling, a half step higher each bar',
       ('Two voices falling through an augmented triad: the lower in quarters, the upper in eighths, each of its notes struck again on the next beat with the lower voice under it; '
        'on beat 4 a shape that leads a half step up into the next bar, where the figure starts again. Wyble starts on C augmented.'),
       'from E with C above, C augmented falling, the figure a half step higher each bar for nine bars.',
       'From {what} of Moonglow’s {ch} (bar 43), D♭ augmented: the upper voice D♭, A, A, F, F, D♭ in eighths, the lower F, D♭, A in quarters, then the lead-in.',
       'A half step higher: D augmented, as the rule goes on.'),
    ex('E19', 'c-19', 'Exercise 19: a ninth chord, a whole step lower each bar',
       ('A bar on one ninth chord: its 3rd and 7th together, then its 5th, 9th, 3rd, 9th and 5th in eighths, and the 3rd and 7th again on beat 4; '
        'the next bar is the same a whole step lower. Wyble starts on D9 and goes down to A♭9.'),
       'from F♯ with C above, D9, then C9, B♭9, A♭9.',
       'From {what} of Moonglow’s {ch} (bar 1): its 3rd and 7th, then B♭, F, G, F, B♭ in eighths, and G with D♭ again.',
       'A whole step lower: D♭9, Moonglow’s own second chord (bar 2).'),
]
EX += [
    ex('E16', 'c-16', 'Exercise 16: the diminished chord climbing by minor thirds',
       ('Two notes of a diminished seventh chord together, then one note alone a half step below the top of the next pair; every pair a minor third higher than the last, '
        'in eighths, up to a held pair at the top. Wyble starts on E♭ and C.'),
       'from E♭ with C above (the diminished chord E♭, F♯, A, C), thirteen shapes, each pair a minor third higher, the strings and fingers marked.',
       'From {what} of Moonglow’s {ch} (bar 44): D and B together, F alone, then pairs a minor third apart up the neck, each with the note a half step below the next top note.',
       'The last pairs and the held top: two notes of the same chord, an octave and a minor third higher.'),
    ex('E18', 'c-18', 'Exercise 18: the diminished chord in triplets',
       ('Two-note shapes from a diminished seventh chord in triplets, six to a figure, the figure a minor third higher each time; '
        'the top and bottom move against each other inside the chord. Wyble starts on F♯ and A.'),
       'from F♯ with A above, triplets, twenty-four shapes over two bars.',
       'From {what} of Moonglow’s {ch} (bar 44): one bar, two figures of six, the second a minor third higher.',
       ''),
    ex('E20', 'c-20', 'Exercise 20: a seventh chord with its 9th and ♭13, a whole step lower each bar',
       ('Like Exercise 19 on another chord: the 7th and 3rd together, then the 9th, the ♭13, the 7th, the ♭13 and the 9th in eighths, and the 7th and 3rd again; '
        'the next bar a whole step lower. Wyble starts on D and G♯, the 7th and 3rd of E7.'),
       'from D with G♯ above, E7, then D7 and C7.',
       'From {what} of Moonglow’s E♭9 (bar 1): D♭ and G, then F, B, D♭, B, F in eighths, and D♭ with G again.',
       'A whole step lower: D♭, as Moonglow’s bar 2.'),
]
SECTION = dict(id='concepts-2', title='Concepts: sequences', part='Exercises', ex=EX)
