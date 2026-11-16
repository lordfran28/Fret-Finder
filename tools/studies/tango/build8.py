"""Build the tango walking-bass entry: python3 build8.py [audio]"""
import sys, os
sys.path.insert(0, '/home/claude/studies'); sys.path.insert(0, '/home/claude/studies/tango')
import study_page as SP
SP.BPM = 92
import entry8 as E
OUT = '/home/claude/studies/tango/out8/'; os.makedirs(OUT, exist_ok=True)
ENTRY = dict(key='tango-walking', title='Tango: walking bass', eyebrow='Exercises · Julián Graciano',
             meta=[['Style', 'Tango walking bass with chords (Graciano, Método de guitarra tango, ch. 6)'],
                   ['Set on', 'I Wonder Who’s Kissing Her Now in E♭; Очи чёрные in A minor; one bar of I’ll Be Seeing You'], ['Tempo', f'{SP.BPM} a minute']],
             lede='The guitar as bass and chords at once: the bass walking in quarters on the low strings, the chord answering above it. Graciano’s rhythms for the chord, his voicings, and his rules for the bass notes, all on your songs.',
             contents_intro='Everything on this page, in order. Each part opens with Graciano’s own first notes or chords, then the rule on one of your songs.',
             track_title='The walking bass, one exercise after another',
             track_intro='Every bar in order. Tap a bar’s number to play from there; the speeds below the player slow it down.',
             track_pattern='Bars marked G are Graciano’s own first notes, in C; the rest are your songs.',
             accent=('#3A2326', '#F3E8E6', '#7A2E2E', '#E0B4B0', '#170D0E', '#E9C2BC'))
bars, toc = SP.assemble(E.SECTIONS, mark='G')
for B in bars:
    for k in ('ch', 'bass', 'strikes'): B.pop(k, None)
starts, spb = SP.times(bars)
if 'audio' in sys.argv:
    print('audio', SP.render(bars, starts, spb, OUT + 'walking.mp3'), 's')
print('page', SP.page(ENTRY, bars, toc, starts, spb, OUT + 'index.html', 'walking.mp3'), 'bytes;', len(bars), 'bars')
