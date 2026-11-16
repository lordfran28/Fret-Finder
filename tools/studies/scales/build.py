import sys, os
sys.path.insert(0, '/home/claude/studies'); sys.path.insert(0, '/home/claude/studies/scales')
import study_page as SP
import entry as E
OUT = '/home/claude/studies/scales/out/'; os.makedirs(OUT, exist_ok=True)
ENTRY = dict(key='scales', title='Scales', eyebrow='Exercises · Andrés Segovia',
             meta=[['Style', 'Classical scales (Segovia)'], ['Keys', 'Those of your songs'], ['Tempo', f'{SP.BPM} a minute']],
             lede='Major and minor scales, two octaves, in the keys of your songs, as Segovia asks for them: apoyando, seven times each.',
             contents_intro='Every scale on this page, in order. The first opens with the beginning of Segovia’s own C major; the fingering of all of them is ours.',
             track_title='The scales, one after another', track_intro='Every bar in order. Tap a bar’s number to play from there.',
             track_pattern='Each scale once through; play it seven times with the right-hand fingers its first bar names.', accent=('#2E2A3A', '#EEEAF4', '#5B3F7A', '#C7B3E6', '#100D17', '#D8C6F0'))
bars, toc = SP.assemble(E.SECTIONS)
starts, spb = SP.times(bars)
if 'audio' in sys.argv: print('audio', SP.render(bars, starts, spb, OUT + 'scales.mp3'), 's')
print('page', SP.page(ENTRY, bars, toc, starts, spb, OUT + 'index.html', 'scales.mp3'), 'bytes;', len(bars), 'bars')
