"""Build the tango fills entry: python3 build5.py [audio]"""
import sys, os
sys.path.insert(0, '/home/claude/studies'); sys.path.insert(0, '/home/claude/studies/tango')
import study_page as SP
SP.BPM = 92
import entry6 as E
OUT = '/home/claude/studies/tango/out6/'; os.makedirs(OUT, exist_ok=True)
ENTRY = dict(key='tango-cadences', title='Tango: cadences', eyebrow='Exercises · Julián Graciano',
             meta=[['Style', 'Tango cadences (Graciano, Método de guitarra tango, ch. 4)'], ['Set on', 'Очи чёрные in A minor; I Wonder Who’s Kissing Her Now in E♭'], ['Tempo', f'{SP.BPM} a minute']],
             lede='How a tango moves from one section to the next, and how it comes to its end: two-voice lines, diminished chords, the bass climbing to the leading note, the decariana.',
             contents_intro='Everything on this page, in order. Each cadence opens with Graciano’s own first beat or two, then the whole cadence in the key of one of your songs.',
             track_title='The cadences, one after another',
             track_intro='Every bar in order. Tap a bar’s number to play from there; the speeds below the player slow it down.',
             track_pattern='Bars marked G are Graciano’s own, in his keys (D minor, C, F); the rest are in A minor (Очи чёрные) or E♭ (I Wonder Who’s Kissing Her Now).',
             accent=('#3A2326', '#F3E8E6', '#7A2E2E', '#E0B4B0', '#170D0E', '#E9C2BC'))
bars, toc = SP.assemble(E.SECTIONS, mark='G')
starts, spb = SP.times(bars)
if 'audio' in sys.argv:
    print('audio', SP.render(bars, starts, spb, OUT + 'cadences.mp3'), 's')
print('page', SP.page(ENTRY, bars, toc, starts, spb, OUT + 'index.html', 'cadences.mp3'), 'bytes;', len(bars), 'bars')
