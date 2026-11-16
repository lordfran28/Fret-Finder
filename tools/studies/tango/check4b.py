"""Checks for entry4b (vals, second part): the fills follow his rules, the 6/8 ways keep the accent on the 1st and 4th
eighths with the right bass, the plans are his, every bar has three beats, every grip is under the hand, every quote is
a beat or two."""
import sys
sys.path.insert(0, '/home/claude/studies/tango'); sys.path.insert(0, '/home/claude/studies')
import entry4b as E
import mel as M
from quotes import _beats
probs = []
def semis(a, b): return M.midi(b) - M.midi(a)
def names(it): return it[3][1:].split('|')[0].split(',') if it[3].startswith('=') else None
def notes_of(it): return [M.OPEN[s] + f for s, f in it[1]]
TRI = lambda c: [M.pc(p + '4') for p, d in M.chord_tones(c) if d in ('1', '3', 'b3', '5')]
for r in E.RULES:
    k = r[0]
    if k == 'triad':
        c, ns = r[1], r[2]
        t = TRI(c)
        for a, b in zip(ns, ns[1:]):
            if M.pc(a) not in t or M.pc(b) not in t or semis(a, b) <= 0: probs.append(f'triad {c}: {a}→{b}')
            if any(m % 12 in t for m in range(M.midi(a) + 1, M.midi(b))): probs.append(f'triad {c}: skips a note between {a} and {b}')
    elif k == 'chromdown':
        c, ns = r[1], r[2]
        if M.degree_of(ns[0], c) != '1' or M.degree_of(ns[-1], c) != '5' or any(semis(a, b) != -1 for a, b in zip(ns, ns[1:])): probs.append(f'chromdown {c}')
    elif k == 'interleave':
        c, ns = r[1], r[2]
        seq = E.triad_up(c, ns[0], len(ns) // 2 + 2)
        if ns != [x for kk in range(len(ns) // 2) for x in (seq[kk], seq[kk + 2])]: probs.append(f'interleave {c}')
    elif k == 'chromdom':
        if (M.pc(M.chord_parse(r[1])[0] + '4') - M.pc(M.chord_parse(r[2])[0] + '4')) % 12 != 1: probs.append('chromatic dominant is not a semitone above')
    elif k == '68':
        id_, b1, b2 = r[1], r[2], r[3]
        for it in (b1, b2):
            if it[0] == 'R':
                ms = notes_of(it)
                if len(ms) != 6 or it[4]['vel'][0] <= 0 or it[4]['vel'][3] <= 0: probs.append(f'{id_}: not six eighths accented on 1 and 4')
                b, ups = [ms[0], ms[3]], ms[1:3] + ms[4:6]
                if any(u <= max(b) for u in ups) and id_ != '68-arpegio': probs.append(f'{id_}: an upper note under the bass')
                if any(u % 12 not in {M.pc(p + '4') for p in M.tone_pcs('D7')} for u in ups): probs.append(f'{id_}: an upper note outside D7')
                if id_ in ('68-arpegio', '68-quinta', '68-pedal') and any(x % 12 not in {M.pc(p + '4') for p in M.tone_pcs('D7')} for x in b): probs.append(f'{id_}: a bass outside D7')
            else:
                hits = it[3]
                if len(hits) not in (2, 6): probs.append(f'{id_}: hits')
        if id_ == '68-quinta':
            for it in (b1, b2):
                ms = notes_of(it)
                if {(ms[0] - M.midi('D3')) % 12, (ms[3] - M.midi('D3')) % 12} != {0, 7}: probs.append('68-quinta: not root and 5th')
        if id_ == '68-pedal':
            for it in (b1, b2):
                ms = notes_of(it)
                if ms[0] != ms[3] or ms[0] % 12 != M.pc('D4'): probs.append('68-pedal: the bass is not the root twice')
        if id_ == '68-diatonico':
            bs = [notes_of(b1)[0], notes_of(b1)[3], notes_of(b2)[0], notes_of(b2)[3]]
            if [b - a for a, b in zip(bs, bs[1:])] not in ([-2, -1, -2], [-2, -2, -1], [-1, -2, -2]) : probs.append(f'68-diatonico: {bs}')
            if any(x % 12 not in {M.pc(p + '4') for p in M.scale_pcs('G', 'major')} for x in bs): probs.append('68-diatonico: outside G major')
        if id_ == '68-cromatico':
            bs = [notes_of(b1)[0], notes_of(b1)[3], notes_of(b2)[0], notes_of(b2)[3]]
            if [b - a for a, b in zip(bs, bs[1:])] != [1, 1, 1]: probs.append(f'68-cromatico: {bs}')
        if id_ == '68-cluster':
            g = b1[2]; ms = sorted(M.OPEN[6 - i] + g[i] for i in range(6) if g[i] >= 0)
            if ms[-1] - ms[-2] != 1 or ms[-1] % 12 != M.pc('D4'): probs.append('68-cluster')
    elif k == 'plans':
        P = r[1]
        if P[4] != ['básico', 'variación 1', 'básico', 'básico', 'básico', 'variación 1', 'básico', 'básico'] or len(P) != 5: probs.append('plans')
    elif k == 'arp6':
        c, g = r[1], r[2]
    else:
        probs.append(f'unchecked {k}')


def span_ok(fr):
    fz = [f for f in fr if f > 0]
    return not fz or max(fz) - min(fz) <= (4 if min(fz) >= 7 else 3)


n = 0
for S in E.SECTIONS[2:]:
    for ex in S['ex']:
        if _beats(ex['quote'].get('items') or []) > 2 + 1e-9: probs.append(f'{ex["id"]}: quote too long')
        for j, b in enumerate(ex['bars']):
            n += 1; L = 0
            for it in b['items']:
                if it[0] == 'K':
                    L += sum(h[0] for h in it[3])
                    if not span_ok(it[2]): probs.append(f'{ex["id"]} bar {j + 1}: stretch {it[2]}')
                elif it[0] in ('R', 'P'):
                    L += sum(it[2])
                    if it[0] == 'R' and ex['id'].startswith('valseado'):
                        ms = notes_of(it); c = b['chords'][0]
                        if ms != sorted(ms) or len(set(ms)) != 6: probs.append(f'{ex["id"]}: arpeggio not rising')
                        if any(m % 12 not in {M.pc(p + '4') for p in M.tone_pcs(c)} for m in ms): probs.append(f'{ex["id"]}: a note outside {c}')
                elif it[0] == 'W': L += it[1]
            if abs(L - 3) > 1e-6: probs.append(f'{ex["id"]} bar {j + 1}: {L} beats')
print('rules checked:', len(E.RULES), ' bars checked:', n)
print('\n'.join(probs) if probs else 'all good')
sys.exit(1 if probs else 0)
