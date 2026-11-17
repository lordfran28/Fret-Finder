"""Independent check of Carcassi's arpeggios 12, 14, 16–20 and 22 (Op. 59, Melos copy pp. 15–16): his two bars written
out here as the notes he prints (written pitch, an octave above the sound), sixteenth or triplet by triplet, read from
the page; the entry's spec applied to his C and G7 grips must give exactly those notes in that rhythm."""
import sys, re
sys.path.insert(0, '/home/claude/studies'); sys.path.insert(0, '/home/claude/studies/carcassi')
import entry as E
OPEN = [40, 45, 50, 55, 59, 64]
LET = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
def nm(n):
    m = re.fullmatch(r'([A-G])(\d)', n); return 12 * (int(m.group(2)) + 1) + LET[m.group(1)]
probs = []
# each slot: notes struck together ('+'), slots separated by spaces; per bar; u = 1/4 or 1/3 of a beat
HIS = {
    12: ('C4 C5 G4 E5 C5 G4 E4 G4 ' * 2, 'G3 B4 G4 F5 B4 G4 D4 G4 ' * 2, 0.25),
    14: ('C4 G4 E4 G4 C5 G4 E4 G4 E5 G4 E4 G4 C5 G4 E4 G4', 'G3 G4 D4 G4 B4 G4 D4 G4 F5 G4 D4 G4 B4 G4 D4 G4', 0.25),
    16: ('C4+G4 E5 C5 E4+G4 E5 C5 ' * 2, 'G3+G4 F5 B4 D4+G4 F5 B4 ' * 2, 1 / 3),
    17: ('C4+G4 C5 E5 E4+E5 C5 G4 ' * 2, 'G3+G4 B4 F5 D4+F5 B4 G4 ' * 2, 1 / 3),
    18: ('C4+E5 E4 G4 ' * 4, 'B3+F5 D4 G4 ' * 4, 1 / 3),
    19: ('C4+G4 C5 E5 C5 E4+G4 C5 E5 C5 ' * 2, 'G3+G4 B4 F5 B4 D4+G4 B4 F5 B4 ' * 2, 0.25),
    20: ('C4+E5 G4 E4 G4 ' * 4, 'G3+F5 G4 D4 G4 ' * 4, 0.25),
    22: ('C4 G4+C5+E5 G4+C5+E5 G4+C5+E5 G4+C5+E5 G4+C5+E5 E4 G4+C5+E5 C4 G4+C5+E5 G4+C5+E5 G4+C5+E5 G4+C5+E5 G4+C5+E5 C4 G4+C5+E5',
         'G3 G4+B4+F5 B3 G4+B4+F5 D4 G4+B4+F5 B3 G4+B4+F5 G3 G4+B4+F5 D4 G4+B4+F5 B3 G4+B4+F5 G3 G4+B4+F5', 0.25),
}
G7, C_ = E.G7, E.C_
def sounds(item):
    name, grip, hits = item[1], item[2], item[3]
    out = []
    for h in hits:
        ms = sorted(OPEN[6 - s] + grip[6 - s] for s in h[1])
        out.append((round(h[0], 6), ms))
    return out
for k, (cb, gb, u) in HIS.items():
    a = E.A[k]
    for label, txt, grip, chord, spec in (('C', cb, C_, 'C', a['spec']), ('G7', gb, G7, 'G7', a.get('spec_g', a['spec']))):
        want = [(round(u, 6), sorted(nm(x) - 12 for x in slot.split('+'))) for slot in txt.split()]
        got = sounds(E.bar(spec(), chord, grip))
        if got != want:
            i = next((j for j, (x, y) in enumerate(zip(got, want)) if x != y), min(len(got), len(want)))
            probs.append(f'No. {k} on {label}: differs at slot {i + 1}: {got[i] if i < len(got) else None} vs {want[i] if i < len(want) else None}')
# ours: the same strings on Я вас любил's G and C major 7 (his C bar on Cmaj7, his G7 bar on G)
EX = {e['id']: e for e in E.EX}
for k in HIS:
    a = E.A[k]
    b_g, b_c = EX[f'arp-{k}']['bars']
    if [h[1] for h in b_g['items'][0][3]] != [h[1] for h in E.bar(a.get('spec_g', a['spec'])(), 'G7', G7)[3]]: probs.append(f'No. {k}: our G bar is not his G7 strings')
    if [h[1] for h in b_c['items'][0][3]] != [h[1] for h in E.bar(a['spec'](), 'C', C_)[3]]: probs.append(f'No. {k}: our C major 7 bar is not his C strings')
    for b, grip in ((b_g, E.G), (b_c, E.CM7)):
        if any(grip[6 - s] < 0 for h in b['items'][0][3] for s in h[1]): probs.append(f'No. {k}: a muted string struck')
print('\n'.join(probs) if probs else 'all good')
sys.exit(1 if probs else 0)
