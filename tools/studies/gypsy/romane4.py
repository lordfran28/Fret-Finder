"""L'Esprit Manouche, part A of chapters 14, 17, 22 and 23 (book pp. 114–186; PDF = book + 1): the half-diminished scale
on a seventh chord, the two major triads a whole step apart linked up the neck, Manouche voicings (the anatole, the II–V–I,
a static top voice over a chromatic bass), and melodies with skipping intervals (tenths, a pivot note). Added to the gypsy
arpeggios page after chapters 1–11 (romane3.py).

The same rule: their tab or diagram moved whole along the neck, every note on the same string. Their D7 goes up a fret to
E♭7 (the dominant of your bars 5–8 and 13–14, which your page has as E♭9); their anatole and II–V–I in G go up six frets
to D♭, the key of your song (your intro is its anatole, bars 15–17 its II–V–I); the static-top-voice ending in G goes down
a fret to G♭ (your bar 25); C major and A minor go up a fret.

Left out: the phrases (43–47, 49–57, 59–65: Romane's own lines), exercise 68 (voicings whose diagrams carry muting marks
and labels I can't read with certainty), the pieces and introductions (75–77), and exercise 74, a sixteen-bar étude of
theirs. check_romane4.py checks every note."""
import sys, importlib.util
sys.path.insert(0, '/home/claude/studies'); sys.path.insert(0, '/home/claude/studies/gypsy')
import romane3 as R3
W = R3.W
R1 = R3.R1
BOOK, OPENS, midi = R1.BOOK, R1.OPENS, R1.midi

THEIRS = {
    'hd48': [(5, f) for f in (5, 6, 8, 9)] + [(4, f) for f in (6, 7, 9, 10)] + [(3, f) for f in (7, 8, 10, 11)]
            + [(2, f) for f in (9, 10, 12, 13)] + [(1, f) for f in (10, 11, 13, 14)],
    's70': [(4, 10), (1, 12), (4, 9), (1, 10), (4, 7), (1, 8), (5, 10), (2, 12), (5, 8), (2, 10), (5, 7), (2, 8), (6, 10), (3, 10), (6, 8), (3, 9)],
    's71': [(1, 12), (2, 15), (1, 12), (2, 13), (1, 12), (2, 12), (1, 12), (3, 14), (1, 12), (3, 13), (1, 12), (3, 14), (1, 12), (2, 12), (1, 12), (2, 13)],
    's72': [(1, 13), (1, 12), (1, 13), (2, 15), (1, 13), (2, 13), (1, 13), (2, 12), (1, 10), (2, 13), (1, 10), (2, 12), (1, 10), (2, 10), (1, 10), (2, 9)],
    's73': [(1, 12), (2, 15), (1, 12), (2, 13), (1, 12), (2, 12), (1, 12), (2, 10), (1, 12), (2, 9), (1, 10), (2, 6), (1, 7), (2, 5), (1, 8), (3, 7), (1, 7)],
}
TRIADS = {   # (name, frets on the three strings, low to high)
    't58a': [('D', (2, 3, 2)), ('C', (5, 5, 3)), ('D', (7, 7, 5)), ('C', (9, 8, 8)), ('D', (11, 10, 10)), ('C', (12, 13, 12)), ('D', (14, 15, 14))],
    't58b': [('C', (2, 0, 1)), ('D', (4, 2, 3)), ('C', (5, 5, 5)), ('D', (7, 7, 7)), ('C', (10, 9, 8)), ('D', (12, 11, 10))],
}
TSTR = {'t58a': (3, 2, 1), 't58b': (4, 3, 2)}
VOICINGS = {
    'v66': [('G6/9', [3, 5, 5, 4, 5, 5]), ('Eb9/Bb', [6, 6, 5, 6, 6, 6]), ('Ab6/9', [4, 6, 6, 5, 6, 6]), ('D9/A', [5, 5, 4, 5, 5, 5]), ('G6/9', [3, 5, 5, 4, 5, 5])],
    'v67': [('Am9', [5, 7, 7, 5, 8, 7]), ('Ab9', [4, 6, 6, 5, 7, 6]), ('G6/9', [3, 5, 5, 4, 5, 5])],
    'v69': [('C#m7b5', [9, -1, 9, 9, 8, -1]), ('F9/C', [8, -1, 7, 8, 8, -1]), ('G/B', [7, -1, 5, 7, 8, -1]), ('Bb13', [6, -1, 6, 7, 8, -1]),
            ('A7', [5, 7, 5, 6, 8, -1]), ('Abmaj7', [4, 6, 6, 5, 8, -1]), ('Gmaj7', [3, 5, 5, 4, 7, 7])],
}
SHIFT = {'hd48': 1, 't58a': 1, 't58b': 1, 'v66': 6, 'v67': 6, 'v69': -1, 's70': 1, 's71': 1, 's72': 1, 's73': 1}
OUR_V = {'v66': ['Db6/9', 'A9/E', 'D6/9', 'Ab9/Eb', 'Db6/9'], 'v67': ['Ebm9', 'D9', 'Db6/9'],
         'v69': ['Cm7b5', 'E9/B', 'Gb/Bb', 'A13', 'Ab7', 'Gmaj7', 'Gbmaj7']}
OUR_T = {'C': 'Db', 'D': 'Eb'}
SP = {
    'hd': {3: 'E♭', 4: 'E', 6: 'F♯', 7: 'G', 9: 'A', 10: 'B♭', 0: 'C', 1: 'D♭'},
    'db': {1: 'D♭', 3: 'E♭', 5: 'F', 6: 'G♭', 8: 'A♭', 10: 'B♭', 0: 'C'},
    'bbm': {10: 'B♭', 0: 'C', 1: 'D♭', 3: 'E♭', 5: 'F', 6: 'G♭', 9: 'A'},
    'tri': {1: 'D♭', 5: 'F', 8: 'A♭', 3: 'E♭', 7: 'G', 10: 'B♭'},
}
SHARPS = {0: 'C', 1: 'C♯', 2: 'D', 3: 'E♭', 4: 'E', 5: 'F', 6: 'F♯', 7: 'G', 8: 'G♯', 9: 'A', 10: 'B♭', 11: 'B'}


def ours(key): return [(s, f + SHIFT[key]) for s, f in THEIRS[key]]
def nms(seq, sp): return [SP[sp][midi(s, f) % 12] for s, f in seq]
def lab(nm, what, marks=None): return '=' + ','.join(n + (marks[i] if marks else '') for i, n in enumerate(nm)) + '|' + what
def grip(strs, frets): g = [-1] * 6; [g.__setitem__(6 - s, f) for s, f in zip(strs, frets)]; return g


def quote(key, n, text, p, durs=None):
    ns = THEIRS[key][:n]
    return R1.T(text, p, ns, durs=durs, names=[SHARPS[midi(s, f) % 12] for s, f in ns])


def chord_quote(text, p, name, g):
    return dict(where=f'{BOOK}, p. {p}', text=text, whose='The original', played='Played here: that chord.', items=[['C', name, g, 2.0, {'roll': 0.03}]])


def run_bars(notes, durs, names, chords_of, what, lead_rest=0.0, marks=None):
    out, cur, t, first = [], [], lead_rest, True
    for i, d in enumerate(durs):
        cur.append(i); t += d
        if t >= 4 - 1e-9 or i == len(durs) - 1:
            its = ([['W', lead_rest]] if first and lead_rest else []) + [['R', [list(notes[j]) for j in cur], [durs[j] for j in cur],
                                                                         lab([names[j] for j in cur], what, [marks[j] for j in cur] if marks else None)]]
            if t < 4 - 1e-9: its.append(['W', 4 - t])
            out.append(dict(chords=chords_of(len(out)), note='', items=its)); cur, t, first = [], 0.0, False
    return out


EX = []
# ---------------------------------------------------------------- chapter 14: the half-diminished scale
hd = ours('hd48')
b = run_bars(hd, [0.5] * 20, nms(hd, 'hd'), lambda k: ['Eb7'], 'the half-diminished scale', marks=['↓', '↑'] * 10)
b[0]['note'] = ('E♭ E F♯ G A B♭ C D♭: half step, whole step, half step, whole step, from the E♭ at the 6th fret of the A string; four notes on each string '
                '(frets n, n+1, n+3, n+4), each string a fret higher than the last and two frets from the G to the B string, up to the F♯ at the 15th fret. '
                'Eighths, the pick down and up in turn.')
EX.append(dict(id='hd48', title='The half-diminished scale on E♭7',
               idea=('The diminished scale that starts with a half step, for a seventh chord: it holds the chord’s root, 3rd, 5th and 7th with the ♭9, ♯9, ♯11 and 13. '
                     'Theirs is on D7; ours a fret higher on E♭7, the dominant of your bars 5–8 and 13–14 (your page has E♭9 there: this scale gives it a ♭9 and ♯9 instead of the 9th).'),
               quote=quote('hd48', 4, 'theirs is on D7 from the 5th fret of the A string: D, D♯, F, F♯.', 114),
               bars=b))

# ---------------------------------------------------------------- chapter 17: two triads a whole step apart
for key, title, where in (('t58a', 'the top three strings', 'G, B and high E'), ('t58b', 'the middle strings', 'D, G and B')):
    strs = TSTR[key]
    tri = [(OUR_T[n], tuple(f + SHIFT[key] for f in fr)) for n, fr in TRIADS[key]]
    path = tri + tri[-2::-1]
    bars = []
    # as chords, a beat each, up the neck and back
    items, t = [], 0
    for n, fr in path:
        items.append(['C', n, grip(strs, fr), 1.0, {'roll': 0.015}]); t += 1
        if t == 4: bars.append(dict(chords=['Eb7'], note='', items=items)); items, t = [], 0
    if items: items.append(['W', 4 - t]); bars.append(dict(chords=['Eb7'], note='', items=items))
    # as arpeggios: going up the neck each triad low to high, coming down high to low
    notes, names = [], []
    for k, (n, fr) in enumerate(path):
        tri_notes = list(zip(strs, fr))
        if k >= len(tri): tri_notes = tri_notes[::-1]
        notes += tri_notes; names += nms(tri_notes, 'tri')
    bars += run_bars(notes, [1 / 3] * len(notes), names, lambda k: ['Eb7'], 'the triads in turn')
    bars[0]['note'] = (f'D♭ and E♭ major on the {where} strings, every inversion, in turn up the neck and back: first as chords, a beat each, then as arpeggios in triplets, '
                       'each triad from its lowest note going up the neck and from its highest coming down.')
    EX.append(dict(id=key, title=f'D♭ and E♭ triads linked: {title}',
                   idea=('Two major triads a whole step apart, over the seventh chord on the higher one’s root: D♭ over E♭7 gives its 7th, 9th and 11th; E♭ its root, 3rd and 5th. '
                         'Seeing both on the neck at once is the base of their two-key phrases. Theirs are C and D over D7; ours a fret higher, D♭ and E♭ over E♭7.'
                         if key == 't58a' else 'The same two triads on the next three strings down.'),
                   quote=dict(where=f'{BOOK}, p. 138', text=f'their first triad, {TRIADS[key][0][0]} major.', whose='The original', played='Played here: that triad.',
                              items=[['C', TRIADS[key][0][0], grip(strs, TRIADS[key][0][1]), 2.0, {'roll': 0.02}]]),
                   bars=bars))


# ---------------------------------------------------------------- chapter 22: Manouche voicings
def vgrips(key):
    return {n: [f + SHIFT[key] if f >= 0 else -1 for f in g] for n, (tn, g) in zip(OUR_V[key], VOICINGS[key])}


GR = {k: vgrips(k) for k in ('v66', 'v67', 'v69')}
seq66 = ['Db6/9', 'A9/E', 'D6/9', 'Ab9/Eb'] * 2 + ['Db6/9']
b = [dict(chords=[n], note='', items=W.pompe([n], GR['v66'])) for n in seq66]
b[0]['note'] = ('D♭6/9 (thumb on the low E string at the 9th fret), A9 with E in the bass (12th fret), D6/9 (thumb at the 10th), A♭9 with E♭ in the bass (11th), a bar each in la pompe, '
                'twice, and D♭6/9. The thumb takes the low E string in the 6/9 chords: the gypsy way, not the classical one.')
EX.append(dict(id='v66', title='The Manouche anatole in D♭',
               idea=('The turnaround as gypsy rhythm players play it, the hand barely moving: I 6/9, then a ninth chord a half step below VI, a 6/9 a half step below II, '
                     'a ninth chord on V with its 5th in the bass. Theirs is in G (for G, E7, Am, D7); ours six frets higher in D♭, for your intro’s D♭maj9, B♭m7, E♭m9, A♭7.'),
               quote=chord_quote('their first chord, G6/9, the thumb on the low E string at the 3rd fret.', 177, 'G6/9', VOICINGS['v66'][0][1]),
               bars=b))
b = [dict(chords=[n], note='', items=W.pompe([n], GR['v67'])) for n in ['Ebm9', 'D9', 'Db6/9', 'Db6/9'] * 2]
b[0]['note'] = ('E♭m9 (thumb on the low E string at the 11th fret), D9 (10th fret), D♭6/9 (9th fret), '
                'a bar each and two of D♭, in la pompe, twice: the hand slides down a fret at a time. D9 stands in for A♭7, a tritone away.')
EX.append(dict(id='v67', title='The Manouche II–V–I in D♭',
               idea=('The II–V–I with the V replaced by the ninth chord a half step above I, so the hand slides down a fret at a time, the thumb on the bass. '
                     'Theirs is in G (Am9, A♭9, G6/9); ours six frets higher in D♭: E♭m9, D9, D♭6/9, for your bars 15–17 (E♭m9, A♭7, D♭maj7).'),
               quote=chord_quote('their first chord, Am9, the thumb on the low E string at the 5th fret.', 177, 'Am9', VOICINGS['v67'][0][1]),
               bars=b))
b = [dict(chords=[n], note='', items=W.pompe([n], GR['v69'])) for n in OUR_V['v69']]
b[0]['note'] = ('Cm7♭5, E9 with B in the bass, G♭ with B♭ in the bass, A13, A♭7, Gmaj7, G♭maj7, a bar each in la pompe. The top note, G♭ on the B string at the 7th fret, '
                'stays put while the bass falls a half step at a time from C to G♭; on the last chord it moves at last, to F with B♭ above.')
EX.append(dict(id='v69', title='A static top voice over a falling bass: an ending in G♭',
               idea=('Voices moving against each other: one note held on top while the bass walks down by half steps, each chord named for what the bass makes of the top note. '
                     'It makes an ending. Theirs ends on G major; ours a fret lower ends on G♭maj7, as your bar 25 does.'),
               quote=chord_quote('their first chord, C♯m7♭5, from the 9th fret of the low E string.', 178, 'C#m7b5', VOICINGS['v69'][0][1]),
               bars=b))

# ---------------------------------------------------------------- chapter 23: skipping intervals
n70 = ours('s70')
nm70 = nms(n70, 'db')
b = [dict(chords=['Db'], note='', items=[['R', n70[:8], [0.5] * 8, lab(nm70[:8], 'tenths, falling')]]),
     dict(chords=['Db'], note='', items=[['R', n70[8:], [0.5] * 7 + [2.5], lab(nm70[8:], 'tenths, falling')], ['W', 2]])]
b[0]['note'] = ('D♭ major falling in tenths, the low note then the high: D♭ (11th fret of the D string) and F (13th of the high E string), C and E♭, B♭ and D♭ … down to D♭ and F, '
                'the last held over the bar line. The low notes on the D, A and low E strings, the high ones on the high E, B and G strings.')
EX.append(dict(id='s70', title='D♭ major in tenths',
               idea=('Their “skipping intervals”: a melody that jumps between two lines, here the scale in tenths, played with the pick or the fingers as you like. '
                     'Theirs is C major; ours a fret higher is D♭ major, your key.'),
               quote=quote('s70', 2, 'theirs starts with C at the 10th fret of the D string and E at the 12th of the high E string.', 185),
               bars=b))
n71 = ours('s71')
nm71 = nms(n71, 'bbm')
b = [dict(chords=['Bbm'], note='', items=[['W', 0.5], ['R', n71[:7], [0.5] * 7, lab(nm71[:7], 'round F')]]),
     dict(chords=['Bbm'], note='', items=[['R', n71[7:15], [0.5] * 8, lab(nm71[7:15], 'round F')]]),
     dict(chords=['Bbm'], note='', items=[['R', n71[15:], [2], lab(nm71[15:], 'home')], ['W', 2]])]
b[0]['note'] = ('After an eighth’s rest, F at the 13th fret of the high E string every other note, while the line under it goes down B♭ minor and back: '
                'E♭ D♭ C (B string), B♭ A B♭ (G string), C, and onto D♭.')
EX.append(dict(id='s71', title='Round one note: F in B♭ minor',
               idea='A line that turns around one fixed note, every other note the same. Theirs circles E in A harmonic minor; ours a fret higher circles F in B♭ harmonic minor.',
               quote=quote('s71', 3, 'theirs circles E at the 12th fret of the high E string: E, D, E.', 185),
               bars=b))
n72 = ours('s72')
b = [dict(chords=['Ebm'], note='', items=[['W', 0.5], ['R', n72[:7], [0.5] * 7, lab(nms(n72[:7], 'bbm'), 'round G♭, then E♭')]]),
     dict(chords=['Ebm'], note='', items=[['R', n72[7:15], [0.5] * 8, lab(nms(n72[7:15], 'bbm'), 'round E♭')]]),
     dict(chords=['F7'], note='', items=[['R', n72[15:], [2], lab(nms(n72[15:], 'bbm'), 'home to the V')], ['W', 2]])]
b[0]['note'] = ('Over E♭ minor: G♭ at the 14th fret of the high E string every other note, the line under it F, E♭, D♭; then E♭ at the 11th fret every other note '
                'over C, D♭, C, B♭; then A, the 3rd of F7, held.')
EX.append(dict(id='s72', title='Round G♭, then E♭: E♭ minor to F7',
               idea=('The turning note changes halfway, and the harmony moves: minor iv to V7. Theirs is D minor to E7 in A minor; '
                     'ours a fret higher is E♭ minor to F7 in B♭ minor (your page has F7 in bars 10–12).'),
               quote=quote('s72', 3, 'theirs circles F at the 13th fret of the high E string: F, E, F.', 186),
               bars=b))
n73 = ours('s73')
end_chord = [-1, -1, -1, 6, 6, 6]
b = [dict(chords=['Bbm'], note='', items=[['W', 0.5], ['R', n73[:7], [0.5] * 7, lab(nms(n73[:7], 'bbm'), 'round F')]]),
     dict(chords=['F7'], note='', items=[['R', n73[7:15], [0.5] * 8, lab(nms(n73[7:15], 'bbm'), 'two lines falling')]]),
     dict(chords=['Bbm'], note='', items=[['R', n73[15:], [0.5, 0.5], lab(nms(n73[15:], 'bbm'), 'home')], ['C', 'Bbm', end_chord, 1.0, {'roll': 0.02}], ['W', 2]])]
b[0]['note'] = ('All three together: F turned around over E♭, D♭, C (as round F); then over F7 two lines falling apart and together: B♭ under F, A under E♭, G♭ under C, F under D♭; '
                'then E♭ and C, and B♭ minor on the top three strings at the 6th fret.')
EX.append(dict(id='s73', title='Skipping intervals together: B♭ minor, F7, B♭ minor',
               idea='Their summary of the three: the turning note, then two lines in wide intervals, and home. Theirs is in A minor; ours a fret higher in B♭ minor.',
               quote=quote('s73', 3, 'theirs circles E at the 12th fret of the high E string: E, D, E.', 186),
               bars=b))

BY = {e['id']: e for e in EX}
SECTIONS = list(R3.SECTIONS) + [dict(id=sid, title=t, part='Exercises', ex=[BY[k] for k in ks]) for sid, t, ks in (
    ('rom-17', 'The half-diminished scale', ('hd48',)),
    ('rom-18', 'Two triads a whole step apart', ('t58a', 't58b')),
    ('rom-19', 'Manouche voicings', ('v66', 'v67', 'v69')),
    ('rom-20', 'Skipping intervals', ('s70', 's71', 's72', 's73')))]
assert sum(len(S['ex']) for S in SECTIONS[len(R3.SECTIONS):]) == len(EX)
