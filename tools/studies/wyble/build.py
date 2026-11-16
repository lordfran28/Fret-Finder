"""Build the Wyble entry: python3 build.py [audio]"""
import sys, os
sys.path.insert(0, '/home/claude/studies'); sys.path.insert(0, '/home/claude/studies/wyble')
import study_page as SP
import entry as E
OUT = '/home/claude/studies/wyble/out/'; os.makedirs(OUT, exist_ok=True)
ENTRY = dict(key='wyble', title='Two lines at once', eyebrow='Exercises · Jimmy Wyble',
             meta=[['Style', 'Two-line counterpoint (Jimmy Wyble)'], ['Set on', 'Moonglow, in F'], ['Tempo', f'{SP.BPM} a minute']],
             lede='Two independent lines on one guitar, the way Jimmy Wyble played: the thumb on the lower line, the fingers on the upper one.',
             contents_intro='Everything on this page, in order. Each exercise opens with the first notes of Wyble’s own where there is one, then ours on the chords of one of your songs.',
             track_title='The exercises, one after another',
             track_intro='Every bar in order. Tap a bar’s number to play from there; the speeds below the player slow it down.',
             track_pattern='Thumb on the lower line, fingers on the upper. Bars marked W are the opening of Wyble’s own exercise; the bars after it are ours.')
bars, toc = SP.assemble(E.SECTIONS)
starts, spb = SP.times(bars)
if 'audio' in sys.argv: print('audio', SP.render(bars, starts, spb, OUT + 'wyble.mp3'), 's')
print('page', SP.page(ENTRY, bars, toc, starts, spb, OUT + 'index.html', 'wyble.mp3'), 'bytes;', len(bars), 'bars')
