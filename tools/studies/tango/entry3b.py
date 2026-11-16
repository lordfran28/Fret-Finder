"""Milonga, the rest of Graciano's ch. 19 (pp. 162–170): the milongueo in a major key, improvising the milongueo's bass,
the contemporary milonga, the milonga fills, the calls (llamadas) and his plans for the four bars Im V7 V7 Im.

Same method as the tango entries since 16 Nov: his rules applied to the owner's songs, his notes quoted by a beat or
two. His examples are in A minor and A major; ours are on I Wonder Who's Kissing Her Now's C minor (Cm7, G7, the A♭7
that leans into G7) and E♭ (E♭, B♭7), felt in 2/4, so nothing of his is moved whole. The contemporary milonga goes on
Очи чёрные's D minor and E7. The plans are his combinations of the rhythms already on this page, on Очи's A minor and
E7. The calls come from milongas still under copyright and are described only. check3b.py checks the rules.
"""
import sys
sys.path.insert(0, '/home/claude/studies'); sys.path.insert(0, '/home/claude/studies/tango')
import entry3 as E3
from entry import K, arr, G4
import mel as M

OWN = 'Graciano’s own'
EX = []
RULES = []                  # for check3b
IW = 'I Wonder Who’s Kissing Her Now'
OCI = 'Очи чёрные'


def where(p): return f'Método de guitarra tango, p. {p}'


def T(text, p, notes=None, durs=None, near=3):
    d = dict(where=where(p), text=text, whose=OWN, played='', by='Graciano')
    if notes: d['items'] = [M.run(notes, durs, 'his notes', near=near)]
    else: d['item'] = None
    return d


def R(notes, pos, durs, label): return M.placed(notes, pos, durs, label)


def bar(chord, items, note=''): return dict(chords=[chord] if isinstance(chord, str) else chord, items=items, note=note)


# ---------------------------------------------------------------- improvising the milongueo's bass (pp. 162–163)
R332 = [0.75, 0.75, 0.5]           # dotted eighth, sixteenth tied to an eighth, eighth: 3+3+2 sixteenths
P = {'C3': (5, 3), 'Ab3': (4, 6), 'G3': (4, 5), 'F3': (4, 3), 'Eb3': (5, 6), 'D3': (5, 5), 'G2': (6, 3), 'A2': (6, 5), 'B2': (5, 2),
     'Eb4': (2, 4), 'C4': (3, 5), 'D4': (2, 3), 'B3': (3, 4), 'G4': (1, 3), 'Bb3': (3, 3), 'Bb2': (6, 6), 'F4': (2, 6), 'D4b': (3, 7),
     'C3b': (6, 8), 'G4b': (2, 8), 'Eb4b': (3, 8), 'C4b': (3, 5)}


def pos(ns): return [P[n] for n in ns]


def bass_only(chord, ns, label, why):
    RULES.append(('bass', chord, ns, why))
    return R(ns, pos(ns), R332, label)


def milongueo(chord, bass, ups, why, ppos=None):
    """bass on the 1st, 4th and 7th sixteenth; the upper pair (ups[0], ups[1]) after the first two bass notes, ups[2] after the last"""
    a, b, c = ups
    ns = [bass[0], a, b, bass[1], a, b, bass[2], c]
    names = [n.rstrip('b') if n.endswith(('4b', '3b')) else n for n in ns]
    RULES.append(('milongueo', chord, [n for n in names], why))
    return R(names, ppos or pos(ns), [0.25] * 8, 'over ' + M.dname(chord))


EX.append(dict(
    id='bajo-332', title='Improvising the milongueo’s bass: the bass alone',
    idea=('Graciano’s way to a milongueo of your own: first the bass alone, keeping the 3+3+2 lengths (a dotted eighth, a sixteenth tied to an eighth, an eighth). '
          'Start from the basic idea, root, ♭6, 5 on a minor chord and root, ♭2, root on its dominant; then let the bass walk on by step through the scale: down the minor '
          'scale on the minor chord, up the melodic minor on the dominant (the scale for each chord is the one his melody chapter gives).'),
    quote=T('On A minor, the basic idea: A, F, E. Then the scale by step, and the same on E7: E, F, E, then up by step.', 162, ['A2', 'F3', 'E3'], R332),
    bars=[bar('Cm7', [bass_only('Cm7', ['C3', 'Ab3', 'G3'], 'the bass', 'minor 1 b6 5')], f'{IW}’s C minor (bars 5–6), felt in 2/4. C minor: C, A♭, G (root, ♭6, 5).'),
          bar('Cm7', [bass_only('Cm7', ['F3', 'Eb3', 'D3'], 'the bass', 'minor step down')], 'Then on down the minor scale by step: F, E♭, D.'),
          bar('G7', [bass_only('G7', ['G2', 'Ab3', 'G3'], 'the bass', 'dominant 1 b2 1')], 'G7: G, A♭, G (root, ♭2, root).'),
          bar('G7', [bass_only('G7', ['G2', 'A2', 'B2'], 'the bass', 'dominant melodic up')], 'Then up C melodic minor from G: G, A, B.')]))

EX.append(dict(
    id='milongueo-menor', title='The milongueo filled with the chord’s notes',
    idea=('Last, fill the sixteenths between the bass notes with the chord’s notes: its 3rd and root above the bass. On the dominant’s second bar the filling over the '
          'step of the bass makes a passing chord, the dominant, the half-diminished on the 6th degree and the dominant with its 3rd in the bass: Graciano keeps that '
          'cadence rather than the dominant’s own notes, because it is how it is usually played.'),
    quote=T('The whole milongueo on A minor and E7, the bass as above with the chord’s notes between (no sound here: his first bar is already on this page).', 163),
    bars=[bar('Cm7', [milongueo('Cm7', ['C3', 'Ab3', 'G3'], ['Eb4', 'C4', 'Eb4'], 'minor 1 b6 5')], f'{IW}’s C minor. Bass C, A♭, G; above, E♭ and C.'),
          bar('Cm7', [milongueo('Cm7', ['F3', 'Eb3', 'D3'], ['Eb4', 'C4', 'Eb4'], 'minor step down')], 'Bass F, E♭, D under the same E♭ and C.'),
          bar('G7', [milongueo('G7', ['G2', 'Ab3', 'G3'], ['D4', 'B3', 'D4'], 'dominant 1 b2 1')], 'G7: bass G, A♭, G; above, D and B.'),
          bar('G7', [R(['G2', 'D4', 'B3', 'A2', 'Eb4', 'C4', 'B2', 'D4'], [(6, 3), (2, 3), (3, 4), (6, 5), (2, 4), (3, 5), (5, 2), (2, 3)], [0.25] * 8, 'over G7')],
              'Bass G, A, B; over the A the filling is E♭ and C (A half-diminished, the 6th degree of C minor), then D over B: G7 with its 3rd in the bass.')]))
RULES.append(('milongueo-aø', 'G7', ['G2', 'D4', 'B3', 'A2', 'Eb4', 'C4', 'B2', 'D4'], 'dominant melodic up'))

EX.append(dict(
    id='milongueo-mayor', title='The milongueo in a major key',
    idea=('The milongueo works in major too, I to V7: on the major chord the bass goes root, 6, 5, then down the major scale by step; on the dominant root, 2, root, '
          'then up by step, with the 6th-degree chord over the second step.'),
    quote=T('On A major: A, then C♯ and A above, F♯, C♯ and A, E, C♯.', 163, ['A2', 'C#4', 'A3', 'F#3', 'C#4', 'A3', 'E3', 'C#4'], [0.25] * 8),
    bars=[bar('Eb', [milongueo('Eb', ['Eb3', 'C4b', 'Bb3'], ['G4', 'Eb4', 'G4'], 'major 1 6 5', ppos=[(5, 6), (1, 3), (2, 4), (3, 5), (1, 3), (2, 4), (3, 3), (1, 3)])],
              f'{IW}, bars 1–2 in 2/4. E♭: bass E♭, C, B♭ (root, 6, 5); above, G and E♭.'),
          bar('Eb', [milongueo('Eb', ['Ab3', 'G3', 'F3'], ['G4', 'Eb4', 'G4'], 'major step down', ppos=[(4, 6), (1, 3), (2, 4), (4, 5), (1, 3), (2, 4), (4, 3), (1, 3)])],
              'Bass A♭, G, F, down the scale.'),
          bar('Bb7', [milongueo('Bb7', ['Bb2', 'C4b', 'Bb3'], ['F4', 'D4b', 'F4'], 'major dominant 1 2 1', ppos=[(6, 6), (2, 6), (3, 7), (3, 5), (2, 6), (3, 7), (4, 8), (2, 6)])],
              'B♭7: bass B♭, C, B♭ (root, 2, root); above, F and D.'),
          bar('Bb7', [R(['Bb2', 'F4', 'D4', 'C3', 'G4', 'Eb4', 'D3', 'F4'], [(6, 6), (2, 6), (3, 7), (6, 8), (2, 8), (3, 8), (5, 5), (2, 6)], [0.25] * 8, 'over B♭7')],
              'Bass B♭, C, D; over the C, G and E♭ (C minor 7, the 6th degree), then F over D: B♭7 with its 3rd in the bass.')]))
RULES.append(('milongueo-vi', 'Bb7', ['Bb2', 'F4', 'D4', 'C3', 'G4', 'Eb4', 'D3', 'F4'], 'major dominant up'))

# ---------------------------------------------------------------- the contemporary milonga (pp. 163–164), in 4/4
CR = [1.5, 0.5, 1.0, 1.0]           # dotted quarter, eighth, quarter, quarter
EX.append(dict(
    id='contemporanea-bajo', title='The contemporary milonga: the bass',
    idea=('Rovira and Piazzolla took the slow southern milonga into their writing in the 1960s and 70s: the milongueo’s sixteenths become eighths, the bar is written in 4/4, '
          'and the bass plays a dotted quarter, an eighth and two quarters. Two ways on a chord: the root three times then the 5th below, or root, 3rd, 5th, then the 5th below. '
          '(Milonga del ángel, Oblivion and the others he names are under copyright; nothing of them here.) Keep this style to pieces of its kind; do not mix it with the older rhythms.'),
    quote=T('The rhythm in slashes, then on A minor: A, A, A, E.', 163, ['A2', 'A2'], [1.5, 0.5]),
    bars=[bar('Dm', [M.run(['D3', 'D3', 'D3', 'A2'], CR, 'the bass', near=5)], f'{OCI}, bar 9: D minor. D, D, D, then A below.'),
          bar('E7', [M.run(['E3', 'E3', 'E3', 'B2'], CR, 'the bass', near=5)], 'Bar 13: E7. E, E, E, then B below.'),
          bar('Dm', [M.run(['D3', 'F3', 'A3', 'A2'], CR, 'the bass', near=5)], 'D minor the other way: D, F, A, then A below.'),
          bar('E7', [M.run(['E3', 'G#3', 'B3', 'B2'], CR, 'the bass', near=5)], 'E7: E, G♯, B, then B below.')]))
RULES += [('cbass1', 'Dm', ['D3', 'D3', 'D3', 'A2']), ('cbass1', 'E7', ['E3', 'E3', 'E3', 'B2']), ('cbass2', 'Dm', ['D3', 'F3', 'A3', 'A2']), ('cbass2', 'E7', ['E3', 'G#3', 'B3', 'B2'])]

EX.append(dict(
    id='contemporanea-guitarra', title='The contemporary milonga: the guitar over it',
    idea=('While the bass plays that line, the guitar climbs the chord in four eighths, the bass note and three of the chord’s notes, and holds the top one through the bar.'),
    quote=T('On A minor: A, C, A, C held.', 164, ['A2', 'C3', 'A3', 'C4'], [0.5] * 4),
    bars=[bar('Dm', [M.run(['D3', 'A3', 'D4', 'F4'], [0.5, 0.5, 0.5, 2.5], 'over Dm', near=5)], f'{OCI}, bars 9–10: D minor, root, 5th, octave, 3rd held.'),
          bar('Dm', [M.run(['D3', 'F3', 'A3', 'D4'], [0.5, 0.5, 0.5, 2.5], 'over Dm', near=5)], 'D minor again: root, 3rd, 5th, octave held.'),
          bar('E7', [M.run(['E3', 'B3', 'E4', 'G#4'], [0.5, 0.5, 0.5, 2.5], 'over E7', near=7)], 'Bars 13–14: E7, root, 5th, octave, 3rd held.'),
          bar('E7', [M.run(['E3', 'B3', 'D4', 'G#4'], [0.5, 0.5, 0.5, 2.5], 'over E7', near=7)], 'E7 again: root, 5th, 7th, 3rd held.')]))
RULES += [('cgtr', 'Dm', ['D3', 'A3', 'D4', 'F4']), ('cgtr', 'Dm', ['D3', 'F3', 'A3', 'D4']), ('cgtr', 'E7', ['E3', 'B3', 'E4', 'G#4']), ('cgtr', 'E7', ['E3', 'B3', 'D4', 'G#4'])]

# ---------------------------------------------------------------- fills (pp. 164–166)
FP = {'F3': (4, 3), 'Ab4': (1, 4), 'Eb3': (5, 6), 'G4': (1, 3), 'D3': (5, 5), 'F4': (2, 6), 'C3': (5, 3), 'Eb4': (2, 4),
      'Bb2': (6, 6), 'D4': (3, 7), 'Ab2': (6, 4), 'C4': (3, 5), 'G2': (6, 3), 'B3': (3, 4)}


def broken(pairs, last, label):
    """dyads broken low-high in sixteenths, then the last dyad landing: its low note a sixteenth, its high note held to the bar's end"""
    ns, ds, ps = [], [], []
    for lo, hi in pairs:
        ns += [lo, hi]; ds += [0.25, 0.25]
    lo, hi = last
    return ns, ds, (lo, hi)


def fill(id_, title, idea, quote, first, second, pairs1, land, chords, notes, pos_):
    a = []
    for lo, hi in pairs1: a += [lo, hi]
    RULES.append((id_, chords, pairs1 + [land]))
    pa = [pos_[n] for n in a]
    EX.append(dict(id=id_, title=title, idea=idea, quote=quote,
                   bars=[bar(chords[0], [R(a, pa, [0.25] * 8, 'over ' + M.dname(chords[0]))], notes[0]),
                         bar(chords[1], [R(list(land), [pos_[land[0]], pos_[land[1]]], [0.25, 1.75], 'over ' + M.dname(chords[1]))], notes[1])]))


fill('decimas-v-i', 'Fill: from the dominant to the minor tonic in 10ths',
     ('Two voices a 10th apart, broken low then high in sixteenths, stepping down the minor scale from the dominant’s 7th to the tonic chord. '
      'Every fill here can also be played in a freer rhythm Graciano gives (dotted figures across the bar), for another kind of phrasing.'),
     T('From E7 to A minor, the voices D and F first.', 164, ['D3', 'F4', 'D3', 'F4'], [0.25] * 4),
     None, None, [('F3', 'Ab4'), ('F3', 'Ab4'), ('Eb3', 'G4'), ('D3', 'F4')], ('C3', 'Eb4'), ['G7', 'Cm7'],
     [f'{IW}’s G7 into C minor (bars 18–19, in 2/4): F and A♭ (its 7th and ♭9), E♭ and G, D and F…', '…landing on C and E♭.'],
     {**FP, 'D3': (5, 5), 'F4': (2, 6)})
fill('decimas-i-v', 'Fill: from the minor tonic to the dominant in 10ths',
     'The same the other way: from the tonic’s root and 3rd down the scale in 10ths to the dominant.',
     T('From A minor to E7, the voices A and C first.', 164, ['A2', 'C4', 'A2', 'C4'], [0.25] * 4),
     None, None, [('C3', 'Eb4'), ('C3', 'Eb4'), ('Bb2', 'D4'), ('Ab2', 'C4')], ('G2', 'B3'), ['Cm7', 'G7'],
     [f'{IW}’s C minor into G7 (bars 5–6, in 2/4): C and E♭, B♭ and D, A♭ and C…', '…landing on G and B.'], FP)
SX = {'B3': (3, 4), 'G4': (1, 3), 'C4': (3, 5), 'A4': (1, 5), 'D4': (3, 7), 'B4': (1, 7), 'Eb4': (3, 8), 'C5': (1, 8), 'Bb4': (1, 6), 'Ab4': (1, 4)}
fill('sextas-v-i', 'Fill: from the dominant to the minor tonic in 6ths',
     'Two voices a 6th apart on the 3rd and 1st strings, climbing the melodic minor from the dominant’s 3rd to the tonic.',
     T('From E7 to A minor, from G♯ and E.', 164, ['G#3', 'E4', 'G#3', 'E4'], [0.25] * 4),
     None, None, [('B3', 'G4'), ('B3', 'G4'), ('C4', 'A4'), ('D4', 'B4')], ('Eb4', 'C5'), ['G7', 'Cm7'],
     [f'{IW}’s G7 into C minor: B and G, C and A, D and B…', '…landing on E♭ and C.'], SX)
fill('sextas-i-v', 'Fill: from the minor tonic to the dominant in 6ths',
     'In 6ths the other way, down the scale from the tonic to the dominant.',
     T('From A minor to E7, from C and A.', 165, ['C4', 'A4', 'C4', 'A4'], [0.25] * 4),
     None, None, [('Eb4', 'C5'), ('Eb4', 'C5'), ('D4', 'Bb4'), ('C4', 'Ab4')], ('B3', 'G4'), ['Cm7', 'G7'],
     [f'{IW}’s C minor into G7: E♭ and C, D and B♭, C and A♭…', '…landing on B and G.'], SX)

GM_IW = {'Cm7': [8, -1, 10, 8, 8, 8], 'G7': [-1, 10, 12, 10, 12, 10], 'Ab7': [-1, 11, 13, 11, 13, 11]}   # closed grips as in the rhythms above
CRO = ['G4', 'F#4', 'G4', 'Bb4', 'A4', 'Ab4', 'F4']
RULES.append(('cromatico', ['Cm7', 'G7'], CRO))
EX.append(dict(
    id='relleno-cromatico', title='Fill: a chromatic melody',
    idea=('A short line that works from the tonic to the dominant or back: the note the two chords share, turned round its lower semitone, then a fall by semitones from the '
          'tonic’s 7th that ends on the dominant’s 7th. Then the next chord in the milonga rhythm. Played to end a piece, the line goes on to the tonic, high, and a deep bass.'),
    quote=T('From A minor to E7: E, D♯, E, then G, F♯, F, D.', 165, ['E4', 'D#4', 'E4', 'G4', 'F#4', 'F4', 'D4'], [0.25] * 7),
    bars=[bar('Cm7', [['W', 0.25], M.run(CRO, [0.25] * 7, 'over Cm7', near=4)], f'{IW}’s C minor into G7: G (shared by both chords), F♯, G, then B♭, A, A♭, F.'),
          bar('G7', E3.basic('G7', g=GM_IW['G7']), 'G7 in the milonga rhythm.')]))

CL = [-1, 10, 9, 11, 8, -1]          # G3 B3 F♯4 G4: the 7th left out, the cluster F♯–G on top
RULES.append(('cluster', 'G7', CL))
EX.append(dict(
    id='clusters', title='Fill: clusters on the dominant',
    idea=('A minor 2nd struck as a cluster on the dominant, best between the chord’s root and the semitone below it. With the root on the 5th string, leave out the chord’s 7th '
          'and put the cluster on top. Graciano also plays it over an open-string bass.'),
    quote=T('On E7: D♯ and E together over the low E (no sound here: described only).', 165),
    bars=[bar('G7', E3.basic('G7', g=CL), f'{IW}’s G7: G and B below, F♯ and G together on top, in the milonga rhythm.'),
          bar('Cm7', E3.basic('Cm7', g=GM_IW['Cm7']), 'Into C minor.')]))

EX.append(dict(
    id='apoyatura-bvi7', title='Fill: the ♭VI7 leaning on the dominant',
    idea=('Before the dominant, the dominant 7th a semitone above it (♭VI7 of the key) for a moment: a harmonic appoggiatura. Graciano also harmonizes a short melody in chords '
          'from the dominant to the tonic and back; the idea is the same, the chords moving with the tune.'),
    quote=T('A minor, F7 for the second half of the bar, then E7, in the milonga rhythm (slashes).', 166),
    bars=[bar(['Cm7', 'Ab7'], [K('Cm7', GM_IW['Cm7'], [(0.5, E3.U(GM_IW['Cm7'])), (0.25, '-'), (0.25, E3.B(GM_IW['Cm7']))]),
                               K('Ab7', GM_IW['Ab7'], [(0.25, E3.U(GM_IW['Ab7'])), (0.25, '-'), (0.5, E3.B(GM_IW['Ab7']))])],
              f'{IW}, bars 21–23 in 2/4: C minor, then A♭7 for the second beat…'),
          bar('G7', E3.basic('G7', g=GM_IW['G7']), '…falling a semitone to G7.'),
          bar('Cm7', E3.basic('Cm7', g=GM_IW['Cm7']), 'C minor.')]))
RULES.append(('bvi7', 'Ab7', 'G7'))

# ---------------------------------------------------------------- his plans for Im V7 V7 Im (pp. 168–169)
SQ = ['Am', 'E7', 'E7', 'Am']


def rhythm_bar(name, c, nxt):
    if name == 'básico': return E3.basic(c)
    if name == 'variación 1': return E3.basic(c, drag=nxt)
    if name == 'variación 2': return E3.octava(c)
    if name == 'variación 3': return E3.octava(c, drag=nxt)
    if name == 'contratiempo': return E3.contra(c)
    if name == 'candombe': return E3.candombe(c)
    if name == 'pesante': return [E3.pesante(c, G4[c]), E3.pesante(c, G4[c])]
    if name == 'milongueo': return [E3.milongueo(c, E3.MIL[c])]
    raise ValueError(name)


PLANS = {'a': ['básico', 'básico', 'contratiempo', 'básico'], 'b': ['básico', 'variación 1', 'contratiempo', 'variación 1'],
         'c': ['básico', 'variación 2', 'variación 2', 'básico'], 'd': ['variación 2', 'variación 3', 'contratiempo', 'básico'],
         'e': ['variación 2', 'variación 2', 'candombe', 'básico'], 'f': ['básico', 'pesante', 'pesante', 'básico'],
         'g': ['básico', 'básico', 'milongueo', 'milongueo']}
PL_BARS = []
for k, plan in PLANS.items():
    for i, (name, c) in enumerate(zip(plan, SQ)):
        nxt = SQ[(i + 1) % 4]
        PL_BARS.append(bar(c, rhythm_bar(name, c, nxt), (f'Plan {k}: ' + ', '.join(plan) + '.') if i == 0 else ''))
ETUDE = [dict(id='planes', title='The four bars Im V7 V7 Im, his seven plans',
              idea=('Graciano’s study plan for the traditional milonga: a common harmonic module, minor tonic, dominant, dominant, minor tonic, played over and over with the '
                    'rhythms in his combinations (básico, the two variations with and without the drag, off the beat, candombe, pesante, milongueo). Then the same four bars '
                    'with a fill in place of one or two bars (his four plans: a fill in bar 3, in bar 1, in bar 2, in bars 1 and 3), using the fills you like best. '
                    'Worked this way, the module gives control of the traditional style. He also recommends knowing the traditional milonga introductions, which he calls '
                    'llamadas (calls): melodic openings that also link one time round the form to the next and can be swapped between pieces. His examples come from milongas '
                    'still under copyright (Milonga que peina canas, Tortazos, Milonga del 900, Milonga sentimental, Payadora, Milonga de mis amores), so they are not written '
                    'out here; he asks for them to be fingered without open strings, moved to other keys, and turned from minor to major and back.'),
              quote=T('The module and the plans as a table of names (no sound here).', 168),
              bars=PL_BARS)]
for b in ETUDE[0]['bars']:
    b['note'] = b['note'] or ''
ETUDE[0]['bars'][0]['note'] = f'{OCI}’s A minor and E7, in 2/4, with the grips of the rhythms above. ' + ETUDE[0]['bars'][0]['note']

E3.SECTIONS[0]['ex'] += []      # the first part stays as it was
SECTIONS = E3.SECTIONS + [dict(id='milonga2', title='Milongueo, contemporary milonga and fills', part='Exercises', ex=EX),
                          dict(id='planes', title='Études', part='Études', ex=ETUDE)]

from quotes import trim as _trim_quotes
_trim_quotes(SECTIONS[1:])
