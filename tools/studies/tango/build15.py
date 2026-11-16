"""Build the tango harmony entry, rebuilt by rule: python3 -B build15.py [audio]"""
import sys, os
sys.path.insert(0, '/home/claude/studies'); sys.path.insert(0, '/home/claude/studies/tango')
import study_page as SP
SP.BPM = 80
import entry15 as E
OUT = '/home/claude/studies/tango/out15/'; os.makedirs(OUT, exist_ok=True)
ENTRY = dict(key='tango-harmony', title='Tango: harmony', eyebrow='Exercises · Julián Graciano',
             meta=[['Style', 'Tango harmonic turns (Graciano, Método de guitarra tango, ch. 5)'],
                   ['Set on', 'Очи чёрные, I Wonder Who’s Kissing Her Now, Я вас любил'],
                   ['Tempo', f'{SP.BPM} a minute']],
             lede='The harmony under a tango: the key’s own chords, the circle of 5ths, tritone substitutes, diminished chords for the dominant, the line cliché and the tritone with its resolutions.',
             contents_intro='Everything on this page, in order. Each turn opens with Graciano’s first beat or two, then his rule worked out on the chords of your songs, two places each where they fit.',
             track_title='The harmony, one turn after another',
             track_intro='Every bar in order. Tap a bar’s number to play from there; the speeds below the player slow it down.',
             track_pattern='Bars marked G are Graciano’s own opening; the rest are your songs.',
             accent=('#3A2326', '#F3E8E6', '#7A2E2E', '#E0B4B0', '#170D0E', '#E9C2BC'))
bars, toc = SP.assemble(E.SECTIONS, mark='G')
starts, spb = SP.times(bars)
if 'audio' in sys.argv:
    print('audio', SP.render(bars, starts, spb, OUT + 'harmony.mp3'), 's')
print('page', SP.page(ENTRY, bars, toc, starts, spb, OUT + 'index.html', 'harmony.mp3'), 'bytes;', len(bars), 'bars')
