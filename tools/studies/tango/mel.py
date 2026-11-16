"""Shared tools for the melody entries from Graciano's ch. 7 (melodía): spelled notes (C♭, E♯ and the rest kept as
written), his scales, his scale-for-a-chord rules (pp. 62–65), single-line fingering in position, and run items.

Notes are strings like 'Eb4', 'C#5', 'Cb5' (sounding pitch, scientific octave: C♭5 sounds as B4)."""
import re

LET = 'CDEFGAB'
LPC = [0, 2, 4, 5, 7, 9, 11]
OPEN = {6: 40, 5: 45, 4: 50, 3: 55, 2: 59, 1: 64}


# ---------------------------------------------------------------- spelling
def parse(n):
    m = re.match(r'^([A-G])(b|#|)(-?\d+)$', n)
    assert m, n
    return LET.index(m.group(1)), {'b': -1, '': 0, '#': 1}[m.group(2)], int(m.group(3))


def midi(n):
    i, a, o = parse(n)
    return 12 * (o + 1) + LPC[i] + a


def mk(i, a, o):
    return LET[i] + {-1: 'b', 0: '', 1: '#'}[a] + str(o)


def tr(n, steps, semis):
    """move a spelled note by letter steps and semitones together (a 4th down: -3, -5); single accidentals only"""
    i, a, o = parse(n)
    j = i + steps
    o2 = o + j // 7; j %= 7
    target = midi(n) + semis
    acc = target - (12 * (o2 + 1) + LPC[j])
    assert acc in (-1, 0, 1), ('double accidental', n, steps, semis)
    return mk(j, acc, o2)


def pc_name(n):
    return n.rstrip('-0123456789')


def disp(n):
    p = pc_name(n)
    return p[0] + p[1:].replace('b', '♭').replace('#', '♯')


def dname(name):
    """a chord or scale name for the page"""
    return name.replace('b', '♭').replace('#', '♯').replace('m7♭5', 'm7♭5').replace('dim7', '°7')


def pc(n): return midi(n) % 12


def at_octave(pcn, o):
    """the note of pitch-class name pcn whose letter sits in octave o (C♭ in octave 5 is C♭5, sounding B4)"""
    return pcn + str(o)


# ---------------------------------------------------------------- scales (pp. 62–65, 71)
SCALES = {
    'major': ([0, 1, 2, 3, 4, 5, 6], [0, 2, 4, 5, 7, 9, 11]),
    'harmonic minor': ([0, 1, 2, 3, 4, 5, 6], [0, 2, 3, 5, 7, 8, 11]),
    'melodic minor': ([0, 1, 2, 3, 4, 5, 6], [0, 2, 3, 5, 7, 9, 11]),          # the same up and down (p. 65)
    'tango minor': ([0, 1, 2, 3, 4, 5, 5, 6, 6], [0, 2, 3, 5, 7, 8, 9, 10, 11]),  # 1 2 b3 4 5 b6 6 b7 7 (p. 63)
    'blues': ([0, 2, 3, 3, 4, 6], [0, 3, 5, 6, 7, 10]),                         # 1 b3 4 #4 5 b7 (p. 71)
    'jazz': ([0, 2, 2, 3, 3, 4, 6, 6], [0, 3, 4, 5, 6, 7, 10, 11]),             # 1 b3 3 4 #4 5 b7 7 (p. 71)
}
SCALE_WORDS = {'major': 'major', 'harmonic minor': 'harmonic minor', 'melodic minor': 'melodic minor',
               'tango minor': 'tango minor', 'blues': 'blues scale', 'jazz': 'jazz scale'}


def scale_pcs(root, kind):
    """the scale's notes as spelled pitch classes, from its root"""
    st, se = SCALES[kind]
    return [pc_name(tr(root + '4', a, b)) for a, b in zip(st, se)]


def scale_notes(root, kind, lo, hi):
    """every note of the scale between two notes (inclusive), low to high, spelled"""
    st, se = SCALES[kind]
    out = []
    for o in range(0, 8):
        base = root + str(o)
        for a, b in zip(st, se):
            n = tr(base, a, b)
            if midi(lo) <= midi(n) <= midi(hi): out.append(n)
    out = sorted(set(out), key=lambda n: (midi(n), n))
    return out


def scale_run(root, kind, start, n, direction=1):
    """n notes of the scale from `start` (which must be in the scale) going up (1) or down (-1) by scale steps"""
    lo = tr(start, -21, -36) if direction < 0 else start
    hi = tr(start, 21, 36) if direction > 0 else start
    ns = scale_notes(root, kind, lo, hi)
    i = ns.index(start)
    return [ns[i + k * direction] for k in range(n)]


def in_scale(note, root, kind):
    return pc_name(note) in scale_pcs(root, kind)


# ---------------------------------------------------------------- chords
DEG = {'1': (0, 0), 'b2': (1, 1), '2': (1, 2), '9': (1, 2), 'b3': (2, 3), '3': (2, 4), '4': (3, 5), '#4': (3, 6), 'b5': (4, 6),
       '5': (4, 7), '#5': (4, 8), 'b6': (5, 8), '6': (5, 9), 'bb7': (6, 9), 'b7': (6, 10), '7': (6, 11)}
QUAL = {'': ['1', '3', '5'], 'maj7': ['1', '3', '5', '7'], '6': ['1', '3', '5', '6'], 'm': ['1', 'b3', '5'], 'm7': ['1', 'b3', '5', 'b7'],
        'm6': ['1', 'b3', '5', '6'], '7': ['1', '3', '5', 'b7'], '9': ['1', '3', '5', 'b7', '9'], 'dim7': ['1', 'b3', 'b5', 'bb7'],
        'm7b5': ['1', 'b3', 'b5', 'b7'], 'aug': ['1', '3', '#5'], '+': ['1', '3', '#5']}
FAMILY = {'': 'maj', 'maj7': 'maj', '6': 'maj', 'm': 'min', 'm7': 'min', 'm6': 'min', '7': 'dom', '9': 'dom',
          'dim7': 'dim', 'm7b5': 'hd', 'aug': 'aug', '+': 'aug'}
DEG_WORD = {'1': 'root', '3': '3rd', 'b3': '3rd', '5': '5th', 'b5': '♭5th', '#5': '♯5th', '6': '6th', '7': '7th', 'b7': '7th',
            'bb7': '7th', '9': '9th'}


def chord_parse(name):
    m = re.match(r'^([A-G][b#]?)(.*?)(?:/([A-G][b#]?))?$', name)
    assert m and m.group(2) in QUAL, name
    return m.group(1), m.group(2), m.group(3)


def chord_tones(name):
    """spelled pitch classes of the chord, with their degree names"""
    r, q, _ = chord_parse(name)
    return [(pc_name(tr(r + '4', *DEG[d])), d) for d in QUAL[q]]


def tone_pcs(name): return [p for p, _ in chord_tones(name)]


def is_tone(note, name):
    return pc(note) in {midi(p + '4') % 12 for p in tone_pcs(name)}


def degree_of(note, name):
    for p, d in chord_tones(name):
        if midi(p + '4') % 12 == pc(note): return d
    return None


def guide_tones(name):
    """Graciano's guide tones (p. 72): the 3rd and the 7th; on diminished, half-diminished and augmented chords the 5th too.
    A plain triad has no 7th; a 6 chord's 6th stands where the 7th would be only if asked."""
    r, q, _ = chord_parse(name)
    fam = FAMILY[q]
    ds = [d for d in QUAL[q] if d in ('3', 'b3', '7', 'b7', 'bb7')]
    if fam in ('dim', 'hd', 'aug'): ds += [d for d in QUAL[q] if d in ('b5', '#5')]
    return [(pc_name(tr(r + '4', *DEG[d])), d) for d in ds]


# ---------------------------------------------------------------- his scale-for-a-chord rules (pp. 62–65)
def key_pcs(key, mode):
    return scale_pcs(key, 'major' if mode == 'major' else 'harmonic minor')


def rule_for(chord, key, mode='major', nxt=None):
    """(rule number, scale root, scale kind, why) for one chord of a song, by Graciano's rules.
    Rule 1: every chord of the key's own scale takes the key's scale. Rule 2: in minor, the harmonic minor of the key.
    3: a major (maj7) chord whose root is outside the key: the major scale a 4th below its name.
    4: a major chord on a root of the key, but not of the key's chords: the major scale from its name.
    5/6: a minor chord that is not one of the key's: the major scale a whole tone below its name.
    7a/7b: a dominant on a root of the key: the major (7a) or harmonic minor (7b) scale a 5th below, by the chord it goes to.
    8: a dominant on a root outside the key: the melodic minor a 4th below (a tritone substitute)."""
    r, q, _ = chord_parse(chord)
    kp = key_pcs(key, mode)
    tones = tone_pcs(chord)
    kmid = {midi(p + '4') % 12 for p in kp}
    diatonic = all(midi(t + '4') % 12 in kmid for t in tones)
    root_in = midi(r + '4') % 12 in kmid
    fam = FAMILY[q]
    if mode == 'minor':
        if diatonic: return ('2', key, 'harmonic minor', 'every chord comes from the key’s harmonic minor')
        raise ValueError(f'no rule for {chord} in {key} minor')
    if diatonic:
        return ('1', key, 'major', 'all the key’s own chords take the key’s scale')
    if fam == 'maj':
        if root_in: return ('4', r, 'major', 'a major chord on a note of the key, not one of its chords: the major scale from its name')
        return ('3', pc_name(tr(r + '4', -3, -5)), 'major', 'a major chord on a note outside the key: the major scale a 4th below its name')
    if fam == 'min':
        return ('5' if root_in else '6', pc_name(tr(r + '4', -1, -2)), 'major',
                'a minor chord that is not one of the key’s: the major scale a whole tone below its name')
    if fam == 'dom':
        if not root_in:
            return ('8', pc_name(tr(r + '4', -3, -5)), 'melodic minor', 'a dominant on a note outside the key: the melodic minor a 4th below its name')
        assert nxt, ('a dominant needs the chord it goes to', chord)
        nr, nq, _ = chord_parse(nxt)
        if (midi(nr + '4') - midi(r + '4')) % 12 != 5: raise ValueError(f'{chord} does not go up a 4th to {nxt}')
        if FAMILY[nq] in ('maj', 'dom'):
            return ('7a', pc_name(tr(r + '4', -4, -7)), 'major', 'a dominant going to a major chord: the major scale a 5th below its name')
        return ('7b', pc_name(tr(r + '4', -4, -7)), 'harmonic minor', 'a dominant going to a minor chord: the harmonic minor a 5th below its name')
    raise ValueError(f'no rule for {chord}')


# ---------------------------------------------------------------- fingering one line in position
def fingering(notes, near=5, allow_open=False, strings=(6, 5, 4, 3, 2, 1), maxf=15, fix=None):
    """strings and frets for a single line: the hand (index at fret h) covers h..h+3, a stretch of one fret either way
    costs a little, a shift costs more; the hand stays near `near`. fix: {index: (string, fret)}."""
    ms = [midi(n) for n in notes]
    lo = 0 if allow_open else 1
    prev = {}
    hist = []
    for i, m in enumerate(ms):
        cands = [(s, m - OPEN[s]) for s in strings if lo <= m - OPEN[s] <= maxf]
        if fix and i in fix: cands = [fix[i]]
        assert cands, (notes[i], 'cannot be played')
        cur = {}
        for s, f in cands:
            for h in range(1, maxf + 1):
                if f == 0: c0 = 0.0
                else:
                    d = f - h
                    if 0 <= d <= 3: c0 = 0.0
                    elif d in (-1, 4): c0 = 0.7
                    else: continue
                if not prev:
                    cur[(s, f, h)] = (c0 + 0.3 * abs(h - near), None)
                    continue
                best = None
                for (s0, f0, h0), (c1, _) in prev.items():
                    c = (c1 + c0 + (0 if h == h0 else 2.5 + 0.4 * abs(h - h0)) + 0.06 * abs(h - near) + 0.12 * abs(s - s0) + 0.03 * f
                         + (0.6 if s == s0 and abs(f - f0) > 2 else 0))
                    if best is None or c < best[0]: best = (c, (s0, f0, h0))
                cur[(s, f, h)] = best
        prev = cur
        hist.append(cur)
    # walk back
    k = min(hist[-1], key=lambda k: hist[-1][k][0])
    path = [k]
    for i in range(len(hist) - 1, 0, -1):
        k = hist[i][k][1]; path.append(k)
    path.reverse()
    return [(s, f) for s, f, h in path], [h for s, f, h in path]


def run(notes, durs, label, near=5, fix=None, strings=(6, 5, 4, 3, 2, 1), extra=None):
    """a numbered run (R item)"""
    pos, _ = fingering(notes, near=near, fix=fix, strings=strings)
    it = ['R', [list(p) for p in pos], list(durs), '=' + ','.join(disp(n) for n in notes) + '|' + label]
    if extra: it.append(extra)
    return it


def placed(notes, pos, durs, label):
    """a run on given strings and frets (checked: each fret sounds its note)"""
    for n, (s, f) in zip(notes, pos): assert OPEN[s] + f == midi(n), (n, s, f)
    return ['R', [list(p) for p in pos], list(durs), '=' + ','.join(disp(n) for n in notes) + '|' + label]
