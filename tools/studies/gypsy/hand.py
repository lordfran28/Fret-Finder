"""Stéphane Wrembel, Getting into Gypsy Jazz Guitar, ch. 1 (pp. 8–13): the right-hand warm-up on open strings. A slow
tempo (40 to 50), a cycle of four beats on each string, each beat divided into 1, 2, ... 9 equal notes with its own
strokes (pp. 8–12); then moving from one division to another: a "pivot" formula, 5-1-5-2-5-3-5-4 (p. 13), and loops
such as 2-3-2-3, 2-4-2-4, 2-5-2-5. He climbs the six open strings and comes back. Ours: his tempo, 46, his cycle of
four beats, his strokes, on the open strings that carry the bass of Очи чёрные (your chart: E7, Am, E7, Am, Dm, Am, E7,
Am, each change one cycle): low E for E7, A for A minor, D for D minor. check_hand.py checks every note and stroke.

The strokes, as he marks them: every beat starts with a downstroke; inside the beat down and up take turns, except
that a beat divided by 3, 6 or 9 is played in groups of three, each down-up-down. Changing strings is always a
downstroke (here strings change only on a beat)."""
import sys
sys.path.insert(0, '/home/claude/studies')

BOOK = 'Getting into Gypsy Jazz Guitar'
BPM = 46
CHART = ['E7', 'Am', 'E7', 'Am', 'Dm', 'Am', 'E7', 'Am']          # your Очи чёрные: each chord's two bars, once
ROOT = {'E7': 6, 'Am': 5, 'Dm': 4}                                 # its root on an open string
GRIP = {6: [0, -1, -1, -1, -1, -1], 5: [-1, 0, -1, -1, -1, -1], 4: [-1, -1, 0, -1, -1, -1]}
STRN = {6: 'low E', 5: 'A', 4: 'D'}
NAMES = {1: 'quarter notes', 2: 'eighth notes', 3: 'triplets', 4: 'sixteenth notes', 5: 'quintuplets', 6: 'sextuplets',
         7: 'septuplets', 8: 'thirty-second notes', 9: 'nonuplets'}
PAGE = {1: 9, 2: 10, 3: 10, 4: 10, 5: 11, 6: 11, 7: 11, 8: 12, 9: 12}
BEAT_ACC, DOWN_ACC, UP_ACC = 0.12, 0.03, -0.06                       # the beat a little louder, upstrokes a little lighter
CHECK = []


def strokes(n):
    """'D'/'U' for each note of a beat divided by n"""
    if n % 3 == 0: return list('DUD' * (n // 3))
    return ['D' if i % 2 == 0 else 'U' for i in range(n)]


def say(n):
    s = strokes(n)
    if n % 3 == 0 and n > 3: return ', '.join(' '.join({'D': 'down', 'U': 'up'}[x] for x in s[i:i + 3]) for i in range(0, n, 3))
    return ' '.join({'D': 'down', 'U': 'up'}[x] for x in s)


def beat(n, string):
    """one beat divided by n on the open string"""
    out = []
    for i, x in enumerate(strokes(n)):
        v = BEAT_ACC if i == 0 else DOWN_ACC if x == 'D' else UP_ACC
        out.append([1 / n, [string], v])
    return out


def cycle(divs, chord):
    """four beats on the chord's root string, beat k divided by divs[k]"""
    s = ROOT[chord]
    hits = sum((beat(n, s) for n in divs), [])
    return ['K', chord, GRIP[s], hits]


def closing(item):
    """end on a downstroke: one more beat, a single note on the last string"""
    s = [x for x in range(6) if item[2][x] == 0][0]
    item[3].append([1.0, [6 - s], BEAT_ACC])
    return item


def run(exid, plan, close=True):
    """plan: the divisions of each beat, for each change of the chart. A phrase ends on a downstroke: if the last
    stroke is an upstroke, one more beat, a single downstroke, closes it."""
    bars = []
    for chord, divs in zip(CHART, plan):
        it = cycle(divs, chord)
        bars.append(dict(chords=[chord], note='', items=[it]))
    closed = close and strokes(plan[-1][-1])[-1] == 'U'
    if closed: closing(bars[-1]['items'][0])
    CHECK.append(dict(id=exid, plan=plan, closed=closed))
    return bars, closed


def T(text, p): return dict(where=f'{BOOK}, p. {p}', text=text, item=None, by='Wrembel', whose='Wrembel’s own', played='')


EX = []
for n in range(1, 10):
    b, closed = run(f'div-{n}', [[n] * 4] * len(CHART))
    b[0]['note'] = (f'Every beat in {n} equal notes{"" if n == 1 else f" ({NAMES[n]})"}, four beats on each string: the low E for E7, the A string for A minor, '
                    f'the D string for D minor, through Очи чёрные’s changes. Strokes in each beat: {say(n)}.'
                    + (' One more downstroke at the end: a phrase ends with the pick coming down.' if closed else ''))
    if n == 1:
        idea = ('Wrembel’s daily warm-up for the right hand, the “plume”: a slow metronome (40 to 50), four beats on each open string, and each beat cut into equal parts, '
                'first one, then two, three, up to nine, each with its own strokes. The wrist moves, not the arm; the pick comes down whenever it changes string, '
                'and every phrase starts and ends with a downstroke. He asks for twenty to thirty minutes a day, calm and relaxed: not speed but even notes, '
                'an even volume on every stroke and a full tone. If a division is too fast, stay on the one before for a few days.')
        q = T('a metronome at 46 and quarter notes, all downstrokes, four on each open string from the low E up to the high E and back down.', PAGE[n])
    else:
        idea = f'The beat in {n}: {NAMES[n]}.' + (' Here the strokes go in threes, each group down, up, down, so every group starts with the pick coming down.' if n in (6, 9) else '')
        q = T(f'{NAMES[n]} on the open strings, four beats on each, the strokes marked over every note.', PAGE[n])
    EX.append(dict(id=f'div-{n}', title=f'The beat in {n}' + ('' if n == 1 else f': {NAMES[n]}'), idea=idea, quote=q, bars=b))

# moving between divisions: the pivot formula on each string, then loops
PIV = [5, 1, 5, 2, 5, 3, 5, 4]
b, closed = run('pivot-5', [PIV] * len(CHART), close=False)          # his own example ends on the sixteenths
b[0]['note'] = ('The formula 5-1-5-2-5-3-5-4, one division to a beat: quintuplets, a quarter note, quintuplets, eighths, quintuplets, triplets, quintuplets, sixteenths. '
                'The whole formula on each string, eight beats, through Очи чёрные’s changes. Each beat keeps its own strokes.')
EX.append(dict(id='pivot-5', title='From one division to another: a pivot',
               idea=('Wrembel’s fourth step: choose one division as the “pivot”, the one you keep coming back to, and step out to the others in between. '
                     'Then do the same without planning it, changing division whenever you like, each beat still even.'),
               quote=T('the pivot 5 with 1, 2, 3 and 4 in turn on the low E string, then the same on every string; then from one division to another without premeditation.', 13),
               bars=b))
for a, c in ((2, 3), (2, 4), (2, 5)):
    b, closed = run(f'loop-{a}{c}', [[a, c, a, c]] * len(CHART))
    b[0]['note'] = (f'{a}-{c}-{a}-{c} on every change: {NAMES[a]} and {NAMES[c]}, a beat each. Strokes: {say(a)}; then {say(c)}.'
                    + (' One more downstroke at the end, to close.' if closed else ''))
    feel = {3: ('Two divisions in turn, a beat each. Some changes are only a doubling (2 to 4), Wrembel says, while others, such as 3 to 5, change the feel of the pulse '
                'completely. Loops like these, then your own combinations.'),
            4: 'Eighths and sixteenths: a doubling, the hand going twice as fast and back.',
            5: 'Eighths and quintuplets.'}[c]
    EX.append(dict(id=f'loop-{a}{c}', title=f'A loop: {a}-{c}-{a}-{c}',
                   idea=feel,
                   quote=T('loops of two divisions such as 2-3-2-3, 2-4-2-4, 2-5-2-5, and your own combinations.', 13), bars=b))

SECTIONS = [dict(id='gypsy-hand', title='The right hand: dividing the beat', part='Exercises', ex=EX)]
