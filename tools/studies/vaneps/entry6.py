"""Van Eps's melodic minor in triads (book pp. 33 and 39; PDF 39 and 45 of the owner's copy): the melodic minor scale
in first-inversion triads, and in second-inversion triads, from the lowest that fits on the three low strings up the
neck, and back down in the relative major's notes (the natural minor), as he writes: "descensions are in relative
major keys". His first key is A minor; ours is A minor too, the key of Очи чёрные, with our own string sets and
positions (least movement, the hand never wider than four frets, five from the 7th fret up), coming down to the
lowest A minor. check6.py checks every triad."""
import sys
sys.path.insert(0, '/home/claude/studies'); sys.path.insert(0, '/home/claude/studies/tango'); sys.path.insert(0, '/home/claude/studies/vaneps')
import entry5 as E5
E1 = E5.E4.E3.E2.E1
from kit_study import N

A_MEL = [9, 11, 0, 2, 4, 6, 8]                          # A B C D E F♯ G♯
A_MEL_N = ['Am', 'Bm', 'Caug', 'D', 'E', 'F#dim', 'G#dim']
A_NAT = [9, 11, 0, 2, 4, 5, 7]                          # A B C D E F G (C major's notes)
A_NAT_N = ['Am', 'Bdim', 'C', 'Dm', 'Em', 'F', 'G']
CHECK = []


def voiced(root, deg, sc, inv):
    """the triad on scale degree deg with its root at midi `root`, in the inversion"""
    t = root + (sc[(deg + 2) % 7] - sc[deg]) % 12
    f = root + (sc[(deg + 4) % 7] - sc[deg]) % 12
    return [t, f, root + 12] if inv == 1 else [f, root + 12, t + 12]


def roots(sc, lo, hi):
    """(root midi, degree) for every scale note from lo to hi"""
    return [(m, sc.index(m % 12)) for m in range(lo, hi + 1) if m % 12 in sc]


def line(inv, top):
    """up in the melodic minor from the lowest triad that fits on the 6th, 5th and 4th strings to the highest that fits
    (top note at most `top`); back down in the natural minor, from the next note down to the lowest A minor"""
    cands = []
    for m, d in roots(A_MEL, 30, 90):
        ms = voiced(m, d, A_MEL, inv)
        if ms[2] <= top and E1.placements(ms): cands.append((m, d, ms))
    first = next(i for i, (m, d, ms) in enumerate(cands) if any(p[0] == 4 for p in E1.placements(ms)))
    up = cands[first:]
    low_a = next(m for m, d, ms in up if d == 0)                  # the lowest A minor on the way up
    down = []
    for m, d in reversed(roots(A_NAT, low_a, up[-1][0] - 1)):
        down.append((m, d, voiced(m, d, A_NAT, inv)))
    names = [A_MEL_N[d] for m, d, ms in up] + [A_NAT_N[d] for m, d, ms in down]
    chords = [ms for m, d, ms in up] + [ms for m, d, ms in down]
    grips = E1.path(chords)
    CHECK.append(dict(inv=inv, up=[(m, d) for m, d, _ in up], down=[(m, d) for m, d, _ in down], names=names, grips=[g for n, g in grips]))
    return names, grips, len(up)


def bars_for(names, grips):
    return E1.bars_from(names, grips)


def sets_text(grips):
    used = []
    for n, g in grips:
        if not used or used[-1] != n: used.append(n)
    return ', '.join(f'{n}/3' for n in used)


EX = []
for inv, exid, title, top, q, idea in [
    (1, 'mel-1st', 'The melodic minor in first-inversion triads', N('A5'),
     dict(where=f'{E5.BOOK}, p. 33', text='his A minor line begins on the lowest strings with D (F♯, A, D) and E (G♯, B, E): the melodic minor’s own triads, the root on top.',
          items=[['C', 'D', [2, 0, 0, -1, -1, -1], 1.0, {'roll': 0.004}], ['C', 'E', [4, 2, 2, -1, -1, -1], 1.0, {'roll': 0.004}], ['W', 2]],
          whose='Van Eps’s own', played='Played here: those two.'),
     'Van Eps gives every scale in triads in the melodic minor too, up the neck in the melodic minor (the 6th and 7th raised: in A, F♯ and G♯) and back down in the '
     'notes of the relative major (in A minor, C major’s notes: F and G natural), the way the melodic minor is sung, up one way and down the other. '
     'Its triads going up: minor, minor, augmented, major, major, diminished, diminished; coming down they are the natural minor’s.'),
    (2, 'mel-2nd', 'The melodic minor in second-inversion triads', N('A5'),
     dict(where=f'{E5.BOOK}, p. 39', text='his A minor line begins with B minor (F♯, B, D) and C augmented (G♯, C, E) on the lowest strings.',
          items=[['C', 'Bm', [2, 2, 0, -1, -1, -1], 1.0, {'roll': 0.004}], ['C', 'Caug', [4, 3, 2, -1, -1, -1], 1.0, {'roll': 0.004}], ['W', 2]],
          whose='Van Eps’s own', played='Played here: those two.'),
     'The same in second inversion: the 5th at the bottom, the root in the middle, the 3rd on top.')]:
    names, grips, n_up = line(inv, top)
    b = bars_for(names, grips)
    b[0]['note'] = (f'Очи чёрные’s key, A minor: up in the melodic minor from {names[0].replace("#", "♯").replace("aug", "+")} on the low strings to the top of the neck, '
                    f'one triad to a beat, then down in the natural minor to A minor. The string sets: {sets_text(grips)}.')
    turn = n_up // 4
    if turn < len(b) and turn > 0:
        b[turn]['note'] = ('Coming down: the natural minor (F and G natural).' if not b[turn]['note'] else b[turn]['note'])
    EX.append(dict(id=exid, title=title, idea=idea, quote=q, bars=b))

# the melodic minor goes beside the other scales in triads, before the open triads
SECTIONS = list(E5.SECTIONS)
SECTIONS.insert(1, dict(id='vaneps-melodic', title='The melodic minor in triads', part='Exercises', ex=EX))
