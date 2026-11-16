"""Van Eps, Harmonic Mechanisms for Guitar vol. 1, more mechanisms (PDF pp. 51–63 of the owner's copy): the scale in
open triads (first inversion, second inversion and root, each spread by an octave), triad arpeggios through the cycle
of fifths, and two lines of triads in contrary motion.

His pages give every key in turn; ours are in the keys of I Wonder Who's Kissing Her Now (E♭ major and its C minor,
in the harmonic minor as he asks), with our own choice of strings and positions, found so the hand moves least.
Nothing of his is copied: his first chords are named in words. check2.py checks every voicing against the mechanism.
"""
import sys
from itertools import combinations
sys.path.insert(0, '/home/claude/studies'); sys.path.insert(0, '/home/claude/studies/tango'); sys.path.insert(0, '/home/claude/studies/vaneps')
import entry as E1
import mel as M

BOOK = E1.BOOK
OPEN = {6: 40, 5: 45, 4: 50, 3: 55, 2: 59, 1: 64}
IW = 'I Wonder Who’s Kissing Her Now'
EB = [3, 5, 7, 8, 10, 0, 2]                     # E♭ F G A♭ B♭ C D
EB_N = ['Eb', 'Fm', 'Gm', 'Ab', 'Bb', 'Cm', 'Ddim']
CH = [0, 2, 3, 5, 7, 8, 11]                     # C harmonic minor: C D E♭ F G A♭ B
CH_N = ['Cm', 'Ddim', 'Eb+', 'Fm', 'G', 'Ab', 'Bdim']
CHECK = []                                      # (exercise, name, mechanism, midis, strings)


def triad_pcs(sc, d): return [sc[d % 7], sc[(d + 2) % 7], sc[(d + 4) % 7]]


def above(m, pc):
    """the first note of pitch class pc strictly above m"""
    x = m + 1
    while x % 12 != pc: x += 1
    return x


def voicing(kind, sc, d, low):
    """three notes, low to high, from a lowest note `low` (which must be the right pitch class)"""
    r, t, f = triad_pcs(sc, d)
    if kind == 'open1':          # 1st inversion with its 3rd dropped an octave: 3rd, 5th a 10th above, root a 4th above that
        a = low; b = above(a, f) + 12; c = above(b, r)
        return [a, b, c]
    if kind == 'open2':          # 2nd inversion opened: root, 5th above it, 3rd a 6th above that
        a = low; b = above(a, f); c = above(b, t)
        return [a, b, c]
    if kind == 'openR':          # root position with the root dropped an octave: root, 3rd a 10th above, 5th
        a = low; b = above(above(a, t), t); c = above(b, f)
        return [a, b, c]
    if kind in ('root', 'first', 'second'):
        a = low; order = {'root': (t, f), 'first': (f, r), 'second': (r, t)}[kind]
        b = above(a, order[0]); c = above(b, order[1])
        return [a, b, c]
    raise ValueError(kind)


def low_pc(kind, sc, d):
    r, t, f = triad_pcs(sc, d)
    return {'open1': t, 'open2': r, 'openR': r, 'root': r, 'first': t, 'second': f}[kind]


def placements(ms, adjacent=False, sets=None):
    out = []
    for ss in combinations((6, 5, 4, 3, 2, 1), 3):
        if adjacent and ss[0] - ss[2] != 2: continue
        if sets and ss not in sets: continue
        fr = [m - OPEN[s] for m, s in zip(ms, ss)]
        if min(fr) < 1 or max(fr) > 15: continue
        if max(fr) - min(fr) > (4 if min(fr) >= 7 else 3): continue
        g = [-1] * 6
        for s, f in zip(ss, fr): g[6 - s] = f
        out.append((ss, g, sum(fr) / 3))
    return out


def path(seq, adjacent=False, apart=False):
    """seq: [(name, midis)]; the placement for each that moves the hand least; apart: consecutive triads on different strings"""
    best = {}
    for i, (nm, ms) in enumerate(seq):
        pl = placements(ms, adjacent)
        assert pl, (nm, ms)
        new = {}
        for ss, g, a in pl:
            if i == 0:
                new[ss] = (a * 0.05, [(nm, ss, g)], a); continue
            cands = []
            for pss, (c, p, pa) in best.items():
                if apart and set(pss) & set(ss): continue
                cands.append((c + abs(a - pa) + (0.5 if ss != pss else 0), p, pa))
            if not cands: continue
            c, p, _ = min(cands, key=lambda x: x[0])
            new[ss] = (c, p + [(nm, ss, g)], a)
        assert new, ('no way on', nm)
        best = new
    return min(best.values(), key=lambda v: v[0])[1]


def scale_line(kind, sc, names, lo='E2', top='A5'):
    out = []
    for octv in range(1, 7):
        for d in range(7):
            pc = low_pc(kind, sc, d)
            low = 12 * (octv + 1) + pc
            ms = voicing(kind, sc, d, low)
            if ms[0] >= M.midi(lo) and ms[2] <= M.midi(top) and placements(ms):
                out.append((names[d], ms, d))
    out.sort(key=lambda x: x[1][0])
    return out


def C(nm, g): return ['C', nm.replace('+', 'aug'), g, 1.0, {'roll': 0.004}]


def bars_of(id_, kind, items, per_bar=4):
    out = []
    for i in range(0, len(items), per_bar):
        chunk = items[i:i + per_bar]
        its = [C(nm, g) for nm, ss, g in chunk]
        if len(chunk) < per_bar: its.append(['W', per_bar - len(chunk)])
        out.append(dict(chords=[M.dname(nm) for nm, _, _ in chunk], note='', items=its))
        for nm, ss, g in chunk: CHECK.append((id_, nm, kind, [OPEN[6 - j] + g[j] for j in range(6) if g[j] >= 0], ss))
    return out


def up_and_back(id_, kind, sc, names, top='A5'):
    line = scale_line(kind, sc, names, top=top)
    up = path([(nm, ms) for nm, ms, d in line])
    back = list(reversed(up))[1:]
    return bars_of(id_, kind, up + back), [nm for nm, _, _ in line]


def sets_text(p):
    seen = []
    for nm, ss, g in p:
        t = '-'.join(str(s) for s in ss)
        if not seen or seen[-1] != t: seen.append(t)
    return ', '.join(seen)


def T(text, p): return dict(where=f'{BOOK}, p. {p}', text=text, item=None, by='Van Eps', whose='Van Eps’s own', played='')


EX = []
b, nms = up_and_back('open1', 'open1', EB, EB_N)
b[0]['note'] = (f'{IW}’s key, E♭ major: each triad with its 3rd at the bottom, the 5th a 10th above it and the root a 4th above that, '
                f'one a beat from the lowest that fits up to the top of the neck and back. The strings skip, so each triad takes three strings that are not side by side.')
EX.append(dict(id='open-first', title='Open triads: the 3rd at the bottom',
               idea=('A first-inversion triad opened out: its 3rd dropped an octave, so the voices are a 10th and a 4th apart, a 13th in all. '
                     'Spread triads like these sound fuller than the close ones and leave room between the voices.'),
               quote=T('His scale in open first-inversion triads, in C, then C harmonic minor, F, and on through the keys.', 51), bars=b))
bh, _ = up_and_back('open1-h', 'open1', CH, CH_N)
bh[0]['note'] = 'The same in C harmonic minor (I Wonder’s C minor, with B♮): C minor, D diminished, E♭ augmented, F minor, G, A♭, B diminished.'
EX.append(dict(id='open-first-minor', title='Open triads, the 3rd at the bottom, in the harmonic minor',
               idea='Van Eps puts each key’s harmonic minor beside it.', quote=T('His C harmonic minor line in open first inversions.', 51), bars=bh))
b2, _ = up_and_back('open2', 'open2', EB, EB_N)
b2[0]['note'] = 'E♭ major: root at the bottom, the 5th above it, the 3rd a 6th above that, a 10th in all.'
EX.append(dict(id='open-second', title='Open triads: root, 5th, 3rd',
               idea='A second-inversion triad opened out: root, 5th, then the 3rd on top; a 5th and a 6th, a 10th in all.',
               quote=T('His scale in open second-inversion triads, key by key.', 54), bars=b2))
bR, _ = up_and_back('openR', 'openR', EB, EB_N)
bR[0]['note'] = 'E♭ major: the root at the bottom, the 3rd a 10th above it, the 5th on top, a 12th in all.'
EX.append(dict(id='open-root', title='Open triads: the root dropped an octave',
               idea='A root-position triad with its root dropped an octave: a 10th and a 3rd, a 12th in all.',
               quote=T('His scale in open root triads, key by key.', 57), bars=bR))

# ---------------------------------------------------------------- triad arpeggios through the cycle of fifths (p. 62)
CYC = [('Cm', CH, 0, 'up'), ('Fm', CH, 3, 'down'), ('Bb', EB, 4, 'up'), ('Eb', EB, 0, 'down')]
arp_items = []
for nm, sc, d, way in CYC:
    vs = []
    for octv in range(1, 7):
        for kind in ('root', 'first', 'second'):
            low = 12 * (octv + 1) + low_pc(kind, sc, d)
            ms = voicing(kind, sc, d, low)
            if ms[0] >= M.midi('E2') and ms[2] <= M.midi('A5') and placements(ms, adjacent=True):
                vs.append((nm + '|' + kind, ms))
    vs.sort(key=lambda x: x[1][0])
    p = path(vs, adjacent=True)
    if way == 'down': p = list(reversed(p))
    arp_items += [(n.split('|')[0], ss, g) for n, ss, g in p]
    CHECK.append(('arp-order', nm, way, [x[1] for x in vs], None))
ba = bars_of('arpeggios', 'arp', arp_items)
ba[0]['note'] = (f'The cycle in {IW}’s last bars, C minor, F minor, B♭, E♭: each chord’s triad through all its inversions on the four sets of three neighbouring '
                 'strings, C minor climbing, F minor coming down, B♭ climbing, E♭ coming down.')
EX.append(dict(id='arpeggios', title='Triad arpeggios through the cycle of fifths',
               idea=('One chord’s triad stepped through its inversions, root, first, second, from the lowest strings to the highest; the next chord in the cycle of fifths '
                     'comes back down, and so on through the keys. It ties each chord’s shapes together across the whole neck.'),
               quote=T('A minor up through its inversions, D minor down, G minor up, C minor down, and on round the cycle.', 62), bars=ba))

# ---------------------------------------------------------------- contrary motion: two lines of triads crossing (p. 63)
up_line = [x for x in scale_line('first', EB, EB_N, lo='G2', top='G5') if x[1][0] >= M.midi('G2')]
lo_seq = [(nm, ms) for nm, ms, d in up_line[:8]]
hi_seq = [(nm, ms) for nm, ms, d in reversed(up_line[-8:])]
mixed = []
for a, b_ in zip(lo_seq, hi_seq): mixed += [a, b_]
pc_ = path(mixed, adjacent=True, apart=True)
bc = bars_of('contrary', 'first', pc_)
bc[0]['note'] = (f'E♭ major in first-inversion triads (root on top): one line climbing from {M.dname(lo_seq[0][0])} on the low strings, the other falling from '
                 f'{M.dname(hi_seq[0][0])} at the top, taking turns, each triad on strings the one before it does not use. They cross in the middle.')
CHECK.append(('contrary-lines', None, None, [lo_seq, hi_seq], None))
EX.append(dict(id='contrary', title='Two lines of triads in contrary motion',
               idea=('Two lines of first-inversion triads moving against each other, one up the scale and one down, played in turn. Each triad goes on a different set of strings '
                     'from its neighbour, so the two lines stay apart: six voices in all, and the mind has to follow two things at once, which Van Eps counts as the point.'),
               quote=T('C major, four “stations”: different starting points for the two crossing lines.', 63), bars=bc))

SECTIONS = E1.SECTIONS + [dict(id='vaneps-open', title='Open triads, arpeggios and contrary motion', part='Exercises', ex=EX)]
