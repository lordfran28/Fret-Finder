"""Argentine folk accompaniment: the rhythm table of Música folklórica argentina (Samela, Melos 1972/2007), p. 3:
an ostinato and a variant for each dance, written for a strummed guitar or a drum (rim = high, centre = low).
On the guitar: the high strokes on the top strings, the low ones on the bass strings. Quoted on G (the book's first
song is in G); ours on Я вас любил's chords and grips in 6/8 (its 3/4 felt in two), the carnavalito on Очи чёрные."""
import sys
sys.path.insert(0, '/home/claude/studies')
import importlib.util
_spec = importlib.util.spec_from_file_location('tango_entry', '/home/claude/studies/tango/entry.py')
_t = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(_t)
K, ACC = _t.K, _t.ACC

BOOK = 'Música folklórica argentina'
YV = {'G': [3, 5, 5, 4, 3, 3], 'Cmaj7': [3, 3, 5, 4, 5, 3], 'Cm': [3, 3, 5, 5, 4, 3], 'D7': [5, 5, 7, 5, 7, 5]}
OCHI = {'Am': [-1, 0, 2, 2, 1, 0], 'E7': [0, 2, 0, 1, 0, 0], 'Dm': [-1, -1, 0, 2, 3, 1]}
G_OPEN = [3, 2, 0, 0, 0, 3]
HI, LO = [3, 2, 1], 'low'


def hits(spec, g):
    """spec: (eighths, 'h'|'l'|'-') ; h = top three strings, l = the grip's bass strings (up to three, below the top three)"""
    low = [s for s in (6, 5, 4) if g[6 - s] >= 0]
    out = []
    for d, w in spec:
        m = '-' if w == '-' else ([] if w == '~' else (HI if w == 'h' else low))
        out.append((d / 2, m, ACC if w == 'h' else 0))
    return out


R = {   # in eighths
    'gato': [(2, 'h'), (1, 'l'), (1, 'h'), (2, 'l')],
    'gato-v': [(2, 'h'), (1, 'l'), (1, 'h'), (1, 'l'), (1, 'l')],
    'zamba': [(1.5, 'h'), (0.5, 'l'), (1, 'l'), (1, 'h'), (2, 'l')],
    'zamba-v': [(1.5, 'h'), (0.5, 'l'), (1, 'l'), (1, 'h'), (0.5, 'l'), (0.5, 'h'), (0.5, 'l'), (0.5, 'l')],
    'cueca': [(1.5, 'h'), (0.5, 'l'), (1, 'l'), (1, 'h'), (2, 'l')],
    'cueca-v': [(1.5, 'h'), (0.5, 'l'), (1, 'l'), (1, 'h'), (0.5, 'l'), (0.5, 'l'), (0.5, 'l'), (0.5, 'l')],
    'carnavalito': [(1, 'h'), (0.5, 'l'), (0.5, 'l'), (1, 'h'), (0.5, 'l'), (0.5, 'l')],
    'carnavalito-v': [(1, 'h'), (0.5, 'l'), (0.5, 'l'), (0.5, '~'), (0.5, 'l'), (1, 'l')],
}
DANCE = {
    'gato': ('Bailecito and gato', 'The ostinato of the bailecitos and gatos, fast and bright: high, low, high, low, a quarter, an eighth, an eighth, a quarter.'),
    'gato-v': ('Bailecito and gato, the variant', 'The variant: the last low quarter split in two eighths. Keep the variants for the places where the tune rests.'),
    'zamba': ('Zamba', 'The zamba’s ostinato, slow and expressive: a dotted eighth high, a sixteenth and an eighth low; an eighth high, a quarter low.'),
    'zamba-v': ('Zamba, the variant', 'The variant: the second half in sixteenths, low, high, low, low after the high eighth.'),
    'cueca': ('Cueca', 'The cueca, moderate: the same ostinato as the zamba, in a livelier tempo.'),
    'cueca-v': ('Cueca, the variant', 'The variant: four low sixteenths after the high eighth.'),
    'carnavalito': ('Carnaval and carnavalito', 'In 2/4, fast: on each beat a high eighth and two low sixteenths.'),
    'carnavalito-v': ('Carnaval and carnavalito, the variant', 'The variant: a high eighth, then low sixteenths, one tied over the beat, and a low eighth.'),
}
SEQ = ['G', 'Cmaj7', 'Cm', 'D7']
EX = []
for k, (title, idea) in DANCE.items():
    if k.startswith('carnavalito'):
        quote = [K('G', G_OPEN, hits(R[k], G_OPEN))]
        bars = [dict(chords=[c], note='', items=[K(c, OCHI[c], hits(R[k], OCHI[c]))]) for c in ('Am', 'Am', 'E7', 'Am')]
        bars[0]['note'] = 'On Очи чёрные’s open grips, A minor and E7: high strokes on the top three strings, low ones on the bass strings.'
    else:
        quote = [K('G', G_OPEN, hits(R[k], G_OPEN))]
        bars = [dict(chords=[c], note='', items=[K(c, YV[c], hits(R[k], YV[c]))]) for c in SEQ]
        bars[0]['note'] = ('On Я вас любил’s chords, G, C major 7, C minor, D7, its 3/4 felt as 6/8, with the song’s barre grips: '
                           'the high strokes on the top three strings, the low ones on the bass strings of each grip.')
    EX.append(dict(id=k, title=title, idea=idea + ' Strummed: high strokes accented on the top strings, low strokes on the bass strings.',
                   quote=dict(where=f'{BOOK}, p. 3', text=('the table of ostinatos and variants, for a strummed guitar or a drum (rim and centre). '
                                                             'Here on G in open position, the key of the book’s first song.'),
                              items=quote, whose='The book’s own', played='Played here: that bar.'),
                   bars=bars))
SECTIONS = [dict(id='folk', title='Argentine folk dances', part='Exercises', ex=EX)]
