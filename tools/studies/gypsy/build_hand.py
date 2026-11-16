"""Build the gypsy right-hand entry: python3 build_hand.py [audio]"""
import sys, os
sys.path.insert(0, '/home/claude/studies'); sys.path.insert(0, '/home/claude/studies/gypsy')
import study_page as SP
import hand as E
SP.BPM = E.BPM; SP.QUOTE_PAD = 4
OUT = '/home/claude/studies/gypsy/out_hand/'; os.makedirs(OUT, exist_ok=True)
ENTRY = dict(key='gypsy-hand', title='Gypsy jazz: the right hand', eyebrow='Exercises · Stéphane Wrembel',
             meta=[['Style', 'Gypsy jazz right hand, the “plume” (Wrembel)'], ['Set on', 'Очи чёрные: the bass of its chords on the open strings'], ['Tempo', f'{SP.BPM} a minute']],
             lede='The beat divided into one, two, three and on up to nine equal notes, four beats on each open string, with Wrembel’s strokes; then moving from one division to another. On the bass of Очи чёрные.',
             contents_intro='Everything on this page, in order.',
             track_title='The right hand, one division after another',
             track_intro='Every bar in order. Tap a bar’s number to play from there; the speeds below the player slow it down.',
             track_pattern='Each beat starts a little louder, so you can hear where it falls; upstrokes are a little lighter.',
             accent=('#3A2F1E', '#F3EDE2', '#7A5A22', '#E3CFA4', '#16120A', '#E8D3A6'))
bars, toc = SP.assemble(E.SECTIONS, mark='W')
starts, spb = SP.times(bars)
if 'audio' in sys.argv: print('audio', SP.render(bars, starts, spb, OUT + 'gypsy-hand.mp3'), 's')
print('page', SP.page(ENTRY, bars, toc, starts, spb, OUT + 'index.html', 'gypsy-hand.mp3'), 'bytes;', len(bars), 'bars')
