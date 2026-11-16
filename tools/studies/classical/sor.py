"""Sor's studies in Segovia's selection, Sor's notes (Mutopia, from the 19th-century editions), our fingering.
python3 sor.py PART [audio]   PART = 1 (I–VI) | 2 (XI–XII) | 3 (XIV, XVII)"""
import sys, os, subprocess
sys.path.insert(0, '/home/claude/studies'); sys.path.insert(0, '/home/claude/studies/classical')
import study_page as SP
import pieces as PC, check_sor as CS
from fractions import Fraction as Fr

STUDIES = {
    'I': dict(op='Op. 6 No. 8', key='C major', time='3/4', idea='Three-note chords in quarter notes, the tune on top and the bass moving under it, every note held its full length: it teaches you to keep a shape down while one voice moves.'),
    'II': dict(op='Op. 35 No. 13', key='C major', time='2/4', idea='Three layers at once: a tune in quarters and eighths on top, sixteenth-note arpeggios in the middle, a bass in half notes. The tune has to sing over the arpeggio.',
               fixes=[(Fr(52), 43, 44)], fixnote='In bar 27 the source has G in the arpeggio against G♯ in the bass; it is played here as G♯, the bass note it doubles.'),
    'III': dict(op='Op. 6 No. 2', key='A major', time='4/4', idea='In eighths, a tune note on top and a two-note chord under it take turns: tune, chord, tune, chord. The tune has to carry over the chords.'),
    'IV': dict(op='Op. 6 No. 1', key='D major', time='4/4', idea='A bass line in eighths answered on every off-beat by the same two-note chord on the upper strings: the thumb walks while the fingers repeat.'),
    'V': dict(op='Op. 35 No. 22', key='B minor', time='3/4', idea='A tune in long notes on top, arpeggios in eighths under it and a bass: the long notes have to ring over everything moving below.'),
    'VI': dict(op='Op. 35 No. 17', key='D major', time='4/4', idea='Mostly one note at a time: a line in eighths and dotted quarters with the bass under it, the hand moving across the strings.'),
    'XI': dict(op='Op. 6 No. 3', key='E major', time='4/4', idea='A chord on every other beat, then a quick figure on top: two thirty-second notes falling into a held note. The figure has to be light and land exactly.'),
    'XII': dict(op='Op. 6 No. 6', key='A major', time='3/8', idea='Thirds and sixths in eighths over a bass held for the whole bar, climbing high on the neck.', maxf=14),
    'XIV': dict(op='Op. 6 No. 12', key='A major', time='4/4', idea='A tune with its chords and bass, mostly in eighths: three and four voices to keep apart.'),
    'XVII': dict(op='Op. 6 No. 11', key='E minor', time='4/4', idea='Triplet arpeggios from start to end, with the tune in the top or in the bass of each group.'),
}
PARTS = {'1': ['I', 'II', 'III', 'IV', 'V', 'VI'], '2': ['XI', 'XII'], '3': ['XIV', 'XVII']}


def build(part, audio):
    keys = PARTS[part]
    ex = []
    for k in keys:
        S = STUDIES[k]
        bars, P = PC.piece_bars(CS.M + CS.T[k], k, fixes=S.get('fixes', ()), maxf=S.get('maxf', 12))
        wide = set(PC.wide_stretches(bars))
        for B in bars:
            B['note'] = ''
            if B['label'] in wide: B['note'] = 'A five-fret stretch low on the neck: the notes leave no other way.'
        if S.get('fixnote'):
            fb = [B for B in bars if B['label'] == f'{k}.27']
            if fb: fb[0]['note'] = (fb[0]['note'] + ' ' + S['fixnote']).strip()
        ex.append(dict(id=f'sor-{k.lower()}', title=f'Study {k} · {S["op"]}, {S["key"]}',
                       idea=f'Segovia’s Study {k}, Sor’s {S["op"]}, {S["key"]}, {S["time"]}. {S["idea"]} Sor’s notes complete, every repeat written out; the fingering is ours.',
                       quote=dict(where='', text='', item=None), bars=bars))
    sections = [dict(id='studies', title='Sor’s studies, Segovia’s numbering', part='Études', ex=ex)]
    slug = f'sor-{part}'
    out = f'/home/claude/studies/classical/out/{slug}/'; os.makedirs(out, exist_ok=True)
    nums = {'1': 'I–VI', '2': 'XI–XII', '3': 'XIV and XVII'}[part]
    entry = dict(key=slug.replace('-', ''), title=f'Sor’s studies, {nums}', eyebrow='Exercises · Fernando Sor',
                 meta=[['Style', 'Classical studies'], ['From', 'Segovia’s twenty, Sor’s own notes'], ['Tempo', f'{SP.BPM} a minute, slow']],
                 lede='Sor’s studies from Segovia’s selection, complete and in playing order, each note on the string and fret shown.',
                 contents_intro='Every study on this page, in order. Each is complete, with its repeats written out.',
                 track_title='The studies, one after another', track_intro='Every bar in order, slowly. Tap a bar’s number to play from there; the speeds below the player slow it further.',
                 track_pattern='Sor’s notes, our fingering. Bar numbers are the study’s number, then the bar.')
    bars, toc = SP.assemble(sections)
    starts, spb = SP.times(bars)
    if audio:
        secs = SP.render(bars, starts, spb, out + slug + '.mp3')
        tmp = out + slug + '.96.mp3'
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', out + slug + '.mp3', '-b:a', '96k', tmp], check=True); os.replace(tmp, out + slug + '.mp3')
        print('audio', secs, 's', os.path.getsize(out + slug + '.mp3') // 1024, 'KB')
    print('page', SP.page(entry, bars, toc, starts, spb, out + 'index.html', slug + '.mp3'), 'bytes;', len(bars), 'bars')
    return slug, entry


if __name__ == '__main__':
    SP.BPM = 72
    build(sys.argv[1], 'audio' in sys.argv)
