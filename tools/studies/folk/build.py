"""Build the folk entry: python3 build.py [audio]"""
import sys, os
sys.path.insert(0, '/home/claude/studies'); sys.path.insert(0, '/home/claude/studies/folk')
import study_page as SP
SP.BPM = 120; SP.QUOTE_PAD = 2
import entry as E
OUT = '/home/claude/studies/folk/out/'; os.makedirs(OUT, exist_ok=True)
ENTRY = dict(key='folk', title='Argentine folk rhythms', eyebrow='Exercises · Música folklórica argentina',
             meta=[['Style', 'Bailecito, gato, zamba, cueca, carnavalito'], ['Set on', 'Я вас любил and Очи чёрные'], ['Tempo', f'{SP.BPM} a minute']],
             lede='The strummed patterns under Argentina’s folk dances, each with its variant for where the tune rests.',
             contents_intro='Everything on this page, in order. Each pattern opens with the book’s own bar, then the same on your songs.',
             track_title='The dances, one after another',
             track_intro='Every bar in order. Tap a bar’s number to play from there; the speeds below the player slow it down.',
             track_pattern='Bars marked F are the book’s own patterns. High strokes on the top three strings, low ones on the bass strings.',
             accent=('#2B3550', '#E8ECF3', '#3D5A8A', '#B4C6E6', '#0F1420', '#C3D2EE'))
bars, toc = SP.assemble(E.SECTIONS, mark='F')
starts, spb = SP.times(bars)
if 'audio' in sys.argv: print('audio', SP.render(bars, starts, spb, OUT + 'folk.mp3'), 's')
print('page', SP.page(ENTRY, bars, toc, starts, spb, OUT + 'index.html', 'folk.mp3'), 'bytes;', len(bars), 'bars')
