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
- `tango/entry5.py`, `entry6.py`, `entry7.py` (Graciano's fills, cadences and harmony, chapters 3–5) were taken out on 16 November: they kept
  his examples as data and moved them whole into other keys. Those pages are being rebuilt from his rules, as `entry8.py` on.
- `tango/entry8.py`: Graciano's walking bass with chords (chapter 6), built from his rules, not from his notes: `formula` makes each bass
  line from his degrees for the chord, `place_bar` puts the bass on the low strings and the chord above it with every held chord under
  the hand, and `check8.py` checks each line against the rule. Held chords use a K item's `{'hold': beats, 'strings': [...]}` and
  bass lines an R item's `{'stop': True}` (both read by `study_page.render`).
- `tango/entry3b.py`: the rest of the milonga chapter (milongueo in major, improvising its bass, the contemporary milonga, the fills,
  the plans), added to `entry3.py`'s page; `check3b.py` checks it. `build3.py` builds the whole milonga page from `entry3b`.
- `tango/entry4b.py`: the rest of the vals chapter (fills, the 6/8 over the waltz, the tango valseado, the plans), added to `entry4.py`'s
  page; `check4b.py` checks it. `build4.py` builds the whole vals page from `entry4b`.
- `tango/entry9.py`: Graciano's melody chapter (chapter 7): his scale for each chord, the tango minor, chromatic notes, blue notes
  and guide tones, each applied to the songs' chords. `mel.py` holds the spelled notes (C♭ and E♯ kept), his scales, his
  scale-for-a-chord rules (`rule_for`) and a single-line fingering in position; `check9.py` checks every line against its rule.
- `tango/entry10.py`: Graciano's melodic patterns (end of chapter 7): `pattern` runs a pattern's shape over a song's chords, each chord
  in the scale `mel.rule_for` gives it and starting on one of its own notes; `check10.py` checks every group against the shape.
- `tango/tune_iw.py`: the chorus of I Wonder Who's Kissing Her Now as the 1909 song has it (a waltz in G, copied from the owner's
  score and moved to E♭); `check_tune.py` checks its bars, ties and the move to E♭. `tune_audio.py` makes a sound file of it to check by ear.
- `tango/entry11.py`: the rest of Graciano's chapter 7 on that tune: his ten paraphrase techniques and four of expression, a guide line
  against the tune, Grela's two lines in one, and an étude. Each change to the tune is made by one function per technique and logged;
  `check11.py` checks every logged change against the technique's rule with its own code. `build9.py` now builds the page from `entry11`.
- `tango/entry12.py`: Graciano's chapter 8, the guitar alone, on that tune: the tune on the top strings, over the plainest chord, over a
  bass line, with dressed-up chords, and an étude mixing them. `solo.py` fingers a tune with chords or a bass under it (one string per
  sounding note, the tune on top on the first three strings, the stretch and four fingers kept at every moment, the hand moving least);
  `check12.py` checks the fingering and each part's rule with its own code. `build12.py` builds the page.
- `tango/quotes.py`: cuts every quote of a book to its first two beats; each entry calls it last.
- `sola/`: Sola's five steps for colouring a song's chords, applied to Очи чёрные (it borrows `K` from `tango/entry.py`).
  Minor 11 chords need the `m11` quality in the song kit's chord table (`scripts/gtr.py`).
- `morel/`: Morel's dance patterns (malambo, samba, clave) on Очи чёрные and Я вас любил.
- `folk/`: the strummed patterns of Música folklórica argentina's rhythm table (bailecito, gato, zamba, cueca, carnavalito).
- `gypsy/`: Wrembel's accompaniment rhythms (la pompe, waltz, bolero, bossa-manouche) on Moonglow, Я вас любил and Очи чёрные.
- `flamenco/`: Graf-Martinez's arpeggio exercises I–IV (right hand kept, on Очи чёрные's open chords) and the five-note tremolo on Я вас любил's tremolo opening.
- `vaneps/`: Van Eps's scale in first-inversion triads, worked out for F major (string sets and positions chosen by least movement).
- `vaneps/entry2.py`: more of Van Eps's mechanisms (open triads in three spreads, triads through the cycle of fifths, two lines of triads in contrary
  motion) in E♭ and C harmonic minor, added to `entry.py`'s page; `check2.py` checks every voicing. `build.py` builds the page from `entry2`.
- `vaneps/entry4.py`: Van Eps's reductions (a held voice and a voice walking the scale between a 3rd and a 6th, four ways) in E♭;
  `check4.py` checks every interval. `build.py` now builds the page from `entry4`.
