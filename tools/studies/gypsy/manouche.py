"""Wrembel, Getting into Gypsy Jazz Guitar, ch. 2 (pp. 16–20): the manouche accompanist's chords, as rules. Major
chords as 6/9 (a maj7 only with its 3rd in the bass); minor chords as minor 6 (or 6/9), never the minor 7; a 7th chord
chosen by where it goes: neutral, or with ♭9 or ♭13 into a minor chord, or as 9, 13, 13♭9, 7♭5, 9♭5 into a major one;
the minor 7♭5 heard as a minor 6 with its 6th in the bass; the diminished chord for a 7♭9 (a half step above the
root, and every minor 3rd from there) and as a passing chord; the line clichés in minor and major; the harmonic march
(no II–V: V7 of V instead). His pages show movable shapes; ours are worked out by rule (voicing.py) for the chords
of Очи чёрные (your chart) and Я вас любил (your bars 8–17), in la pompe. check_chords.py checks every grip."""
import sys
sys.path.insert(0, '/home/claude/studies'); sys.path.insert(0, '/home/claude/studies/gypsy')
import entry as G0
import voicing as V

K, BOOK, SQ, WH = G0.K, G0.BOOK, G0.SQ, G0.WH
S6, S5, S5x, S6x = (6, 4, 3, 2), (5, 4, 3, 2), (5, 4, 3, 2, 1), (6, 5, 4, 3, 2, 1)
R6 = [(6, 4, 3, 2), (6, 4, 3, 2, 1), (6, 5, 4, 3, 2, 1)]      # root on the low E string, the A string silent (or all six)
R5 = [(5, 4, 3, 2), (5, 4, 3, 2, 1), (5, 3, 2, 1)]            # root on the A string
CHECK = []                 # (exercise, name, grip)
FIX = {}                   # one grip per chord on the whole page: the first one found


def T(text, p): return dict(where=f'{BOOK}, p. {p}', text=text, item=None, by='Wrembel')


def bar_of(chords):
    """la pompe under one, two or four chords: (name, grip) each"""
    if len(chords) == 1: return [K(chords[0][0], chords[0][1], SQ + WH + SQ + WH)]
    if len(chords) == 2: return [K(n, g, SQ + WH) for n, g in chords]
    if len(chords) == 4: return [K(n, g, SQ if k % 2 == 0 else WH) for k, (n, g) in enumerate(chords)]
    raise ValueError(len(chords))


def lay(exid, rows, strings, near, note='', root_needed=None):
    """rows: chord names per bar; the grips by least movement on the string sets given (one per chord, in order)"""
    names = [n for r in rows for n in r]
    st = strings if isinstance(strings, list) else [strings] * len(names)
    grips = V.path(names, st, near, root_needed=root_needed, fixed=FIX)
    for n, g in zip(names, grips): FIX.setdefault(n, g)
    bars, k = [], 0
    for r in rows:
        ch = [(n, grips[k + j]) for j, n in enumerate(r)]
        k += len(r)
        bars.append(dict(chords=list(r), note='', items=bar_of(ch)))
        for n, g in ch: CHECK.append((exid, n, g))
    bars[0]['note'] = note
    return bars


def cliche(exid, start, names, string, step, rows, note=''):
    """a line cliché: the first grip held, one string's note moving a half step (`step`) each chord"""
    grips, g = [], list(start)
    for k, n in enumerate(names):
        if k: g = list(g); g[6 - string] += step
        grips.append(g)
    bars, k = [], 0
    for r in rows:
        ch = [(names[k + j], grips[k + j]) for j in range(r)]
        k += r
        bars.append(dict(chords=[n for n, _ in ch], note='', items=bar_of(ch)))
        for n, g_ in ch: CHECK.append((exid, n, g_))
    bars[0]['note'] = note
    return bars


def dims(exid, near, note):
    """E7 as diminished chords a half step above E, then each minor 3rd up: one shape moved three frets at a time,
    each going to the same A minor 6"""
    d0 = V.best('Abdim7', near, strings=(6, 4, 3, 2))
    am6 = FIX['Am6']
    bars = []
    for k, n in enumerate(['Abdim7', 'Bdim7', 'Ddim7']):
        g = [f + 3 * k if f > 0 else f for f in d0]
        bars.append(dict(chords=[n, 'Am6'], note='', items=bar_of([(n, g), ('Am6', am6)])))
        CHECK.append((exid, n, g)); CHECK.append((exid, 'Am6', am6))
    bars[0]['note'] = note
    return bars


STRN = {6: 'low E', 5: 'A', 4: 'D'}
NM = ['C', 'D♭', 'D', 'E♭', 'E', 'F', 'F♯', 'G', 'A♭', 'A', 'B♭', 'B']


def ordn(n): return f'{n}{"th" if 10 <= n % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")}'


def disp(n): return n.replace('b', '♭').replace('#', '♯').replace('dim7', '°7')


def where(exid):
    """'G6/9: G on the low E string, 3rd fret; ...' for each chord of the exercise, once"""
    seen, out = set(), []
    for e, n, g in CHECK:
        if e != exid or (n, tuple(g)) in seen: continue
        seen.add((n, tuple(g)))
        i = next(i for i, f in enumerate(g) if f >= 0)
        m = V.OPENS[i] + g[i]
        root, q, bass = G0.gtr.parse(n) if hasattr(G0, 'gtr') else V.gtr.parse(n)
        nm = (disp(n.split('/')[1]) if bass is not None and m % 12 == bass else
              disp(n[:2] if n[1:2] in ('b', '#') else n[0]) if m % 12 == root else NM[m % 12])
        out.append(f'{disp(n)}: {nm} on the {STRN[6 - i]} string, {ordn(g[i])} fret')
    return 'The bass of each grip: ' + '; '.join(out) + '.'


EX = []
# 1. major chords: 6/9
EX.append(dict(
    id='w-maj69', title='Major chords: the 6/9',
    idea=('Wrembel: in the manouche style a plain major chord, a major 6, a 6/9 or a major 7 written on the chart are all played as the 6/9, the major 7 only when its 3rd is '
          'in the bass. The 6th and the 9th make the gypsy major sound; the major 7th is left to the soloist.'),
    quote=T('his major chords: two 6/9 shapes, one with the root on the low E string, one on the A string, and the major 7 with its 3rd in the bass.', 16),
    bars=lay('w-maj69', [['G6/9'], ['C6/9']], [R6, R5], 3,
             'Я вас любил, bars 8–9: G and C major 7 on your chart, both played as 6/9 (and so is bar 10’s C). G with the root on the low E string, all six strings; C with the root on the A string.')))
# 2. minor chords: minor 6
EX.append(dict(
    id='w-min6', title='Minor chords: the minor 6',
    idea=('The minor 7th is the note to avoid on a minor chord, Wrembel says: the 6th is the colour of manouche minor, and it lets the soloist choose between the 7th and the major 7th. '
          'A minor 6/9 adds the 9th.'),
    quote=T('his minor chords: the minor, minor 6/9 and minor 6 shapes, the root on the low E or A string; the last minor 6 has no root in the bass.', 16),
    bars=lay('w-min6', [['Am6'], ['Am6/9'], ['Dm6'], ['Dm6/9'], ['Am6'], ['Am6/9']], [R6, R6 + R5, R5, R5, R6, R6 + R5], 5,
             'Очи чёрные’s A minor and D minor (your bars 7–12) as minor 6 and minor 6/9.')))
# 3. sevenths into minor
EX.append(dict(
    id='w-7min', title='Seventh chords going to a minor chord',
    idea=('A 7th chord’s colour depends on where it goes. The plain 7 is neutral, at home before major or minor. Going to a minor chord it takes one of three tensions: '
          'the ♯9, the ♭9 or the ♭13.'),
    quote=T('the neutral 7 in three shapes; then the 7♯9, 7♭9 and 7♭13 that resolve to minor.', 17),
    bars=lay('w-7min', [['E7', 'Am6'], ['E7#9', 'Am6'], ['E7b9', 'Am6'], ['E7b13', 'Am6']], [R5, R6] * 4, 6,
             'Очи чёрные’s E7 going to A minor 6: plain, with the ♯9 (G), with the ♭9 (F), with the ♭13 (C).')))
# 4. sevenths into major
EX.append(dict(
    id='w-7maj', title='Seventh chords going to a major chord',
    idea=('Going to a major chord the 7th has seven forms in Wrembel’s list: 9, 13, 13♭9, 7♭5, 9♭5 and second shapes of the 9 and the 7♭5. '
          'He warns that the last two (7♭5 and 9♭5) are tricky to use.'),
    quote=dict(where=f'{BOOK}, pp. 17–18', text='the 9, 13, 13(♭9), 7♭5 and 9♭5 shapes going to a major chord.', item=None, by='Wrembel'),
    bars=lay('w-7maj', [['D9', 'G6/9'], ['D13', 'G6/9'], ['D13b9', 'G6/9'], ['D7b5', 'G6/9'], ['D9b5', 'G6/9']],
             [R5, R6] * 5, 5,
             'Я вас любил’s D7 going to G, five ways: D9, D13, D13♭9, D7♭5, D9♭5, each answered by G6/9. D with the root on the A string.')))
# 5. minor 7♭5 = minor 6 with the 6th in the bass
EX.append(dict(
    id='w-m7b5', title='The minor 7♭5 as a minor 6',
    idea=('Wrembel: the minor 7♭5 is rarely meant as such; it is a minor 6 with its 6th in the bass. F♯ minor 7♭5 has the notes of A minor 6.'),
    quote=T('the two main ways to voice the minor 7♭5.', 18),
    bars=lay('w-m7b5', [['Am6', 'F#m7b5'], ['Am6', 'F#m7b5'], ['Dm6', 'Bm7b5'], ['Dm6', 'Bm7b5']], [R6, R6, R6, R6, R5, R5, R5, R5], 5,
             'Очи чёрные’s A minor 6 and then the same notes over F♯ (F♯ minor 7♭5); D minor 6 and the same over B (B minor 7♭5).',
             root_needed=[True] * 8)))
# 6. the diminished chord for the 7♭9
EX.append(dict(
    id='w-dim', title='The diminished chord for the 7♭9',
    idea=('A diminished chord is built of minor 3rds, so it repeats every three frets. Wrembel uses it most often for a 7♭9: the diminished chord a half step above the 7th chord’s root, '
          'or any of its copies a minor 3rd apart (on the 3rd, 5th and 7th of the 7th chord).'),
    quote=T('E7♭9 written as D, F and A♭ diminished in turn, each going back to A minor 6.', 19),
    bars=dims('w-dim', 4,
             'Очи чёрные’s E7 as diminished chords a half step above E and up from there by minor 3rds: A♭, B, D diminished, each going to A minor 6. '
             'Each grip is the one before moved up three frets.')))
# 7. the passing diminished chord
EX.append(dict(
    id='w-pass', title='The passing diminished chord',
    idea='Between two chords a whole step apart, the diminished chord on the note between: Wrembel’s example, C minor, C♯ diminished, D minor.',
    quote=T('C minor to D minor with C♯ diminished between.', 18),
    bars=lay('w-pass', [['Cm6', 'C#dim7'], ['Dsus4']], [R5, R5, R5], 3,
             'Я вас любил, bars 11–12: C minor (as minor 6), C♯ diminished on the way, D sus4: the bass climbs C, C♯, D.')))
# 8. clichés
EX.append(dict(
    id='w-cl-min', title='The minor line cliché',
    idea=('On a minor chord that lasts, Wrembel’s cliché: minor, minor with major 7, minor 7, minor 6, one voice falling a half step at a time from the root.'),
    quote=T('the cliché on A minor and on D minor.', 20),
    bars=cliche('w-cl-min', [5, -1, 7, 5, 5, -1], ['Am', 'Am(maj7)', 'Am7', 'Am6'], 4, -1, [2, 2],
                'Очи чёрные’s two bars of A minor: the D string falls A, G♯, G, F♯ under C and E held on the G and B strings; A on the low E string throughout.')))
EX.append(dict(
    id='w-cl-maj', title='The major cliché',
    idea='On a major chord, Wrembel’s cliché climbs: 6/9, then minor 6 a step up, minor 6 a half step higher, then the major 7 with its 3rd in the bass, into the next chord.',
    quote=T('G6/9, A minor 6, B♭ minor 6, G major 7 over B.', 20),
    bars=lay('w-cl-maj', [['G6/9', 'Am6', 'Bbm6', 'Gmaj7/B'], ['C6/9']], [R6, R6, R6, R6, R5], 3,
             'Я вас любил, bars 8–9: its G, a beat to each chord, the bass climbing G, A, B♭, B, into its C (as 6/9).')))
# 9. the harmonic march
EX.append(dict(
    id='w-march', title='The harmonic march',
    idea=('Wrembel: there is almost no II–V in gypsy jazz. A chain of 7th chords, each resolving to the next (E7, A7, D7, G7), is the “harmonic march”; '
          'where a chart has a minor II before the V, play it as a 7th (D7 rather than D minor 7 before G7).'),
    quote=T('the march E7, A7, D7, G7, practised in every key; Dm7 G7 C played as D7 G7 C.', 20),
    bars=lay('w-march', [['E9', 'A13'], ['D9', 'G6/9']], [R5, R6, R5, R6], 7,
             'In G, Я вас любил’s key: E9, A13, D9 and home to G6/9, each 7th chord resolving to the next.')))
EX.append(dict(
    id='w-march-song', title='The march in Я вас любил',
    idea='Я вас любил already marches in its bars 15–17: G, then A7 where a II–V would have A minor 7, then D7, G. Here with the march’s chords.',
    quote=T('“there is almost no II–V in gypsy jazz”.', 20),
    bars=lay('w-march-song', [['G6/9', 'A13'], ['D9'], ['G6/9']], [R6, R6, R5, R6], 3,
             'Я вас любил, bars 15–17. Your chart has A7 over C♯; here A13 with its root in the bass, as the march plays it.')))
for ex in EX:
    ex['bars'][0]['note'] = (ex['bars'][0]['note'] + ' ' + where(ex['id'])).strip()
SECTION = dict(id='gypsy-chords', title='The accompanist’s chords', part='Exercises', ex=EX)
SECTIONS = list(G0.SECTIONS)
SECTIONS.insert(1, SECTION)
