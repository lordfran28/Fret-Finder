"""Where the songs are instrumental (no voice for two bars or more), and how the guitar fills it:
bass on beats 1 and 3, attacks a beat, and bars that only hold a chord. The owner (17 Nov): instrumentals must
always carry a bass line and never be stiff or empty."""
import re, json, sys, os
ROOT = '/home/claude/fret-finder/songs/'


def hits(it):
    """[(beat offset, strings struck)] for one item; strings 1..6 from the high E"""
    k = it[0]
    out = []
    if k == 'K':
        g = it[2]; idx = [6 - i for i, f in enumerate(g) if f >= 0]
        x = 0.0
        for h in it[3]:
            sel = h[1] if isinstance(h[1], list) else {'a': idx, 'b': idx[:1], 't': idx[1:]}.get(h[1], idx)
            out.append((x, list(sel))); x += h[0]
    elif k == 'C':
        g = it[2]; out.append((0.0, [6 - i for i, f in enumerate(g) if f >= 0]))
    elif k == 'R':
        x = 0.0
        for (s, f), d in zip(it[1], it[2]):
            out.append((x, [s])); x += d
    elif k == 'T':                       # tremolo: the thumb's notes spread over the item, the tremolo above
        th = (it[4] or {}).get('thumb') or [[6 - next(i for i, f in enumerate(it[2]) if f >= 0), 0]]
        d = it[3] / len(th)
        for j, (s, f) in enumerate(th):
            out.append((j * d, [s])); out.append((j * d + d / 2, [1]))
    elif k == 'X':                       # a bass note laid under what follows (it takes no time of its own)
        out.append((0.0, [s for s, f in it[1]]))
    elif k == 'P':                       # a line in pairs (octaves, sixths)
        x = 0.0
        for pr, d in zip(it[1], it[2]):
            out.append((x, [s for s, f in pr])); x += d
    elif k == 'Y':                       # half triads
        x = 0.0
        for tri, d in zip(it[2], it[3]):
            out.append((x, [4, 3, 2])); x += d
    return out


def beats(it):
    k = it[0]
    if k == 'K': return sum(h[0] for h in it[3])
    if k in ('C', 'T'): return it[3]
    if k == 'R': return sum(it[2])
    if k == 'W': return it[1]
    if k == 'P': return sum(it[2])
    if k == 'Y': return sum(it[3])
    return 0


def scan(slug):
    h = open(ROOT + slug + '/index.html', encoding='utf-8').read()
    m = re.search(r'const DATA = (\{.*?\});\n', h, re.S)
    if not m: return None
    D = json.loads(m.group(1)); rep = []
    for tr in D['tracks']:
        bars = tr['bars']
        quiet = [i for i, b in enumerate(bars) if b.get('voc') is not None and '█' not in b.get('voc', '')]
        runs = []
        for i in quiet:
            if runs and runs[-1][-1] == i - 1: runs[-1].append(i)
            else: runs.append([i])
        for r in runs:
            if len(r) < 2: continue
            nobass, held, att, static = [], [], [], []
            for i in r:
                b = bars[i]; x = 0.0; ev = []
                for it in b['items']:
                    for o, ss in hits(it): ev.append((x + o, ss))
                    x += beats(it)
                nb = x or 4
                low = [o for o, ss in ev if max(ss) >= 4]           # a note on the D, A or low E string
                if not any(o < 0.25 for o in low) or (nb >= 4 and not any(abs(o - 2) < 0.3 for o in low)):
                    nobass.append(b['label'])
                if len(ev) <= 1: held.append(b['label'])
                if len(low) <= 1 and nb >= 3: static.append(b['label'])
                att.append(len(ev) / nb)
            rep.append(dict(track=tr['key'], bars=f"{bars[r[0]]['label']}–{bars[r[-1]]['label']}", n=len(r), sec=bars[r[0]].get('sec'),
                            nobass=nobass, held=held, static=static, att=round(sum(att) / len(att), 2)))
    return rep


if __name__ == '__main__':
    slugs = sys.argv[1:] or sorted(d for d in os.listdir(ROOT) if os.path.isdir(ROOT + d))
    for s in slugs:
        try: rep = scan(s)
        except Exception as e: print(s, 'ERR', e); continue
        if rep is None: print(f'{s}: older page, not read'); continue
        for r in rep:
            flag = ('NO BASS in %d of %d bars' % (len(r['nobass']), r['n']) if r['nobass'] else '') + ('; held only: ' + ','.join(r['held']) if r['held'] else '') + ('; one bass note a bar in %d' % len(r['static']) if r['static'] else '')
            print(f"{s:34s} {r['track']:5s} {r['bars']:>12s} ({r['n']:2d} bars, {r['sec']}) {r['att']:.2f}/beat {flag}")
