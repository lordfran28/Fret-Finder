"""Vals, the rest of Graciano's ch. 20 (pp. 175–179): the fills (rellenos) 2–8, his plans for Im Im V7 V7 V7 V7 Im Im,
the 6/8 laid over the waltz (eight ways), and the tango valseado.

Same method as the tango entries since 16 Nov: his rules applied to the owner's songs, never his notes moved whole.
His examples are in A major, A minor and on E7; ours are on Я вас любил (G major, its D7, and E minor with B7 from its
pre-chorus) and, for the tango valseado, Очи чёрные in its own 3/4. Fills 5–8 are described only (block-chord fills
read too uncertainly from his page to be set without guessing). check4b.py checks every rule.
"""
import sys
sys.path.insert(0, '/home/claude/studies'); sys.path.insert(0, '/home/claude/studies/tango')
import entry4 as E4
from entry import K, ACC, G4
import mel as M

OWN = 'Graciano’s own'
YVL = 'Я вас любил'
OCI = 'Очи чёрные'
RULES = []
E6 = [0.5] * 6


def where(p): return f'Método de guitarra tango, p. {p}'


def T(text, p, notes=None, durs=None, near=3):
    d = dict(where=where(p), text=text, whose=OWN, played='', by='Graciano')
    if notes: d['items'] = [M.run(notes, durs, 'his notes', near=near)]
    else: d['item'] = None
    return d


def bar(c, items, note=''): return dict(chords=[c] if isinstance(c, str) else c, items=items, note=note)


def run(ns, durs, label, near=4, vel=None):
    it = M.run(ns, durs, label, near=near)
    if vel: it.append({'vel': vel})
    return it


GR = dict(E4.YV, Em=[-1, 7, 9, 9, 8, 7], B7=[-1, 2, 4, 2, 4, 2])      # E minor at the 7th fret, B7 at the 2nd: the pre-chorus

# ================================================================ fills 2–4 (p. 175)
FILLS = []


def triad_up(chord, root_note, n=6):
    tones = [p for p, d in M.chord_tones(chord) if d in ('1', '3', 'b3', '5')]
    out, cur = [root_note], M.midi(root_note)
    seq = [p for p in tones]
    k = 0
    while len(out) < n:
        k += 1
        p = seq[k % 3]
        m = cur + 1
        while M.midi(p + '4') % 12 != m % 12: m += 1
        o = (m - M.midi(p + '0')) // 12
        out.append(p + str(o)); cur = m
    return out


g_up = triad_up('G', 'G2'); e_up = triad_up('Em', 'E3')
FILLS.append(dict(
    id='vals-final-doble', title='Fill: to end, in double time',
    idea='To end a vals: the tonic chord climbed in eighths, root, 3rd, 5th and on, two octaves of it, landing on the root at the top; then silence.',
    quote=T('In A major: A, C♯, E, A, C♯, E, then the high A. The same in A minor.', 175, ['A2', 'C#3', 'E3', 'A3'], [0.5] * 4),
    bars=[bar('G', [run(g_up, E6, 'over G', near=3)], f'{YVL}’s G: G, B, D up two octaves…'),
          bar('G', [run(['G4'], [1.0], 'over G', near=3), ['W', 2.0]], '…to G at the top, and silence.'),
          bar('Em', [run(e_up, E6, 'over Em', near=7)], 'In minor, on its E minor: E, G, B…'),
          bar('Em', [run(['E5'], [1.0], 'over Em', near=7), ['W', 2.0]], '…to the top E.')]))
RULES += [('triad', 'G', g_up + ['G4']), ('triad', 'Em', e_up + ['E5'])]

g_ch = M.midi('G4')
desc_g = ['G4', 'F#4', 'F4', 'E4', 'Eb4', 'D4']
desc_e = ['E5', 'D#5', 'D5', 'C#5', 'C5', 'B4']
FILLS.append(dict(
    id='vals-arpegio-cromatismo', title='Fill: up the chord, down by semitones',
    idea='The tonic chord climbed in eighths, then from its root at the top down by semitones to its 5th, which is the root of the dominant: into the dominant in the waltz rhythm.',
    quote=T('A major (and A minor): up the chord, then A, G♯, G, F♯, F, E into E7 (no sound here: its first bar is the fill above).', 175),
    bars=[bar('G', [run(g_up, E6, 'over G', near=3)], f'{YVL}’s G: up the chord…'),
          bar('G', [run(desc_g, E6, 'over G', near=3)], '…then G, F♯, F, E, E♭, D by semitones…'),
          bar('D7', [E4.basico('D7', GR['D7'])], '…into D7, the basic waltz rhythm.'),
          bar('Em', [run(e_up, E6, 'over Em', near=7)], 'In E minor: up the chord…'),
          bar('Em', [run(desc_e, E6, 'over Em', near=7)], '…E, D♯, D, C♯, C, B…'),
          bar('B7', [E4.basico('B7', GR['B7'])], '…into B7.')]))
RULES += [('chromdown', 'G', desc_g), ('chromdown', 'Em', desc_e)]


def interleave(chord, start, n_pairs=6):
    seq = triad_up(chord, start, n_pairs + 2)
    out = []
    for k in range(n_pairs): out += [seq[k], seq[k + 2]]
    return out


g_int = interleave('G', 'G2'); e_int = interleave('Em', 'E3')
FILLS.append(dict(
    id='vals-arpegio-alternado', title='Fill: the chord in an interleaved order',
    idea='The chord’s notes in rising order, each played with the chord note two places above it: root and 5th, 3rd and root, 5th and 3rd, and on up.',
    quote=T('On A major: A, E, C♯, A, E, C♯, …', 175, ['A2', 'E3', 'C#3', 'A3'], [0.5] * 4),
    bars=[bar('G', [run(g_int[:6], E6, 'over G', near=3)], f'{YVL}’s G: G and D, B and G, D and B…'),
          bar('G', [run(g_int[6:], E6, 'over G', near=3)], '…on up.'),
          bar('Em', [run(e_int[:6], E6, 'over Em', near=7)], 'E minor: E and B, G and E, B and G…'),
          bar('Em', [run(e_int[6:], E6, 'over Em', near=9)], '…on up.')]))
RULES += [('interleave', 'G', g_int), ('interleave', 'Em', e_int)]

EB7 = [-1, 6, 8, 6, 8, 6]            # E♭7 from the A string at the 6th fret
FILLS.append(dict(
    id='vals-acorde-cromatico', title='Fill: the chromatic dominant',
    idea=('On the last beat before the dominant, the dominant 7th a semitone above it, which then slides down onto the dominant. Graciano notes it works for the main '
          'dominant in major or minor and for every secondary dominant. His other waltz fills are in chords too: a melody in eighths with a chord struck under its '
          'strong notes, and runs of block chords into the dominant (for a half cadence) and from V7 to the major tonic; they are described here, not written out.'),
    quote=T('A major: A in the bass, the chord, then F7 on the third beat; E7 in the next bar.', 176),
    bars=[bar(['G', 'Eb7'], [K('G', GR['G'], [(1.0, [6]), (1.0, [4, 3, 2])]), K('Eb7', EB7, [(1.0, [4, 3, 2])])],
              f'{YVL}’s G: the bass, the chord, then E♭7 on the third beat, a semitone above D7…'),
          bar('D7', [E4.basico('D7', GR['D7'])], '…sliding down into D7.'),
          bar('G', [E4.basico('G', GR['G'])], 'G.')]))
RULES += [('chromdom', 'Eb7', 'D7')]

# ================================================================ the 6/8 over the waltz (pp. 176–178)
VEL = [ACC, 0, 0, ACC, 0, 0]
D7B = [5, 5, 7, 5, 7, 5]             # D7 barred at the 5th with A on the low E string: A2 D3 A3 C4 F♯4 A4
D7L = [-1, 5, 4, 5, 3, -1]           # D7 low: D3 F♯3 C4 D4
D7C = [5, 5, -1, 6, 3, -1]           # A2 D3 C♯4 D4: root and major 7th as a cluster on top


def way(id_, title, idea, b1, b2, txts, quote_text, p=177):
    RULES.append(('68', id_, b1, b2))
    return dict(id=id_, title=title, idea=idea, quote=T(quote_text, p),
                bars=[bar('D7', [b1], txts[0]), bar('D7', [b2], txts[1]), bar('G', [E4.basico('G', GR['G'])], 'Home to G in the waltz rhythm.')])


SIX = 'Six eighths in the bar, accented on the 1st and the 4th, so the waltz’s three beats are heard as two of 6/8. '
WAYS = [
    way('68-arpegio', 'In 6/8: the chord as an arpeggio', SIX + 'The accented notes are the bass, and each is a note of the chord.',
        run(['D3', 'A3', 'C4', 'F#2', 'A3', 'C4'], E6, 'over D7', 3, VEL), run(['A2', 'F#3', 'C4', 'C3', 'F#3', 'A3'], E6, 'over D7', 3, VEL),
        [f'{YVL}’s D7 going home (as at the end of its chorus), two bars: D, then F♯ in the bass…', '…then A and C in the bass.'],
        'Over Am, E7, E7, Am: the E7 bars arpeggiated, the bass notes accented.'),
    way('68-diatonico', 'In 6/8: a bass walking down the scale', SIX + 'The bass, on the accents, walks down the scale; the chord’s 5th and 3rd above it.',
        run(['D3', 'A3', 'F#3', 'C3', 'A3', 'F#3'], E6, 'over D7', 3, VEL), run(['B2', 'A3', 'F#3', 'A2', 'A3', 'F#3'], E6, 'over D7', 3, VEL),
        ['D7: the bass D, C…', '…B, A, then G.'], 'Over E7, the bass E, D, C, B on the accents.'),
    way('68-cromatico', 'In 6/8: a chromatic bass', SIX + 'The bass climbs by semitones on the accents; the chord’s 5th and 7th above it.',
        run(['D3', 'A3', 'C4', 'D#3', 'A3', 'C4'], E6, 'over D7', 3, VEL), run(['E3', 'A3', 'C4', 'F3', 'A3', 'C4'], E6, 'over D7', 3, VEL),
        ['D7: the bass D, D♯…', '…E, F, then G.'], 'Over E7, the bass rising by semitones from E.'),
    way('68-quinta', 'In 6/8: root and 5th', SIX + 'The bass alternates the chord’s root and 5th on the accents.',
        run(['D3', 'F#3', 'C4', 'A2', 'F#3', 'C4'], E6, 'over D7', 3, VEL), run(['D3', 'C4', 'F#3', 'A2', 'C4', 'F#3'], E6, 'over D7', 3, VEL),
        ['D7: D, then A below…', '…the same with the upper notes turned round.'], 'Over E7: E and B in the bass.'),
    way('68-bloque', 'In 6/8: two block chords', SIX + 'The whole chord struck twice in the bar, each a dotted quarter: two against the waltz’s three.',
        K('D7', E4.YV['D7'], [(1.5, 'A', ACC), (1.5, 'A', ACC)]), K('D7', D7L, [(1.5, 'A', ACC), (1.5, 'A', ACC)]),
        ['D7 as a barre from the A string at the 5th fret, struck twice…', '…then lower, D, F♯, C, D.'], 'E7 as two dotted-quarter chords a bar.'),
    way('68-bajo-acorde', 'In 6/8: bass, chord, chord', SIX + 'Each half of the bar: the bass, then the chord twice.',
        K('D7', D7B, [(0.5, [5], ACC), (0.5, [4, 3, 2]), (0.5, [4, 3, 2]), (0.5, [6], ACC), (0.5, [4, 3, 2]), (0.5, [4, 3, 2])]),
        K('D7', D7B, [(0.5, [6], ACC), (0.5, [4, 3, 2]), (0.5, [4, 3, 2]), (0.5, [5], ACC), (0.5, [4, 3, 2]), (0.5, [4, 3, 2])]),
        ['D7 barred at the 5th: D in the bass, the chord twice; A in the bass, the chord twice.', 'The basses the other way round: A, then D.'], 'Over E7: E, chord, chord; B, chord, chord.'),
    way('68-cluster', 'In 6/8: a cluster', SIX + 'Bass, then a cluster of the root and the semitone under it, twice in each half.',
        K('D7', D7C, [(0.5, [5], ACC), (0.5, [3, 2]), (0.5, [3, 2]), (0.5, [6], ACC), (0.5, [3, 2]), (0.5, [3, 2])]),
        K('D7', D7C, [(0.5, [6], ACC), (0.5, [3, 2]), (0.5, [3, 2]), (0.5, [5], ACC), (0.5, [3, 2]), (0.5, [3, 2])]),
        ['D7: D in the bass, then C♯ and D together; A, then the cluster.', 'The basses the other way round.'], 'Over E7: D♯ and E together after each bass.', 178),
    way('68-pedal', 'In 6/8: a pedal in the bass', SIX + 'The root held as a pedal on both accents while the notes above it move.',
        run(['D3', 'F#3', 'C4', 'D3', 'A3', 'C4'], E6, 'over D7', 3, VEL), run(['D3', 'A3', 'F#4', 'D3', 'C4', 'A4'], E6, 'over D7', 3, VEL),
        ['D7: D on both accents, F♯ and C, then A and C above.', 'D again, the upper notes climbing.'], 'Over E7: E on both accents.', 178),
]
WAYS[0]['idea'] += (' Graciano advises it for two to four bars only, best on the approach to a cadence (in two six-bar phrases, between the 2nd and 5th bar of the '
                    'second), and above all on the dominant, whose movement it suits. Roberto Grela made it his own in the waltz.')

# ================================================================ his plans for the waltz (p. 176)
SEQ8 = ['Em', 'Em', 'B7', 'B7', 'B7', 'B7', 'Em', 'Em']
FN = {'básico': E4.basico, 'variación 1': E4.var1, 'variación 2': E4.var2, 'variación 3': E4.var3}
PLANS = {1: ['básico'] * 2 + ['básico'] * 2 + ['variación 1'] * 2 + ['básico'] * 2,
         2: ['variación 2'] * 2 + ['básico'] * 2 + ['variación 1'] * 2 + ['variación 2'] * 2,
         3: ['variación 3'] * 6 + ['básico'] * 2,
         4: ['básico', 'variación 1', 'básico', 'básico', 'básico', 'variación 1', 'básico', 'básico'],
         5: ['básico', 'variación 2', 'básico', 'variación 2', 'variación 2', 'variación 1', 'variación 2', 'variación 1']}
PB = []
for k, plan in PLANS.items():
    for i, (name, c) in enumerate(zip(plan, SEQ8)):
        PB.append(bar(c, [FN[name](c, GR[c])], (f'Plan {k}: ' + ', '.join(plan) + '.') if i == 0 else ''))
PB[0]['note'] = f'{YVL}’s E minor and B7 (its pre-chorus), E minor at the 7th fret, B7 at the 2nd. ' + PB[0]['note']
RULES.append(('plans', PLANS))
ETUDE = [dict(id='vals-planes', title='Im Im V7 V7 V7 V7 Im Im, his five plans',
              idea=('A common harmonic module of the waltz, minor tonic for two bars, dominant for four, tonic for two (the waltz takes two bars where the tango takes one), '
                    'played over and over with the waltz rhythms in his combinations: basic, variation 1, 2 and 3, a pair of bars each or, in his last two plans, a different '
                    'rhythm in single bars. Each chord can be split between rhythms, which gives a wide range for accompanying.'),
              quote=T('The module and the five plans as a table of names (no sound here).', 176), bars=PB)]

# ================================================================ the tango valseado (pp. 178–179), on Очи чёрные in its own 3/4
VQ = ['Dm', 'Am', 'E7', 'Am']


def arp_item(c):
    """six eighths up the chord's notes from its bass"""
    g = G4[c]
    lo = min(M.OPEN[6 - i] + g[i] for i in range(6) if g[i] >= 0)
    pcs = {M.pc(p + '4'): p for p in M.tone_pcs(c)}
    ns, m = [], lo
    while len(ns) < 6:
        if m % 12 in pcs: ns.append(pcs[m % 12] + str((m - M.midi(pcs[m % 12] + '0')) // 12))
        m += 1
    return M.run(ns, E6, 'over ' + M.dname(c), near=5)


VALS = [dict(id='valseado-basica', title='The tango valseado: the basic rhythm',
             idea=('A tango played in 3/4. Leave out the waltz rhythms above, which spoil the illusion; use three of its own. The basic: silence on the first beat, the chord on '
                   'the second, held through the third. The tune is still thought in 2/4, to keep the tango’s accent: three bars of 2/4 run across two of 3/4, a hemiola. '
                   'Not too long: it can confuse the listener and the players. (His example of a tune laid over it is described only.)'),
             quote=T('In slashes: a quarter rest, a half note.', 178),
             bars=[bar(c, [K(c, G4[c], [(1.0, '-'), (2.0, 'C')])], f'{OCI} in its own 3/4: D minor, A minor, E7, A minor.' if i == 0 else '') for i, c in enumerate(VQ)]),
        dict(id='valseado-variacion', title='The tango valseado: the variation',
             idea='A quarter, an eighth, an eighth tied over the beat, an eighth: the chord struck on 1, on the “and” of 1, on the “and” of 2 (held over 3) and on the “and” of 3.',
             quote=T('In slashes: quarter, eighth, eighth tied to an eighth, eighth.', 178),
             bars=[bar(c, [K(c, G4[c], [(1.0, 'A'), (0.5, 'C'), (1.0, 'C'), (0.5, 'C')])]) for c in VQ]),
        dict(id='valseado-arpegio', title='The tango valseado: the arpeggio',
             idea='Six eighths climbing the chord.',
             quote=T('In slashes: six rising eighths.', 178),
             bars=[bar(c, [arp_item(c)]) for c in VQ])]
for c in VQ: RULES.append(('arp6', c, G4[c]))

SECTIONS = E4.SECTIONS + [dict(id='vals-rellenos', title='Waltz fills', part='Exercises', ex=FILLS),
                          dict(id='vals-68', title='The 6/8 over the waltz', part='Exercises', ex=WAYS),
                          dict(id='valseado', title='The tango valseado', part='Exercises', ex=VALS),
                          dict(id='vals-planes', title='Études', part='Études', ex=ETUDE)]
from quotes import trim as _trim_quotes
_trim_quotes(SECTIONS[2:])
