# How an arrangement is made

20 November 2026. The owner called the four pages made that day (Ты мама, Город влюблённых людей, Maria, Я вас любил in E) terrible: no beauty, no likeness to the record, no fidelity. He was right. They were made by a program. It read a chord on every beat of the record, took a grip for each from a list, and put every note it heard from the piano onto some string. The only test was how close the guitar's overall harmony came to the record's. That number says nothing about whether a guitarist would play it, or whether it sounds good. None of the checks in CLAUDE.md had been run. This is the process that replaces it.

## What guitarists and arrangers say

- **Ted Greene**, *Voice-Leading* (lesson sheet, 1975, tedgreene.com): connect two chords by keeping the notes they share where they are and moving each other note to the nearest note of the next chord. When the bass moves by a step, move the upper voices the other way.
- **Tuck Andress**, as Julian Lage tells it (*Digging Deeper: Learning Tunes in Three Dimensions*, Premier Guitar): learn the tune and the bass first; they are the frame. Then add one inner voice, and make it a line of its own. Add a third voice only if it makes the harmony better.
- **Keyboard style** (*Piano Basics*, Baylor University open book, "Two-Hand Harmonization"): the bass alone below, three voices close together above, so they move smoothly. A pianist accompanying a singer mostly plays this way, and a guitar can.
- **Premier Guitar**, *A Walking Tour of Bass Lines*: over a moving bass, a little chord goes a long way.
- **PianoGroove**, *Accompaniment Basics: Melody, Harmony & Bass*: singers lean on hearing the bass on 1; under a singer, smooth voice leading.
- **guitar9**, on playing a piano part on guitar: copying the piano note for note often doesn't work; keep its feel. Arpeggiate, put in a few chord hits, and move up the neck to sit where the piano sits.

## The steps

1. **Read the record before writing a note.** For the instrument that carries the accompaniment, write a reduction bar by bar: where it strikes, its bass, its top note, the chord, and every run or fill where the voice rests. The separated track and the note readings help, but every bar is decided by hand. It is a new chord only if the bass, the other notes and the tune agree; a note that lasts a fraction of a beat is a passing note. Where the song repeats, read every repeat and keep what they agree on. Take the pulse and the bars from the music itself (the strikes, the tune, where phrases start), not from a beat tracker alone; a free intro or a two-beat bar stays free or short.
2. **Plan the guitar.** The key he asks for. Where each part sits on the neck. One grip per chord, chosen so that:
   - its lowest note is the record's bass (an octave lower is fine);
   - its top note is the record's top note, and where the piano doubles the tune, so does the guitar;
   - it keeps the notes it shares with the chord before it, so the hand moves only as far as the music does;
   - it is a closed grip around the 5th–6th fret unless the bass or the record puts it somewhere else; open strings only where they ring as part of the music;
   - it has the piano's number of voices, usually four or five, not a full barre.
3. **Play it the way the record's player plays it.** A chord where he strikes one, broken where he breaks it, held where he holds it, rolled from the bass up like a pianist's chord. Softer under the voice, fuller where it rests. His runs and fills go in note for note where the guitar can play them (an octave lower where the piano is too high) and show as numbered dots.
4. **Keep a bass.** Where the record drops its bass (the piano's left hand stops, the band leaves), the guitar still plays one, chosen to lead to the next chord.
5. **Pilot first.** A new song goes up first as its opening (intro, a verse, a chorus) beside the page it replaces, for the owner to hear. The rest follows when he says it is right.

## Before it goes up

`tools/arrange/checks.py` prints most of this; the rest is looking and listening.

- Every grip: four fingers at most (a barre counts as one), the stretch the hand allows at that height, one note per string, every struck string in the grip.
- Every chord is a change the record makes. No diagram is repeated. The diagram count is reported to the owner.
- The top note of every strike next to the tune and the record's top note.
- The bass of every strike next to the record's bass.
- How many of the guitar's strikes land on one of the record's (nearly all should), and which of the record's strikes are left out, and why.
- Any guitar note a semitone from the note he sings (an octave under the record) is listed, and kept only if the record has the same rub.
- A picture of the record's notes, the voice and the guitar together, looked at bar by bar.
- The guitar track rendered with the rolls and the loudness, then played against the record. The owner's ears decide.

## Tools

- `tools/arrange/solver.py`: every playable grip for a chord with a given bass and top note, the inner voices you want counted, ranked by how little the hand moves from the last grip.
- `tools/arrange/checks.py`: the checks above, for a page's track bars, the record's note readings and the voice's pitch.
