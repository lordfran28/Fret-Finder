"""Build the tango entry: python3 build.py [audio]"""
import sys, os
sys.path.insert(0, '/home/claude/studies'); sys.path.insert(0, '/home/claude/studies/tango')
import study_page as SP
SP.BPM = 112
import entry as E
OUT = '/home/claude/studies/tango/out/'; os.makedirs(OUT, exist_ok=True)
ENTRY = dict(key='tango', title='Tango: the right hand', eyebrow='Exercises · Julián Graciano',
             meta=[['Style', 'Tango accompaniment (Graciano, Método de guitarra tango, ch. 1)'], ['Set on', 'Очи чёрные, D minor, A minor, E7'], ['Tempo', f'{SP.BPM} a minute']],
             lede='The rhythms a tango guitarist accompanies with: marcatto, yumbado, sincopado and its drag, the double syncopation, umpa-umpa, 3+3+2 and Gardel’s two.',
             contents_intro='Everything on this page, in order. Each rhythm opens with Graciano’s own bar, then the same rhythm on the chords of one of your songs.',
             track_title='The rhythms, one after another',
             track_intro='Every bar in order. Tap a bar’s number to play from there; the speeds below the player slow it down.',
             track_pattern='Bars marked G are Graciano’s own. A rest in the tab, (½), is where a short stroke is stopped by easing the left hand.',
             accent=('#3A2326', '#F3E8E6', '#7A2E2E', '#E0B4B0', '#170D0E', '#E9C2BC'))
bars, toc = SP.assemble(E.SECTIONS, mark='G')
starts, spb = SP.times(bars)
if 'audio' in sys.argv: print('audio', SP.render(bars, starts, spb, OUT + 'tango.mp3'), 's')
print('page', SP.page(ENTRY, bars, toc, starts, spb, OUT + 'index.html', 'tango.mp3'), 'bytes;', len(bars), 'bars')
