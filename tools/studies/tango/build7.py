"""Build the tango fills entry: python3 build5.py [audio]"""
import sys, os
sys.path.insert(0, '/home/claude/studies'); sys.path.insert(0, '/home/claude/studies/tango')
import study_page as SP
SP.BPM = 92
import entry7 as E
OUT = '/home/claude/studies/tango/out7/'; os.makedirs(OUT, exist_ok=True)
ENTRY = dict(key='tango-harmony', title='Tango: harmony', eyebrow='Exercises · Julián Graciano',
             meta=[['Style', 'Tango harmony (Graciano, Método de guitarra tango, ch. 5)'], ['Set on', 'Очи чёрные in A minor; I Wonder Who’s Kissing Her Now in E♭'], ['Tempo', f'{SP.BPM} a minute']],
             lede='The turns of harmony a tango guitarist reaches for: the key’s chords between tonic and subdominant, the circle of 5ths, the tritone substitute, the diminished chord, the line cliché and the tritone with its four resolutions.',
             contents_intro='Everything on this page, in order. Each turn opens with Graciano’s own first chords or notes, then the whole of it on one of your songs.',
             track_title='The turns of harmony, one after another',
             track_intro='Every bar in order. Tap a bar’s number to play from there; the speeds below the player slow it down.',
             track_pattern='Bars marked G are Graciano’s own, in his keys (C minor, D minor, A minor, C); the rest are in A minor (Очи чёрные) or C minor and E♭ (I Wonder Who’s Kissing Her Now).',
             accent=('#3A2326', '#F3E8E6', '#7A2E2E', '#E0B4B0', '#170D0E', '#E9C2BC'))
bars, toc = SP.assemble(E.SECTIONS, mark='G')
starts, spb = SP.times(bars)
if 'audio' in sys.argv:
    print('audio', SP.render(bars, starts, spb, OUT + 'harmony.mp3'), 's')
print('page', SP.page(ENTRY, bars, toc, starts, spb, OUT + 'index.html', 'harmony.mp3'), 'bytes;', len(bars), 'bars')
