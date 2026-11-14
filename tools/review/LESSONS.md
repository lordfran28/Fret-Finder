# Lessons

Each mistake, why it happened, and the rule (and check) that prevents it. Newest first.

## 14 November 2026

- **I Wonder Who's Kissing Her Now, Key Finder, bars 24 (both choruses).** The beginner rearrangement turned the song's F minor 6 into F minor 7, so the piano held E♭ a half step above Dean's D on "won-der if" for about four seconds. The guitar page already said an E♭ would rub there. *Why:* the beginner tool folds chords into one kind per root without asking what is sung over the new chord. *Rule:* when a chart is simplified, every chord that changes kind is checked against the held sung notes; a chord whose new tone sits a half step from one is kept as it was. *Check:* `review.py SLUG --voice --kf`.
- **I Wish You Love and What a Diff'rence a Day Made, Fret Finder.** The trumpet lines' "hear it" buttons pointed at the singer's track by its open name after that track went up locked, so they played nothing. *Why:* locking renamed the track in the track list but not in the trumpet part's pointer. *Rule:* when a track is locked, every name that points at it goes too; the trumpet buttons use the open full track. *Check:* `site_files.py` lists every file a page names that isn't in its folder.
- **How Deep Is the Ocean, bar 13.** A7♯9 put a C against Perry's C♯. *Why:* the chord was chosen for a note he doesn't sing, read from an earlier guess instead of his track. *Rule:* read the melody from the singer's own track, never from a MIDI file or a guess. *Check:* `review.py SLUG --voice`.
- **How Deep Is the Ocean, Intro 3.** F7♭9 at the 1st fret when the same chord sat next door at the 8th. *Rule:* choose each grip with the chords around it; jump only for a reason, such as a lower bass. *Check:* `review.py` jumps.

## 13 November 2026

- **How Deep Is the Ocean, bar 29.** A♭7♭13 was bent to fit Perry's blue note instead of the song's D♭ major 7. *Rule:* follow the song's harmony; a blue note sits over the real chord.
