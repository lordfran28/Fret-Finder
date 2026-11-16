"""Tango melody: Graciano, Método de guitarra tango, ch. 7 ("Melodía: improvisación tanguística"), pp. 57–79 of the
owner's copy: his scale for every kind of chord, his tango minor scale, chromatic notes (fingerings, arpeggios,
neighbours, passing notes, links between chords, chromatic patterns), blue notes, and guide-tone lines.

Every line of ours applies one of his rules to the chords of the owner's songs (I Wonder Who's Kissing Her Now in
E♭, Очи чёрные in A minor, Я вас любил in G, Glinka's Я помню чудное мгновенье in E♭). Nothing of his is moved
note for note: his examples are quoted by their first beat or two, his examples from tangos still under copyright
(Troilo, Piazzolla, Rovira, Salgán, Laurenz, Expósito) are described in words only. check9.py checks every note of
ours against the rule it stands for.

His melodic paraphrase and expression (pp. 57–61) work on a plain written melody; they wait for a reliable score of
one of the owner's public-domain songs. His melodic patterns (pp. 75–79) are a separate entry (entry10).
"""
import sys
sys.path.insert(0, '/home/claude/studies'); sys.path.insert(0, '/home/claude/studies/tango')
import mel as M
from entry import K
from kit_study import place_lines, two_lines, shape

OWN = 'Graciano’s own'
EXS = {}
LINES = []          # (exercise id, bar index, segment) for check9
IW = 'I Wonder Who’s Kissing Her Now'
OCI = 'Очи чёрные'
YVL = 'Я вас любил'
GLI = 'Я помню чудное мгновенье'
E8 = [0.5] * 8


def where(p): return f'Método de guitarra tango, p. {p}'


def ex(sec, id, title, idea, quote, bars):
    EXS.setdefault(sec, []).append(dict(id=id, title=title, idea=idea, quote=quote, bars=bars))


def his(notes, durs, near=3):
    """his first notes, at sounding pitch (an octave under his treble clef)"""
    return M.run(notes, durs, 'his notes', near=near)


def T(text, p, notes=None, durs=None, near=3, played=''):
    d = dict(where=where(p), text=text, whose=OWN, played=played, by='Graciano')
    if notes: d['items'] = [his(notes, durs, near)]
    else: d['item'] = None
    return d


def seg(chord, notes, durs, **chk):
    """one chord's stretch of a line; chk says which rule it shows (for check9)"""
    return dict(chord=chord, notes=list(notes), durs=list(durs), chk=chk)


def rest(d): return dict(rest=d)


def line_bars(id_, bars, notes_txt, near=6, fix=None, label=None):
    """bars: [[seg or rest, ...], ...]; one fingering for the whole exercise, one numbered run per chord stretch"""
    allnotes = [n for b in bars for s in b if 'rest' not in s for n in s['notes']]
    pos, _ = M.fingering(allnotes, near=near, fix=fix)
    k = 0; out = []
    for bi, (b, txt) in enumerate(zip(bars, notes_txt)):
        items, chords = [], []
        for s in b:
            if 'rest' in s:
                items.append(['W', s['rest']]); continue
            p = pos[k:k + len(s['notes'])]; k += len(s['notes'])
            lab = label or ('over ' + M.dname(s['chord']))
            items.append(['R', [list(x) for x in p], s['durs'], '=' + ','.join(M.disp(n) for n in s['notes']) + '|' + lab])
            if s['chord'] and s['chord'] not in chords: chords.append(s['chord'])
            LINES.append((id_, bi, s))
        out.append(dict(chords=chords, items=items, note=txt))
    return out


def scale_seg(chord, notes, durs, key, mode='major', nxt=None, rule=None):
    r = M.rule_for(chord, key, mode, nxt)
    if rule: assert r[0] == rule, (chord, r, rule)
    return seg(chord, notes, durs, type='scale', root=r[1], kind=r[2], start_tone=True)


def tango_seg(chord, notes, durs, key):
    return seg(chord, notes, durs, type='scale', root=key, kind='tango minor', start_tone=True)


def sname(root, kind): return f'{M.disp(root + "4")} {M.SCALE_WORDS[kind]}'


# ================================================================ the scale for each chord (pp. 62–65)
ex('escala', 'mayor', 'A major-key progression: the key’s own scale',
   ('Where every chord belongs to one major key, every chord takes that key’s scale: theory calls it Ionian, Dorian, Mixolydian and the rest, '
    'Graciano says that in practice it is all one major scale. What matters is to rest on the chord’s own notes and its guide tones. '
    'Here each chord’s stretch of the line begins on one of its own notes.'),
   T('Over C, Dm, G7 and C, each bar runs the C major scale up from the chord’s root in eighths.', 62, ['C3', 'D3', 'E3', 'F3'], [0.5] * 4),
   line_bars('mayor', [
       [scale_seg('Eb', ['Eb4', 'F4', 'G4', 'Ab4', 'Bb4', 'C5', 'D5', 'Eb5'], E8, 'Eb', rule='1')],
       [scale_seg('Bb7', ['D5', 'C5', 'Bb4', 'Ab4', 'G4', 'F4', 'Eb4', 'D4'], E8, 'Eb', rule='1')],
       [scale_seg('Eb', ['Eb4', 'F4', 'G4', 'Ab4', 'Bb4'], [0.5] * 4 + [2.0], 'Eb', rule='1')]],
       [f'{IW}, bars 1–3. E♭: the E♭ major scale up from the root.',
        'B♭7 is the key’s own dominant: the same E♭ scale, down from D, the chord’s 3rd.',
        'E♭ again, up to B♭, its 5th.']))

ex('escala', 'menor', 'A minor-key progression: the harmonic minor',
   ('Tango’s minor progressions come from the harmonic minor, and over each chord you can run that scale. Graciano adds that its sound is not quite the tango’s '
    '(the next exercise has his own scale).'),
   T('Over Cm, Dm7♭5, G7 and Cm, each bar runs C harmonic minor up from the chord’s root.', 63, ['C3', 'D3', 'Eb3', 'F3'], [0.5] * 4),
   line_bars('menor', [
       [scale_seg('E7', ['E4', 'F4', 'G#4', 'A4', 'B4', 'C5', 'D5', 'E5'], E8, 'A', 'minor', rule='2')],
       [scale_seg('E7', ['D5', 'C5', 'B4', 'A4', 'G#4', 'F4', 'E4', 'D4'], E8, 'A', 'minor', rule='2')],
       [scale_seg('Am', ['C4', 'D4', 'E4', 'F4', 'G#4', 'A4', 'B4', 'C5'], E8, 'A', 'minor', rule='2')],
       [scale_seg('Am', ['A4', 'B4', 'C5', 'B4', 'A4'], [0.5] * 4 + [2.0], 'A', 'minor', rule='2')]],
       [f'{OCI}, the last four bars. E7: A harmonic minor up from E (F and G♯ against the chord).',
        'E7 again, down from D, its 7th.', 'A minor, from C, its 3rd.', 'Home on A.']))

ex('escala', 'tango', 'His tango minor scale',
   ('Graciano’s own scale, drawn from the playing of tango’s great players: the natural, harmonic and melodic minors at once, 1 2 ♭3 4 5 ♭6 6 ♭7 7. '
    'Both 6ths and both 7ths, played the same way up and down; he calls it the sound of the bandoneons. Rest on the chord’s own notes as it runs. In A: '
    'A B C D E F F♯ G G♯.'),
   T('The scale written out on C in quarters, its degrees numbered under it.', 63, ['C3', 'D3'], [1.0, 1.0]),
   line_bars('tango', [
       [tango_seg('E7', ['E4', 'F4', 'F#4', 'G4', 'G#4', 'A4', 'B4', 'C5'], E8, 'A')],
       [tango_seg('E7', ['D5', 'C5', 'B4', 'A4', 'G#4', 'G4', 'F#4', 'F4'], E8, 'A')],
       [tango_seg('Am', ['E4', 'F4', 'F#4', 'G4', 'G#4', 'A4', 'B4'], [1.0] + [0.5] * 6, 'A')],
       [tango_seg('Am', ['C5', 'B4', 'A4', 'G#4', 'A4'], [0.5] * 4 + [2.0], 'A')]],
       [f'{OCI}, bars 1–4 (in four). E7: up from E through both 6ths (F, F♯) and both 7ths (G, G♯).',
        'E7, down from D, its 7th: the same notes the same way down.', 'A minor, from E, its 5th.', 'From C, its 3rd, home to A.']))

ex('escala', 'mayor-fuera', 'A major chord on a note outside the key',
   ('A maj7 chord whose root is not in the key (in C, A♭maj7 or E♭maj7) is borrowed from another mode: play the major scale a 4th below its name. '
    'Over B major 7 in E♭, that is F♯ major, with its E♯.'),
   T('Over C, E♭maj7, A♭maj7 and D♭maj7, each borrowed chord gets the major scale a 4th below its name (B♭, E♭, A♭ major); here the start of the B♭ scale over E♭maj7.', 63,
     ['Bb2', 'C3', 'D3', 'Eb3'], [0.5] * 4),
   line_bars('mayor-fuera', [
       [scale_seg('Bb7', ['Bb4', 'Ab4', 'G4', 'F4', 'Eb4', 'D4', 'C4', 'Bb3'], E8, 'Eb', rule='1')],
       [scale_seg('Bb7', ['D4', 'Eb4', 'F4', 'G4'], [0.5] * 4, 'Eb', rule='1'),
        scale_seg('Bmaj7', ['D#4', 'E#4', 'F#4', 'G#4'], [0.5] * 4, 'Eb', rule='3')],
       [scale_seg('Eb', ['G4'], [4.0], 'Eb', rule='1')]],
       [f'{IW}, bars 31–32 and the next bar 1. B♭7: E♭ major, down from the root.',
        'B♭7, then B major 7 (the borrowed ♭VI): F♯ major from D♯, its 3rd; E♯ is its own note.',
        'Back to E♭: the G♯ falls a semitone to G.']))

ex('escala', 'mayor-dentro', 'A major chord on a note of the key',
   ('A maj7 chord on a note of the key that is not one of the key’s own chords (D major 7 in G, where the key has D7): play the major scale from its name, as '
    'if the music had changed key for a moment. Not on the IV, which is the key’s own.'),
   T('Over C, G7, D and A7, the D bar runs the D major scale.', 63, ['D3', 'E3', 'F#3', 'G3'], [0.5] * 4),
   line_bars('mayor-dentro', [
       [scale_seg('D', ['D4', 'E4', 'F#4', 'G4', 'A4', 'B4'], [0.5] * 6, 'G', rule='1')],
       [scale_seg('Dmaj7', ['C#5', 'D5'], [0.5, 0.5], 'G', rule='4'),
        scale_seg('D7', ['C5', 'B4'], [0.5, 0.5], 'G', rule='1'),
        scale_seg('G', ['G4'], [1.0], 'G', rule='1')],
       [scale_seg('G', ['B4', 'A4', 'G4'], [0.5, 0.5, 2.0], 'G', rule='1')]],
       [f'{YVL}, bars 4–6, in three. D: the key’s own G major scale.',
        'D major 7 for a beat: its own D major scale, so C♯; then D7 for a beat, back in G, so C♮.',
        'G.']))

ex('escala', 'menor-dentro', 'A minor chord that is not the key’s',
   ('A minor chord that does not belong to the key (in C, Fm7 or Gm7): play the major scale a whole tone below its name. The same rule holds when its root is outside '
    'the key altogether (B♭m7 in C: A♭ major), where Graciano hears it as the II of a passing key, with or without its V7. Not on II and III, which are the key’s own.'),
   T('Over C, Fm7, C and Gm7, Fm7 gets E♭ major and Gm7 F major.', 64, ['Eb3', 'F3', 'G3', 'Ab3'], [0.5] * 4),
   line_bars('menor-dentro', [
       [scale_seg('Cm7', ['C4', 'D4', 'Eb4', 'F4'], [0.5] * 4, 'Eb', rule='1'),
        scale_seg('Abm6', ['Ab4', 'Bb4', 'Cb5', 'Db5'], [0.5] * 4, 'Eb', rule='5')],
       [scale_seg('Eb', ['Eb5', 'D5', 'C5', 'Bb4', 'Ab4', 'G4', 'F4', 'Eb4'], E8, 'Eb', rule='1')]],
       [f'{IW}, bars 19–20. C minor 7, the key’s own; then A♭ minor 6, the borrowed minor IV: G♭ major from its root, with C♭ and D♭.',
        'E♭: the D♭ steps up to E♭ and the line comes down the E♭ scale.']))

ex('escala', 'dom-mayor', 'A dominant going to a major chord',
   ('A dominant 7th on a note of the key, going to a major chord of the key (a secondary dominant): play the major scale a 5th below its name. '
    'F7 going to B♭7 takes B♭ major, with its A♮.'),
   T('Over C, D7, G7 and C7, D7 gets G major and C7 F major.', 64, ['G3', 'A3', 'B3', 'C4'], [0.5] * 4),
   line_bars('dom-mayor', [
       [scale_seg('Cm7', ['C5', 'Bb4', 'Ab4', 'G4', 'F4', 'Eb4', 'D4', 'C4'], E8, 'Eb', rule='1')],
       [scale_seg('F7', ['Eb4', 'F4', 'G4', 'A4', 'Bb4', 'C5', 'D5', 'Eb5'], E8, 'Eb', nxt='Bb7', rule='7a')],
       [scale_seg('F7', ['C5', 'Bb4', 'A4', 'G4'], [0.5] * 4, 'Eb', nxt='Bb7', rule='7a'),
        scale_seg('Bb7', ['Ab4', 'Bb4', 'C5', 'D5'], [0.5] * 4, 'Eb', rule='1')],
       [scale_seg('Bb7', ['Bb4', 'Ab4', 'G4', 'F4', 'Eb4', 'D4', 'C4', 'Bb3'], E8, 'Eb', rule='1')],
       [scale_seg('Eb', ['Eb4'], [4.0], 'Eb', rule='1')]],
       [f'{IW}, bars 13–17. C minor 7: E♭ major, down from the root.',
        'F7, on its way to B♭7: B♭ major, up from E♭, its 7th.', 'F7 from C, its 5th; then B♭7, back in E♭ major, from A♭, its 7th: A to G to A♭.',
        'B♭7, down from the root.', 'E♭.']))

ex('escala', 'dom-menor', 'A dominant going to a minor chord',
   ('A dominant 7th on a note of the key, going to a minor chord of the key: play the harmonic minor a 5th below its name. C7 going to Fm7 takes F harmonic minor, '
    'with D♭ and E. Graciano adds that he uses his tango minor in every such case; the second time here it is the tango minor.'),
   T('Over C, E7, Am and A7, E7 gets A harmonic minor (and A7, going to D minor, D melodic minor in theory, harmonic minor in practice).', 64,
     ['A3', 'B3', 'C4', 'D4'], [0.5] * 4),
   line_bars('dom-menor', [
       [scale_seg('Abmaj7', ['C5', 'Bb4', 'Ab4', 'G4'], [0.5] * 4, 'Eb', rule='1'),
        scale_seg('C7', ['E4', 'F4', 'G4', 'Ab4'], [0.5] * 4, 'Eb', nxt='Fm7', rule='7b')],
       [scale_seg('C7', ['Bb4', 'C5', 'Db5', 'E5', 'Db5', 'C5', 'Bb4', 'Ab4'], E8, 'Eb', nxt='Fm7', rule='7b')],
       [scale_seg('Fm7', ['F4', 'G4', 'Ab4', 'Bb4', 'C5'], [0.5] * 4 + [2.0], 'Eb', rule='1')],
       [seg('C7', ['C5', 'Db5', 'D5', 'Eb5', 'E5', 'Eb5', 'D5', 'Db5'], E8, type='scale', root='F', kind='tango minor', start_tone=True)],
       [scale_seg('Fm7', ['C5', 'Bb4', 'Ab4', 'G4', 'F4'], [0.5] * 4 + [2.0], 'Eb', rule='1')]],
       [f'{IW}, bars 7–9. A♭ major 7, the key’s own, from C, its 3rd; then C7, going to F minor: F harmonic minor from E, its 3rd.',
        'C7 from B♭, its 7th, through D♭ and E.', 'F minor 7, back in E♭ major.',
        'Bar 8 again with his tango minor of F: C, D♭, D, E♭, E, both ways.', 'F minor 7, from C, its 5th.']))

ex('escala', 'dom-fuera', 'A dominant on a note outside the key',
   ('A dominant 7th whose root is not in the key works as a tritone substitute: play the melodic minor a 4th below its name, the same way up and down. '
    'D♭9 in E♭ takes A♭ melodic minor: C♭ and G♮ over D♭.'),
   T('Over C, A♭7, G7 and D♭7, A♭7 gets E♭ melodic minor and D♭7 A♭ melodic minor.', 65, ['Eb3', 'F3', 'Gb3', 'Ab3'], [0.5] * 4),
   line_bars('dom-fuera', [
       [scale_seg('Fm7', ['F4', 'G4', 'Ab4', 'Bb4', 'C5', 'D5', 'Eb5', 'D5'], E8, 'Eb', rule='1')],
       [scale_seg('Fm7', ['Eb5', 'D5', 'C5', 'Bb4'], [0.5] * 4, 'Eb', rule='1'),
        scale_seg('Db9', ['Cb5', 'Bb4', 'Ab4', 'G4'], [0.5] * 4, 'Eb', rule='8')],
       [scale_seg('Cm7', ['Eb4', 'F4', 'G4', 'Ab4', 'Bb4', 'C5', 'Bb4'], [0.5] * 6 + [1.0], 'Eb', rule='1')]],
       [f'{IW}, bars 24–26. F minor 7, the key’s own scale.', 'F minor 7, then D♭9 (a tritone away from G7, on its way to C minor): A♭ melodic minor from C♭, its 7th, down to G.',
        'C minor 7, from E♭, its 3rd.']))


# ================================================================ chromatic notes (pp. 65–70)
# E♭ major in the 5th position, where I Wonder's grips sit: (note, string, fret, finger)
POS5 = {6: [('Ab2', 4, '1, stretched'), ('Bb2', 6, '2'), ('C3', 8, '4')], 5: [('D3', 5, '1'), ('Eb3', 6, '2'), ('F3', 8, '4')],
        4: [('G3', 5, '1'), ('Ab3', 6, '2'), ('Bb3', 8, '4')], 3: [('C4', 5, '1'), ('D4', 7, '3'), ('Eb4', 8, '4')],
        2: [('F4', 6, '2'), ('G4', 8, '4')], 1: [('Ab4', 4, '1, stretched'), ('Bb4', 6, '2'), ('C5', 8, '4')]}
SF = {n: (s, f) for s, L in POS5.items() for n, f, _ in L}


def fixed(id_, notes, label, txt_bars, extra_pos=None, beats=8):
    """a run on the position's own strings (chromatic notes on the string they fill), split into bars of 4"""
    where_ = dict(SF); where_.update(extra_pos or {})
    durs = [0.5] * (len(notes) - 1)
    durs.append(beats - sum(durs))
    pos = [where_[n] for n in notes]
    bars, i, t = [], 0, 0.0
    while i < len(notes):
        ns, ps, ds = [], [], []
        while i < len(notes) and t < 4 - 1e-9:
            d = min(durs[i], 4 - t)
            ns.append(notes[i]); ps.append(pos[i]); ds.append(d); t += d
            if d < durs[i] - 1e-9: durs[i] -= d; break
            i += 1
        bars.append((ns, ps, ds)); t = 0.0
    out = []
    for (ns, ps, ds), txt in zip(bars, txt_bars):
        out.append(dict(chords=['Eb'], items=[M.placed(ns, ps, ds, label)], note=txt))
        LINES.append((id_, len(out) - 1, seg('Eb', ns, ds, type='chromatic-scale', root='Eb', pos=ps)))
    return out


ex('cromatismo', 'digitaciones', 'A chromatic note inside the scale’s fingering',
   ('Take the major scale in one position with its proper fingering. On a string where the fingers leave a gap, add the missing finger: that is the chromatic note. '
    'His cases: fingers 1-2-4 (add the 3rd), 1-3-4 (add the 2nd), 2-4 (add the 3rd), and the 1st finger stretched back a fret with 2 and 4 (slide the 1st up to its own fret, '
    'or add the 3rd, or both: five notes). The practice: play the scale from the bottom, use the chromatic fingering on one string, go on three notes into the next string, '
    'and come back down through it. One string at a time; two at once loses the music. '
    'Here E♭ major in the 5th position, where I Wonder’s grips sit. His last case (fingers 2-3, add the 1st) does not come up in this position.'),
   T('His seven major-scale fingerings in position, then the seven ways a string’s fingering takes a chromatic note (no sound: diagrams).', 66),
   fixed('digitaciones', ['Ab2', 'A2', 'Bb2', 'C3', 'D3', 'Eb3', 'F3', 'Eb3', 'D3', 'C3', 'Bb2', 'A2', 'Ab2'], 'E♭ major, 5th position',
         ['Low E string, fingers 1 (stretched) 2 4: slide the 1st up to its fret for A♮. Then three notes on the A string, and back.', '…down through the A♮.'],
         {'A2': (6, 5)})
   + fixed('digitaciones', ['Ab2', 'Bb2', 'B2', 'C3', 'D3', 'Eb3', 'F3', 'Eb3', 'D3', 'C3', 'B2', 'Bb2', 'Ab2'], 'E♭ major, 5th position',
           ['The same string, adding the 3rd finger instead: B♮.', '…and back through it.'], {'B2': (6, 7)})
   + fixed('digitaciones', ['Ab2', 'A2', 'Bb2', 'B2', 'C3', 'D3', 'Eb3', 'F3', 'Eb3', 'D3', 'C3', 'B2', 'Bb2', 'A2', 'Ab2'], 'E♭ major, 5th position',
           ['Both: slide the 1st and add the 3rd, five notes on one string.', '…and back.'], {'A2': (6, 5), 'B2': (6, 7)})
   + fixed('digitaciones', ['Ab2', 'Bb2', 'C3', 'D3', 'Eb3', 'E3', 'F3', 'G3', 'Ab3', 'Bb3', 'Ab3', 'G3', 'F3', 'E3', 'Eb3', 'D3'], 'E♭ major, 5th position',
           ['A string, fingers 1 2 4: add the 3rd, E♮. Up from the low E string, three notes on the D string…', '…and back down through the E♮.'], {'E3': (5, 7)})
   + fixed('digitaciones', ['D3', 'Eb3', 'F3', 'G3', 'Ab3', 'A3', 'Bb3', 'C4', 'D4', 'Eb4', 'D4', 'C4', 'Bb3', 'A3', 'Ab3', 'G3'], 'E♭ major, 5th position',
           ['D string, fingers 1 2 4 again: A♮ under the 3rd finger.', '…back through it.'], {'A3': (4, 7)})
   + fixed('digitaciones', ['G3', 'Ab3', 'Bb3', 'C4', 'C#4', 'D4', 'Eb4', 'F4', 'G4', 'Ab4', 'G4', 'F4', 'Eb4', 'D4', 'Db4', 'C4'], 'E♭ major, 5th position',
           ['G string, fingers 1 3 4: add the 2nd, C♯ going up…', '…D♭ coming down.'], {'C#4': (3, 6), 'Db4': (3, 6)})
   + fixed('digitaciones', ['C4', 'D4', 'Eb4', 'F4', 'F#4', 'G4', 'Ab4', 'Bb4', 'C5', 'Bb4', 'Ab4', 'G4', 'Gb4', 'F4', 'Eb4', 'D4'], 'E♭ major, 5th position',
           ['B string, fingers 2 4: add the 3rd, F♯ going up…', '…G♭ coming down. (The high E string has the low E string’s fingering: practise it the same way.)'],
           {'F#4': (2, 7), 'Gb4': (2, 7)}))

ex('cromatismo', 'apoyatura', 'Five chromatic notes on one string',
   ('The same practice with one note more: lead into the string’s first fretted note from a fret below, with the 1st finger, and add the missing finger, so the string '
    'carries a run of semitones. For fingers 1-2-4 and 1-3-4 the 1st finger plays the extra note and slides up; for 2-4 the 1st finger plays the note under the 2nd. '
    'Not for the stretched fingerings.'),
   T('The three fingerings with the chromatic lead-in marked in brackets (no sound: diagrams).', 66),
   fixed('apoyatura', ['Bb2', 'C3', 'Db3', 'D3', 'Eb3', 'E3', 'F3', 'G3', 'Ab3', 'Bb3', 'Ab3', 'G3', 'F3', 'E3', 'Eb3', 'D3'], 'E♭ major, 5th position',
         ['A string: D♭ under the 1st finger at the 4th fret, slide it to D, then E♭, E♮, F…', '…three on the D string, and back.'], {'Db3': (5, 4), 'E3': (5, 7)})
   + fixed('apoyatura', ['Ab3', 'Bb3', 'B3', 'C4', 'C#4', 'D4', 'Eb4', 'F4', 'G4', 'Ab4', 'G4', 'F4', 'Eb4', 'D4', 'Db4', 'C4'], 'E♭ major, 5th position',
           ['G string: B♮ under the 1st finger, slide to C, then C♯, D, E♭…', '…and back.'], {'B3': (3, 4), 'C#4': (3, 6), 'Db4': (3, 6)})
   + fixed('apoyatura', ['C4', 'D4', 'Eb4', 'E4', 'F4', 'F#4', 'G4', 'Ab4', 'Bb4', 'C5', 'Bb4', 'Ab4', 'G4', 'Gb4', 'F4', 'E4'], 'E♭ major, 5th position',
           ['B string: E♮ under the 1st finger, then F (2nd), F♯ (3rd), G (4th)…', '…and back down to the E♮.'], {'E4': (2, 5), 'F#4': (2, 7), 'Gb4': (2, 7)}))


def chrom_up(n):
    i, a, o = M.parse(n)
    if a == -1: return M.mk(i, 0, o)
    if a == 0 and M.LET[i] in 'EB': return M.tr(n, 1, 1)
    if a == 0: return M.mk(i, 1, o)
    return M.tr(n, 1, 1)


def chrom_down(n):
    i, a, o = M.parse(n)
    if a == 1: return M.mk(i, 0, o)
    if a == 0 and M.LET[i] in 'CF': return M.tr(n, -1, -1)
    if a == 0: return M.mk(i, -1, o)
    return M.tr(n, -1, -1)


def arp_shape(chord, root_note, root_string, width=4):
    """the chord's notes from the root upward, in one position (the index finger at the root's fret or one below it, each
    finger its own fret; a string with no chord note there may reach one fret further), then every pair of chord notes on
    one string joined by the frets between them (p. 67)"""
    tones = {M.pc(p + '4') for p in M.tone_pcs(chord)}
    rf = M.midi(root_note) - M.OPEN[root_string]
    best = None
    for h in (rf - 1, rf):
        notes, last = [], M.midi(root_note) - 1
        for s in range(root_string, 0, -1):
            got = [f for f in range(h, h + width) if (M.OPEN[s] + f) % 12 in tones and M.OPEN[s] + f > last]
            if not got:
                got = [f for f in (h - 1, h + width) if (M.OPEN[s] + f) % 12 in tones and M.OPEN[s] + f > last][:1]
            for f in got:
                notes.append((M.OPEN[s] + f, s, f)); last = M.OPEN[s] + f
        if best is None or len(notes) > len(best[1]): best = (h, notes)
    h, notes = best
    out = []
    for k, (m, s, f) in enumerate(notes):
        out.append((m, s, f, 'tone'))
        if k + 1 < len(notes) and notes[k + 1][1] == s:
            for ff in range(f + 1, notes[k + 1][2]): out.append((M.OPEN[s] + ff, s, ff, 'fill'))
    return out, h


def spell_line(chord, ms_kinds):
    """chord notes spelled from the chord; fills spelled up from the note below"""
    tone_name = {M.pc(p + '4'): p for p in M.tone_pcs(chord)}
    out = []
    for m, kind in ms_kinds:
        if kind == 'tone':
            p = tone_name[m % 12]
            o = (m - M.midi(p + '0')) // 12
            out.append(p + str(o))
        else:
            out.append(chrom_up(out[-1]))
            assert M.midi(out[-1]) == m, (out, m)
    return out


def arp_bars(chord, root_note, root_string, txt, width=4):
    sh, h = arp_shape(chord, root_note, root_string, width)
    names = spell_line(chord, [(m, k) for m, s, f, k in sh])
    pos = [(s, f) for m, s, f, k in sh]
    n = len(names)
    total = 4 * -(-(0.5 * (n - 1) + 1.0) // 4)
    durs = [0.5] * (n - 1) + [total - 0.5 * (n - 1)]
    # split at 4 beats
    bars, cur, t = [], [], 0.0
    for nm, p, d in zip(names, pos, durs):
        while d > 1e-9:
            take = min(d, 4 - t)
            cur.append((nm, p, take)); t += take; d -= take
            if t >= 4 - 1e-9: bars.append(cur); cur, t = [], 0.0
    if cur: bars.append(cur)
    out = []
    for j, b in enumerate(bars):
        ns = [x[0] for x in b]; ps = [x[1] for x in b]; ds = [x[2] for x in b]
        out.append(dict(chords=[chord], items=[M.placed(ns, ps, ds, 'over ' + M.dname(chord))], note=txt if j == 0 else '…on up.'))
    LINES.append(('arpegios', 0, seg(chord, names, durs, type='arp', pos=pos, kinds=[k for (m, s, f, k) in sh])))
    return out


ex('cromatismo', 'arpegios', 'Chromatic notes inside an arpeggio',
   ('Take any arpeggio shape that suits your fingering. Wherever two of the chord’s notes lie on the same string, play the frets between them: chromatic notes inside the '
    'arpeggio. Graciano advises knowing at least two shapes for each kind of chord, one with the root on the 6th string and one with the root on the 5th. Here the shapes '
    'for the chords of your songs, each played up with its chromatic notes.'),
   T('A C7 arpeggio shape beside the same shape with its chromatic notes marked, then the shapes he uses most: maj7, m7, 7, °7, m7♭5 and augmented (no sound: diagrams).', 67),
   arp_bars('Cm7', 'C3', 6, f'{IW}, bar 5: C minor 7, root on the 6th string. Each pair of chord notes on one string is joined by the frets between.')
   + arp_bars('Fm7', 'F3', 5, 'Bar 9: F minor 7, root on the 5th string.')
   + arp_bars('Bb7', 'Bb2', 6, 'Bar 2: B♭7, root on the 6th string.')
   + arp_bars('F7', 'F3', 5, 'Bar 11: F7, root on the 5th string.')
   + arp_bars('Abmaj7', 'Ab2', 6, 'Bar 7: A♭ major 7, root on the 6th string.')
   + arp_bars('Abmaj7', 'Ab3', 5, 'The same chord, root on the 5th string.')
   + arp_bars('Abm6', 'F3', 5, 'Bar 19: A♭ minor 6, the same four notes as F half-diminished (F, A♭, C♭, E♭): its shape from F, root on the 5th string.')
   + arp_bars('Adim7', 'A2', 6, f'{GLI}, bar 7: A°7, root on the 6th string.')
   + arp_bars('G+', 'G3', 5, f'{YVL}, bar 24: G augmented, root on the 5th string. Its notes are a major 3rd apart, so the shape takes five frets (from the 8th fret up, where the hand allows it).', width=5))


def nb_up(n):
    """the semitone above, on the next letter (E→F, D→E♭), or the same letter raised where the next would be F♭ or C♭"""
    c = M.tr(n, 1, 1)
    if c[0] in 'FC' and c[1:2] == 'b': c = M.mk(M.parse(n)[0], M.parse(n)[1] + 1, M.parse(n)[2])
    return c


def nb_down(n):
    """the semitone below, on the letter below (E→D♯, D→C♯), or the same letter lowered where it would be E♯ or B♯"""
    c = M.tr(n, -1, -1)
    if c[0] in 'EB' and c[1:2] == '#': c = M.mk(M.parse(n)[0], M.parse(n)[1] - 1, M.parse(n)[2])
    return c


def vecina(chord, t):
    return seg(chord, [t, nb_up(t), t, nb_down(t), t], [0.5] * 5, type='neighbour')


ex('cromatismo', 'vecina', 'Neighbour notes',
   ('Aim at a note of the chord, the target, then touch the nearest note a semitone above it and the nearest a semitone below, coming back to the target each time. '
    'It works going up or going down. His figure fills three beats, so here it sits on a waltz, one chord a bar.'),
   T('Over A minor: an eighth rest, then E, F, E, D♯, E; then C with D♭ and B; then A with B♭ and G♯.', 67, ['E4', 'F4', 'E4', 'D#4'], [0.5] * 4),
   line_bars('vecina', [[rest(0.5), vecina('G', 'D5')], [rest(0.5), vecina('C', 'G4')], [rest(0.5), vecina('Cm6', 'Eb5')], [rest(0.5), vecina('D', 'F#4')]],
             [f'{YVL}, bars 1–4, in three. G: around D, its 5th.', 'C: around G, its 5th.', 'C minor 6: around E♭, its 3rd (the semitone above it is E♮).',
              'D: around F♯, its 3rd (the semitone below it is F♮).'], near=7))


def chrom_run(a, b):
    """semitones from a to b, spelled: going down on flats, going up on sharps"""
    out = [a]
    while M.midi(out[-1]) != M.midi(b):
        out.append(chrom_down(out[-1]) if M.midi(b) < M.midi(out[-1]) else chrom_up(out[-1]))
        if M.midi(out[-1]) == M.midi(b): out[-1] = b
    return out


A_FORM = [0.25, 0.25, 1 / 6, 1 / 6, 1 / 6]      # his first figure: two sixteenths, a sixteenth triplet, then the note
B_FORM = [0.25] * 4                              # his second: four sixteenths, then the note
C_FORM = [1 / 3] * 3                             # his third: an eighth-note triplet, then the note

ex('cromatismo', 'paso', 'Passing notes',
   ('Join two notes of the chord by the semitones between them. His three figures: a 4th filled in sixteenths and a sixteenth triplet, a major 3rd in four sixteenths, '
    'a minor 3rd in an eighth-note triplet, each landing on the chord note. Here each lands and is held to the end of the bar.'),
   T('Over A minor: A down to E, then E down to C, then C down to A, by semitones.', 68, ['A4', 'Ab4', 'G4', 'Gb4', 'F4', 'E4'], A_FORM + [0.5]),
   line_bars('paso', [
       [seg('Eb', chrom_run('Eb5', 'Bb4'), A_FORM + [3.0], type='passing')],
       [seg('Bb7', chrom_run('D5', 'Bb4'), B_FORM + [3.0], type='passing')],
       [seg('Eb', chrom_run('Bb4', 'G4'), C_FORM + [3.0], type='passing')]],
       [f'{IW}, bars 1–3. E♭: from the root down a 4th to B♭, his first figure.', 'B♭7: from D, its 3rd, down a major 3rd to the root, his second.',
        'E♭: from B♭ down a minor 3rd to G, his third.']))


def combo(chord, x, y, pass_form):
    run_ = chrom_run(y, x)
    return seg(chord, [x, nb_up(x), x, nb_down(x), x] + run_, [0.5, 0.25, 0.25, 0.25, 0.25] + pass_form + [1.0], type='combo', target=x, top=y)


ex('cromatismo', 'combinacion', 'Neighbours and passing notes together',
   ('The two together: the neighbour figure around a note of the chord, then a leap up to another note of the chord and down again by semitones to the first.'),
   T('Over A minor: E with its neighbours in sixteenths, then A down to E by semitones; then the same on A (from C) and on C (from E).', 68,
     ['E4', 'F4', 'E4', 'D#4', 'E4', 'A4', 'Ab4'], [0.5, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25]),
   line_bars('combinacion', [
       [rest(0.5), combo('Fm7', 'C4', 'F4', A_FORM)],
       [rest(0.5), combo('C7', 'E4', 'G4', C_FORM)],
       [rest(0.5), combo('F7', 'F4', 'A4', B_FORM)]],
       [f'{IW}, bars 9–11. F minor 7: around C, its 5th, then down from F by semitones.', 'C7: around E, its 3rd, then down from G.',
        'F7: around the root, then down from A, its 3rd.'], near=6))


def link(chord, arp, run_from, run_to, nxt):
    run_ = chrom_run(run_from, run_to)[:-1]
    return seg(chord, arp + run_, [1.0] * len(arp) + [0.5] * len(run_), type='link', arp=len(arp), next_chord=nxt, target=run_to)


ex('cromatismo', 'enlace', 'A chromatic link between two chords',
   ('Join a note of one chord to a note of the next by semitones, so the line arrives on the new chord exactly as it changes. Here two beats of the chord’s own notes, '
    'then the semitones into the next chord.'),
   T('From A minor to E7 (no sound here: his line is quoted in words only).', 68),
   line_bars('enlace', [
       [link('C7', ['E4', 'G4'], 'C5', 'Ab4', 'Fm7')], [seg('Fm7', ['Ab4'], [4.0], type='land')],
       [link('F7', ['F3', 'A3'], 'Eb4', 'G4', 'Cm7')], [seg('Cm7', ['G4'], [4.0], type='land')],
       [link('G7', ['G3', 'B3'], 'D4', 'Bb3', 'Cm7')], [seg('Cm7', ['Bb3'], [2.0], type='land'), rest(2.0)]],
       [f'{IW}, bars 8–9. C7: E and G, then from C down by semitones…', '…to A♭, the 3rd of F minor 7, as it arrives.',
        'Bars 12–13. F7: F and A, then from E♭, its 7th, up by semitones…', '…to G, the 5th of C minor 7.',
        'Bars 18–19. G7: G and B, then from D down…', '…to B♭, the 7th of C minor 7.'], near=6))

ex('cromatismo', 'patrones', 'Chromatic patterns',
   ('Two chromatic patterns in sixteenths. a) Three sounds down and up: a note, the semitone under it, the note again, then a semitone up; the next group starts a semitone '
    'higher still, so the line climbs. b) By whole tones: four semitones down, and each group starts a whole tone below the last. '
    'His examples of all these devices in use come from tangos still under copyright and are described here, not written out: a variation on Troilo’s Responso '
    '(a running sixteenth line over D7 and G minor made almost entirely of neighbour and passing semitones), the second part of Piazzolla’s Otoño porteño (a long note in '
    'each bar answered by a chromatic run), a background for Rovira’s A Evaristo Carriego (a held note over an inner line creeping down by semitones), and the Troilo '
    'orchestra’s variation on Inspiración.'),
   T('a) from E up to B; b) from A down, in four groups.', 69, ['E4', 'D#4', 'E4', 'F4', 'F#4', 'E#4', 'F#4', 'G4'], [0.25] * 8),
   line_bars('patrones', [
       [seg('Bb7', ['D4', 'C#4', 'D4', 'Eb4', 'E4', 'D#4', 'E4', 'F4', 'F#4', 'F4', 'F#4', 'G4', 'G#4', 'G4', 'G#4', 'A4'], [0.25] * 16, type='chrom-a', next_target='Bb4', next_chord='Eb')],
       [seg('Eb', ['Bb4'], [4.0], type='land')],
       [seg('Bb7', ['F5', 'E5', 'Eb5', 'D5', 'Eb5', 'D5', 'Db5', 'C5', 'Db5', 'C5', 'B4', 'Bb4', 'B4', 'Bb4', 'A4', 'Ab4'], [0.25] * 16, type='chrom-b', next_target='G4', next_chord='Eb')],
       [seg('Eb', ['G4'], [4.0], type='land')]],
       [f'{IW}, bars 2–3. B♭7: pattern a from D, its 3rd, climbing a whole tone a group…', '…onto B♭, the 5th of E♭.',
        'Bars 16–17. B♭7: pattern b from F, its 5th, falling a whole tone a group…', '…and the last semitone falls onto G, the 3rd of E♭.'], near=7))


# ================================================================ blue notes (pp. 71–72)
def two(bars_steps, label, lo_strings=(6, 5, 4, 3), up_strings=(3, 2, 1)):
    """two-voice bars from (lower, upper, beats) steps"""
    out = []
    for steps in bars_steps:
        seq = [(M.midi(lo) if lo else None, M.midi(up) if up else None, d) for lo, up, d in steps]
        pl = place_lines(seq, lo_strings=lo_strings, up_strings=up_strings, maxf=13, prefer=6, open_cost=2.0)
        out.append(two_lines(pl, over=label))
    return out


ex('blue', 'blues', 'The blues scale',
   ('In the blues the raised 4th is played as an inflection of the line: the blue note. The blues scale: 1, ♭3, 4, ♯4, 5, ♭7. Graciano shows it entering tango, in the writing and '
    'the arranging, from the 1960s on: the main motive of Piazzolla’s Otoño porteño, a phrase of his Escualo, Graciano’s own A Rovira and Salgán’s A fuego lento all '
    'put the raised 4th of the minor key into their melody (all still under copyright, described here, not written out).'),
   T('The blues scale on A in quarters, the ♯4 circled as the blue note.', 71, ['A2', 'C3'], [1.0, 1.0]),
   line_bars('blues', [
       [seg('Am', ['A3', 'C4', 'D4', 'D#4', 'E4', 'G4', 'A4', 'G4'], E8, type='scale', root='A', kind='blues', start_tone=True)],
       [seg('Am', ['E4', 'D#4', 'D4', 'C4', 'A3'], [0.5] * 4 + [2.0], type='scale', root='A', kind='blues', start_tone=True)]],
       [f'{OCI}, bars 3–4: A minor. Up the A blues scale through the D♯…', '…and down again.'], near=5))

ex('blue', 'jazz', 'The jazz scale',
   ('Jazz added two more blue notes, the major 7th and the major 3rd: 1, ♭3, 3, 4, ♯4, 5, ♭7, 7.'),
   T('The jazz scale on A, its three blue notes circled.', 71, ['A2', 'C3'], [1.0, 1.0]),
   line_bars('jazz', [
       [seg('Am', ['A3', 'C4', 'C#4', 'D4', 'D#4', 'E4', 'G4', 'G#4'], E8, type='scale', root='A', kind='jazz', start_tone=True)],
       [seg('Am', ['A4', 'G#4', 'G4', 'E4', 'D#4', 'D4', 'C#4', 'C4'], E8, type='scale', root='A', kind='jazz', start_tone=True)]],
       [f'{OCI}, bars 7–8: A minor. Up the A jazz scale…', '…and down, ending on C.'], near=5))

ex('blue', 'dominante', 'The major 7th over a dominant',
   ('Over a dominant chord, the major 7th as a blue note between the chord’s 7th and its root: ♭7, 7, root, each time an octave higher. '
    'Graciano gives it as a fill typical of Orlando Goñi’s piano.'),
   T('A fill over G7: F, F♯, G, climbing by octaves (no sound here: described only).', 71),
   [dict(chords=['E7'], items=[M.placed(['D3', 'D#3', 'E3', 'D4', 'D#4', 'E4', 'D5', 'D#5', 'E5'],
                                        [(5, 5), (5, 6), (5, 7), (3, 7), (3, 8), (3, 9), (1, 10), (1, 11), (1, 12)],
                                        [1 / 3] * 8 + [1 / 3 + 1.0], 'over E7')],
         note=f'{OCI}, bar 1: E7. D, D♯, E in three octaves, in triplets: each cell on one string, the hand moving up for the next.')])
LINES.append(('dominante', 0, seg('E7', ['D3', 'D#3', 'E3', 'D4', 'D#4', 'E4', 'D5', 'D#5', 'E5'], [1 / 3] * 8 + [1 / 3 + 1.0], type='blue7')))

ex('blue', 'interludio', 'The raised 4th over a minor chord',
   ('Between two parts, over a minor chord with the bass moving under it, the line touches the raised 4th, the blue note, between the 4th and the 5th.'),
   T('Over D minor, the bass moving in quarters, the line reaches G♯ and comes back to it (no sound here: described only).', 71),
   [dict(chords=['Am'], items=two([[('A2', None, 0.5), (None, 'C4', 0.5), ('E2', 'D4', 1.0), ('A2', 'D#4', 1.0), ('E2', 'E4', 1.0)]], 'two lines'),
         note=f'{OCI}, bar 11: A minor. The bass A and E; above it C, D, D♯, E.'),
    dict(chords=['Am'], items=two([[('A2', 'E4', 1.0), ('E2', 'D#4', 0.5), (None, 'D4', 0.5), ('A2', 'C4', 2.0)]], 'two lines'),
         note='Bar 12: down again through the D♯.')])
LINES += [('interludio', 0, seg('Am', ['C4', 'D4', 'D#4', 'E4'], [0.5, 1.0, 1.0, 1.0], type='blue4', root='A')),
          ('interludio', 1, seg('Am', ['E4', 'D#4', 'D4', 'C4'], [1.0, 0.5, 0.5, 2.0], type='blue4', root='A'))]

ex('blue', 'pedal', 'A pedal note on top',
   ('Over a minor chord, the top note held as a pedal while an inner voice moves under it through the raised 4th.'),
   T('Over A minor, A held on top while the voice under it moves through D♯ (no sound here: described only).', 72),
   [dict(chords=['Dm'], items=two([[('F4', 'D5', 1.0), ('G4', 'D5', 1.0), ('G#4', 'D5', 1.0), ('A4', 'D5', 1.0)]], 'two lines', (4, 3, 2), (2, 1)),
         note=f'{OCI}, bar 9: D minor. D held on top; under it F, G, G♯, A.'),
    dict(chords=['Dm'], items=two([[('A4', 'D5', 1.0), ('G#4', 'D5', 1.0), ('G4', 'D5', 1.0), ('F4', 'D5', 1.0)]], 'two lines', (4, 3, 2), (2, 1)),
         note='Bar 10: back down.')])
LINES += [('pedal', 0, seg('Dm', ['F4', 'G4', 'G#4', 'A4'], [1.0] * 4, type='blue4', root='D', pedal='D5')),
          ('pedal', 1, seg('Dm', ['A4', 'G#4', 'G4', 'F4'], [1.0] * 4, type='blue4', root='D', pedal='D5'))]

CL = [[[6, 0]], [[3, 8], [2, 5]], [[6, 7]], [[3, 8], [2, 5]]]
ex('blue', 'cluster', 'A cluster on the root and the major 7th',
   ('Over a dominant, the root and the major 7th struck together as a cluster, high above the bass.'),
   T('Over A7, G♯ and A together above the bass (no sound here: described only).', 72),
   [dict(chords=['E7'], items=[two_lines([(g, 1.0) for g in CL], over='=E,D♯+E,B,D♯+E|the cluster')],
         note=f'{OCI}, bar 13: E7. The bass E and B; above it D♯ and E together, a semitone apart.')])
LINES += [('cluster', 0, seg('E7', ['D#4', 'E4'], [1.0, 1.0], type='cluster', pos=[(3, 8), (2, 5)]))]

E7G = [-1, 7, 6, 7, 5, -1]          # E7: E3 G♯3 D4 E4
APIC = [-1, 12, 11, 9, 10, 9]       # A major with C♯ on top: A3 C♯4 E4 A4 C♯5
ex('blue', 'picardia', 'The major 3rd at the end of a phrase',
   ('In a minor key, ending a phrase on the major 3rd: the old tierce de Picardie. Graciano’s example is from Laurenz and Maffia’s Amurado (still under copyright, '
    'described only), where a phrase in C minor ends on E♮.'),
   T('From Amurado: the phrase in C minor ends on E♮ (described only).', 72),
   line_bars('picardia', [[seg('E7', ['E4', 'F4', 'G#4', 'A4', 'B4', 'C5', 'D5'], [0.5] * 6 + [1.0], type='scale', root='A', kind='harmonic minor', start_tone=True)]],
             [f'{OCI}, bars 15–16. E7: up A harmonic minor to D, its 7th…'], near=7)
   + [dict(chords=['A'], items=[K('A', APIC, [(4.0, [5, 4, 3, 2, 1])])], note='…which falls a semitone to C♯: the last chord A major, not A minor, its 3rd on top.')])
LINES += [('picardia', 1, seg('A', ['C#5'], [4.0], type='picardy', grip=APIC, key='A'))]


# ================================================================ guide tones (pp. 72–75)
def gseg(chord, notes, durs, cadence=False):
    return seg(chord, notes, durs, type='guide', cadence=cadence)


GT_TXT = ['C minor 7', 'F7', 'F7, then B♭7', 'B♭7', 'E♭']
ex('guias', 'septima', 'From the 7th',
   ('Graciano’s rules for a guide-tone line, the counter-melody a second guitar plays under the tune: use each chord’s 3rd and 7th (and on diminished, half-diminished '
    'and augmented chords, its 5th too). Pick the first note, then join a 3rd to a 7th and a 7th to a 3rd, with no leap where the chord changes; a leap is allowed only '
    'inside one chord. It sings that way. Where the tune itself has the 3rd or 7th, leave that note out of the line. '
    'His examples are on the chords of Expósito’s Naranjo en flor (still under copyright); ours on I Wonder’s. First: start on the 7th, one note a chord.'),
   T('Over Fmaj7, F7, G7, C7, Fmaj7: E, E♭, F, E, A, one note a chord.', 73, ['E3'], [2.0]),
   line_bars('septima', [[gseg('Cm7', ['Bb4'], [4.0])], [gseg('F7', ['A4'], [4.0])], [gseg('F7', ['A4'], [2.0]), gseg('Bb7', ['Ab4'], [2.0])],
                         [gseg('Bb7', ['Ab4'], [4.0])], [gseg('Eb', ['G4'], [4.0])]],
             [f'{IW}, bars 13–17. C minor 7: B♭, its 7th.', 'F7: down a semitone to A, its 3rd.', 'A still; then B♭7: down to A♭, its 7th.', 'A♭.',
              'E♭: down to G, its 3rd.'], near=6))

ex('guias', 'tercera', 'From the 3rd',
   ('The same rules, starting on the 3rd. At the cadence, where the line would end on a 7th, tango usually ends on the root.'),
   T('Over the same chords: A, B, B♭, A.', 73, ['A3'], [2.0]),
   line_bars('tercera', [[gseg('Cm7', ['Eb4'], [4.0])], [gseg('F7', ['Eb4'], [4.0])], [gseg('F7', ['Eb4'], [2.0]), gseg('Bb7', ['D4'], [2.0])],
                         [gseg('Bb7', ['D4'], [4.0])], [gseg('Eb', ['Eb4'], [4.0], cadence=True)]],
             [f'{IW}, bars 13–17. C minor 7: E♭, its 3rd.', 'F7: E♭ stays, now its 7th.', 'Then B♭7: down to D, its 3rd.', 'D.',
              'E♭: up to the root, as tango ends.'], near=6))

ex('guias', 'ambas7', 'Both guide tones, from the 7th',
   ('Both guide tones in each chord, the 7th first: the leap is inside the chord, the step at the change.'),
   T('Over the same chords, two notes a chord.', 73, ['E3', 'A3'], [1.0, 1.0]),
   line_bars('ambas7', [[gseg('Cm7', ['Bb4', 'Eb5'], [2.0, 2.0])], [gseg('F7', ['Eb5', 'A4'], [2.0, 2.0])],
                        [gseg('F7', ['Eb5'], [2.0]), gseg('Bb7', ['D5'], [2.0])], [gseg('Bb7', ['Ab4', 'D5'], [2.0, 2.0])], [gseg('Eb', ['Eb5'], [4.0], cadence=True)]],
             [f'{IW}, bars 13–17. C minor 7: B♭, then E♭.', 'F7: E♭ stays (its 7th now), then A.', 'E♭ again; B♭7: down to D.', 'A♭, D.', 'E♭.'], near=7))

ex('guias', 'ambas3', 'Both guide tones, from the 3rd',
   ('Both in each chord, the 3rd first.'),
   T('Over the same chords, from the 3rd.', 73, ['A3', 'E3'], [1.0, 1.0]),
   line_bars('ambas3', [[gseg('Cm7', ['Eb4', 'Bb4'], [2.0, 2.0])], [gseg('F7', ['A4', 'Eb5'], [2.0, 2.0])],
                        [gseg('F7', ['A4'], [2.0]), gseg('Bb7', ['Ab4'], [2.0])], [gseg('Bb7', ['D5', 'Ab4'], [2.0, 2.0])], [gseg('Eb', ['G4'], [4.0])]],
             [f'{IW}, bars 13–17. C minor 7: E♭, then B♭.', 'F7: down to A, then E♭.', 'A; B♭7: A♭.', 'D, A♭.', 'E♭: G.'], near=7))

ex('guias', 'disminuido', 'The 5th of a diminished chord',
   ('On diminished, half-diminished and augmented chords the 5th is a guide tone too.'),
   T('The rule in words: on these three chords, add the 5th.', 72),
   line_bars('disminuido', [[gseg('G7', ['B4', 'F4'], [2.0, 2.0])], [gseg('Cm', ['Eb4'], [2.0]), gseg('Adim7', ['Eb4', 'C4'], [1.0, 1.0])],
                            [gseg('Bb', ['D4'], [2.0]), gseg('Bb7', ['D4'], [2.0])]],
             [f'{GLI}, bars 6–8. G7: B, then F.', 'C minor: E♭; A°7: E♭ stays, now its 5th, then C, its 3rd.', 'B♭: up to D, and D stays into B♭7.'], near=6))

ex('guias', 'adorno', 'Adding ornaments',
   ('The second stage: once the 3rds and 7ths join, ornament the line with passing notes, an appoggiatura (a step above or below, then the note) and arpeggiation, '
    'keeping the guide tones where they were.'),
   T('The line from the 3rd over the same chords, with passing notes, an appoggiatura and an arpeggio marked (no sound here: described only).', 73),
   line_bars('adorno', [[seg('Cm7', ['Eb4', 'F4', 'G4', 'Ab4', 'Bb4'], [1.0, 0.5, 0.5, 1.0, 1.0], type='adorno', guides=['Eb4', 'Bb4'])],
                        [seg('F7', ['A4', 'C5', 'Eb5'], [1.0, 1.0, 2.0], type='adorno', guides=['A4', 'Eb5'])],
                        [seg('F7', ['A4'], [2.0], type='adorno', guides=['A4']), seg('Bb7', ['G4', 'Ab4'], [0.5, 1.5], type='adorno', guides=['Ab4'])],
                        [seg('Bb7', ['D5', 'C5', 'Bb4', 'Ab4'], [1.0, 0.5, 0.5, 2.0], type='adorno', guides=['D5', 'Ab4'])],
                        [seg('Eb', ['G4'], [4.0], type='adorno', guides=['G4'])]],
             [f'{IW}, bars 13–17, the line from the 3rd. C minor 7: E♭ to B♭ through F, G, A♭ (passing notes).', 'F7: A to E♭ through C (arpeggiation).',
              'A; then B♭7: G a step under A♭, then A♭ (an appoggiatura).', 'D to A♭ through C, B♭.', 'G.'], near=7))

ex('guias', 'retardo', 'Suspension and anticipation',
   ('A guide tone held over into the next chord, then resolved (suspension), or the next chord’s guide tone arriving before its chord (anticipation).'),
   T('Over the same chords, suspensions and an anticipation marked R and A.', 74, ['A3', 'E3'], [1.0, 1.0]),
   line_bars('retardo', [[gseg('Cm7', ['Bb4'], [4.0])], [seg('F7', ['Bb4', 'A4'], [1.0, 3.0], type='suspension')],
                         [gseg('F7', ['A4'], [2.0]), seg('Bb7', ['A4', 'Ab4'], [0.5, 1.5], type='suspension')],
                         [seg('Bb7', ['Ab4', 'G4'], [3.5, 0.5], type='anticipation', next_chord='Eb')], [gseg('Eb', ['G4'], [4.0])]],
             [f'{IW}, bars 13–17, the line from the 7th. C minor 7: B♭.', 'F7: the B♭ held over the change, then down to A.', 'A; B♭7: the A held over a moment, then A♭.',
              'A♭, and G, E♭’s 3rd, comes early.', 'E♭.'], near=6))


# the guide tone on top of the chord (p. 74): grips whose top note is the line from the 7th
CM7T = [8, 10, -1, 8, 11, -1]        # C3 G3 E♭4 B♭4
F7T = [-1, 8, 10, 8, 10, -1]         # F3 C4 E♭4 A4
BB7T = [6, 8, -1, 7, 9, -1]          # B♭2 F3 D4 A♭4
EBT = [-1, 6, 8, 8, 8, -1]           # E♭3 B♭3 E♭4 G4


def strings_of(g): return [6 - i for i in range(6) if g[i] >= 0]


ex('guias', 'arriba', 'The guide tone on top of the chord',
   ('On one guitar: make the guide tone the chord’s top note. At the top it rings brighter, and the chords carry a counter-line of their own. '
    'Then fill it out with passing notes, fills and bass notes, keeping the top line whole. Each chord here is struck once and rings while it lasts.'),
   T('Fmaj7, F7, G7, D♭7, C7, F with the guide tones on top (no sound here: described only).', 74),
   [dict(chords=['Cm7'], items=[K('Cm7', CM7T, [(4.0, strings_of(CM7T))])], note=f'{IW}, bars 13–17. C minor 7 with B♭ on top.'),
    dict(chords=['F7'], items=[K('F7', F7T, [(4.0, strings_of(F7T))]) + [{'hold': 6.0, 'strings': strings_of(F7T)}]], note='F7 with A on top, ringing into the next bar.'),
    dict(chords=['F7', 'Bb7'], items=[['W', 2.0], K('Bb7', BB7T, [(2.0, strings_of(BB7T))]) + [{'hold': 6.0, 'strings': strings_of(BB7T)}]],
         note='B♭7 with A♭ on top, ringing through the next bar.'),
    dict(chords=['Bb7'], items=[['W', 4.0]], note='(B♭7 rings on.)'),
    dict(chords=['Eb'], items=[K('Eb', EBT, [(4.0, strings_of(EBT))])], note='E♭ with G on top.'),
    dict(chords=['Cm7'], items=[K('Cm7', CM7T, [(3.0, strings_of(CM7T))]), M.placed(['E3'], [(5, 7)], [1.0], 'the bass into F')],
         note='Filled out: C minor 7, then E in the bass on beat 4, a semitone under F.'),
    dict(chords=['F7'], items=[K('F7', F7T, [(3.0, strings_of(F7T))]), M.placed(['C3'], [(6, 8)], [1.0], 'the bass')],
         note='F7, and C, its 5th, in the bass.'),
    dict(chords=['F7', 'Bb7'], items=[M.placed(['A2'], [(6, 5)], [2.0], 'the bass into B♭'), K('Bb7', BB7T, [(2.0, strings_of(BB7T))])],
         note='A in the bass under the F7 (its 3rd, a semitone under B♭), then B♭7.'),
    dict(chords=['Bb7'], items=[M.placed(['F3', 'D3'], [(5, 8), (5, 5)], [3.0, 1.0], 'the bass into E♭')],
         note='The B♭7 rings on over F in the bass, then D, a semitone under E♭.'),
    dict(chords=['Eb'], items=[K('Eb', EBT, [(4.0, strings_of(EBT))])], note='E♭: the top line B♭, A, A♭, G is unbroken.')])
LINES += [('arriba', i, seg(c, [n], [1.0], type='top', grip=g)) for i, (c, n, g) in enumerate([('Cm7', 'Bb4', CM7T), ('F7', 'A4', F7T), ('Bb7', 'Ab4', BB7T), ('Eb', 'G4', EBT)])]


SECTIONS = [dict(id='escala', title='The scale for each chord', part='Exercises', ex=EXS['escala']),
            dict(id='cromatismo', title='Chromatic notes', part='Exercises', ex=EXS['cromatismo']),
            dict(id='blue', title='Blue notes', part='Exercises', ex=EXS['blue']),
            dict(id='guias', title='Guide tones', part='Exercises', ex=EXS['guias'])]

sys.path.insert(0, '/home/claude/studies/tango')
from quotes import trim as _trim_quotes   # quotes stay a beat or two
_trim_quotes(SECTIONS)
