"""Tango, the right hand: the accompaniment rhythms of Julián Graciano's Método de guitarra tango (Melos, 2016),
chapter 1, pp. 11–18 of the owner's copy. Each rhythm opens with Graciano's own bar (he writes most of them as rhythm
slashes; those are played on his A minor chord from p. 13), then the same rhythm, stroke for stroke, on the chords of
Очи чёрные (its second half: D minor, A minor, E7, A minor, a bar each), closed grips around the 5th fret.

Hits: [beats, strings or '-' (a rest: everything stops) or [] (nothing new), velocity change]. Staccato is a stroke
half its written length, then a rest. The arrastre (Graciano's drag into the next downbeat) is a slide up the bass
string from three frets below, the first touch muffled."""
import sys
sys.path.insert(0, '/home/claude/studies')
from kit_study import OPEN, nn

BOOK = 'Graciano, Método de guitarra tango'
ACC, SOFT, GHOST = 0.15, -0.2, -0.3

# ---- grips (strings 6..1, index 0 = low E) ----
# bass + three notes on the D, G and B strings: Graciano's own A minor on p. 13 (A2 + A3 C4 E4) and the same family
G4 = {'Dm': [-1, 5, 7, 7, 6, -1],     # D3 A3 D4 F4: barre at the 5th fret, root on the A string
      'Am': [5, -1, 7, 5, 5, -1],     # A2 A3 C4 E4: root on the low E string, 5th fret (A string muted)
      'E7': [-1, 7, 6, 7, 5, -1],     # E3 G#3 D4 E4: root on the A string, 7th fret
      'Dm/F': [-1, 8, 7, 7, 6, -1],   # the bass moved up to F
      'Am/C': [8, -1, 7, 5, 5, -1],   # the bass moved up to C
      'E7/G#': [4, -1, 6, 7, 5, -1],  # the bass moved down to G#
      'E7/B': [7, -1, 6, 7, 5, -1],
      'G': [3, -1, 5, 4, 3, -1], 'F': [1, -1, 3, 2, 1, -1], 'E7o': [0, -1, 2, 1, 3, -1],
      'Gm7': [3, -1, 3, 3, 3, -1], 'A7': [5, -1, 5, 6, 5, -1]}
# the same with a fifth note on top (the full chord on the downbeat of the umpa-umpa), like Graciano's G7 on p. 16
G5 = {'Dm': [-1, 5, 7, 7, 6, 5], 'Am': [5, -1, 7, 5, 5, 5], 'E7': [-1, 7, 9, 7, 9, 7], 'G7': [3, -1, 3, 4, 3, 3]}
# three notes on the top strings (the yumbado's chord), with the open low strings
GY = {'Dm': [0, 0, 0, 7, 6, 5], 'Am': [0, 0, 0, 5, 5, 5], 'E7': [0, 0, 0, 7, 9, 7]}
# whole barres (Gardel's arpeggio: the same six-string order on every chord)
G6 = {'Dm': [10, 12, 12, 10, 10, 10], 'Am': [5, 7, 7, 5, 5, 5], 'E7': [0, 2, 0, 1, 0, 0]}
# bass + chord on the top three strings (Gardel's paso doble rhythm)
GT = {'Dm': [-1, 5, 7, 7, 6, 5], 'Am': [5, -1, 7, 5, 5, 5], 'E7': [-1, 7, 9, 7, 9, 7]}

OURS = ['Dm', 'Am', 'E7', 'Am']
OURS_NOTE = 'On the chords of the second half of Очи чёрные (D minor, A minor, E7, A minor), a bar each; the song gives each two.'


def strings_of(g): return [6 - i for i in range(6) if g[i] >= 0]


def roles(g):
    s = strings_of(g)
    return dict(A=s, B=s[:1], C=s[1:4] if len(s) >= 4 else s[1:], I=s[1:-1], T=[3, 2, 1], P=[2, 1], O=[6, 5, 4])


def K(name, grip, spec):
    R = roles(grip); hits = []
    for h in spec:
        d, r = h[0], h[1]
        v = h[2] if len(h) > 2 else 0
        m = '-' if r == '-' else [] if r == '~' else (list(r) if isinstance(r, (list, tuple)) else R[r])
        hits.append([d, m] + ([v] if v else []))
    assert abs(sum(x[0] for x in hits) - sum(h[0] for h in spec)) < 1e-9
    return ['K', name, grip, hits]


def st(d, r, v=0):
    """a staccato stroke: half its length, then silence"""
    return [(d / 2, r, v), (d / 2, '-')]


def bass_of(g):
    s = strings_of(g)[0]
    return s, g[6 - s]


def arr(grip, over, beats=0.5):
    """Graciano's arrastre: a drag up the bass string into the next chord's bass, from three frets below; the first
    touch muffled. In an eighth (the 'and' of the beat) or a whole beat (from the beat itself)."""
    s, f = bass_of(grip)
    assert f >= 3, ('no drag into an open or low bass', grip)
    fr = [f - 3, f - 2, f - 1]
    d = [1 / 6] * 3 if beats == 0.5 else [0.5, 0.25, 0.25]
    return ['R', [[s, x] for x in fr], d, over, {'vel': [GHOST, -0.1, -0.05]}]


def flat(*parts):
    out = []
    for p in parts:
        if isinstance(p, list): out += p
        else: out.append(p)
    return out


def describe(name, g):
    s = strings_of(g)
    names = ' '.join(nn(OPEN[6 - x] + g[6 - x]) for x in s)
    return f'{name}: {names}'


# ---------------- the rhythms ----------------
def marcatto4(c, g): return K(c, g, flat(st(1, 'A', ACC), st(1, 'I'), st(1, 'A', ACC), st(1, 'I')))
def marcatto4_v1(c, g): return K(c, g, flat(st(1, 'A', ACC), [(1, 'I')], st(1, 'A', ACC), [(1, 'I')]))
def marcatto2(c, g): return K(c, g, [(0.5, 'A', ACC), (1.5, '-'), (0.5, 'A', ACC), (1.5, '-')])
def pesante(c, g, c2=None, g2=None):
    if c2: return [K(c, g, [(1.75, 'A'), (0.25, '-')]), K(c2, g2, [(1.75, 'A'), (0.25, '-')])]
    return [K(c, g, [(1.75, 'A'), (0.25, '-'), (2, 'A')])]
def yumbado(c, g): return K(c, g, [(0.75, 'T'), (0.25, '-'), (0.75, 'O'), (0.25, '-'), (0.75, 'T'), (0.25, '-'), (0.75, 'O'), (0.25, '-')])
def yumbado_v(c, g): return K(c, g, [(0.75, 'T'), (0.25, '-'), (0.75, 'O'), (0.25, '-'), (0.5, 'T'), (0.25, 'T', SOFT), (0.25, '-'), (0.75, 'O'), (0.25, '-')])
SINC = flat([(0.5, 'B')], st(1, 'C'), [(0.5, 'B')], st(1, 'C'))
def sincopado(c, g): return K(c, g, SINC + [(1, '-')])
def sincopado_sin_bajo(c, g): return K(c, g, flat([(0.5, '-')], st(1, 'C'), [(0.5, '-')], st(1, 'C'), [(1, '-')]))
def sinc_arr(c, g, nxt, tied=False):
    first = [(0.5, 'B', GHOST)] if tied else [(0.5, 'B')]
    its = [K(c, g, first + SINC[1:] + [(0.5, '-')])]
    if nxt: its.append(arr(nxt[1], nxt[0]))
    else: its[0][3].append([0.5, '-'])
    return its
def sinc_tierra(c, g, nxt): return [K(c, g, SINC), arr(nxt[1], nxt[0], beats=1)]
def sinc_octava(c, g1, g2):
    return [K(c, g1, flat([(0.5, 'B')], st(1, 'C'))), K(c, g2, flat([(0.5, 'B')], st(1, 'C'), [(1, '-')]))]
def doble(c, g, c2=None, g2=None):
    half = flat(st(0.5, 'A', ACC), [(0.5, 'A'), (1, '-')])
    if c2: return [K(c, g, half), K(c2, g2, half)]
    return [K(c, g, half + half)]
def doble_arr(c, g, c2, g2, nxt, tied=False):
    first = [(0.5, 'B', GHOST)] if tied else st(0.5, 'A', ACC)
    half = flat(first, [(0.5, 'A'), (0.5, '-')])
    its = [K(c, g, half), arr(g2, c2), K(c2, g2, half)]
    if nxt: its.append(arr(nxt[1], nxt[0]))
    else: its[2][3].append([0.5, '-'])
    return its
def contratiempo(c, g, c2, g2): return [K(c, g, [(0.5, 'B'), (1.5, 'C')]), K(c2, g2, [(0.5, 'B'), (1.5, 'C')])]
def contratiempo_v(c, g, c2, g2): return [K(c, g, [(0.5, 'B'), (0.5, 'C'), (1, 'B')]), K(c2, g2, [(0.5, 'B'), (0.5, 'C'), (1, 'B')])]
UMPA = flat(st(1, 'A', ACC), [(0.5, 'B')], st(0.5, 'C'), [(0.5, 'B')], st(0.5, 'C'))
def umpa(c, g, nxt):
    return [K(c, g, UMPA), arr(nxt[1], nxt[0], beats=1)] if nxt else [K(c, g, UMPA + [(1, '-')])]
def umpa_8va(c, g, g8, nxt):
    its = [K(c, g, flat(st(1, 'A', ACC), [(0.5, 'B')], st(0.5, 'C'))), K(c, g8, flat([(0.5, 'B')], st(0.5, 'C')))]
    its.append(arr(nxt[1], nxt[0], beats=1) if nxt else ['W', 1])
    return its
def umpa_oct(c, g, go, nxt, muted=False):
    lo, hi = strings_of(go)
    up = [(0.12, [hi], GHOST), (0.38, '-')] if muted else st(0.5, [hi])
    its = [K(c, g, st(1, 'A', ACC)), K(c, go, flat([(0.5, [lo])], up, [(0.5, [lo])], up))]
    its.append(arr(nxt[1], nxt[0], beats=1) if nxt else ['W', 1])
    return its
def tres(c, g): return K(c, g, [(1.5, 'A', ACC), (1.5, 'A', ACC), (1, 'A', ACC)])
def tres_v1(c, g): return K(c, g, [(1, 'A', ACC), (0.5, 'B'), (1.5, 'C', ACC), (1, 'A', ACC)])
def tres_v2(c, g): return K(c, g, [(0.5, 'C', ACC), (0.5, 'B'), (0.5, 'B'), (0.5, 'C', ACC), (0.5, 'B'), (0.5, 'B'), (0.5, 'C', ACC), (0.5, 'B')])
def tres_v2i(c, g): return K(c, g, [(0.5, 'B', ACC), (0.5, 'C'), (0.5, 'C'), (0.5, 'B', ACC), (0.5, 'C'), (0.5, 'C'), (0.5, 'B', ACC), (0.5, 'C')])
def gobbi(c1, g1, c2, g2, c3, g3):
    return [K(c1, g1, flat([(0.5, 'B')], st(1, 'C'))), K(c2, g2, flat([(0.5, 'B')], st(1, 'C'))), K(c3, g3, flat([(0.5, 'B')], st(0.5, 'C')))]
def whole(c, g): return K(c, g, [(4, 'A')])
GARDEL = flat([(0.5, [6])], st(0.5, [3, 2], ACC), st(0.5, [5]), st(0.5, [4]), st(0.5, [3]), st(0.5, [2, 1]))
def gardel(c, g, ghost=False):
    return K(c, g, GARDEL + (flat(st(1, [6], GHOST)) if ghost else [(1, '-')]))
PASO_B1 = flat(st(0.5, 'T'), [(0.25, 'P'), (0.25, 'P')])
def paso(c, g): return K(c, g, flat(PASO_B1, st(0.5, 'P'), [(0.5, 'B')], st(1, 'T'), st(1, 'T', GHOST)))
def paso_v(c, g): return K(c, g, flat(PASO_B1, st(0.5, 'P'), [(0.5, 'B')], PASO_B1, st(0.5, 'P'), [(0.5, 'B')]))


def ours(fn, grips=G4, note_extra=''):
    """the rhythm on the four chords, one bar each"""
    out = []
    for c in OURS:
        it = fn(c, grips[c])
        out.append(dict(chords=[c], items=it if isinstance(it, list) and it and isinstance(it[0], list) else [it], note=''))
    return out


def notes_for(bars, first, rest=''):
    bars[0]['note'] = first
    for b in bars[1:]: b['note'] = b['note'] or rest
    return bars


def where(p): return f'Método de guitarra tango, p. {p}'


QAM = G4['Am']                       # Graciano's own A minor (p. 13): A2 under A3 C4 E4
SLASH = 'He writes it as rhythm slashes, without notes; played here on his A minor from p. 13 (A on the low E string under A, C and E).'
RH_SINC = 'Right hand: the thumb on the bass, index, middle and ring together on the chord (or a pick, every stroke down).'
POS = ('The grips: D minor as a barre at the 5th fret with the root on the A string, A minor with the root on the low E string at the 5th fret (the A string muted), '
       'E7 with the root on the A string at the 7th fret; the three notes above the bass are always on the D, G and B strings.')

EX_M, EX_Y, EX_S, EX_D, EX_C, EX_U, EX_T, EX_G = [], [], [], [], [], [], [], []

# ---------- marcatto ----------
EX_M.append(dict(
    id='marcatto-4', title='Marcatto in four',
    idea=('Four short strokes to the bar, the 1st and 3rd accented: the whole chord on 1 and 3, only its middle notes on 2 and 4. '
          'Each stroke is cut short by easing the left hand off the strings, not by lifting it away. The ground of a tango accompaniment, good for a whole song.'),
    quote=dict(where=where(11), text='Marcatto 4: four staccato quarter notes, accents on 1 and 3. ' + SLASH, item=marcatto4('Am', QAM), whose='Graciano’s own', played='Played here: that bar.'),
    bars=notes_for(ours(marcatto4), OURS_NOTE + ' ' + POS + ' On 2 and 4 only the D and G strings sound.')))
EX_M.append(dict(
    id='marcatto-4-v1', title='Marcatto in four, the 2nd beat ringing',
    idea=('The same, but the stroke on 2 is left to ring into the 3rd (and the 4th has no staccato mark either). '
          'Graciano keeps it for a bar here and there, not for long stretches.'),
    quote=dict(where=where(11), text='Variación 1: the 2nd quarter slurred into the 3rd. ' + SLASH, item=marcatto4_v1('Am', QAM), whose='Graciano’s own', played='Played here: that bar.'),
    bars=notes_for(ours(marcatto4_v1), OURS_NOTE)))
q_decaro = [K('Gm7', G4['Gm7'], [(1, 'B'), (1, 'C', ACC)]), K('A7', G4['A7'], [(1, 'B'), (1, 'C', ACC)]),
            K('Dm', G4['Dm'], [(0.5, 'B'), (1, 'C'), (0.5, 'B'), (1, 'C'), (1, '-')])]
b_decaro = []
for _ in range(2):
    b_decaro.append(dict(chords=['Dm', 'E7'], note='', items=[K('Dm', G4['Dm'], [(1, 'B'), (1, 'C', ACC)]), K('E7', G4['E7'], [(1, 'B'), (1, 'C', ACC)])]))
    b_decaro.append(dict(chords=['Am'], note='', items=[K('Am', G4['Am'], [(0.5, 'B'), (1, 'C'), (0.5, 'B'), (1, 'C'), (1, '-')])]))
EX_M.append(dict(
    id='marcatto-de-caro', title='Marcatto with the accent on 2 and 4 (De Caro)',
    idea=('From Julio De Caro’s sextet (about 1928): the accents move to 2 and 4. The bass alone on 1 and 3, the chord (usually three notes) on 2 and 4. '
          'Best kept to one bar, on two chords of a cadence; his example lands on the next bar with the figure of the sincopado (eighth, quarter, eighth, quarter, rest), played here bass and chord as in the sincopado.'),
    quote=dict(where=where(12), text='Variación 2, on G minor 7 and A7 (two beats each), resolving to D minor: bass, chord, bass, chord, accents on the chords; then bass, chord, bass, chord, rest. He writes slashes under the chord names; the grips are ours.',
               items=q_decaro, whose='Graciano’s own', played='Played here: both bars.'),
    bars=notes_for(b_decaro, 'The same on Очи чёрные’s cadence in A minor: D minor and E7 (two beats each), resolving to A minor; twice.')))
EX_M.append(dict(
    id='marcatto-2', title='Marcatto in two',
    idea=('Two accented short strokes, on 1 and 3, and nothing on 2 and 4: more air for the singer, for melodies with long notes. '
          'Four bars at the most, then back to the four. Graciano’s advice: mark 2 and 4 with the hand in the air so the pulse stays.'),
    quote=dict(where=where(12), text='Marcatto 2: accented staccato quarters on 1 and 3, quarter rests between. ' + SLASH, item=marcatto2('Am', QAM), whose='Graciano’s own', played='Played here: that bar.'),
    bars=notes_for(ours(marcatto2), OURS_NOTE + ' The whole chord each time.')))
b_pes = [dict(chords=[c], note='', items=pesante(c, G4[c])) for c in OURS]
b_pes40 = [dict(chords=[c, c2], note='', items=pesante(c, G4[c], c2, G4[c2])) for c, c2 in (('Dm', 'Dm/F'), ('Am', 'Am/C'), ('E7', 'E7/G#'), ('Am', 'Am/C'))]
EX_M.append(dict(
    id='pesante', title='Pesante',
    idea=('Two half notes, just parted by the moment it takes to change chord; when the chord stays, ease the left hand between them. '
          'Flat and plain, it leaves the singer in front and only shows the harmony. Good for the cadence of a phrase inside a marcatto 4; for Gardel’s style it is the ground rhythm. '
          'From the 1940s on, one chord of four beats is often split in two: root position, then with its 3rd in the bass.'),
    quote=dict(where=where(12), text='Pesante: two half notes with a breath mark between them. ' + SLASH, item=pesante('Am', QAM)[0], whose='Graciano’s own', played='Played here: that bar.'),
    bars=notes_for(b_pes, OURS_NOTE + ' First as two plain halves.') + notes_for(b_pes40, 'Then the 1940s way: the second half with the 3rd in the bass. Only the bass moves: D to F on the A string (8th fret), A to C on the low E string (8th fret), E down to G♯ on the low E string (4th fret).')))

# ---------- yumbado ----------
YPOS = ('The chord on the top three strings (D minor at the 5th–7th fret, A minor across the 5th, E7 at the 7th–9th: D, G♯, B); '
        'on 2 and 4 the open low E, A and D strings together, whatever the key.')
EX_Y.append(dict(
    id='yumbado', title='Yumbado',
    idea=('Osvaldo Pugliese’s yumba, from the piano: the chord in the middle on 1 and 3, the lowest notes on 2 and 4. On the guitar the low notes are the open '
          '6th, 5th and 4th strings struck together, a “noise” like the pianist’s left hand, the same in every key. '
          'After each chord let the left hand slide down toward the nut while the right hand strikes the open strings: that delay holds the beat back, as the pianist does going down the keyboard. '
          'It adds a lot of tension; keep it for the most expressive passages.'),
    quote=dict(where=where(13), text='Yumbado, básico: chord on 1 and 3, x-notes on the open low strings on 2 and 4. ' + 'He writes the chords as slashes; played here on A minor across the 5th fret.', item=yumbado('Am', GY['Am']), whose='Graciano’s own', played='Played here: that bar.'),
    bars=notes_for(ours(yumbado, GY), OURS_NOTE + ' ' + YPOS)))
EX_Y.append(dict(
    id='yumbado-v', title='Yumbado with a light eighth',
    idea=('The same, with one more stroke on the “and” of 3, very light: an up-stroke of the pick or the index finger alone. It gives the yumba more motion; use it in some bars only.'),
    quote=dict(where=where(13), text='Variación: the 3rd beat split into two eighths. As above, on A minor.', item=yumbado_v('Am', GY['Am']), whose='Graciano’s own', played='Played here: that bar.'),
    bars=notes_for(ours(yumbado_v, GY), OURS_NOTE)))

# ---------- sincopado and the arrastre ----------
EX_S.append(dict(
    id='sincopado', title='Sincopado',
    idea=('The other ground rhythm beside the marcatto 4, with more movement, for melodies full of syncopation: the bass on the beat as an eighth, then the rest of the chord '
          'as a short quarter on the “and”; twice, then a rest on 4. ' + RH_SINC),
    quote=dict(where=where(13), text='Sincopado, written out on A minor: A on the low E string, then A, C and E short. This one has his notes.', item=sincopado('Am', QAM), whose='Graciano’s own', played='Played here: that bar.'),
    bars=notes_for(ours(sincopado), OURS_NOTE + ' ' + POS)))
EX_S.append(dict(
    id='sincopado-sin-bajo', title='Sincopado without the bass',
    idea='Now and then the bass notes are left out and only the short chords on the “and” sound, with rests where the bass was.',
    quote=dict(where=where(13), text='he gives it in words only, under the sincopado.', item=None, by='Graciano'),
    bars=notes_for(ours(sincopado_sin_bajo), OURS_NOTE)))
b_sa = []
seq = OURS + OURS
for i, c in enumerate(seq):
    nxt = (seq[i + 1], G4[seq[i + 1]]) if i + 1 < len(seq) else None
    b_sa.append(dict(chords=[c], note='', items=sinc_arr(c, G4[c], nxt, tied=(i >= 5))))
q_sa = sinc_arr('Am', QAM, ('Am', QAM)) + [K('Am', QAM, SINC + [(1, '-')])]
EX_S.append(dict(
    id='sincopado-arrastre', title='Sincopado with the arrastre',
    idea=('The sincopado with an arrastre, the tango drag, from the “and” of 4 into the next downbeat. Played here: touch the bass string three frets below, muffled (his x-note), and slide up into the next bass (his slide lines). '
          'Two ways to take the downbeat after it: strike it (first four bars), or let the slide carry it and strike only the syncopated chord (last three: the slide arrives without a new stroke). '
          'Listen to Aníbal Troilo’s orchestra for the arrastre.'),
    quote=dict(where=where(14), text='Sincopado con arrastre: an eighth rest and an x-eighth on the 4th beat, with the slide lines into the next bar. As above, on A minor; both bars.', items=q_sa, whose='Graciano’s own', played='Played here: his two bars.'),
    bars=notes_for(b_sa, OURS_NOTE + ' The slide goes into each next bass: up the A string to D (5th fret), the low E string to A (5th), the A string to E (7th).')))
b_st = []
for c, c2 in (('Dm', 'Am'), ('E7', 'Am')):
    b_st.append(dict(chords=[c], note='', items=sinc_tierra(c, G4[c], (c2, G4[c2]))))
    b_st.append(dict(chords=[c2], note='', items=[marcatto4(c2, G4[c2])]))
q_st = sinc_tierra('Am', QAM, ('Am', QAM)) + [marcatto4('Am', QAM)]
EX_S.append(dict(
    id='arrastre-tierra', title='The arrastre from the 4th beat, into the marcatto',
    idea=('The drag can also start on the 4th beat itself, a whole beat long: the way to go from a sincopado to a marcatto. Never tie it into the next downbeat; strike the 1. '
          'And sometimes there is no drag in the bass at all, only the feel of it, by playing the chord a little ahead.'),
    quote=dict(where=where(14), text='Ejemplo: sincopado, then the arrastre from the 4th beat into a bar of marcatto 4. As above, on A minor.', items=q_st, whose='Graciano’s own', played='Played here: his two bars.'),
    bars=notes_for(b_st, 'D minor into A minor, then E7 into A minor, the arrastre taking the whole 4th beat each time.')))
E7lo, E7hi = [0, 5, 6, 4, -1, -1], [-1, 7, 9, 7, 9, -1]
Amlo, Amhi = [5, 7, 7, 5, -1, -1], [-1, -1, 7, 5, 5, 5]
b_so = [dict(chords=['E7'], note='', items=sinc_octava('E7', E7lo, E7hi)), dict(chords=['E7'], note='', items=sinc_octava('E7', E7lo, E7hi)),
        dict(chords=['Am'], note='', items=sinc_octava('Am', Amlo, Amhi)), dict(chords=['Am'], note='', items=sinc_octava('Am', Amlo, Amhi))]
EX_S.append(dict(
    id='sincopado-octava', title='Sincopado with a change of octave',
    idea=('The second bass an octave up and the second chord moved up the neck with it: the top note of the first chord becomes the bottom note of the second.'),
    quote=dict(where=where(14), text='Variación, con cambio de octava, on G7: G on the low E string under F, B and D; then G an octave up under D, F and B, short.',
               items=sinc_octava('G7', [3, -1, 3, 4, 3, -1], [-1, -1, 5, 7, 6, 7]), whose='Graciano’s own', played='Played here: that bar.'),
    bars=notes_for(b_so, 'On the first phrase of Очи чёрные: E7, E7, A minor, A minor. E7: the open low E under D, G♯ and B (A, D and G strings, 4th–6th fret); then E on the A string, 7th fret, under B, D and G♯ (7th–9th fret), the same notes Graciano’s G7 uses, a minor 3rd lower.',
                   'A minor: A on the low E string, 5th fret, under E, A and C; then A on the D string, 7th fret, under C, E and A on the top three strings at the 5th.')))

# ---------- doble síncopa ----------
b_ds = [dict(chords=['Dm'], note='', items=[marcatto4('Dm', G4['Dm'])]), dict(chords=['Am'], note='', items=[marcatto4('Am', G4['Am'])]),
        dict(chords=['Dm', 'E7'], note='', items=doble('Dm', G4['Dm'], 'E7', G4['E7'])), dict(chords=['Am'], note='', items=doble('Am', G4['Am']))]
EX_D.append(dict(
    id='doble-sincopa', title='Doble síncopa',
    idea=('Two eighths and a rest, twice: the first eighth short and accented. Nothing is syncopated on paper; the syncopation is only felt. Typical of Juan D’Arienzo. '
          'Use it when the ground is a fast marcatto 4, at the cadence, with two chords to the bar.'),
    quote=dict(where=where(14), text='Doble síncopa: two eighths, a quarter rest, twice; accents on 1 and 3. ' + SLASH, item=doble('Am', QAM)[0], whose='Graciano’s own', played='Played here: that bar.'),
    bars=notes_for(b_ds, 'Two bars of marcatto 4 on D minor and A minor, then the cadence in doble síncopa: D minor and E7 (two beats each), then A minor.')))
b_dsa = []
b_dsa.append(dict(chords=['Dm', 'E7'], note='', items=doble_arr('Dm', G4['Dm'], 'E7', G4['E7'], ('Am', G4['Am']))))
b_dsa.append(dict(chords=['Am'], note='', items=doble_arr('Am', G4['Am'], 'Am', G4['Am'], ('Dm', G4['Dm']))))
b_dsa.append(dict(chords=['Dm', 'E7'], note='', items=doble_arr('Dm', G4['Dm'], 'E7', G4['E7'], ('Am', G4['Am']), tied=True)))
b_dsa.append(dict(chords=['Am'], note='', items=doble_arr('Am', G4['Am'], 'Am', G4['Am'], None, tied=True)))
EX_D.append(dict(
    id='doble-sincopa-arrastre', title='Doble síncopa with the arrastre',
    idea=('An arrastre into each pair of eighths. Two ways: strike the first eighth after the drag (first two bars), or tie the drag into it, so only the second eighth is struck (last two). '
          'The first has more attack; the second gives the syncopation more weight. Ideal for the melodic cadence, two chords to the bar; listen to Troilo.'),
    quote=dict(where=where(14), text='Doble síncopa con arrastre: the slide lines before each pair. As above, on A minor.', items=doble_arr('Am', QAM, 'Am', QAM, ('Am', QAM)), whose='Graciano’s own', played='Played here: that bar.'),
    bars=notes_for(b_dsa, 'D minor and E7, then A minor; twice.')))

# ---------- contratiempo y síncopa ----------
pairs = (('Dm', 'Dm/F'), ('Am', 'Am/C'), ('E7', 'E7/G#'), ('Am', 'Am/C'))
QAM3, QAMG = [5, -1, -1, 5, 5, 5], [3, -1, -1, 5, 5, 5]
EX_C.append(dict(
    id='contratiempo', title='Contratiempo y síncopa',
    idea=('From the sincopado, more relaxed: the bass as an eighth on the beat, the rest of the chord on the “and”, held for a dotted quarter; twice. '
          'Best with the chord in root position first, then with another bass.'),
    quote=dict(where=where(15), text='Contratiempo y síncopa, on A minor and A minor over G (slashes under the chord names; the grips are ours: A, then G, on the low E string under C, E and A at the 5th fret).',
               items=contratiempo('Am', QAM3, 'Am/G', QAMG), whose='Graciano’s own', played='Played here: that bar.'),
    bars=notes_for([dict(chords=[c, c2], note='', items=contratiempo(c, G4[c], c2, G4[c2])) for c, c2 in pairs],
                   OURS_NOTE + ' Each chord first in root position, then with its 3rd in the bass; only the bass moves (D to F, A to C, E to G♯).')))
EX_C.append(dict(
    id='contratiempo-v', title='Contratiempo with the bass on every beat',
    idea=('The bass on all four beats as quarter notes, the chord struck on the “and” of 1 and of 3 and held across the beat. The steady bass makes the off-beat clearer. '
          'Usual from the mid-1950s on.'),
    quote=dict(where=where(15), text='Variación, on A minor and A minor over G: quarter notes in the bass, the chord on the “and”, tied over the beat.',
               items=contratiempo_v('Am', QAM3, 'Am/G', QAMG), whose='Graciano’s own', played='Played here: that bar.'),
    bars=notes_for([dict(chords=[c, c2], note='', items=contratiempo_v(c, G4[c], c2, G4[c2])) for c, c2 in pairs], OURS_NOTE)))

# ---------- umpa-umpa ----------
def umpa_bars(fn, seq, grips):
    out = []
    for i, c in enumerate(seq):
        nxt = (seq[i + 1], grips[seq[i + 1]]) if i + 1 < len(seq) else None
        out.append(dict(chords=[c], note='', items=fn(c, grips[c], nxt)))
    return out
EX_U.append(dict(
    id='umpa-umpa', title='Umpa-umpa',
    idea=('Horacio Salgán’s rhythm, with Ubaldo De Lío’s guitar: chord, bass and chord, bass and chord, arrastre. The first chord accented and short; '
          'the bass and chord pairs in eighths, the chords short; the 4th beat drags into the next downbeat.'),
    quote=dict(where=where(16), text='Posibilidades de aplicación, 1 (the same bass and chord), on G7: G, F, B, D, G; then G and F–B–D twice; the x on the 4th beat with the slide lines.',
               items=umpa('G7', G5['G7'], ('G7', G5['G7'])), whose='Graciano’s own', played='Played here: that bar.'),
    bars=notes_for(umpa_bars(umpa, OURS, G5), OURS_NOTE + ' The full chord now has a fifth note on top: A on the high E for D minor and A minor; E7 is the barre at the 7th fret, root on the A string (E, B, D, G♯, B).')))
E7f = G5['E7']
b_u8 = []
seqE = ['Dm', 'Dm', 'Am', 'Am']            # Очи чёрные, the bars after the turn: D minor twice, A minor twice
hi8 = {'Dm': [-1, -1, 12, 10, 10, 10], 'Am': Amhi}
for i, c in enumerate(seqE):
    nxt = (seqE[i + 1], G5[seqE[i + 1]]) if i + 1 < len(seqE) else None
    b_u8.append(dict(chords=[c], note='', items=umpa_8va(c, G5[c], hi8[c], nxt)))
EX_U.append(dict(
    id='umpa-octava', title='Umpa-umpa, the second bass and chord an octave up',
    idea='The second bass-and-chord pair moved up an octave, as in the sincopado with a change of octave.',
    quote=dict(where=where(16), text='Posibilidades, 2, on G7: the second pair is G an octave up and D, F, B.', items=umpa_8va('G7', G5['G7'], [-1, -1, 5, 7, 6, 7], ('G7', G5['G7'])), whose='Graciano’s own', played='Played here: that bar.'),
    bars=notes_for(b_u8, 'On D minor, D minor, A minor, A minor, as Очи чёрные goes after the turn. The pair up an octave: D on the D string, 12th fret, under F, A and D at the 10th; A on the D string, 7th fret, under C, E and A at the 5th.')))
OCT = {'Dm': [-1, -1, -1, 7, -1, 10], 'Am': [-1, -1, 7, -1, 10, -1]}
for muted in (False, True):
    b = []
    for i, c in enumerate(seqE):
        nxt = (seqE[i + 1], G5[seqE[i + 1]]) if i + 1 < len(seqE) else None
        b.append(dict(chords=[c], note='', items=umpa_oct(c, G5[c], OCT[c], nxt, muted)))
    EX_U.append(dict(
        id='umpa-muted' if muted else 'umpa-octaves', title='Umpa-umpa, a muted string' if muted else 'Umpa-umpa in octaves',
        idea=('As in octaves, but the upper note is only a click: the finger rests on the string without pressing it down.' if muted else
              'The bass-and-chord pairs replaced by an octave, broken: the low note, then the high one, short.'),
        quote=dict(where=where(16), text=('Posibilidades, 4, cuerda muteada: the upper G as an x.' if muted else 'Posibilidades, 3, on G7: G and the G above it, twice.'),
                   items=umpa_oct('G7', G5['G7'], [-1, -1, 5, -1, 8, -1], ('G7', G5['G7']), muted), whose='Graciano’s own', played='Played here: that bar.'),
        bars=notes_for(b, 'D minor, D minor, A minor, A minor. The octaves, an octave above the bass like Graciano’s: D on the G string, 7th fret, and on the high E, 10th; A on the D string, 7th fret, and on the B string, 10th.')))

# ---------- 3+3+2 ----------
EX_T.append(dict(
    id='tres-tres-dos', title='3+3+2',
    idea=('The bar of eight eighths split three, three, two: accents on the 1st, 4th and 7th eighth, the “broken bar”. Brought into tango by the De Caro brothers in the early 1930s, '
          'traditionally on the cadence at the end of a phrase, for a bar or two; in Piazzolla it is the ground of the music (Libertango keeps it from start to end).'),
    quote=dict(where=where(16), text='3+3+2: dotted quarter, dotted quarter, quarter. ' + SLASH, item=tres('Am', QAM), whose='Graciano’s own', played='Played here: that bar.'),
    bars=notes_for(ours(tres), OURS_NOTE)))
EX_T.append(dict(
    id='tres-v1', title='3+3+2, the bass on its own',
    idea='The chords keep the 3+3+2; the bass changes: a quarter on 1, a half note on 2, a quarter on 4.',
    quote=dict(where=where(17), text='Variación 1, on A minor: the chord (A, C, E) on 1, the “and” of 2 and on 4; the low A on 1, 2 and 4.', item=tres_v1('Am', QAM), whose='Graciano’s own', played='Played here: that bar.'),
    bars=notes_for(ours(tres_v1), OURS_NOTE)))
EX_T.append(dict(
    id='tres-v2', title='3+3+2 in eighths',
    idea='Every eighth struck: the chord on the 1st, 4th and 7th, accented, the bass on all the others. More dizzying; don’t overdo it. Then turned round: the bass accented on 1, 4 and 7, the chord on the others.',
    quote=dict(where=where(17), text='Variación 2, on A minor, and the same turned round (“también se lo puede invertir”).', items=[tres_v2('Am', QAM), tres_v2i('Am', QAM)], whose='Graciano’s own', played='Played here: both bars.'),
    bars=notes_for(ours(tres_v2) + ours(tres_v2i), OURS_NOTE + ' First the chord on 1, 4 and 7, then four bars turned round.')))
q_ga = gobbi('Am', [5, -1, -1, 5, 5, 5], 'G', [3, -1, -1, 4, 3, 3], 'F', [1, -1, -1, 2, 1, 1])
b_ga = [dict(chords=['Am'], note='A minor in marcatto 4, as Очи чёрные has it before E7.', items=[marcatto4('Am', G4['Am'])]),
        dict(chords=['Am', 'G', 'F'], note='The bar before E7 split 3+3+2 into A minor, G and F, each a bass on the low E string under three notes on the D, G and B strings, moving down: 5th, 3rd, 1st fret.',
             items=gobbi('Am', G4['Am'], 'G', G4['G'], 'F', G4['F'])),
        dict(chords=['E7'], note='E7: the open low E under E, G♯ and D (D string 2nd fret, G string 1st, B string 3rd), the same shape a step lower.', items=[whole('E7', G4['E7o'])])]
q_gb = gobbi('Dm', G4['Dm'], 'Am/C', [8, 7, 7, -1, 5, -1], 'E7/B', [7, 5, 6, 7, -1, -1])
b_gb = [dict(chords=['E7'], note='E7 in sincopado, as Очи чёрные has it before A minor.', items=[sincopado('E7', G4['E7'])]),
        dict(chords=['Dm', 'Am/C', 'E7/B'], note='The second E7 bar split 3+3+2 into D minor, A minor over C, E7 over B: the bass walks down D, C, B (A string 5th fret, low E 8th, low E 7th) under three notes on the D, G and B strings.',
             items=gobbi('Dm', G4['Dm'], 'Am/C', G4['Am/C'], 'E7/B', G4['E7/B'])),
        dict(chords=['Am'], note='Into A minor, the bass down to A (low E, 5th fret).', items=[whole('Am', G4['Am'])])]
EX_T.append(dict(
    id='tres-gobbi-a', title='3+3+2 on three chords: minor to the dominant',
    idea=('Alfredo Gobbi’s 3+3+2: one bar split into three different chords, each a bass eighth and a short chord. Its first use: from the minor tonic down to the dominant, '
          'I minor, VII, VI, V7, known in tango as the Andalusian cadence.'),
    quote=dict(where=where(17), text='Variación 3, a): A minor, G, F, then E. Only his first bar.', items=q_ga, whose='Graciano’s own', played='Played here: that bar.'),
    bars=b_ga))
EX_T.append(dict(
    id='tres-gobbi-b', title='3+3+2 on three chords: the dominant to minor',
    idea='Its second use: from the dominant back to the minor tonic, through IV minor, I minor with its 3rd in the bass, and V7 with its 5th in the bass.',
    quote=dict(where=where(17), text='Variación 3, b): after a bar of E7, D minor (D under A, D, F), A minor over C (C under E, A, E), E7 over B (B under D, G♯, D), then A minor. Only the bar with the three chords.', items=q_gb, whose='Graciano’s own', played='Played here: that bar.'),
    bars=b_gb))

# ---------- Gardel ----------
G6POS = ('D minor as a barre at the 10th fret, A minor at the 5th, E7 in open position (Очи чёрные’s own E7): the same six-string order every time. '
         'The rest on 4 is the time to move.')
EX_G.append(dict(
    id='gardel-arpegio', title='Gardel’s arpeggio',
    idea=('The first of the two rhythms Gardel’s guitarists brought, an arpeggio that dresses up the marcatto 4: bass; two notes together; then three single notes up the chord; '
          'two notes together at the top; a rest on 4. All short but the bass. Right hand: thumb on the bass, middle and ring on the pair, thumb on the next two notes, '
          'index on the one after, middle and ring on the top pair (with a pick, all down-strokes).'),
    quote=dict(where=where(18), text='Ritmo gardeleano, written out on A minor: A; C and E together, accented; E, A, C; E and A together; rest.', item=gardel('Am', G6['Am']), whose='Graciano’s own', played='Played here: that bar.'),
    bars=notes_for(ours(gardel, G6), OURS_NOTE + ' ' + G6POS)))
EX_G.append(dict(
    id='gardel-fantasma', title='Gardel’s arpeggio with a ghost bass',
    idea='In place of the rest, the bass again, very softly, like a ghost note.',
    quote=dict(where=where(18), text='The same bar with the low A in brackets on the 4th beat.', item=gardel('Am', G6['Am'], ghost=True), whose='Graciano’s own', played='Played here: that bar.'),
    bars=notes_for(ours(lambda c, g: gardel(c, g, True), G6), OURS_NOTE)))
EX_G.append(dict(
    id='gardel-paso-doble', title='Gardel’s paso doble rhythm',
    idea=('The second rhythm, taken from the paso doble: the chord short, then its top two notes as two sixteenths and a short eighth, the bass on the “and” of 2, '
          'then the chord short on 3 and very soft on 4.'),
    quote=dict(where=where(18), text='On A minor: C, E and A on the top three strings; E and A; the low A; the 4th beat pianissimo.', item=paso('Am', GT['Am']), whose='Graciano’s own', played='Played here: that bar.'),
    bars=notes_for(ours(paso, GT), OURS_NOTE + ' The chord on the top three strings: D, F, A (D minor), C, E, A (A minor), D, G♯, B (E7 at the 7th fret); the bass on the A string or the low E.')))
EX_G.append(dict(
    id='gardel-paso-doble-v', title='Gardel’s paso doble rhythm, twice in a bar',
    idea='The first two beats twice: chord, the two sixteenths, the short eighth, the bass. Graciano mixes it in among bars of marcatto 4.',
    quote=dict(where=where(18), text='Variación, on A minor.', item=paso_v('Am', GT['Am']), whose='Graciano’s own', played='Played here: that bar.'),
    bars=notes_for(ours(paso_v, GT), OURS_NOTE)))

# ---------- étude: Очи чёрные as a tango ----------
CHART = ['E7', 'E7', 'Am', 'Am', 'E7', 'E7', 'Am', 'Am', 'Dm', 'Dm', 'Am', 'Am', 'E7', 'E7', 'Am', 'Am']


def etude():
    b = []
    nxt = lambda i: (CHART[i + 1], G4[CHART[i + 1]])
    # 1–4: marcatto 4, the 4th bar sincopado with the arrastre into 5
    for i in range(3): b.append(dict(chords=[CHART[i]], items=[marcatto4(CHART[i], G4[CHART[i]])], note=''))
    b.append(dict(chords=['Am'], items=sinc_arr('Am', G4['Am'], nxt(3)), note=''))
    # 5–8: sincopado with the arrastre; bar 8 contratiempo, root then 3rd in the bass
    for i in range(4, 7): b.append(dict(chords=[CHART[i]], items=sinc_arr(CHART[i], G4[CHART[i]], nxt(i)), note=''))
    b.append(dict(chords=['Am', 'Am/C'], items=contratiempo('Am', G4['Am'], 'Am/C', G4['Am/C']), note=''))
    # 9–12: yumbado, the most expressive phrase
    for i in range(8, 11): b.append(dict(chords=[CHART[i]], items=[yumbado(CHART[i], GY[CHART[i]])], note=''))
    b.append(dict(chords=['Am'], items=[yumbado_v('Am', GY['Am'])], note=''))
    # 13–16: marcatto, Gobbi's 3+3+2 into the tonic, pesante, the last chord
    b.append(dict(chords=['E7'], items=[marcatto4('E7', G4['E7'])], note=''))
    b.append(dict(chords=['Dm', 'Am/C', 'E7/B'], items=gobbi('Dm', G4['Dm'], 'Am/C', G4['Am/C'], 'E7/B', G4['E7/B']), note=''))
    b.append(dict(chords=['Am', 'Am/C'], items=pesante('Am', G4['Am'], 'Am/C', G4['Am/C']), note=''))
    b.append(dict(chords=['Am'], items=[K('Am', G4['Am'], [(0.5, 'A', ACC), (3.5, '-')])], note=''))
    b[0]['note'] = ('The sixteen bars of Очи чёрные’s chorus, each bar of the song a bar of four (E7, E7, A minor, A minor; again; D minor, D minor, A minor, A minor; E7, E7, A minor, A minor), '
                    'with the rhythms chosen the way Graciano advises on p. 20: with one chord to the bar, marcatto or sincopado; the arrastre in Troilo’s manner; the yumbado for the most expressive phrase (p. 13); '
                    'two or three chords in a bar at the cadence. Bars 1–3: marcatto 4.')
    b[3]['note'] = 'Bar 4: sincopado, dragging into the second phrase.'
    b[4]['note'] = 'Bars 5–7: sincopado with the arrastre into every downbeat.'
    b[7]['note'] = 'Bar 8: contratiempo, A minor, then over C.'
    b[8]['note'] = 'Bars 9–12: yumbado, the chord on the top strings, the open low strings between; the light eighth in bar 12.'
    b[12]['note'] = 'Bar 13: back to the marcatto 4.'
    b[13]['note'] = 'Bar 14: Gobbi’s 3+3+2 in place of the second E7: D minor, A minor over C, E7 over B.'
    b[14]['note'] = 'Bar 15: pesante, A minor, then over C.'
    b[15]['note'] = 'Bar 16: one short chord, accented.'
    return b


ETUDES = [dict(id='etude-ochi', title='Очи чёрные as a tango', idea='', quote=dict(where='', text='', item=None), bars=etude())]

# a quote that ends with an arrastre drags into the first bar that follows it (ours), as the slide lines lead on to the next downbeat
for _ex in EX_M + EX_Y + EX_S + EX_D + EX_C + EX_U + EX_T + EX_G:
    _q = _ex['quote']; _its = _q.get('items') or ([_q['item']] if _q.get('item') else [])
    if _its and _its[-1][0] == 'R':
        _k = next(x for x in _ex['bars'][0]['items'] if x[0] == 'K')
        _its[-1] = arr(_k[2], _k[1], beats=sum(_its[-1][2]))
        if _q.get('item'): _q['item'] = _its[0]
        else: _q['items'] = _its

SECTIONS = [dict(id='marcatto', title='Marcatto and pesante', part='Exercises', ex=EX_M),
            dict(id='yumbado', title='Yumbado', part='Exercises', ex=EX_Y),
            dict(id='sincopado', title='Sincopado and the arrastre', part='Exercises', ex=EX_S),
            dict(id='doble', title='Doble síncopa', part='Exercises', ex=EX_D),
            dict(id='contratiempo', title='Contratiempo y síncopa', part='Exercises', ex=EX_C),
            dict(id='umpa', title='Umpa-umpa', part='Exercises', ex=EX_U),
            dict(id='tres', title='3+3+2', part='Exercises', ex=EX_T),
            dict(id='gardel', title='Gardel’s rhythms', part='Exercises', ex=EX_G),
            dict(id='etudes', title='Études', part='Études', ex=ETUDES)]
