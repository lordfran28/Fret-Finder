"""Build an Exercises entry page (studies/<slug>/) from an entry module: the bars in order (each exercise its own part),
the audio of every bar, and the page itself (the song template with the song-only sections left out, a contents list
at the front linking every exercise, étude and piece)."""
import sys, json, html, re, subprocess, os
sys.path.insert(0, '/home/claude/kit'); sys.path.insert(0, '/home/claude/render'); sys.path.insert(0, '/home/claude/studies')
import numpy as np
from core import bar_events, damp, to_mp3, item_beats
from kit_study import OPEN
import page as PG
from song_page import build as build_song

BPM = 66
QUOTE_PAD = 4          # a quote shorter than this many beats is filled out with silence (2 for pieces in 2/4)


def item_len(it):
    if it[0] == 'K': return sum(h[0] for h in it[3])
    if it[0] in ('C', 'T'): return it[3]
    if it[0] in ('R', 'P'): return sum(it[2])
    if it[0] == 'W': return it[1]
    return 0


def assemble(sections, mark='W'):
    """Bars in order. A quote of the original's opening figure (when there is one) leads each exercise, then our bars.
    The quote's bar is labelled with `mark` (W for Wyble, Carcassi and the classical books, G for Graciano...)."""
    bars, toc = [], []
    for S in sections:
        sec_toc = dict(title=S['title'], part=S['part'], items=[])
        for ex in S['ex']:
            first = len(bars)
            q = ex['quote']
            head = f"{ex['idea']}"
            if q.get('item') or q.get('items'):
                its = list(q['items']) if q.get('items') else [q['item']]
                L = sum(item_len(x) for x in its)
                if L < QUOTE_PAD: its.append(['W', QUOTE_PAD - L])
                bars.append(dict(label=f'{mark}{len(toc_flat(toc, sec_toc)) + 1}', sec=ex['title'], items=its, chords=[],
                                 note=f"{head} {q.get('whose', 'Wyble’s own')}, {q['where']}: {q['text']} {q.get('played', 'Played here: its opening only.')}", quote=True))
                first_note_done = True
            else:
                first_note_done = False
            for j, b in enumerate(ex['bars']):
                note = b['note']
                if not first_note_done and j == 0:
                    note = f"{head} {(q.get('by', 'Wyble') + ' (' + q['where'] + '): ' + q['text'] + ' ') if q.get('text') else ''}{note}"
                bars.append(dict(label=b.get('label') or str(sum(1 for x in bars if not x.get('quote')) + 1), sec=ex['title'], items=b['items'], chords=b['chords'], note=note))
            sec_toc['items'].append(dict(id=ex['id'], title=ex['title'], bar=first))
        toc.append(sec_toc)
    for B in bars:
        L = sum(item_len(it) for it in B['items'])
        assert 0.25 <= L <= 8, (B['label'], L)                                # 4/4, 5/4 where the book is in 5, a piece's own bars
        B['beats'] = L
    return bars, toc


def toc_flat(toc, cur):
    return [i for s in toc for i in s['items']] + cur['items']


def times(bars, gap=0.0):
    spb = 60 / BPM; t = 0.6; out = {}
    for B in bars:
        out[B['label']] = t; t += B.get('beats', 4) * spb + gap
    return out, spb


def render(bars, starts, spb, out_mp3):
    rng = np.random.default_rng(7)
    ev = []
    for B in bars:
        x = 0.0; t0 = starts[B['label']]
        for it in B['items']:
            dv = []; shorts = []                                   # (beat in the item, velocity change): accents, ghost notes
            hold = stop = None
            if it[0] == 'K' and len(it) > 4 and isinstance(it[4], dict):    # {'hold': beats, 'strings': [...]}: those strings ring on
                hold = it[4]; it = it[:4]
            if it[0] == 'R' and len(it) > 4 and isinstance(it[4], dict) and it[4].get('stop'):
                stop = True                                         # a bass line: each note stops at its written end
            pinfo = None
            if it[0] == 'P' and len(it) > 4 and isinstance(it[4], dict):   # {'hold': [strings]}: those notes ring until
                pinfo = it[4]; it = it[:4]                          # struck again; every other note ends at its own end
            ups = []                                                # upstrokes: the strum runs from the high string down
            if it[0] == 'K' and hold and hold.get('up'):
                y = 0.0
                for k, h in enumerate(it[3]):
                    if k in hold['up']: ups.append(y)
                    y += h[0]
            if it[0] == 'K' and any(len(h) > 2 for h in it[3]):
                y = 0.0
                for h in it[3]:
                    if len(h) > 2 and h[2]: dv.append((y, h[2]))
                    y += h[0]
                it = ['K', it[1], it[2], [list(h[:2]) for h in it[3]]]
            elif it[0] == 'R' and len(it) > 4 and isinstance(it[4], dict):
                y = 0.0
                for d, v in zip(it[2], it[4].get('vel', [])):
                    if v: dv.append((y, v))
                    y += d
                y = 0.0
                for d, sh in zip(it[2], it[4].get('short', [])):     # staccato notes in a run: half their length
                    if sh: shorts.append((x + y, d))
                    y += d
                it = it[:4]
            e = bar_events([it], lambda y, x0=x, t0=t0: t0 + (x0 + y) * spb, vel=0.5, rng=rng, accent_beats=())
            for q in e:
                q['src'] = it[0]
                if hold and q['string'] in hold.get('strings', []): q['hold_end'] = q['t'] + hold['hold'] * spb
                if stop: q['stop'] = True
                if pinfo is not None:
                    if q['string'] in pinfo.get('hold', []): q['p_hold'] = True
                    else: q['short_end'] = q['end'] + 0.03
                yb = (q['t'] - t0) / spb - x
                for y, v in dv:
                    if -0.02 <= yb - y <= 0.14: q['vel'] += v
                for y, d in shorts:
                    if abs((q['t'] - t0) / spb - y) < 0.02: q['short_end'] = q['t'] + 0.45 * d * spb
            for y in ups:
                grp = [q for q in e if q.get('midi') is not None and -0.02 <= (q['t'] - t0) / spb - x - y <= 0.14]
                ts = sorted(q['t'] for q in grp)
                for q, t in zip(sorted(grp, key=lambda q: q['string']), ts): q['t'] = t; q['vel'] -= 0.04
            ev += e; x += item_len(it)
    notes = damp(ev, staccato=0.05)
    # two lines: each voice rings until its string is played again (legato), as the lines are written
    bys = {}
    for e in sorted(notes, key=lambda e: e['t']): bys.setdefault(e['string'], []).append(e)
    for s, lst in bys.items():
        for a, b in zip(lst, lst[1:] + [None]):
            if a.get('src') in ('P', 'R'):
                a['off'] = min(b['t'] + 0.01 if b else a['t'] + 2.0, a['t'] + 2.4); a['rel_tau'] = 0.06
            if a.get('p_hold'): a['off'] = min(b['t'] + 0.01 if b else a['t'] + 4.5, a['t'] + 4.5)
            if a.get('short_end'): a['off'] = min(a['off'], a['short_end'])
            if a.get('hold_end'): a['off'] = min(b['t'] + 0.01 if b else a['hold_end'], a['hold_end']); a['rel_tau'] = 0.06
            if a.get('stop'): a['off'] = min(a['off'], a['end'] + 0.03)
    import guitar
    from core import render_guitar
    SR = guitar.SR
    if max(e['t'] for e in notes) < 300:
        gt = render_guitar(notes, None, seed=11, wet=0.24, tail=8.0)
    else:
        # a long page: render it in pieces of about two and a half minutes and add them up (the body and the room are
        # linear filters, so the sum is the same sound); one piece at a time keeps the memory down
        SEG, TAIL = 150.0, 8.0
        end = max(e['off'] for e in notes) + TAIL
        gt = np.zeros((int(end * SR) + SR, 2), dtype=np.float32)
        k = 0
        while k * SEG <= max(e['t'] for e in notes):
            s0 = k * SEG
            part = [dict(e, t=e['t'] - s0, off=e['off'] - s0) for e in notes if s0 <= e['t'] < s0 + SEG]
            if part:
                g = render_guitar(part, None, seed=11 + k, wet=0.24, tail=TAIL).astype(np.float32)
                a = int(round(s0 * SR)); n = min(len(g), len(gt) - a)
                gt[a:a + n] += g[:n]
                del g
            k += 1
    return round(to_mp3(gt, SR, out_mp3, fade=1.5), 1)


INDEX_CSS = """
<style>
#contents .toc-part { margin: 6px 0 14px; }
#contents .toc-part h3 { font-size: 15px; margin: 10px 0 6px; color: var(--accent); letter-spacing: .02em; }
#contents ol { margin: 0 0 0 20px; padding: 0; display: grid; gap: 4px; }
#contents li a { color: var(--ink); text-decoration: none; border-bottom: 1px solid var(--line); }
#contents li a:hover { color: var(--accent); border-color: var(--accent); }
#contents .toc-sec { font-weight: 700; margin: 8px 0 4px; }
.fbar.is-quote { outline: 1px dashed var(--line); outline-offset: 4px; }
</style>"""


def page(entry, bars, toc, starts, spb, out_html, audio_name):
    TIM = {B['label']: dict(start=round(starts[B['label']] - 0.6 + 0.6, 3), voc='', pcs=[], words='', mel='') for B in bars}
    key = entry['key']
    cfg = dict(bars=bars, timing=TIM, key_pc=entry.get('key_pc', 5), key_name=entry.get('key_name', 'F'), flats=True, spb=spb, meter=4,
               song=dict(id=key, singer='', sharps=False, words=False, title=entry['title'], artist=entry['eyebrow'], key='', tonic='', meter=4, bpm=BPM,
                         meta=entry['meta'], lede=entry['lede'], tuning_note='', lyrics_note='', map_intro='', cues=False),
               moves=[], lessons={}, roadmap=[], src={}, track=dict(key=key, title=entry['track_title'], jump='Exercises', audio=audio_name,
                                                                    intro=entry['track_intro'], pattern=entry['track_pattern']),
               words=False, cues=False, extra_src=[], lib_notes={}, src_note='', sec_notes={}, slots=[], seqs={}, ie=[], studio=[],
               fill_min=99, no_fill_secs=(), replaced=[], replaced_p='', cp_title='', cp_lede='', ie_p='', out=out_html, title=entry['title'],
               accent=entry.get('accent', ('#2B3552', '#E7E9F2', '#5C4A2A', '#A8B5DA', '#10131C', '#DCC895')))
    PG.TEMPLATE = '/home/claude/studies/page/template_study.html'
    build_song(cfg)
    h = open(out_html).read()
    if not h.lstrip().lower().startswith('<!doctype'):
        h = ('<!doctype html><html><head><meta charset=utf8><meta name=viewport content="width=device-width,initial-scale=1,viewport-fit=cover">'
             + open('/home/claude/sf3/work/skeleton_style.txt').read() + '</head><body>' + h + '</body></html>')
    # the compendium belongs to song pages
    h = re.sub(r'<!-- compendium:start -->.*?<!-- compendium:end -->', '<!-- compendium:start --><!-- compendium:end -->', h, flags=re.S)
    # the contents at the front: every exercise (and later every étude and piece) on the page, linked
    parts, last = [], None
    for S in toc:
        lis = ''.join(f'<li><a href="#fb-{key}-{it["bar"]}">{html.escape(it["title"])}</a></li>' for it in S['items'])
        head = f'<h3>{html.escape(S["part"])}</h3>' if S['part'] != last else ''      # the part's name once, over its sections
        last = S['part']
        parts.append(f'<div class="toc-part">{head}<div class="toc-sec">{html.escape(S["title"])}</div><ol>{lis}</ol></div>')
    contents = (f'<section class="block" id="contents"><div class="block-head"><h2>Contents</h2><p>{html.escape(entry["contents_intro"])}</p></div>'
                + ''.join(parts) + '</section>')
    h = h.replace('<div id="tracks"></div>', contents + '<div id="tracks"></div>', 1)
    # song-only sections stay out; the nav lists what this page has
    quote_idx = [i for i, B in enumerate(bars) if B.get('quote')]
    tail = ("<script>(function(){['chords','moves','play','map','spoken','ends','practice','about','sources','trumpet'].forEach(function(id){var s=document.getElementById(id);if(s)s.hidden=true;});"
            "var j=document.getElementById('jumps');if(j)j.innerHTML='<a href=\"#contents\">Contents</a><a href=\"#" + key + "\">Exercises</a>';"
            f"var q={json.dumps(quote_idx)};q.forEach(function(i){{var b=document.getElementById('fb-{key}-'+i);if(b)b.classList.add('is-quote');}});"
            "})();</script>")
    h = h.replace('</head>', INDEX_CSS + '</head>', 1).replace('</body>', tail + '</body>', 1)
    open(out_html, 'w').write(h)
    return len(h)
