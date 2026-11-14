import json, os, re, subprocess, sys
SITE = '/tmp/claude-0/-home-claude/32eff81e-a259-5caa-a171-2530c104e7b0/scratchpad/site/'
for site in ('Fret-Finder', 'Key-Finder'):
    root = SITE + site + '/songs/'
    idx = json.load(open(root + 'index.json'))
    songs = idx['songs'] if isinstance(idx, dict) else idx
    listed = {s.get('slug') or s.get('path', '').strip('/').split('/')[-1] for s in songs}
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
    print('  problems:', len(probs)); [print('   ', p) for p in probs]
