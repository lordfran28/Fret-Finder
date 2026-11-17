"""A small reader for the LilyPond the Mutopia guitar scores use: notes with their onsets and lengths, voice by
voice, ties joined, repeats written out, grace notes left out (listed). Enough for Sor, Carcassi, Giuliani, Aguado.
parse(path) -> dict(time=(n, d), partial=beats or 0, voices={name: [(onset, dur, [midis], tied_from_prev)]},
                    notes=[(onset, dur, midi, voice)], length=whole notes)"""
import re
from fractions import Fraction as Fr

STEP = {'c': 0, 'd': 2, 'e': 4, 'f': 5, 'g': 7, 'a': 9, 'b': 11}
LET = 'cdefgab'


def strip_comments(s):
    s = re.sub(r'%\{.*?%\}', ' ', s, flags=re.S)
    return re.sub(r'%[^\n]*', ' ', s)


TOKEN = re.compile(r'''
   (?P<str>\#?"(?:[^"\\]|\\.)*")
 | (?P<scheme>\#'?\(  )
 | (?P<hash>\#[^\s{}()<>]*)
 | (?P<open><<|\{)
 | (?P<close>>>|\})
 | (?P<chordopen><(?![<]))
 | (?P<chordclose>>(?!>))
 | (?P<voicesep>\\\\)
 | (?P<cmd>\\[A-Za-z][A-Za-z_\-]*|\\[()\[\]<>!~^_.+\-]|\\\d+)
 | (?P<note>(?:[a-g](?:isis|eses|is|es|s)?|[r]|[sR]|q)(?![A-Za-z])[',]*[!?=]?[',]*(?:\d+|\\breve)?\.*(?:\*\d+(?:/\d+)?)*)
 | (?P<frac>\d+/\d+(?![\d.*]))
 | (?P<dur>(?:\d+|\\breve)\.*(?:\*\d+(?:/\d+)?)*)
 | (?P<tie>~)
 | (?P<word>[A-Za-z][A-Za-z_\-]*)
 | (?P<eq>=)
 | (?P<num>-?\d+(?:/\d+)?)
 | (?P<other>.)
''', re.X | re.S)


def tokens(s):
    out = []
    for m in TOKEN.finditer(s):
        k = m.lastgroup; v = m.group()
        if k == 'other' and v.isspace(): continue
        if k == 'scheme':            # skip a scheme expression with balanced parentheses
            depth, i = 0, m.start() + v.index('(')
            j = i
            while j < len(s):
                if s[j] == '(': depth += 1
                elif s[j] == ')':
                    depth -= 1
                    if depth == 0: break
                j += 1
            out.append(('skipto', j + 1)); continue
        out.append((k, v, m.start(), m.end()))
    return out


def tokenize(s):
    """tokens, skipping scheme expressions properly"""
    toks, pos = [], 0
    while pos < len(s):
        m = TOKEN.match(s, pos)
        if not m: pos += 1; continue
        k, v = m.lastgroup, m.group()
        if k == 'other' and v.isspace(): pos = m.end(); continue
        if k == 'scheme':
            depth, j = 0, s.index('(', m.start())
            while j < len(s):
                if s[j] == '(': depth += 1
                elif s[j] == ')':
                    depth -= 1
                    if depth == 0: break
                j += 1
            pos = j + 1; continue
        toks.append((k, v)); pos = m.end()
    return toks


def pitch_of(name):
    """'cis' -> (letter index, semitone offset from natural)"""
    l = name[0]; acc = name[1:]
    alt = {'': 0, 'is': 1, 'isis': 2, 'es': -1, 's': -1, 'eses': -2}[acc]
    return LET.index(l), STEP[l] + alt


DUR_RE = re.compile(r'(\d+|\\breve)(\.*)((?:\*\d+(?:/\d+)?)*)')


def dur_of(txt):
    m = DUR_RE.fullmatch(txt)
    if not m: return None
    base = Fr(2) if m.group(1) == '\\breve' else Fr(1, int(m.group(1)))
    d = base; add = base
    for _ in m.group(2): add /= 2; d += add
    for mul in re.findall(r'\*(\d+)(?:/(\d+))?', m.group(3)):
        d *= Fr(int(mul[0]), int(mul[1]) if mul[1] else 1)
    return d


class Music:
    def __init__(self, toks, defs):
        self.t = toks; self.i = 0; self.defs = defs
        self.graces = 0

    def peek(self, k=0): return self.t[self.i + k] if self.i + k < len(self.t) else (None, None)

    def next(self):
        x = self.t[self.i]; self.i += 1; return x

    def skip_arg(self):
        """skip one argument: a {..} block, a string, a word, a number, a #thing"""
        k, v = self.peek()
        if k == 'open':
            depth = 0
            while True:
                k2, v2 = self.next()
                if k2 == 'open': depth += 1
                elif k2 == 'close':
                    depth -= 1
                    if depth == 0: return
        else:
            self.next()


SKIP0 = {'\\voiceOne', '\\voiceTwo', '\\voiceThree', '\\voiceFour', '\\oneVoice', '\\stemUp', '\\stemDown', '\\stemNeutral',
         '\\tieUp', '\\tieDown', '\\tieNeutral', '\\slurUp', '\\slurDown', '\\slurNeutral', '\\break', '\\noBreak', '\\pageBreak',
         '\\(', '\\)', '\\[', '\\]', '\\<', '\\>', '\\!', '\\fermata', '\\staccato', '\\tenuto', '\\accent', '\\arpeggio',
         '\\p', '\\pp', '\\ppp', '\\f', '\\ff', '\\fff', '\\mf', '\\mp', '\\sf', '\\sfz', '\\fz', '\\rfz', '\\cresc', '\\dim',
         '\\decresc', '\\espressivo', '\\trill', '\\prall', '\\mordent', '\\turn', '\\harmonic', '\\glissando', '\\laissezVibrer',
         '\\portato', '\\marcato', '\\upbow', '\\downbow', '\\flageolet', '\\stopped', '\\open', '\\shortfermata', '\\longfermata',
         '\\sustainOn', '\\sustainOff', '\\startTrillSpan', '\\stopTrillSpan', '\\startTextSpan', '\\stopTextSpan', '\\slurDashed',
         '\\slurSolid', '\\tieDashed', '\\tieSolid', '\\autoBeamOff', '\\autoBeamOn', '\\cadenzaOn', '\\cadenzaOff', '\\default',
         '\\mbreak', '\\pbreak', '\\-', '\\.', '\\^', '\\_', '\\+', '\\~', '\\dynamicUp', '\\dynamicDown', '\\textLengthOn',
         '\\textLengthOff', '\\mergeDifferentlyDottedOn', '\\mergeDifferentlyHeadedOn', '\\shiftOn', '\\shiftOff', '\\shiftOnn',
         '\\arpeggioArrowUp', '\\arpeggioNormal', '\\sostenutoOn', '\\sostenutoOff', '\\segno', '\\coda', '\\breathe',
         '\\startGroup', '\\stopGroup', '\\pp', '\\prallprall', '\\upprall', '\\reverseturn', '\\thumb', '\\segnoMark',
         '\\fine', '\\stemDown', '\\noBeam', '\\melisma', '\\melismaEnd', '\\hideNotes', '\\unHideNotes', '\\showStaffSwitch',
         '\\hideStaffSwitch', '\\voiceOneStyle', '\\voiceTwoStyle', '\\stopStaff', '\\startStaff', '\\oneVoice'}
SKIP1 = {'\\clef', '\\bar', '\\mark', '\\tempo', '\\override', '\\revert', '\\set', '\\unset', '\\once', '\\markup',
         '\\label', '\\tweak', '\\instrumentSwitch', '\\ottava', '\\finger', '\\rightHandFinger', '\\textMark', '\\sectionLabel',
         '\\barNumberCheck', '\\footnote', '\\omit', '\\hide', '\\undo', '\\temporary', '\\shape', '\\offset', '\\keepWithTag',
         '\\removeWithTag', '\\tag', '\\mergeDifferentlyDottedOff', '\\parenthesize'}


class Reader:
    def __init__(self, src):
        self.src = strip_comments(src)
        self.toks = tokenize(self.src)
        self.defs = {}
        self.time = (4, 4); self.partial = Fr(0); self.graces = []; self.voltas = []; self.checks = []
        self._defs()
        for k_, v_ in enumerate(self.toks):
            if v_ == ('cmd', '\\time') and k_ + 1 < len(self.toks) and self.toks[k_ + 1][0] == 'frac':
                n_, d_ = self.toks[k_ + 1][1].split('/'); self.time = (int(n_), int(d_)); break

    def _defs(self):
        t = self.toks; i = 0; depth = 0
        while i < len(t) - 2:
            if t[i][0] == 'open': depth += 1; i += 1; continue
            if t[i][0] == 'close': depth -= 1; i += 1; continue
            if depth == 0 and t[i][0] == 'word' and t[i + 1][0] == 'eq':
                name = t[i][1]; j = i + 2
                # take the expression: optional \relative x / \fixed x / \transpose a b, then a block
                start = j
                if t[j][0] in ('cmd', 'str', 'hash', 'num', 'dur', 'word', 'frac') and t[j][1] not in ('\\relative', '\\fixed', '\\transpose', '\\absolute', '\\new', '\\context', '\\simultaneous', '\\sequential', '\\markup', '\\with'):
                    self.defs[name] = t[j:j + 1]; i = j + 1; continue
                while j < len(t) and t[j][0] != 'open': j += 1
                if j >= len(t): break
                depth = 0; k = j
                while k < len(t):
                    if t[k][0] == 'open': depth += 1
                    elif t[k][0] == 'close':
                        depth -= 1
                        if depth == 0: break
                    k += 1
                self.defs[name] = t[start:k + 1]
                i = k + 1
            else:
                i += 1

    # ---------- music
    def run(self, toks, mode=('abs', None)):
        """-> list of events (onset, dur, [midis], tie_start) for one voice; voices from << \\ >> come back as extra."""
        self.voices = {}
        st = dict(t=Fr(0), dur=Fr(1, 4), mode=mode, last=None, lastchord=None, scale=Fr(1))
        ev = []
        self._seq(toks, 0, len(toks), st, ev, 'v')
        return ev

    def _ref_octave(self, txt):
        """'c'' -> midi of that pitch in absolute terms"""
        m = re.fullmatch(r"([a-g](?:isis|eses|is|es|s)?)([',]*)", txt)
        li, semi = pitch_of(m.group(1))
        o = 3 + m.group(2).count("'") - m.group(2).count(',')
        return (li, o)

    def _note(self, txt, st):
        """parse a note token -> (midi or None for rest, duration, is_skip)"""
        m = re.fullmatch(r"((?:[a-g](?:isis|eses|is|es|s)?)|r|s|R|q)([',]*)([!?=]?)([',]*)((?:\d+|\\breve)?\.*(?:\*\d+(?:/\d+)?)*)", txt)
        name, oct1, mark, oct2, d = m.groups()
        octs = oct1 + oct2 if mark != '=' else ''
        if d:
            dd = dur_of(d)
            if dd is not None: st['dur'] = dd
        dur = st['dur'] * st['scale']
        if name in ('r', 's', 'R'): return None, dur, name
        if name == 'q': return 'q', dur, 'q'
        li, semi = pitch_of(name)
        up, down = octs.count("'"), octs.count(',')
        kind, ref = st['mode']
        if kind == 'abs':
            o = 3 + up - down
        elif kind == 'fixed':
            o = ref[1] + up - down
        else:  # relative
            pl, po = st['last'] if st['last'] else ref
            # choose octave so that the letter distance is <= 3
            best = None
            for o in (po - 1, po, po + 1):
                dist = (o * 7 + li) - (po * 7 + pl)
                if abs(dist) <= 3: best = o; break
            o = best + up - down
            if mark == '=':
                o = 3 + oct2.count("'") - oct2.count(',')  # octave check: absolute
            st['last'] = (li, o)
        midi = 12 * (o + 1) + semi
        if kind == 'abs' or kind == 'fixed':
            pass
        return midi, dur, 'n'

    def _block_end(self, toks, i):
        depth = 0; j = i
        while j < len(toks):
            if toks[j][0] == 'open': depth += 1
            elif toks[j][0] == 'close':
                depth -= 1
                if depth == 0: return j
            j += 1
        raise ValueError('unbalanced')

    def _seq(self, toks, a, b, st, ev, vname):
        i = a
        while i < b:
            k, v = toks[i]
            if k == 'open' and v == '{':
                j = self._block_end(toks, i)
                self._seq(toks, i + 1, j, st, ev, vname); i = j + 1; continue
            if k == 'open' and v == '<<':
                j = self._block_end(toks, i)
                self._simul(toks, i + 1, j, st, ev, vname); i = j + 1; continue
            if k == 'close': i += 1; continue
            if k == 'chordopen':
                j = i + 1; ms = []; saved = st['last']; first = None
                while toks[j][0] != 'chordclose':
                    if toks[j][0] == 'note':
                        midi, _, _ = self._note(toks[j][1], st)
                        ms.append(midi)
                        if first is None: first = st['last']
                    j += 1
                # duration after the chord
                j += 1; d = None
                if j < b and toks[j][0] == 'dur':
                    d = dur_of(toks[j][1]); j += 1
                if d is not None: st['dur'] = d
                if st['mode'][0] == 'rel' and first: st['last'] = first
                dur = st['dur'] * st['scale']
                tie = j < b and toks[j][0] == 'tie'
                ev.append([st['t'], dur, ms, tie]); st['lastchord'] = ms; st['t'] += dur
                i = j + (1 if tie else 0); continue
            if k == 'note':
                midi, dur, kind = self._note(v, st)
                j = i + 1
                # a pitched rest: "f4\rest"
                if j < b and toks[j] == ('cmd', '\\rest'): midi = None; j += 1
                tie = False
                if j < b and toks[j][0] == 'tie': tie = True; j += 1
                if midi == 'q': ev.append([st['t'], dur, list(st['lastchord'] or []), tie])
                elif midi is not None: ev.append([st['t'], dur, [midi], tie])
                st['t'] += dur
                i = j; continue
            if k == 'dur':           # a bare duration repeats the last note ("c4 8 8")
                d = dur_of(v); st['dur'] = d
                if ev:
                    ev.append([st['t'], d * st['scale'], list(ev[-1][2]), False]); st['t'] += d * st['scale']
                i += 1; continue
            if k == 'tie':
                if ev: ev[-1][3] = True
                i += 1; continue
            if k == 'cmd':
                if v in ('\\relative', '\\fixed'):
                    j = i + 1; ref = None
                    if toks[j][0] == 'note':
                        ref = self._ref_octave(toks[j][1]); j += 1
                    else:
                        ref = (0, 4)  # \relative { } defaults to c'
                    save = (st['mode'], st['last'])
                    st['mode'] = ('rel', ref) if v == '\\relative' else ('fixed', ref)
                    st['last'] = None
                    e = self._block_end(toks, j)
                    self._seq(toks, j + 1, e, st, ev, vname)
                    st['mode'], st['last'] = save
                    i = e + 1; continue
                if v == '\\absolute':
                    i += 1; continue
                if v in ('\\time',):
                    n, d = toks[i + 1][1].split('/'); self.time = (int(n), int(d)); i += 2; continue
                if v == '\\partial':
                    self.partial = dur_of(toks[i + 1][1]); i += 2; continue
                if v == '\\key':
                    i += 3; continue
                if v in ('\\tuplet', '\\times'):
                    frac = toks[i + 1][1]; n, d = [int(x) for x in frac.split('/')]
                    f = Fr(d, n) if v == '\\tuplet' else Fr(n, d)
                    j = i + 2
                    if toks[j][0] == 'dur' or toks[j][0] == 'num': j += 1   # \tuplet 3/2 8 { }
                    e = self._block_end(toks, j)
                    old = st['scale']; st['scale'] = old * f
                    self._seq(toks, j + 1, e, st, ev, vname)
                    st['scale'] = old; i = e + 1; continue
                if v in ('\\grace', '\\acciaccatura', '\\appoggiatura', '\\slashedGrace', '\\afterGrace'):
                    j = i + 1
                    if v == '\\afterGrace':
                        # \afterGrace main { graces }: keep the main note, drop the graces
                        pass
                    if toks[j][0] == 'open':
                        e = self._block_end(toks, j)
                        # keep relative pitch tracking through the grace notes
                        tmp = []; save = st['t']
                        self._seq(toks, j + 1, e, st, tmp, vname)
                        st['t'] = save                      # a grace's duration carries on to the next notes
                        self.graces.append((st['t'], [m for x in tmp for m in x[2]]))
                        i = e + 1
                    else:
                        # one grace note, or one grace chord <...> with its duration
                        e = j + 1
                        if toks[j][0] == 'chordopen':
                            while toks[e - 1][0] != 'chordclose': e += 1
                        if e < b and toks[e][0] == 'dur': e += 1
                        tmp = []; save = st['t']
                        self._seq(toks, j, e, st, tmp, vname)
                        st['t'] = save
                        self.graces.append((st['t'], [m for x in tmp for m in x[2]]))
                        i = e
                    continue
                if v == '\\repeat':
                    kind = toks[i + 1][1]; n = int(toks[i + 2][1]); j = i + 3
                    e = self._block_end(toks, j)
                    body = (j + 1, e)
                    alts = []
                    k2 = e + 1
                    if k2 < b and toks[k2] == ('cmd', '\\alternative'):
                        e2 = self._block_end(toks, k2 + 1)
                        q = k2 + 2
                        while q < e2:
                            if toks[q][0] == 'open':
                                qe = self._block_end(toks, q); alts.append((q + 1, qe)); q = qe + 1
                            else: q += 1
                        k2 = e2 + 1
                    if kind in ('volta', 'segno'):
                        # as printed: the body once, then each ending; the repeat is written out later for all voices
                        t0 = st['t']
                        self._seq(toks, body[0], body[1], st, ev, vname)
                        t1 = st['t']; altspans = []
                        for a2 in alts:
                            a0 = st['t']; self._seq(toks, a2[0], a2[1], st, ev, vname); altspans.append((a0, st['t']))
                        self.voltas.append((t0, t1, n, tuple(altspans)))
                    else:
                        for r in range(n):
                            self._seq(toks, body[0], body[1], st, ev, vname)
                            if alts:
                                a2 = alts[min(r, len(alts) - 1)]
                                self._seq(toks, a2[0], a2[1], st, ev, vname)
                    i = k2; continue
                if v in SKIP0: i += 1; continue
                if v == '\\tempo':
                    j = i + 1
                    if j < b and toks[j][0] == 'str': j += 1
                    if j + 2 < b + 1 and j < b and toks[j][0] in ('dur', 'num') and j + 1 < b and toks[j + 1][0] == 'eq': j += 3
                    i = j; continue
                if v in ('\\omit', '\\hide', '\\undo', '\\temporary'):
                    j = i + 1
                    while j < b and (toks[j][0] == 'word' or toks[j] == ('other', '.')): j += 1
                    i = j; continue
                if v in SKIP1:
                    j = i + 1
                    # skip until an argument is consumed (for \override/\set: path = value)
                    if v in ('\\override', '\\set', '\\revert', '\\unset', '\\once', '\\tweak', '\\omit', '\\hide', '\\undo', '\\temporary'):
                        if v == '\\once': i = j; continue
                        # a property path (words and dots, maybe a #'symbol), then for \set/\override "= value"
                        while j < b and (toks[j][0] in ('word', 'hash') or toks[j] == ('other', '.')): j += 1
                        if j < b and toks[j][0] == 'eq':
                            j += 1
                            if j < b and toks[j][0] in ('hash', 'num', 'str', 'word', 'dur', 'frac'): j += 1
                        i = j; continue
                    if j < b and toks[j][0] == 'open':
                        i = self._block_end(toks, j) + 1
                    else:
                        i = j + 1
                    continue
                name = v[1:]
                if name in self.defs:
                    sub = self.defs[name]
                    self._seq(sub, 0, len(sub), st, ev, vname); i += 1; continue
                if re.fullmatch(r'\\\d+', v): i += 1; continue   # string number
                i += 1; continue
            if k == 'other' and v == '|':
                self.checks.append((st['t'], vname, i, st['scale']))
                i += 1; continue
            # fingering "-1", articulation "-." etc.
            if k == 'other' and v in '-^_':
                j = i + 1
                if j < b and toks[j][0] in ('num', 'str', 'other', 'dur', 'cmd'): j += 1
                i = j; continue
            i += 1

    def _simul(self, toks, a, b, st, ev, vname):
        """<< A \\\\ B >> or << {A} {B} >>: each part from the same start; the first part continues this voice."""
        parts, cur, i = [], [], a
        depth = 0; start = a
        # split on top-level \\ and on top-level blocks
        segs = []; i = a; segstart = a
        while i < b:
            k, v = toks[i]
            if k == 'open': i = self._block_end(toks, i) + 1; continue
            if k == 'voicesep': segs.append((segstart, i)); segstart = i + 1
            i += 1
        segs.append((segstart, b))
        t0 = st['t']; ends = []
        for n_, (s0, s1) in enumerate(segs):
            # within a segment, top-level blocks without \\ run simultaneously too
            blocks = []; i = s0
            while i < s1:
                if toks[i][0] == 'open' and toks[i][1] == '{':
                    e = self._block_end(toks, i); blocks.append((i, e + 1)); i = e + 1
                elif toks[i][0] == 'cmd' and toks[i][1][1:] in self.defs:
                    blocks.append((i, i + 1)); i += 1
                elif toks[i][0] == 'cmd' and toks[i][1] in ('\\new', '\\context'):
                    # \new Voice = "x" { } / \new Staff ...: take the next block
                    j = i + 1
                    while j < s1 and toks[j][0] != 'open' and not (toks[j][0] == 'cmd' and toks[j][1][1:] in self.defs): j += 1
                    if j < s1 and toks[j][0] == 'open':
                        e = self._block_end(toks, j); blocks.append((j, e + 1)); i = e + 1
                    elif j < s1: blocks.append((j, j + 1)); i = j + 1
                    else: i = j
                else:
                    i += 1
            if not blocks: blocks = [(s0, s1)]
            for (x0, x1) in blocks:
                # relative pitches run on through the parts in the order they are written (LilyPond reads them so)
                st2 = dict(st); st2['t'] = t0
                tgt = ev if (n_ == 0 and (x0, x1) == blocks[0]) else self.voices.setdefault(f'{vname}.{n_}.{x0}', [])
                self._seq(toks, x0, x1, st2, tgt, vname)
                ends.append(st2['t'])
                st['last'] = st2['last']; st['lastchord'] = st2['lastchord']
                if tgt is ev: st['dur'] = st2['dur']
        st['t'] = max(ends) if ends else t0


def join_ties(ev):
    """merge tied notes: a note tied into the next event with the same pitch lengthens it"""
    out = []
    pend = {}     # midi -> index in out
    for t, d, ms, tie in sorted(ev, key=lambda x: x[0]):
        for m in ms:
            if m in pend and abs(out[pend[m]][0] + out[pend[m]][1] - t) < Fr(1, 1000):
                out[pend[m]][1] += d; idx = pend[m]
            else:
                out.append([t, d, m]); idx = len(out) - 1
            if tie: pend[m] = idx
            elif m in pend: del pend[m]
        for m in list(pend):
            if m not in ms and abs(out[pend[m]][0] + out[pend[m]][1] - t - d) > Fr(1, 1000) and out[pend[m]][0] + out[pend[m]][1] < t: del pend[m]
    return out


def parse(path):
    R = Reader(open(path, encoding='utf-8', errors='replace').read())
    # the score: find \score { ... } and run it, or else run every voice-like definition
    t = R.toks
    si = next((i for i, x in enumerate(t) if x == ('cmd', '\\score')), None)
    voices = {}
    # the voices: definitions the score uses that hold notes, each read on its own (global first, for \time)
    used = []
    if si is not None:
        e = R._block_end(t, si + 1)
        for k, v in t[si:e]:
            if k == 'cmd' and v[1:] in R.defs and v[1:] not in used: used.append(v[1:])
    def has_notes(name, seen=()):
        for k, v in R.defs[name]:
            if k == 'note' and not v.startswith(('r', 's', 'R')): return True
            if k == 'cmd' and v[1:] in R.defs and v[1:] not in seen and v[1:] != name and has_notes(v[1:], seen + (name,)): return True
        return False
    music = [u for u in used if has_notes(u)]
    for u in used:
        if u not in music:
            R.run(R.defs[u])                      # \global and the like: \time, \partial
    bad = []
    if music:
        for u in music:
            R.checks = []
            ev = R.run(R.defs[u])
            n_, d_ = R.time; bl_ = Fr(n_, d_)
            for t_, vn, ti, sc in R.checks:
                if sc == 1 and (t_ - R.partial) % bl_ != 0:
                    toks_ = R.defs[u]
                    bad.append((u, float((t_ - R.partial) / bl_), ' '.join(x[1] for x in toks_[max(0, ti - 12):ti + 1])))
            voices[u] = ev
            for k, v in R.voices.items(): voices[u + ':' + k] = v
        si = None
    if si is not None:
        j = si + 1
        e = R._block_end(t, j)
        body = t[j + 1:e]
        # drop \layout { } \midi { } \header { }
        clean = []; i = 0
        while i < len(body):
            if body[i][0] == 'cmd' and body[i][1] in ('\\layout', '\\midi', '\\header', '\\paper'):
                k = i + 1
                if k < len(body) and body[k][0] == 'open': i = R._block_end(body, k) + 1; continue
            clean.append(body[i]); i += 1
        ev = R.run(clean)
        voices['main'] = ev
        for k, v in R.voices.items(): voices[k] = v
    printed = []
    for name, ev in voices.items():
        for t0, d, m in join_ties(ev):
            printed.append((t0, d, m, name))
    printed.sort()
    # write the volta repeats out for every voice: [body, ending 1, body, ending 2, ...] in playing order
    vol = sorted(set(R.voltas))
    plen = max((t0 + d for t0, d, m, n in printed), default=Fr(0))
    spans = []; cur = Fr(0)
    for t0, t1, n, alts in vol:
        if t0 < cur: continue                       # the same repeat seen in another voice
        if t0 > cur: spans.append((cur, t0))
        end = alts[-1][1] if alts else t1
        for r in range(n):
            spans.append((t0, t1))
            if alts: spans.append(alts[min(r, len(alts) - 1)])
        cur = end
    if cur < plen: spans.append((cur, plen))
    notes = []; out_t = Fr(0)
    for a, b in spans:
        for t0, d, m, n in printed:
            if a <= t0 < b: notes.append((out_t + t0 - a, min(d, b - t0) if t0 + d > b else d, m, n))
        out_t += b - a
    notes.sort()
    length = max((t0 + d for t0, d, m, n in notes), default=Fr(0))
    return dict(time=R.time, partial=R.partial, voices=voices, notes=notes, length=length, graces=R.graces, bad=bad)


def bars(P):
    """notes per bar, onsets in quarter-note beats from the bar's start"""
    n, d = P['time']; bl = Fr(n, d)
    out = {}
    for t0, du, m, v in P['notes']:
        x = t0 - P['partial']
        b = int(x // bl) + (1 if P['partial'] else 1)
        if x < 0: b = 0
        out.setdefault(b, []).append(((x - (b - 1) * bl) * 4 if x >= 0 else (t0) * 4, du * 4, m, v))
    return out


if __name__ == '__main__':
    import sys
    P = parse(sys.argv[1])
    n, d = P['time']; bl = Fr(n, d)
    print('time', P['time'], 'partial', P['partial'], 'length', P['length'], 'bars', float((P['length'] - P['partial']) / bl), 'voices', {k: len(v) for k, v in P['voices'].items()}, 'graces', len(P['graces']))
    NM = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B']
    B = bars(P)
    for b in sorted(B)[:int(sys.argv[2]) if len(sys.argv) > 2 else 4]:
        print(b, ' '.join(f"{float(o):g}:{NM[m % 12]}{m // 12 - 1}/{float(du):g}" for o, du, m, v in sorted(B[b])))
