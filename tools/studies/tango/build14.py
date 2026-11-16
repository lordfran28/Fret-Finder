"""Build the tango cadences entry, rebuilt by rule: python3 -B build14.py [audio]"""
import sys, os
sys.path.insert(0, '/home/claude/studies'); sys.path.insert(0, '/home/claude/studies/tango')
import study_page as SP
SP.BPM = 84
import entry14 as E
OUT = '/home/claude/studies/tango/out14/'; os.makedirs(OUT, exist_ok=True)
ENTRY = dict(key='tango-cadences', title='Tango: cadences', eyebrow='Exercises · Julián Graciano',
             meta=[['Style', 'Tango cadences (Graciano, Método de guitarra tango, ch. 4)'],
                   ['Set on', 'Очи чёрные, I Wonder Who’s Kissing Her Now, Я помню чудное мгновенье, Я вас любил'],
                   ['Tempo', f'{SP.BPM} a minute']],
             lede='How tango joins one section to the next and how it lands at the end: two lines in contrary motion, the ♭VI7, triads over a pedal, bass lines through diminished chords, the decariana and its octaves.',
             contents_intro='Everything on this page, in order. Each cadence opens with Graciano’s first beat or two, then his rule worked out in the keys and chords of your songs.',
             track_title='The cadences, one after another',
             track_intro='Every bar in order. Tap a bar’s number to play from there; the speeds below the player slow it down.',
             track_pattern='Bars marked G are Graciano’s own opening; the rest are your songs.',
             accent=('#3A2326', '#F3E8E6', '#7A2E2E', '#E0B4B0', '#170D0E', '#E9C2BC'))
bars, toc = SP.assemble(E.SECTIONS, mark='G')
starts, spb = SP.times(bars)
if 'audio' in sys.argv:
    print('audio', SP.render(bars, starts, spb, OUT + 'cadences.mp3'), 's')
print('page', SP.page(ENTRY, bars, toc, starts, spb, OUT + 'index.html', 'cadences.mp3'), 'bytes;', len(bars), 'bars')
