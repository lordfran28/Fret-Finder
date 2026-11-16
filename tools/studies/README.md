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
- `tango/entry13.py`: Graciano's fills (chapter 3), rebuilt from his rules: one function per fill (the scale down or up, the pattern,
  the campanitas, tenths, octaves, sixths and thirds, the marcatto in inversions) applied to chords of Очи чёрные, I Wonder Who's Kissing
  Her Now and Я вас любил, two or three places each, and two études (the second on the 1909 chorus, fills where the voice holds). Only the
  first beat or two of his examples is kept, for the quotes. `check13.py` checks every fill against the rule with its own code. `build13.py`.
- `tango/entry14.py`: Graciano's cadences (chapter 4), rebuilt from his rules on entry13's helpers: the two-line links between sections
  (minor and major, both voicings), the ♭VI7, triads over an open-string pedal, four ways from I to the relative minor's dominant (a
  voice-leading search places each chord: the bass line his, the upper voices moving least), barres sliding from Im to V7, and the six
  endings, in the keys of Очи чёрные, I Wonder Who's Kissing Her Now, Я помню чудное мгновенье and Я вас любил. `check14.py` checks each rule.
- `tango/entry15.py`: Graciano's harmony (chapter 5), rebuilt from his rules on entry14's voicing search: the key's own chords from Im
  to IVm and to V7, Grela's pedal on top, the circle of 5ths (twice), tritone substitutes (the shared notes held), diminished chords for
  the dominant and their grips, the line cliché from the octave and from the 5th in every voice and way of playing it, and the tritone
  with its four replacements, resolutions, fingerings and uses, on Очи чёрные, I Wonder Who's Kissing Her Now and Я вас любил.
  `check15.py` checks each rule.
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
- `gypsy/manouche.py`: Wrembel's accompanist's chords (ch. 2): 6/9, minor 6, sevenths by where they go, minor 7♭5 as minor 6,
  diminished for 7♭9 and passing, the line clichés, the harmonic march, on Очи чёрные and Я вас любил in la pompe. The grips come
  from `voicing.py` (chord tones, no open strings, four frets, four fingers, the bass in reach, one grip per chord on the page);
  `check_manouche.py` checks every grip, every rule and the song bars against your pages. `build.py` builds the page from it.
- `gypsy/solo.py`: Gypsy Guitar: The Secrets (Roux, Daussat, Debarre), part two: rest strokes, the triplet stroke, sweeping, rolling
  (one note, chords, the tune), chromatics, artificial and natural harmonics, octaves, all on Очи чёрные (its chords from your page,
  Hermann's public-domain tune from `oci/music.py`); `check_solo.py`; `build_solo.py`. Run items may carry `{'trem': n}` (each note
  repeated n to a beat in the sound) and `{'harm': True}` (sounds an octave up) or `'nat'` (a natural harmonic at the pitch written).
- `gypsy/hand.py`: Wrembel's right-hand warm-up (ch. 1): the beat divided by 1 to 9 with his strokes, four beats on each string, on the
  bass of Очи чёрные (E7, Am, Dm on the open strings), the pivot 5-1-5-2-5-3-5-4 and the loops 2-3, 2-4, 2-5; `check_hand.py` compares
  the strokes with a table read from his pages and the chords with your Очи чёрные page; `build_hand.py` (46 a minute).
- `gypsy/romane.py`: L'Esprit Manouche (Romane and Derek Sébastian), part A of chapters 1–4: their fingerboard diagrams
  (minor and major triads in many forms, the diminished seventh, the harmonic minor in position and reaching over, the minor
  chord with a 6th or a 9th, speed on two strings, the chromatic scale with open strings), each moved one fret up on the same
  strings from their A minor into It Had to Be You's B♭ minor; `check_romane.py` reads their diagrams again as notes on strings,
  checks ours is theirs moved up a fret, every note against its chord, the rhythm, the names, the fingers and the song bars
  the text names (from your page); `build_romane.py` (100 a minute). Needs `m(add9)` in `scripts/gtr.py`.
- `page/template_study.html`: note lengths of a seventh or a ninth of a beat are written 1/7 and 1/9.
- `flamenco/`: Graf-Martinez's arpeggio exercises I–IV (right hand kept, on Очи чёрные's open chords) and the five-note tremolo on Я вас любил's tremolo opening.
- `flamenco/serrano_arp.py`: Serrano's four arpeggio exercises (pp. 46–48) over Очи чёрные's changes with the root on the low E
  string, added to the flamenco right-hand page; `check_arp.py` compares every note with his patterns read from his tablature.
  `build.py` builds that page from it. A section can carry its own quote mark (`mark`), numbered from 1.
- `flamenco/rasgueado.py`: Serrano's rasgueado (Basic Techniques pp. 21–29): the preparatory study, three exercises and five
  studies, his strokes and fingers on Очи чёрные's chords; `check_ras.py` compares every stroke with his bars as transcribed and
  the chords with your Очи чёрные page; `build_ras.py`. Rhythm items may now carry `{'up': [...], 'marks': [...]}`: upstrokes in the
  sound, and a finger and arrow under each strum in the tab (`study_page.py`, `page/template_study.html`).
- `vaneps/`: Van Eps's scale in first-inversion triads, worked out for F major (string sets and positions chosen by least movement).
- `vaneps/entry2.py`: more of Van Eps's mechanisms (open triads in three spreads, triads through the cycle of fifths, two lines of triads in contrary
  motion) in E♭ and C harmonic minor, added to `entry.py`'s page; `check2.py` checks every voicing. `build.py` builds the page from `entry2`.
- `vaneps/entry4.py`: Van Eps's reductions (a held voice and a voice walking the scale between a 3rd and a 6th, four ways) in E♭;
  `check4.py` checks every interval. `entry3.py`: super and sub (a voice moved a step from the triad and back), `check3.py`.
- `vaneps/entry5.py`: Van Eps's chromatics: major triads climbing by half steps over G (Я вас любил) and minor over A (Очи чёрные), each
  inversion, the pedal moving only when the triad leaves the hand; chromatic scales in octaves, 10ths, 12ths, 13ths and two octaves;
  the 10th to the 3rd over a held bass (one hand position the whole time). `check5.py` works every note out again from the exercise's
  definition and checks names, strings and reach; page numbers are the printed ones.
- `vaneps/entry6.py`: the melodic minor in first- and second-inversion triads in A (up melodic, down natural, as Van Eps does),
  placed after the other scales in triads; `check6.py`. `build.py` now builds the page from `entry6`.
- `study_page.py`: a two-voice item may carry `{'hold': [strings]}` (those notes ring until struck again, the rest stop at their own
  end); pages longer than five minutes are rendered in pieces and added up.
