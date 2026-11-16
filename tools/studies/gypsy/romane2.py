"""L'Esprit Manouche, part A of chapters 5–9 (book pp. 41–75; PDF = book + 1), the diagrams and the exercises built from
them, added to the gypsy arpeggios page after chapters 1–4 (romane.py).

The rule is the same: their diagram or tab moved whole along the neck, every note on the same string, into the keys of
your It Had to Be You (D♭ major, its minor side B♭ minor, and G♭ major where bars 24–25 go): their A minor up a fret to
B♭ minor, their C major up a fret to D♭, their G major down a fret to G♭ (none of their G major diagrams uses an open
string, so moving down is possible). Their G7 is C major's V, so it goes up a fret to A♭7, your V. Where a diagram has
no key (the circle of fifths, the tritone), the note says why ours sits where it does.

Left out: exercises 23, 25 and 26 (and 28's neighbours in later chapters) are phrases, Romane's own melodies: the
book's, not exercises to move. check_romane2.py checks every note."""
import sys
sys.path.insert(0, '/home/claude/studies'); sys.path.insert(0, '/home/claude/studies/gypsy')
import romane as R1

BOOK, OPENS = R1.BOOK, R1.OPENS
midi = R1.midi

# their tabs and diagrams as read from the book: (string, fret) in playing order; 1 = the high E string
DIM12 = R1.THEIRS['dim']                                                      # ex 15 uses ex 3's twelve notes
BROKEN = [(1, 2), (1, 2), (3, 2), (3, 4), (3, 4), (5, 4), (5, 6), (5, 6), (7, 6), (7, 8), (7, 8), (9, 8), (9, 10), (9, 10), (11, 10), (11, 12)]
THEIRS = {
    'brk':  [DIM12[i - 1] for p in BROKEN for i in p],
    'maj7': [(6, 2), (6, 3), (5, 2), (5, 5), (4, 4), (4, 5), (3, 4), (3, 7), (2, 7), (2, 8), (1, 7), (1, 10),
             (1, 10), (1, 7), (2, 8), (2, 7), (3, 7), (3, 4), (4, 5), (4, 4), (5, 5), (5, 2), (6, 3), (6, 2)],
    'sw1':  [(4, 4), (4, 5), (3, 4), (2, 3), (2, 7), (2, 3), (3, 4), (4, 5)],
    'sw2':  [(4, 6), (4, 7), (3, 5), (2, 5), (2, 8), (2, 5), (3, 5), (4, 7)],
    'c6':   [(6, 7), (6, 8), (5, 6), (5, 7), (4, 4), (4, 5), (3, 4), (3, 5), (2, 4), (2, 5), (1, 4), (1, 5)],
    'wt1':  [(6, 7), (6, 9), (5, 6), (5, 8), (4, 5), (4, 7), (3, 4), (3, 6), (2, 4), (2, 6), (1, 3), (1, 5), (1, 7)],
    'wt2':  [(6, 3), (6, 5), (6, 7), (5, 4), (5, 6), (5, 8), (4, 5), (4, 7), (4, 9), (3, 6), (3, 8), (3, 10),
             (2, 8), (2, 10), (2, 12), (1, 9), (1, 11), (1, 13), (1, 15)],
    'add9': [(6, 3), (6, 5), (6, 7), (5, 5), (4, 5), (4, 7), (4, 9), (3, 7), (2, 8), (2, 10), (1, 7), (1, 10), (1, 12)],
    'diat': [(4, 5), (3, 4), (2, 3), (1, 3), (1, 5), (2, 7), (3, 5), (4, 7),
             (4, 9), (3, 7), (2, 8), (1, 7), (1, 8), (2, 10), (3, 8), (4, 10),
             (4, 9), (3, 7), (2, 8), (1, 7), (1, 5), (2, 7), (3, 5), (4, 7), (4, 5)],
    'sus':  [(6, 3), (5, 5), (4, 3), (3, 5), (2, 3), (1, 5), (2, 3), (3, 5), (4, 3), (5, 5), (6, 3)],
    'anat1': [(5, 3), (6, 5), (5, 5), (6, 3), (5, 3)],
    'anat2': [(6, 13), (6, 10), (5, 10), (6, 8), (5, 8)],
    'circ': [(6, 12), (5, 12), (6, 10), (5, 10), (6, 8), (5, 8), (6, 6), (5, 6), (6, 4), (5, 4), (6, 2), (5, 2), (6, 0)],
    'trit': [(6, 5), (5, 6), (4, 7), (5, 6), (4, 7), (3, 8)],
    'wtt':  [(5, 12), (4, 13), (3, 14), (3, 12), (4, 11), (5, 10), (5, 8), (4, 9), (3, 10), (3, 8), (4, 7), (5, 6),
             (5, 4), (4, 5), (3, 6), (3, 4), (4, 3), (5, 2), (5, 0)],
    'b5':   [(6, 3), (5, 4), (4, 3), (3, 4), (2, 3), (1, 4), (2, 3), (3, 4), (4, 3), (5, 4), (6, 3)],
    'dmsw': [(3, 7), (2, 6), (1, 5), (1, 10), (1, 5), (2, 6), (3, 7), (2, 6), (1, 5), (1, 9), (1, 5), (2, 6),
             (3, 7), (2, 6), (1, 5), (1, 8), (1, 5), (2, 6)],
}
SHIFT = {'brk': 1, 'maj7': -1, 'sw1': -1, 'sw2': -1, 'c6': 1, 'wt1': 1, 'wt2': 1, 'add9': -1, 'diat': -1, 'sus': 1,
         'anat1': 1, 'anat2': 1, 'circ': 1, 'trit': 3, 'wtt': 1, 'b5': 1, 'dmsw': 1}
SPELL = {
    'gb': {6: 'G♭', 8: 'A♭', 10: 'B♭', 11: 'C♭', 1: 'D♭', 3: 'E♭', 5: 'F', 7: 'G', 9: 'A', 2: 'D'},
    'db': {1: 'D♭', 3: 'E♭', 5: 'F', 6: 'G♭', 8: 'A♭', 10: 'B♭', 0: 'C', 2: 'D', 4: 'E', 7: 'G', 9: 'A', 11: 'C♭'},
    'wt': {0: 'C', 2: 'D', 4: 'E', 6: 'G♭', 8: 'A♭', 10: 'B♭'},
    'dim': {6: 'G♭', 9: 'A', 0: 'C', 3: 'E♭'},
    'circ': {5: 'F', 10: 'B♭', 3: 'E♭', 8: 'A♭', 1: 'D♭', 6: 'G♭', 11: 'B', 4: 'E', 9: 'A', 2: 'D', 7: 'G', 0: 'C'},
}
THEIR_NM = {0: 'C', 1: 'C♯', 2: 'D', 3: 'D♯', 4: 'E', 5: 'F', 6: 'F♯', 7: 'G', 8: 'G♯', 9: 'A', 10: 'B♭', 11: 'B'}
THEIR_FLAT = {0: 'C', 1: 'D♭', 2: 'D', 3: 'E♭', 4: 'E', 5: 'F', 6: 'G♭', 7: 'G', 8: 'A♭', 9: 'A', 10: 'B♭', 11: 'B'}


def ours(key): return [(s, f + SHIFT[key]) for s, f in THEIRS[key]]
def names(key, sp, seq=None): return [SPELL[sp][midi(s, f) % 12] for s, f in (seq or ours(key))]
def lab(nm, marks=None, what=''):
    if marks: nm = [n + m for n, m in zip(nm, marks)]
    return '=' + ','.join(nm) + '|' + what


def split(notes, durs, nmz, bar_len, chord_of, what, vel=None):
    """notes with their lengths into bars of bar_len beats; chord_of(bar index) gives the bar's chords"""
    out, cur, t = [], [], 0.0
    for i, (n, d) in enumerate(zip(notes, durs)):
        cur.append(i); t += d
        if t >= bar_len - 1e-9 or i == len(notes) - 1:
            it = ['R', [list(notes[j]) for j in cur], [durs[j] for j in cur], lab([nmz[j] for j in cur], what=what)]
            if vel: it.append({'vel': [vel[j] for j in cur]})
            items = [it]
            if t < bar_len - 1e-9: items.append(['W', bar_len - t])
            out.append(dict(chords=chord_of(len(out)), note='', items=items))
            cur, t = [], 0.0
    return out


def updown(seq): return list(seq) + list(seq[-2::-1])


def quote(key, n, text, p, durs=None, nm=THEIR_NM):
    ns = THEIRS[key][:n]
    return R1.T(text, p, ns, durs=durs, names=[nm[midi(s, f) % 12] for s, f in ns])


def fingers(seq, fs):
    STR = {6: 'low E', 5: 'A', 4: 'D', 3: 'G', 2: 'B', 1: 'high E'}
    out, cur = [], None
    for (s, f), x in zip(seq, fs):
        if s != cur: out.append([s, []]); cur = s
        out[-1][1].append(str(x))
    return '; '.join(f'{STR[s]} {"-".join(xs)}' for s, xs in out)


EX = []
H = -0.12                                                    # a hammered or pulled note sounds softer

# ---------------------------------------------------------------- chapter 5
seq = ours('brk')
full = seq + seq[::-1]
nmz = names('brk', 'dim', full)
b = split(full, [0.5] * len(full), nmz, 4, lambda k: ['Gbdim7'], 'the diminished seventh, broken')
b[0]['note'] = ('The twelve notes of the diminished seventh two to a string (G♭, A, C, E♭ from the 2nd fret of the low E string, as in the first diminished exercise), '
                'played in an order that goes forward two notes and back one: G♭ A G♭ A, C A C E♭, C E♭ G♭ E♭ … to the top, four bars of eighths; then all of it backwards. '
                'Index and little finger, the hand a fret higher for each string and two frets from the G to the B string.')
EX.append(dict(id='brk', title='The diminished seventh, broken',
               idea=('The same notes as the plain diminished arpeggio, in a new order: a longer line over the same chord, which you can play wherever the 7♭9 chord is. '
                     'Ours is theirs a fret higher, G♭°7: your F7♭9 (bars 10 and 27) and A♭7♭9 without their roots.'),
               quote=quote('brk', 4, 'theirs is F°7 from the 1st fret: F, G♯, F, G♯.', 41),
               bars=b))

seq = ours('maj7')
nmz = names('maj7', 'gb')
durs = [0.5] * 23 + [2.5, ]
b = split(seq, durs, nmz, 4, lambda k: ['Gbmaj7'], 'G♭maj7 over three octaves')
# the last note is tied across the bar line: the third bar holds it two beats and a half, then rests
b = b[:2] + [dict(chords=['Gbmaj7'], note='', items=[['R', [list(x) for x in seq[16:]], [0.5] * 7 + [2.5], lab(nmz[16:], what='G♭maj7 over three octaves')], ['W', 2]])]
b[0]['note'] = ('F, G♭, B♭, D♭ two notes a string from the F at the 1st fret of the low E string to the D♭ at the 9th fret of the high E string, '
                'the top note twice, and back down to the F, held. The first four notes make a shape that repeats on every pair of strings (the B string a fret higher). '
                f'Fingers: {fingers(seq[:12], [1, 2, 1, 4, 1, 2, 1, 4, 1, 2, 1, 4])}.')
EX.append(dict(id='maj7', title='G♭ major 7 over three octaves',
               idea=('The major seventh arpeggio in three octaves with two notes on each string, starting from its 7th. '
                     'Theirs is G major 7; ours is a fret lower, G♭maj7, the chord of your bar 25.'),
               quote=quote('maj7', 4, 'theirs is Gmaj7 from the F♯ at the 2nd fret of the low E string: F♯, G, B, D.', 42),
               bars=b))

# ---------------------------------------------------------------- chapter 6: sweeps
SW_MARKS = ['↓', 'h', '↓', '↓', '↑', '↑', '↑', '↑']
SW_VEL = [0.05, H, 0, 0, 0, 0, 0, 0]


def sweep_bars(seqs, chords, spells, what):
    out = []
    for k, (sq, ch, sp) in enumerate(zip(seqs, chords, spells)):
        nm = names(None, sp, sq)
        marks = list(SW_MARKS)
        vel = list(SW_VEL)
        if k: marks[0] = 'p'; vel[0] = H                        # pulled off from the last note before
        out.append(dict(chords=[ch], note='', items=[['R', [list(x) for x in sq], [0.5] * 8, lab(nm, marks, what), {'vel': vel}]]))
    return out


SP_AB = {8: 'A♭', 11: 'C♭', 3: 'E♭', 6: 'G♭', 7: 'G'}
SPELL['abm'] = SP_AB
SPELL['bbm'] = {10: 'B♭', 1: 'D♭', 5: 'F', 8: 'A♭', 9: 'A'}
SPELL['cb'] = {11: 'C♭', 3: 'E♭', 6: 'G♭', 10: 'B♭'}
s1, s2 = ours('sw1'), ours('sw2')
b = sweep_bars([s1, s1], ['Gbmaj7', 'Gbmaj7'], ['gb', 'gb'], 'the sweep on G♭maj7')
b[0]['note'] = ('F hammered onto G♭ on the D string, then B♭ and D♭ on the next strings in one sweep of the pick down, the F at the 6th fret of the B string, '
                'and back down to G♭ in one sweep up; the G♭ pulls off to the F to start again. Twice. ↓ down, ↑ up, h hammered, p pulled off.')
EX.append(dict(id='sw1', title='The sweep on G♭ major 7',
               idea=('The right hand sweeps: one stroke carries the pick across several strings, down going up and up coming down, a note on each string; '
                     'the left hand hammers and pulls the two notes on the bottom string. Theirs is on G major 7, ours a fret lower on G♭maj7.'),
               quote=quote('sw1', 4, 'theirs: F♯ hammered onto G on the D string, then B and D, down strokes.', 49),
               bars=b))
b = sweep_bars([s2, s2], ['Abm7', 'Abm7'], ['abm', 'abm'], 'the sweep on A♭m7')
b[0]['note'] = ('The same sweep on A♭ minor 7: G hammered onto A♭ on the D string, C♭, E♭, the G♭ at the 7th fret of the B string, and back down. Twice.')
EX.append(dict(id='sw2', title='The sweep on A♭ minor 7',
               idea='The same sweep on the minor seventh chord a step up: theirs Am7, ours A♭m7, the chord of your bar 24.',
               quote=quote('sw2', 4, 'theirs: G♯ hammered onto A, then C and E.', 49),
               bars=b))
s3 = [(s, f + 2) for s, f in s2]                               # III: the minor sweep two frets up
s4 = [(s, f + 5) for s, f in s1]                               # IV: the major sweep five frets up
b = sweep_bars([s1, s2, s3, s4], ['Gbmaj7', 'Abm7', 'Bbm7', 'Cbmaj7'], ['gb', 'abm', 'bbm', 'cb'], 'up the key in sweeps')
b[0]['note'] = ('The two sweeps joined up the key of G♭: G♭maj7 (I), A♭m7 (II), B♭m7 (III: the minor sweep two frets higher), C♭maj7 (IV: the major sweep five frets higher), a bar each.')
EX.append(dict(id='sw3', title='The sweeps up the key: I, II, III, IV',
               idea=('Their next step: join the two sweeps and climb the key, the minor one moved up two frets for the III chord and the major one five frets for the IV. '
                     'In G♭: G♭maj7, A♭m7, B♭m7, C♭maj7 (your bars 24–26 have A♭m7, G♭maj7 and C♭9).'),
               quote=R1.T('their G major 7, A minor 7, B minor 7, C major 7, the sweeps moved along the neck.', 50),
               bars=b))

c6 = ours('c6')
nm6 = names('c6', 'db')
PAIRS = [1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1, 2, 3, 4, 5, 6]          # their tab, pair by pair
line = [x for p in PAIRS for x in (c6[2 * p - 2], c6[2 * p - 1])]
line_nm = [x for p in PAIRS for x in (nm6[2 * p - 2], nm6[2 * p - 1])]
stars = ['', '*'] * 16
b = split(updown(c6), [0.5] * 22 + [1], names('c6', 'db', updown(c6)), 4, lambda k: ['Db6'], 'D♭6, each note from a half step below')
b += [dict(chords=['Db6'], note='', items=[['R', [list(x) for x in line[i:i + 8]], [0.5] * 8, lab(line_nm[i:i + 8], stars[i:i + 8], 'the pairs up, down and up')]]) for i in range(0, 32, 8)]
b[0]['note'] = ('D♭, F, A♭ and B♭, each one reached from the note a half step below it on the same string, index then middle finger only: '
                'C D♭ from the 8th fret of the low E string, E F, G A♭, C D♭, E F, A B♭ at the 5th and 6th frets of the high E string; up and back. '
                'Then the pairs in the order of their tab: up four, then 5 6 5 4, 3 2 1 2, 3 4 5 6 (* the chord’s notes).')
EX.append(dict(id='c6', title='D♭6, each note from a half step below',
               idea=('Every note of a chord approached from a half step below, the way Django played it with two fingers: the tension of the lower note resolves into the chord. '
                     'It works with almost any chord, best over V going to I. Theirs is C6; ours a fret higher is D♭6, as in your bars 30–31, where A♭13 (its 3rd is C, the step below D♭) goes to D♭6/9.'),
               quote=quote('c6', 4, 'theirs is C6 from the 7th fret of the low E string: B, C, D♯, E.', 50),
               bars=b))

# ---------------------------------------------------------------- chapter 7: the whole tone scale
WT_NOTE = ('The whole tone scale has only whole steps, six notes, the same scale from any of them; it goes with seventh chords. '
           'Theirs is the scale of B (and of G, the same six notes), for B7, D♭7, E♭7, F7, G7 and A7; ours is a fret higher, the scale of A♭7♯5 '
           '(your bars 1, 16, 17 and 32) and of B♭7, C7, D7, E7 and G♭7.')
w1 = ours('wt1')
up1 = updown(w1)
b = split(up1, [0.5] * 24 + [3], names('wt1', 'wt', up1), 3, lambda k: ['Ab7#5'], 'the whole tone scale in descending steps')
tri = split(up1, [1 / 3] * 24 + [4 - 24 / 3 + 8], names('wt1', 'wt', up1), 4, lambda k: ['Ab7#5'], 'the same in triplets')
b[0]['note'] = ('C, D, E, G♭, A♭, B♭ two notes a string from the C at the 8th fret of the low E string, each string a fret lower than the last '
                '(the B string the same as the G), up to the C at the 8th fret of the high E string, in eighths, three beats to a bar as they write it; '
                'then back. Then the same in triplets, twelve to a bar.')
EX.append(dict(id='wt1', title='The whole tone scale in descending steps', idea=WT_NOTE + ' Here the hand steps down the neck as the scale goes up.',
               quote=quote('wt1', 4, 'theirs is B’s from the 7th fret of the low E string: B, D♭, E♭, F.', 57, nm=THEIR_FLAT),
               bars=b + tri))
w2 = ours('wt2')
up2 = updown(w2)
b = split(up2, [0.5] * 36 + [3], names('wt2', 'wt', up2), 3, lambda k: ['Ab7#5'], 'the whole tone scale in ascending steps')
tri = split(up2, [1 / 3] * 36 + [4], names('wt2', 'wt', up2), 4, lambda k: ['Ab7#5'], 'the same in triplets')
b[0]['note'] = ('A♭, B♭, C, D, E, G♭ three notes a string, index, middle, little finger two frets apart, each string a fret higher (two from the G to the B string), '
                'from the A♭ at the 4th fret of the low E string to the A♭ at the 16th fret of the high E string; back down. Then in triplets. '
                'Afterwards play both scales over G♭7, B♭7, D7, C7, E7 and A♭7, two bars each: the same six notes fit all six.')
EX.append(dict(id='wt2', title='The whole tone scale in ascending steps', idea='The same scale three notes a string, the hand stepping up the neck.',
               quote=quote('wt2', 4, 'theirs is G’s from the 3rd fret of the low E string: G, A, B, D♭.', 58, nm=THEIR_FLAT),
               bars=b + tri))

# ---------------------------------------------------------------- chapter 8
a9 = ours('add9')
b = split(a9, [0.5] * 12 + [2], names('add9', 'gb'), 4, lambda k: ['Gbadd9'], 'G♭ with the 9th')
b[-1]['items'] = [b[-1]['items'][0][:3] + [b[-1]['items'][0][3]], ['W', 1]]
b[-1]['items'][0][2] = [0.5] * 4 + [1]
b[0]['note'] = ('G♭, A♭, B♭ and D♭ up from the 2nd fret of the low E string: three notes on it, one on the A string, three on the D string, one on the G string, two on the B string '
                'and three on the high E string, to the E♭ at the 11th fret, which ends their tab on the chord’s 6th. Up only, as they play it.')
EX.append(dict(id='add9', title='G♭ major with the 9th',
               idea=('The major chord coloured with the 9th, a shape gypsy players use all the time, the major cousin of the minor one with the 9th. '
                     'Theirs is G; ours a fret lower is G♭, your bar 25.'),
               quote=quote('add9', 4, 'theirs is G from the 3rd fret of the low E string: G, A, B, D.', 65),
               bars=b))
dt = ours('diat')
dt_nm = names('diat', 'gb')
DCH = [['Gb', 'Abm6'], ['Gb/Bb', 'Cbm6'], ['Gb', 'Db7'], ['Gb']]
marks = (['↓'] * 4 + ['↑'] * 4) * 3 + ['']
b = []
for k in range(4):
    ns = dt[8 * k:8 * k + 8]
    if k < 3:
        b.append(dict(chords=DCH[k], note='', items=[['R', [list(x) for x in ns], [0.5] * 8, lab(dt_nm[8 * k:8 * k + 8], marks[8 * k:8 * k + 8], 'up one chord, down the next')]]))
    else:
        b.append(dict(chords=DCH[k], note='', items=[['R', [list(x) for x in ns], [2], lab(dt_nm[24:], what='home')], ['W', 2]]))
b[0]['note'] = ('A sweep down the pick up one chord (G♭: G♭ B♭ D♭ G♭ from the 4th fret of the D string), a sweep up the pick down the next (A♭, F, C♭, A♭: A♭ minor with its 6th), '
                'then G♭ with B♭ in the bass up and C♭ minor 6 down (C♭, A♭, D, C♭), G♭ up and D♭7 down, and G♭. They name the minor chords Am7 and Cm7; the line plays them with the 6th.')
EX.append(dict(id='diat', title='Up the key in sweeps: G♭, A♭m7, G♭/B♭, C♭m7, D♭7',
               idea=('Chords of the key linked a step at a time, each swept: down the pick going up one chord, up the pick coming down the next. '
                     'Theirs is in G; ours a fret lower in G♭.'),
               quote=quote('diat', 4, 'theirs starts on G at the 5th fret of the D string: G, B, D, G.', 66),
               bars=b))
su = ours('sus')
SUS_MARKS = ['↓'] * 6 + ['↑'] * 5
su_nm = names('sus', 'db')
b = [dict(chords=['Ab7sus4'], note='', items=[['R', [list(x) for x in su[i:j]], d, lab(su_nm[i:j], SUS_MARKS[i:j], 'one note a string, two frets apart')]])
     for i, j, d in ((0, 4, [0.5] * 4), (4, 8, [0.5] * 4), (8, 11, [0.5, 0.5, 1]))]
b[0]['note'] = ('A♭ at the 4th fret of the low E string, then E♭, G♭, D♭, E♭, B♭: one note a string, index and ring finger in turn at the 4th and 6th frets, '
                'down strokes going up and up strokes coming down; two beats to a bar as they write it.')
EX.append(dict(id='sus', title='A♭7sus4 in one sweep',
               idea=('A typical gypsy shape: one note on each string, two frets apart, for the 7sus4 chord with the 9th in place of the root on top '
                     '(which also makes it the minor 7 chord a fifth up). Theirs is G7sus4 (= Dm7); ours a fret higher is A♭7sus4 (= E♭m7): your E♭m9 (bar 15) going to A♭7 (bar 16).'),
               quote=quote('sus', 4, 'theirs is G7sus4 from the 3rd fret of the low E string: G, D, F, C.', 67),
               bars=b))

# ---------------------------------------------------------------- chapter 9: the notes on the neck
an1, an2 = ours('anat1'), ours('anat2')
SPELL['an'] = {1: 'D♭', 10: 'B♭', 3: 'E♭', 8: 'A♭', 6: 'G♭'}
b = [dict(chords=['Dbmaj9', 'Bbm7', 'Ebm9', 'Ab7'], note='', items=[['R', [list(x) for x in an1[:4]], [1] * 4, lab(names(None, 'an', an1[:4]), what='the anatole’s roots, at the 4th fret')]]),
     dict(chords=['Dbmaj9'], note='', items=[['R', [list(an1[4])], [4], lab(names(None, 'an', an1[4:]), what='home')]]),
     dict(chords=['Gbmaj7', 'Ebm7', 'Abm7', 'Db7'], note='', items=[['R', [list(x) for x in an2[:4]], [1] * 4, lab(names(None, 'an', an2[:4]), what='the anatole’s roots, higher up')]]),
     dict(chords=['Gbmaj7'], note='', items=[['R', [list(an2[4])], [4], lab(names(None, 'an', an2[4:]), what='home')]])]
b[0]['note'] = ('The anatole is I, VI, II, V: your intro, D♭maj9, B♭m7, E♭m9, A♭7. With I on the A string at the 4th fret, VI is two frets up on the low E string, '
                'II two frets up on the A string, V on the low E string under I. Then the same with I on the low E string at the 14th fret: G♭, E♭, A♭, D♭, G♭.')
EX.append(dict(id='anat', title='The anatole’s roots on the two bass strings',
               idea=('Gypsy players find chords by their roots on the two bass strings. The turnaround, I VI II V, sits in a little box there: learn the box. '
                     'Theirs is in C (C, A, D, G) and in F; ours a fret higher is in D♭, the turnaround of your intro, and in G♭.'),
               quote=quote('anat1', 2, 'their first box is in C at the 3rd fret: C, A.', 73, durs=[1, 1]),
               bars=b))
ci = ours('circ')
cnm = names('circ', 'circ')
b = [dict(chords=[], note='', items=[['R', [list(x) for x in ci[i:i + 4]], [1] * len(ci[i:i + 4]) if i < 12 else [4], lab(cnm[i:i + 4], what='round the circle of fifths')]]) for i in range(0, 13, 4)]
b[0]['note'] = ('All twelve roots, each a fifth below the last (a fourth above): F at the 13th fret of the low E string, B♭ on the A string next to it, E♭ two frets lower on the low E string, '
                'A♭ beside it, and so down the neck two frets at a time to the F at the 1st fret. Each five in a row is a turnaround: III, VI, II, V, I.')
EX.append(dict(id='circ', title='Round the circle of fifths',
               idea=('Joining the boxes, the roots walk down the circle of fifths through all twelve notes on the two bass strings. '
                     'Theirs starts on E at the 12th fret; ours on F at the 13th, so the circle passes B♭, E♭ and A♭ first, the roots of your B♭9 (bars 3–4), E♭9 (bars 5–8) and A♭7 (bar 9).'),
               quote=quote('circ', 2, 'theirs starts on E at the 12th fret of the low E string: E, A.', 73, durs=[1, 1]),
               bars=b))
tt = ours('trit')
SPELL['tt'] = {0: 'C', 6: 'G♭'}
tt_full = updown(tt)
b = split(tt_full, [0.5] * 10 + [3], names(None, 'tt', tt_full), 4, lambda k: ['Ab7'], 'tritones')
b[0]['note'] = ('C on the low E string at the 8th fret, G♭ a string up and a fret higher, C again a string up and a fret higher: an octave in two tritones. '
                'Then G♭, C, G♭ the same way from the A string. Up and back.')
EX.append(dict(id='trit', title='Tritones',
               idea=('Half an octave, three whole steps: the interval at the heart of the 7th chord (its 3rd and 7th) and of the tritone substitution. On the neck it is a string up and a fret higher. '
                     'Theirs starts on A at the 5th fret (A and E♭); ours starts three frets higher on C, so its notes are C and G♭, the 3rd and 7th of A♭7, your V chord.'),
               quote=quote('trit', 3, 'theirs starts on A at the 5th fret of the low E string: A, E♭, A.', 74, nm=THEIR_FLAT),
               bars=b))
wtt = ours('wtt')
wtt_nm = names('wtt', 'wt')
marks = (['↓'] * 3 + ['↑'] * 3) * 3 + ['']
b = [dict(chords=['Bb7'], note='', items=[['R', [list(x) for x in wtt[:12]], [1 / 3] * 12, lab(wtt_nm[:12], marks[:12], 'the whole tone scale in tritones')]]),
     dict(chords=['Bb7'], note='', items=[['R', [list(x) for x in wtt[12:]], [1 / 3] * 6 + [2], lab(wtt_nm[12:], marks[12:], 'the whole tone scale in tritones')]])]
b[0]['note'] = ('From the B♭ at the 13th fret of the A string: B♭, E, B♭ up across three strings, then A♭, D, A♭ down, two frets lower, and so on down the neck a whole step at a time '
                'to the B♭ at the 1st fret of the A string, in triplets: down strokes going up, up strokes coming down.')
EX.append(dict(id='wtt', title='The whole tone scale in tritones, on B♭7',
               idea=('The whole tone scale found through the tritone: three notes, an octave in two tritones, then the next three a whole step down. '
                     'Theirs is on A7; ours a fret higher is on B♭7, your B♭9 of bars 3–4 and 19–20.'),
               quote=quote('wtt', 3, 'theirs is on A7 from the A at the 12th fret of the A string: A, E♭, A.', 74, durs=[1 / 3] * 3, nm=THEIR_FLAT),
               bars=b))
b5 = ours('b5')
SPELL['b5'] = {8: 'A♭', 2: 'D', 6: 'G♭', 0: 'C', 3: 'E♭', 9: 'A'}
b5nm = names(None, 'b5', b5)
B5_MARKS = ['↓'] * 6 + ['↑'] * 5
b = [dict(chords=['Ab7b5'], note='', items=[['R', [list(x) for x in b5[i:j]], d, lab(b5nm[i:j], B5_MARKS[i:j], 'tritones across the strings')]])
     for i, j, d in ((0, 4, [0.5] * 4), (4, 8, [0.5] * 4), (8, 11, [0.5, 0.5, 1]))]
b[0]['note'] = ('A♭ at the 4th fret of the low E string, D, G♭, C, E♭, A: one note a string at the 4th and 5th frets, index and middle finger, '
                'every pair of strings a tritone apart (A♭–D, G♭–C, E♭–A); down strokes going up, up strokes coming down, two beats to a bar.')
EX.append(dict(id='b5', title='The sweep on A♭7♭5',
               idea=('A typical gypsy lead that shows the tritone on the neck: the seventh chord with a flat 5th, a note on each string, swept. '
                     'Theirs is on G7(♭5); ours a fret higher is on A♭7(♭5), your V.'),
               quote=quote('b5', 4, 'theirs is on G7(♭5) from the 3rd fret of the low E string: G, C♯, F, B.', 75),
               bars=b))
dm = ours('dmsw')
SPELL['dm'] = {3: 'E♭', 6: 'G♭', 10: 'B♭', 2: 'D', 1: 'D♭'}
dmnm = names(None, 'dm', dm)
DM_MARKS = ['↓', '↓', '↓', '↓', '↑', '↑'] * 3
b = [dict(chords=['Ebm'], note='', items=[['R', [list(x) for x in dm[i:i + 6]], [1 / 3] * 6, lab(dmnm[i:i + 6], DM_MARKS[i:i + 6], 'E♭ minor with a falling top note')]]) for i in (0, 6, 12)]
b[0]['note'] = ('E♭ minor on the top three strings (E♭ at the 8th fret of the G string, G♭, B♭) swept down in a triplet, then a top note and back: '
                'E♭ (the root), then D (the major 7th), then D♭ (the minor 7th), one bar each, two beats to a bar.')
EX.append(dict(id='dmsw', title='E♭ minor swept, the top note falling',
               idea=('A sweep on the minor chord with a top note that falls a half step at a time, root, major 7th, minor 7th: the line inside E♭m, E♭m(maj7), E♭m7. '
                     'Theirs is on D minor; ours a fret higher is on E♭ minor, your E♭m9 of bars 15 and 32.'),
               quote=quote('dmsw', 3, 'theirs is on D minor at the 7th fret of the G string: D, F, A.', 75, durs=[1 / 3] * 3),
               bars=b))

BY = {e['id']: e for e in EX}
SECTIONS = list(R1.SECTIONS) + [dict(id=sid, title=t, part='Exercises', ex=[BY[k] for k in ks]) for sid, t, ks in (
    ('rom-5', 'The diminished seventh broken; the major seventh', ('brk', 'maj7')),
    ('rom-6', 'Sweeps', ('sw1', 'sw2', 'sw3')),
    ('rom-7', 'Each note from a half step below', ('c6',)),
    ('rom-8', 'The whole tone scale', ('wt1', 'wt2')),
    ('rom-9', 'Major with the 9th; the key in sweeps; 7sus4', ('add9', 'diat', 'sus')),
    ('rom-10', 'The notes on the neck', ('anat', 'circ', 'trit', 'wtt')),
    ('rom-11', 'Swept: the 7♭5 chord and a falling top note', ('b5', 'dmsw')))]
assert sum(len(S['ex']) for S in SECTIONS[len(R1.SECTIONS):]) == len(EX)
