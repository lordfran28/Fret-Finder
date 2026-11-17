"""Turn a Mutopia score into Exercises-page bars: every bar in playing order, one 'P' item per bar holding the
notes struck at each onset with the string and fret our fingering gives them."""
import sys
from fractions import Fraction as Fr
sys.path.insert(0, '/home/claude/studies/classical'); sys.path.insert(0, '/home/claude/studies')
import lyparse as L, finger as F

NM = ['C', 'C♯', 'D', 'E♭', 'E', 'F', 'F♯', 'G', 'A♭', 'A', 'B♭', 'B']


def where(frets):
    fr = [f for f in frets if f > 0]
    if not fr or max(fr) <= 4: return '@first position'
    lo = min(fr)
    return f'@from the {lo}{"st" if lo == 1 else "nd" if lo == 2 else "rd" if lo == 3 else "th"} fret'


def piece_bars(path, prefix, tuning=F.STD, fixes=(), maxf=12, shift=0):
    """fixes: (onset in beats, wrong midi, right midi) for misprints in the source, each with its reason on the page"""
    P = L.parse(path)
    n, d = P['time']; bl = Fr(n, d) * 4                     # bar length in quarter beats
    part = P['partial'] * 4
    raw = [(t * 4, du * 4, m + shift) for t, du, m, v in P['notes']]          # shift: -12 where the source writes guitar music an octave up without treble_8
    for ft, wrong, right in fixes:
        hit = [k for k, (t, du, m) in enumerate(raw) if t == ft and m == wrong]
        assert hit, ('fix not found', prefix, ft, wrong)
        for k in hit: raw[k] = (raw[k][0], raw[k][1], right)
    notes = F.dedupe(raw)
    pl = F.finger(notes, tuning, maxf=maxf)
    total = P['length'] * 4
    # bar starts: a pickup bar first if there is one
    starts = ([Fr(0)] if part else []) + [part + k * bl for k in range(int((total - part) / bl + Fr(999, 1000)))]
    if starts and starts[-1] >= total: starts.pop()
    bars = []
    for bi, b0 in enumerate(starts):
        b1 = starts[bi + 1] if bi + 1 < len(starts) else max(total, b0 + (part if (part and bi == 0) else bl))
        if part and bi == 0: b1 = part
        idx = [i for i, (t, du, m) in enumerate(notes) if b0 <= t < b1]
        onsets = sorted({notes[i][0] for i in idx})
        groups, durs = [], []
        for k, t in enumerate(onsets):
            g = sorted(([pl[i][0], pl[i][1]] for i in idx if notes[i][0] == t), key=lambda x: -x[0])
            nxt = onsets[k + 1] if k + 1 < len(onsets) else b1
            if k == 0 and t > b0:                                  # the bar starts with a rest
                groups.append([]); durs.append(float(t - b0))
            groups.append(g); durs.append(float(nxt - t))
        label = f'{prefix}.{bi + (0 if part else 1)}'
        if not groups:
            items = [['W', float(b1 - b0)]]
        else:
            # a rest at the start: a W item, then the P item
            items = []
            if groups and groups[0] == []:
                items.append(['W', durs[0]]); groups, durs = groups[1:], durs[1:]
            items.append(['P', groups, durs, where([f for g in groups for s, f in g])])
        bars.append(dict(label=label, beats=float(b1 - b0), items=items, chords=[], n=bi + (0 if part else 1)))
    wide = []
    for i, (t, du, m) in enumerate(notes):
        pass
    return bars, P


def wide_stretches(bars):
    """bars where the frets held at one moment span five below the 7th fret"""
    out = []
    for B in bars:
        for it in B['items']:
            if it[0] != 'P': continue
            for g in it[1]:
                fr = [f for s, f in g if f > 0]
                if fr and max(fr) - min(fr) + 1 > (5 if min(fr) >= 7 else 4): out.append(B['label'])
    return sorted(set(out))
