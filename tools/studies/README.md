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
- `sola/`: Sola's five steps for colouring a song's chords, applied to Очи чёрные (it borrows `K` from `tango/entry.py`).
  Minor 11 chords need the `m11` quality in the song kit's chord table (`scripts/gtr.py`).
- `morel/`: Morel's dance patterns (malambo, samba, clave) on Очи чёрные and Я вас любил.
- `folk/`: the strummed patterns of Música folklórica argentina's rhythm table (bailecito, gato, zamba, cueca, carnavalito).
- `gypsy/`: Wrembel's accompaniment rhythms (la pompe, waltz, bolero, bossa-manouche) on Moonglow, Я вас любил and Очи чёрные.
- `flamenco/`: Graf-Martinez's arpeggio exercises I–IV (right hand kept, on Очи чёрные's open chords) and the five-note tremolo on Я вас любил's tremolo opening.
- `vaneps/`: Van Eps's scale in first-inversion triads, worked out for F major (string sets and positions chosen by least movement).
