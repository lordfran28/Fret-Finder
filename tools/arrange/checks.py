"""Checks for a hand-made arrangement page (see ARRANGING.md).

    from checks import report
    report(bars, record_notes, voice)   # bars: the page's track bars; record_notes: [[start, end, midi, amp], ...]
                                        # voice: (times, midi, prob) arrays of the record's voice
Prints: unplayable grips, struck strings missing from their grip, the diagram count, the top note and the
bass of every strike next to the tune and the record, the rubs against the voice an octave down, and how
the guitar's strikes line up with the record's.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'tools'))
import numpy as np
from solver import playable, nm, OPEN
def pick(f, m):
    idx = [j for j, x in enumerate(f) if x >= 0]
    if isinstance(m, list): return [6 - s for s in m]
    return {'a': idx, 'b': idx[:1], 't': idx[1:], 'h': idx[-3:], '-': []}.get(m, [])
def beat_time(bt, x):
    k = max(0, min(int(x), len(bt) - 2)); return bt[k] + (x - k) * (bt[k + 1] - bt[k])
def events(bars):
    """the notes as the page plays and lights them: dict(t, s, f, m, bar, kind)"""
    out = []
    for b in bars:
        x = 0.0; bt = b['bt']; pend = None
        for it in b['items']:
            k = it[0]
            if k == 'X': pend = it[1]; continue
            if k == 'W':
                for s, fr in (pend or []): out.append(dict(t=beat_time(bt, x), s=s, f=fr, m=OPEN[6 - s] + fr, bar=b['label'], kind='bass'))
                pend = None; x += it[1]; continue
            if k == 'K':
                for d, m in it[3]:
                    for j in pick(it[2], m):
                        if it[2][j] >= 0: out.append(dict(t=beat_time(bt, x), s=6 - j, f=it[2][j], m=OPEN[j] + it[2][j], bar=b['label'], kind='chord'))
                    x += d
                continue
            if k == 'R':
                for n, ((s, fr), d) in enumerate(zip(it[1], it[2])):
                    if n == 0 and pend:
                        for s2, f2 in pend: out.append(dict(t=beat_time(bt, x), s=s2, f=f2, m=OPEN[6 - s2] + f2, bar=b['label'], kind='bass'))
                        pend = None
                    out.append(dict(t=beat_time(bt, x), s=s, f=fr, m=OPEN[6 - s] + fr, bar=b['label'], kind='run')); x += d
                continue
    return out
def report(bars, record_notes, voice, amin=0.3, tol=0.1):
    VT, VM, VP = voice
    def sung(a, b):
        k = (VT >= a) & (VT < b) & (VP > 0.45) & ~np.isnan(VM)
        return int(round(np.median(VM[k]))) if k.sum() > 3 else None
    grips = [(b['label'], it[1], it[2]) for b in bars for it in b['items'] if it[0] == 'K']
    for lab, n, f in grips:
        if not playable(f): print('UNPLAYABLE', lab, n, f)
    for b in bars:
        for it in b['items']:
            if it[0] == 'K':
                for d, m in it[3]:
                    if isinstance(m, list):
                        for s in m:
                            if it[2][6 - s] < 0: print('STRING NOT IN GRIP', b['label'], it[1], s)
    print('diagrams:', sum(1 for b in bars for it in b['items'] if it[0] in 'KRP'))
    ev = events(bars)
    by = {}
    for e in ev: by.setdefault(round(e['t'], 3), []).append(e)
    print('strike     bar  bass  top   tune  record low/high')
    for t, es in sorted(by.items()):
        lo = min(es, key=lambda e: e['m']); hi = max(es, key=lambda e: e['m'])
        rec = [n for n in record_notes if n[3] >= amin and abs(n[0] - t) < 0.12]
        v = sung(t, t + 0.4)
        print(f"{t:7.2f}  {es[0]['bar']:>4}  {nm(lo['m']):5} {nm(hi['m']):5} {nm(v) if v else '-':5} {nm(min(r[2] for r in rec)) + '/' + nm(max(r[2] for r in rec)) if rec else '-'}")
    rubs = []
    for e in ev:
        v = sung(e['t'], e['t'] + 0.35)
        if v is not None and abs(e['m'] - (v - 12)) in (1, 11, 13): rubs.append((e['bar'], round(e['t'], 2), nm(e['m']), 'he sings ' + nm(v - 12)))
    print('rubs against his voice:', rubs)
    go = []
    for t in sorted(set(round(e['t'], 2) for e in ev)):
        if not go or t - go[-1] > 0.09: go.append(t)
    t1 = max(go) + 1
    po = []
    for n in sorted(record_notes):
        if n[3] >= amin and n[0] < t1 and (not po or n[0] - po[-1] > 0.09): po.append(n[0])
    if po and go:
        c1 = np.mean([min(abs(x - y) for y in po) <= tol for x in go]); c2 = np.mean([min(abs(x - y) for y in go) <= tol for x in po])
        print(f'guitar strikes on a record strike: {c1:.0%}; record strikes the guitar plays: {c2:.0%}')
        print('record strikes left out:', [round(x, 2) for x in po if min(abs(x - y) for y in go) > tol])
