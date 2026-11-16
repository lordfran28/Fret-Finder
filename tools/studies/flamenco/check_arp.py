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
if set(EXS) != set(HIS): P(f'exercises {sorted(EXS)}')
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
print('patterns checked:', len(HIS), '· changes:', ' '.join(changes))
print('\n'.join(probs) if probs else 'all good')
sys.exit(1 if probs else 0)
