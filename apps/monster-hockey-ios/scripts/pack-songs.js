// Build the songs straight into the game page so the app never has to load them as files
// (inside an iOS app the game can't fetch its own mp3s the way the website does).
const fs = require('fs'), path = require('path');
const www = path.join(__dirname, '..', 'www'), page = path.join(www, 'index.html');
const SONGS = { game: 'halloween-arcade-run.mp3', fight: 'fight-fight-fight.mp3', zomboni: 'brains.mp3', menu: 'skating-groove.mp3' };
let s = fs.readFileSync(page, 'utf8');
s = s.replace(/<script id="mi-songs">[\s\S]*?<\/script>\n?/, '');   // replace an older packed copy
const packed = {};
for (const [k, f] of Object.entries(SONGS)){ const p = path.join(www, f); if (fs.existsSync(p)) packed[k] = fs.readFileSync(p).toString('base64'); }
const tag = '<script id="mi-songs">window.MI_SONGS = ' + JSON.stringify(packed) + ';</script>\n';
const at = s.indexOf('<script>\n(() => {');
if (at < 0){ console.warn('Could not find the game script; songs not packed.'); process.exit(0); }
s = s.slice(0, at) + tag + s.slice(at);
fs.writeFileSync(page, s);
console.log('Songs packed into the app: ' + Object.keys(packed).join(', '));
