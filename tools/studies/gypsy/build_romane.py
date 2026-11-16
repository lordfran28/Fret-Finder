"""Build the gypsy arpeggios entry: python3 build_romane.py [audio]"""
import sys, os
sys.path.insert(0, '/home/claude/studies'); sys.path.insert(0, '/home/claude/studies/gypsy')
import study_page as SP
SP.BPM = 100; SP.QUOTE_PAD = 3
import romane as E
OUT = '/home/claude/studies/gypsy/out_romane/'; os.makedirs(OUT, exist_ok=True)
ENTRY = dict(key='gypsy-romane', title='Gypsy jazz: arpeggios and scales across the neck', eyebrow='Exercises · Romane',
             meta=[['Style', 'Gypsy jazz (Romane)'], ['Set on', 'It Had to Be You: B♭ minor, its minor side'], ['Tempo', f'{SP.BPM} a minute, in eighths']],
             lede=('Minor and major triads all over the neck, the diminished seventh, the harmonic minor scale, the minor chord with a 6th or a 9th, '
                   'and three exercises for speed: Romane’s diagrams, each moved one fret up into It Had to Be You’s B♭ minor.'),
             contents_intro='Everything on this page, in order.',
             track_title='The exercises, one after another',
             track_intro='Every bar in order. Tap a bar’s number to play from there; the speeds below the player slow it down.',
             track_pattern='Each diagram goes up its numbers and back down, in eighths, alternate strokes.',
             accent=('#3A2F1E', '#F3EDE2', '#7A5A22', '#E3CFA4', '#16120A', '#E8D3A6'))
bars, toc = SP.assemble(E.SECTIONS, mark='R')
starts, spb = SP.times(bars)
if 'audio' in sys.argv: print('audio', SP.render(bars, starts, spb, OUT + 'gypsy-romane.mp3'), 's')
print('page', SP.page(ENTRY, bars, toc, starts, spb, OUT + 'index.html', 'gypsy-romane.mp3'), 'bytes;', len(bars), 'bars')
