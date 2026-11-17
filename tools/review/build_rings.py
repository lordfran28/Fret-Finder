"""python3 build_rings.py BUILD_DIR: runs a song build's note making (build_audio.py up to its render, nothing rendered)
and lists every note still sounding when its string is played again: two notes on one string at once, which a guitar
can't do (Crush and I'll Be Seeing You, 17 Nov). The kit's render_guitar now stops such notes itself; this finds the
tracks made before that. Needs the build folder and the kit in /home/claude."""
import sys, os, io, contextlib
d = sys.argv[1]; src = open(d + '/build_audio.py').read()
cut = src.find("if 'render' not in sys.argv")
if cut < 0: cut = src.find("if mode != 'render'")
code = src[:cut]
sys.argv = [d + '/build_audio.py']; os.chdir(d); sys.path.insert(0, d); sys.path.insert(0, '/home/claude/kit')
ns = {'__name__': '__main__', '__file__': d + '/build_audio.py'}
with contextlib.redirect_stdout(io.StringIO()): exec(compile(code, 'build', 'exec'), ns)
notes = ns['notes']
same = []; last = {}
for e in sorted(notes, key=lambda e: e['t']):
    s = e.get('string')
    p = last.get(s)
    if p is not None and p['off'] > e['t'] + 0.03 and not (p['midi'] == e['midi']):
        same.append((round(p['t'], 2), p['midi'], e['midi'], s, round(p['off'] - e['t'], 2)))
    last[s] = e
NM = ['C','D♭','D','E♭','E','F','G♭','G','A♭','A','B♭','B']
nn = lambda m: f'{NM[m % 12]}{m // 12 - 1}'
print(d.split('/')[-1], 'notes', len(notes), '| two notes on one string at once:', len(same), '| total overlap', round(sum(x[4] for x in same), 1), 's')
half = [x for x in same if abs(x[1] - x[2]) in (1, 2)]
print('   of which a half or whole step apart:', len(half))
for x in sorted(same, key=lambda x: -x[4])[:8]: print(f'   t={x[0]} string {x[3]}: {nn(x[1])} still ringing {x[4]}s over {nn(x[2])}')
