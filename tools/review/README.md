# The night review

Working tools for the nightly check. Nothing here runs on the site, and the singer key they use stays in the session's scratchpad.

- `review.py SLUG [--voice] [--sound] [--kf]` goes through one song bar by bar: every grip against its chord name, one grip per chord, jumps across the neck when the same chord sits by the hand (a jump for a lower bass is fine), a picking pattern that never sounds the chord's root or 3rd (its 7th is listed apart), a bar note that names a fret no grip of the bar is at, and with `--voice` every guitar note a half step or a minor 9th from a held sung note, plus every page line that says what he sings next to what the track says. `--sound` checks the guitar track against the diagrams: notes it plays that they don't have, their notes it never plays (the root and the 3rd by their own pitch), and every note of a run or line at its time. It reads the older pages too (Barquito de papel), which keep only grips and bar times; where the singer's track also has the trumpet, take the guitar and trumpet out first and put the voice in the scratchpad's `night/rv_SLUG/KEY-voc.wav`. `--kf` does the same song on Key Finder. It needs the arranging kit in `/home/claude/kit`.
- `peek.py SLUG TRACK BAR,BAR` prints what the guitar track plays in those bars, note by note, next to the diagram.
- `site_pages.js`, `site_files.py` and `site_locks.mjs` are the site check: every page at 390 px, every track a playable file that the page names, every locked track opening with the key. They read copies of the live branches in the scratchpad, served by `serve.js`.
- `build_rings.py BUILD_DIR` runs a song's build without rendering and lists every note still ringing when its string is played again (two notes on one string at once). The kit's renderer now stops them, so this is for tracks made before 17 November.
- `instr.py` lists every stretch of two bars or more where the voice rests, with how often the guitar strikes and every bar with no bass on beat 1 or 3 (the owner, 17 November: an instrumental always carries a bass line, on 1 and 3 at least, never stiff or empty).
- `site_mix.py` checks that every singer's track holds the same take as the plain guitar (or piano) track it goes with, so he never hears other chords under the singer than the diagrams show.
- `LESSONS.md`: every mistake, why it happened and the rule that prevents it.
- `log.json`: when each song was last reviewed, and what each night found.

## Without the singer key (since 23 November)

The singer's tracks stay locked during the review: nothing here opens them. The sung line comes from the record instead, from the vocal stem he sent or one separated in the scratchpad (Kim_Vocal_2), and the band's notes from the instrumental. The tools in `nokey/` need `/home/claude/cp` (cplib) and work on the live pages:

- `align.py GUITAR RECORD`: how many half steps the record sits above the page and the time offset between them, by chroma.
- `vc.py SLUG STEM [SEMI OFF]`: the sung line by pyin (cached in `/tmp/night`), the page's sung line (from its Valve Finder part) against it, and every guitar note a half step or a minor 9th from a note he holds half a second or more, with ring time.
- `rv.py SLUG [TRACK]`: every grip against its chord name, chords with more than one grip, a pattern that never strikes the root or the 3rd, rubs against the Valve Finder line, and the track's notes against the diagrams.
- `band.py SLUG INSTRUMENTAL SEMI OFF BAR:B0-B1 ...`: the band's pitch classes in those beats, to tell whether the record has the same rub.
- `altg.py SLUG SEMI OFF`: for a chord with several grips, where each is used and whether the main grip would rub there.
- `vline2.py SLUG A B STEP SEMI`: the sung pitch every STEP seconds.
