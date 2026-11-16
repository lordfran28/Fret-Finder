"""Build the second tango entry (bordoneos): python3 build2.py [audio]"""
import sys, os
sys.path.insert(0, '/home/claude/studies'); sys.path.insert(0, '/home/claude/studies/tango')
import study_page as SP
SP.BPM = 104
import entry2 as E
OUT = '/home/claude/studies/tango/out2/'; os.makedirs(OUT, exist_ok=True)
ENTRY = dict(key='tangobass', title='Tango: the bass', eyebrow='Exercises · Julián Graciano',
             meta=[['Style', 'Tango bordoneos (Graciano, Método de guitarra tango, ch. 2)'], ['Set on', 'Очи чёрные, D minor, A minor, E7'], ['Tempo', f'{SP.BPM} a minute']],
             lede='Bordoneos: phrases on the bass strings that lean into the next chord, walk it to its 3rd or 7th, start the song and end it.',
             contents_intro='Everything on this page, in order. Each figure opens with Graciano’s own, then the same figure where Очи чёрные needs it.',
             track_title='The bass phrases, one after another',
             track_intro='Every bar in order. Tap a bar’s number to play from there; the speeds below the player slow it down.',
             track_pattern='Bars marked G are Graciano’s own. The numbered dots are the bass phrase, in the order played.',
             accent=('#3A2326', '#F3E8E6', '#7A2E2E', '#E0B4B0', '#170D0E', '#E9C2BC'))
bars, toc = SP.assemble(E.SECTIONS, mark='G')
starts, spb = SP.times(bars)
if 'audio' in sys.argv:
    print('audio', SP.render(bars, starts, spb, OUT + 'tango-bass.mp3'), 's')
print('page', SP.page(ENTRY, bars, toc, starts, spb, OUT + 'index.html', 'tango-bass.mp3'), 'bytes;', len(bars), 'bars')
