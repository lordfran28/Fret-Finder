# Fret Finder: working instructions

Draft 2, 31 October 2026. The Orthodox and Unorthodox choice comes from the owner; the rest is still to be revised with him before it is treated as settled.

These are the standing instructions for anyone, person or Claude, changing this site. Read them before touching `index.html`.

## Since 31 October 2026: the shelf

The owner decided the automatic transcription can't produce diagrams a guitarist can play from, so the site's main job is now a **shelf for the arrangements made in conversation with Claude**. The transcription engine below stays in the code but is not the focus.

- Each arrangement is a folder `songs/<slug>/` holding the arrangement page (`index.html`), the audio it uses, and `song.json` (title, instrument, date, source artifact).
- Put one there with `python3 tools/import_arrangement.py PAGE.html SLUG "Title" --file NAME=PATH ... [--locked NAME.mp3.locked=PATH ...] [--drop-alt]`. It adds Fret Finder's look (`assets/shelf.css`, which only sets the page's colour and type variables), a link back to the songs, and `assets/ring.js`, which lights each diagram dot gold as its note sounds in the track and makes the fret number beside every diagram huge.
- The site is public. Never put a record's own audio (a vocal mix, a stem) or copyrighted lyrics on it in the open; `--drop-alt` removes a page's second audio track. Pages for songs still under copyright need their lyrics taken out, or a private way to serve them, before they go up.
- **The singer's track goes up locked.** The owner wants every song that had a track with the singer on its artifact to have it on the shelf too, now and for every new song. Add it to the page's track list under the name `NAME.mp3.locked` (after the open tracks, never first) and pass `--locked NAME.mp3.locked=PATH`. `tools/lock_voice.mjs` encrypts it to the public key in `assets/voice-key.json`; `assets/voice.js` plays it on devices where the owner entered the singer key on the owner page (`#owner`), and hides its button everywhere else. The private half of the key is never in this repository or in any page.
- **Locked copies.** Where the faithful version of a page holds music still under copyright (a tune's own phrase in a run, say), that version goes up as a locked copy beside the open page: the open page stays as it is for everyone, and on a device with the singer key `assets/locked-page.js` goes to `real.html`, a stub that opens `real.html.locked` (the whole page, encrypted with `tools/lock_voice.mjs`) and writes it in. Its tracks are locked too. The open page names the copy with `<meta name="ff-locked-copy" content="real.html">` after `voice.js`. First used on Don't Get Around Much Anymore (Ellington's opening phrase as the intro's run).
- **Slower tracks.** `assets/speed.js` puts a row of speeds (100% down to 50%) inside every track player on a song page. The pitch stays the same, the lighting follows the slower track, and each song remembers its own speed on the device (`ff.speed:` + the page's path). The import tool adds it to every page; it is separate from the page's own 100/75/50 buttons, which only slow the short play-this-bar sounds.
- **Other grips.** `assets/grips.js` puts arrows under each chord diagram of a song page's arrangement. They step through the same notes elsewhere on the neck (nearest to the chords around it first), then the other chords the page's compendium lists for that bar. The new grip is drawn in place and sounded, and the choice is kept on the device (`ff.grip:` + the page's path). The import tool adds it to every page.
- **8 strings** (since 22 November 2026). Every song page has a checkbox, "8 strings" (`assets/eight.js`, added by the import tool). Ticked, it holds for every song on the device (`ff.eight`), and a song with an 8-string version opens `eight.html` beside its `index.html` (metas `ff-eight` and `ff-six`). The guitar is tuned A1 B1 E2 A2 D3 G3 B3 E4, low to high; strings keep their numbers (1 the high E, 7 the low B, 8 the low A). A song may retune the 7th or 8th string where that helps it a lot, and says so at the top. `tools/eight.py` widens a page's grips to eight strings and patches its code to draw them; the arrangement stays as it is and the two low strings add only what serves it (the record's bass at its own octave, low basses that ring, a line against the 6th-string bass, walking). Its tracks are NAME-8.mp3 and NAME-8.mp3.locked. The checkbox's picture is a real photo or drawing (`assets/eight-headstock.jpg`), never one we draw. Contemporary songs first; the classical pieces later.
- `.github/scripts/song_index.py` lists every such folder in `songs/index.json`; the library links straight to the page.
- The library lists only these arrangements, A to Z, and has no way to add a song. Songs transcribed on a device before the shelf are cleared from it when the library opens.
- Titles of classical pieces start with the composer: "Bach – Prelude and Fugue, BWV 867".
- Before a page goes up, take out anything copyrighted: a record's vocal or stem in the open (also as a track choice in the page's data; locked is fine), the sung melody of a song under copyright (including the compendium's "you sing" notes), and the owner's own recordings of other people's records (those can go up locked too). Earlier-version iframes go too unless each one is checked.

## Exercises (since 16 November 2026)

Below the songs, the library lists **Exercises**: long entries built from the guitar books the owner owns, one entry per style (Jimmy Wyble, Van Eps, tango, Argentine folk, classical warm-ups, octaves, gypsy jazz, flamenco, Sola's harmony).

- Each entry is a folder `studies/<slug>/` with the page (`index.html`), its audio and `entry.json` (title, style, files, date). Put one there with `python3 tools/import_study.py PAGE.html SLUG "Title" --style "Jimmy Wyble" --file NAME=PATH`; it adds the shelf look, `ring.js` and `speed.js`. `.github/scripts/study_index.py` writes `studies/index.json` (the *Exercise list* workflow runs it on every push that touches `studies/`).
- An entry opens with its own **Contents**: every exercise, étude and piece on the page, linked. Then straight exercises, then études, then pieces. The contents describe the entry, not the books.
- **The books stay off the site.** Each exercise is ours, set on the chords of one of the owner's songs. Next to it goes a short quote of the original's opening figure (a beat or two, never the whole exercise), a plain description of what the original does, and its page in the owner's copy. Public-domain works (Carcassi, Sor's notes, Broca) may go up complete, with our own fingerings where an edition's are someone else's.
- The pages are built in `/home/claude/studies/` (`study_page.py`, one folder per entry) on a copy of the song template in which a two-line step may hold one note or two.

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

How an arrangement is made, step by step, and the checks it must pass before it goes up: `ARRANGING.md` (20 November 2026, after he rejected four pages made by a program).

**Layout**
- The full arrangement goes at the top, bar 1, bar 2 and on, in playing order, with no repeats or jumps left for the player to follow. Explanations and alternatives go at the bottom.
- The singing goes on top of each bar. Every chord change sits against the word it falls on.
- Runs, scales and octaves are shown as numbered dots in chord diagrams, not as tab. Nothing else gets numbers: other dots are plain and light up in order as they're played.
- A diagram means a change, so never repeat one. A grip or run that keeps going gets one diagram: the bars after it show none (its dots keep lighting in that one), and the same tab isn't printed again. A grip that comes back after a different one is drawn again in full; never replace it with a name like "back to A". Each part opens with its own diagrams. A three-chord song should come to a few dozen diagrams, not one per bar.
- No rhythm line under the diagrams.
- The fret number beside a diagram is large; it matters.
- For each chord, show the main grip with a few other ways to play it right underneath (triads, inversions, wider stretches). Don't hide them behind a click.
- Describe positions plainly ("barre at the 5th fret, root on the 6th string"). Don't use CAGED names such as "E shape".

**Grips and positions**
- Prefer closed barre shapes around the 5th to 6th fret. Use open strings only where they clearly fit.
- Keep one grip per chord. Don't switch to a different voicing of the same chord at the same spot without a musical reason.
- Moving around the neck is good when it serves the music. Don't jump positions, add runs, or double notes just for their own sake.
- Put tremolo between the 5th and 10th frets.

**Arranging**
- Never stuffed. Add a scale, an octave, counterpoint or an extra chord only where it's truly beautiful.
- The record's orchestration (keyboards, synths, strings, horns) goes into the guitar for the whole song, under the singing too, not only where the voice rests: inner lines, octaves, counterpoint, tremolo, harmonics, the record's chord colours. Still never stuffed, and always playable while singing.
- He always plays alone, so the bass never drops out: in an instrumental, keep it going under the line (on 1 and 3 at least), and runs or variations that stand in for a riff keep the riff's bass and its rhythm.
- Where the record's bass does something (a walk, a run, a moving line, a push into the next chord), the guitar plays it too. That is mostly in the verses, under the singing, and above all in the Rod Stewart arrangements; it isn't hard on the guitar. It is not a matter of inventing a walking bass where he rests: follow the record's bass, and play plain roots only where the record does. His rule, 18 November 2026.
- Never simplify. Don't drop or thin a part on the assumption it's too hard. Write the real part.
- Never stilted or robotic. The guitar imitates the record's piano, or whatever instrument carries the record's accompaniment, hit by hit: its rhythm (pushes, held chords, rests), its voicings as far as the grip reaches, its top line, its run-ups and fills where the voice rests. It plays less under the voice and more in the gaps, with the record's dynamics. One broken-chord figure repeated in every bar is wrong, and old arrangements get the same treatment when they are revised. His rule, 19 November 2026.
- When the record's accompaniment is itself a guitar, play what that guitarist plays: his intro, his voicings in his positions, his broken chords and runs, note by note from the record, with the bass added where he plays alone. Never trade a guitarist's own part for a simpler one. The faithful version is the record's arrangement, so it goes up as the locked copy. His rule, 18 November 2026 (It Was Almost Like a Song).
- The high version is the main arrangement (the beautiful arpeggios). Every high progression also carries its low version as `bar.low`, shown second in the arrows under its diagrams as "Low option", switching the whole progression at once. His rule, 20 November 2026.
- Play the bass: every now and again, where he holds or rests, three to five quick notes on the bass strings into the next chord's bass, and under the singing a bass that moves by step; never every bar, never instead of the high arrangement. Built from `techniques/bass.md` (the books), not by copying one player. His rule, 20 November 2026.
- Where a song falls by a descending bass and then lifts to a major chord, he wants the fall milked: suspensions hanging over each new bass note, inner lines, counterpoint, every step held back before it resolves. His words, 18 November 2026: "take your time and make beautiful arrangements with wonderful progressions."
- When a record has a trumpet, its lines go on the song page note for note with exact valve fingerings (the trumpet section at the bottom), locked whenever they are under copyright. His rule, 18 November 2026, for every song.
- It must be easy to play while singing. When two choices are equal, take the one with more notes or the nicer sound that's also easier to play.
- Follow the song's real chord changes. Keep the harmony sparse but good, and change a chord only for a reason.
- When reharmonizing, only where it still sounds like the song.

**Keys**
- Keep the key the owner asks for. Don't add a capo unless he asks.
- When he names no key, he likes a deep baritone range, like Dick Haymes's (starting low, around B♭2, the top around D4 or E♭4); never at the cost of the harmony or a beautiful arrangement.

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
- Other parts added to the guitar: tick a part (flute, piano, voice) and each bar gets a second row where its notes are red rings fitted around what the guitar plays, moving the guitar only where that's the only way to fit them. Play includes them.
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
