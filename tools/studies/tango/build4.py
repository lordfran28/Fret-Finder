"""Build the vals entry: python3 build4.py [audio]"""
import sys, os
sys.path.insert(0, '/home/claude/studies'); sys.path.insert(0, '/home/claude/studies/tango')
import study_page as SP
SP.BPM = 132
SP.QUOTE_PAD = 3
import entry4 as E
OUT = '/home/claude/studies/tango/out4/'; os.makedirs(OUT, exist_ok=True)
ENTRY = dict(key='vals', title='Vals', eyebrow='Exercises · Julián Graciano',
             meta=[['Style', 'Tango vals (Graciano, Método de guitarra tango, ch. 20)'], ['Set on', 'Я вас любил, in G'], ['Tempo', f'{SP.BPM} a minute, in 3/4']],
             lede='The tango waltz: its rhythms for the right hand, the two ways to end, and the bass phrases that walk between the chords.',
             contents_intro='Everything on this page, in order. Each rhythm opens with Graciano’s own bar, then the same in G on Я вас любил.',
             track_title='The vals, one figure after another',
             track_intro='Every bar in order. Tap a bar’s number to play from there; the speeds below the player slow it down.',
             track_pattern='Bars marked G are Graciano’s own. Bars marked G are Graciano’s own, in A; the rest are in G, on Я вас любил.',
             accent=('#3A2326', '#F3E8E6', '#7A2E2E', '#E0B4B0', '#170D0E', '#E9C2BC'))
bars, toc = SP.assemble(E.SECTIONS, mark='G')
starts, spb = SP.times(bars)
if 'audio' in sys.argv:
    print('audio', SP.render(bars, starts, spb, OUT + 'vals.mp3'), 's')
print('page', SP.page(ENTRY, bars, toc, starts, spb, OUT + 'index.html', 'vals.mp3'), 'bytes;', len(bars), 'bars')
