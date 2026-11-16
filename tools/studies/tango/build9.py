"""Build the tango melody entry: python3 build9.py [audio]"""
import sys, os
sys.path.insert(0, '/home/claude/studies'); sys.path.insert(0, '/home/claude/studies/tango')
import study_page as SP
SP.BPM = 76
import entry9 as E
OUT = '/home/claude/studies/tango/out9/'; os.makedirs(OUT, exist_ok=True)
ENTRY = dict(key='tango-melody', title='Tango: melody', eyebrow='Exercises · Julián Graciano',
             meta=[['Style', 'Tango melody and improvisation (Graciano, Método de guitarra tango, ch. 7)'],
                   ['Set on', 'I Wonder Who’s Kissing Her Now in E♭; Очи чёрные in A minor; Я вас любил in G; Glinka’s Я помню чудное мгновенье'],
                   ['Tempo', f'{SP.BPM} a minute']],
             lede='The line itself: which scale goes over each chord, Graciano’s tango minor, chromatic notes, blue notes and guide tones. His rules, each one on your songs’ chords.',
             contents_intro='Everything on this page, in order. Each part opens with Graciano’s own first notes where he gives notes, then the rule on one of your songs.',
             track_title='The lines, one exercise after another',
             track_intro='Every bar in order. Tap a bar’s number to play from there; the speeds below the player slow it down.',
             track_pattern='Bars marked G are Graciano’s own first notes; the rest are your songs.',
             accent=('#3A2326', '#F3E8E6', '#7A2E2E', '#E0B4B0', '#170D0E', '#E9C2BC'))
bars, toc = SP.assemble(E.SECTIONS, mark='G')
starts, spb = SP.times(bars)
if 'audio' in sys.argv:
    print('audio', SP.render(bars, starts, spb, OUT + 'melody.mp3'), 's')
print('page', SP.page(ENTRY, bars, toc, starts, spb, OUT + 'index.html', 'melody.mp3'), 'bytes;', len(bars), 'bars')
