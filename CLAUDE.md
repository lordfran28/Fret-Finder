# Fret Finder: working instructions

Draft 2, 31 October 2026. The Orthodox and Unorthodox choice comes from the owner; the rest is still to be revised with him before it is treated as settled.

These are the standing instructions for anyone, person or Claude, changing this site. Read them before touching `index.html`.

## What the site is for

The owner sings and plays guitar at the same time. He feeds Fret Finder a song file and wants back a page he can play from: every bar in playing order, one diagram per hand position, notes numbered in the order they're played, the singing line with its chord changes over the words, and sound to check it by ear.

When a file is opened the player picks one of two ways to play it, and the code must always know which one it is doing.

1. **Orthodox.** Copy the piece exactly. This is what most people want most of the time, for example when transcribing a solo.
   - Nothing added, nothing simplified, nothing dropped without saying so.
   - It works for any instrument's part. A trumpet solo, a sax line or a piano melody comes out as guitar frets at the pitch it sounds; transposing parts such as B♭ trumpet are read through `<transpose>`.
   - Where the file gives strings (tab), keep them. Where it doesn't, finger it the way a good guitarist playing that piece would: if you watched the player on the recording, his hand would be where the diagram says.
   - Chord symbols with no written notes get a plain grip, nothing more.
2. **Unorthodox.** Improvise techniques into the piece, the way a player who knows many styles would.
   - The techniques come from books the owner provides: Jimmy Wyble's counterpoint, octaves, flamenco, Argentine folk with half triads moving up and down the neck, gypsy jazz triads and arpeggios, and others.
   - Each technique is written up in `techniques/` in our own words as rules the arranger can follow, with the book it came from. Book text is never copied onto the site.
   - The player can choose which techniques to allow.
   - The owner's arranging rules below still hold, above all "never stuffed".
   - This mode also covers turning a lead sheet, a piano and voice score or a band score into a guitar accompaniment for singing over.

Valve Finder and Fret Finder are connected: where a trumpet plays, its valve fingerings can show under the bar, and a trumpet part can be opened in Fret Finder to get the guitar frets.

## What "accurate" means

Each item below is a check that runs on every song in the test set. A change that breaks one is not finished. In Unorthodox mode, item 1 applies to the source's melody and harmony; added notes are allowed but must still pass items 2 to 6.

1. **Nothing lost.** Every note in the source appears in exactly one diagram, or is listed on the page as left out, with the reason.
2. **Right pitch.** Every diagram note, played on the string and fret shown, sounds the source pitch. Moving a note by an octave is allowed only with a note on the page saying so.
3. **Right time.** Onsets and lengths match the file after repeats, voltas, D.S., D.C., coda and fine are written out in playing order. Ties join. Grace notes come before the beat they lean on. Tuplets keep their proportions.
4. **Playable.**
   - One note per string at a time.
   - Four fingers at most, with a barre counting as one.
   - Stretches no wider than the hand allows at that height on the neck: four frets below the 5th fret, five from the 7th fret up.
   - A held note is never cut off by another note on its string unless the file leaves no other way, and then the page says so.
5. **Right names.**
   - Chord symbols in the file are shown as written.
   - Chords the site works out itself must be right for the usual set: triads, sixths, sevenths, half-diminished, diminished, suspended, ninths, elevenths, thirteenths, altered tones and slash bass.
   - Notes and chords are spelled for the key: B♭ in F major, not A♯.
6. **What you hear is what you see.** Playback plays the strings and frets in the diagrams, in that rhythm.

## The owner's rules for arranging and fingering

These come from his own corrections over many arrangements. They outrank anything an algorithm prefers.

**Layout**
- The full arrangement goes at the top, bar 1, bar 2 and on, in playing order, with no repeats or jumps left for the player to follow. Explanations and alternatives go at the bottom.
- The singing goes on top of each bar. Every chord change sits against the word it falls on.
- Runs, scales and octaves are shown as numbered dots in chord diagrams, not as tab.
- For each chord, show the main grip with a few other ways to play it right underneath (triads, inversions, wider stretches). Don't hide them behind a click.
- Describe positions plainly ("barre at the 5th fret, root on the 6th string"). Don't use CAGED names such as "E shape".

**Grips and positions**
- Prefer closed barre shapes around the 5th to 6th fret. Use open strings only where they clearly fit.
- Keep one grip per chord. Don't switch to a different voicing of the same chord at the same spot without a musical reason.
- Moving around the neck is good when it serves the music. Don't jump positions, add runs, or double notes just for their own sake.
- Put tremolo between the 5th and 10th frets.

**Arranging**
- Never stuffed. Add a scale, an octave, counterpoint or an extra chord only where it's truly beautiful.
- Never simplify. Don't drop or thin a part on the assumption it's too hard. Write the real part.
- It must be easy to play while singing. When two choices are equal, take the one with more notes or the nicer sound that's also easier to play.
- Follow the song's real chord changes. Keep the harmony sparse but good, and change a chord only for a reason.
- When reharmonizing, only where it still sounds like the song.

**Keys**
- Keep the key the owner asks for. Don't add a capo unless he asks.

## How work is done here

- **No build step.** The site is one page, `index.html`, plus assets. Keep it that way unless there's a strong reason.
- **Keep instructions off the site.** The page doesn't explain how it works internally. Page text is short and plain.
- **Run the checks before and after every change.** Use `node tools/check.mjs`, to be written in stage 1. A change that makes any song worse on any check is reverted or fixed before it's pushed.
- **Every bug gets a test.** Each bug fixed gets a small file in `tests/fixtures/` that would have caught it.
- **Golden songs need the owner's OK.** Songs in `tests/golden/` have an answer key: the fingerings and chord names the owner agreed are right. Changing an answer key needs his agreement.
- **Write commit messages for the player.** Say in plain words what changed for him, not which function moved.

## Where it stands (31 October 2026)

**Works**
- MusicXML: notes, chords, voices, ties, grace notes, chord symbols, lyrics, repeats, voltas and tab strings.
- MIDI, by bar.
- Guitar Pro 7 and 8.
- Fingering for the whole song by least hand movement.
- Diagrams with numbered dots and a rhythm line.
- Moving a note to another string.
- Chord grips for symbol-only bars.
- Playback from real guitar recordings.

**Known gaps**
- 8va and 8vb markings (`<octave-shift>`) are ignored.
- D.S., D.C., coda and fine are not written out.
- No finger numbers: the site says where, not with which finger.
- Barres are only drawn on chord-symbol grips.
- MIDI voices are not separated, and timing is only snapped to sixteenths and triplets.
- Guitar Pro 3 to 6 can't be read.
- Chord detection is a simple template match with no key awareness.
- Arranging is limited to chord grips.

## Plan, in order

Each stage ends when its checks pass on the whole test set.

1. **Checks and test set.**
   - `tools/check.mjs` runs every file in `tests/` through the real page in a headless browser and tests items 1 to 6 above.
   - Test set:
     - the public MusicXML test suite and Guitar Pro samples;
     - public-domain classical guitar studies whose printed editions mark strings, to measure fingering against;
     - the owner's own files and arrangements, as the golden songs.
2. **Reading everything.**
   - 8va and 8vb markings.
   - D.S., D.C., coda and fine.
   - Cross-staff notes; multiple verses of lyrics; chord symbols on any staff.
   - MIDI voice separation and better quantizing.
   - Guitar Pro 3 to 5.
3. **Fingering like a guitarist.**
   - Finger numbers for every note, and barres found and drawn.
   - Stretch limits that depend on where on the neck you are.
   - Slides and slurs kept on one string.
   - Position shifts on rests, long notes and phrase ends.
   - The same grip each time a chord comes back.
   - Target: agree with the printed fingering of the classical studies on at least 85% of notes.
4. **Harmony.**
   - Chords worked out beat by beat, with the key worked out too, and names spelled for the key.
   - Target: at least 95% agreement with the chord symbols in files that have them, with the symbols hidden.
5. **Unorthodox.**
   - Read the owner's books one at a time and write each technique up in `techniques/`.
   - Arranging for voice and guitar: lead sheet (grips, bass line and voice leading under the melody), piano and voice (the piano brought down to the guitar), band or orchestra (bass moves and instrument lines taken into the guitar where the voice rests).
   - Density rules so it's never stuffed.
   - Choices of arpeggio pattern and tremolo.
6. **The page.**
   - The Orthodox / Unorthodox choice when a file is opened.
   - Alternatives for every chord and run gathered at the bottom.
   - A printable version.
   - Trumpet valve fingerings under bars where a trumpet plays, from Valve Finder.
