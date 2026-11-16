"""Tango: the guitar alone. Graciano, Método de guitarra tango, ch. 8 ("La guitarra solista", pp. 83–86 of the owner's
copy): the guitar as a small orchestra. First the tune an octave up on the top strings; then the tune over the plainest
chord; then the tune over a bass line (root, 3rd and 5th, the 2nd passing, the 7th on dominants going to the next
chord's 3rd); then the chords dressed up (inversions, soli in two or three parts, his harmonic turns); then the three
mixed. His example is the introduction of Gardel and Razzano's Mano a mano, still under copyright: described, never
written out. Ours is the chorus of I Wonder Who's Kissing Her Now (the 1909 waltz, tune_iw.py) in E♭.

Every note is fingered by solo.py (one string each, the tune on top on the first three strings, the hand within four
frets, five from the 7th up, four fingers at most) and check12.py checks the fingering and the rule of each part with
its own code.
"""
import sys
sys.path.insert(0, '/home/claude/studies'); sys.path.insert(0, '/home/claude/studies/tango')
import mel as M
import solo as S
import entry11 as E11

IW = 'I Wonder Who’s Kissing Her Now'
OWN = 'Graciano’s own'
EXS = {}
SHOWN = []          # (exercise id, kind, bars data) for check12: kind and per bar (bar number, events, positions, chord segments)
TUNE = E11.TUNE


def where(p): return f'Método de guitarra tango, p. {p}'
def T(text, p): return dict(where=where(p), text=text, whose=OWN, played='', by='Graciano', item=None)


def ex(sec, id, title, idea, quote, bars):
    EXS.setdefault(sec, []).append(dict(id=id, title=title, idea=idea, quote=quote, bars=bars))


bs, bl = E11.bar_start, E11.bar_len


def mel_events(b):
    s, L = bs(b), bl(b)
    return [dict(t=e['t'] - s, n=e['n'], d=e['d'], role='mel') for e in TUNE if s - 1e-9 <= e['t'] < s + L - 1e-9]


def chords_in(b):
    s, L = bs(b), bl(b)
    out = []
    for tt, c in E11.CHORDS:
        if s - 1e-9 <= tt < s + L - 1e-9: out.append((tt - s, c))
    if not out or out[0][0] > 1e-9:
        c0 = E11.chord_at(s)
        if c0: out.insert(0, (0.0, c0))
    return out


def lowest_mel_during(b, t0, t1):
    """the lowest tune note sounding between t0 and t1 of bar b (notes carried in from before count)"""
    s = bs(b)
    ms = [M.midi(e['n']) for e in TUNE if e['t'] < s + t1 - 1e-9 and e['t'] + e['d'] > s + t0 + 1e-9]
    return min(ms) if ms else 80


SPELL = {'Eb': ['Eb', 'G', 'Bb'], 'G': ['G', 'B', 'D'], 'Ab': ['Ab', 'C', 'Eb'], 'C7': ['C', 'E', 'G', 'Bb'], 'Fm': ['F', 'Ab', 'C'],
         'F7': ['F', 'A', 'C', 'Eb'], 'Bb7': ['Bb', 'D', 'F', 'Ab'], 'F': ['F', 'A', 'C']}


# ---------------------------------------------------------------- drawing
def items_for(evs, pos, L, label):
    order = sorted(range(len(evs)), key=lambda i: (evs[i]['t'], M.midi(evs[i]['n'])))
    ts = sorted({round(evs[i]['t'], 6) for i in order})
    items = []
    if not ts: return [['W', L]]
    if ts[0] > 1e-9: items.append(['W', ts[0]])
    only_mel = all(e['role'] == 'mel' for e in evs)
    if only_mel:
        run = None
        for k, t in enumerate(ts):
            i = next(i for i in order if abs(evs[i]['t'] - t) < 1e-6)
            nxt = ts[k + 1] if k + 1 < len(ts) else L
            d = min(evs[i]['d'], nxt - t)
            if run is None: run = ['R', [], [], []]
            run[1].append(list(pos[i])); run[2].append(round(d, 6)); run[3].append(evs[i]['n'])
            if d < nxt - t - 1e-9:
                items.append(run); run = None; items.append(['W', round(nxt - t - d, 6)])
        if run: items.append(run)
        return [['R', r[1], r[2], '=' + ','.join(M.disp(n) for n in r[3]) + '|' + label] if r[0] == 'R' else r for r in items]
    groups, durs, names = [], [], []
    for k, t in enumerate(ts):
        idx = [i for i in order if abs(evs[i]['t'] - t) < 1e-6]
        groups.append([list(pos[i]) for i in idx]); durs.append(round((ts[k + 1] if k + 1 < len(ts) else L) - t, 6))
        names.append('+'.join(M.disp(evs[i]['n']) for i in idx))
    items.append(['P', groups, durs, '=' + ','.join(names) + '|' + label])
    return items


def draw(exid, kind, specs, label, notes_txt, beam=10):
    """specs: [(bar, [alternative event lists], chord segments)] -> page bars; the fingering chosen over all the bars"""
    lens = [bl(b) for b, alts, segs in specs]
    chosen = S.arrange_alts([alts for b, alts, segs in specs], lens, beam=beam)
    out, data = [], []
    for (b, alts, segs), (ai, pos) in zip(specs, chosen):
        evs = alts[ai]
        out.append(dict(chords=[M.dname(c) for t, c in chords_in(b)], items=items_for(evs, pos, bl(b), label), note=notes_txt.get(b, '')))
        data.append((b, evs, pos, segs))
    SHOWN.append((exid, kind, data))
    return out


def txt(b0, b1, more=''):
    span = f'the pickup and bars 1–{b1}' if b0 == 0 else f'bars {b0}–{b1}'
    return f'{IW}, {span}{(": " + more) if more else "."}'


# ================================================================ 1. the tune on the top strings (p. 84)
SEC = 'solista'
specs = [(b, [mel_events(b)], []) for b in range(0, 33)]
ex(SEC, 'arriba', 'The tune an octave up, on the top strings',
   ('Graciano treats the guitar alone as a small orchestra: you need the tune and its basic harmony, nothing more. He gives three cases: a guitar with a singer, '
    'where this material makes the introduction and an interlude between verse and chorus; a guitar with another instrument, where it makes the four to eight bars '
    'the guitar plays alone; and the guitar as the only instrument, where it runs through the whole piece. His example is the introduction of Gardel and Razzano’s '
    'Mano a mano (still under copyright, described only). The first step: play the tune an octave above where a singer’s part is written, since the guitar sounds '
    'an octave lower than it reads, so the tune sits on the top three strings, mostly the 1st and 2nd. He wants it read that way at sight, without writing it out.'),
   T('Mano a mano’s introduction, the tune an octave up on the first strings (described only).', 84),
   draw('arriba', 'mel', specs, 'the tune', {0: txt(0, 32, 'the whole chorus on the 1st, 2nd and 3rd strings, a singer’s written notes read an octave up.')}))


# ================================================================ 2. the tune over the plainest chord (p. 84)
def chord_alts(b, size_pref=(3, 2), extra_need=()):
    """the tune of bar b with each chord of the bar struck under it, root lowest, held to the next chord or the bar's end"""
    mel = mel_events(b)
    segs = chords_in(b)
    per_seg = []
    for k, (t, c) in enumerate(segs):
        t1 = segs[k + 1][0] if k + 1 < len(segs) else bl(b)
        top = lowest_mel_during(b, t, t1)
        names = SPELL[c]
        in_mel = {M.pc(e['n']) for e in mel if t - 1e-9 <= e['t'] < t1 - 1e-9}
        need = [x for x in names[1:2] + names[3:4] if M.midi(x + '4') % 12 not in in_mel]       # the 3rd, and a dominant's 7th
        vs = []
        for size in size_pref + (4,):
            vs += [v for v in S.voicings(names, names[0], size, top, need=need) if M.midi(v[0]) <= 57][:10]
        per_seg.append([[dict(t=t, n=n, d=t1 - t, role='acc') for n in v] for v in vs])
    from itertools import product
    alts = [mel + [e for part in combo for e in part] for combo in product(*per_seg)][:40]
    return alts, segs


specs = []
for b in range(1, 18):
    alts, segs = chord_alts(b)
    specs.append((b, alts, segs))
ex(SEC, 'acorde', 'The tune over the plainest chord',
   ('Next, lay the plainest guitar chord under the tune. How often you strike it depends on how many chords the bar has; with one chord to the bar, Graciano strikes it in '
    'halves (pesante) or as a marcatto in two, as far as the fingering lets the tune and the chord sit together. In a waltz bar that means the chord once, on the downbeat, '
    'held under the tune. Each chord here has its root at the bottom and the tune on top.'),
   T('Mano a mano’s introduction with the plainest chord under the tune, in halves (described only).', 84),
   draw('acorde', 'chord', specs, 'tune and chord', {1: txt(1, 17, 'each chord on the downbeat, its root lowest, held under the tune.'),
                                                       4: 'Where the tune is held over the bar line, the chord comes in under it alone.'}))

# ================================================================ 3. the tune over a bass line (p. 85)
BASS = {1: [('Eb3', 2), ('Bb2', 1)], 2: [('G2', 2), ('Bb2', 1)], 3: [('Eb3', 3)], 4: [('Bb2', 2), ('G2', 1)], 5: [('Eb3', 2), ('F3', 1)],
        6: [('G3', 2), ('B2', 1)], 7: [('C3', 2), ('Ab2', 1)], 8: [('G2', 2), ('Bb3', 1)], 9: [('Ab3', 2), ('F3', 1)], 10: [('C3', 2), ('Bb2', 1)],
        11: [('A2', 2), ('C3', 1)], 12: [('F2', 2), ('G2', 1)], 13: [('A2', 2), ('C3', 1)], 14: [('F2', 2), ('Eb3', 1)], 15: [('D3', 2), ('Bb2', 1)],
        16: [('F3', 2), ('Ab2', 1)], 17: [('G2', 3)]}
BASS_TXT = {1: txt(1, 17, 'the tune over a bass line in halves and quarters: root, 3rd and 5th, the 2nd passing, the 7th on the dominants.'),
            5: 'F, the 2nd, passing from E♭ to G.', 6: 'G major: its root, then B, its 3rd, leading to C.', 7: 'A♭ with C, its 3rd, in the bass first.',
            8: 'C7: G, then B♭, its 7th…', 9: '…which falls to A♭, the 3rd of F minor.', 10: 'C7 again: its 7th B♭…', 11: '…falls to A, the 3rd of F7.',
            12: 'G, the 2nd, passing from F to A.', 14: 'E♭, the 7th of F7…', 15: '…falls to D, the 3rd of B♭7.', 16: 'A♭, the 7th of B♭7…', 17: '…falls to G, the 3rd of E♭.'}


def bass_events(b):
    t, out = 0.0, []
    for n, d in BASS[b]:
        out.append(dict(t=t, n=n, d=float(d), role='acc')); t += d
    return out


specs = [(b, [mel_events(b) + bass_events(b)], chords_in(b)) for b in range(1, 18)]
ex(SEC, 'bajos', 'The tune over a bass line',
   ('Now only the tune and a bass line under it. The bass takes the root, the 3rd and the 5th of every chord, with the 2nd as a passing note; on a dominant chord it adds '
    'the 7th, and the dominant’s 7th always goes down to the 3rd of the chord it resolves to. In halves and quarters rather than anything busier.'),
   T('Mano a mano’s introduction, the tune over its bass line in halves and quarters (described only).', 85),
   draw('bajos', 'bass', specs, 'tune and bass', BASS_TXT))


# ================================================================ 4. dressing the chords (pp. 85–86)
PCS = dict(SPELL, Dm7b5=['D', 'F', 'Ab', 'C'], Adim7=['A', 'C', 'Eb', 'Gb'], Ddim7=['D', 'F', 'Ab', 'Cb'], B7=['B', 'D#', 'F#', 'A'])


def scale_third_below(n, chord, nxt):
    """the note a 3rd below n in the chord's scale (Graciano's rule for the chord, mel.rule_for)"""
    r = M.rule_for(chord, 'Eb', 'major', nxt)
    return M.scale_run(r[1], r[2], n, 3, -1)[2]


def seg_alts(b, segs, soli=None, sizes=(3, 4, 2, 1)):
    """segs: [(t, d, name, bass, tag)]: a chord struck at t under the tune, `bass` lowest; soli: [(t, d, how)]: a voice under the tune"""
    mel = mel_events(b)
    fixed, per = [], []
    for t, d, how in (soli or []):
        for e in mel:
            if t - 1e-9 <= e['t'] < t + d - 1e-9:
                fixed.append(dict(t=e['t'], n=how(e['n']), d=e['d'], role='acc', tag='soli'))
    for t, d, name, bass, tag in segs:
        top = min([lowest_mel_during(b, t, t + d)] + [M.midi(f['n']) for f in fixed if f['t'] < t + d - 1e-9 and f['t'] + f['d'] > t + 1e-9])
        in_mel = {M.pc(e['n']) for e in mel if e['t'] < t + d - 1e-9 and e['t'] + e['d'] > t + 1e-9}
        names = PCS[name]
        need = [x for x in names[1:2] + names[3:4] if M.midi(x + '4') % 12 not in in_mel] if tag in ('basic', 'inv1') and name in SPELL else []
        if tag == 'dim' and M.midi(names[3] + '4') % 12 not in in_mel: need = [names[3]]          # the flat 9th that makes it diminished
        bass_pc, bass_oct = (bass[:-1], int(bass[-1])) if bass[-1].isdigit() else (bass, None)
        vs = []
        chord_pcs = {M.midi(x + '4') % 12 for x in names}
        by_size = []
        for size in ((1,) if tag == 'bass' else sizes):
            lst = []
            for v in S.voicings(names, bass_pc, size, top, need=need):
                if M.midi(v[0]) > 59 or (bass_oct is not None and v[0] != bass): continue
                if tag not in ('bass', 'basic') and len({M.pc(x) for x in v} | (in_mel & chord_pcs)) < 3: continue   # the chord must be heard
                lst.append(v)
            by_size.append(lst)
        k = 0
        while len(vs) < 10 and any(k < len(l) for l in by_size):          # a few of each size, smallest spread first
            for l in by_size:
                if k < len(l) and len(vs) < 10: vs.append(l[k])
            k += 1
        per.append([[dict(t=t, n=n, d=d, role='acc', tag=tag, chord=name) for n in v] for v in vs])
    from itertools import product
    alts = [mel + fixed + [e for part in combo for e in part] for combo in product(*per)][:160]
    return alts


D = {}          # bar -> (segments, soli, note)
D[9] = ([(0, 2, 'Fm', 'F', 'basic'), (2, 1, 'Dm7b5', 'D', 'm7b5')], None,
        'F minor, plain; on beat 3 D minor 7 flat 5 in its place (the same notes as F minor 6 with D below): Graciano puts a half-diminished chord a minor 3rd under a minor chord in its place.')
D[10] = ([(0, 3, 'C7', 'C', 'bass')], [(0, 3, lambda n: scale_third_below(n, 'C7', 'F7'))],
         'C7: the tune in two parts, a 3rd under it all the way (E under G, G under B♭), over C in the bass.')
D[11] = ([(0, 2, 'F7', 'F', 'basic'), (2, 1, 'F7', 'A', 'inv1')], None, 'F7 plain, then with A, its 3rd, in the bass: the first inversion.')
D[12] = ([(0, 3, 'Adim7', 'A', 'dim')], None,
         'The tune holds C. In place of F7, the diminished chord on its 3rd: A, C, E♭, G♭, which is F7 with a flat 9th and no F.')
D[13] = ([(0, 3, 'F7', 'F', 'bass')], [(0, 3, lambda n: scale_third_below(n, 'F7', 'Bb7'))], 'F7: the tune in two parts again, E♭ under G, D under F.')
D[14] = ([(0, 1, 'F7', 'F', 'basic'), (1, 2, 'B7', 'B', 'tritone')], None,
         'F7, then B7 (C♭7), its tritone substitute, under the held F, which is its raised 11th. It slides down a semitone into B♭7.')
D[15] = ([(0, 2, 'Bb7', 'Bb', 'basic'), (2, 1, 'Ddim7', 'D', 'dim')], None, 'B♭7 under C, its 9th; on C♭, the diminished chord on D: B♭7 with a flat 9th.')
D[16] = ([(0, 1, 'Eb', 'Bb', 'cadential'), (1, 2, 'Bb7', 'Bb', 'basic')], None,
         'A cadence added: E♭ with B♭ at the bottom, then B♭7 on the same bass, going home to E♭.')
D[17] = ([(0, 2, 'Eb', 'Eb', 'basic'), (2, 1, 'Eb', 'G', 'inv1')], None, 'Home: E♭ plain, then with G at the bottom.')
specs = [(b, seg_alts(b, D[b][0], D[b][1]), D[b]) for b in range(9, 18)]
ex(SEC, 'adornos', 'Dressing up the chords',
   ('Then the harmony is dressed up: chords in inversion, a chromatic leaning chord, the tune played in two or three parts like a soli section, or any of the harmonic turns '
    'from his harmony chapter. In his eight bars of Mano a mano he names what each bar does: plain chords and first inversions, the tune in two and three parts, '
    'a dominant a semitone above the dominant it leads to, a diminished chord and the same chord with another note at the bottom, a tritone substitute, a half-diminished chord in place of a minor one, '
    'and a cadence added at the end (described only; the bars are his). Here the same tools on the chorus’s third phrase, one or two to a bar.'),
   T('Mano a mano’s introduction with each bar’s chords dressed up, every bar’s devices named (described only).', 86),
   draw('adornos', 'dressed', specs, 'dressed up', {b: (txt(9, 17) + ' ' if b == 9 else '') + D[b][2] for b in D}))

# ================================================================ étude: the three mixed (p. 86)
for b, segs in {18: [('Bb2', 2), ('G2', 1)], 19: [('Eb3', 3)], 20: [('Bb2', 2), ('G2', 1)], 21: [('Eb3', 2), ('F3', 1)], 22: [('G3', 2), ('B2', 1)],
                23: [('C3', 2), ('Ab2', 1)], 24: [('G2', 2), ('Bb2', 1)]}.items():
    BASS[b] = segs
D2 = {25: ([(0, 3, 'Fm', 'Ab2', 'inv1')], None, 'F minor with A♭ at the bottom: B♭, the 7th of C7, has gone down to it.'),
      26: ([(0, 2, 'Fm', 'Ab2', 'inv1'), (2, 1, 'F', 'A2', 'inv1')], None, 'F minor still over A♭, then F major with A at the bottom: the bass climbs A♭, A, as the 1909 song has it.'),
      27: ([(0, 1, 'Eb', 'Bb2', 'inv2')], None, 'E♭ with B♭ at the bottom, struck with G on the downbeat, the bass still climbing; then the hand lets it go and climbs with the tune.'),
      28: ([(0, 3, 'C7', 'C', 'basic')], None, 'C7, the high C held as long as you like.'),
      29: ([(0, 3, 'Fm', 'F', 'basic')], None, 'F minor.'),
      30: ([(0, 3, 'Bb7', 'Bb', 'basic')], None, 'B♭7.'),
      31: ([(0, 3, 'Eb', 'Eb', 'basic')], None, 'E♭, and the tune held to the end.'),
      32: ([], None, '')}
ET_SPECS = []
for b in range(0, 33):
    if b == 0: ET_SPECS.append((b, [mel_events(b)], ('mel',))); continue
    if 1 <= b <= 8:
        alts, segs = chord_alts(b); ET_SPECS.append((b, alts, ('chord', segs))); continue
    if 9 <= b <= 17:
        ET_SPECS.append((b, seg_alts(b, D[b][0], D[b][1]), ('dressed', D[b]))); continue
    if 18 <= b <= 24:
        ET_SPECS.append((b, [mel_events(b) + bass_events(b)], ('bass', chords_in(b)))); continue
    ET_SPECS.append((b, seg_alts(b, D2[b][0], D2[b][1]) if D2[b][0] else [mel_events(b)], ('dressed', D2[b])))
ET_TXT = {0: txt(0, 32, 'the three ways mixed, as Graciano asks: plain chords for the first two phrases, the dressed-up chords for the third, a bass line for the fourth, '
                        'and the last with inversions that let the bass climb.'),
          1: 'The tune over the plainest chords…', 9: '…the chords dressed up (as in the exercise before)…',
          18: '…the tune over a bass line, the 7ths going down to the next 3rds…', 24: 'B♭, C7’s 7th, falls to A♭.'}
ET_TXT.update({b: D2[b][2] for b in D2 if D2[b][2]})
ETUDE = [dict(id='solista-etude', title='Étude: the chorus for the guitar alone',
              idea=('Graciano’s three ways, the tune with the plainest chord, the tune with a bass line, and the tune with dressed-up chords, mixed clearly through a whole piece. '
                    'For an introduction or an interlude you use few of them; for a whole piece alone you use everything, and your own invention on top.'),
              quote=T('Mix the three clearly; few resources for an introduction, all of them for a whole piece alone.', 86),
              bars=draw('solista-etude', 'etude', ET_SPECS, 'the guitar alone', ET_TXT))]

SECTIONS = [dict(id='solista', title='The guitar alone', part='Exercises', ex=EXS['solista']),
            dict(id='etudes', title='Étude', part='Études', ex=ETUDE)]
from quotes import trim as _trim_quotes
_trim_quotes(SECTIONS)
