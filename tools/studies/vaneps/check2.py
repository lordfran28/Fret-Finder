"""Checks for entry2 (Van Eps, open triads, arpeggios, contrary motion): every triad has the chord's notes in the voice
order of its mechanism, the lines follow the scale, consecutive triads in contrary motion share no string, every grip
is under the hand."""
import sys
sys.path.insert(0, '/home/claude/studies'); sys.path.insert(0, '/home/claude/studies/tango'); sys.path.insert(0, '/home/claude/studies/vaneps')
import entry2 as E
probs = []
PCS = {}
for key, sc, names in (('EB', E.EB, E.EB_N), ('CH', E.CH, E.CH_N)):
    for d, n in enumerate(names): PCS[(key, n)] = (sc[d], sc[(d + 2) % 7], sc[(d + 4) % 7], sc, d)
def scale_key(ex, nm):
    if ex == 'open1-h': return 'CH'
    if ex == 'arpeggios' and nm in ('Cm', 'Fm'): return 'CH'
    return 'EB'
ROLE = {'open1': (1, 2, 0), 'open2': (0, 2, 1), 'openR': (0, 1, 2), 'first': (1, 2, 0)}
seqs = {}
for ex, nm, kind, ms, ss in E.CHECK:
    if ex in ('arp-order', 'contrary-lines'): continue
    r, t, f, sc, d = PCS[(scale_key(ex, nm), nm)]
    pcs = (r, t, f)
    if sorted(m % 12 for m in ms) != sorted(pcs): probs.append(f'{ex}: {nm} {ms} is not the chord'); continue
    if kind in ROLE:
        want = [pcs[i] for i in ROLE[kind]]
        if [m % 12 for m in ms] != want: probs.append(f'{ex}: {nm} voices in the wrong order')
        a, b, c = ms
        if kind == 'open1' and not (12 < b - a < 24 and 0 < c - b < 12): probs.append(f'{ex}: {nm} not 10th + 4th')
        if kind == 'open2' and not (0 < b - a < 12 and 0 < c - b < 12 and c - a > 12): probs.append(f'{ex}: {nm} not 5th + 6th')
        if kind == 'openR' and not (12 < b - a < 24 and 0 < c - b < 12): probs.append(f'{ex}: {nm} not 10th + 3rd')
        if kind == 'first' and not (c - a < 12): probs.append(f'{ex}: {nm} not close')
    if kind == 'arp' and max(ms) - min(ms) >= 12: probs.append(f'{ex}: {nm} not a close triad')
    seqs.setdefault(ex, []).append((nm, ss, d, ms))
# the scale lines go up the scale a step at a time, then back
for ex, L in seqs.items():
    if ex in ('open1', 'open1-h', 'open2', 'openR'):
        ds = [d for nm, ss, d, ms in L]
        half = (len(ds) + 1) // 2
        for a, b in zip(ds[:half], ds[1:half]):
            if (b - a) % 7 != 1: probs.append(f'{ex}: {a}→{b} is not the next triad of the scale')
        lows = [ms[0] for nm, ss, d, ms in L[:half]]
        if lows != sorted(lows): probs.append(f'{ex}: the line does not climb')
    if ex == 'contrary':
        for (n1, s1, d1, m1), (n2, s2, d2, m2) in zip(L, L[1:]):
            if set(s1) & set(s2): probs.append(f'contrary: {n1} and {n2} share a string')
        up = [d for nm, ss, d, ms in L[0::2]]; dn = [d for nm, ss, d, ms in L[1::2]]
        if any((b - a) % 7 != 1 for a, b in zip(up, up[1:])) or any((a - b) % 7 != 1 for a, b in zip(dn, dn[1:])): probs.append('contrary: the lines do not move by step')
for ex, nm, way, vs, _ in E.CHECK:
    if ex == 'arp-order':
        lows = [v[0] for v in vs]
        if lows != sorted(lows): probs.append(f'arpeggio {nm}: inversions out of order')
n = 0
for S in E.SECTIONS[1:]:
    for e in S['ex']:
        for j, b in enumerate(e['bars']):
            n += 1
            for it in b['items']:
                if it[0] == 'C':
                    fr = [x for x in it[2] if x > 0]
                    if max(fr) - min(fr) > (4 if min(fr) >= 7 else 3): probs.append(f'{e["id"]} bar {j + 1}: stretch {it[2]}')
            if abs(sum(it[3] if it[0] == 'C' else it[1] for it in b['items']) - 4) > 1e-9: probs.append(f'{e["id"]} bar {j + 1}: beats')
print('triads checked:', len(E.CHECK), ' bars:', n)
print('\n'.join(probs) if probs else 'all good')
sys.exit(1 if probs else 0)
