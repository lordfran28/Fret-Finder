"""Build the tango solo-guitar entry: python3 -B build12.py [audio]"""
import sys, os
sys.path.insert(0, '/home/claude/studies'); sys.path.insert(0, '/home/claude/studies/tango')
import study_page as SP
SP.BPM = 80
import entry12 as E
OUT = '/home/claude/studies/tango/out12/'; os.makedirs(OUT, exist_ok=True)
ENTRY = dict(key='tango-solo', title='Tango: the guitar alone', eyebrow='Exercises · Julián Graciano',
             meta=[['Style', 'Tango, the guitar as soloist (Graciano, Método de guitarra tango, ch. 8)'],
                   ['Set on', 'I Wonder Who’s Kissing Her Now in E♭, the 1909 waltz'],
                   ['Tempo', f'{SP.BPM} a minute']],
             lede='The guitar as a small orchestra: the tune on the top strings, then over a plain chord, over a bass line, with dressed-up chords, and all three mixed through the chorus.',
             contents_intro='Everything on this page, in order: four exercises, then an étude. Graciano works on a tango still under copyright, so his bars are described, not played.',
             track_title='The exercises, one after another',
             track_intro='Every bar in order. Tap a bar’s number to play from there; the speeds below the player slow it down.',
             track_pattern='Every bar is your song: the tune always on top, as written.',
             accent=('#3A2326', '#F3E8E6', '#7A2E2E', '#E0B4B0', '#170D0E', '#E9C2BC'))
bars, toc = SP.assemble(E.SECTIONS, mark='G')
starts, spb = SP.times(bars)
if 'audio' in sys.argv:
    print('audio', SP.render(bars, starts, spb, OUT + 'solo.mp3'), 's')
print('page', SP.page(ENTRY, bars, toc, starts, spb, OUT + 'index.html', 'solo.mp3'), 'bytes;', len(bars), 'bars')
