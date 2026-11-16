"""Diego Sola, Recursos armónicos para guitarra (Melos, 2017/2019): varying a song's chords in five steps.
Sola gives no notated exercises: chord tables, the places of each chord along the neck, and his own five steps
(the song's chords; its key; their degrees and functions; extensions from his table; linking them by nearness).
Ours: the five steps on Очи чёрные's second half (Dm Dm Am Am E7 E7 Am Am), in 3/4, bass then the chord twice,
every grip around the 5th fret so the voices move little. His table rows are quoted as chord names only."""
import sys
sys.path.insert(0, '/home/claude/studies')
import importlib.util
_spec = importlib.util.spec_from_file_location('tango_entry', '/home/claude/studies/tango/entry.py')
_tango = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(_tango)
K = _tango.K                                     # the stroke-pattern item from the tango entries

GR = {
    # the song's chords
    'Dm': [-1, 5, 7, 7, 6, 5], 'Am': [5, 7, 7, 5, 5, 5], 'E7': [-1, 7, 6, 7, 5, -1],
    # option 1 (sevenths; on the dominant its b13)
    'Dm7': [-1, 5, 7, 5, 6, -1], 'Am7': [5, -1, 5, 5, 5, -1], 'E7b13': [-1, 7, -1, 7, 9, 8],
    # option 2 (Sola's second row: m7/11 on IV, m9 on I, 7/b9 on V)
    'Dm11': [-1, 5, 5, 5, 6, -1], 'Am9': [5, -1, 5, 5, 5, 7], 'E7b9': [-1, 7, 6, 7, 6, -1],
    # option 3 (m9 on IV, m7/11 on I, 7/13 on V)
    'Dm9': [-1, 5, 3, 5, 5, -1], 'Am11': [5, -1, 5, 5, 3, -1], 'E13': [-1, 7, -1, 7, 9, 9],
    # minor 6ths (Sola's extrAcordes)
    'Dm6': [-1, 5, 7, 4, 6, -1], 'Am6': [5, -1, 4, 5, 5, -1],
    # added dominants and their substitutes
    'A7': [5, -1, 5, 6, 5, -1], 'A7b9': [5, -1, 5, 6, 5, 6], 'B7': [7, -1, 7, 8, 7, -1], 'B7b9': [7, -1, 7, 8, 7, 8],
    'Bb7': [6, -1, 6, 7, 6, -1], 'F7': [-1, 8, 7, 8, 6, -1], 'Eb7': [-1, 6, 5, 6, 4, -1],
}
TONES = {'Dm': {2, 5, 9}, 'Am': {9, 0, 4}, 'E7': {4, 8, 11, 2}, 'Dm7': {2, 5, 9, 0}, 'Am7': {9, 0, 4, 7}, 'E7b13': {4, 8, 11, 2, 0},
         'Dm11': {2, 5, 9, 0, 7}, 'Am9': {9, 0, 4, 7, 11}, 'E7b9': {4, 8, 11, 2, 5}, 'Dm9': {2, 5, 9, 0, 4}, 'Am11': {9, 0, 4, 7, 2},
         'E13': {4, 8, 11, 2, 1}, 'Dm6': {2, 5, 9, 11}, 'Am6': {9, 0, 4, 6}, 'A7': {9, 1, 4, 7}, 'A7b9': {9, 1, 4, 7, 10},
         'B7': {11, 3, 6, 9}, 'B7b9': {11, 3, 6, 9, 0}, 'Bb7': {10, 2, 5, 8}, 'F7': {5, 9, 0, 3}, 'Eb7': {3, 7, 10, 1},
         'Am (open)': {9, 0, 4}, 'Am (7th)': {9, 0, 4}, 'E7 (open)': {4, 8, 11, 2}, 'E7 (2nd)': {4, 8, 11, 2}, 'E7 (7th)': {4, 8, 11, 2}, 'E7 (12th)': {4, 8, 11, 2}}
HALF2 = ['Dm', 'Dm', 'Am', 'Am', 'E7', 'E7', 'Am', 'Am']


def strings(g): return [6 - i for i in range(6) if g[i] >= 0]


def bar(c, g=None):
    g = g or GR[c]; s = strings(g)
    return dict(chords=[c], note='', items=[K(c, g, [(1, s[:1]), (1, s[1:]), (1, s[1:])])])


def row(names, note):
    b = [bar(c) for c in names]
    b[0]['note'] = note
    return b


def T(where, text): return dict(where=where, text=text, item=None, by='Sola')


BOOK = 'Recursos armónicos para guitarra'
EX = []
EX.append(dict(
    id='sola-original', title='Step 1–3: the song’s chords, their degrees',
    idea=('Sola’s first three steps: take the song’s chords, check they belong to one key, and name each one’s degree and job (tonic, subdominant, dominant). '
          'Очи чёрные’s second half in A minor: D minor is IV (subdominant), A minor is I (tonic), E7 is V (dominant, with its 7th already in the song). '
          'Bass, then the chord twice, as in the song’s 3/4.'),
    quote=T(f'{BOOK}, p. 26', 'his first song’s chords are G, Em, C, D: I, VI, IV, V in G.'),
    bars=row(HALF2, 'D minor as a barre at the 5th fret, root on the A string; A minor as a full barre at the 5th; E7 from the A string at the 7th fret (E, G♯, D, E). All within the 5th to 7th fret.')))
EX.append(dict(
    id='sola-opcion-1', title='Step 4–5, first choice: sevenths',
    idea=('Step 4: from Sola’s table of extensions, a 7th on each chord; on the dominant, which already has its 7th, one of the dominant’s tensions, here the ♭13. '
          'Step 5: link them by nearness, the top notes moving as little as possible.'),
    quote=T(f'{BOOK}, p. 27', 'his second song (Am, A7, Dm, G, C, E) in his first choice becomes Am7, A7, Dm7, G7, CMaj7, E7/13b.'),
    bars=row(['Dm7', 'Dm7', 'Am7', 'Am7', 'E7b13', 'E7b13', 'Am7', 'Am7'],
             'D minor 7 (D, A, C, F at the 5th–7th fret), A minor 7 (A, G, C, E across the 5th), E7 with ♭13 (E, D, G♯, C at the 7th–9th).')))
EX.append(dict(
    id='sola-opcion-2', title='Step 4–5, second choice: 11ths, 9ths and the ♭9',
    idea='Sola’s second row for a minor song: minor 7 with 11 on IV, minor 9 on I, 7 with ♭9 on V.',
    quote=T(f'{BOOK}, p. 27', 'the second choice for the same song: Am9, A7/9b, Dm7/11, G7/9b, CMaj7, E7/9b.'),
    bars=row(['Dm11', 'Dm11', 'Am9', 'Am9', 'E7b9', 'E7b9', 'Am9', 'Am9'],
             'D minor 11, Sola’s m7/11 (D, G, C, F at the 5th–6th fret), A minor 9 (A, G, C, E, B at the 5th–7th), E7 ♭9 (E, G♯, D, F at the 6th–7th).')))
EX.append(dict(
    id='sola-opcion-3', title='Step 4–5, third choice: the colours swapped',
    idea='Sola’s third row: minor 9 on IV, minor 7/11 on I, 7 with 13 on V.',
    quote=T(f'{BOOK}, p. 27', 'the third choice: Am7/11, A7/13b, Dm9, G7/13, C9, E7/13.'),
    bars=row(['Dm9', 'Dm9', 'Am11', 'Am11', 'E13', 'E13', 'Am11', 'Am11'],
             'D minor 9 (D, F, C, E at the 3rd–5th fret), A minor 11, his m7/11 (A, G, C, D at the 3rd–5th), E13, his 7/13 (E, D, G♯, C♯ at the 7th–9th).')))
EX.append(dict(
    id='sola-sextas', title='Minor 6ths',
    idea='From Sola’s extrAcordes: the minor 6 in place of the plain minor chord, linked by its nearest top notes; only the strings that are pressed are played.',
    quote=T(f'{BOOK}, p. 23', 'his extrAcordes include the minor 6 and the major 6, three places each.'),
    bars=row(['Dm6', 'Dm6', 'Am6', 'Am6', 'E7', 'E7', 'Am6', 'Am6'],
             'D minor 6 (D, A, B, F at the 4th–7th fret), A minor 6 (A, F♯, C, E at the 4th–5th), the song’s E7 between.')))
EX.append(dict(
    id='sola-dominantes', title='Adding dominants',
    idea=('Sola: a chord can be altered or added to become the dominant of what comes next, as zambas do (his example puts A7 between A minor and D minor). '
          'Here A7 before D minor and B7 before E7, each with a ♭9 the second time.'),
    quote=T(f'{BOOK}, pp. 27 and 30', 'in his second song, after Am comes A7: the dominant of the Dm that follows.'),
    bars=row(['Am', 'A7', 'Dm', 'Dm', 'Am', 'B7', 'E7', 'E7'], 'A minor, A7 into D minor (A, G, C♯, E at the 5th–6th fret); A minor, B7 into E7 (B, A, D♯, F♯ at the 7th–8th).')
         + row(['Am', 'A7b9', 'Dm', 'Dm', 'Am', 'B7b9', 'E7', 'E7'], 'The same with ♭9 on the added dominants: B♭ on top of A7, C on top of B7.')))
EX.append(dict(
    id='sola-sustituto', title='Substituting the dominant',
    idea=('Sola: the dominant can be replaced by the 7th chord a tritone away, which shares its 3rd and 7th. B♭7 for E7, F7 for B7, E♭7 for A7: '
          'the bass falls by a semitone into the next chord.'),
    quote=T(f'{BOOK}, p. 29', 'his chapter on substituting the dominant.'),
    bars=row(['Am', 'Eb7', 'Dm', 'Dm', 'Am', 'F7', 'E7', 'Bb7', 'Am', 'Am'],
             'A minor, E♭7 (for A7) into D minor; A minor, F7 (for B7) into E7, then B♭7 (for E7) into A minor. Each substitute keeps the 3rd and 7th of the chord it replaces, swapped.')))
PL = [('Am', [-1, 0, 2, 2, 1, 0]), ('Am', [5, 7, 7, 5, 5, 5]), ('Am', [-1, -1, 7, 9, 10, 8])]
PE = [('E7', [0, 2, 0, 1, 0, 0]), ('E7', [-1, -1, 2, 4, 3, 4]), ('E7', [-1, 7, 6, 7, 5, -1]), ('E7', [-1, 7, 9, 7, 9, 7]), ('E7', [12, 11, 12, 13, 12, 12])]
EX.append(dict(
    id='sola-lugares', title='One chord, every place on the neck',
    idea=('Sola’s system: every major chord has five places along the neck, every minor chord three, each with its own top note. Learn them with one pattern, '
          'from the lowest place to the highest and back; then a song can stay in one place, or move to where its top notes sing best.'),
    quote=T(f'{BOOK}, pp. 12–13', 'five places for each major chord, three for each minor one, in order up the neck.'),
    bars=[bar(n, g) for n, g in PL] + [bar(n, g) for n, g in PE]))
EX[-1]['bars'][0]['note'] = ('A minor three ways: in open position; as a full barre at the 5th fret; at the 7th–10th fret on the top four strings (A, E, A, C). '
                             'Then E7 five ways: open; at the 2nd–4th fret on the top four strings; from the A string at the 5th–7th; as a barre at the 7th from the A string; as a barre at the 12th.')

SECTIONS = [dict(id='sola', title='Varying the chords of a song', part='Exercises', ex=EX)]
