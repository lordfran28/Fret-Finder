"""The 8-string version of a song page (songs/SLUG/eight.html).

The 8-string guitar here is tuned, low to high, A1 B1 E2 A2 D3 G3 B3 E4: the six strings as always and two basses
under them (the owner's choice, 22 November 2026). Strings keep their numbers: 1 is the high E, 6 the low E,
7 the B under it and 8 the A at the bottom. A song may retune the 7th or 8th string when that helps it a lot;
its page says so at the top.

    patch_kit(html)       the page's code made to draw any number of strings (DATA.song.tuning)
    to_eight(D, tuning)   the page's data with every grip widened to eight strings (the new basses left off)
    write(slug, D8, C8)   eight.html beside index.html, both pages linked to each other for assets/eight.js
"""
import re, json, os, sys

def _split(h):
    i = h.index('const DATA = ') + len('const DATA = ')
    D, end = json.JSONDecoder().raw_decode(h[i:])
    a = h.index('<script id="cp-data" type="application/json">') + len('<script id="cp-data" type="application/json">')
    b = h.index('</script>', a)
    return D, json.loads(h[a:b]), (i, i + end), (a, b)

def _put(h, D=None, C=None):
    _, Cold, (i, j), (a, b) = _split(h)
    cp = json.dumps(C if C is not None else Cold, ensure_ascii=False); assert '</' not in cp
    h = h[:a] + cp + h[b:]
    if D is not None:
        _, _, (i, j), _ = _split(h)
        dj = json.dumps(D, ensure_ascii=False); assert '</' not in dj
        h = h[:i] + dj + h[j:]
    return h

TUNING = [33, 35, 40, 45, 50, 55, 59, 64]      # A1 B1 E2 A2 D3 G3 B3 E4, low to high
SIX = [40, 45, 50, 55, 59, 64]

KIT = [   # (old, new, how many) inside the page's main script
    ("const OPEN = [40, 45, 50, 55, 59, 64];\n  const SN = ['E', 'A', 'D', 'G', 'B', 'e'];",
     "const OPEN = (DATA.song && DATA.song.tuning) || [40, 45, 50, 55, 59, 64]; const NSTR = OPEN.length;\n"
     "  const SN = OPEN.map((m, i) => i === OPEN.length - 1 ? 'e' : ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'][m % 12]);", 1),
    ("for (let i = 0; i < 6; i++)", "for (let i = 0; i < NSTR; i++)", 2),
    ("for (let r = 0; r < 6; r++)", "for (let r = 0; r < NSTR; r++)", 2),
    ("5 * SW", "(NSTR - 1) * SW", 8),
    ("['', '', '', '', '', '']", "Array(NSTR).fill('')", 3),
    ("[-1, -1, -1, -1, -1, -1]", "Array(NSTR).fill(-1)", 2),
    ("[-1, -1, -1].concat(tri)", "Array(NSTR - 3).fill(-1).concat(tri)", 1),
    ("[0, 1, 2, 3, 4, 5].map(i => ss.includes(6 - i)", "[...Array(NSTR).keys()].map(i => ss.includes(NSTR - i)", 1),
    ("ss: [6, 5, 4]", "ss: [NSTR, NSTR - 1, NSTR - 2]", 2),
    ("const s = 5 - r;", "const s = NSTR - 1 - r;", 1),
    ("col.trem !== undefined && 5 - r === col.trem) rows[r] += (col.c[5 - r] ? '-' + col.c[5 - r]",
     "col.trem !== undefined && NSTR - 1 - r === col.trem) rows[r] += (col.c[NSTR - 1 - r] ? '-' + col.c[NSTR - 1 - r]", 1),
    ("else rows[r] += ('-' + col.c[5 - r]).padEnd(w, '-');", "else rows[r] += ('-' + col.c[NSTR - 1 - r]).padEnd(w, '-');", 1),
]

def patch_kit(h):
    i = h.index("const OPEN = [40, 45, 50, 55, 59, 64];\n  const SN")
    j = h.index('</script>', i)
    body = h[i:j]
    for old, new, n in KIT:
        assert body.count(old) == n, (old, body.count(old))
        body = body.replace(old, new)
    body, k = re.subn(r'\b6 - (?=[a-z]\b|[a-z]\[|th\[|m\[)', 'NSTR - ', body)
    assert k >= 20, k
    assert not re.search(r'\b6 - [a-z]', body), re.findall(r'.{30}\b6 - [a-z].{20}', body)
    return h[:i] + body + h[j:]

def widen(f, n=8):
    return [-1] * (n - 6) + list(f)

def _is_frets(x):
    return isinstance(x, list) and len(x) == 6 and all(isinstance(v, int) and -2 <= v <= 24 for v in x)

def to_eight(D, tuning=TUNING):
    """every six-string grip in the data gets two muted low strings in front"""
    def walk(x):
        if isinstance(x, dict):
            return {k: (widen(v) if k in ('f', 'hold') and _is_frets(v) else walk(v)) for k, v in x.items()}
        if isinstance(x, list):
            if x and x[0] in ('K', 'C', 'T') and len(x) > 2 and _is_frets(x[2]):
                return [x[0], x[1], widen(x[2])] + [walk(v) for v in x[3:]]
            if all(_is_frets(v) or v == [] for v in x) and any(_is_frets(v) for v in x):   # a list of grips (fs)
                return [widen(v) if v else v for v in x]
            return [walk(v) for v in x]
        return x
    D8 = walk(json.loads(json.dumps(D)))
    D8['song'] = dict(D8['song'], tuning=list(tuning), strings=len(tuning))
    return D8

def note_name(m):
    return ['C', 'C♯', 'D', 'D♯', 'E', 'F', 'F♯', 'G', 'G♯', 'A', 'A♯', 'B'][m % 12] + str(m // 12 - 1)

TAG8 = '<script src="../../assets/eight.js"></script>'
def add_script(h):
    """assets/eight.js right after the page's metas (after voice.js and any ff-eight / ff-six / ff-locked-copy meta), before locked-page.js"""
    h = h.replace(TAG8, '')
    m = re.search(r'<script src="\.\./\.\./assets/voice\.js"></script>((?:<meta [^>]*>|<script>window\.FF_TUNING[^<]*</script>)*)', h)
    if not m: m = re.search(r'<meta charset=[^>]*>', h)
    if not m: raise ValueError('no place for assets/eight.js on this page')
    return h[:m.end()] + TAG8 + h[m.end():]

def write(slug, D8, C8=None, title_note=''):
    root = '/home/claude/fret-finder/songs/%s/' % slug
    h = open(root + 'index.html').read()
    # the six-string page names its 8-string version
    h6 = re.sub(r'<meta name="ff-eight"[^>]*>', '', h)
    h6 = h6.replace('<script src="../../assets/voice.js"></script>',
                    '<script src="../../assets/voice.js"></script><meta name="ff-eight" content="eight.html">', 1)
    h6 = add_script(h6)
    open(root + 'index.html', 'w').write(h6)
    # the 8-string page: its own data, the kit for eight strings, no locked copy of its own
    e = re.sub(r'<meta name="ff-eight"[^>]*>', '', h)
    e = re.sub(r'<meta name="ff-locked-copy"[^>]*>', '', e)
    e = e.replace('<script src="../../assets/voice.js"></script>',
                  '<script src="../../assets/voice.js"></script><meta name="ff-six" content="./">'
                  '<script>window.FF_TUNING = %s;</script>' % json.dumps(D8['song']['tuning']), 1)
    e = add_script(e)
    e = patch_kit(e)
    e = _put(e, D=D8, C=C8)
    e = re.sub(r'<title>(.*?)</title>', lambda m: '<title>%s · 8 strings</title>' % m.group(1).split(' · ')[0], e, 1)
    open(root + 'eight.html', 'w').write(e)
    return root + 'eight.html'
