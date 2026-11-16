"""Build the flamenco entry: python3 build.py [audio]"""
import sys, os
sys.path.insert(0, '/home/claude/studies'); sys.path.insert(0, '/home/claude/studies/flamenco')
import study_page as SP
SP.BPM = 72; SP.QUOTE_PAD = 1
import serrano_arp as E
OUT = '/home/claude/studies/flamenco/out/'; os.makedirs(OUT, exist_ok=True)
ENTRY = dict(key='flamenco', title='Flamenco right hand', eyebrow='Exercises · Gerhard Graf-Martinez, Juan Serrano',
             meta=[['Style', 'Flamenco (Graf-Martinez, method vol. 2, lesson 6; Serrano, Basic Techniques)'], ['Set on', 'Очи чёрные and Я вас любил'], ['Tempo', f'{SP.BPM} a minute']],
             lede='The flamenco arpeggios and the five-note tremolo, then Serrano’s four arpeggios with the ring finger apoyando and his study for the thumb: the right hand of flamenco on your songs.',
             contents_intro='Everything on this page, in order. Each exercise opens with its author’s first beat, then the same pattern on one of your songs.',
             track_title='The rhythms, one after another',
             track_intro='Every bar in order. Tap a bar’s number to play from there; the speeds below the player slow it down.',
             track_pattern='Bars marked G are Graf-Martinez’s own, S Serrano’s. p is the thumb, i the index, m the middle, a the ring finger.',
             accent=('#3A2F1E', '#F3EDE2', '#7A5A22', '#E3CFA4', '#16120A', '#E8D3A6'))
bars, toc = SP.assemble(E.SECTIONS, mark='G')
starts, spb = SP.times(bars)
if 'audio' in sys.argv: print('audio', SP.render(bars, starts, spb, OUT + 'flamenco.mp3'), 's')
print('page', SP.page(ENTRY, bars, toc, starts, spb, OUT + 'index.html', 'flamenco.mp3'), 'bytes;', len(bars), 'bars')
