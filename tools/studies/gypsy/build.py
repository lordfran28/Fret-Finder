"""Build the gypsy entry: python3 build.py [audio]"""
import sys, os
sys.path.insert(0, '/home/claude/studies'); sys.path.insert(0, '/home/claude/studies/gypsy')
import study_page as SP
SP.BPM = 132; SP.QUOTE_PAD = 3
import entry as E
OUT = '/home/claude/studies/gypsy/out/'; os.makedirs(OUT, exist_ok=True)
ENTRY = dict(key='gypsy', title='Gypsy jazz rhythm', eyebrow='Exercises · Stéphane Wrembel',
             meta=[['Style', 'Gypsy jazz accompaniment (Wrembel)'], ['Set on', 'Moonglow, Я вас любил, Очи чёрные'], ['Tempo', f'{SP.BPM} a minute']],
             lede='La pompe, the gypsy waltz, the bolero and the bossa-manouche: the right hand of gypsy jazz on your songs.',
             contents_intro='Everything on this page, in order. Each rhythm opens with Wrembel’s bar, then the same pattern on one of your songs.',
             track_title='The rhythms, one after another',
             track_intro='Every bar in order. Tap a bar’s number to play from there; the speeds below the player slow it down.',
             track_pattern='Bars marked W are Wrembel’s own rhythms. Squashed strokes ring a little; whipped ones are cut at once.',
             accent=('#3A2F1E', '#F3EDE2', '#7A5A22', '#E3CFA4', '#16120A', '#E8D3A6'))
bars, toc = SP.assemble(E.SECTIONS, mark='W')
starts, spb = SP.times(bars)
if 'audio' in sys.argv: print('audio', SP.render(bars, starts, spb, OUT + 'gypsy.mp3'), 's')
print('page', SP.page(ENTRY, bars, toc, starts, spb, OUT + 'index.html', 'gypsy.mp3'), 'bytes;', len(bars), 'bars')
