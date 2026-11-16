"""Denis Roux and Samy Daussat with Angelo Debarre, Gypsy Guitar: The Secrets, vol. 1, part two, "playing solo" (book
pp. 22–29; PDF = book + 2): the soloist's techniques. Their exercises are their own phrases; ours apply each technique,
as they describe it, to Очи чёрные (Les Yeux Noirs): its chords as your chart has them and its tune (Hermann's Valse
hommage, 1879, public domain), so nothing of theirs is copied but a description and the page.
- rest stroke ("damping"): every note a downstroke that comes to rest on the next string; ascending arpeggios;
- the triplet stroke: down-up-down in every triplet;
- sweeping: across the strings the pick goes one way, down going up, up coming down;
- rolling (tremolo): one note, chords, and the tune;
- chromatics: a chromatic run, alternate strokes;
- harmonics: artificial (the left hand frets, the right index touches the string twelve frets higher, the pick held
  between thumb and middle finger) and natural, at the 12th fret;
- octaves: two notes an octave apart, the strings between muted, the right hand striking through.
Left out: their "up and down" (Django's two-finger fingering: we can't show which finger plays what) and the bends,
vibrato and slides (the sound here can't bend a note). check_solo.py checks every note."""
import sys
sys.path.insert(0, '/home/claude/studies'); sys.path.insert(0, '/home/claude/studies/gypsy'); sys.path.insert(0, '/home/claude/oci')
import music as OCI
from kit_study import N, place_lines, two_lines

BOOK = 'Gypsy Guitar: The Secrets, vol. 1'
OPENS = [40, 45, 50, 55, 59, 64]
CHART = ['E7', 'E7', 'Am', 'Am', 'E7', 'E7', 'Am', 'Am', 'Dm', 'Dm', 'Am', 'Am', 'E7', 'E7', 'Am', 'Am']
CHANGES = CHART[0::2]
ROOT6 = {'E7': [0, 2, 0, 1, 0, 0], 'Am': [5, 7, 7, 5, 5, 5], 'Dm': [10, 12, 12, 10, 10, 10]}   # the root on the low E string
GYPSY = {'E7': [-1, 7, 6, 7, 5, -1], 'Am': [5, -1, 4, 5, 5, -1], 'Dm': [-1, 5, 7, 4, 6, -1]}     # your gypsy page's grips (E7, A minor 6, D minor 6)
GYPSY_NAME = {'E7': 'E7', 'Am': 'Am6', 'Dm': 'Dm6'}
NM = ['C', 'C♯', 'D', 'D♯', 'E', 'F', 'F♯', 'G', 'G♯', 'A', 'B♭', 'B']      # A minor's spellings
CHECK = {}


def nm(m): return NM[m % 12]
def midi(s, f): return OPENS[6 - s] + f
def T(text, p): return dict(where=f'{BOOK}, p. {p}', text=text, item=None, by='Debarre, Daussat and Roux')
def lab(names, what): return '=' + ','.join(names) + '|' + what


# ------------------------------------------------------------------ the tune of Очи чёрные, as notes (midi, beats) per bar
def tune_bars(shift=0):
    """the pickup and the sixteen bars: [(midi or None for a rest, beats, tied_from_before)] per bar"""
    out = [[(N(n) + shift, d, False) for n, d in OCI.PICKUP]]
    last = None
    for bar in OCI.TUNE:
        row = []
        for n, d in bar:
            if n == '~': row.append((last, d, True))
            elif n == 'r': row.append((None, d, False))
            else: last = N(n) + shift; row.append((last, d, False))
        out.append(row)
    return out


def line_fingering(ms, strings=(1, 2, 3, 4), maxf=12, start=5):
    """one line: the hand moving as little as it can, fewer string changes, no open strings"""
    cand = [[(s, m - OPENS[6 - s]) for s in strings if 1 <= m - OPENS[6 - s] <= maxf] for m in ms]
    best = [(abs(f - start), [(s, f)]) for s, f in cand[0]]
    for C in cand[1:]:
        best = [min(((c + abs(f - p[-1][1]) + 0.4 * (s != p[-1][0]), p + [(s, f)]) for c, p in best), key=lambda x: x[0]) for s, f in C]
    return [list(x) for x in min(best, key=lambda x: x[0])[1]]


EX = []
# ------------------------------------------------------------------ rest stroke (p. 23)
b = []
for c in CHANGES:
    g = ROOT6[c]
    notes = [[s, g[6 - s]] for s in (6, 5, 4, 3, 2, 1)]
    names = [nm(midi(*x)) + '↓' for x in notes]
    b.append(dict(chords=[c], note='', items=[['R', notes, [1 / 3] * 6, lab(names, 'rest strokes'), {'vel': [0.06, 0, 0, 0.04, 0, 0]}],
                                              ['C', c, g, 2.0, {'roll': 0.03}]]))
b[0]['note'] = ('Up the chord a string at a time in triplets, every note a downstroke that comes to rest on the next string, then the whole chord rolled, held two beats. '
                'Очи чёрные’s changes with the root on the low E string: E7 open, A minor at the 5th fret, D minor at the 10th.')
CHECK['damp'] = ROOT6
EX.append(dict(id='damp', title='The rest stroke (“damping”)',
               idea=('Their first technique for clarity and volume: the pick strikes the string and stops on the next one, which damps it. Gypsy guitarists play almost every downstroke this way. '
                     'Going up a chord a string at a time, every note is a rest stroke, so the pick falls through the chord.'),
               quote=T('the pick strikes the string and rests on the following one; their second exercise climbs chords in triplets this way and rolls the chord at the end.', 23),
               bars=b))

# ------------------------------------------------------------------ the triplet stroke (p. 24)
SC = [m for m in range(45, 70) if m % 12 in (9, 11, 0, 2, 4, 5, 8)]       # A harmonic minor, A2 to A4


def pos5(m):
    """the 5th position (frets 4–8): the thickest string that has the note there"""
    for s in (6, 5, 4, 3, 2, 1):
        f = m - OPENS[6 - s]
        if 4 <= f <= 8: return [s, f]
    raise ValueError(m)


down = list(reversed(SC)); up = SC
line = down + up                                             # 15 down, 15 up: ten beats of triplets
strokes = ['↓', '↑', '↓'] * 10
b, k = [], 0
for n_notes, rest in ((12, 0), (12, 0), (6, 2)):
    seg = line[k:k + n_notes]; st = strokes[k:k + n_notes]; k += n_notes
    its = [['R', [pos5(m) for m in seg], [1 / 3] * len(seg), lab([nm(m) + s for m, s in zip(seg, st)], 'down-up-down in each triplet'),
            {'vel': [0.06 if j % 3 == 0 else 0 for j in range(len(seg))]}]]
    if rest: its.append(['W', rest])
    b.append(dict(chords=[], note='', items=its))
b[0]['note'] = ('Очи чёрные’s scale, A harmonic minor, in the 5th position: down two octaves from A and back up, in triplets, each triplet down, up, down, '
                'so every beat starts with a downstroke.')
CHECK['triplet'] = line
EX.append(dict(id='triplet', title='The triplet stroke',
               idea='A stroke Django used, little known and hard to get but very clear: in every triplet, down, up, down; the next triplet starts down again.',
               quote=T('their exercises run lines of triplets, each one marked down-up-down.', 24), bars=b))

# ------------------------------------------------------------------ sweeping (p. 25)
b = []
for c in CHANGES:
    g = ROOT6[c]
    order = [6, 5, 4, 3, 2, 1, 2, 3, 4]
    notes = [[s, g[6 - s]] for s in order]
    st = ['↓'] * 6 + ['↑'] * 3
    b.append(dict(chords=[c], note='', items=[['R', notes, [1 / 3] * 9, lab([nm(midi(*x)) + a for x, a in zip(notes, st)], 'one way across the strings'),
                                               {'vel': [0.06, 0, 0, 0.04, 0, 0, 0.04, 0, 0]}]]))
b[0]['note'] = ('Up the chord from the low E string to the high E with one long downstroke, a note on each string; back down to the D string with one upstroke. '
                'Three beats of triplets on each change of Очи чёрные, the same grips as the rest strokes.')
EX.append(dict(id='sweep', title='Sweeping',
               idea='For balance, and speed across the strings: the pick moves in one direction through the strings, down going up, up coming down, instead of alternating.',
               quote=T('the pick plays in a single direction across the strings; their exercises mark each sweep.', 25), bars=b))

# ------------------------------------------------------------------ rolling (p. 26)
# 1. one note, faster and faster (16 notes in a bar of four, each shorter by the same ratio)
lo, hi = 0.9, 1.0
for _ in range(60):
    r = (lo + hi) / 2
    tot = 0.5 * (1 - r ** 16) / (1 - r)
    lo, hi = (r, hi) if tot < 4 else (lo, r)
R_ACC = r
ACC = [0.5 * r ** k for k in range(16)]
ACC[-1] += 4 - sum(ACC)
b = []
for s, c in ((6, 'E7'), (5, 'Am'), (4, 'Dm')):
    st = ['↓' if j % 2 == 0 else '↑' for j in range(16)]
    b.append(dict(chords=[c], note='', items=[['R', [[s, 0]] * 16, ACC, lab([nm(OPENS[6 - s]) + a for a in st], 'faster and faster')]]))
b[0]['note'] = ('One note, down and up, from eighths to as fast as the hand goes in one bar of four, evenly faster. The open strings that are the roots of Очи чёрные’s chords: '
                'the low E (E7), the A (A minor), the D (D minor).')
CHECK['roll-acc'] = ACC
EX.append(dict(id='roll-acc', title='Rolling: one note, faster and faster',
               idea='Rolling is the tremolo, taken from the mandolin: the pick down and up on one note or one chord, so fast it sounds held. Start slowly and speed up smoothly.',
               quote=T('one open string, sixteen notes getting faster in one bar, down and up.', 26), bars=b))
# 2. on chords
b = []
for c in CHART[:8]:
    g = GYPSY[c]
    strs = sorted((6 - i for i, f in enumerate(g) if f >= 0), reverse=True)
    hits = [[1 / 6, strs, 0.05 if j % 6 == 0 else 0] for j in range(18)]
    b.append(dict(chords=[GYPSY_NAME[c]], note='', items=[['K', GYPSY_NAME[c], g, hits, {'up': [j for j in range(18) if j % 2], 'marks': ['↓' if j % 2 == 0 else '↑' for j in range(18)]}]]))
b[0]['note'] = ('The chord rolled, down and up six to a beat, through the first eight bars of Очи чёрные with the grips of your gypsy page (E7, A minor 6, D minor 6): '
                'small strokes across the four strings of the grip.')
EX.append(dict(id='roll-chords', title='Rolling on chords',
               idea='The same on chords: the pick goes down and up across the chord without stopping.',
               quote=T('rolling on chords: D minor 6/9, B7, A minor 7, C minor 6.', 26), bars=b))
# 3. on the tune, an octave above the voice
tb = tune_bars(12)
ms = [m for bar in tb for m, d, tie in bar if m is not None and not tie]
fing = line_fingering(ms)
b, k, prev = [], 0, None
chords = [None] + CHART
for j, bar in enumerate(tb):
    notes, durs, names = [], [], []
    for m, d, tie in bar:
        if m is None: notes.append(None); durs.append(d); continue
        if tie: sf = prev
        else: sf = fing[k]; k += 1
        prev = sf
        notes.append(sf); durs.append(d); names.append(nm(m))
    its = []
    if notes and notes[-1] is None:
        its.append(['R', [x for x in notes if x], [d for x, d in zip(notes, durs) if x], lab(names, 'rolled'), {'trem': 6}])
        its.append(['W', sum(d for x, d in zip(notes, durs) if x is None)])
    else:
        its.append(['R', notes, durs, lab(names, 'rolled'), {'trem': 6}])
    b.append(dict(chords=[chords[j]] if chords[j] else [], note='', items=its))
b[0]['note'] = ('Очи чёрные’s tune an octave above where you sing it, every note rolled, six strokes to a beat (a held note keeps rolling across the bar line). '
                'On the top four strings, the hand moving as little as it can.')
CHECK['roll-tune'] = (tb, fing)
EX.append(dict(id='roll-tune', title='Rolling the tune',
               idea='Rolling on a melody, the way a mandolin sustains a tune: every note tremoloed for its whole length.',
               quote=T('“it can be played on one note or on chords”.', 26), bars=b))

# ------------------------------------------------------------------ chromatics (p. 27)
run = list(range(N('E2'), N('A3') + 1))                      # from E7's root up to A minor's
# the first position: each note on the thickest string that has it between the open string and the 4th fret
fp = [next([s_, m - OPENS[6 - s_]] for s_ in (6, 5, 4, 3, 2, 1) if 0 <= m - OPENS[6 - s_] <= 4) for m in run]
st = ['↓' if j % 2 == 0 else '↑' for j in range(len(run))]
b = [dict(chords=['E7'], note='', items=[['R', fp[:16], [0.25] * 16, lab([nm(m) + a for m, a in zip(run[:16], st[:16])], 'chromatic, down and up')]]),
     dict(chords=['Am'], note='', items=[['R', fp[16:], [0.25] * (len(run) - 16), lab([nm(m) + a for m, a in zip(run[16:], st[16:])], 'chromatic, down and up')],
                                       ['C', 'Am', [-1, 0, 2, 2, 1, 0], 4 - 0.25 * (len(run) - 16), {'roll': 0.03}]])]
b[0]['note'] = ('From E7’s root, the open low E, up by half steps to A, A minor’s root, in sixteenths, the pick down and up; then A minor. In the first position: '
                'each string from open to the 4th fret, a finger for each fret.')
CHECK['chrom'] = (run, fp)
EX.append(dict(id='chrom', title='Chromatics',
               idea='A chromatic run gives the line a push into the next chord. Every half step, the pick strictly down and up.',
               quote=T('chromatic runs, the fingering written over every note, ending on A minor 7.', 27), bars=b))

# ------------------------------------------------------------------ harmonics (p. 28)
b = []
for c1, c2 in zip(CHANGES[0::2], CHANGES[1::2]):
    its = []
    for c in (c1, c2):
        g = GYPSY[c]
        notes = [[6 - i, f] for i, f in enumerate(g) if f >= 0]
        its.append(['R', notes, [0.5] * 4, lab([nm(midi(*x) + 12) for x in notes], f'{GYPSY_NAME[c]} in harmonics, touched 12 frets higher'), {'harm': True}])
    b.append(dict(chords=[GYPSY_NAME[c1], GYPSY_NAME[c2]], note='', items=its))
b[0]['note'] = ('Each grip of your gypsy page (E7, A minor 6, D minor 6) fretted as usual and played a note at a time, each as an artificial harmonic: the right index touches the string '
                'twelve frets above the fretted note, the pick, held between thumb and middle finger, plays it; it sounds an octave up. Two chords a bar, through Очи чёрные’s changes.')
EX.append(dict(id='harm-art', title='Artificial harmonics',
               idea=('The left hand plays normally. The right index touches the string lightly twelve frets above the left hand, and the pick, held between the thumb and the middle finger, '
                     'plays the string: a bell an octave up.'),
               quote=T('artificial harmonics on chords, a note at a time: B minor 7, E9, B♭ minor 7, E♭9, A minor 7, D7♭9, G major 7.', 28), bars=b))
NAT = {'E7': [6, 4, 2, 1], 'Am': [5, 6, 1], 'Dm': [4, 5]}        # open strings whose note is in the chord: their 12th-fret harmonics
OPEN_G = {'E7': [0, 2, 0, 1, 0, 0], 'Am': [-1, 0, 2, 2, 1, 0], 'Dm': [-1, -1, 0, 2, 3, 1]}
b = []
for c in ('E7', 'Am', 'Dm', 'Am'):
    notes = [[s, 12] for s in NAT[c]]
    d = 2 / len(notes)
    b.append(dict(chords=[c], note='', items=[['R', notes, [d] * len(notes), lab([nm(OPENS[6 - s]) for s in NAT[c]], 'harmonics at the 12th fret'), {'harm': 'nat'}],
                                              ['C', c, OPEN_G[c], 2.0, {'roll': 0.03}]]))
b[0]['note'] = ('Natural harmonics: touch the string right over the 12th fret and pick it; it sounds an octave above the open string. For each chord, the open strings whose notes are in it '
                '(E7: low E, D, B, high E; A minor: A, low E, high E; D minor: D, A), then the chord itself.')
CHECK['harm-nat'] = NAT
EX.append(dict(id='harm-nat', title='Natural harmonics',
               idea='Natural harmonics, played by touching the strings at the frets marked, then a chord: E7, A minor, D minor and A minor.',
               quote=T('natural harmonics at the 11th, 12th and 7th frets, then an E minor 9/11 chord.', 28), bars=b))

# ------------------------------------------------------------------ octaves (p. 29): the tune in octaves
tb = tune_bars(0)
seq = []
for bar in tb:
    for m, d, tie in bar:
        if m is None or tie: continue
        seq.append((m, m + 12, d))
def octave_fingering(seq, start=5):
    """octaves with one string between (low E with D, A with G two frets up; D with B, G with high E three frets up),
    no open strings, the hand moving as little as it can"""
    cand = []
    for lo_, up_, d in seq:
        c = []
        for s_ in (6, 5, 4, 3):
            f = lo_ - OPENS[6 - s_]
            fu = f + (2 if s_ >= 5 else 3)
            if 1 <= f <= 12 and fu <= 15 and OPENS[6 - (s_ - 2)] + fu == up_: c.append(((s_, f), (s_ - 2, fu)))
        cand.append(c)
    best = [(abs(lw[1] - start), [(lw, upp)]) for lw, upp in cand[0]]
    for C in cand[1:]:
        best = [min(((c + abs(lw[1] - p[-1][0][1]) + 0.3 * (lw[0] != p[-1][0][0]), p + [(lw, upp)]) for c, p in best), key=lambda x: x[0]) for lw, upp in C]
    return [([list(lw), list(upp)], d) for (lw, upp), (_, _, d) in zip(min(best, key=lambda x: x[0])[1], seq)]


pl = octave_fingering(seq)
b, k = [], 0
for j, bar in enumerate(tb):
    steps, names, its = [], [], []
    for m, d, tie in bar:
        if m is None:
            if steps: its.append(two_lines(steps, over=lab(names, 'octaves')) + [{'hold': []}]); steps, names = [], []
            its.append(['W', d]); continue
        if tie:
            its.append(['W', d]); continue
        g, dd = pl[k]; k += 1
        steps.append((g, d)); names.append(f'{nm(m)}+{nm(m)}')
    if steps: its.append(two_lines(steps, over=lab(names, 'octaves')) + [{'hold': []}])
    b.append(dict(chords=[chords[j]] if chords[j] else [], note='', items=its))
for j in range(len(tb) - 1):                                   # a note tied into the next bar rings on: its strings hold
    if tb[j + 1] and tb[j + 1][0][2]:
        last = [it for it in b[j]['items'] if it[0] == 'P'][-1]
        last[4] = {'hold': [s_ for s_, f in last[1][-1]]}
b[0]['note'] = ('Очи чёрные’s tune where you sing it, doubled an octave up: the lower note on a bass string, the upper two strings higher, the string between muted by the '
                'fretting fingers, so the right hand can strike through all the strings and only the octave sounds. A held note across the bar line rings on.')
CHECK['octaves'] = (seq, pl)
EX.append(dict(id='octaves', title='Octaves',
               idea=('The hard part, they say, is to sound nothing but the octave while the right hand strikes all the strings: the fingers that fret the two notes lie across the strings '
                     'between them and mute them.'),
               quote=T('octaves on the low strings, the strings between muffled, the right hand striking through the six strings.', 29), bars=b))

SECTIONS = [dict(id='gypsy-solo', title='The soloist’s techniques', part='Exercises', ex=EX)]
