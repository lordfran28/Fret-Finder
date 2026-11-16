"""Build the Morel entry: python3 build.py [audio]"""
import sys, os
sys.path.insert(0, '/home/claude/studies'); sys.path.insert(0, '/home/claude/studies/morel')
import study_page as SP
SP.BPM = 104; SP.QUOTE_PAD = 2
import entry as E
OUT = '/home/claude/studies/morel/out/'; os.makedirs(OUT, exist_ok=True)
ENTRY = dict(key='morel', title='Latin American rhythms', eyebrow='Exercises · Jorge Morel',
             meta=[['Style', 'Latin American dances (Morel)'], ['Set on', 'Очи чёрные and Я вас любил'], ['Tempo', f'{SP.BPM} a minute']],
             lede='The malambo, the samba and the clave: the pattern under each dance, in Morel’s bar and then on your songs.',
             contents_intro='Everything on this page, in order. Each dance opens with the bar of Morel’s pattern, then the same pattern on one of your songs.',
             track_title='The rhythms, one after another',
             track_intro='Every bar in order. Tap a bar’s number to play from there; the speeds below the player slow it down.',
             track_pattern='Bars marked M are Morel’s own.',
             accent=('#3A2F1E', '#F3EDE2', '#7A5A22', '#E3CFA4', '#16120A', '#E8D3A6'))
bars, toc = SP.assemble(E.SECTIONS, mark='M')
starts, spb = SP.times(bars)
if 'audio' in sys.argv: print('audio', SP.render(bars, starts, spb, OUT + 'morel.mp3'), 's')
print('page', SP.page(ENTRY, bars, toc, starts, spb, OUT + 'index.html', 'morel.mp3'), 'bytes;', len(bars), 'bars')
