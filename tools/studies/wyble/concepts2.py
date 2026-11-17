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
}
WHERE = {'P1U': (11, 7), 'P1D': (11, 8), 'P2U': (12, 1), 'P2D': (12, 2), 'E9': (14, 1), 'E10U': (15, 1), 'E10D': (15, 2)}   # PDF page, system
BOOKP = {'P1U': 9, 'P1D': 9, 'P2U': 10, 'P2D': 10, 'E9': 12, 'E10U': 13, 'E10D': 13}


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
        for e in ev[b:b + per]:
            lo, up = (e[0], e[1]) if len(e) == 2 else ((e[0], None) if e[0] < 60 else (None, e[0]))
            seq.append((lo, up, d))
        out.append(two_lines(place_lines(seq, lo_strings=(6, 5, 4, 3), up_strings=(1, 2, 3, 4), maxf=15), over=ch if b == 0 else ''))
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
    bars = [dict(chords=[ch] if i == 0 else [], note='', items=[b]) for i, b in enumerate(bs)]
    bars[0]['note'] = first_note.format(ch=ch.replace('b', '♭'), what=what, a=nm(ev[0][0]), b=nm(ev[0][-1]))
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
SECTION = dict(id='concepts-2', title='Concepts: sequences', part='Exercises', ex=EX)
