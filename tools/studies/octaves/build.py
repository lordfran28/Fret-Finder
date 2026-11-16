import sys, os
sys.path.insert(0, '/home/claude/studies'); sys.path.insert(0, '/home/claude/studies/octaves')
import study_page as SP
import entry as E
OUT = '/home/claude/studies/octaves/out/'; os.makedirs(OUT, exist_ok=True)
ENTRY = dict(key='octaves', title='Octaves', eyebrow='Exercises · Wes Montgomery',
             meta=[['Style', 'Jazz octaves (Wes Montgomery)'], ['Set on', 'Moonglow, in F'], ['Tempo', f'{SP.BPM} a minute']],
             lede='Melodies in octaves with the thumb, the way Wes Montgomery played them.',
             contents_intro='Everything on this page, in order. The folio has no exercises, only Wes’s solos; these are ours, on Moonglow’s chords.',
             track_title='The exercises, one after another', track_intro='Every bar in order. Tap a bar’s number to play from there.',
             track_pattern='Both notes of each octave together, with the thumb.', accent=('#3A2A1E', '#F3EAE0', '#7A4E22', '#E0B98E', '#140E09', '#E8C79E'))
bars, toc = SP.assemble(E.SECTIONS)
starts, spb = SP.times(bars)
if 'audio' in sys.argv: print('audio', SP.render(bars, starts, spb, OUT + 'octaves.mp3'), 's')
print('page', SP.page(ENTRY, bars, toc, starts, spb, OUT + 'index.html', 'octaves.mp3'), 'bytes;', len(bars), 'bars')
