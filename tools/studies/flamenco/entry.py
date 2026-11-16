"""Flamenco, the right hand: Gerhard Graf-Martinez, Flamenco Guitar Method vol. 2 (Schott 2003), lesson 6:
Arpegio Exercises I–IV (pp. 9–10) and the flamenco tremolo (p. 22). His exercises walk a two-note shape up the neck
over the open E strings; ours keep his right hand exactly (the same fingers in the same order and rhythm) on
Очи чёрные's open chords, and the tremolo on the tremolo opening of your Я вас любил."""
import sys
sys.path.insert(0, '/home/claude/studies')
import importlib.util
_spec = importlib.util.spec_from_file_location('tango_entry', '/home/claude/studies/tango/entry.py')
_t = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(_t)
K, ACC = _t.K, _t.ACC
BOOK = 'Flamenco Guitar Method, vol. 2'

OCHI = {'Am': [-1, 0, 2, 2, 1, 0], 'Dm': [-1, -1, 0, 2, 3, 1], 'E7': [0, 2, 0, 1, 0, 0]}   # the song's own open grips
SEQ = ['Am', 'Dm', 'E7', 'Am']
FING = {'p': 'B', 'i': [3], 'm': [2], 'a': [1]}


def pattern(order, per_beat):
    d = 1 / per_beat
    return [(d, FING[f], 0.1 if f == 'p' else 0) for f in order]


ARP = {'I': ('p a m i', 4), 'II': ('p i m a', 4), 'III': ('p a m i m a', 6), 'IV': ('p i m a m i', 6)}
EX = []
for n, (order, per) in ARP.items():
    one = pattern(order.split(), per)
    q_grip = [0, -1, -1, 1, 0, 0]                 # his first beat: the open low E, then the open high E, B open, G 1st fret
    EX.append(dict(
        id=f'arpegio-{n.lower()}', title=f'Arpegio {n}: {order.replace(" ", "-")}',
        idea=(f'{"Sixteenths" if per == 4 else "Six to a beat"}: the thumb on the bass, then {", ".join(order.split()[1:])}, the fingers on the G (i), B (m) and high E (a) strings. '
              'The thumb always apoyando (resting on the next string), close to the bridge. A warm-up for both hands.' +
              (' Graf-Martinez also asks for p-m-i-a, p-m-a-i, p-a-i-m, p-i-a-m, i-p-m-a and a-p-m-i.' if n in ('I', 'II') else
               ' He adds the classical patterns p-i-m-i-a-i-m-i, p-a-m-a-i-a-m-a, p-m-i-m-p-a-m-i and p-i-m-a-i-m-a-i; Sabicas began this one p-i-m-a and drew the ring finger back across the treble strings.' if n == 'IV' else '')),
        quote=dict(where=f'{BOOK}, p. {9 if n in ("I", "II") else 10}', text=('his first beat: the open low E with the thumb, the fingers on the top strings over it; the two-note shape on the G and B strings '
                                                                            'then climbs a fret each beat up to the 12th and comes back down.'),
                   items=[K('E7', q_grip, one), ['W', 3]], whose='Graf-Martinez’s own', played='Played here: that beat.'),
        bars=[dict(chords=[c], note='', items=[K(c, OCHI[c], one * 4)]) for c in SEQ]))
    EX[-1]['bars'][0]['note'] = ('The same fingers in the same order on Очи чёрные’s open chords, A minor, D minor, E7, A minor, a bar each: '
                                 'the thumb on the bass (open A, open D, open low E), i, m and a on the G, B and high E strings.')

# ---------- tremolo ----------
# Я вас любил, bars 1–6 of your arrangement: its tremolo opening (melody held on the B or high E string, the thumb walking below)
YVT = [  # (chord, [(thumb [s,f], first melody note, second melody note or None), ...one per beat])
    ('G', [([5, 10], [2, 8], None), ([4, 9], [2, 8], None), ([4, 9], [2, 8], None)]),
    ('C/E', [([6, 0], [2, 8], None), ([3, 9], [2, 8], None), ([3, 9], [2, 8], None)]),
    ('Cm6/Eb', [([5, 6], [1, 5], None), ([3, 5], [1, 5], None), ([3, 5], [1, 5], None)]),
    ('D', [([4, 0], [1, 5], None), ([2, 7], [1, 5], None), ([4, 0], [1, 10], None)]),
    ('Dmaj7', [([4, 0], [1, 9], None), ([2, 7], [1, 8], [1, 7]), ([4, 9], [1, 7], None)]),
    ('G', [([5, 10], [1, 7], None), ([4, 9], [1, 7], None), ([4, 9], [1, 7], None)]),
]
FIVE = 0.2


def trem_bar(beats, over):
    notes, durs = [], []
    for th, m1, m2 in beats:
        notes += [th, m1, m1, m2 or m1, m2 or m1]
        durs += [FIVE] * 5
    return ['R', notes, durs, over]


EX.append(dict(
    id='tremolo', title='The flamenco tremolo',
    idea=('Flamenco’s tremolo is five notes to a beat: the thumb, then four on the melody note, p-i-a-m-i (also p-m-a-m-i, p-i-m-a-m), the thumb again apoyando. '
          'Practise each finger order until the tremolo sounds round and even.'),
    quote=dict(where=f'{BOOK}, p. 22', text='Tremolo Exercise I, in 3/4: the thumb on the open low E, then D on the B string four times. Played here: its first beat.',
               items=[['R', [[6, 0]] + [[2, 3]] * 4, [FIVE] * 5, 'Em'], ['W', 2]], whose='Graf-Martinez’s own', played=''),
    bars=[dict(chords=[c], note='', items=[trem_bar(b, c)]) for c, b in YVT]))
EX[-1]['bars'][0]['note'] = ('The tremolo opening of your Я вас любил (bars 1–6) played the flamenco way: the same melody notes and the same bass notes on each beat, '
                             'four repeated notes after each thumb instead of three. The melody: G on the B string (8th fret), then A, D, C♯, C, B on the high E.')
EX[-1]['bars'][4]['note'] = 'Here the melody moves: C♯ (D major 7), then C for half a beat (D7) and B (G): the B comes in on the 4th of the five notes, just after the “and”; the G in the bass waits for the 3rd beat.'

SECTIONS = [dict(id='flamenco', title='Flamenco right hand', part='Exercises', ex=EX)]

sys.path.insert(0, '/home/claude/studies/tango')
from quotes import trim as _trim_quotes   # quotes stay a beat or two
_trim_quotes(SECTIONS)
