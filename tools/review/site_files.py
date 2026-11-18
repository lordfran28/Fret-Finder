import json, os, re, subprocess, sys
SITE = '/tmp/claude-0/-home-claude/32eff81e-a259-5caa-a171-2530c104e7b0/scratchpad/site/'
SP = '/tmp/claude-0/-home-claude/32eff81e-a259-5caa-a171-2530c104e7b0/scratchpad/'
for site in ('Fret-Finder', 'Key-Finder'):
    root = SITE + site + '/songs/'
    idx = json.load(open(root + 'index.json'))
    songs = idx['songs'] if isinstance(idx, dict) else idx
    listed = {s.get('id') or s.get('slug') or (s.get('page') or s.get('path', '')).strip('/').split('/')[-1] for s in songs}
    folders = {d for d in os.listdir(root) if os.path.isdir(root + d)}
    print(site, len(folders), 'folders,', len(listed), 'listed; missing from index', sorted(folders - listed), 'listed without folder', sorted(listed - folders))
    probs = []
    for d in sorted(folders):
        f = root + d + '/index.html'
        if not os.path.exists(f): probs.append(d + ': no index.html'); continue
        html = open(f, encoding='utf-8').read()
        refs = set(re.findall(r'["\'(/]([\w.%() -]+\.mp3(?:\.locked)?)["\')]', html))
        for r in refs:
            if r.startswith('http'): continue
            if not os.path.exists(root + d + '/' + r): probs.append(f'{d}: page names {r}, not in folder')
        for m in os.listdir(root + d):
            if m.endswith('.mp3'):
                p = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', root + d + '/' + m], capture_output=True, text=True)
                try:
                    if float(p.stdout.strip()) < 5: probs.append(f'{d}/{m}: only {p.stdout.strip()} s')
                except ValueError: probs.append(f'{d}/{m}: not playable ({p.stderr.strip()[:80]})')
        sj = root + d + '/song.json'
        if not os.path.exists(sj): probs.append(d + ': no song.json')
        # no CAGED names (17 Nov: “the A-shape at the 3rd fret” on You'd Be So Nice): positions by fret and string
        for m in re.finditer(r'\b[CAGED][- ](?:shape|form)\b', html):
            probs.append(f'{d}: CAGED name “{html[max(0, m.start() - 30):m.end() + 20]}”')
    print('  problems:', len(probs)); [print('   ', p) for p in probs]

# the Exercises entries: every folder listed, every file a page names in its folder, every mp3 playable
for site in ('Fret-Finder',):
    root = SITE + site + '/studies/'
    if not os.path.isdir(root): continue
    idx = json.load(open(root + 'index.json'))
    listed = {s.get('id') for s in idx.get('studies', [])}
    folders = {d for d in os.listdir(root) if os.path.isdir(root + d)}
    print(site, 'exercises:', len(folders), 'folders,', len(listed), 'listed; missing from index', sorted(folders - listed), 'listed without folder', sorted(listed - folders))
    probs = []
    for d in sorted(folders):
        f = root + d + '/index.html'
        if not os.path.exists(f): probs.append(d + ': no index.html'); continue
        html = open(f, encoding='utf-8').read()
        for r in set(re.findall(r'["\'(/]([\w.%() -]+\.mp3)["\')]', html)):
            if not os.path.exists(root + d + '/' + r): probs.append(f'{d}: page names {r}, not in folder')
        for m in os.listdir(root + d):
            if m.endswith('.mp3'):
                p = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', root + d + '/' + m], capture_output=True, text=True)
                try:
                    if float(p.stdout.strip()) < 5: probs.append(f'{d}/{m}: only {p.stdout.strip()} s')
                except ValueError: probs.append(f'{d}/{m}: not playable')
        if not os.path.exists(root + d + '/entry.json'): probs.append(d + ': no entry.json')
        for m in re.finditer(r'\b[CAGED][- ](?:shape|form)\b', html):
            probs.append(f'{d}: CAGED name “{html[max(0, m.start() - 30):m.end() + 20]}”')
    print('  problems:', len(probs)); [print('   ', p) for p in probs]

# the Classical section (locked whole): every folder listed, a stub page, the page, its card and its tracks all locked;
# with the key at hand, every file the unlocked page names is in its folder
for site in ('Fret-Finder',):
    root = SITE + site + '/classical/'
    if not os.path.isdir(root): continue
    listed = {p['id'] for p in json.load(open(root + 'index.json')).get('pieces', [])}
    folders = {d for d in os.listdir(root) if os.path.isdir(root + d)}
    print(site, 'classical:', len(folders), 'folders,', len(listed), 'listed; missing from index', sorted(folders - listed), 'listed without folder', sorted(listed - folders))
    probs = []
    unlock = SP + 'unlock.mjs'
    for d in sorted(folders):
        f = root + d + '/'
        stub = open(f + 'index.html', encoding='utf-8').read() if os.path.exists(f + 'index.html') else ''
        if 'ff-locked-file' not in stub or 'ff-locked-back' not in stub: probs.append(d + ': the stub page is missing or wrong')
        for m in os.listdir(f):
            if m == 'index.html': continue
            if not m.endswith('.locked'): probs.append(f'{d}/{m}: open file in the locked section'); continue
            if open(f + m, 'rb').read(4) != b'FFV1': probs.append(f'{d}/{m}: not locked')
        if os.path.exists(unlock) and os.path.exists(WORD_FILE := SP + 'voicekey/singer-word.txt') and os.path.exists(f + 'page.html.locked'):
            out = SP + 'night/_page.html'
            if subprocess.run(['node', unlock, f + 'page.html.locked', out], capture_output=True).returncode == 0:
                html = open(out, encoding='utf-8').read(); os.remove(out)
                for r in set(re.findall(r'["\'(/]([\w.%() -]+\.mp3(?:\.locked)?)["\')]', html)):
                    if not os.path.exists(f + r): probs.append(f'{d}: page names {r}, not in folder')
                    elif not r.endswith('.locked'): probs.append(f'{d}: page names the open file {r}')
            else: probs.append(d + ': the page would not open with the key')
    print('  problems:', len(probs)); [print('   ', p) for p in probs]

# the singer key's word is never in a file or a commit message of the three sites (17 Nov: it was in two commit
# messages of 13 Nov and in site_pages.js). The word is read from the scratchpad, never written here.
WORD = SP + 'voicekey/singer-word.txt'
if os.path.exists(WORD):
    w = open(WORD).read().strip()
    for site in ('Fret-Finder', 'Key-Finder', 'Valve-Finder'):
        g = SITE + site
        files = subprocess.run(['git', '-C', g, 'grep', '-I', '-l', '-i', '-w', '-e', w, '--', '.', ':!*.musicxml', ':!*.vf.json', ':!songs/index.json'], capture_output=True, text=True).stdout.split()
        msgs = [l for l in subprocess.run(['git', '-C', g, 'log', '--since=2026-11-14', '--format=%h %s%n%b'], capture_output=True, text=True).stdout.splitlines()
                if re.search(r'\b' + re.escape(w) + r'\b', l, re.I)]
        print(site, 'singer key word: in', len(files), 'files', files, '; in', len(msgs), 'new commit messages')
