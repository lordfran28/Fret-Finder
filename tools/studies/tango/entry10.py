"""Tango melodic patterns: Graciano, Método de guitarra tango, ch. 7 ("Patrones melódicos"), pp. 75–79 of the owner's
copy: scale patterns, scale with arpeggio, intervals, chord notes with a chromatic approach, diatonic triads and
diatonic 7th chords.

Graciano writes each pattern as a drill up and down C major and asks for it in all twelve keys and in minor; and he
says the art is to apply the patterns to each chord change, over the scale that goes with that chord. Ours do that:
each pattern's shape runs over a few bars of one of the owner's songs, each chord taking its own scale by his rules
(entry9, mel.rule_for), each chord's first group starting on one of its own notes. His drills are quoted by their
first two beats only. check10.py checks every group of ours against the pattern's shape.
"""
import sys
sys.path.insert(0, '/home/claude/studies'); sys.path.insert(0, '/home/claude/studies/tango')
import mel as M

OWN = 'Graciano’s own'
EXS = {}
LINES = []
IW = 'I Wonder Who’s Kissing Her Now'
OCI = 'Очи чёрные'
YVL = 'Я вас любил'


def where(p): return f'Método de guitarra tango, p. {p}'


def ex(sec, id, title, idea, quote, bars):
    EXS.setdefault(sec, []).append(dict(id=id, title=title, idea=idea, quote=quote, bars=bars))


def Q(text, p, notes, durs):
    """his first two beats, at sounding pitch (an octave under his treble clef)"""
    return dict(where=where(p), text=text, whose=OWN, played='', by='Graciano', items=[M.run(notes, durs, 'his notes', near=3)])


def scale_of(chord, key, mode, nxt):
    r = M.rule_for(chord, key, mode, nxt)
    return r[1], r[2], r[0]


def sc_list(root, kind): return M.scale_notes(root, kind, 'E2', 'C6')


def shapes_cycle(shapes, k): return shapes[k % len(shapes)]


def snap(anchor_pc_note, chord, root, kind, shape0, direction):
    """the anchor nearest the sequence's next anchor (moving on in the pattern's direction first) whose first note is the chord's own"""
    sc = sc_list(root, kind)
    m = M.midi(anchor_pc_note)
    base = min(range(len(sc)), key=lambda i: (abs(M.midi(sc[i]) - m), -direction * M.midi(sc[i])))
    for k in (0, 1, -1, 2, -2, 3):
        i = base + k * direction
        if 0 <= i + shape0 < len(sc) and 0 <= i < len(sc) and M.is_tone(sc[i + shape0], chord): return sc[i]
    raise ValueError(f'no anchor for {chord} near {anchor_pc_note}')


def pattern(chords, shapes, rhythm, step, start, key, mode='major'):
    """chords: [(chord, beats, next chord)]; shapes: offsets in scale steps from each group's anchor (cycled);
    rhythm: the durations of one group's notes; step: the anchor moves by this many scale steps a group.
    Returns one segment per chord: dict(chord, notes, durs, groups=[(anchor, shape)], root, kind)."""
    segs, anchor = [], start
    gl = sum(rhythm)
    k = 0
    for ci, (chord, beats, nxt) in enumerate(chords):
        root, kind, rule = scale_of(chord, key, mode, nxt)
        sc = sc_list(root, kind)
        sh0 = shapes_cycle(shapes, k)[0]
        if ci == 0:
            i0 = sc.index(start)
            anchor = start if M.is_tone(sc[i0 + sh0], chord) else snap(start, chord, root, kind, sh0, step)
        elif chord != chords[ci - 1][0]:
            anchor = snap(anchor, chord, root, kind, sh0, step)
        notes, durs, groups = [], [], []
        n_groups = round(beats / gl)
        assert abs(n_groups * gl - beats) < 1e-9, (chord, beats, gl)
        for g in range(n_groups):
            shp = shapes_cycle(shapes, k)
            i = sc.index(anchor)
            notes += [sc[i + o] for o in shp]; durs += list(rhythm)
            groups.append((anchor, shp)); k += 1
            anchor = sc[i + step]
        segs.append(dict(chord=chord, notes=notes, durs=durs, groups=groups, root=root, kind=kind, rule=rule, key=key, mode=mode, nxt=nxt))
    return segs, anchor


def to_bars(id_, segs, bar_beats, txts, near=6, label_extra=''):
    """segments laid into bars (a chord never crosses a bar line here), one fingering for the whole exercise"""
    allnotes = [n for s in segs for n in s['notes']]
    pos, _ = M.fingering(allnotes, near=near)
    k, out, cur, t = 0, [], [], 0.0
    for s in segs:
        p = pos[k:k + len(s['notes'])]; k += len(s['notes'])
        cur.append(('R', s, p)); t += sum(s['durs'])
        LINES.append((id_, len(out), s))
        if t >= bar_beats - 1e-9:
            assert abs(t - bar_beats) < 1e-9, (id_, t)
            out.append(cur); cur, t = [], 0.0
    assert not cur, (id_, 'a bar is not full')
    bars = []
    for b, txt in zip(out, txts):
        items, chords = [], []
        for _, s, p in b:
            items.append(['R', [list(x) for x in p], s['durs'], '=' + ','.join(M.disp(n) for n in s['notes']) + '|over ' + M.dname(s['chord'])])
            if s['chord'] not in chords: chords.append(s['chord'])
        bars.append(dict(chords=chords, items=items, note=txt))
    assert len(out) == len(txts), (id_, len(out), len(txts))
    return bars


E8 = [0.5]
def pat_ex(sec, id_, title, idea, quote, parts, txts, bar_beats=4, near=6):
    segs = []
    for p in parts:
        s, _ = pattern(**p)
        for x in s: x['shapes'] = p['shapes']; x['step'] = p['step']; x['rhythm'] = p['rhythm']
        segs += s
    ex(sec, id_, title, idea, quote, to_bars(id_, segs, bar_beats, txts, near))


# the song stretches
IW_1_2 = [('Eb', 4, None), ('Bb7', 4, 'Eb')]
IW_5_6 = [('Cm7', 4, None), ('G7', 4, 'Cm7')]           # (as a dominant going to C minor: bar 6's G7 heads for C minor)
IW_9_10 = [('Fm7', 4, None), ('C7', 4, 'F7')]
IW_13_14 = [('Cm7', 4, None), ('F7', 4, 'Bb7')]
IW_17_18 = [('Eb', 4, None), ('G7', 4, 'Cm7')]
IW_24_25 = [('Fm7', 4, None), ('Fm7', 2, None), ('Db9', 2, 'Cm7')]
IW_26_27 = [('Cm7', 4, None), ('Gm7', 2, None), ('C7', 2, 'Fm7')]
IW_29_30 = [('Fm7', 4, None), ('Bb7', 4, 'Eb')]
OC_1_2 = [('E7', 4, 'Am'), ('E7', 4, 'Am')]
OC_9_10 = [('Dm', 4, None), ('Dm', 4, None)]
OC_13_14 = [('E7', 4, 'Am'), ('E7', 4, 'Am')]
YV_1_4 = [('G', 3, None), ('C', 3, None), ('Cm6', 3, None), ('D', 3, 'G')]

# ================================================================ scale patterns (pp. 75–76)
S = 'escalares'
pat_ex(S, 'e1', 'Up three, back to the first',
       'Groups of four eighths: three notes up the scale and back to the first; each group starts a step higher.',
       Q('Up C major from C: C D E C, D E F D, and so on to the top.', 75, ['C3', 'D3', 'E3', 'C3'], [0.5] * 4),
       [dict(chords=IW_1_2, shapes=[[0, 1, 2, 0]], rhythm=[0.5] * 4, step=1, start='Eb4', key='Eb')],
       [f'{IW}, bars 1–2. E♭, in E♭ major: from the root, each group a step higher.', 'B♭7: the groups go on climbing in the same scale, from A♭, its 7th.'])

pat_ex(S, 'e2', 'Down three, back to the first',
       'The same downward: three notes down and back to the first; each group starts a step lower.',
       Q('Down C major from C.', 75, ['C4', 'B3', 'A3', 'C4'], [0.5] * 4),
       [dict(chords=IW_5_6, shapes=[[0, -1, -2, 0]], rhythm=[0.5] * 4, step=-1, start='Eb5', key='Eb')],
       [f'{IW}, bars 5–6. C minor 7, in E♭ major: from E♭, its 3rd, each group a step lower.',
        'G7, on its way to C minor: C harmonic minor (his rule), its first group from one of its own notes.'])

pat_ex(S, 'e3', 'A 3rd up, back by step',
       'Up a 3rd, then back down by step to where it began; each group a step higher.',
       Q('C E D C, D F E D, …', 76, ['C3', 'E3', 'D3', 'C3'], [0.5] * 4),
       [dict(chords=OC_1_2, shapes=[[0, 2, 1, 0]], rhythm=[0.5] * 4, step=1, start='E4', key='A', mode='minor')],
       [f'{OCI}, bars 1–2. E7, in A harmonic minor: from E.', 'E7 still, climbing.'])

pat_ex(S, 'e4', 'A 3rd down, back by step',
       'Down a 3rd, then back up by step; each group a step lower.',
       Q('C A B C, B G A B, …', 76, ['C4', 'A3', 'B3', 'C4'], [0.5] * 4),
       [dict(chords=IW_9_10, shapes=[[0, -2, -1, 0]], rhythm=[0.5] * 4, step=-1, start='C5', key='Eb')],
       [f'{IW}, bars 9–10. F minor 7, in E♭ major: from C, its 5th.', 'C7, going to F: F major (his rule for a dominant going to a major chord).'])

pat_ex(S, 'e5', 'Three up from every note',
       'Three notes up the scale from each note in turn, an eighth and two sixteenths.',
       Q('C D E, D E F, E F G, …', 76, ['C3', 'D3', 'E3', 'D3', 'E3', 'F3'], [0.5, 0.25, 0.25] * 2),
       [dict(chords=IW_17_18, shapes=[[0, 1, 2]], rhythm=[0.5, 0.25, 0.25], step=1, start='Eb3', key='Eb')],
       [f'{IW}, bars 17–18. E♭: from the root, one group a beat.', 'G7, going to C minor: C harmonic minor, from one of its own notes.'])

pat_ex(S, 'e6', 'Three down from every note',
       'Three notes down from each note in turn.',
       Q('C B A, B A G, …', 76, ['C4', 'B3', 'A3', 'B3', 'A3', 'G3'], [0.5, 0.25, 0.25] * 2),
       [dict(chords=OC_9_10, shapes=[[0, -1, -2]], rhythm=[0.5, 0.25, 0.25], step=-1, start='A4', key='A', mode='minor')],
       [f'{OCI}, bars 9–10. D minor, in A harmonic minor: from A, its 5th.', 'D minor still, on down.'])

pat_ex(S, 'e7', 'The note below',
       'Each note, the scale note under it, and the note again; then the next note up.',
       Q('C B C, D C D, E D E, …', 76, ['C3', 'B2', 'C3', 'D3', 'C3', 'D3'], [0.5, 0.25, 0.25] * 2),
       [dict(chords=IW_26_27, shapes=[[0, -1, 0]], rhythm=[0.5, 0.25, 0.25], step=1, start='C4', key='Eb')],
       [f'{IW}, bars 26–27. C minor 7: from the root.', 'G minor 7, then C7 (going to F minor: F harmonic minor), each from one of its own notes.'])

pat_ex(S, 'e8', 'The note above',
       'Each note, the scale note over it, and the note again; then the next note up.',
       Q('C D C, D E D, E F E, …', 76, ['C3', 'D3', 'C3', 'D3', 'E3', 'D3'], [0.5, 0.25, 0.25] * 2),
       [dict(chords=IW_29_30, shapes=[[0, 1, 0]], rhythm=[0.5, 0.25, 0.25], step=1, start='F3', key='Eb')],
       [f'{IW}, bars 29–30. F minor 7: from the root.', 'B♭7: from one of its own notes, on up.'])

pat_ex(S, 'e9', 'Up, with the top note repeated',
       'Four notes up the scale with the top one struck three times, six eighths; each group starts a step higher. In a waltz each group is one bar.',
       Q('C D E, E struck again, then C D E F and F three times, …', 76, ['C3', 'D3', 'E3', 'E3'], [0.5] * 4),
       [dict(chords=YV_1_4, shapes=[[0, 1, 2, 3, 3, 3]], rhythm=[0.5] * 6, step=1, start='D4', key='G')],
       [f'{YVL}, bars 1–4, in three. G: from D, its 5th.', 'C: G major still (the key’s own chord), from E, its 3rd.',
        'C minor 6, not the key’s: B♭ major, a tone below its name (his rule), from G.', 'D: G major, from A.'], bar_beats=3, near=5)

pat_ex(S, 'e10', 'Down, with the bottom note repeated',
       'Four notes down with the last struck three times; each group a step lower.',
       Q('C B A, A again, then C B A G and G three times, …', 76, ['C4', 'B3', 'A3', 'A3'], [0.5] * 4),
       [dict(chords=YV_1_4, shapes=[[0, -1, -2, -3, -3, -3]], rhythm=[0.5] * 6, step=-1, start='D5', key='G')],
       [f'{YVL}, bars 1–4. G: from D.', 'C: from C.', 'C minor 6 (B♭ major): from A, its 6th.', 'D: from F♯, its 3rd.'], bar_beats=3, near=7)


# ================================================================ scale with arpeggio (p. 77)
def arp_scale(id_, title, idea, quote, bars_spec, txts, near=6):
    """bars_spec: [[(chord, notes, durs, kind, key, mode, nxt)]] where kind is 'arp' (the chord's notes in order) or 'scale'"""
    segs = []
    for b in bars_spec:
        for chord, notes, durs, kind, key, mode, nxt in b:
            root, sk, rule = scale_of(chord, key, mode, nxt)
            segs.append(dict(chord=chord, notes=notes, durs=durs, groups=None, root=root, kind=sk, rule=rule, part=kind, key=key, mode=mode, nxt=nxt))
    ex('arpegio', id_, title, idea, quote, to_bars(id_, segs, 4, txts, near))


Q4 = [1.0] * 4
arp_scale('a1', 'The triad up, the scale down',
          'The chord’s triad up in quarters to the octave, then down the scale.',
          Q('C E G C, then B A G F E D C.', 77, ['C3', 'E3'], [1.0, 1.0]),
          [[('Eb', ['Eb4', 'G4', 'Bb4', 'Eb5'], Q4, 'arp', 'Eb', 'major', None)],
           [('Bb7', ['D5', 'C5', 'Bb4', 'Ab4'], Q4, 'scale', 'Eb', 'major', 'Eb')],
           [('Eb', ['G4', 'F4', 'Eb4'], [1.0, 1.0, 2.0], 'scale', 'Eb', 'major', None)]],
          [f'{IW}, bars 1–3. E♭: up its triad.', 'B♭7: down the E♭ scale from D, its 3rd.', 'E♭: on down to the root.'])

arp_scale('a2', 'The triad down, the scale up',
          'The triad down from the octave, then up the scale.',
          Q('C G E C, then D E F G A B C.', 77, ['C4', 'G3'], [1.0, 1.0]),
          [[('Eb', ['Eb5', 'Bb4', 'G4', 'Eb4'], Q4, 'arp', 'Eb', 'major', None)],
           [('G7', ['F4', 'G4', 'Ab4', 'B4'], Q4, 'scale', 'Eb', 'major', 'Cm7')],
           [('Cm7', ['C5', 'D5', 'Eb5'], [1.0, 1.0, 2.0], 'scale', 'Eb', 'major', None)]],
          [f'{IW}, bars 17–19. E♭: down its triad.', 'G7: up C harmonic minor from F, its 7th.', 'C minor 7: on up in E♭ major to E♭.'])

arp_scale('a3', 'Triads up two octaves, the scale down',
          'The triad up through two octaves in eighths, then down the scale.',
          Q('C E G C E G C, then down.', 77, ['C3', 'E3', 'G3', 'C4'], [0.5] * 4),
          [[('Bb7', ['Bb2', 'D3', 'F3', 'Bb3', 'D4', 'F4', 'Bb4'], [0.5] * 6 + [1.0], 'arp', 'Eb', 'major', 'Eb')],
           [('Bb7', ['Ab4', 'G4', 'F4', 'Eb4', 'D4', 'C4', 'Bb3'], [0.5] * 6 + [1.0], 'scale', 'Eb', 'major', 'Eb')]],
          [f'{IW}, bars 30–31. B♭7: its triad up two octaves from the low B♭.', 'B♭7 still: down the E♭ scale from A♭, its 7th, to the root.'], near=5)

arp_scale('a4', 'Triads down two octaves, the scale up',
          'The triad down through two octaves, then up the scale.',
          Q('C G E C G E C, then up.', 77, ['C5', 'G4', 'E4', 'C4'], [0.5] * 4),
          [[('F7', ['F5', 'C5', 'A4', 'F4', 'C4', 'A3', 'F3'], [0.5] * 6 + [1.0], 'arp', 'Eb', 'major', 'Bb7')],
           [('F7', ['G3', 'A3', 'Bb3', 'C4', 'D4', 'Eb4', 'F4'], [0.5] * 6 + [1.0], 'scale', 'Eb', 'major', 'Bb7')]],
          [f'{IW}, bars 11–12. F7: its triad down two octaves.', 'F7 still (going to B♭7: B♭ major), up the scale to the root.'], near=6)


# ================================================================ intervals (pp. 77–78)
S = 'intervalos'
pat_ex(S, 'i1', 'In 3rds, up and down',
       'Pairs a 3rd apart, the lower first, climbing a step a pair; then the pairs come down, the upper first.',
       Q('C E, D F, E G, F A, …', 77, ['C3', 'E3', 'D3', 'F3'], [0.5] * 4),
       [dict(chords=IW_13_14[:1], shapes=[[0, 2]], rhythm=[0.5] * 2, step=1, start='C4', key='Eb'),
        dict(chords=IW_13_14[1:], shapes=[[0, -2]], rhythm=[0.5] * 2, step=-1, start='A4', key='Eb')],
       [f'{IW}, bars 13–14. C minor 7: up in 3rds from the root.', 'F7, going to B♭7 (B♭ major): down in 3rds from A, its 3rd.'])

pat_ex(S, 'i2', 'In 3rds, one up, one down',
       'Pairs a 3rd apart climbing a step a pair, every other pair turned over: up a 3rd, down a 3rd, up, down.',
       Q('C E, F D, E G, A F, …', 77, ['C3', 'E3', 'F3', 'D3'], [0.5] * 4),
       [dict(chords=OC_13_14[:1], shapes=[[0, 2], [2, 0]], rhythm=[0.5] * 2, step=1, start='E4', key='A', mode='minor'),
        dict(chords=OC_13_14[1:], shapes=[[0, 2], [2, 0]], rhythm=[0.5] * 2, step=-1, start='B4', key='A', mode='minor')],
       [f'{OCI}, bars 13–14. E7, in A harmonic minor: from E, climbing.', 'E7 still: the same pairs coming down, from B.'])

pat_ex(S, 'i3', 'In 4ths, up and down',
       'Pairs a 4th apart, up, then down.',
       Q('C F, D G, E A, …', 77, ['C3', 'F3', 'D3', 'G3'], [0.5] * 4),
       [dict(chords=IW_24_25[:1], shapes=[[0, 3]], rhythm=[0.5] * 2, step=1, start='F3', key='Eb'),
        dict(chords=IW_24_25[1:], shapes=[[0, -3]], rhythm=[0.5] * 2, step=-1, start='Eb4', key='Eb')],
       [f'{IW}, bars 24–25. F minor 7: up in 4ths from the root.', 'F minor 7, then D♭9 (A♭ melodic minor, his rule for a dominant outside the key): down in 4ths.'])

pat_ex(S, 'i4', 'In 4ths, one up, one down',
       'Pairs a 4th apart climbing a step a pair, every other pair turned over.',
       Q('C F, G D, E A, B F, …', 78, ['C3', 'F3', 'G3', 'D3'], [0.5] * 4),
       [dict(chords=OC_9_10[:1], shapes=[[0, 3], [3, 0]], rhythm=[0.5] * 2, step=1, start='D4', key='A', mode='minor'),
        dict(chords=OC_9_10[1:], shapes=[[0, 3], [3, 0]], rhythm=[0.5] * 2, step=-1, start='A4', key='A', mode='minor')],
       [f'{OCI}, bars 9–10. D minor, in A harmonic minor: from the root, climbing.', 'D minor: coming down, from A.'])

pat_ex(S, 'i5', 'In 6ths, up and down',
       'Pairs a 6th apart, up, then down.',
       Q('C A, D B, E C, …', 78, ['C3', 'A3', 'D3', 'B3'], [0.5] * 4),
       [dict(chords=IW_26_27[:1], shapes=[[0, 5]], rhythm=[0.5] * 2, step=1, start='C4', key='Eb'),
        dict(chords=IW_26_27[1:], shapes=[[0, -5]], rhythm=[0.5] * 2, step=-1, start='G4', key='Eb')],
       [f'{IW}, bars 26–27. C minor 7: up in 6ths from the root.', 'G minor 7, then C7 (F harmonic minor): down in 6ths.'])

pat_ex(S, 'i6', 'In 6ths, one up, one down',
       'Pairs a 6th apart climbing a step a pair, every other pair turned over.',
       Q('C A, B D, E C, …', 78, ['C3', 'A3', 'B3', 'D3'], [0.5] * 4),
       [dict(chords=OC_1_2[:1], shapes=[[0, 5], [5, 0]], rhythm=[0.5] * 2, step=1, start='E3', key='A', mode='minor'),
        dict(chords=OC_1_2[1:], shapes=[[0, 5], [5, 0]], rhythm=[0.5] * 2, step=-1, start='B3', key='A', mode='minor')],
       [f'{OCI}, bars 1–2. E7, in A harmonic minor: from E, climbing.', 'E7: coming down, from B.'], near=5)


# ================================================================ chord notes with a chromatic approach (pp. 78–79)
def below(n): return M.tr(n, -1, -1) if not (M.tr(n, -1, -1)[0] in 'EB' and M.tr(n, -1, -1)[1:2] == '#') else M.mk(M.parse(n)[0], M.parse(n)[1] - 1, M.parse(n)[2])


CELLS = {   # what each chord note gets, in order: T the note, C the semitone below it, D the next scale note above it
    'c1': (['C', 'T'], [0.5, 0.5]), 'c2': (['T', 'C', 'T'], [0.5, 0.25, 0.25]), 'c3': (['D', 'C', 'T'], [0.5, 0.25, 0.25]),
    'c4': (['T', 'D', 'C', 'T'], [0.5] * 4), 'c5': (['T', 'C', 'D', 'T'], [0.5] * 4), 'c6': (['D', 'T', 'C', 'T'], [0.5] * 4)}


def chord_cells(cell, chords, starts, key='Eb', mode='major'):
    """each chord's notes upward from `start` (or the nearest above it), each dressed in the cell; every chord starts again from there"""
    names, durs = CELLS[cell]
    segs = []
    for (chord, beats, nxt), start in zip(chords, starts if isinstance(starts, list) else [starts] * len(chords)):
        t = M.midi(start)
        root, kind, rule = scale_of(chord, key, mode, nxt)
        sc = sc_list(root, kind)
        n_cells = round(beats / sum(durs))
        tones = [n for n in sc if M.is_tone(n, chord) and M.midi(n) >= t]
        notes, ds, targets = [], [], []
        for T in tones[:n_cells]:
            above = sc[sc.index(T) + 1]
            for x in names: notes.append({'T': T, 'C': below(T), 'D': above}[x])
            ds += list(durs); targets.append(T)
        segs.append(dict(chord=chord, notes=notes, durs=ds, groups=None, root=root, kind=kind, rule=rule, cell=cell, targets=targets, key=key, mode=mode, nxt=nxt))
    return segs


def cell_ex(id_, title, idea, quote, chords, start, txts, near=6):
    segs = chord_cells(id_, chords, start)
    ex('cromatica', id_, title, idea, quote, to_bars(id_, segs, 4, txts, near))


cell_ex('c1', 'A semitone into each chord note',
        'Each note of the chord, from the root up, reached from the semitone below it: an appoggiatura.',
        Q('Over C: B C, D♯ E, F♯ G, B C.', 78, ['B2', 'C3', 'D#3', 'E3'], [0.5] * 4),
        IW_5_6, 'C4', [f'{IW}, bars 5–6. C minor 7: C, E♭, G, B♭, each from a semitone below.', 'G7: D, F, G, B the same way.'])
cell_ex('c2', 'The semitone below and back',
        'Each chord note, the semitone below it, and the note again: an eighth and two sixteenths.',
        Q('Over C: C B C, E D♯ E, G F♯ G, C B C.', 78, ['C3', 'B2', 'C3', 'E3', 'D#3', 'E3'], [0.5, 0.25, 0.25] * 2),
        IW_9_10, 'F4', [f'{IW}, bars 9–10. F minor 7, from the root.', 'C7, from G, its 5th.'])
cell_ex('c3', 'Closed in from above and below',
        'Each chord note approached from the scale note above it and then the semitone below it.',
        Q('Over C: D B C, F D♯ E, A F♯ G, D B C.', 78, ['D3', 'B2', 'C3', 'F3', 'D#3', 'E3'], [0.5, 0.25, 0.25] * 2),
        IW_13_14, 'C4', [f'{IW}, bars 13–14. C minor 7, in E♭ major.', 'F7, in B♭ major (his rule for F7 going to B♭7).'])
cell_ex('c4', 'The note, the scale note above, the semitone below, the note',
        'Four eighths to each chord note: the note, the scale note above, the semitone below, the note.',
        Q('Over C: C D B C, E F D♯ E, …', 78, ['C3', 'D3', 'B2', 'C3'], [0.5] * 4),
        IW_17_18, 'Eb4', [f'{IW}, bars 17–18. E♭: the root, then G.', 'G7 (C harmonic minor): two of its notes.'])
cell_ex('c5', 'The note, the semitone below, the scale note above, the note',
        'The same four with the middle two turned round.',
        Q('Over C: C B D C, E D♯ F E, …', 78, ['C3', 'B2', 'D3', 'C3'], [0.5] * 4),
        IW_29_30, ['F4', 'Bb4'], [f'{IW}, bars 29–30. F minor 7, from the root.', 'B♭7, from its root.'])
cell_ex('c6', 'The scale note above, the note, the semitone below, the note',
        'The scale note above first, then the note, the semitone below, the note.',
        Q('Over C: D C B C, F E D♯ E, …', 79, ['D3', 'C3', 'B2', 'C3'], [0.5] * 4),
        IW_1_2, 'Eb4', [f'{IW}, bars 1–2. E♭, from the root.', 'B♭7.'])


# ================================================================ diatonic triads and 7th chords (p. 79)
S = 'triadas'
T3 = [[0, 2, 4]]; T3D = [[4, 2, 0]]
pat_ex(S, 't1', 'Triads up',
       'The triad on each note of the scale in turn, each played upward; three eighths each, so two to a waltz bar.',
       Q('C E G, D F A, E G B, F A C.', 79, ['C3', 'E3', 'G3', 'D3'], [0.5] * 4),
       [dict(chords=YV_1_4, shapes=T3, rhythm=[0.5] * 3, step=1, start='G3', key='G')],
       [f'{YVL}, bars 1–4. G: the triads of G major from G.', 'C: from C.', 'C minor 6: the triads of B♭ major, from G.', 'D: back in G major.'], bar_beats=3, near=5)
pat_ex(S, 't2', 'Triads down',
       'Each triad played downward from its top.',
       Q('G E C, A F D, B G E, C A F.', 79, ['G3', 'E3', 'C3', 'A3'], [0.5] * 4),
       [dict(chords=YV_1_4, shapes=T3D, rhythm=[0.5] * 3, step=1, start='G3', key='G')],
       [f'{YVL}, bars 1–4. G.', 'C.', 'C minor 6 (B♭ major).', 'D.'], bar_beats=3, near=5)
pat_ex(S, 't3', 'Triads up, then down',
       'One triad up, the next down, and so on.',
       Q('C E G, A F D, E G B, C A F.', 79, ['C3', 'E3', 'G3', 'A3'], [0.5] * 4),
       [dict(chords=YV_1_4, shapes=[[0, 2, 4], [4, 2, 0]], rhythm=[0.5] * 3, step=1, start='G3', key='G')],
       [f'{YVL}, bars 1–4. G.', 'C.', 'C minor 6 (B♭ major).', 'D.'], bar_beats=3, near=5)
pat_ex(S, 't4', 'Triads down, then up',
       'One triad down, the next up.',
       Q('G E C, D F A, B G E, F A C.', 79, ['G3', 'E3', 'C3', 'D3'], [0.5] * 4),
       [dict(chords=YV_1_4, shapes=[[4, 2, 0], [0, 2, 4]], rhythm=[0.5] * 3, step=1, start='G3', key='G')],
       [f'{YVL}, bars 1–4. G.', 'C.', 'C minor 6 (B♭ major).', 'D.'], bar_beats=3, near=5)

S = 'septimas'
pat_ex(S, 's1', '7th chords up',
       'The 7th chord on each note of the scale in turn, played upward in eighths.',
       Q('C E G B, D F A C, …', 79, ['C3', 'E3', 'G3', 'B3'], [0.5] * 4),
       [dict(chords=IW_29_30, shapes=[[0, 2, 4, 6]], rhythm=[0.5] * 4, step=1, start='F3', key='Eb')],
       [f'{IW}, bars 29–30. F minor 7: the 7th chords of E♭ major from F.', 'B♭7: from one of its own notes.'], near=5)
pat_ex(S, 's2', '7th chords down',
       'Each 7th chord played downward from its 7th.',
       Q('B G E C, C A F D, …', 79, ['B3', 'G3', 'E3', 'C3'], [0.5] * 4),
       [dict(chords=IW_1_2, shapes=[[6, 4, 2, 0]], rhythm=[0.5] * 4, step=1, start='C4', key='Eb')],
       [f'{IW}, bars 1–2. E♭: from B♭, each chord down from its 7th.', 'B♭7.'], near=6)
pat_ex(S, 's3', '7th chords up, then down',
       'One 7th chord up, the next down from its 7th.',
       Q('C E G B, C A F D, …', 79, ['C3', 'E3', 'G3', 'B3'], [0.5] * 4),
       [dict(chords=IW_13_14, shapes=[[0, 2, 4, 6], [6, 4, 2, 0]], rhythm=[0.5] * 4, step=1, start='C4', key='Eb')],
       [f'{IW}, bars 13–14. C minor 7, in E♭ major.', 'F7, in B♭ major.'], near=6)
pat_ex(S, 's4', '7th chords down, then up',
       'One down from its 7th, the next up.',
       Q('B G E C, D F A C, …', 80, ['B3', 'G3', 'E3', 'C3'], [0.5] * 4),
       [dict(chords=IW_17_18, shapes=[[6, 4, 2, 0], [0, 2, 4, 6]], rhythm=[0.5] * 4, step=1, start='C4', key='Eb')],
       [f'{IW}, bars 17–18. E♭.', 'G7, in C harmonic minor.'], near=6)

for sec in EXS.values():
    for e in sec:
        e['idea'] += ''

SECTIONS = [dict(id='escalares', title='Scale patterns', part='Exercises', ex=EXS['escalares']),
            dict(id='arpegio', title='Scale with arpeggio', part='Exercises', ex=EXS['arpegio']),
            dict(id='intervalos', title='Intervals', part='Exercises', ex=EXS['intervalos']),
            dict(id='cromatica', title='Chord notes with a chromatic approach', part='Exercises', ex=EXS['cromatica']),
            dict(id='triadas', title='Diatonic triads', part='Exercises', ex=EXS['triadas']),
            dict(id='septimas', title='Diatonic 7th chords', part='Exercises', ex=EXS['septimas'])]

sys.path.insert(0, '/home/claude/studies/tango')
from quotes import trim as _trim_quotes   # quotes stay a beat or two
_trim_quotes(SECTIONS)
