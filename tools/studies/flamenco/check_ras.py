"""Independent checks for rasgueado.py: the strokes of every bar against Serrano's bars as transcribed here from his
pages 23–26 (finger, direction and length of each stroke), the chords against your Очи чёрные page, every grip
against its chord name, every strum across exactly the strings the grip sounds, and the upstrokes marked for the sound."""
import sys, re, json
sys.path.insert(0, '/home/claude/studies'); sys.path.insert(0, '/home/claude/studies/flamenco'); sys.path.insert(0, '/home/claude/scripts')
import rasgueado as R
import gtr

probs = []
def P(m): probs.append(m)

# Serrano's bars (pp. 23–26), as read: a stroke is finger+direction (D down, U up) and its length in beats; '-' a rest; '.' an unlettered downstroke
def S(txt):
    out = []
    for tok in txt.split():
        f, l = tok.split('/', 1)
        out.append((f, float(eval(l))))
    return out
ISAM = 'iD/1/4 sD/1/4 aD/1/4 mD/1/4'
BARS = {
    'prep': S('iD/1 sD/1 aD/1 mD/1'),
    'ex1': S(f'{ISAM} iD/1 -/1'),
    'ex2': S(f'{ISAM} {ISAM} iD/1 -/1'),
    'ex3a': S(f'{ISAM} {ISAM} {ISAM}'), 'ex3b': S('iD/1 -/2'),
    'st1': S(f'{ISAM} iD/1 ./1'), 'st1x': S('./1 -/2'),
    'st2a': S(f'{ISAM} {ISAM} iD/1'), 'st2b': S('./1 ./1 ./1'),
    'st3a': S(f'{ISAM} {ISAM} iD/1/2 iU/1/2'), 'st3b': S('iD/1/2 iU/1/2 iD/1/2 iU/1/2 iD/1/2 iU/1/2'),
    'st4a': S(f'{ISAM} {ISAM} {ISAM}'), 'st4b': S('iD/1/2 iU/1/2 iD/1/2 iU/1/2 iD/1/2 iU/1/2'),
    'st5': S(f'{ISAM} {ISAM} iD/1/2 iU/1/2'), 'st5e': S(f'{ISAM} {ISAM} {ISAM}'),
    'end': S('./1 -/2'), 'endi': S('iD/1 -/2'), 'endi4': S('iD/1 -/3'),
}
# which of his bars each of our bars uses, in order (k = bar index within the song's 16)
def four(a, b, c):   # his four-bar shape: a, b, a, c
    return [a, b, a, c]
PLAN = {
    'prep': ['prep'] * 8 + ['endi4'],
    'ex1': ['ex1'] * 8, 'ex2': ['ex2'] * 8,
    'ex3': ['ex3a', 'ex3b'] * 8,
    'st1': ['st1', 'st1', 'st1', 'st1x'] * 4,
    'st2': four('st2a', 'st2b', 'st2b') * 4 + ['end'],
    'st3': four('st3a', 'st3b', 'st3b') * 4 + ['end'],
    'st4': four('st4a', 'st4b', 'st4b') * 4 + ['end'],
    'st5': ['st5'] * 6 + ['st5e', 'endi'],
}

# the song: your Очи чёрные page, its plain chart
h = open('/home/claude/fret-finder/songs/ochi-chyornye/index.html').read()
m = re.search(r'"title": "The plain chart".*?"chords": (\[\[.*?\]\]), "tab"', h, flags=re.S)
chart = [b[0]['c'] for b in json.loads(m.group(1))]
changes = chart[0::2]
SONG = {'prep': changes + ['Am'], 'ex1': chart[:8], 'ex2': changes, 'ex3': chart, 'st1': chart,
        'st2': chart + ['Am'], 'st3': chart + ['Am'], 'st4': chart + ['Am'], 'st5': changes}

OPENS = [40, 45, 50, 55, 59, 64]
EXS = {ex['id']: ex for S_ in R.SECTIONS for ex in S_['ex']}
if set(EXS) != set(PLAN): P(f'exercises {sorted(EXS)}')
for exid, plan in PLAN.items():
    ex = EXS.get(exid)
    if not ex: continue
    if len(ex['bars']) != len(plan): P(f'{exid}: {len(ex["bars"])} bars, wants {len(plan)}'); continue
    for k, (B, want) in enumerate(zip(ex['bars'], plan)):
        want = want.rstrip('*')
        strokes, chords = [], []
        for it in B['items']:
            name, g, hits = it[1], it[2], it[3]
            ups = it[4]['up'] if len(it) > 4 else []
            marks = it[4].get('marks') if len(it) > 4 else None
            if marks is None or len(marks) != len(hits): P(f'{exid} bar {k + 1}: strokes not marked on the page')
            else:
                for j, (hh, mk) in enumerate(zip(hits, marks)):
                    if hh[1] == '-': continue
                    if mk[-1] != ('↑' if j in ups else '↓'): P(f'{exid} bar {k + 1}: the mark {mk} does not match the stroke')
            if name != 'A' or exid != 'quote':
                pcs = {(OPENS[i] + f) % 12 for i, f in enumerate(g) if f >= 0}
                if pcs != gtr.chord_pcs(name) and not pcs <= gtr.chord_pcs(name): P(f'{exid} bar {k + 1}: {name} {g} is not that chord')
                if min(OPENS[i] + f for i, f in enumerate(g) if f >= 0) % 12 != gtr.parse(name)[0]: P(f'{exid} bar {k + 1}: {name} has another bass')
            if exid == 'st5' and k < 6 and any(f == 0 for f in g): P(f'{exid} bar {k + 1}: an open string in a barre chord')
            if exid != 'st5' and name in ('Am', 'Dm', 'E7') and any(f > 3 for f in g): P(f'{exid} bar {k + 1}: not the open grip')
            sounding = sorted((6 - i for i, f in enumerate(g) if f >= 0), reverse=True)
            for j, hh in enumerate(hits):
                if hh[1] == '-': strokes.append(('-', hh[0])); continue
                if sorted(hh[1], reverse=True) != sounding: P(f'{exid} bar {k + 1}: a stroke misses strings of {name}')
                strokes.append(('U' if j in ups else 'D', hh[0]))
            chords += [name] * len(hits)
        exp = [('-' if f == '-' else 'U' if f.endswith('U') else 'D', l) for f, l in BARS[want]]
        fingers = [mk[:-1] for it in B['items'] for mk, hh in zip(it[4]['marks'], it[3]) if hh[1] != '-'] if all(len(it) > 4 for it in B['items']) else []
        want_f = [f[:-1] if f not in ('-', '.') else '' for f, l in BARS[want] if f != '-']
        if fingers != want_f: P(f'{exid} bar {k + 1}: fingers {fingers} vs Serrano’s {want_f}')
        if len(strokes) != len(exp) or any(a[0] != b[0] or abs(a[1] - b[1]) > 1e-9 for a, b in zip(strokes, exp)):
            P(f'{exid} bar {k + 1}: strokes {strokes} vs Serrano’s {want}')
        # the chord: the song's bar; in studies 2–4 the fourth bar's last beat carries the next bar's chord
        song = SONG[exid][k]
        if exid in ('st2', 'st3', 'st4') and k < 16 and k % 4 == 3 and k + 1 < 16:
            nxt = chart[k + 1]
            n_last = 1 if exid == 'st2' else 2
            if chords[:-n_last] != [song] * (len(chords) - n_last) or chords[-n_last:] != [nxt] * n_last: P(f'{exid} bar {k + 1}: {chords}, wants {song} then {nxt}')
        elif set(chords) != {song}: P(f'{exid} bar {k + 1}: {set(chords)}, the song has {song}')
        beats = sum(l for _, l in exp)
        if abs(sum(l for _, l in strokes) - beats) > 1e-9: P(f'{exid} bar {k + 1}: length')
# the fingers named in the notes: i s a m in that order
for exid in PLAN:
    if exid in EXS and 'i s a m' not in ' '.join(EXS[exid]['bars'][0]['note'].replace('↓', '').split()) and exid not in ('prep',):
        P(f'{exid}: the note does not give the fingers')
print('exercises checked:', len(PLAN), '· chart:', ' '.join(changes))
print('\n'.join(probs) if probs else 'all good')
sys.exit(1 if probs else 0)
