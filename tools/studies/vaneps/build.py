"""Build the Van Eps entry: python3 build.py [audio]"""
import sys, os
sys.path.insert(0, '/home/claude/studies'); sys.path.insert(0, '/home/claude/studies/vaneps')
import study_page as SP
SP.BPM = 72; SP.QUOTE_PAD = 4
import entry as E
OUT = '/home/claude/studies/vaneps/out/'; os.makedirs(OUT, exist_ok=True)
ENTRY = dict(key='vaneps', title='Three-voice triads', eyebrow='Exercises · George Van Eps',
             meta=[['Style', 'Harmony on the neck (Van Eps, Harmonic Mechanisms)'], ['Set on', 'F major, the key of Moonglow'], ['Tempo', f'{SP.BPM} a minute']],
             lede='The scale of your key in three-voice triads, first with the root on top, then with it in the middle, from the bottom of the neck to the top and back.',
             contents_intro='Everything on this page, in order. It opens with Van Eps’s own first two triads, then the same in the key of one of your songs.',
             track_title='The rhythms, one after another',
             track_intro='Every bar in order. Tap a bar’s number to play from there; the speeds below the player slow it down.',
             track_pattern='Bars marked V are Van Eps’s own. One triad to a beat.',
             accent=('#3A2F1E', '#F3EDE2', '#7A5A22', '#E3CFA4', '#16120A', '#E8D3A6'))
bars, toc = SP.assemble(E.SECTIONS, mark='V')
starts, spb = SP.times(bars)
if 'audio' in sys.argv: print('audio', SP.render(bars, starts, spb, OUT + 'vaneps.mp3'), 's')
print('page', SP.page(ENTRY, bars, toc, starts, spb, OUT + 'index.html', 'vaneps.mp3'), 'bytes;', len(bars), 'bars')
