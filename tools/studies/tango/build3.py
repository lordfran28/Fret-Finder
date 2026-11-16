"""Build the milonga entry: python3 build3.py [audio]"""
import sys, os
sys.path.insert(0, '/home/claude/studies'); sys.path.insert(0, '/home/claude/studies/tango')
import study_page as SP
SP.BPM = 96
SP.QUOTE_PAD = 2
import entry3b as E
OUT = '/home/claude/studies/tango/out3/'; os.makedirs(OUT, exist_ok=True)
ENTRY = dict(key='milonga', title='Milonga', eyebrow='Exercises · Julián Graciano',
             meta=[['Style', 'Milonga (Graciano, Método de guitarra tango, ch. 19)'], ['Set on', 'Очи чёрные in A minor; I Wonder Who’s Kissing Her Now’s C minor and E♭'], ['Tempo', f'{SP.BPM} a minute, in 2/4 (the contemporary milonga in 4/4)']],
             lede='The milonga’s rhythms for the right hand, its candombe and pesante, the milongueo and how to improvise its bass, the slow contemporary milonga, the fills, and Graciano’s plans for practising them together.',
             contents_intro='Everything on this page, in order. Each rhythm opens with Graciano’s own bar, then the same on the chords of one of your songs.',
             track_title='The milonga rhythms, one after another',
             track_intro='Every bar in order. Tap a bar’s number to play from there; the speeds below the player slow it down.',
             track_pattern='Bars marked G are Graciano’s own. Every stroke down. A rest in the tab is the short silence of the left hand easing off.',
             accent=('#3A2326', '#F3E8E6', '#7A2E2E', '#E0B4B0', '#170D0E', '#E9C2BC'))
bars, toc = SP.assemble(E.SECTIONS, mark='G')
starts, spb = SP.times(bars)
if 'audio' in sys.argv:
    print('audio', SP.render(bars, starts, spb, OUT + 'milonga.mp3'), 's')
print('page', SP.page(ENTRY, bars, toc, starts, spb, OUT + 'index.html', 'milonga.mp3'), 'bytes;', len(bars), 'bars')
