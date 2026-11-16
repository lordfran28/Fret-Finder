"""Jorge Morel, Latin American Rhythms for Guitar (Mel Bay, 1997). Each dance in the book is a short piece of his
built on one accompaniment pattern; we quote the pattern's opening bar and set the same pattern on the owner's songs:
the malambo (IV V I) on Очи чёрные's own open grips, the samba and the clave in G on Я вас любил's grips."""
import sys
sys.path.insert(0, '/home/claude/studies')
import importlib.util
_spec = importlib.util.spec_from_file_location('tango_entry', '/home/claude/studies/tango/entry.py')
_t = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(_t)
K, ACC = _t.K, _t.ACC

BOOK = 'Latin American Rhythms for Guitar'
OWN = dict(whose='Morel’s own')
OCHI = {'Dm': [-1, -1, 0, 2, 3, 1], 'E7': [0, 2, 0, 1, 0, 0], 'Am': [-1, 0, 2, 2, 1, 0]}     # Очи чёрные's open grips
YV = {'G': [3, 5, 5, 4, 3, 3], 'Cmaj7': [3, 3, 5, 4, 5, 3], 'Cm': [3, 3, 5, 5, 4, 3], 'D7': [5, 5, 7, 5, 7, 5]}  # Я вас любил, with a 5th in the bass
BASS = {'G': (6, 5), 'Cmaj7': (5, 6), 'Cm': (5, 6), 'D7': (5, 6), 'Am7': (5, 6)}       # (root string, string of the 5th)
CH = [4, 3, 2]

EX = []
# ---------- malambo ----------
def mal68(c1, g1, c2, g2): return [K(c1, g1, [(1, 'A', ACC), (0.5, '-')]), K(c2, g2, [(1, 'A', ACC), (0.5, '-')])]
def mal34(c, g): return [K(c, g, [(1, 'A'), (1, 'A', ACC), (1, 'A')])]
EX.append(dict(
    id='malambo', title='Malambo',
    idea=('The malambo, from Argentina’s folk dances: 6/8, two strokes to the bar, both accented, often turned into 3/4 with the accent on the 2nd beat. '
          'The harmony is usually IV, V, I. Morel’s tambora (tapping the bridge with the right hand, the accent on the 2nd beat, the chord left ringing) is a sound, not a note: try it on the held chords.'),
    quote=dict(where=f'{BOOK}, p. 10', text=('his basic rhythm in D (6th string tuned to D): G, then A7, each a quarter and an eighth rest, accented. '
                                              'Played here in standard tuning, the same notes: G under the open D, G and B strings; A7 on the open A.'),
               items=mal68('G', [3, -1, 0, 0, 0, -1], 'A7', [-1, 0, 2, 0, 2, -1]), played='Played here: that bar.', **OWN),
    bars=[dict(chords=['Dm', 'E7'], note=('The same in A minor on Очи чёрные’s own open grips: D minor, then E7, the IV and V; then A minor. Bars 2 and 4 in 3/4, '
                                          'the accent on the 2nd beat, the way Morel says the malambo mixes the two.'), items=mal68('Dm', OCHI['Dm'], 'E7', OCHI['E7'])),
          dict(chords=['Am'], note='', items=mal34('Am', OCHI['Am'])),
          dict(chords=['Dm', 'E7'], note='', items=mal68('Dm', OCHI['Dm'], 'E7', OCHI['E7'])),
          dict(chords=['Am'], note='', items=[K('Am', OCHI['Am'], [(3, 'A')])])]))

# ---------- samba ----------
def samba(c, g, second=False):
    r, f = BASS[c]
    if not second: return [K(c, g, [(0.5, [r]), (0.5, CH), (0.25, [f]), (0.5, CH), (0.25, CH)])]
    return [K(c, g, [(0.25, [r]), (0.5, CH), (0.25, CH), (0.5, [f]), (0.5, CH)])]
AM7 = [0, 0, 2, 0, 1, -1]
EX.append(dict(
    id='samba', title='Samba',
    idea=('Brazil’s samba in 2/4: the bass on each beat, root then the 5th below, and three chord strokes in the sixteenths around it, '
          'a two-bar pattern: in the first bar on the “and” of 1, the 2nd sixteenth of 2 and the last sixteenth (tied over the bar); in the second on the 2nd sixteenth, the 4th, and the “and” of 2.'),
    quote=dict(where=f'{BOOK}, pp. 12–13', text='his two-bar pattern on A minor 7: the open A, then the open low E; the chord E, G, C (D string 2nd fret, G open, B 1st).',
               items=samba('Am7', AM7) + samba('Am7', AM7, True), played='Played here: those two bars.', **OWN),
    bars=[dict(chords=[c], note='', items=samba(c, YV[c], i % 2 == 1)) for i, c in enumerate(['G', 'G', 'Cmaj7', 'Cmaj7', 'Cm', 'Cm', 'D7', 'D7'])]))
EX[-1]['bars'][0]['note'] = ('On Я вас любил’s first phrase in G, two bars a chord, with the song’s barre grips: G at the 3rd fret (bass G, then D on the A string), '
                             'C major 7 and C minor at the 3rd (bass C, then G on the low E), D7 at the 5th (bass D, then A). The chord strokes on the D, G and B strings.')

# ---------- the clave ----------
def clave(c, g, strings_):
    return [K(c, g, [(1, strings_), (0.5, '-'), (0.5, strings_), (1, '-'), (1, strings_)])], [K(c, g, [(1, '-'), (1, strings_), (1, strings_), (1, '-')])]
qa, qb = clave('C', [-1, -1, -1, -1, 1, -1], [2])
EX.append(dict(
    id='clave', title='The clave',
    idea=('The pattern under salsa, played by two wooden sticks: three strokes in the first bar (on 1, the “and” of 2, and 4), two in the second (on 2 and 3). '
          'Clap it first; then put the chords on it, short.'),
    quote=dict(where=f'{BOOK}, p. 14', text='the clave on one note, C on the B string.', items=qa + qb, played='Played here: those two bars.', **OWN),
    bars=[]))
for c in ('G', 'Cmaj7', 'D7', 'G'):
    a, b = clave(c, YV[c], CH)
    EX[-1]['bars'] += [dict(chords=[c], note='', items=a), dict(chords=[c], note='', items=b)]
EX[-1]['bars'][0]['note'] = 'The clave on Я вас любил’s chords, G, C major 7, D7, G, two bars each: the chord on the D, G and B strings at each stroke.'

SECTIONS = [dict(id='morel', title='Rhythms of Latin America', part='Exercises', ex=EX)]

sys.path.insert(0, '/home/claude/studies/tango')
from quotes import trim as _trim_quotes   # quotes stay a beat or two
_trim_quotes(SECTIONS)
