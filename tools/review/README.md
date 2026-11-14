# The night review

Working tools for the nightly check. Nothing here runs on the site, and the singer key they use stays in the session's scratchpad.

- `review.py SLUG [--voice] [--sound] [--kf]` goes through one song bar by bar: every grip against its chord name, one grip per chord, jumps across the neck when the same chord sits by the hand (a jump for a lower bass is fine), and with `--voice` every guitar note a half step or a minor 9th from a held sung note, plus every page line that says what he sings next to what the track says. `--sound` checks the guitar track against the diagrams. `--kf` does the same song on Key Finder. It needs the arranging kit in `/home/claude/kit`.
- `peek.py SLUG TRACK BAR,BAR` prints what the guitar track plays in those bars, note by note, next to the diagram.
- `site_pages.js`, `site_files.py` and `site_locks.mjs` are the site check: every page at 390 px, every track a playable file that the page names, every locked track opening with the key. They read copies of the live branches in the scratchpad, served by `serve.js`.
- `LESSONS.md`: every mistake, why it happened and the rule that prevents it.
- `log.json`: when each song was last reviewed, and what each night found.
