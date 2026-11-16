"""Gypsy jazz accompaniment after Stéphane Wrembel, Getting into Gypsy Jazz Guitar (Mel Bay), ch. 3, pp. 21–22:
la pompe (swing), the waltz, the bolero (two ways) and the bossa-manouche. Wrembel's examples are rhythm slashes on
A minor/E7 and D minor/G minor; ours: la pompe on Moonglow's A section with your arrangement's grips, the waltz on
Я вас любил with its grips, the bolero and the bossa-manouche on Очи чёрные (Les Yeux Noirs to gypsy players)."""
import sys
sys.path.insert(0, '/home/claude/studies')
import importlib.util
_spec = importlib.util.spec_from_file_location('tango_entry', '/home/claude/studies/tango/entry.py')
_t = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(_t)
K, ACC = _t.K, _t.ACC
BOOK = 'Getting into Gypsy Jazz Guitar'
UP = -0.12

# Moonglow, bars 4–11 of your arrangement, with its grips
MG = {'Bbmaj7': [6, 8, 7, 7, 6, -1], 'Bbm6': [6, -1, 5, 6, 6, -1], 'Am7': [5, 7, 5, 5, 5, 5], 'Dm9': [-1, 5, 3, 5, 5, -1], 'G13': [3, 5, 3, 4, 5, -1],
      'Gm7': [3, 5, 3, 3, 3, -1], 'Db9': [-1, 4, 3, 4, 4, -1], 'C9': [-1, 3, 2, 3, 3, -1], 'F6/C': [-1, 3, 3, 2, 3, -1], 'Fm6/C': [-1, 3, 3, 1, 3, -1],
      'B7b5': [-1, 2, 3, 2, 4, -1]}
MOON = [['Bbmaj7'], ['Bbm6'], ['Am7', 'Dm9'], ['G13'], ['Gm7'], ['Db9', 'C9'], ['F6/C', 'Fm6/C'], ['F6/C', 'B7b5']]
# Я вас любил, bars 8–15, with its grips
YV = {'G': [3, 5, 5, 4, 3, 3], 'Cmaj7': [-1, 3, 5, 4, 5, 3], 'C': [-1, 3, 5, 5, 5, 3], 'Cm': [-1, 3, 5, 5, 4, 3], 'Dsus4': [-1, 5, 7, 7, 8, 5],
      'D7': [-1, 5, 7, 5, 7, 5], 'A7/C#': [-1, 4, 5, 2, 5, -1]}
YVB = [['G'], ['Cmaj7'], ['Cmaj7', 'C'], ['Cm'], ['Dsus4'], ['Dsus4', 'D7'], ['D7'], ['G', 'A7/C#']]
OCHI = {'Am': [5, 7, 7, 5, 5, 5], 'Dm': [-1, 5, 7, 7, 6, 5], 'E7': [-1, 7, 6, 7, 5, -1]}
WR = {'Am': [5, 7, 7, 5, 5, 5], 'E7': [0, 2, 0, 1, 0, 0], 'Dm': [-1, 5, 7, 7, 6, 5]}

SQ = [(0.5, 'A'), (0.5, '-')]           # squashed: pressed, dry and bassy, a little longer
WH = [(0.25, 'A', -0.05), (0.75, '-')]    # whipped: very short, like a snare


def pompe(names, grips):
    beats = [SQ, WH, SQ, WH]
    if len(names) == 1: return [K(names[0], grips[names[0]], sum(beats, []))]
    return [K(names[0], grips[names[0]], SQ + WH), K(names[1], grips[names[1]], SQ + WH)]


def valse(names, grips):
    if len(names) == 1: return [K(names[0], grips[names[0]], SQ + WH + WH)]
    return [K(names[0], grips[names[0]], SQ + WH), K(names[1], grips[names[1]], WH)]


T3 = 1 / 6
BOL = [(0.5, 'A'), (T3, 'A'), (T3, 'A', UP), (T3, 'A'), (0.5, 'A', UP), (0.5, 'A'), (0.5, 'A'), (0.5, 'A', UP), (0.5, 'A'), (0.5, 'A', UP)]
BOL2 = [(0.5, 'A'), (1, 'A', UP), (0.5, 'A', UP), (0.5, 'A'), (0.5, 'A', UP), (0.5, 'A'), (0.5, 'A', UP)]
BOSSA = [(0.5, 'A'), (0.5, 'A', UP), (0.5, 'A', ACC), (0.5, 'A', UP), (0.5, 'A'), (0.5, 'A', UP), (0.5, 'A', ACC), (0.5, 'A', UP)]
OCHI_SEQ = ['Am', 'Am', 'Dm', 'Dm', 'Am', 'Am', 'E7', 'E7']
OWN = dict(whose='Wrembel’s own', played='Played here: that bar.')


def bars(fn, seq, grips, note):
    b = [dict(chords=list(n) if isinstance(n, list) else [n], note='', items=fn(n, grips)) for n in seq]
    b[0]['note'] = note
    return b


EX = []
EX.append(dict(
    id='pompe', title='La pompe',
    idea=('Swing accompaniment in four: the whole chord on every beat, each beat equal in loudness. 1 and 3 “squashed”: press the strings right down, a dry, bassy sound; '
          '2 and 4 “whipped”: very short and dry, like a snare drum. Free the left hand on every beat, so it never becomes one long beat and one short one. '
          'Wrembel’s practice: with a metronome clicking on every beat, then on 1 and 3 only, then on 2 and 4 only. It should bounce, like a train.'),
    quote=dict(where=f'{BOOK}, p. 21', text='his exercises are on A minor, four beats to the bar.', items=pompe(['Am'], WR), **OWN),
    bars=bars(pompe, MOON, MG, 'Moonglow’s A section (bars 4–11 of your arrangement) with its own grips: B♭ major 7, B♭ minor 6, A minor 7 and D minor 9, G13, G minor 7, D♭9 and C9, F6 and F minor 6 over C, F6 and B7♭5.')))
EX.append(dict(
    id='valse', title='The gypsy waltz',
    idea='Three beats, the 1st squashed, the 2nd and 3rd whipped.',
    quote=dict(where=f'{BOOK}, p. 22', text='his waltz example: A minor for four bars, then E7 for four.', items=valse(['Am'], WR) + valse(['E7'], WR),
               whose='Wrembel’s own', played='Played here: a bar of each.'),
    bars=bars(valse, YVB, YV, 'Я вас любил, bars 8–15, with the song’s grips: G, C major 7, C major 7 and C, C minor, D sus 4, D sus 4 and D7, D7, G and A7 over C♯.')))
EX.append(dict(
    id='bolero', title='The gypsy bolero',
    idea=('A South-American rhythm much played in gypsy jazz: down on 1, a triplet of sixteenths (down, up, down) on the “and”, then up, down, down, up, down, up on the eighths. '
          'The up-strokes lighter.'),
    quote=dict(where=f'{BOOK}, p. 22', text='his bolero (examples on D minor and G minor); played on D minor.', items=[K('Dm', WR['Dm'], BOL)], **OWN),
    bars=bars(lambda n, g: [K(n, g[n], BOL)], OCHI_SEQ, OCHI, 'Очи чёрные, which gypsy players call Les Yeux Noirs: A minor, A minor, D minor, D minor, A minor, A minor, E7, E7, barre grips at the 5th to 7th fret.')))
EX.append(dict(
    id='bolero-2', title='The gypsy bolero, the simpler way',
    idea='Wrembel’s other bolero: down on 1, up on the “and” held through 2, up on the “and” of 2, then down, up, down, up.',
    quote=dict(where=f'{BOOK}, p. 22', text='“sometimes this rhythm is used”; played on D minor.', items=[K('Dm', WR['Dm'], BOL2)], **OWN),
    bars=bars(lambda n, g: [K(n, g[n], BOL2)], OCHI_SEQ, OCHI, 'On Очи чёрные again.')))
EX.append(dict(
    id='bossa-manouche', title='Bossa-manouche',
    idea='Close to the gypsy rumba: eight strokes, down and up, the accents on 2 and 4.',
    quote=dict(where=f'{BOOK}, p. 22', text='his bossa-manouche (examples on D minor and G minor); played on D minor.', items=[K('Dm', WR['Dm'], BOSSA)], **OWN),
    bars=bars(lambda n, g: [K(n, g[n], BOSSA)], OCHI_SEQ, OCHI, 'On Очи чёрные.')))
SECTIONS = [dict(id='gypsy', title='Gypsy jazz accompaniment', part='Exercises', ex=EX)]
