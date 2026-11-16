"""Quotes of the book stay short: a beat or two of the original's opening (Fret Finder's rule for the Exercises).
trim(SECTIONS) cuts every quote's items to its first two beats (leading silence dropped) and says so in its text."""
import re

MAX = 2.0


def _cut_list(xs, n): return list(xs[:n])


def _trim_items(items, limit=MAX):
    out, t, started = [], 0.0, False
    for it in items:
        rem = limit - t
        if rem <= 1e-9: break
        kind = it[0]
        if kind == 'W':
            if not started: continue                      # no silence before the first note
            d = min(it[1], rem); out.append(['W', d]); t += d; continue
        started = True
        if kind == 'K':
            hits, keep, tt = it[3], [], 0.0
            for h in hits:
                if tt >= rem - 1e-9: break
                d = min(h[0], rem - tt); keep.append((d,) + tuple(h[1:])); tt += d
            out.append([it[0], it[1], it[2], keep] + list(it[4:])); t += tt; continue
        if kind in ('R', 'P'):
            durs, tt, n = it[2], 0.0, 0
            nd = []
            for d in durs:
                if tt >= rem - 1e-9: break
                d2 = min(d, rem - tt); nd.append(d2); tt += d2; n += 1
            new = [kind, _cut_list(it[1], n), nd]
            if len(it) > 3:
                lab = it[3]
                if isinstance(lab, str) and lab.startswith('='):
                    head, _, tail = lab[1:].partition('|')
                    names = head.split(',')[:n]
                    lab = '=' + ','.join(names) + ('|' + tail if tail else '')
                new.append(lab)
            if len(it) > 4:
                extra = dict(it[4])
                for k in ('vel', 'short'):
                    if k in extra: extra[k] = _cut_list(extra[k], n)
                new.append(extra)
            out.append(new); t += tt; continue
        out.append(it)
    return out, t


def _beats(items):
    t = 0.0
    for it in items:
        if it[0] == 'K': t += sum(h[0] for h in it[3])
        elif it[0] in ('R', 'P'): t += sum(it[2])
        elif it[0] == 'W': t += it[1]
    return t


def trim(sections, limit=MAX):
    n = 0
    for S in sections:
        for ex in S['ex']:
            q = ex.get('quote') or {}
            its = q.get('items') or ([q['item']] if q.get('item') else None)
            if not its: continue
            lead = 0
            for it in its:
                if it[0] == 'W': lead += 1
                else: break
            if _beats(its) <= limit + 1e-9 and not lead: continue
            new, t = _trim_items(its, limit)
            if _beats(its) > limit + 1e-9:
                txt = q.get('text', '')
                if 'Played here:' in txt: q['text'] = txt[:txt.index('Played here:')].rstrip()
                q['played'] = 'Played here: its first two beats.' if t > 1.5 else 'Played here: its opening only.'
                n += 1
            q['items'] = new; q.pop('item', None)
    return n
