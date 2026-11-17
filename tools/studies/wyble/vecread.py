"""Read Concepts for the Classical and Jazz Guitar (vector music, Anastasia font) note by note: python3 vecread.py PAGE
Every notehead's pitch from its height on the staff (bottom line = E4 written; the guitar sounds an octave lower),
accidentals carried through the bar, onsets grouped by x, bars split at barlines. Prints written pitches."""
import sys, glob, pdfplumber
F = glob.glob('/mnt/user-data/attachments/*/5f5b3612*')[0]
HEADS = set('ˆœ˙w')
LET = 'CDEFGAB'


def read(page_no):
    pg = pdfplumber.open(F).pages[page_no - 1]
    ch = [c for c in pg.chars if 'Anastasia' in c['fontname']]
    clefs = sorted([c for c in ch if c['text'] == '&'], key=lambda c: -c['y0'])
    systems = []
    for k, cl in enumerate(clefs):
        base = cl['y0']; half = cl['size'] / 8
        lo = base - 40; hi = base + 52
        heads = [c for c in ch if c['text'] in HEADS and lo < c['y0'] < hi]
        accs = [c for c in ch if c['text'] in '#bn' and lo < c['y0'] < hi and c['x0'] > cl['x0'] + 20]
        bars = sorted(c['x0'] for c in ch if c['text'] == 'l' and abs(c['y0'] - base) < 2)
        notes = []
        for h in heads:
            step = round((h['y0'] - base) / half)          # 0 = E4
            idx = 2 + step                                   # C=0 ... E4 at index 2 of octave 4
            octave = 4 + idx // 7; letter = LET[idx % 7]
            notes.append(dict(x=h['x0'], step=step, name=f'{letter}{octave}', glyph=h['text'], y=h['y0']))
        # accidentals: the nearest to the left at the same height, within 14 pt
        for a in accs:
            st = round((a['y0'] - base) / half)
            cand = [n for n in notes if n['step'] == st and 0 < n['x'] - a['x0'] < 16]
            if cand:
                n = min(cand, key=lambda n: n['x'] - a['x0']); n['acc'] = {'#': '♯', 'b': '♭', 'n': '♮'}[a['text']]
        systems.append(dict(base=base, bars=bars, notes=sorted(notes, key=lambda n: (n['x'], n['step']))))
    return systems


def spell(systems):
    """accidentals hold to the end of the bar (same letter and octave)"""
    out = []
    for S in systems:
        bars = [b for b in S['bars']] + [1e9]
        cur, b0, row, bar = {}, -1, [], []
        for n in S['notes']:
            bi = next(i for i, b in enumerate(bars) if n['x'] < b)
            if bi != b0:
                if bar: row.append(bar)
                bar, cur, b0 = [], {}, bi
            key = n['name']
            if 'acc' in n: cur[key] = n['acc']
            acc = cur.get(key, '')
            if acc == '♮': acc = ''
            if bar and abs(bar[-1][0] - n['x']) < 3: bar[-1][1].append(n['name'][0] + acc + n['name'][1:])
            else: bar.append([n['x'], [n['name'][0] + acc + n['name'][1:]]])
        if bar: row.append(bar)
        out.append(row)
    return out


if __name__ == '__main__':
    p = int(sys.argv[1])
    for si, row in enumerate(spell(read(p))):
        print(f'-- system {si + 1}')
        for bi, bar in enumerate(row):
            print(f'  bar {bi + 1}: ' + ' | '.join('+'.join(sorted(ns, key=lambda s: s[-1] + s[0])) for x, ns in bar))
