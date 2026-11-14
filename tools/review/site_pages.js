// night survey: every page of the Finder sites at 390 px; page errors, failed local requests, sideways scroll, what rendered
const { chromium } = require('playwright'); const fs = require('fs');
const SITE = '/tmp/claude-0/-home-claude/32eff81e-a259-5caa-a171-2530c104e7b0/scratchpad/site/';
const B = 'http://127.0.0.1:' + (process.argv[2] || 8766) + '/';
const only = process.argv[3];
const jobs = [];
for (const s of ['Fret-Finder', 'Key-Finder']) {
  jobs.push([s, s + '/index.html', 'home'], [s, s + '/index.html#owner', 'owner']);
  if (s === 'Key-Finder') jobs.push([s, s + '/index.html#shapes', 'shapes']);
  for (const d of fs.readdirSync(SITE + s + '/songs').filter(d => fs.statSync(SITE + s + '/songs/' + d).isDirectory())) jobs.push([s, s + '/songs/' + d + '/', 'song']);
}
const vf = JSON.parse(fs.readFileSync(SITE + 'Valve-Finder/songs/index.json'));
jobs.push(['Valve-Finder', 'Valve-Finder/index.html', 'home'], ['Valve-Finder', 'Valve-Finder/index.html#owner', 'owner']);
for (const x of vf.songs) if (fs.existsSync(SITE + 'Valve-Finder/' + x.file)) jobs.push(['Valve-Finder', 'Valve-Finder/index.html#song-' + x.id, 'vfsong']);
const J = only ? jobs.filter(j => j[1].includes(only)) : jobs;
(async () => {
  const b = await chromium.launch(); const out = [];
  let i = 0;
  async function worker() {
    while (i < J.length) {
      const [site, url, kind] = J[i++];
      const ctx = await b.newContext({ viewport: { width: 390, height: 860 }, serviceWorkers: 'block' });
      if (kind === 'withkey') await ctx.addInitScript(() => { try { localStorage.setItem('ff.voicekey', 'fran'); } catch (e) {} });
      const p = await ctx.newPage(); const errs = [], fails = [], cons = [];
      p.on('pageerror', e => errs.push(String(e.message).slice(0, 140)));
      p.on('console', m => { if (m.type() === 'error') cons.push(m.text().slice(0, 140)); });
      p.on('response', r => { if (r.status() >= 400 && r.url().startsWith(B)) fails.push(r.status() + ' ' + decodeURIComponent(r.url().slice(B.length))); });
      p.on('requestfailed', r => { if (r.url().startsWith(B) && !/ERR_ABORTED/.test(r.failure().errorText)) fails.push('failed ' + decodeURIComponent(r.url().slice(B.length))); });
      let info = {};
      try {
        await p.goto(B + url, { waitUntil: 'load', timeout: 30000 });
        await p.waitForTimeout(kind === 'withkey' ? 5000 : kind === 'vfsong' ? 1800 : 1500);
        info = await p.evaluate(() => {
          const vis = e => e && e.offsetParent !== null;
          const svgs = [...document.querySelectorAll('svg')].filter(s => s.childElementCount >= 6 && vis(s));
          return {
            wide: document.documentElement.scrollWidth > innerWidth + 1,
            svgs: svgs.length, dg: document.querySelectorAll('svg.dg').length,
            ffg: document.querySelectorAll('.ffg').length,
            audio: document.querySelectorAll('audio').length,
            links: document.querySelectorAll('a[href*="songs/"]').length,
            text: document.body.innerText.length,
            head: document.body.innerText.replace(/\s+/g, ' ').slice(0, 90)
          };
        });
      } catch (e) { errs.push('LOAD ' + e.message.slice(0, 100)); }
      out.push({ site, url, kind, errs, fails: [...new Set(fails)], cons: [...new Set(cons)].filter(c => !/Failed to load resource/.test(c)), ...info });
      await ctx.close();
    }
  }
  await Promise.all([worker(), worker(), worker(), worker()]);
  fs.writeFileSync(SITE + '../night/survey.json', JSON.stringify(out, null, 1));
  const bad = out.filter(o => o.errs.length || o.fails.length || o.cons.length || o.wide);
  console.log('pages', out.length, 'with trouble', bad.length);
  for (const o of bad) console.log(o.url, o.kind, JSON.stringify({ e: o.errs, f: o.fails, c: o.cons, wide: o.wide }));
  await b.close();
})();
