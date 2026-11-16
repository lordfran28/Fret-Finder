"""L'Esprit Manouche, part A of chapters 10 and 11 (book pp. 81–91; PDF = book + 1): designated notes (a chord's root or
5th approached from the scale step above and the half step below), II–V–I voicings in la pompe, designated notes with the
V arpeggio in a minor key, and the major scale broken in pairs and in fours. Added to the gypsy arpeggios page after
chapters 1–9 (romane2.py).

The same rule as before: their tab moved whole along the neck, every note on the same string. G major goes down a fret to
G♭ (your bars 24–25: A♭m7, D♭7, G♭maj7), A minor up a fret to B♭ minor, C major up a fret to D♭, C minor down two frets
to B♭ minor (your F7♭9 to B♭m7, bars 10–11), and B♭ major down four frets to G♭ (up three would climb to the 18th fret).
check_romane3.py checks every note."""
import sys, importlib.util
sys.path.insert(0, '/home/claude/studies'); sys.path.insert(0, '/home/claude/studies/gypsy')
import romane2 as R2
_spec = importlib.util.spec_from_file_location('gypsy_entry', '/home/claude/studies/gypsy/entry.py')
W = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(W)

R1 = R2.R1
BOOK, OPENS, midi = R1.BOOK, R1.OPENS, R1.midi

# their tabs, as read from the book: (string, fret) in playing order; 1 = the high E string
THEIRS = {
    'd31': [(2, 5), (2, 3), (2, 2), (2, 3), (1, 5), (1, 3), (1, 2), (1, 3)],
    'd32': [(2, 10), (2, 8), (2, 7), (2, 8), (1, 12), (1, 10), (1, 9), (1, 10)],
    'd33': [(2, 6), (2, 5), (2, 4), (2, 5), (1, 7), (1, 5), (1, 4), (1, 5)],
    'd34': [(2, 12), (2, 10), (2, 9), (2, 10), (1, 13), (1, 12), (1, 11), (1, 12)],
    'd37': [(s, f) for s, t in ((1, 13), (2, 11), (3, 10), (4, 8), (5, 8), (6, 6)) for f in (t, t - 1, t + 2, t)],
    'd38': [(s, f) for s, t in ((6, 6), (5, 8), (4, 8), (3, 10), (2, 11), (1, 13)) for f in (t, t + 2, t - 1, t)],
    'd39': [(2, 4), (2, 3), (2, 6), (2, 4), (4, 5), (3, 4), (2, 3), (3, 5)],
    'd40': [(2, 8), (2, 7), (2, 9), (2, 8), (4, 9), (3, 7), (2, 6), (3, 8)],
    'b41': [(5, 3), (5, 2), (5, 5), (5, 3), (4, 2), (5, 5), (4, 3), (4, 2), (4, 5), (4, 3), (4, 7), (4, 5), (3, 4), (4, 7), (3, 5), (3, 4),
            (3, 7), (3, 5), (2, 5), (3, 7), (2, 6), (2, 5), (2, 8), (2, 6), (1, 5), (2, 8), (1, 7), (1, 5), (1, 8), (1, 7), (1, 10), (1, 8)],
}
G42 = [(6, 7), (6, 8), (6, 10), (5, 7), (5, 9), (5, 10), (4, 7), (4, 9), (4, 10), (3, 7), (3, 9), (2, 7), (2, 8), (2, 10), (1, 7), (1, 8), (1, 10)]
THEIRS['b42'] = [G42[i + j] for i in range(14) for j in range(4)]
VOICINGS = {   # their grips, low E string first
    'v35': [('Am11', [5, -1, 5, 5, 3, -1]), ('Adim7', [5, -1, 4, 5, 4, -1]), ('G6', [3, -1, 5, 4, 5, -1])],
    'v36': [('Am9', [-1, 12, 10, 12, 12, -1]), ('D7#5', [10, -1, 10, 11, 11, -1]), ('Gmaj9', [-1, 10, 9, 11, 10, -1])],
}
SHIFT = {'d31': -1, 'd32': -1, 'd33': 1, 'd34': 1, 'v35': -1, 'v36': -1, 'd37': -4, 'd38': -4, 'd39': -2, 'd40': -2, 'b41': 1, 'b42': -1}
OUR_V = {'v35': ['Abm11', 'Abdim7', 'Gb6'], 'v36': ['Abm9', 'Db7#5', 'Gbmaj9']}
SP = {
    'gb': {6: 'G♭', 8: 'A♭', 10: 'B♭', 11: 'C♭', 1: 'D♭', 3: 'E♭', 5: 'F', 0: 'C'},
    'bbm': {10: 'B♭', 0: 'C', 1: 'D♭', 3: 'E♭', 5: 'F', 6: 'G♭', 9: 'A', 4: 'E'},
    'db': {1: 'D♭', 3: 'E♭', 5: 'F', 6: 'G♭', 8: 'A♭', 10: 'B♭', 0: 'C'},
}
EXSP = {'d31': 'gb', 'd32': 'gb', 'd33': 'bbm', 'd34': 'bbm', 'd37': 'gb', 'd38': 'gb', 'd39': 'bbm', 'd40': 'bbm', 'b41': 'db', 'b42': 'gb'}
SHARPS = {0: 'C', 1: 'C♯', 2: 'D', 3: 'E♭', 4: 'E', 5: 'F', 6: 'F♯', 7: 'G', 8: 'G♯', 9: 'A', 10: 'B♭', 11: 'B'}


def ours(key): return [(s, f + SHIFT[key]) for s, f in THEIRS[key]]
def names(key): return [SP[EXSP[key]][midi(s, f) % 12] for s, f in ours(key)]
def lab(nm, marks, what): return '=' + ','.join(n + m for n, m in zip(nm, marks)) + '|' + what


def quote(key, n, text, p, durs=None):
    ns = THEIRS[key][:n]
    return R1.T(text, p, ns, durs=durs, names=[SHARPS[midi(s, f) % 12] for s, f in ns])


EX = []
STAR = ['', '*'] * 4
# ---------------------------------------------------------------- chapter 10: designated notes, major and minor


def cell_bars(key, chord, what):
    ns, nm = ours(key), names(key)
    return [dict(chords=[chord], note='', items=[['R', [list(x) for x in ns], [0.5] * 8, lab(nm, STAR, what)]]),
            dict(chords=[chord], note='', items=[['R', [list(ns[-1])], [2], lab(nm[-1:], ['*'], 'held')], ['W', 2]])]


b = cell_bars('d31', 'Gb', 'D♭ then G♭, each from above and below')
b[0]['note'] = ('On the B string the step above the 5th, the 5th, the half step below it, the 5th again: E♭ D♭ C D♭ (4th, 2nd, 1st, 2nd frets, little, middle, index, middle); '
                'then the same on the high E string for the root: A♭ G♭ F G♭, held over the bar line. * the chord’s notes.')
EX.append(dict(id='d31', title='Designated notes: G♭, the 5th then the root',
               idea=('Their “designated notes”: a cell that circles a chord note, the scale step above, the note, the half step below, the note again, '
                     'so the line always lands on the chord. In a major key, on the 5th and the root. Theirs is in G; ours a fret lower in G♭, your G♭maj7 of bar 25.'),
               quote=quote('d31', 4, 'theirs is in G at the 2nd fret of the B string: E, D, C♯, D.', 81),
               bars=b))
b = cell_bars('d32', 'Gb', 'G♭ then D♭, each from above and below')
b[0]['note'] = ('The cell the other way round, root first and 5th after, higher up: A♭ G♭ F G♭ on the B string (9th, 7th, 6th, 7th frets), '
                'then E♭ D♭ C D♭ on the high E string two frets higher (11th, 9th, 8th, 9th). This follows their tab; their diagram shows the same cell at the 2nd fret, '
                'with the D♭ an octave lower.')
EX.append(dict(id='d32', title='Designated notes: G♭, the root then the 5th',
               idea='The inversion: the same cell with the root first, on the opposite strings.',
               quote=quote('d32', 4, 'theirs, at the 7th fret of the B string: A, G, F♯, G.', 81),
               bars=b))
b = cell_bars('d33', 'Bbm', 'F then B♭, each from above and below')
b[0]['note'] = ('In minor: G♭ F E F on the B string (7th, 6th, 5th, 6th frets): the 5th is approached by half steps from both sides; '
                'then C B♭ A B♭ on the high E string for the root (8th, 6th, 5th, 6th), the A being the leading note. Held over the bar line.')
EX.append(dict(id='d33', title='Designated notes: B♭ minor, the 5th then the root',
               idea=('The same cell in a minor key. To sound minor, the 5th is reached from a half step on either side; the root, as in major, from its half step below. '
                     'Theirs is in A minor; ours a fret higher in B♭ minor, your B♭m7.'),
               quote=quote('d33', 4, 'theirs is in A minor at the 4th fret of the B string: F, E, D♯, E.', 82),
               bars=b))
b = cell_bars('d34', 'Bbm', 'B♭ then F, each from above and below')
b[0]['note'] = 'The other way round, higher: C B♭ A B♭ on the B string (13th, 11th, 10th, 11th frets), then G♭ F E F on the high E string (14th, 13th, 12th, 13th).'
EX.append(dict(id='d34', title='Designated notes: B♭ minor, the root then the 5th',
               idea='The minor cell with the root first, up the neck.',
               quote=quote('d34', 4, 'theirs, at the 9th fret of the B string: B, A, G♯, A.', 82),
               bars=b))


def voicing_bars(key):
    nm = OUR_V[key]
    gr = {n: [f + SHIFT[key] if f >= 0 else -1 for f in g] for n, (tn, g) in zip(nm, VOICINGS[key])}
    out = []
    for _ in range(2):
        for n in (nm[0], nm[1], nm[2], nm[2]):
            out.append(dict(chords=[n], note='', items=W.pompe([n], gr)))
    return out, gr


b, GR35 = voicing_bars('v35')
b[0]['note'] = ('A♭m7 with its 11th (root at the 4th fret of the low E string), A♭°7 (D♭7♭9 without its root), G♭6 (root at the 2nd fret), '
                'a bar each and two of G♭, in la pompe, twice. The top note climbs a half step at a time: D♭, D, E♭. '
                '(Their text says the top note falls; their diagrams climb, and this follows the diagrams.)')
EX.append(dict(id='v35', title='II–V–I voicings in G♭ (1)',
               idea=('Voicings for the II–V–I, each chord coloured, the top note moving by half steps so the chords sing. Play them in la pompe with a metronome until each sounds right. '
                     'Theirs is in G (Am7, D7, G); ours a fret lower in G♭: A♭m7, D♭7, G♭, your bars 24–25.'),
               quote=dict(where=f'{BOOK}, p. 83', text='their first chord, A minor 7 with the 11th: A, G, C, D from the 5th fret.', whose='The original',
                          played='Played here: that chord.', items=[['C', 'Am11', VOICINGS['v35'][0][1], 2.0, {'roll': 0.03}]]),
               bars=b))
b, GR36 = voicing_bars('v36')
b[0]['note'] = ('A♭m9 (root on the A string at the 11th fret), D♭7♯5 (root on the low E string at the 9th fret), G♭maj9 (root on the A string at the 9th fret), '
                'in la pompe, twice. Now the top note falls: B♭ (the 9th), A (the ♯5), A♭ (the 9th).')
EX.append(dict(id='v36', title='II–V–I voicings in G♭ (2)',
               idea='Another set, higher up, with the 9th on the II and I chords and the raised 5th on the V.',
               quote=dict(where=f'{BOOK}, p. 83', text='their first chord, A minor 9: A, C, G, B from the 12th fret of the A string.', whose='The original',
                          played='Played here: that chord.', items=[['C', 'Am9', VOICINGS['v36'][0][1], 2.0, {'roll': 0.03}]]),
               bars=b))

# ---------------------------------------------------------------- chapter 11


def cells24(key, chord, fingers, what):
    ns, nm = ours(key), names(key)
    out = []
    for k in range(6):
        out.append(dict(chords=[chord], note='', items=[['R', [list(x) for x in ns[4 * k:4 * k + 4]], [0.5] * 4,
                                                          lab(nm[4 * k:4 * k + 4], ['', '', '', '*'], what)]]))
    return out


b = cells24('d37', 'Gb', 'iiam', 'down the strings')
b[0]['note'] = ('Two beats to a bar. On each string from the top, the chord note (D♭ or G♭), the half step below, the step above, the note again: '
                'D♭ C E♭ D♭ on the high E string at the 9th fret, G♭ F A♭ G♭ on the B string, and so down to the low E string at the 2nd fret. '
                'Fingers index, index, little, middle: the index plays the note, then slides back a fret for the half step below, and the hand stays there.')
EX.append(dict(id='d37', title='Designated notes down the strings: G♭',
               idea=('The cell on every string in turn, the root and the 5th of the chord alternating, the index finger leading the hand along. '
                     'Theirs is on B♭; ours four frets lower on G♭ (three higher would reach the 18th fret).'),
               quote=quote('d37', 4, 'theirs is on B♭ from the 13th fret of the high E string: F, E, G, F.', 89),
               bars=b))
b = cells24('d38', 'Gb', 'maii', 'up the strings')
b[0]['note'] = ('Up from the low E string: the chord note, the step above, the half step below, the note: G♭ A♭ F G♭ at the 2nd fret, D♭ E♭ C D♭ on the A string, '
                'and so up to the high E string at the 9th fret. Fingers middle, little, index, index.')
EX.append(dict(id='d38', title='Designated notes up the strings: G♭',
               idea='The cell going up the strings, its middle two notes the other way round.',
               quote=quote('d38', 4, 'theirs, from the 6th fret of the low E string: B♭, C, A, B♭.', 89),
               bars=b))


def minor_v(key, what):
    ns, nm = ours(key), names(key)
    marks = ['', '', '', '*', '', '', '', '*']
    return [dict(chords=['Bbm'], note='', items=[['W', 0.5], ['R', [list(x) for x in ns[:7]], [0.5] * 7, lab(nm[:7], marks[:7], what)]]),
            dict(chords=['Bbm'], note='', items=[['R', [list(ns[7])], [2], lab(nm[7:], ['*'], 'home')], ['W', 2]])]


b = minor_v('d39', 'the chord, then the V arpeggio home')
b[0]['note'] = ('After an eighth’s rest: D♭ C E♭ D♭ (the minor 3rd circled on the B string at the 1st–4th frets), then F, A, C, the arpeggio of F, the V chord, '
                'which falls onto B♭, the root, at the 3rd fret of the G string.')
EX.append(dict(id='d39', title='B♭ minor: the 3rd, then the V arpeggio home',
               idea=('In minor the designated notes are reached through the V chord: the 3rd circled, then the V arpeggio resolving onto the root, tension then rest. '
                     'Theirs is in C minor with G; ours two frets lower in B♭ minor with F, your F7♭9 going to B♭m7 in bars 10–11.'),
               quote=quote('d39', 4, 'theirs is in C minor at the 3rd fret of the B string: E♭, D, F, E♭.', 90),
               bars=b))
b = minor_v('d40', 'the 5th, then the diminished arpeggio home')
b[0]['note'] = ('F E G♭ F (the 5th circled on the B string at the 5th–7th frets), then A, C, E♭, the diminished arpeggio on A (F7 without its root), '
                'which falls onto D♭, the minor 3rd, at the 6th fret of the G string.')
EX.append(dict(id='d40', title='B♭ minor: the 5th, then the diminished arpeggio home',
               idea='The same with the 5th circled, and the V chord replaced by the diminished arpeggio on its 3rd, which lands on the minor 3rd.',
               quote=quote('d40', 4, 'theirs, at the 7th fret of the B string: G, F♯, A♭, G.', 90),
               bars=b))

ns, nm = ours('b41'), names('b41')
b = [dict(chords=['Db'], note='', items=[['R', [list(x) for x in ns[8 * k:8 * k + 8]], [0.5] * 8, lab(nm[8 * k:8 * k + 8], [''] * 8, 'the scale in pairs')]]) for k in range(4)]
b[0]['note'] = ('D♭ major from the D♭ at the 4th fret of the A string, each note followed by the one below: D♭ C, E♭ D♭, F E♭, G♭ F … up to E♭ D♭ at the 11th and 9th frets of the high E string. '
                'Reaching over: the hand moves up as the scale climbs, three or four notes a string.')
EX.append(dict(id='b41', title='D♭ major broken in pairs',
               idea=('Longer lines from a whole scale by changing the order of its notes: here each note and then the one below it. '
                     'Theirs is C major; ours a fret higher is D♭ major, the key of your song.'),
               quote=quote('b41', 4, 'theirs is C major from the 3rd fret of the A string: C, B, D, C.', 91),
               bars=b))
ns, nm = ours('b42'), names('b42')
durs = [0.25] * 55 + [2]
b, cur, t, k0 = [], [], 0.25, 0
for i, d in enumerate(durs):
    cur.append(i); t += d
    if t >= 4 - 1e-9:
        its = ([['W', 0.25]] if not b else []) + [['R', [list(ns[j]) for j in cur], [durs[j] for j in cur], lab([nm[j] for j in cur], [''] * len(cur), 'the scale in fours')]]
        b.append(dict(chords=['Gb'], note='', items=its)); cur, t = [], 0.0
b[0]['note'] = ('G♭ major in one position at the 6th fret (index at the 6th, little finger at the 9th), four notes up from each note of the scale in turn: '
                'B♭ C♭ D♭ E♭, C♭ D♭ E♭ F, D♭ E♭ F G♭ … to A♭ B♭ C♭ D♭, in sixteenths after a sixteenth’s rest, so each four starts off the beat.')
EX.append(dict(id='b42', title='G♭ major in fours, in position',
               idea=('The scale in groups of four, each group starting a step higher, all in one hand position. '
                     'Theirs is G major at the 7th fret; ours a fret lower, G♭ major at the 6th.'),
               quote=quote('b42', 4, 'theirs is G major at the 7th fret of the low E string: B, C, D, E.', 91, durs=[0.25] * 4),
               bars=b))

BY = {e['id']: e for e in EX}
SECTIONS = list(R2.SECTIONS) + [dict(id=sid, title=t, part='Exercises', ex=[BY[k] for k in ks]) for sid, t, ks in (
    ('rom-12', 'Designated notes', ('d31', 'd32', 'd33', 'd34')),
    ('rom-13', 'II–V–I voicings', ('v35', 'v36')),
    ('rom-14', 'Designated notes on every string', ('d37', 'd38')),
    ('rom-15', 'Designated notes through the V chord', ('d39', 'd40')),
    ('rom-16', 'Broken scales', ('b41', 'b42')))]
assert sum(len(S['ex']) for S in SECTIONS[len(R2.SECTIONS):]) == len(EX)
