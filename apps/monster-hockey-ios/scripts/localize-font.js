// Bundle the game's pixel font inside the app so it looks right offline.
// Downloads Press Start 2P (SIL Open Font License) once and points the game at the local copy.
const fs = require('fs'), path = require('path'), https = require('https');
const www = path.join(__dirname, '..', 'www'), dir = path.join(www, 'fonts'), file = path.join(dir, 'PressStart2P-Regular.ttf');
const URL = 'https://raw.githubusercontent.com/google/fonts/main/ofl/pressstart2p/PressStart2P-Regular.ttf';
function get(url, cb){ https.get(url, r => { if (r.statusCode >= 300 && r.headers.location) return get(r.headers.location, cb); if (r.statusCode !== 200) return cb(new Error('HTTP ' + r.statusCode)); const b = []; r.on('data', d => b.push(d)); r.on('end', () => cb(null, Buffer.concat(b))); }).on('error', cb); }
function patch(){
  const p = path.join(www, 'index.html'); let s = fs.readFileSync(p, 'utf8');
  if (!s.includes('fonts/PressStart2P-Regular.ttf')){
    s = s.replace('<head>', '<head>\n<style>@font-face{font-family:"Press Start 2P";src:url("fonts/PressStart2P-Regular.ttf") format("truetype");font-display:block}</style>');
    fs.writeFileSync(p, s);
  }
  console.log('Font bundled.');
}
fs.mkdirSync(dir, { recursive: true });
if (fs.existsSync(file)) patch();
else get(URL, (err, buf) => { if (err){ console.warn('Could not download the font (' + err.message + '); the app will use it whenever there is internet.'); return; } fs.writeFileSync(file, buf); patch(); });
