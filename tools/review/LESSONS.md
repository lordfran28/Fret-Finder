# Lessons

Each mistake, why it happened, and the rule (and check) that prevents it. Newest first.

## 14 November 2026

- **I Wonder Who's Kissing Her Now, bars 26–27 (a wrong proposal, caught before it went in).** The review read Dean's held note as A against the B♭ of C minor 7 and proposed C minor 6. He sings B♭, a quarter tone flat, and B♭ is in the chord. *Why:* the review tool took the singer's tuning as the median of rounded fractions, which flips a note sung a quarter tone flat to the note below. *Rule:* the singer's tuning is a circular mean over steady frames, and any note that decides a change is measured again with it before the change. *Check:* `review.py` now does this.
- **Marble Halls, bars 34, 38, 78, 82.** The diagram showed E♭ over B♭, but the picking played only the B♭s and G, so the E♭ was never heard and the chord sounded like G minor over B♭. *Why:* the pattern was chosen to keep the E♭ above middle C away from the sung D, and dropped every E♭ with it. *Rule:* a pattern may leave notes of the grip out, but never the root or the 3rd; when one octave is in the way, use the other. *Check:* `review.py SLUG --sound` (“diagram's … not heard”).
- **How Deep Is the Ocean, compendium, “Replaced” for bars 13 and 29.** Their ▶ played nothing: the notes were written with string numbers (6 for the low E) where the page counts strings from 0. *Rule:* compendium sounds count strings from the low E, 0 to 5. *Check:* `review.py` (“cp sound”).
- **I Wonder Who's Kissing Her Now, Key Finder, bars 24 (both choruses).** The beginner rearrangement turned the song's F minor 6 into F minor 7, so the piano held E♭ a half step above Dean's D on "won-der if" for about four seconds. The guitar page already said an E♭ would rub there. *Why:* the beginner tool folds chords into one kind per root without asking what is sung over the new chord. *Rule:* when a chart is simplified, every chord that changes kind is checked against the held sung notes; a chord whose new tone sits a half step from one is kept as it was. *Check:* `review.py SLUG --voice --kf`.
- **I Wish You Love and What a Diff'rence a Day Made, Fret Finder.** The trumpet lines' "hear it" buttons pointed at the singer's track by its open name after that track went up locked, so they played nothing. *Why:* locking renamed the track in the track list but not in the trumpet part's pointer. *Rule:* when a track is locked, every name that points at it goes too; the trumpet buttons use the open full track. *Check:* `site_files.py` lists every file a page names that isn't in its folder.
- **How Deep Is the Ocean, bar 13.** A7♯9 put a C against Perry's C♯. *Why:* the chord was chosen for a note he doesn't sing, read from an earlier guess instead of his track. *Rule:* read the melody from the singer's own track, never from a MIDI file or a guess. *Check:* `review.py SLUG --voice`.
- **How Deep Is the Ocean, Intro 3.** F7♭9 at the 1st fret when the same chord sat next door at the 8th. *Rule:* choose each grip with the chords around it; jump only for a reason, such as a lower bass. *Check:* `review.py` jumps.

## 13 November 2026

- **How Deep Is the Ocean, bar 29.** A♭7♭13 was bent to fit Perry's blue note instead of the song's D♭ major 7. *Rule:* follow the song's harmony; a blue note sits over the real chord.
