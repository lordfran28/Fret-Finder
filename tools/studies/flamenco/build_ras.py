"""Build the rasgueado entry: python3 build_ras.py [audio]"""
import sys, os
sys.path.insert(0, '/home/claude/studies'); sys.path.insert(0, '/home/claude/studies/flamenco')
import study_page as SP
SP.BPM = 72; SP.QUOTE_PAD = 3
import rasgueado as E
OUT = '/home/claude/studies/flamenco/out_ras/'; os.makedirs(OUT, exist_ok=True)
ENTRY = dict(key='flamenco-rasgueado', title='Flamenco: rasgueado', eyebrow='Exercises · Juan Serrano',
             meta=[['Style', 'Flamenco rasgueado (Serrano, Basic Techniques)'], ['Set on', 'Очи чёрные: E7, A minor, D minor'], ['Tempo', f'{SP.BPM} a minute: slowly, as Serrano asks']],
             lede='The flamenco strum: the index, then the little, ring and middle fingers flicked out across the strings in turn. One finger a beat, then the four strokes in a beat, in three and in four, with the index alone and the index up and down; the last study on barre chords. On Очи чёрные’s chords.',
             contents_intro='Everything on this page, in order.',
             track_title='The rasgueado, one exercise after another',
             track_intro='Every bar in order. Tap a bar’s number to play from there; the speeds below the player slow it down.',
             track_pattern='↓ a downstroke, from the low string to the high; ↑ an upstroke, with the index, from the high string down.',
             accent=('#3A2F1E', '#F3EDE2', '#7A5A22', '#E3CFA4', '#16120A', '#E8D3A6'))
bars, toc = SP.assemble(E.SECTIONS, mark='S')
starts, spb = SP.times(bars)
if 'audio' in sys.argv: print('audio', SP.render(bars, starts, spb, OUT + 'flamenco-rasgueado.mp3'), 's')
print('page', SP.page(ENTRY, bars, toc, starts, spb, OUT + 'index.html', 'flamenco-rasgueado.mp3'), 'bytes;', len(bars), 'bars')
