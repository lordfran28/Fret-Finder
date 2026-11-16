"""Checks on the transcription: every bar 3 beats (the pickup 1), ties land on the same note, every note and chord moved
from G to E♭ by the same interval (a major 3rd down: two letters, four semitones), the chords as printed."""
import sys
sys.path.insert(0, '/home/claude/studies/tango')
import tune_iw as T, mel as M
bad = []
for body in (T.TUNE_G, T.TUNE_G[:30] + T.SECOND):
    for i, (b, chs, notes, w) in enumerate(body):
        L = sum(d for n, d in notes)
        if L != (1 if b == 0 else 3): bad.append(f'bar {b}: {L} beats')
        for c, at in chs:
            M.chord_parse(c if c != 'A' else 'A')
            if not 0 <= at < 3: bad.append(f'bar {b}: chord at {at}')
        if notes[-1][0].endswith('~'):
            nxt = body[i + 1][2][0][0].rstrip('~')
            if nxt != notes[-1][0].rstrip('~'): bad.append(f'bar {b}: tie to {nxt}')
for ending in (1, 2):
    g = T.TUNE_G[:30] + (T.TUNE_G[30:] if ending == 1 else T.SECOND)
    e = T.in_eb(ending)
    for (b, cg, ng, w), (b2, ce, ne, w2) in zip(g, e):
        for (a, _), (x, _) in zip(ng, ne):
            if a == 'r': assert x == 'r'; continue
            a, x = a.rstrip('~'), x.rstrip('~')
            if M.midi(a) - M.midi(x) != 4: bad.append(f'bar {b}: {a}->{x} semitones')
            la, lx = M.parse(a), M.parse(x)
            if (la[0] + 7 * la[2]) - (lx[0] + 7 * lx[2]) != 2: bad.append(f'bar {b}: {a}->{x} letters')
        for (c, _), (y, _) in zip(cg, ce):
            if (M.midi(M.chord_parse(c)[0] + '4') - M.midi(M.chord_parse(y)[0] + '4')) % 12 != 4: bad.append(f'bar {b}: {c}->{y}')
# the printed chords, bar by bar (G), as read from the score's diagrams
PRINTED = 'G G G G G B C E7 Am E7 A7 A7 A7 A7 D7 D7 G G G G G B C E7 Am Am/A G E7 Am D7 G D7'.split()
got = ['/'.join(c for c, _ in chs) for b, chs, n, w in T.TUNE_G[1:]]
if got != PRINTED: bad.append(f'chords {got}')
print('\n'.join(bad) if bad else 'tune: all bars 3 beats, ties hold, every note and chord a major 3rd down, chords as printed')
