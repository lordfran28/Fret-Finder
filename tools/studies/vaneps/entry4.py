"""Van Eps's reductions, "scales within scales" (PDF pp. 70–80 of the owner's copy): two voices, one held, the other
walking the scale from a 3rd to a 6th or from a 6th to a 3rd, up or down; each station a step higher. His studies
end each station on the first-inversion triad the last interval belongs to, for orientation. Ours: E♭ major (I Wonder
Who's Kissing Her Now), four stations each way, one note a beat, the held voice struck on the first beat and the last.
check4.py checks every interval. His pages are named, not copied."""
import sys
sys.path.insert(0, '/home/claude/studies'); sys.path.insert(0, '/home/claude/studies/tango'); sys.path.insert(0, '/home/claude/studies/vaneps')
import entry3 as E3
import mel as M
from kit_study import place_lines, two_lines, check_item

SC = [m for m in range(40, 82) if m % 12 in E3.EB]
def st(m, k): return SC[SC.index(m) + k]
CHECK = []
VARS = {'3-6-up': ('upper', +1, [2, 3, 4, 5]), '3-6-down': ('lower', -1, [2, 3, 4, 5]),
        '6-3-up': ('lower', +1, [5, 4, 3, 2]), '6-3-down': ('upper', -1, [5, 4, 3, 2])}


def station(var, held):
    """four beats: the held note and the moving voice at each interval (scale steps) in turn"""
    who, way, steps = VARS[var]
    out = []
    for k, n in enumerate(steps):
        if var in ('3-6-up', '6-3-down'):            # the held voice is the lower; the moving one above it
            lo, up = held, st(held, n)
        else:                                          # the held voice is the upper; the moving one below it
            lo, up = st(held, -n), held
        out.append((lo, up))
    CHECK.append((var, held, out))
    seq = []
    for k, (lo, up) in enumerate(out):
        if k == 0 or k == 3: seq.append((lo, up, 1.0))
        elif who == 'upper': seq.append((None, up, 1.0))
        else: seq.append((lo, None, 1.0))
    return seq


def bars_for(var, start, n=4):
    bars = []
    held = start
    for i in range(n):
        seq = station(var, held)
        for pref in (6, 8, 5, 9, 4, 10):         # the first position that keeps the hand within its stretch
            pl = place_lines(seq, lo_strings=(6, 5, 4, 3, 2), up_strings=(4, 3, 2, 1), maxf=13, prefer=pref, open_cost=2.0)
            if not check_item(two_lines(pl, over='')): break
        lab = '=' + ','.join('+'.join(M.disp(M.mk(0, 0, 4)) if False else _nm(x) for x in pair if x is not None) for pair in [(a, b) for a, b, d in seq]) + '|two voices'
        bars.append(dict(chords=['Eb'], note='', items=[two_lines(pl, over=lab)]))
        held = st(held, 1)
    return bars


NAMES12 = ['C', 'D♭', 'D', 'E♭', 'E', 'F', 'G♭', 'G', 'A♭', 'A', 'B♭', 'B']
def _nm(m): return NAMES12[m % 12]


def T(text, p): return dict(where=f'{E3.E2.BOOK}, p. {p}', text=text, item=None, by='Van Eps', whose='Van Eps’s own', played='')


EX = []
for var, title, idea, start, p in [
        ('3-6-up', 'Reductions: a 3rd opening up to a 6th', 'The lower voice holds; the upper climbs the scale from a 3rd above it to a 6th: 3rd, 4th, 5th, 6th. Then the next station a step higher.', 'Eb3', 72),
        ('3-6-down', 'Reductions: a 3rd opening down to a 6th', 'The upper voice holds; the lower goes down the scale from a 3rd below it to a 6th.', 'G4', 74),
        ('6-3-up', 'Reductions: a 6th closing up to a 3rd', 'The upper voice holds; the lower climbs from a 6th below it to a 3rd.', 'C4', 76),
        ('6-3-down', 'Reductions: a 6th closing down to a 3rd', 'The lower voice holds; the upper comes down from a 6th above it to a 3rd.', 'Eb3', 78)]:
    b = bars_for(var, M.midi(start))
    b[0]['note'] = (f'E♭ major, the key of I Wonder Who’s Kissing Her Now: four stations, each starting a step higher. Each last interval is the outer pair of a first-inversion '
                    'triad of the key, which Van Eps writes after it for orientation (it need not be played).')
    EX.append(dict(id='red-' + var, title=title, idea=idea + (' Van Eps calls these “scales within scales”: learn the shapes the fingers make, he says, as much as the sounds.' if var == '3-6-up' else ''),
                   quote=T('His studies in C and every key, major and minor.', p), bars=b))
SECTIONS = E3.SECTIONS + [dict(id='vaneps-reductions', title='Reductions: 3rds and 6ths', part='Exercises', ex=EX)]
