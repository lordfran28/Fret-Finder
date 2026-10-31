# Fret Finder

Valve Finder's sister site, for the guitar. Give it a MusicXML, MIDI or Guitar Pro file and it lays the song out bar by bar in playing order: one diagram for each hand position, the notes numbered in the order you play them, the rest of the chord in pale rings, a rhythm line under each diagram, and the singing line with its chord changes on top of every bar.

Live at **https://lordfran28.github.io/fret-finder/** once GitHub Pages is on (Settings → Pages → Deploy from a branch → `main`, `/ (root)`).

## Songs

Songs are files in the `songs` folder, the same way as on Valve Finder. Add them from the site on a connected device, or put them in the folder and push. See `songs/README.md`.

To change songs from the site, open the owner page (`#owner`) and connect the device with a GitHub key that has *Contents: Read and write* on this repository. A Valve Finder key won't work here unless fret-finder is added to it.

## How a song is read

- **MusicXML** is the best source. If the file has tab (string and fret for each note), those strings are kept. Chord symbols, lyrics, repeats and voltas are read.
- **MIDI** works too; bars come from the file's time signature.
- **Guitar Pro 7 and 8** (`.gp`) files open directly. For older Guitar Pro files, export MusicXML from Guitar Pro.

When there's no tab, Fret Finder works out a fingering for the whole song at once: as little hand movement as it can, small shapes, held notes left ringing, and closed shapes around the 5th fret when they're no harder. Tap any note to hear it or put it on another string; the rest of the song is refingered around it and the choice is saved with the song.

Under Settings each part of the file can be the guitar, the singing line, or off, so a piano part, a band arrangement or a lead sheet can all be turned into guitar. Bars with only a chord symbol get a grip for that chord. Tuning, capo and octave can be changed there too.

## Credits

- Johannes Vermeer, *The Guitar Player* (c. 1672), Kenwood House. Public domain.
- Venetian or Genoese silk damask, 17th century, The Metropolitan Museum of Art (216471), open access, recoloured.
- Behind the songs, drawn faintly from public-domain paintings: Dirck van Baburen, Hendrick ter Brugghen, Frans Hals, Gerard van Honthorst, Caspar Netscher, Antoine Watteau, Caravaggio, Judith Leyster, Jan van Bronckhorst, the Master of the Annunciation to the Shepherds, Federico Andreotti, Alessandro Sani, and three 19th-century lute players by unknown painters.
- Guitar recordings: University of Iowa Electronic Music Studios, Musical Instrument Samples (guitar, mf), cut into one file per string and fret.
- EB Garamond and IM Fell French Canon (SIL Open Font License). QR codes by qrcode-generator (MIT).
