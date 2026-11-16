"""I Wonder Who's Kissing Her Now (Joseph E. Howard and Harold Orlob, words by Will M. Hough and Frank R. Adams, 1909):
the chorus tune and its chords, copied note by note from the owner's score (IMSLP 680131, the 1947 Edward B. Marks
printing, pp. 3–4: G major, 3/4, Tempo di Valse). Only the 1909 tune, its chord symbols and the English words are
taken; not the 1947 piano part or the French words.

Read at 600 dpi bar by bar; the piano's right hand doubles the tune and was read as a second witness, and the piano's
bass was read where a chord diagram's place was unclear (bar 26: Am, then A on beat 3 over C♯ in the bass; bar 27: G
over D in the bass).

TUNE_G: [(bar, chord(s), [(note, beats)], words)], bar 0 the pickup; 'r' a rest; '~' ties a note into the next.
CHORDS: [(name, beat in the bar)] per bar, beats counted from 0.
"""
import mel as M

TUNE_G = [
    (0,  [], [('D4', 1)], 'I'),
    (1,  [('G', 0)], [('B4', 1), ('D5', 1), ('B4', 1)], 'won-der who’s'),
    (2,  [('G', 0)], [('A4', 1), ('D5', 1), ('A4', 1)], 'kiss-ing her'),
    (3,  [('G', 0)], [('G4~', 3)], 'now,'),
    (4,  [('G', 0)], [('G4', 2), ('r', 1)], ''),
    (5,  [('G', 0)], [('G4', 1), ('B4', 1), ('G4', 1)], 'Won-der who’s'),
    (6,  [('B', 0)], [('F#4', 1), ('B4', 1), ('F#4', 1)], 'teach-ing her'),
    (7,  [('C', 0)], [('E4~', 3)], 'how,'),
    (8,  [('E7', 0)], [('E4', 2), ('r', 1)], ''),
    (9,  [('Am', 0)], [('C5', 1), ('E5', 1), ('C5', 1)], 'Won-der who’s'),
    (10, [('E7', 0)], [('B4', 1), ('D5', 1), ('B4', 1)], 'look-ing in-'),
    (11, [('A7', 0)], [('A4', 2), ('G4', 1)], 'to her'),
    (12, [('A7', 0)], [('E4', 3)], 'eyes,'),
    (13, [('A7', 0)], [('B4', 2), ('A4', 1)], 'Breath-ing'),
    (14, [('A7', 0)], [('A4', 3)], 'sighs,'),
    (15, [('D7', 0)], [('E5', 2), ('Eb5', 1)], 'tell-ing'),
    (16, [('D7', 0)], [('D5', 2), ('D4', 1)], 'lies; I'),
    (17, [('G', 0)], [('B4', 1), ('D5', 1), ('B4', 1)], 'won-der who’s'),
    (18, [('G', 0)], [('A4', 1), ('D5', 1), ('A4', 1)], 'buy-ing the'),
    (19, [('G', 0)], [('G4~', 3)], 'wine'),
    (20, [('G', 0)], [('G4', 1), ('r', 1), ('D4', 1)], 'For'),
    (21, [('G', 0)], [('G4', 1), ('B4', 1), ('G4', 1)], 'lips that I'),
    (22, [('B', 0)], [('F#4', 1), ('B4', 1), ('F#4', 1)], 'used to call'),
    (23, [('C', 0)], [('E4~', 3)], 'mine,'),
    (24, [('E7', 0)], [('E4', 2), ('r', 1)], ''),
    (25, [('Am', 0)], [('E4', 1), ('F#4', 1), ('G4', 1)], 'Won-der if'),
    (26, [('Am', 0), ('A', 2)], [('A4', 1), ('G4', 1), ('A4', 1)], 'she ev-er'),
    (27, [('G', 0)], [('B4', 1), ('D5', 1), ('F#5', 1)], 'tells him of'),
    (28, [('E7', 0)], [('E5', 2), ('B4', 1)], 'me, I'),          # E5 under a fermata
    (29, [('Am', 0)], [('D5', 1), ('C5', 1), ('E4', 1)], 'won-der who’s'),
    # first ending (back to bar 1)
    (30, [('D7', 0)], [('B4', 1), ('A4', 1), ('D4', 1)], 'kiss-ing her'),
    (31, [('G', 0)], [('G4~', 3)], 'now.'),
    (32, [('D7', 0)], [('G4', 1), ('r', 1), ('D4', 1)], 'I'),
]
SECOND = [   # second ending, in place of bars 30–32
    (30, [('D7', 0)], [('B4', 1), ('A4', 1), ('D5', 1)], 'kiss-ing her'),
    (31, [('G', 0)], [('G4~', 3)], 'now.'),
    (32, [('G', 0)], [('G4', 1), ('r', 2)], ''),
]

STEPS, SEMIS = -2, -4                     # G major to E♭ major: a major 3rd down, letters and semitones together


def chord_to(name, steps=STEPS, semis=SEMIS):
    import re
    m = re.match(r'^([A-G][b#]?)(.*)$', name)
    return M.pc_name(M.tr(m.group(1) + '4', steps, semis)) + m.group(2)


def note_to(n, steps=STEPS, semis=SEMIS, octave=0):
    if n == 'r': return 'r'
    tie = n.endswith('~'); n = n.rstrip('~')
    out = M.tr(n, steps + 7 * octave, semis + 12 * octave)
    return out + ('~' if tie else '')


def in_eb(ending=2, octave=0):
    """the chorus in E♭, 3/4, with the chosen ending; octave=+1 puts it an octave up for the guitar's top strings"""
    body = TUNE_G[:30] + (TUNE_G[30:] if ending == 1 else SECOND)
    return [(b, [(chord_to(c), at) for c, at in chs], [(note_to(n, octave=octave), d) for n, d in notes], w) for b, chs, notes, w in body]


if __name__ == '__main__':
    for b, chs, notes, w in in_eb():
        print(f'{b:>2}  {" ".join(M.dname(c) + ("@" + str(at + 1) if at else "") for c, at in chs):<10} '
              f'{" ".join(("rest" if n == "r" else M.disp(n.rstrip("~")) + n[-1:].replace("~", "~").strip("0123456789")) + "/" + str(d) for n, d in notes):<28} {w}')
