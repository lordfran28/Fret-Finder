"""Build the Carcassi entry: python3 build.py [audio]"""
import sys, os
sys.path.insert(0, '/home/claude/studies'); sys.path.insert(0, '/home/claude/studies/carcassi')
import study_page as SP
import entry as E
OUT = '/home/claude/studies/carcassi/out/'; os.makedirs(OUT, exist_ok=True)
ENTRY = dict(key='carcassi', title='Right-hand arpeggios', eyebrow='Exercises · Matteo Carcassi',
             meta=[['Style', 'Classical method (Carcassi, Op. 59)'], ['Set on', 'Я вас любил, G and C major 7'], ['Tempo', f'{SP.BPM} a minute']],
             lede='Carcassi’s arpeggios for the right hand: the same order of thumb and fingers every time, until it runs by itself.',
             contents_intro='Everything on this page, in order. Each arpeggio opens with Carcassi’s own bar, then the same arpeggio on two chords of one of your songs.',
             track_title='The arpeggios, one after another',
             track_intro='Every bar in order. Tap a bar’s number to play from there; the speeds below the player slow it down.',
             track_pattern='p is the thumb, i the index, m the middle, a the ring finger. Bars marked W are Carcassi’s own.',
             accent=('#3B2F2A', '#F1E9E3', '#6B4A2E', '#D9B99B', '#16110E', '#E4C9A8'))
bars, toc = SP.assemble(E.SECTIONS)
starts, spb = SP.times(bars)
if 'audio' in sys.argv: print('audio', SP.render(bars, starts, spb, OUT + 'carcassi.mp3'), 's')
print('page', SP.page(ENTRY, bars, toc, starts, spb, OUT + 'index.html', 'carcassi.mp3'), 'bytes;', len(bars), 'bars')
