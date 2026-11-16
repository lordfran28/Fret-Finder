"""Build the gypsy soloing entry: python3 build_solo.py [audio]"""
import sys, os
sys.path.insert(0, '/home/claude/studies'); sys.path.insert(0, '/home/claude/studies/gypsy')
import study_page as SP
SP.BPM = 96; SP.QUOTE_PAD = 3
import solo as E
OUT = '/home/claude/studies/gypsy/out_solo/'; os.makedirs(OUT, exist_ok=True)
ENTRY = dict(key='gypsy-solo', title='Gypsy jazz: the soloist’s techniques', eyebrow='Exercises · Roux, Daussat and Debarre',
             meta=[['Style', 'Gypsy jazz soloing (Gypsy Guitar: The Secrets, part two)'], ['Set on', 'Очи чёрные: its chords and its tune'], ['Tempo', f'{SP.BPM} a minute']],
             lede='Rest strokes, the triplet stroke, sweeping, rolling (on one note, on chords and on the tune), chromatics, artificial and natural harmonics, and octaves: the gypsy soloist’s techniques, on Очи чёрные.',
             contents_intro='Everything on this page, in order.',
             track_title='The techniques, one after another',
             track_intro='Every bar in order. Tap a bar’s number to play from there; the speeds below the player slow it down.',
             track_pattern='↓ a downstroke, ↑ an upstroke. Harmonics sound an octave above the fretted note.',
             accent=('#3A2F1E', '#F3EDE2', '#7A5A22', '#E3CFA4', '#16120A', '#E8D3A6'))
bars, toc = SP.assemble(E.SECTIONS, mark='D')
starts, spb = SP.times(bars)
if 'audio' in sys.argv: print('audio', SP.render(bars, starts, spb, OUT + 'gypsy-solo.mp3'), 's')
print('page', SP.page(ENTRY, bars, toc, starts, spb, OUT + 'index.html', 'gypsy-solo.mp3'), 'bytes;', len(bars), 'bars')
