"""Every song's singer track against its guitar-alone (or piano) track: the singer's track should hold the same take
(Misty on 16 Nov, My One and Only Love on 17 Nov held another take, so what he heard with the singer was not what the
diagrams show). python3 site_mix.py [Fret-Finder|Key-Finder] [slug]"""
import os, re, sys, json, subprocess
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
SP = '/tmp/claude-0/-home-claude/32eff81e-a259-5caa-a171-2530c104e7b0/scratchpad/'
SITE = SP + 'site/'


def wav(p):
    r = subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-ac', '1', '-ar', '11025', '-f', 'f32le', '-'], capture_output=True, check=True)
    return np.frombuffer(r.stdout, dtype=np.float32).astype(np.float64)


def pairs(site, d, html):
    """(plain track, locked track) pairs a page offers: each singer's track with the plain track it is built on"""
    srcs = re.findall(r'["\']([\w.() -]+\.mp3(?:\.locked)?)["\']', html)
    plain = [s for s in dict.fromkeys(srcs) if s.endswith('.mp3') and os.path.exists(d + s)]
    lk = [s for s in dict.fromkeys(srcs) if s.endswith('.mp3.locked') and os.path.exists(d + s)]
    base = plain
    if not base: return []
    pre = lambda a, b: len(os.path.commonprefix([a, b]))
    # each singer's track goes with the plain track whose name it shares most (jim-groove-voice with jim-groove-guitar)
    return [(max(base, key=lambda p: (pre(p, l), bool(re.search(r'guitar|piano', p)), -base.index(p))), l) for l in lk]


def label(html, f):
    m = re.search(r'data-src="' + re.escape(f) + r'"[^>]*>([^<]*)<', html) or re.search(r'\["([^"]*)", *"' + re.escape(f) + r'"\]', html)
    return m.group(1) if m else ''


out = []
sites = [a for a in sys.argv[1:2] if a in ('Fret-Finder', 'Key-Finder')] or ['Fret-Finder', 'Key-Finder']
only = sys.argv[2] if len(sys.argv) > 2 else None
for site in sites:
    root = SITE + site + '/songs/'
    for slug in sorted(os.listdir(root)):
        if only and slug != only: continue
        d = root + slug + '/'
        if not os.path.isfile(d + 'index.html'): continue
        html = open(d + 'index.html', encoding='utf-8').read()
        for p, l in pairs(site, d, html):
            if re.search(r'recording|real|tpt|tune', l) or re.search(r'the record\b', label(html, l), re.I): continue     # recordings and other parts are not a guitar mix
            tmp = SP + 'night/_mix.mp3'
            subprocess.run(['node', SP + 'unlock.mjs', d + l, tmp], check=True, capture_output=True)
            g = wav(d + p); m = wav(tmp); os.remove(tmp)
            n = min(len(g), len(m)); g, m = g[:n], m[:n]
            # a mix made by another tool can sit a few milliseconds late (Bach's "Both", 5 ms): line the two up first
            s0 = min(n // 3, 11025 * 20); seg = slice(s0, min(n, s0 + 11025 * 30))
            from scipy.signal import correlate
            x = correlate(m[seg], g[seg], mode='full', method='fft'); mid = len(g[seg]) - 1; w = 551
            lag = int(np.argmax(x[mid - w:mid + w + 1])) - w
            if lag > 0: m, g = m[lag:], g[:n - lag]
            elif lag < 0: m, g = m[:n + lag], g[-lag:]
            a = float(np.dot(m, g) / np.dot(g, g)); left = float(np.sqrt(np.mean((m - a * g) ** 2)) / np.sqrt(np.mean(m ** 2)))
            flag = '' if a > 0.3 else ('   <-- another take' if a < 0.15 else '   (the guitar is quiet in it)')
            out.append((site, slug, p, l, round(a, 3), round(left, 2)))
            print(f'{site:11s} {slug:34s} {l:28s} on {p:24s} x{a:.3f} left {left:.0%}{flag}', flush=True)
json.dump(out, open(SP + 'night/mix.json', 'w'), indent=1)
