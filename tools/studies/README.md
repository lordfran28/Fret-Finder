# The Exercises entries: how they are built

Copies of the build area (`/home/claude/studies/` in the working session), kept here so the entries can be rebuilt.
They also need the song kit (`/home/claude/kit`, `/home/claude/render`), which is not in this repository.

- `kit_study.py`: note names, two-voice fingering (`place_lines`), chord shapes (`shape`), playability checks.
- `study_page.py`: bars, audio and page for an entry, on `page/template_study.html` (the song template with
  two-line steps).
- `wyble/`: the Wyble entry (`entry.py` holds every exercise and the rule it follows; `catalog.md` our notes on the
  books with page numbers).
- `carcassi/`: Carcassi's right-hand arpeggios as patterns of thumb and fingers.
- `classical/`: public-domain pieces from Mutopia's LilyPond files: `lyparse.py` reads them (checked against the
  file's own bar checks), `finger.py` fingers a whole piece, `pieces.py` turns it into bars, `sor.py` builds the
  Sor entries. Mutopia's files are fetched with a sparse checkout of github.com/MutopiaProject/MutopiaProject.
- `tango/`: Graciano's accompaniment rhythms (chapter 1), each a pattern of strokes on a grip: bass, chord, middle
  notes, open low strings; staccato is a stroke then a rest, accents and ghost notes a third value on the stroke, and the
  arrastre a slide up the bass string into the next downbeat.
- `tango/entry5.py`: Graciano's fills (chapter 3). Each fill is kept twice, his notes in C and ours, made by moving his
  whole by one interval (letters and semitones, so the spelling follows); `check5.py` proves every note moved by the
  same amount and the rhythm is his, value for value, and checks the grips, the two-note shapes and where the x falls.
  A run's given names may carry their own label after a bar: `=E,G,F|over E7`. A run may mark short notes: `{'short': [...]}`.
- `tango/entry6.py`: Graciano's cadences (chapter 4), kept the same way as the fills; `place` finds strings for each chord or
  pair of notes (one note per string, the stretch kept, nearest the position asked); `check6.py` proves the notes are his, moved.
- `tango/entry7.py`: Graciano's harmony (chapter 5), on `entry6.py`'s chords and pairs (it loads that file and clears its record
  of moves); `check7.py` checks it the same way. The ♯11 chord and the augmented 5th need the `m#5` quality in `scripts/gtr.py`.
- `tango/entry8.py`: Graciano's walking bass with chords (chapter 6), built from his rules, not from his notes: `formula` makes each bass
  line from his degrees for the chord, `place_bar` puts the bass on the low strings and the chord above it with every held chord under
  the hand, and `check8.py` checks each line against the rule. Held chords use a K item's `{'hold': beats, 'strings': [...]}` and
  bass lines an R item's `{'stop': True}` (both read by `study_page.render`).
- `tango/entry9.py`: Graciano's melody chapter (chapter 7): his scale for each chord, the tango minor, chromatic notes, blue notes
  and guide tones, each applied to the songs' chords. `mel.py` holds the spelled notes (C♭ and E♯ kept), his scales, his
  scale-for-a-chord rules (`rule_for`) and a single-line fingering in position; `check9.py` checks every line against its rule.
- `tango/quotes.py`: cuts every quote of a book to its first two beats; each entry calls it last.
- `sola/`: Sola's five steps for colouring a song's chords, applied to Очи чёрные (it borrows `K` from `tango/entry.py`).
  Minor 11 chords need the `m11` quality in the song kit's chord table (`scripts/gtr.py`).
- `morel/`: Morel's dance patterns (malambo, samba, clave) on Очи чёрные and Я вас любил.
- `folk/`: the strummed patterns of Música folklórica argentina's rhythm table (bailecito, gato, zamba, cueca, carnavalito).
- `gypsy/`: Wrembel's accompaniment rhythms (la pompe, waltz, bolero, bossa-manouche) on Moonglow, Я вас любил and Очи чёрные.
- `flamenco/`: Graf-Martinez's arpeggio exercises I–IV (right hand kept, on Очи чёрные's open chords) and the five-note tremolo on Я вас любил's tremolo opening.
- `vaneps/`: Van Eps's scale in first-inversion triads, worked out for F major (string sets and positions chosen by least movement).
