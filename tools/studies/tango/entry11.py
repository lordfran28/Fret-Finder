"""Tango melody, the rest of Graciano's ch. 7: paraphrasing a written tune (his ten techniques, pp. 58–60), expression
(pp. 60–62), chromatic notes in a tune (p. 65), a guide line against the tune and Grela's two lines in one guitar
(pp. 74–75), and an étude that puts them together on the whole chorus.

Every exercise works on the chorus of I Wonder Who's Kissing Her Now as the 1909 song has it (tune_iw.py: copied from
the owner's score, a waltz, here in E♭ at the score's pitch). Graciano's own examples are tangos still under copyright
(Troilo's La última curda, Plaza's Nostálgico, Piana's Tinta roja, the Expósitos' Naranjo en flor): they are described,
never written out. Each change to the tune is made by one function per technique and logged; check11.py checks every
logged change against the technique's rule with its own code, and checks the bars against the changed tune.
"""
import sys, copy
sys.path.insert(0, '/home/claude/studies'); sys.path.insert(0, '/home/claude/studies/tango')
import mel as M
import tune_iw as TU
import entry9 as E9
from kit_study import place_lines, two_lines

IW = 'I Wonder Who’s Kissing Her Now'
OWN = 'Graciano’s own'
LOG = []            # every change: dict(ex, kind, params, before, after)
SHOWN = []          # (exercise id, events, bars, b0, b1): the bars drawn for a set of events, for check11
EXS = {}


def where(p): return f'Método de guitarra tango, p. {p}'


def T(text, p): return dict(where=where(p), text=text, whose=OWN, played='', by='Graciano', item=None)


def ex(sec, id, title, idea, quote, bars):
    EXS.setdefault(sec, []).append(dict(id=id, title=title, idea=idea, quote=quote, bars=bars))


# ---------------------------------------------------------------- the tune as events
def bar_start(b): return 0.0 if b == 0 else 1.0 + 3.0 * (b - 1)
def bar_len(b): return 1.0 if b == 0 else 3.0
def bar_of(t): return 0 if t < 1 - 1e-9 else 1 + int((t - 1 + 1e-9) // 3)


def tune_events():
    """the chorus with the second ending: ties joined, each note dict(t, n, d, tag=None)"""
    ev, t, tie = [], 0.0, False
    for b, chs, notes, w in TU.in_eb(ending=2):
        for n, d in notes:
            if n == 'r': t += d; tie = False; continue
            nn = n.rstrip('~')
            if tie and ev and ev[-1]['n'] == nn: ev[-1]['d'] += d
            else: ev.append(dict(t=t, n=nn, d=float(d), tag=None))
            tie = n.endswith('~'); t += d
    return ev


TUNE = tune_events()
CHORDS = []         # (time, chord)
for b, chs, notes, w in TU.in_eb(ending=2):
    for c, at in chs: CHORDS.append((bar_start(b) + at, c))
WORDS = {b: w for b, chs, notes, w in TU.in_eb(ending=2)}


def chord_at(t):
    c = None
    for tt, cc in CHORDS:
        if tt <= t + 1e-9: c = cc
    return c


def key_scale_at(t):
    """the scale for the chord sounding at t, by Graciano's rules (mel.rule_for)"""
    c = chord_at(t)
    nxt = None
    for tt, cc in CHORDS:
        if tt > t + 1e-9 and cc != c: nxt = cc; break
    r = M.rule_for(c, 'Eb', 'major', nxt)
    return r[1], r[2]


def cp(ev): return copy.deepcopy(ev)


def idx_at(ev, t, n=None):
    for i, e in enumerate(ev):
        if abs(e['t'] - t) < 1e-6 and (n is None or e['n'] == n): return i
    raise KeyError((t, n))


def at(b, beat): return bar_start(b) + beat


def log(exid, kind, before, after, **params):
    LOG.append(dict(ex=exid, kind=kind, params=params, before=cp(before), after=cp(after)))
    return after


# ---------------------------------------------------------------- the techniques, one function each
def displace(exid, ev, t0, durs, kind='displace'):
    """notes from time t0 on take new lengths, one after another with no gap: nothing added or taken away"""
    out = cp(ev); i = idx_at(out, t0); t = out[i]['t']
    for k, d in enumerate(durs):
        out[i + k]['t'] = t; out[i + k]['d'] = d; t += d
    return log(exid, kind, ev, out, t0=t0, durs=list(durs))


def delay(exid, ev, moves):
    """moves: [(old onset, new onset, new length)]: notes come in later than written, rests in front of them"""
    out = cp(ev)
    for t_old, t_new, d in moves:
        i = idx_at(out, t_old); out[i]['t'] = t_new; out[i]['d'] = d
    out.sort(key=lambda e: e['t'])
    return log(exid, 'delay', ev, out, moves=moves)


def anticipate(exid, ev, t, by=0.5):
    """the note at t comes in early by `by`, held through its beat; the note before it is cut short to make room"""
    out = cp(ev); i = idx_at(out, t)
    out[i]['t'] -= by; out[i]['d'] += by
    out[i - 1]['d'] = min(out[i - 1]['d'], out[i]['t'] - out[i - 1]['t'])
    return log(exid, 'anticipate', ev, out, t=t, by=by)


def edit(exid, ev, drop):
    out = [e for e in cp(ev) if not any(abs(e['t'] - t) < 1e-6 for t in drop)]
    return log(exid, 'edit', ev, out, drop=list(drop))


def chrom_between(a, b):
    """the semitones strictly between two notes, spelled for E♭: up with ♯ (or the key's own note), down with ♭"""
    ma, mb = M.midi(a), M.midi(b)
    up = mb > ma
    UPN = {0: 'C', 1: 'C#', 2: 'D', 3: 'Eb', 4: 'E', 5: 'F', 6: 'F#', 7: 'G', 8: 'Ab', 9: 'A', 10: 'Bb', 11: 'B'}
    DNN = {0: 'C', 1: 'Db', 2: 'D', 3: 'Eb', 4: 'E', 5: 'F', 6: 'Gb', 7: 'G', 8: 'Ab', 9: 'A', 10: 'Bb', 11: 'B'}
    out = []
    for m in (range(ma + 1, mb) if up else range(ma - 1, mb, -1)):
        name = (UPN if up else DNN)[m % 12]
        o = m // 12 - 1
        n = name + str(o)
        assert M.midi(n) == m
        out.append(n)
    return out


def diat_between(a, b, root='Eb', kind='major'):
    ms = M.scale_notes(root, kind, a if M.midi(a) < M.midi(b) else b, b if M.midi(a) < M.midi(b) else a)
    inner = [n for n in ms if min(M.midi(a), M.midi(b)) < M.midi(n) < max(M.midi(a), M.midi(b))]
    return inner if M.midi(b) > M.midi(a) else list(reversed(inner))


def fill(exid, ev, t, keep, how='chrom'):
    """the leap from the note at t to the next note filled: the note keeps `keep` beats, the fill shares the rest equally"""
    out = cp(ev); i = idx_at(out, t); a, b = out[i], out[i + 1]
    notes = chrom_between(a['n'], b['n']) if how == 'chrom' else diat_between(a['n'], b['n'])
    span = b['t'] - a['t']
    step = (span - keep) / len(notes)
    a['d'] = keep
    new = [dict(t=a['t'] + keep + k * step, n=n, d=step, tag='fill') for k, n in enumerate(notes)]
    out[i + 1:i + 1] = new
    return log(exid, 'fill_' + how, ev, out, t=t, keep=keep)


def neighbour(exid, ev, t, nb, durs):
    """the note at t, then its neighbour, then the note again, in the note's own time"""
    out = cp(ev); i = idx_at(out, t); x = out[i]
    assert abs(sum(durs) - x['d']) < 1e-6
    a = dict(x, d=durs[0]); m = dict(t=x['t'] + durs[0], n=nb, d=durs[1], tag='nb'); c = dict(x, t=x['t'] + durs[0] + durs[1], d=durs[2], tag='back')
    out[i:i + 1] = [a, m, c]
    return log(exid, 'neighbour', ev, out, t=t, nb=nb)


def overshoot(exid, ev, t, d_over):
    """the leap into the note at t goes one step of the scale too far, then comes back to the note"""
    out = cp(ev); i = idx_at(out, t); x = out[i]; prev = out[i - 1]
    root, kind = key_scale_at(x['t'])
    up = M.midi(x['n']) > M.midi(prev['n'])
    over = M.scale_run(root, kind, x['n'], 2, 1 if up else -1)[1]
    a = dict(t=x['t'], n=over, d=d_over, tag='over'); c = dict(x, t=x['t'] + d_over, d=x['d'] - d_over, tag='back')
    out[i:i + 1] = [a, c]
    return log(exid, 'overshoot', ev, out, t=t)


def octave_up(exid, ev, t):
    out = cp(ev); i = idx_at(out, t); out[i]['n'] = M.tr(out[i]['n'], 7, 12)
    return log(exid, 'octave', ev, out, t=t)


def anacrusis(exid, ev, t_target, n_notes=2, each=0.5):
    """notes of the chord's scale climbing by step into a phrase that starts on the downbeat, in the rest before it"""
    out = cp(ev); i = idx_at(out, t_target); x = out[i]
    t0 = t_target - n_notes * each
    root, kind = key_scale_at(t0)
    run = M.scale_run(root, kind, x['n'], n_notes + 1, -1)[1:][::-1]
    new = [dict(t=t0 + k * each, n=n, d=each, tag='ana') for k, n in enumerate(run)]
    out[i:i] = new
    return log(exid, 'anacrusis', ev, out, t=t_target, n=n_notes, each=each)


def mordent(exid, ev, t, small=0.125):
    out = cp(ev); i = idx_at(out, t); x = out[i]
    root, kind = key_scale_at(x['t'])
    nb = M.scale_run(root, kind, x['n'], 2, -1)[1]
    a = dict(x, d=small, tag='mord'); m = dict(t=x['t'] + small, n=nb, d=small, tag='mord'); c = dict(x, t=x['t'] + 2 * small, d=x['d'] - 2 * small, tag='back')
    out[i:i + 1] = [a, m, c]
    return log(exid, 'mordent', ev, out, t=t)


def mark(exid, ev, kind, times, value=True):
    """expression: kind 'acc' (an accent), 'short' (staccato: half its length) or 'slur' (no new stroke: the same string)"""
    out = cp(ev)
    for t in times: out[idx_at(out, t)][kind] = value
    return log(exid, 'mark_' + kind, ev, out, times=list(times))


# ---------------------------------------------------------------- drawing events as bars
def bars_of(exid, ev, b0, b1, label, near=5, note_txt=None, fix=None, held_from_before=None):
    """one run per stretch of notes in a bar; rests and held notes as silence items; one fingering for the whole set"""
    t_lo, t_hi = bar_start(b0), bar_start(b1) + bar_len(b1)
    sel = [e for e in ev if t_lo - 1e-9 <= e['t'] < t_hi - 1e-9]
    notes = [e['n'] for e in sel]
    fx = None
    if fix:
        fx = {}
        for t, sf in fix.items(): fx[next(k for k, e in enumerate(sel) if abs(e['t'] - t) < 1e-6)] = sf
    pos, _ = M.fingering(notes, near=near, fix=fx)
    out = []
    k = 0
    for b in range(b0, b1 + 1):
        s, L = bar_start(b), bar_len(b)
        items, cur, run = [], s, None
        bev = [(j, e) for j, e in enumerate(sel) if s - 1e-9 <= e['t'] < s + L - 1e-9]
        for j, e in bev:
            if e['t'] > cur + 1e-9:
                if run: items.append(run); run = None
                items.append(['W', round(e['t'] - cur, 6)])
                cur = e['t']
            nxt = bev[bev.index((j, e)) + 1][1]['t'] if bev.index((j, e)) + 1 < len(bev) else s + L
            d = min(e['t'] + e['d'], nxt) - e['t']
            if run is None: run = ['R', [], [], [], {}]
            run[1].append(list(pos[j])); run[2].append(round(d, 6)); run[3].append(e['n'])
            for kk in ('acc', 'short', 'slur'):
                run[4].setdefault(kk, []).append(bool(e.get(kk)))
            cur = e['t'] + d
            if d < nxt - e['t'] - 1e-9:
                items.append(run); run = None
        if run: items.append(run)
        if cur < s + L - 1e-9: items.append(['W', round(s + L - cur, 6)])
        fin = []
        for it in items:
            if it[0] != 'R': fin.append(it); continue
            ext = {}
            if any(it[4]['acc']): ext['vel'] = [0.16 if a else (-0.06 if True else 0) for a in it[4]['acc']]
            if any(it[4]['short']): ext['short'] = it[4]['short']
            if any(it[4]['slur']):
                ext.setdefault('vel', [0.0] * len(it[1]))
                ext['vel'] = [v - 0.12 if sl else v for v, sl in zip(ext['vel'], it[4]['slur'])]
            r = ['R', it[1], it[2], '=' + ','.join(M.disp(n) for n in it[3]) + '|' + label]
            if ext: r.append(ext)
            fin.append(r)
        cs = [c for c in [chord_at(s)] + [c for tt, c in CHORDS if s + 1e-9 < tt < s + L - 1e-9] if c]
        out.append(dict(chords=[M.dname(c) for c in cs], items=fin, note=(note_txt or {}).get(b, '')))
    SHOWN.append((exid, sel, out, b0, b1))
    return out


def plain_and(exid, ev, b0, b1, label, txt_plain, txt_new, near=5, fix=None, fix_plain=None):
    """the tune's bars, then the same bars changed"""
    return (bars_of(exid + ':tune', TUNE, b0, b1, 'the tune', near, txt_plain, fix_plain)
            + bars_of(exid, ev, b0, b1, label, near, txt_new, fix))


def bw(b0, b1):
    ws = [WORDS[b] for b in range(b0, b1 + 1) if WORDS.get(b)]
    return '“' + ' '.join(ws).replace('-', '').replace(' ,', ',').strip(' ,;') + '”'


def tune_txt(b0, b1, more=''):
    span = f'the pickup and bars 1–{b1}' if b0 == 0 else f'bars {b0}–{b1}'
    return {b0: f'{IW}, {span} as written: {bw(b0, b1)}.{(" " + more) if more else ""}'}


# ================================================================ paraphrase (pp. 58–60)
PA = 'parafraseo'
INTRO_PA = ('Graciano starts from the fact that a tune is written “flat”, without phrasing, and turns the phrasing of the great players by ear into ten techniques '
            'you can apply to any tune. His example is Troilo’s La última curda (still under copyright, so described here, not written out): its plain melody, '
            'then each technique applied to it with a mark under every changed note. Ours are applied to your chorus, each set of bars first as written, then changed. ')

e = displace('desplazamiento', TUNE, at(1, 0), [1.5, 0.5, 1.0, 1.5, 0.5, 1.0])
e = displace('desplazamiento', e, at(9, 0), [0.5, 1.5, 1.0, 0.5, 1.5, 1.0, 2.5, 0.5])
ex(PA, 'desplazamiento', '1. Rhythmic displacement',
   INTRO_PA + 'The first technique adds no note and takes none away: some notes are held longer and, to balance them, others are made shorter. He counts it among the most used in tango.',
   T('La última curda, with some notes lengthened and others shortened (described only).', 58),
   plain_and('desplazamiento', e, 0, 4, 'displaced', tune_txt(0, 4), {1: 'Each bar’s first note held half a beat longer, the second note cut to half a beat; the third keeps its place. Bar 2 the same.'})
   + plain_and('desplazamiento', e, 9, 12, 'displaced', tune_txt(9, 12), {9: 'The other way round: the first note cut to half a beat, the high note held for a beat and a half.',
                                                                         11: 'F held half a beat longer, E♭ squeezed into the last half beat.'}))

e = delay('retrasado', TUNE, [(at(1, 0), at(1, 0.5), 1.0), (at(1, 1), at(1, 1.5), 0.5), (at(2, 0), at(2, 0.5), 1.0), (at(2, 1), at(2, 1.5), 0.5)])
ex(PA, 'retrasado', '2. Delayed attack',
   'Close to displacement, but rests are put in so that notes come in after the beat: playing with the off-beat.',
   T('La última curda with rests before some notes (described only).', 58),
   plain_and('retrasado', e, 0, 4, 'delayed', tune_txt(0, 4), {1: 'A half-beat rest on the downbeat: G comes in on the “and”, B♭ on the “and” of 2, G back on beat 3.',
                                                                 2: 'The same in bar 2.'}))

e = anticipate('anticipacion', TUNE, at(6, 0))
e = anticipate('anticipacion', e, at(7, 0))
ex(PA, 'anticipacion', '3. Anticipation',
   ('A note comes in half a beat early, before its beat, and is held through it. Graciano says it is found mostly in groups with drums, where a cymbal stroke '
    'backs the early note: a jazz habit that came into tango in the 1960s.'),
   T('La última curda with some notes coming early (described only).', 58),
   plain_and('anticipacion', e, 5, 8, 'anticipated', tune_txt(5, 8), {5: 'D, the first note of bar 6, comes in on the last half beat of bar 5 and is held over the bar line.',
                                                                         6: 'The same with C: it comes in half a beat before bar 7 and is held to the end of the phrase.'}))

e = displace('patron', TUNE, at(1, 0), [0.5, 1.0, 1.5, 0.5, 1.0, 1.5], kind='pattern')
e = displace('patron', e, at(5, 0), [0.5, 1.0, 1.5, 0.5, 1.0, 1.5], kind='pattern')
ex(PA, 'patron', '4. A rhythmic pattern',
   ('One rhythm laid on two segments of a phrase. It lets a whole row of bandoneons or strings play a tune together and still sound phrased. '
    'Here the two segments are “wonder who’s kissing her” and “wonder who’s teaching her”, the same six notes’ worth of rhythm each time.'),
   T('La última curda: the same rhythm laid on segment a and segment b of one phrase (described only).', 58),
   plain_and('patron', e, 1, 8, 'the pattern', tune_txt(1, 8), {1: 'Segment a: short, a beat, long; then the same in bar 2.', 5: 'Segment b: the same rhythm on bars 5 and 6.'}))

e = edit('edicion', TUNE, [at(25, 1), at(25, 2), at(26, 1), at(27, 2)])
ex(PA, 'edicion', '5. Editing and space',
   ('Editing keeps what serves the tune best; the space comes from leaving out the notes that only fill. The notes to keep are the ones that still let you hear the tune: '
    'the chord’s own notes. How many to leave out is your choice; Graciano kept the odd leaning note. Ours keeps only chord notes, each where it was.'),
   T('La última curda with its filling notes taken out (described only).', 59),
   plain_and('edicion', e, 25, 28, 'edited', tune_txt(25, 28, 'Over F minor, D and E♭ are not chord notes; over E♭, D is not.'),
             {25: 'C (the 5th of F minor) kept; D and E♭ left out.', 26: 'F kept, E♭ left out, F (the root of F) kept.', 27: 'G and B♭ kept, D left out.', 28: 'C and G belong to C7: both kept.'}))

e = fill('relleno', TUNE, at(9, 0), 0.25)
e = fill('relleno', e, at(9, 1), 0.25)
e = fill('relleno', e, at(10, 0), 1 / 3)
e = fill('relleno', e, at(10, 1), 1 / 3)
e = fill('relleno', e, at(11, 2), 1 / 3)
e = fill('relleno', e, at(12, 0), 2.0)
ex(PA, 'relleno', '6. Filling a leap',
   ('With displacement, the technique tango uses most: a leap in the tune filled with chromatic notes. A leap means a minor 3rd or more. '
    'Graciano comes back to it under chromatic notes (p. 65) with Piana and Castillo’s Tinta roja, still under copyright, so described only. '
    'The filling notes take their time from the note before the leap; the note after it still lands on its own beat.'),
   T('La última curda, its leaps filled chromatically; on p. 65, Tinta roja the same way (described only).', 59),
   plain_and('relleno', e, 9, 13, 'filled', tune_txt(9, 13),
             {9: 'A♭ to C is a major 3rd: A, B♭, B fill it in sixteenths; C back down to A♭ the same way.',
              10: 'G to B♭ and back are minor 3rds: two notes each, in triplets.',
              11: 'E♭ down to C, a minor 3rd: D and D♭ in a triplet on beat 3.',
              12: 'C up to G, a 5th: six semitones on the last beat, into bar 13.'}))

e2 = fill('relleno-diatonico', TUNE, at(1, 0), 0.5, 'diat')
e2 = fill('relleno-diatonico', e2, at(1, 1), 0.5, 'diat')
e2 = fill('relleno-diatonico', e2, at(2, 0), 1 / 3, 'diat')
e2 = fill('relleno-diatonico', e2, at(2, 1), 1 / 3, 'diat')
ex(PA, 'relleno-diatonico', '6b. Filling a leap with the scale',
   'Graciano adds that a leap can be filled with the notes of the scale instead; it is used less.',
   T('A note under his chromatic fills: diatonic fills are possible too.', 59),
   plain_and('relleno-diatonico', e2, 0, 3, 'filled', tune_txt(0, 3),
             {1: 'G to B♭ and back: A♭, the one note of E♭ major between them, in eighths.', 2: 'F to B♭, a 4th: G and A♭ in a triplet; back down the same.'}))

e = neighbour('vecina', TUNE, at(5, 0), 'D4', [1 / 3, 1 / 3, 1 / 3])
e = neighbour('vecina', e, at(6, 1), 'F#4', [1 / 3, 1 / 3, 1 / 3])
e = neighbour('vecina', e, at(7, 0), 'B3', [1.0, 1.0, 3.0])
ex(PA, 'vecina', '7. The neighbour note',
   ('From a note of the tune to the nearest note beside it and back again. The neighbour can be a note of the scale or a chromatic one, and usually lies below.'),
   T('La última curda with neighbour notes (described only).', 59),
   plain_and('vecina', e, 5, 8, 'neighbours', tune_txt(5, 8),
             {5: 'E♭, D (the scale’s note below), E♭, as a triplet on beat 1.', 6: 'G, F♯ (a semitone below), G, as a triplet on beat 2.', 7: 'The long C: C, then B♮ a semitone below on beat 2, then C held on.'}))

e = overshoot('sobresalto', TUNE, at(1, 0), 0.5)
e = overshoot('sobresalto', e, at(2, 1), 0.5)
ex(PA, 'sobresalto', '8. A wider leap, and back',
   ('Singers use it to show their range; on an instrument it adds tension. The leap is made one step of the scale wider (a 4th becomes a 5th), '
    'then the line comes back to the written note. It can go downward too, less often.'),
   T('La última curda with two leaps widened (described only).', 59),
   plain_and('sobresalto', e, 0, 3, 'wider', tune_txt(0, 3),
             {1: 'B♭ up to G, a 6th, made a 7th: A♭, then back to G.', 2: 'F up to B♭, a 4th, made a 5th: C, then back to B♭.'}))
e3 = overshoot('sobresalto-abajo', TUNE, at(27, 2), 0.5)
e3 = overshoot('sobresalto-abajo', e3, at(29, 2), 0.5)
ex(PA, 'sobresalto-abajo', '8b. Wider leaps up and down',
   'The same in the last phrase, upward once and downward once.',
   T('His note: the wider leap can also go downward, less often.', 59),
   plain_and('sobresalto-abajo', e3, 27, 30, 'wider', tune_txt(27, 30),
             {27: 'B♭ up to D, a 3rd, made a 4th: E♭, then back to D.', 29: 'A♭ down to C, a 6th, made a 7th: B♭, then up to C.'}))

e = octave_up('registro', TUNE, at(12, 0))
e = octave_up('registro', e, at(14, 0))
ex(PA, 'registro', '9. A change of register',
   ('A note of the phrase taken in its upper octave. Graciano credits the bandoneons with it, Eduardo Arolas above all.'),
   T('La última curda with one note taken an octave up (described only).', 59),
   plain_and('registro', e, 9, 16, 'register', tune_txt(9, 16),
             {12: 'C, which the tune takes down a 3rd from E♭, an octave up: a 6th up instead.', 14: 'F, held, an octave up: the line jumps to the top and comes back down to C.'}))

e = anacrusis('anacrusa', TUNE, at(5, 0))
e = anacrusis('anacrusa', e, at(9, 0))
ex(PA, 'anacrusa', '10. A pickup',
   ('Good for phrases that start squarely on the downbeat: a few notes before it lead in. Graciano notes that La última curda already has pickups in its phrases. '
    'Ours climb by step through the chord’s scale into the phrase’s first note, in the rest before it.'),
   T('La última curda: its phrases already lead in with pickups (described only).', 60),
   plain_and('anacrusa', e, 4, 9, 'pickup', tune_txt(4, 9),
             {4: 'In the rest: C, D, climbing in E♭ major into E♭.', 8: 'In the rest: F, G, climbing in F harmonic minor (C7 going to F minor) into A♭.'}))

# ================================================================ expression (pp. 60–62)
EX_ = 'expresion'
e = mark('acentos', TUNE, 'acc', [at(1, 0), at(2, 0), at(3, 0)])
e_w = mark('acentos', TUNE, 'acc', [at(0, 0), at(1, 1), at(2, 1)])
ex(EX_, 'acentos', 'Accents',
   ('Notes alone are not the whole of it: how you play them is the other half. First, accents. Each metre has its own: 4/4 strong, weak, half-strong, half-weak; '
    '3/4 strong, weak, weak; 2/4 strong, weak. Accents written in (>) give the tune another sense. Graciano shows it on Julián Plaza’s Nostálgico, '
    'still under copyright, so described only.'),
   T('Nostálgico as written, then with accents written in (described only).', 60),
   bars_of('acentos:metre', e, 0, 4, 'the metre’s accents', 5, {0: f'{IW}, the pickup and bars 1–4: the accents of 3/4, each downbeat stressed.'})
   + bars_of('acentos', e_w, 0, 4, 'written accents', 5, {0: 'Accents written in on the pickup and on the high B♭s, the 2nd beats; the downbeats left soft.'}))

e = mark('ataque', TUNE, 'short', [at(5, 0), at(5, 1), at(5, 2), at(6, 0), at(6, 1), at(6, 2)])
ex(EX_, 'ataque', 'The attack: legato and picado',
   ('Two ways to sound a note: for its whole length (legato), or cut to half its length (staccato, which tango players call “picado”).'),
   T('Nostálgico as written, then with each note’s attack marked (described only).', 61),
   bars_of('ataque:legato', TUNE, 5, 8, 'legato', 5, {5: f'{IW}, bars 5–8, legato: each note held for its whole length.'})
   + bars_of('ataque', e, 5, 8, 'picado', 5, {5: 'Picado: the quarters cut to half their length, the long C left legato.'}))

e = mark('ligado', TUNE, 'slur', [at(11, 2), at(13, 2), at(15, 2)])
ex(EX_, 'ligado', 'Slurs',
   ('A slur makes the line more supple. On the guitar it means ligados, a hammer-on going up or a pull-off coming down, the second note sounding '
    'without a new stroke; on strings, one bow.'),
   T('Nostálgico as written, then with slurs (described only).', 61),
   bars_of('ligado', e, 9, 16, 'slurred', 5, {9: f'{IW}, bars 9–16. Three falling steps slurred, each pulled off on one string: F to E♭ (bar 11), G to F (bar 13), C to C♭ (bar 15).'},
           fix={at(11, 0): (2, 6), at(11, 2): (2, 4), at(13, 0): (2, 8), at(13, 2): (2, 6), at(15, 0): (1, 8), at(15, 2): (1, 7)}))

e = mordent('mordente', TUNE, at(3, 0))
e = mordent('mordente', e, at(7, 0))
ex(EX_, 'mordente', 'Grace notes: the mordent',
   'Of the grace notes, the mordent is the one tango uses most: the note, the note below it and the note again, fast, at the start of the note.',
   T('Nostálgico as written, then with mordents (described only).', 61),
   plain_and('mordente', e, 0, 8, 'mordents', tune_txt(0, 8),
             {3: 'The long E♭: E♭, D, E♭ in a flash on the downbeat, then held.', 7: 'The long C: C, B♭, C, then held.'}))

# ================================================================ a guide line against the tune (pp. 73–74), and Grela's two lines (p. 75)
GU = 'contracanto'
GUIDE = {'C7': ('E', 'Bb'), 'F7': ('A', 'Eb'), 'Bb7': ('D', 'Ab')}
COUNTER = [(at(10, 0), 'E4', 3.0), (at(11, 0), 'Eb4', 1.0), (at(11, 1), 'A3', 3.0), (at(12, 1), 'Eb3', 1.0), (at(12, 2), 'A3', 2.0),
           (at(13, 1), 'Eb4', 3.0), (at(14, 1), 'A3', 1.0), (at(14, 2), 'Eb4', 1.0), (at(15, 0), 'D4', 1.0), (at(15, 1), 'Ab3', 3.0),
           (at(16, 1), 'D3', 2.0), (at(17, 0), 'Eb3', 3.0)]
COUNTERS = []       # (exercise id, tune events, counter events, t0, t1) for check11


def two_bars(exid, tune, counter, b0, b1, label, notes_txt):
    """two voices, the tune on top: one step wherever either voice moves"""
    out = []
    for b in range(b0, b1 + 1):
        s, L = bar_start(b), bar_len(b)
        ts = sorted({round(e['t'], 6) for e in tune + counter if s - 1e-9 <= e['t'] < s + L - 1e-9} | {s})
        seq, names = [], []
        for k, t in enumerate(ts):
            d = (ts[k + 1] if k + 1 < len(ts) else s + L) - t
            lo = next((c for c in counter if abs(c['t'] - t) < 1e-6), None)
            up = next((u for u in tune if abs(u['t'] - t) < 1e-6), None)
            if not lo and not up:
                if seq: seq[-1] = (seq[-1][0], seq[-1][1], seq[-1][2] + d); continue
            seq.append((M.midi(lo['n']) if lo else None, M.midi(up['n']) if up else None, d))
            names.append('+'.join(M.disp(x['n']) for x in (lo, up) if x) if (lo or up) else '–')
        if seq and seq[0][0] is None and seq[0][1] is None:
            seq = seq[1:]; names = names[1:]
        pl = place_lines(seq, lo_strings=(6, 5, 4, 3), up_strings=(3, 2, 1), maxf=13, prefer=5, open_cost=2.0)
        lead = []
        if ts and not any(abs(e['t'] - s) < 1e-6 for e in tune + counter):
            pass
        it = two_lines(pl, over='=' + ','.join(names) + '|' + label)
        cs = [c for c in [chord_at(s)] + [c for tt, c in CHORDS if s + 1e-9 < tt < s + L - 1e-9] if c]
        out.append(dict(chords=[M.dname(c) for c in cs], items=[it], note=notes_txt.get(b, '')))
    return out


cev = [dict(t=t, n=n, d=d, tag='counter') for t, n, d in COUNTER]
tune_win = [e for e in TUNE if at(10, 0) - 1e-9 <= e['t'] < at(17, 3) - 1e-9]
COUNTERS.append(('contracanto', tune_win, cev, at(10, 0), at(17, 3)))
ex(GU, 'contracanto', 'A guide line against the tune',
   ('Now the guide line is set against the tune itself, not only against the chords. You have to know the tune well, so that the two lines never clash or lean on the same notes: '
    'where the tune is on the beat, the guide line moves off it, and the other way round; where the tune holds a long note the guide line moves, and where the tune moves '
    'the guide line holds. Where the tune itself has the chord’s 3rd or 7th, the guide line does not double it. At the cadence it ends on the key note. '
    'Graciano works it on the Expósito brothers’ Naranjo en flor (still under copyright, described only) and points to the strings and bandoneons of the orchestras, '
    'and to Roberto Grela and Ubaldo De Lío on the guitar.'),
   T('A counter-line of 3rds and 7ths against a tango’s tune, with a table of long against short and on the beat against off it (described only).', 74),
   bars_of('contracanto:tune', TUNE, 10, 17, 'the tune', 5, tune_txt(10, 17))
   + two_bars('contracanto', tune_win, cev, 10, 17, 'two lines', {
       10: 'C7: E, the 3rd, held under the moving tune (its B♭ is the 7th, so the line takes the 3rd).',
       11: 'F7: E♭, the 7th, a semitone down from E; then A, the 3rd, while the tune holds F, so the tune’s E♭ on beat 3 is not doubled.',
       12: 'The tune holds C: the line moves, E♭ and A on beats 2 and 3.',
       13: 'The tune leans on G for two beats: E♭ comes in on beat 2.',
       14: 'The tune holds F: A, then E♭, off the downbeat.',
       15: 'B♭7: E♭ falls a semitone to D, the 3rd; A♭, the 7th, comes in while the tune holds C.',
       16: 'The tune holds B♭, then drops to B♭ below: the line goes under it to D.',
       17: 'E♭: the tune has G, the 3rd, so the line ends on E♭, the key note, a semitone up from D.'}))

GR = [(at(11, 1), 'A3'), (at(12, 1), 'Eb3'), (at(13, 1), 'A3'), (at(14, 1), 'Eb3'), (at(15, 1), 'D3'), (at(16, 1), 'Ab3')]


def grela(exid, ev, pairs):
    """Grela: where the tune holds a long note, the note is cut to a beat and a guide tone sounds below it for the rest of the note's time"""
    out = cp(ev)
    for t, n in pairs:
        i = max(k for k, e in enumerate(out) if e['t'] < t - 1e-9)
        x = out[i]; end = x['t'] + x['d']
        x['d'] = t - x['t']
        out.insert(i + 1, dict(t=t, n=n, d=end - t, tag='guide'))
    return log(exid, 'grela', ev, out, pairs=pairs)


e = grela('grela', TUNE, GR)
ex(GU, 'grela', 'Two lines in one: Grela’s way',
   ('The third use Graciano gives the guide line: making one guitar sound like two lines at once, a way Roberto Grela explored. Where the tune rests or holds a long note, '
    'you slip in guide tones, so a second, lower line seems to run under the tune. Here each long note is cut to one beat and the guide tone follows it, low.'),
   T('Guide tones slipped into a tune where it holds or rests (described only).', 75),
   plain_and('grela', e, 9, 17, 'two lines in one', tune_txt(9, 17),
             {11: 'F for a beat, then A, the 3rd of F7, low, under it; then the tune’s E♭.', 12: 'C, then E♭, the 7th, low.', 13: 'G, then A.', 14: 'F, then E♭.',
              15: 'B♭7: C, then D, the 3rd (E♭ fell a semitone to it); then the tune’s C♭.', 16: 'B♭, then A♭, the 7th, which falls to G when the tune comes back in bar 17.'}))

# ================================================================ étude: the whole chorus
ET = 'etude'
e = TUNE
e = displace(ET, e, at(1, 0), [1.5, 0.5, 1.0, 1.5, 0.5, 1.0], kind='pattern')
e = mark(ET, e, 'acc', [at(1, 1.5), at(2, 1.5)])
e = mordent(ET, e, at(3, 0))
e = displace(ET, e, at(5, 0), [1.5, 0.5, 1.0, 1.5, 0.5, 1.0], kind='pattern')
e = anacrusis(ET, e, at(5, 0))
e = neighbour(ET, e, at(7, 0), 'B3', [1.0, 1.0, 3.0])
e = anacrusis(ET, e, at(9, 0))
e = fill(ET, e, at(9, 0), 0.25)
e = delay(ET, e, [(at(10, 0), at(10, 0.5), 1.0), (at(10, 1), at(10, 1.5), 0.5)])
e = mark(ET, e, 'slur', [at(11, 2)])
e = octave_up(ET, e, at(12, 0))
e = anticipate(ET, e, at(13, 0))
e = neighbour(ET, e, at(14, 0), 'Eb4', [1.0, 1.0, 1.0])
e = mark(ET, e, 'slur', [at(15, 2)])
e = displace(ET, e, at(17, 0), [0.5, 1.5, 1.0, 0.5, 1.5, 1.0])
e = mark(ET, e, 'acc', [at(17, 0.5), at(18, 0.5)])
e = mordent(ET, e, at(19, 0))
e = anacrusis(ET, e, at(25, 0))
e = overshoot(ET, e, at(27, 2), 0.5)
e = mark(ET, e, 'acc', [at(28, 0)])
e = overshoot(ET, e, at(29, 2), 0.5)
e = fill(ET, e, at(30, 1), 1 / 3, 'diat')
ETUDE = e
ET_TXT = {0: 'The whole chorus, second ending, with a few of the techniques at a time, never all at once. The pickup as written.',
          1: 'A rhythmic pattern (long, short, a beat) on “wonder who’s kissing her”, the high B♭ accented…',
          3: '…a mordent on the long E♭…', 4: '…and a pickup, C and D, into the next phrase…',
          5: '…which takes the same pattern: segment b.', 7: 'The long C with its lower neighbour B♮.', 8: 'A pickup, F and G, into A♭…',
          9: '…and the leap from A♭ to C filled chromatically.', 10: 'Delayed attack: G and B♭ come in after the beat.', 11: 'F slurred down to E♭.',
          12: 'C taken an octave up…', 13: '…and G anticipated: it comes in half a beat before bar 13.', 14: 'The long F with its lower neighbour E♭.',
          15: 'C slurred down to C♭.', 16: 'As written.', 17: 'Rhythmic displacement: short first notes, long high ones, accented on the “and”.',
          19: 'A mordent on the long E♭.', 21: 'As written: space before the last phrase.', 24: 'A pickup, A♭ and B♭, into “wonder if”.',
          27: 'The leap from B♭ to D made wider: E♭, then back to D.', 28: 'The high C accented and held.', 29: 'The leap down from A♭ to C made wider: B♭, then C.',
          30: 'F to B♭ filled with the scale: G and A♭.', 31: 'And home, plain.'}
ETUDE_BARS = bars_of(ET, ETUDE, 0, 32, 'the étude', 5, ET_TXT, fix={at(11, 0): (2, 6), at(11, 2): (2, 4), at(15, 0): (1, 8), at(15, 2): (1, 7)})
ETUDES = [dict(id='etude', title='Étude: the chorus paraphrased',
               idea=('Graciano’s advice for both the paraphrase and the expression: take a tune you know well and write out the techniques on it, play what you wrote, '
                     'then vary it and improvise on it until it comes by itself. He ends the expression pages with Nostálgico using all of them together '
                     '(still under copyright, described only). Here is one written-out version of your chorus to start from; each bar says what it does.'),
               quote=T('Write the paraphrase, play it, then improvise on what you wrote; Nostálgico with every expression technique at once (described only).', 60),
               bars=ETUDE_BARS)]

NEW_SECTIONS = [dict(id='parafraseo', title='Paraphrasing the tune', part='Exercises', ex=EXS['parafraseo']),
                dict(id='expresion', title='Expression', part='Exercises', ex=EXS['expresion'])]
GUIDE_EXTRA = EXS['contracanto']
SECTIONS = []
for S in E9.SECTIONS:
    if S['id'] == 'escala': SECTIONS += NEW_SECTIONS
    S2 = dict(S)
    if S['id'] == 'guias': S2['ex'] = S['ex'] + GUIDE_EXTRA
    SECTIONS.append(S2)
SECTIONS.append(dict(id='etudes', title='Étude', part='Études', ex=ETUDES))
from quotes import trim as _trim_quotes
_trim_quotes(SECTIONS)
