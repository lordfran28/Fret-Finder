"""Build the Sola entry: python3 build.py [audio]"""
import sys, os
sys.path.insert(0, '/home/claude/studies'); sys.path.insert(0, '/home/claude/studies/sola')
import study_page as SP
SP.BPM = 100; SP.QUOTE_PAD = 3
import entry as E
OUT = '/home/claude/studies/sola/out/'; os.makedirs(OUT, exist_ok=True)
ENTRY = dict(key='sola', title='Varying a song’s chords', eyebrow='Exercises · Diego Sola',
             meta=[['Style', 'Harmony (Sola, Recursos armónicos para guitarra)'], ['Set on', 'Очи чёрные, its second half'], ['Tempo', f'{SP.BPM} a minute, in 3/4']],
             lede='Sola’s five steps for colouring a song’s chords: their degrees, the extensions that suit each job, added dominants and their substitutes, all linked by the nearest notes.',
             contents_intro='Everything on this page, in order. Sola writes no exercises, only tables and steps; each one here quotes his step, then applies it to Очи чёрные.',
             track_title='The chords, one choice after another',
             track_intro='Every bar in order. Tap a bar’s number to play from there; the speeds below the player slow it down.',
             track_pattern='Bass, then the chord twice, in each bar. Compare each choice with the song’s plain chords at the top.',
             accent=('#2E3A2E', '#E9F1E7', '#4E6B3A', '#B9D3AE', '#101710', '#C9DDB8'))
bars, toc = SP.assemble(E.SECTIONS)
starts, spb = SP.times(bars)
if 'audio' in sys.argv:
    print('audio', SP.render(bars, starts, spb, OUT + 'sola.mp3'), 's')
print('page', SP.page(ENTRY, bars, toc, starts, spb, OUT + 'index.html', 'sola.mp3'), 'bytes;', len(bars), 'bars')
