"""Octaves, Wes Montgomery's way (The Wes Montgomery Guitar Folio, transcribed by Steve Khan: no exercises in the
book, so these are ours, on Moonglow's chords, with a quote of the first beat of Wes's first octave chorus)."""
import sys
sys.path.insert(0, '/home/claude/studies')
from kit_study import N, two_lines, nn, OPEN

FOLIO = 'The Wes Montgomery Guitar Folio'


def octave(lower_s, lower_f):
    """an octave from a lower note: strings 6–4 and 5–3 two frets up, 4–2 and 3–1 three frets up (one string muted between)"""
    up = lower_f + (2 if lower_s >= 5 else 3)
    return [[lower_s, lower_f], [lower_s - 2, up]]


def oct_of(name, s):
    m = N(name); f = m - OPEN[6 - s]; assert 0 <= f <= 15, (name, s)
    g = octave(s, f)
    assert OPEN[6 - g[1][0]] + g[1][1] == m + 12
    return g


RH = 'Thumb down-strokes on both notes at once; the index frets the low note, the ring finger or little finger the high one, and the flat of the index rests on the string between to keep it quiet.'
EX = []
EX.append(dict(
    id='oct-shapes', title='The four octave shapes',
    idea='An octave with one string skipped between the two notes. On the low pairs (6th and 4th, 5th and 3rd strings) the high note is two frets above the low one; on the high pairs (4th and 2nd, 3rd and 1st) three frets, because of the B string. ' + RH,
    quote=dict(where=f'{FOLIO}, p. 10, West Coast Blues, the fifth chorus of Wes’s solo, where his octaves start',
               text='He opens the chorus with a single octave B♭ on the beat and rests, then answers with octaves off the beat. The folio gives no strings; it is shown here on the G and high E strings.',
               item=two_lines([([[3, 3], [1, 6]], 1.0)]), whose='Wes’s own', played='Played here: that first octave.'),
    bars=[dict(chords=['Bbmaj7'], note='B♭ four ways, one to a beat: low E and D strings (6th fret), A and G strings (1st fret), then an octave up on the D and B strings (8th fret) and the G and high E strings (3rd fret).',
               items=[two_lines([(oct_of('Bb2', 6), 1.0), (oct_of('Bb2', 5), 1.0), (oct_of('Bb3', 4), 1.0), (oct_of('Bb3', 3), 1.0)])]),
          dict(chords=['Bbm6'], note='A, the note Moonglow holds over B♭ minor 6, the same four ways: 5th fret, open A string, 7th fret, 2nd fret.',
               items=[two_lines([(oct_of('A2', 6), 1.0), (oct_of('A2', 5), 1.0), (oct_of('A3', 4), 1.0), (oct_of('A3', 3), 1.0)])])]))

scale = [('Bb2', 6), ('C3', 6), ('D3', 5), ('E3', 5), ('F3', 5), ('G3', 5), ('A3', 4), ('Bb3', 4)]
EX.append(dict(
    id='oct-scale', title='A scale in octaves',
    idea='Up the scale of B♭ major 7 (with Moonglow’s E natural) in octaves, one to a beat, moving from one pair of strings to the next as the notes climb. Keep the hand shape fixed and move the whole hand. ' + RH,
    quote=dict(where='', text='', item=None),
    bars=[dict(chords=['Bbmaj7'], note='B♭, C on the low E and D strings (6th and 8th fret), D, E on the A and G strings (5th and 7th fret).',
               items=[two_lines([(oct_of(n, s), 1.0) for n, s in scale[:4]])]),
          dict(chords=['Bbmaj7'], note='F, G on the A and G strings (8th and 10th fret), then A, B♭ on the D and B strings (7th and 8th fret), three frets apart now.',
               items=[two_lines([(oct_of(n, s), 1.0) for n, s in scale[4:]])])]))

EX.append(dict(
    id='oct-line', title='Moonglow’s line in octaves',
    idea='Octaves sliding one fret at a time on one pair of strings: the falling line under Moonglow’s first chords (D, D♭, C, B), two beats each. Slide, don’t lift: the octave shape stays locked. ' + RH,
    quote=dict(where='', text='', item=None),
    bars=[dict(chords=['Bbmaj7', 'Bbm6'], note='D, then D♭, on the A and G strings (5th and 4th fret): the 3rd of B♭ major 7 falling to the minor 3rd of B♭ minor 6.',
               items=[two_lines([(oct_of('D3', 5), 2.0), (oct_of('Db3', 5), 2.0)])]),
          dict(chords=['Am7', 'G13'], note='C, then B (3rd and 2nd fret): the 3rd of A minor 7, then the 3rd of G13.',
               items=[two_lines([(oct_of('C3', 5), 2.0), (oct_of('B2', 5), 2.0)])])]))

SECTIONS = [dict(id='octaves', title='Octaves', part='Exercises', ex=EX)]
