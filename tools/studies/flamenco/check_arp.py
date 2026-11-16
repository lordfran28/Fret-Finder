"""Independent checks for serrano_arp.py: every bar's notes (string and length, finger from the accents) against Serrano's
four patterns as transcribed here from his pages 46–48 (strings read from his tablature), the chords against your
Очи чёрные page, each grip against its chord with the root on the low E string."""
import sys, re, json
sys.path.insert(0, '/home/claude/studies'); sys.path.insert(0, '/home/claude/studies/flamenco'); sys.path.insert(0, '/home/claude/scripts')
import serrano_arp as A
import gtr

probs = []
def P(m): probs.append(m)

# his patterns, beat by beat: finger and string (1 = high E)
HIS = {
    'arp-1': ['p6 a1 m2 i3', 'p5 a1 m2 i3', 'p4 a1 m2 i3'],
    'arp-2': ['p6 i3 m2 a1 m2 i3', 'p5 i3 m2 a1 m2 i3', 'p4 i3 m2 a1 m2 i3'],
    'arp-3': ['p6 i4 m3 i4', 'a2 i4 m3 i4', 'a1 i4 m3 i4', 'a2 i4 m3 i4'],
    'arp-4': ['p6 i3 m2', 'a1 m2 i3', 'a2 m3 i4', 'a3 m4 i5'],
}
h = open('/home/claude/fret-finder/songs/ochi-chyornye/index.html').read()
m = re.search(r'"title": "The plain chart".*?"chords": (\[\[.*?\]\]), "tab"', h, flags=re.S)
changes = [b[0]['c'] for b in json.loads(m.group(1))][0::2]
OPENS = [40, 45, 50, 55, 59, 64]
EXS = {ex['id']: ex for ex in A.SECTION['ex']}
if set(EXS) != set(HIS) | {'thumb', 'trem'}: P(f'exercises {sorted(EXS)}')
for exid, beats in HIS.items():
    ex = EXS.get(exid)
    if not ex: continue
    want = [(tok[0], int(tok[1:]), 1 / len(b.split())) for b in beats for tok in b.split()]
    if len(ex['bars']) != len(changes) + 1: P(f'{exid}: {len(ex["bars"])} bars')
    for k, B in enumerate(ex['bars']):
        it = B['items'][0]
        name, g, hits = it[1], it[2], it[3]
        pcs = {(OPENS[i] + f) % 12 for i, f in enumerate(g) if f >= 0}
        if not pcs <= gtr.chord_pcs(name) or not ({gtr.parse(name)[0]} <= pcs): P(f'{exid} bar {k + 1}: {name} {g}')
        if g[0] < 0 or (OPENS[0] + g[0]) % 12 != gtr.parse(name)[0]: P(f'{exid} bar {k + 1}: the root is not on the low E string')
        if k < len(changes):
            if name != changes[k]: P(f'{exid} bar {k + 1}: {name}, the song has {changes[k]}')
            got = [(h_[1], h_[0], h_[2] if len(h_) > 2 else 0) for h_ in hits]
            if len(got) != len(want): P(f'{exid} bar {k + 1}: {len(got)} notes'); continue
            for j, ((ss, d, v), (f, s, wd)) in enumerate(zip(got, want)):
                if ss != [s]: P(f'{exid} bar {k + 1} note {j + 1}: string {ss}, Serrano {s}')
                if abs(d - wd) > 1e-9: P(f'{exid} bar {k + 1} note {j + 1}: length')
                if (v > 0) != (f in 'pa'): P(f'{exid} bar {k + 1} note {j + 1}: the {f} is {"marked" if v > 0 else "not marked"}')
        else:
            if name != 'Am' or len(hits) != 1 or hits[0][1] != [6]: P(f'{exid}: does not end on the bass alone')
            if abs(hits[0][0] - len(beats)) > 1e-9: P(f'{exid}: the last bar is not a whole bar')
    # the quote: his first beat on E
    q = ex['quote']['items'][0]
    if q[2] != [0, 2, 2, 1, 0, 0] or [h_[1][0] for h_ in q[3]] != [int(t[1:]) for t in beats[0].split()]: P(f'{exid}: quote')
# the thumb study: his contour (p. 41) in A harmonic minor: up in pairs a step apart, upper note first, A to F; G♯ over E;
# down in pairs a third apart, F to A; then the note a step above the last
sc = [m for m in range(30, 80) if m % 12 in {9, 11, 0, 2, 4, 5, 8}]
i_a, i_f = sc.index(45), sc.index(65)
want = [x for k in range(i_a, i_f + 1) for x in (sc[k], sc[k - 1])] + [sc[i_f + 1], sc[i_f - 1]] + [x for k in range(i_f, i_a - 1, -1) for x in (sc[k], sc[k - 2])] + [sc[i_a - 1]]
if len(want) != 55: P('thumb: his study has 55 notes')
ex = EXS.get('thumb')
if not ex: P('thumb study missing')
else:
    got, durs = [], []
    for B in ex['bars']:
        it = B['items'][0]
        if it[0] != 'R': P('thumb: not a run'); continue
        for (st, f), d in zip(it[1], it[2]):
            if not 0 <= f <= 4: P(f'thumb: fret {f} outside the first position')
            got.append(OPENS[6 - st] + f); durs.append(d)
        if abs(sum(it[2]) - 4) > 1e-9: P('thumb: a bar is not four beats')
        names = it[3][1:].split('|')[0].split(',')
        NMS = {'A': 9, 'B': 11, 'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G♯': 8}
        if [NMS.get(n) for n in names] != [(OPENS[6 - st] + f) % 12 for st, f in it[1]]: P('thumb: the names do not match the notes')
    if got != want: P(f'thumb: the notes differ from his contour at {next((k for k, (a, b) in enumerate(zip(got, want)) if a != b), len(got))}')
    if durs[:-1] != [0.5] * (len(durs) - 1) or durs[-1] != 1.0: P('thumb: not eighths ending on a quarter')
# the tremolo study (p. 36): each beat the thumb on the chord's string, then the top note (high E string) four times;
# the thumb over two bars: low E, A, D, G, then B, G, D, A strings
THUMB = [6, 5, 4, 3, 2, 3, 4, 5]
ex = EXS.get('trem')
if not ex: P('tremolo study missing')
else:
    if len(ex['bars']) != 2 * len(changes) + 1: P(f'trem: {len(ex["bars"])} bars')
    for k, B in enumerate(ex['bars'][:-1]):
        it = B['items'][0]
        chord = changes[k // 2]
        g = A.GRIP[chord] if B['chords'] == [chord] else None
        if g is None: P(f'trem bar {k + 1}: {B["chords"]}, the song has {chord}'); continue
        notes, durs = it[1], it[2]
        if len(notes) != 20 or any(abs(d - 0.2) > 1e-9 for d in durs): P(f'trem bar {k + 1}: not five to a beat'); continue
        for b in range(4):
            th, *tr = notes[5 * b:5 * b + 5]
            s_ = THUMB[4 * (k % 2) + b]
            if th != [s_, g[6 - s_]]: P(f'trem bar {k + 1} beat {b + 1}: thumb {th}, wants string {s_}')
            if any(t != [1, g[5]] for t in tr): P(f'trem bar {k + 1} beat {b + 1}: the tremolo is not the top note')
        pcs = {(OPENS[i] + f) % 12 for i, f in enumerate(g) if f >= 0}
        if not pcs <= gtr.chord_pcs(chord): P(f'trem: {chord} grip')
print('patterns checked:', len(HIS), '· changes:', ' '.join(changes))
print('\n'.join(probs) if probs else 'all good')
sys.exit(1 if probs else 0)
