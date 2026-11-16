"""Wyble: two lines at once. The entry's content: our exercises set on the chords of one of the owner's songs, each
beside a short quote of the opening of Wyble's own (a beat) and its page in the owner's copy.
Part I, section 1: the two-line basics (The Art of Two-Line Improvisation, pp. 1–7, Examples 1–23).
Each exercise keeps Wyble's device exactly: the same rhythm in each voice, the same ratio of notes between the voices,
the same direction of each voice, the same bar-to-bar change (bar 2 of Examples 2–13 falls back with the upper voice
displaced an eighth). What changes is the scale: Wyble writes them on his own scale in C and asks for all twelve keys;
here each is on the chord scale of Moonglow (in F) at that spot."""
import sys
sys.path.insert(0, '/home/claude/studies')
from kit_study import N, place, two_lines, nn, place_lines, shape

W2 = 'The Art of Two-Line Improvisation'
LOW, UP = (6, 5, 4, 3), (1, 2, 3, 4)


def lo(n, a=5, b=8): return place(N(n), a, b, LOW)
def up(n, a=5, b=8): return place(N(n), a, b, UP)


def T(lower, upper, over, beats=None, **kw):
    """lower, upper: lists of note names (or None) per step; beats: per-step lengths (default eighths)."""
    n = max(len(lower), len(upper))
    lower = lower + [None] * (n - len(lower)); upper = upper + [None] * (n - len(upper))
    beats = beats or [0.5] * n
    seq = [(N(a) if a else None, N(b) if b else None, d) for a, b, d in zip(lower, upper, beats)]
    return two_lines(place_lines(seq, **kw), over=over)


def run(notes, over):
    st = place_lines([(N(n), None, .5) for n in notes], lo_strings=(6, 5, 4, 3, 2))
    return ['R', [g[0] for g, d in st], [.5] * len(notes), over]


def on_beats(notes):          # one upper note on each beat: steps 0, 2, 4, 6
    out = [None] * 8
    for i, x in enumerate(notes): out[2 * i] = x
    return out


def off_beats(notes):         # one upper note on each "and": steps 1, 3, 5, 7
    out = [None] * 8
    for i, x in enumerate(notes): out[2 * i + 1] = x
    return out


BMAJ_UP = ['Bb2', 'C3', 'D3', 'E3', 'F3', 'G3', 'A3', 'Bb3']             # B♭ major 7: B♭ with E natural (Moonglow is in F)
BM6_DOWN = ['Bb3', 'A3', 'G3', 'F3', 'Eb3', 'Db3', 'C3', 'Bb2']          # B♭ minor 6: B♭ minor with G and A
BM6_UP = list(reversed(BM6_DOWN))
RH2 = 'Thumb and index take turns on the lower line; the upper note is struck by m or a together with the thumb.'

EX = []          # each: dict(id, title, idea, quote=dict(where, text, item), bars=[dict(chords, items, note)])

EX.append(dict(
    id='one-line', title='One line, two fingers',
    idea='Every line in this entry is played by two fingers taking turns: the thumb and the index on a single line, so that later the thumb can keep a low line and the fingers an upper one.',
    quote=dict(where=f'{W2}, p. 1, Example 1',
               text='The scale Wyble uses for all the opening examples: C, D, E♭, F♯, G♯, A, B, a major scale with its 3rd lowered and its 4th and 5th raised. He asks for every single line to be played thumb and index in turn, and for every example in all twelve keys.',
               item=['R', [[5, 3], [5, 5], [5, 6], [4, 4], [4, 6], [4, 7], [3, 4], [3, 5]], [.5] * 8, '=C,D,E♭,F♯,G♯,A,B,C']),
    bars=[dict(chords=['Bbmaj7'], note='B♭ major 7, the first chord of Moonglow’s A section: from B♭ on the low E string (6th fret) up to the B♭ an octave higher, thumb and index in turn, starting with the thumb. Hand at the 5th fret.',
               items=[run(BMAJ_UP, 'Bbmaj7')]),
          dict(chords=['Bbm6'], note='B♭ minor 6, the next chord: back down from B♭ to B♭ through B♭ minor with the G and A of minor 6.',
               items=[run(BM6_DOWN, 'Bbm6')])]))

# ---- Examples 2–7: a held note above. Bar 1: the lower line climbs in eighths, the held note struck on every beat.
#      Bar 2: the lower line falls; the held note comes on every "and" (an eighth rest first). Wyble does it with six
#      different held notes over the same scale; here three, over Moonglow's first two chords.
held = []
for top, where in (('A4', 'the tune’s long A (the high E string, 5th fret)'), ('F4', 'F, the 5th of both chords'), ('C5', 'C, the 9th of both chords')):
    held += [dict(chords=['Bbmaj7'], note=f'Bar 1 of the pair: {where} on every beat; under it the B♭ major 7 line climbs in eighths. {RH2}',
                  items=[T(BMAJ_UP, on_beats([top] * 4), 'Bbmaj7')]),
             dict(chords=['Bbm6'], note=f'Bar 2: the line falls through B♭ minor 6, and the {top[:-1].replace("b", "♭")} moves off the beat: rest an eighth, then strike it on every “and”. Start the line with the index, so the thumb comes with the upper note.',
                  items=[T(BM6_DOWN, off_beats([top] * 4), 'Bbm6')])]
EX.append(dict(
    id='held-above', title='A held note above',
    idea='The plainest counterpoint: one voice stays on one note while the other moves. In the first bar the held note is struck on every beat; in the second the line turns round and the held note moves off the beat, so the two voices stop sharing a rhythm.',
    quote=dict(where=f'{W2}, pp. 2–3, Examples 2–7 (the opening of Example 2)',
               text='The lower voice climbs his scale from C on the A string (3rd fret) in eighths while the upper voice strikes D on the B string (3rd fret) on every beat; in the second bar the lower voice falls and the D comes on the off-beats. Examples 3–7 do the same with other held notes. The opening: C and D together, then D on the open D string.',
               item=two_lines([[[5, 3], [2, 3]], [[4, 0]]])),
    bars=held))

EX.append(dict(
    id='held-below', title='A held note below',
    idea='The same with the voices swapped: the bass stays and the upper voice moves. Bar 1 strikes the bass on every beat, bar 2 on every “and”.',
    quote=dict(where=f'{W2}, p. 2, the note above Examples 2–7',
               text='Wyble asks you to try the held note in the lower voice as well. There is no written example of it; this is it.',
               item=None),
    bars=[dict(chords=['Dm9'], note='D minor 9 (Moonglow’s third bar): the open D string with the thumb on every beat, a pedal that frees the left hand; the fingers climb from E (B string, 5th fret) to the E an octave up, shifting up the high E string at the end.',
               items=[T(on_beats(['D3'] * 4), ['E4', 'F4', 'G4', 'A4', 'B4', 'C5', 'D5', 'E5'], 'Dm9', lo_strings=(4,), up_strings=(1, 2, 3))]),
          dict(chords=['G13'], note='G13: the fingers fall back from E; the thumb strikes the open D (the 5th of G) on every “and”.',
               items=[T(off_beats(['D3'] * 4), ['E5', 'D5', 'C5', 'B4', 'A4', 'G4', 'F4', 'E4'], 'G13', lo_strings=(4,), up_strings=(1, 2, 3))])]))

EX.append(dict(
    id='contrary-2-1', title='Contrary motion, two notes against one',
    idea='The voices move in opposite directions: in the first bar the bass climbs in eighths while the top falls in quarters, two lower notes to every upper one; in the second the bass falls and the top climbs, now on the off-beats.',
    quote=dict(where=f'{W2}, pp. 3–4, Examples 8–13 (the opening of Example 8)',
               text='The lower voice climbs from C on the low E string (8th fret); the upper voice falls from D on the high E string (10th fret), one upper note to every two lower ones; in the second bar the lower voice falls and the upper climbs on the off-beats. The opening: C and D together, then D on the low E string (10th fret).',
               item=two_lines([[[6, 8], [1, 10]], [[6, 10]]])),
    bars=[dict(chords=['Am7', 'Dm9'], note=f'Moonglow’s third bar, A minor 7 then D minor 9: the bass climbs A to A, the top falls G, F, E, D on the beats. {RH2}',
               items=[T(['A2', 'B2', 'C3', 'D3', 'E3', 'F3', 'G3', 'A3'], on_beats(['G4', 'F4', 'E4', 'D4']), 'Am7')]),
          dict(chords=['Am7', 'Dm9'], note='The same chords, the lines turned round: the bass falls A to A, the top climbs D, E, F, G, each on an “and”. Start the bass with the index, so the thumb comes with the upper note.',
               items=[T(['A3', 'G3', 'F3', 'E3', 'D3', 'C3', 'B2', 'A2'], off_beats(['D4', 'E4', 'F4', 'G4']), 'Am7')]),
          dict(chords=['Gm7', 'C9'], note='On G minor 7 and C9, the bar before Moonglow comes home: the bass climbs G to G, the top falls F, E, D, C on the beats.',
               items=[T(['G2', 'A2', 'Bb2', 'C3', 'D3', 'E3', 'F3', 'G3'], on_beats(['F4', 'E4', 'D4', 'C4']), 'C9')]),
          dict(chords=['Gm7', 'C9'], note='Turned round: the bass falls G to G, the top climbs C, D, E, F on the off-beats, the thumb with each upper note.',
               items=[T(['G3', 'F3', 'E3', 'D3', 'C3', 'Bb2', 'A2', 'G2'], off_beats(['C4', 'D4', 'E4', 'F4']), 'C9')])]))

# ---- Examples 14–17: note against note (1:1), contrary motion: the voices close in, then open out again.
EX.append(dict(
    id='contrary-1-1', title='Contrary motion, note against note',
    idea='Both voices in eighths, one note against one, moving in opposite directions: they close in for a bar and open out again in the next. Where they meet changes: on a 2nd, on the same note, or crossing over.',
    quote=dict(where=f'{W2}, p. 5, Examples 14–17 (the opening of Example 14)',
               text='The lower voice climbs from C on the low E string (8th fret) while the upper voice falls from D on the high E string (10th fret), a note against a note, until they are a 2nd apart; the second bar opens them out again. Example 15 starts two octaves apart and meets on the same note, Example 16 crosses over. The opening: C and D, then D on the A string (5th fret) and C on the high E string (8th fret).',
               item=two_lines([[[6, 8], [1, 10]], [[5, 5], [1, 8]]])),
    bars=[dict(chords=['Bbmaj7'], note=f'Closing in on B♭ major 7: the bass climbs B♭ to B♭, the top falls C to C; they meet a 2nd apart. Thumb and index take turns on the lower line, m and a on the upper.',
               items=[T(BMAJ_UP, ['C5', 'Bb4', 'A4', 'G4', 'F4', 'E4', 'D4', 'C4'], 'Bbmaj7')]),
          dict(chords=['Bbm6'], note='Opening out on B♭ minor 6: from the same 2nd, the bass falls and the top climbs back to C.',
               items=[T(BM6_DOWN, ['C4', 'Db4', 'Eb4', 'F4', 'G4', 'A4', 'Bb4', 'C5'], 'Bbm6')]),
          dict(chords=['Gm7', 'C9'], note='Two octaves apart on G minor 7 and C9: the bass climbs E to E, the top falls E to E, and they meet on the same E: the G string, 9th fret, against the open high E string.',
               items=[T(['E3', 'F3', 'G3', 'A3', 'Bb3', 'C4', 'D4', 'E4'], ['E5', 'D5', 'C5', 'Bb4', 'A4', 'G4', 'F4', 'E4'], 'C9', lo_strings=(6, 5, 4, 3, 2))]),
          dict(chords=['F6'], note='From the same E, out again over F6: the bass falls to E, the top climbs to E.',
               items=[T(['E4', 'D4', 'C4', 'Bb3', 'A3', 'G3', 'F3', 'E3'], ['E4', 'F4', 'G4', 'A4', 'Bb4', 'C5', 'D5', 'E5'], 'F6', lo_strings=(6, 5, 4, 3, 2))]),
          dict(chords=['Am7', 'Dm9'], note='Crossing over on A minor 7 and D minor 9: the bass climbs A to A, the top falls G to G, and in the last eighth the top is a step under the bass (the open G under the A on the D string).',
               items=[T(['A2', 'B2', 'C3', 'D3', 'E3', 'F3', 'G3', 'A3'], ['G4', 'F4', 'E4', 'D4', 'C4', 'B3', 'A3', 'G3'], 'Am7')]),
          dict(chords=['G13'], note='Uncrossing on G13: the bass falls back to A, the top climbs back to G.',
               items=[T(['A3', 'G3', 'F3', 'E3', 'D3', 'C3', 'B2', 'A2'], ['G3', 'A3', 'B3', 'C4', 'D4', 'E4', 'F4', 'G4'], 'G13')])]))

# ---- Examples 18–19: three lower notes to one upper: the upper voice in a dotted quarter, an eighth tied to a
#      quarter, and a quarter (3 + 3 + 2 eighths), so its second note comes off the beat.
EX.append(dict(
    id='three-to-one', title='Three notes against one',
    idea='Three lower notes to each upper one: the upper voice lasts three eighths, then three, then two, so its second note lands between beats 2 and 3. First the top falls; then it climbs and comes back.',
    quote=dict(where=f'{W2}, p. 6, Examples 18–19 (the opening of Example 18)',
               text='The lower voice climbs his scale from C on the A string (3rd fret) in eighths; above it B (high E string, 7th fret) lasts three eighths, then A, entering on the “and” of 2, three more, then G♯ for the last two. Example 19 has the upper voice go up and back: G♯, A, G♯. The opening: C and B together, then D on the A string (5th fret).',
               item=two_lines([[[5, 3], [1, 7]], [[5, 5]]])),
    bars=[dict(chords=['Bbmaj7'], note=f'The B♭ major 7 line climbs under A, G and F: A for three eighths, G from the “and” of 2, F on beat 4. {RH2}',
               items=[T(BMAJ_UP, ['A4', None, None, 'G4', None, None, 'F4', None], 'Bbmaj7')]),
          dict(chords=['Bbm6'], note='The B♭ minor 6 line climbs under F, G and F again: up a step and back.',
               items=[T(BM6_UP, ['F4', None, None, 'G4', None, None, 'F4', None], 'Bbm6')])]))

# ---- Example 20: the upper voice rocks between two notes a half step apart, in quarters: on the beats over a
#      climbing line, then on the "ands" over a falling one.
EX.append(dict(
    id='rocking', title='The upper voice rocks',
    idea='The upper voice stops going anywhere: it rocks between two notes a half step apart, a quarter each, while the line below climbs; in the second bar it rocks on the off-beats while the line falls.',
    quote=dict(where=f'{W2}, p. 6, Example 20 (its opening)',
               text='The lower voice climbs from C on the A string (3rd fret) in eighths; the upper rocks G♯, A, G♯, A on the high E string (4th and 5th fret), one to a beat; in the second bar the lower voice falls and the upper rocks on the off-beats. The opening: C and G♯ together, then D.',
               item=two_lines([[[5, 3], [1, 4]], [[5, 5]]])),
    bars=[dict(chords=['Bbmaj7'], note=f'A and B♭ on the high E string (5th and 6th fret), one to a beat, over the B♭ major 7 line. {RH2}',
               items=[T(BMAJ_UP, on_beats(['A4', 'Bb4', 'A4', 'Bb4']), 'Bbmaj7')]),
          dict(chords=['Bbm6'], note='The line falls through B♭ minor 6; B♭ and A rock on the “ands”. Start the line with the index, so the thumb comes with the upper note.',
               items=[T(BM6_DOWN, off_beats(['Bb4', 'A4', 'Bb4', 'A4']), 'Bbm6')])]))

# ---- Example 21: leaps in both voices. Bar 1: four eighths climb, then the lower voice leaps up, down and down to
#      a quarter on the low string; the upper falls by step in quarters. Bar 2: the upper moves in eighths with two
#      wide leaps to a long note; the lower: a quarter, then a long note a leap below.
EX.append(dict(
    id='leaps', title='Leaps',
    idea='The lines leave the scale. After four steps the bass leaps up a 7th, down a 5th and down to the low A while the top falls in quarters; then the top moves in eighths with leaps (down a 6th, up a 3rd, up a 6th) to a long note over a bass that drops to the root.',
    quote=dict(where=f'{W2}, p. 6, Example 21 (its opening)',
               text='The lower voice climbs four notes from C on the A string (3rd fret), then leaps up to C, down to E♭ and down to A on the low E string; the upper voice falls B, A, G♯, F♯ in quarters. In the second bar the upper voice moves in eighths with wide leaps to a long B. The opening: C and B together, then D.',
               item=two_lines([[[5, 3], [1, 7]], [[5, 5]]])),
    bars=[dict(chords=['Am7', 'Dm9'], note=f'A minor 7 into D minor 9: the bass climbs A, B, C, D on the low E and A strings (5th–8th fret), leaps up to C (G string, 5th fret), down to F and down to A for a quarter; the top falls A, G, F, E, one to a beat. {RH2}',
               items=[T(['A2', 'B2', 'C3', 'D3', 'C4', 'F3', 'A2'], ['A4', None, 'G4', None, 'F4', None, 'E4'], 'Am7', beats=[.5, .5, .5, .5, .5, .5, 1.0])]),
          dict(chords=['G13'], note='G13: the top climbs E to F, drops a 6th to A, climbs to C and leaps a 6th to a long A; under it the bass plays B for a beat, then G for three.',
               items=[T(['B2', None, 'G2', None, None], ['E4', 'F4', 'A3', 'C4', 'A4'], 'G13', beats=[.5, .5, .5, .5, 2.0], up_strings=(1, 2, 3, 4))])]))

# ---- Example 22: a chromatic lower line (♭3, 2, ♭2, 1 of the chord) with its third note an octave up, in eighths,
#      the last held; above, the 6th for a dotted quarter, then the 7th from the "and" of 2, held.
EX.append(dict(
    id='chromatic-octave', title='A falling line, one note an octave up',
    idea='The lower voice walks down by half steps into the root, and its third note jumps up an octave: the line is still chromatic, but it no longer sounds like one. Above, the 6th of the chord, then its major 7th.',
    quote=dict(where=f'{W2}, p. 7, Example 22 (its opening)',
               text='The lower voice walks down E♭, D, D♭, C in eighths, with the D♭ an octave up, and holds the C; the upper voice holds A, then B from the “and” of 2. The opening: E♭ (A string, 6th fret) with A on the high E string (5th fret), then D (A string, 5th fret).',
               item=two_lines([[[5, 6], [1, 5]], [[5, 5]]])),
    bars=[dict(chords=['Bbmaj7'], note='On B♭ major 7, Moonglow’s first chord: D♭, C, then C♭ an octave up, and B♭ held; above, G for three eighths, then A held, the major 7th.',
               items=[T(['Db3', 'C3', 'B3', 'Bb2'], ['G4', None, None, 'A4'], 'Bbmaj7', beats=[.5, .5, .5, 2.5])]),
          dict(chords=['F6'], note='On F6, its last chord: A♭, G, G♭ an octave up, F held; above, D, then E.',
               items=[T(['Ab3', 'G3', 'Gb4', 'F3'], ['D5', None, None, 'E5'], 'F6', beats=[.5, .5, .5, 2.5])])]))

# ---- Example 23: Example 22 through the circle of fifths, a bar in each key.
EX.append(dict(
    id='circle', title='The same, round the circle of fifths',
    idea='The figure of the exercise before, a bar on each chord a fifth below the last: here from Moonglow’s F to its first chord, B♭, and on to E♭ and A♭.',
    quote=dict(where=f'{W2}, p. 7, Example 23 (its opening)',
               text='Example 22 in C, F, B♭ and E♭, one bar each, moving up and down the neck. The opening, in C: E♭ on the low E string (11th fret) with A on the B string (10th fret), then D on the low E string (10th fret).',
               item=two_lines([[[6, 11], [2, 10]], [[6, 10]]])),
    bars=[dict(chords=['F6'], note='F: A♭, G, G♭ up an octave, F; above, D, then E.',
               items=[T(['Ab3', 'G3', 'Gb4', 'F3'], ['D5', None, None, 'E5'], 'F6', beats=[.5, .5, .5, 2.5])]),
          dict(chords=['Bbmaj7'], note='B♭: D♭, C, C♭ up an octave, B♭; above, G, then A.',
               items=[T(['Db3', 'C3', 'B3', 'Bb2'], ['G4', None, None, 'A4'], 'Bbmaj7', beats=[.5, .5, .5, 2.5])]),
          dict(chords=['Ebmaj7'], note='E♭: G♭, F, F♭ (E) up an octave, E♭; above, C, then D.',
               items=[T(['Gb3', 'F3', 'E4', 'Eb3'], ['C5', None, None, 'D5'], 'Ebmaj7', beats=[.5, .5, .5, 2.5])]),
          dict(chords=['Abmaj7'], note='A♭: C♭ (B), B♭, B♭♭ (A) up an octave, A♭; above, F, then G.',
               items=[T(['B2', 'Bb2', 'A3', 'Ab2'], ['F4', None, None, 'G4'], 'Abmaj7', beats=[.5, .5, .5, 2.5])])]))

SECTIONS = [dict(id='basics', title='The two-line basics', part='Exercises', ex=EX)]


# ======================= Part II: Concepts for the Classical and Jazz Guitar (Wyble & Berman) =======================
W1 = 'Concepts for the Classical and Jazz Guitar'


def M(m): return nn(m).replace('♭', 'b')


def rule_dyads(lo0, up0, n, top, bot):
    """n dyads from (lo0, up0), the voices moving by the given steps in turn (semitones)."""
    lo_, up_ = N(lo0), N(up0); out = [(lo_, up_)]
    for i in range(n - 1):
        lo_ += bot[i % len(bot)]; up_ += top[i % len(top)]; out.append((lo_, up_))
    return out


def dyad_bars(dyads, over, broken=False, per_bar=4):
    """Quarter-note dyads (or the same broken into eighths, low then high), per_bar dyads a bar."""
    bars = []
    for b in range(0, len(dyads), per_bar):
        chunk = dyads[b:b + per_bar]
        if broken:
            seq = [x for lo_, up_ in chunk for x in ((lo_, None, .5), (None, up_, .5))]
        else:
            seq = [(lo_, up_, 1.0) for lo_, up_ in chunk]
        bars.append(two_lines(place_lines(seq, up_strings=(4, 3, 2, 1)), over=over))
    return bars


def intervals_ok(dyads, want=(11, 8)):
    return all((u - l) == want[i % 2] for i, (l, u) in enumerate(dyads))


CEX = []

# ---- Exercise 1 (with 2 and 3, the same cell higher up the neck): a minor 6th, a note, a major 7th, a note; the cell
#      moves up a minor 3rd each bar. Relative to the cell's first bass note X: X with the note a minor 6th above;
#      X + a whole step; X − a half step with X + a minor 7th; X + a minor 3rd (which is the next bar's X).
def cell1(x):
    X = N(x)
    return [(X, X + 8, 1.0), (X + 2, None, 1.0), (X - 1, X + 10, 1.0), (X + 3, None, 1.0)]

c1 = [two_lines(place_lines(cell1('F2'), up_strings=(5, 4, 3, 2)), over='F6'), two_lines(place_lines(cell1('Ab2'), up_strings=(5, 4, 3, 2)), over='')]
CEX.append(dict(
    id='c-cell', title='A 6th, a 7th, up a minor third',
    idea='One bar, four beats: two notes a minor 6th apart, a single note a step above the lower one, two notes a major 7th apart (the lower note a half step down, the upper a step up), and a single note a minor 3rd above where the bar began. That last note starts the next bar, so the bar climbs the neck in minor thirds; in four bars it has used all twelve notes.',
    quote=dict(where=f'{W1}, p. 4, Exercise 1 (CD 1), with Exercises 2 and 3 (pp. 5–6), the same bar carried higher',
               text='Wyble starts on C on the A string (3rd fret) with G♯ above it, then D, then B with A♯, then D♯, and goes on from E♭, F♯ and A; Exercises 2 and 3 carry it on up the neck. Berman’s versions play the beats in the order 3-4-2-1, play it falling, and put each single note an octave up. The opening: C with G♯ (G string, 1st fret).',
               item=two_lines([([[5, 3], [3, 1]], 1.0)])),
    bars=[dict(chords=['F6'], note='The same bar from F, Moonglow’s home note: F with D♭ above, G, E with E♭ above, A♭. Wyble writes it as a figure, not over a chord; on Moonglow it is a colour to slip in over the last F, or to practise on its own.',
               items=[c1[0]]),
          dict(chords=[], note='Up a minor third, from A♭: A♭ with E, B♭, G with F♯, B. Two more bars (from B and from D) bring it back to F an octave up.',
               items=[c1[1]])]))

# ---- Berman's patterns on p. 5: major 7th to minor 6th, each voice moving by fixed steps.
pa = rule_dyads('Bb2', 'A3', 8, top=(-2, +5), bot=(+1, +2)); assert intervals_ok(pa)
ba = dyad_bars(pa, 'Bbmaj7')
CEX.append(dict(
    id='c-7-6-up', title='Major 7th to minor 6th, climbing',
    idea='Two voices a major 7th apart close to a minor 6th and open again: the top steps down a whole step, then up a fourth; the bottom steps up a half step, then a whole step. Every two moves the pair is a minor third higher.',
    quote=dict(where=f'{W1}, p. 5, Berman’s pattern after Exercise 1 (CD 4)',
               text='Berman’s rule: major 7th to minor 6th, top voice down a major 2nd then up a 4th, bottom voice up a minor 2nd then up a major 2nd, in quarter notes from F with E above (low E string, 1st fret, and D string, 2nd fret). The opening: F with E, then F♯ with the open D.',
               item=two_lines([([[6, 1], [4, 2]], 1.0), ([[6, 2], [4, 0]], 1.0)])),
    bars=[dict(chords=['Bbmaj7'], note='From B♭ with A above, the major 7th of Moonglow’s first chord: B♭–A, B–G, C♯–C, D–B♭. Thumb on the lower note, a finger on the upper.', items=[ba[0]]),
          dict(chords=[], note='The rule carries on by itself: E–E♭, F–C♯, G–F♯, A♭–E, a minor third higher every two beats.', items=[ba[1]])]))

pb = rule_dyads('Bb3', 'A4', 8, top=(-2, -1), bot=(+1, -4)); assert intervals_ok(pb)
bb = dyad_bars(pb, 'Bbmaj7')
CEX.append(dict(
    id='c-7-6-down', title='Major 7th to minor 6th, falling',
    idea='The same two intervals going down the neck: the top steps down a whole step, then a half step; the bottom up a half step, then down a major third. Every two moves the pair is a minor third lower.',
    quote=dict(where=f'{W1}, p. 5, Berman’s second pattern (CD 4)',
               text='Top voice down a major 2nd then a minor 2nd, bottom voice up a minor 2nd then down a major 3rd, from F on the G string (10th fret) with E on the high E string (12th fret). The opening: F with E, then F♯ with D.',
               item=two_lines([([[3, 10], [1, 12]], 1.0), ([[3, 11], [1, 10]], 1.0)])),
    bars=[dict(chords=['Bbmaj7'], note='From B♭ with A a major 7th above, an octave higher than the climbing pattern: B♭–A, B–G, G–F♯, A♭–E.', items=[bb[0]]),
          dict(chords=[], note='On down: E–E♭, F–C♯, C♯–C, D–B♭.', items=[bb[1]])]))

pc = rule_dyads('Bb2', 'A3', 8, top=(-2, +4), bot=(+1, +1)); assert intervals_ok(pc)
bc = dyad_bars(pc, 'Bbmaj7', broken=True, per_bar=4)
CEX.append(dict(
    id='c-7-6-broken', title='Major 7th to minor 6th, broken',
    idea='The pair played one note at a time in eighths, low then high: the top steps down a whole step, then up a major third; the bottom climbs a half step each time. Every two moves the pair is a whole step higher.',
    quote=dict(where=f'{W1}, p. 5, Berman’s third pattern (CD 5)',
               text='Top voice down a major 2nd then up a major 3rd, bottom voice up a minor 2nd each time, broken into eighths from the open low E with E♭ above (A string, 6th fret). The opening: E, E♭.',
               item=['R', [[6, 0], [5, 6]], [.5, .5], '']),
    bars=[dict(chords=['Bbmaj7'], note='From B♭ and A: B♭, A, B, G, C, B, C♯, A. Thumb on the low notes, index or middle on the high ones.', items=[bc[0]]),
          dict(chords=[], note='D, C♯, E♭, B, E, D♯, F, C♯: a whole step higher every two pairs, all the way up if you like.', items=[bc[1]])]))

# ---- Exercise 11: five beats; the top note (root's 13th) struck on beat 1 and held, root, 5th, 7th and 11th
#      climbing under it on beats 2-5; carried through every degree of the scale. Here through Moonglow's chords,
#      each with its own scale.
FIG = [('Bbmaj7', 'B♭ major 7', ['Bb2', 'F3', 'A3', 'E4', 'G4'], 'G over B♭, F, A, E: the 13th held over root, 5th, 7th and ♯11'),
       ('Bbm6', 'B♭ minor 6', ['Bb2', 'F3', 'A3', 'Eb4', 'G4'], 'the same with E♭, the 11th of B♭ minor; A stays, as the tune holds it'),
       ('Am7', 'A minor 7', ['A2', 'E3', 'G3', 'D4', 'F4'], 'F over A, E, G, D'),
       ('Dm9', 'D minor 9', ['D3', 'A3', 'C4', 'G4', 'B4'], 'B over D, A, C, G'),
       ('G13', 'G13', ['G2', 'D3', 'F3', 'C4', 'E4'], 'E over G, D, F, C: the 11th, C, makes it G7sus4 for a moment, as in Wyble’s own'),
       ('C9', 'C9', ['C3', 'G3', 'Bb3', 'F4', 'A4'], 'A over C, G, B♭, F'),
       ('F6', 'F6', ['F2', 'C3', 'E3', 'Bb3', 'D4'], 'D over F, C, E, B♭: home')]
fig_bars, prev = [], 5
for ch, nm, notes, what in FIG:
    ms = [N(n) for n in notes]
    sh = shape(ms, near=prev)
    prev = min(f for s, f in sh if f > 0)
    steps = [([sh[4]], 1.0)] + [([sh[i]], 1.0) for i in range(4)]
    fig_bars.append(dict(chords=[ch], note=f'{nm}: {what}. Strike the top note, then the four below it one to a beat, holding everything.',
                         items=[two_lines(steps, over=ch)]))
CEX.append(dict(
    id='c-eleven', title='Five notes, the top one held',
    idea='Bars of five beats. The top note is struck on beat 1 and held; under it four notes climb one to a beat: the root, its 5th, its 7th and its 11th, with the top note the 13th. There is no 3rd anywhere, so the figure floats; Wyble carries it up every degree of the scale. Hold every note as long as the fingers allow.',
    quote=dict(where=f'{W1}, p. 14, Exercise 11 (CD 32), with Berman’s versions in harmonic and melodic minor (pp. 17–22)',
               text='In 5/4, on every degree of C major: the top note held as a whole note from beat 1, a quarter rest under it, then four quarters climbing; the first bar is C held over the open low E, B, the open D and A. Berman also plays it in 4/4 and 6/8, drops the last note for a five-note figure, and builds chords from its notes. The opening: C on the B string (1st fret), then the open low E.',
               item=two_lines([([[2, 1]], 1.0), ([[6, 0]], 1.0)])),
    bars=fig_bars))

# ---- Berman: chords from the figure's top four notes (5th, 7th, 11th, 13th), carried through the scale.
vo = []
for ch, nm, notes, what in FIG:
    ms = [N(n) for n in notes[1:]]
    vo.append((ch, ms))
vbars = []
for k in range(0, len(vo), 2):
    pair = vo[k:k + 2]
    items = []
    prevf = 5
    for ch, ms in pair:
        sh = shape(ms, near=prevf, allow_open=False)
        g = [-1] * 6
        for s, f in sh: g[6 - s] = f
        b = 2.0 if len(pair) == 2 else 4.0
        items.append(['K', ch, g, [[b, 'a']]])
    vbars.append(dict(chords=[c for c, _ in pair], note='The top four notes of the figure as one chord: ' + ', then '.join(
        c.replace('b', '♭', 1) if len(c) > 1 and c[1] == 'b' else c for c, _ in pair) + '.', items=items))
CEX.append(dict(
    id='c-voicings', title='Chords from the figure',
    idea='Berman takes the top four notes of the five (the 5th, 7th, 11th and 13th) and plays them together as a chord on every degree. No root and no 3rd: open, modern chords that still say which chord they belong to.',
    quote=dict(where=f'{W1}, p. 16, Berman’s voicings from Exercise 11 (CD 39–41)',
               text='The top four notes, numbers 2-3-4-5 of the figure, as a chord on each degree of the scale; then chords from notes 1-3-4-5, 1-2-4-5, 1-2-3-4 and 1-2-3-5.',
               item=None),
    bars=vbars))

SECTIONS.append(dict(id='concepts', title='Concepts: figures and permutations', part='Exercises', ex=CEX))


# ======================= Études =======================
# Étude 1: Moonglow's A section in two lines, each bar one of the exercises above, in order, on its own chord.
ET = []
et_bars = [
    dict(chords=['Bbmaj7'], note='Bar 1, a held note above: the bass climbs B♭ major 7, the A struck on every beat.',
         items=[T(BMAJ_UP, on_beats(['A4'] * 4), 'Bbmaj7')]),
    dict(chords=['Bbm6'], note='Bar 2: the bass falls through B♭ minor 6, the A on the off-beats (start the bass with the index).',
         items=[T(BM6_DOWN, off_beats(['A4'] * 4), 'Bbm6')]),
    dict(chords=['Am7', 'Dm9'], note='Bar 3, two against one in contrary motion: the bass climbs A to A, the top falls G, F, E, D.',
         items=[T(['A2', 'B2', 'C3', 'D3', 'E3', 'F3', 'G3', 'A3'], on_beats(['G4', 'F4', 'E4', 'D4']), 'Am7')]),
    dict(chords=['G13'], note='Bar 4, three against one: the bass climbs G to G; above it E for three eighths, F from the “and” of 2, E again on beat 4.',
         items=[T(['G2', 'A2', 'B2', 'C3', 'D3', 'E3', 'F3', 'G3'], ['E4', None, None, 'F4', None, None, 'E4', None], 'G13')]),
    dict(chords=['Gm7'], note='Bar 5, note against note, closing in: the bass climbs G to G, the top falls B♭ to B♭, a 3rd apart at the end.',
         items=[T(['G2', 'A2', 'Bb2', 'C3', 'D3', 'E3', 'F3', 'G3'], ['Bb4', 'A4', 'G4', 'F4', 'E4', 'D4', 'C4', 'Bb3'], 'Gm7')]),
    dict(chords=['C9'], note='Bar 6, the upper voice rocks: B♭ and A, a half step apart, on the beats, while the bass climbs C9 from C to C.',
         items=[T(['C3', 'D3', 'E3', 'F3', 'G3', 'A3', 'Bb3', 'C4'], on_beats(['Bb4', 'A4', 'Bb4', 'A4']), 'C9')]),
    dict(chords=['F6'], note='Bar 7, the falling line with one note an octave up: A♭, G, G♭ up an octave, F held; above, D, then E.',
         items=[T(['Ab3', 'G3', 'Gb4', 'F3'], ['D5', None, None, 'E5'], 'F6', beats=[.5, .5, .5, 2.5])]),
    dict(chords=['Gm7', 'C9'], note='Bar 8, leaps to turn round: the bass G, up to D, down to C, then a leap down to the low E, the 3rd of C9; the top falls B♭, A, G and leaps back to B♭, one to a beat.',
         items=[T(['G2', 'D3', 'C3', 'E2'], ['Bb4', 'A4', 'G4', 'Bb4'], 'C9', beats=[1.0, 1.0, 1.0, 1.0])]),
]
ET.append(dict(id='etude-moonglow', title='Étude: Moonglow’s first eight bars in two lines',
               idea='Moonglow’s A section, one exercise to a bar in the order of this page: the held note on and off the beat, two against one, three against one, note against note, the rocking voice, the chromatic line, a turn-round. Play it slowly until each bar flows into the next.',
               quote=dict(where='', text='', item=None), bars=et_bars))
SECTIONS.append(dict(id='etudes', title='Études on your songs', part='Études', ex=ET))

sys.path.insert(0, '/home/claude/studies/tango')
from quotes import trim as _trim_quotes   # quotes stay a beat or two
_trim_quotes(SECTIONS)
