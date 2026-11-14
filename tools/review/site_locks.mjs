// every .mp3.locked on Fret Finder and Key Finder opens with the singer key; size = locked - 97; an mp3 inside
import fs from 'fs'; import path from 'path';
const { subtle } = globalThis.crypto;
const SITE = '/tmp/claude-0/-home-claude/32eff81e-a259-5caa-a171-2530c104e7b0/scratchpad/site/';
const d = fs.readFileSync('/tmp/claude-0/-home-claude/32eff81e-a259-5caa-a171-2530c104e7b0/scratchpad/voicekey/singer-key.txt', 'utf8').trim();
const INFO = new TextEncoder().encode('fret-finder voice');
let ok = 0, bad = [];
for (const site of ['Fret-Finder', 'Key-Finder']) {
  const p = JSON.parse(fs.readFileSync(SITE + site + '/assets/voice-key.json', 'utf8'));
  const priv = await subtle.importKey('jwk', { kty: 'EC', crv: 'P-256', x: p.x, y: p.y, d, ext: true }, { name: 'ECDH', namedCurve: 'P-256' }, false, ['deriveBits']);
  const walk = dir => fs.readdirSync(dir, { withFileTypes: true }).flatMap(e => e.isDirectory() ? walk(path.join(dir, e.name)) : [path.join(dir, e.name)]);
  const files = walk(SITE + site).filter(f => f.endsWith('.locked') && !f.includes('/.git/'));
  for (const f of files) {
    const u = new Uint8Array(fs.readFileSync(f));
    try {
      if (String.fromCharCode(...u.slice(0, 4)) !== 'FFV1') throw 'not FFV1';
      const epk = u.slice(4, 69), iv = u.slice(69, 81), ct = u.slice(81);
      const pk = await subtle.importKey('raw', epk, { name: 'ECDH', namedCurve: 'P-256' }, false, []);
      const bits = await subtle.deriveBits({ name: 'ECDH', public: pk }, priv, 256);
      const hk = await subtle.importKey('raw', bits, 'HKDF', false, ['deriveKey']);
      const k = await subtle.deriveKey({ name: 'HKDF', hash: 'SHA-256', salt: epk, info: INFO }, hk, { name: 'AES-GCM', length: 256 }, false, ['decrypt']);
      const pt = new Uint8Array(await subtle.decrypt({ name: 'AES-GCM', iv }, k, ct));
      if (pt.length !== u.length - 97) throw 'size ' + pt.length + ' vs ' + (u.length - 97);
      if (f.endsWith('.mp3.locked') && !((pt[0] === 0x49 && pt[1] === 0x44 && pt[2] === 0x33) || (pt[0] === 0xff && (pt[1] & 0xe0) === 0xe0))) throw 'no mp3 header';
      ok++;
    } catch (e) { bad.push(f.replace(SITE, '') + ': ' + e); }
  }
  console.log(site, files.length, 'locked files');
}
console.log('opened', ok, 'bad', bad.length); bad.forEach(b => console.log('  BAD', b));
