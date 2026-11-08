// Captures a design kit for "You Call Yourself a New Yorker?":
//   design-kit/screens/*.png    key screens, phone portrait + landscape
//   design-kit/elements/*.png   every UI piece on a transparent background
//   design-kit/sprite-sheet.png all the pieces on one labeled sheet
// Run by .github/workflows/new-yorker-design-kit.yml (serves the repo on :8080 first).
import { chromium } from "playwright";
import fs from "fs";

const URL = "http://localhost:8080/games/you-call-yourself-a-new-yorker/";
const OUT = "games/you-call-yourself-a-new-yorker/design-kit";
fs.mkdirSync(OUT + "/screens", { recursive: true });
fs.mkdirSync(OUT + "/elements", { recursive: true });
const sleep = ms => new Promise(r => setTimeout(r, ms));

async function boot(browser, w, h, dpr) {
  const p = await browser.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: dpr });
  p.on("pageerror", e => console.log("PAGEERR", e.message));
  p.setDefaultTimeout(20000);
  await p.addInitScript(() => { try { localStorage.clear(); } catch (e) {} Math.random = (() => { let s = 7; return () => ((s = (s * 16807) % 2147483647) / 2147483647); })(); });
  await p.goto(URL, { waitUntil: "networkidle" });
  await p.waitForFunction(() => !document.getElementById("startBtn").disabled, null, { timeout: 60000 });
  await sleep(1500);
  return p;
}
async function mapTap(p, fx, fy) { const b = await p.locator("#map").boundingBox(); await p.mouse.click(b.x + b.width * fx, b.y + b.height * fy); await sleep(400); }

async function screens(browser, w, h, dpr, tag) {
  const shot = async (p, name) => { await p.screenshot({ path: `${OUT}/screens/${tag}-${name}.png` }); console.log("shot", tag, name); };

  // ---- single player
  let p = await boot(browser, w, h, dpr);
  await shot(p, "01-title");
  await p.click("#startBtn"); await sleep(3500);
  await shot(p, "02-look-aperture");
  await p.click("#widenBtn"); await sleep(1300);
  await shot(p, "03-look-bigger");
  await p.click("#readyBtn"); await sleep(4500);
  await shot(p, "04-map");
  await mapTap(p, 0.42, 0.42);
  await shot(p, "05-map-pinned");
  await p.click("#helpBtn"); await sleep(400);
  await p.click("#hSubway"); await sleep(1200);
  await shot(p, "06-helpers-panel");
  await p.click("#hColor"); await p.click("#hRoads"); await p.click("#helpBtn"); await sleep(1500);
  await shot(p, "07-helpers-on");
  await p.click("#lockBtn"); await sleep(2600);
  await shot(p, "08-reveal");
  await p.click("#apWrap"); await sleep(1000);
  await shot(p, "09-reveal-photo");
  await p.close();
  // ---- three players
  p = await boot(browser, w, h, dpr);
  await p.click('#pcount button[data-n="3"]'); await sleep(300);
  for (const [i, n] of ["Steph", "Mom", "Kiddo"].entries()) await p.fill(`#pnames input[data-i="${i}"]`, n);
  await shot(p, "10-title-3-players");
  await p.click("#startBtn"); await sleep(3500);
  await p.click("#readyBtn"); await sleep(1500);
  for (let r = 0; r < 5; r++) {
    for (let t = 0; t < 3; t++) {
      await mapTap(p, 0.35 + t * 0.12, 0.40 + t * 0.06);
      if (r === 0 && t === 2) await shot(p, "11-multi-picking");
      await p.click("#lockBtn"); await sleep(500);
    }
    await sleep(2200);
    if (r === 0) await shot(p, "12-multi-reveal");
    await p.click("#nextBtn"); await sleep(r < 4 ? 3500 : 1200);
    if (r < 4) { await p.click("#readyBtn"); await sleep(1500); }
  }
  await shot(p, "13-final-standings");
  await p.close();
}

async function kit(browser) {
  const p = await boot(browser, 1400, 1000, 2);
  await p.evaluate(() => {
    const css = `
      #kit{position:fixed;inset:0;z-index:999;overflow:auto;background:#2a2b2f;color:#eee;font:14px Helvetica,Arial,sans-serif;padding:24px}
      #kit h3{font-family:Bungee;font-weight:400;color:#f7b500;margin:22px 0 8px;font-size:18px}
      #kit .row{display:flex;flex-wrap:wrap;gap:22px;align-items:flex-end}
      #kit figure{margin:0;display:flex;flex-direction:column;align-items:center;gap:6px}
      #kit figcaption{font-size:12px;color:#bbb;text-align:center;max-width:220px}
      #kit .sp{display:inline-block}
      #kit .sw{width:110px;height:64px;border-radius:8px;border:2px solid #000}
      .kitbubble{position:relative;background:#f2ead6;color:#141414;border-radius:14px;padding:8px 12px;border:3px solid #000;box-shadow:3px 3px 0 #000;font:17px Oswald;max-width:260px}`;
    const st = document.createElement("style"); st.textContent = css; document.head.appendChild(st);
    const k = document.createElement("div"); k.id = "kit"; document.body.appendChild(k);
    const fig = (html, cap, id) => `<figure><div class="sp" id="${id}">${html}</div><figcaption>${cap}</figcaption></figure>`;
    const apSvg = document.getElementById("apSvg").innerHTML;
    const blades = a => apSvg.replace(/rotate\(-?[\d.]+ 100 18\)/g, `rotate(${a} 100 18)`);
    const ap = (a, sz, noBlades) => `<svg viewBox="-4 -4 208 208" width="${sz}" height="${sz}" style="overflow:visible">${noBlades ? apSvg.replace('id="blades"','id="blades" style="display:none"') : blades(a)}</svg>`;
    const rat = (open) => `<svg viewBox="0 0 140 110" width="260" height="204" class="rat">${ratSVG().replace(open ? 'M114 64 Q 119 67 125 64' : '###', 'M114 63 Q 119 70 125 63')}</svg>`;
    const pin = col => { const c = document.createElement("canvas"); c.width = 60; c.height = 80; const x = c.getContext("2d"); x.scale(2, 2);
      x.fillStyle = "rgba(0,0,0,.3)"; x.beginPath(); x.ellipse(18, 36, 6, 2.5, 0, 0, 7); x.fill();
      x.strokeStyle = "#111"; x.lineWidth = 2; x.beginPath(); x.moveTo(15, 35); x.lineTo(15, 13); x.stroke();
      x.fillStyle = col; x.strokeStyle = "#fff"; x.lineWidth = 2.5; x.beginPath(); x.arc(15, 10, 7.5, 0, 7); x.fill(); x.stroke(); return c.toDataURL(); };
    const star = () => { const c = document.createElement("canvas"); c.width = 120; c.height = 120; const x = c.getContext("2d"); x.scale(2, 2);
      x.strokeStyle = "rgba(155,59,42,.6)"; x.lineWidth = 3; x.beginPath(); x.arc(30, 30, 22, 0, 7); x.stroke();
      x.fillStyle = "#d8432f"; x.strokeStyle = "#000"; x.lineWidth = 1.5; x.beginPath();
      for (let i = 0; i < 10; i++) { const r = i % 2 ? 4 : 10, a = -Math.PI / 2 + i * Math.PI / 5; x.lineTo(30 + Math.cos(a) * r, 30 + Math.sin(a) * r); } x.closePath(); x.fill(); x.stroke(); return c.toDataURL(); };
    const C = CONFIG.colors;
    const swatch = (col, name) => `<figure><div class="sw" style="background:${col}"></div><figcaption>${name}<br>${col}</figcaption></figure>`;
    k.innerHTML = `
      <h3>Aperture (manhole cover)</h3><div class="row">
        ${fig(ap(3, 300), "Iris closed", "el-aperture-closed")}
        ${fig(ap(-20, 300), "Iris half open", "el-aperture-half")}
        ${fig(ap(-44, 300), "Iris open (play size)", "el-aperture-open")}
        ${fig(ap(0, 300, true), "Ring only (no blades)", "el-aperture-ring")}
        ${fig('<div id="steamDemo" style="width:120px;height:160px;background:radial-gradient(ellipse at 50% 80%, rgba(255,255,255,.55), transparent 65%);filter:blur(6px)"></div>', "Steam puff", "el-steam")}
      </div>
      <h3>Sal the Rat</h3><div class="row">
        ${fig(rat(false), "Sal — idle", "el-sal-idle")}
        ${fig(rat(true), "Sal — talking (mouth open)", "el-sal-talking")}
        ${fig(`<div class="kitbubble">Aperture's open. Whaddaya think? Want it bigger?</div>`, "Speech bubble", "el-bubble")}
      </div>
      <h3>Buttons</h3><div class="row">
        ${fig('<button class="btn">Ready</button>', "Primary (taxi yellow)", "el-btn-primary")}
        ${fig('<button class="btn alt">Bigger (85%)</button>', "Secondary (cream)", "el-btn-secondary")}
        ${fig('<button class="btn" disabled>Wide open</button>', "Disabled", "el-btn-disabled")}
        ${fig('<button class="btn" style="font-size:16px;padding:12px 20px">Lock it in</button>', "Lock in (map)", "el-btn-lock")}
        ${fig('<button class="btn round">+</button>', "Zoom in", "el-btn-zoom-in")}
        ${fig('<button class="btn round">−</button>', "Zoom out", "el-btn-zoom-out")}
        ${fig('<button class="btn round" style="font-size:16px">◎</button>', "Whole city", "el-btn-home")}
        ${fig('<button class="btn round" style="font-size:18px">🚇</button>', "Map helpers", "el-btn-helpers")}
        ${fig('<div class="pcount" style="display:flex;gap:8px"><button>1</button><button class="on">2</button><button>3</button><button>4</button></div>', "Player count picker", "el-player-picker")}
      </div>
      <h3>Map markers</h3><div class="row">
        ${["#111111", "#e0337a", "#1f6fd1", "#2a9d3f"].map((c, i) => fig(`<img src="${pin(c)}" width="30" height="40">`, "Pin — player " + (i + 1), "el-pin-p" + (i + 1))).join("")}
        ${fig(`<img src="${star()}" width="60" height="60">`, "Answer star + pulse", "el-target")}
      </div>
      <h3>Tags, chips, HUD</h3><div class="row">
        ${fig('<div style="background:#111;color:#fff;font:700 11px Helvetica;padding:2px 8px;border-radius:10px;border:2px solid #f7b500">TAP TO LOOK</div>', "Mini-aperture tag", "el-tag-tap")}
        ${fig('<span style="display:inline-block;background:#000;color:#f7b500;font-size:11px;letter-spacing:1px;padding:1px 6px;border-radius:4px;font-family:Oswald">GONE</span>', "Gone tag", "el-tag-gone")}
        ${fig('<div class="chip"><i style="background:#e0337a"></i><span>Mom\'s pin</span></div>', "Turn chip", "el-chip")}
        ${fig('<div class="gauges" style="display:flex;gap:6px;background:#111;padding:8px"><div class="gauge">ROUND<b>2/5</b></div><div class="gauge">SCORE<b>734,210</b></div></div>', "Header gauges", "el-gauges")}
        ${fig('<div style="background:#111;padding:4px 12px;border-radius:20px;border:1px solid #f7b500;color:#fff;font:600 13px Helvetica">Tap where you think it is</div>', "Hint pill", "el-hint")}
        ${fig('<div style="width:420px;position:relative;height:auto">' + document.getElementById("helpPanel").outerHTML.replace('class="hidden"', 'style="position:static;display:block"') + '</div>', "Map helpers panel", "el-helpers-panel")}
      </div>
      <h3>Cards</h3><div class="row">
        ${fig('<div class="card" style="width:360px"><div class="checker"></div><div class="in"><h2 style="font-size:26px">Real New Yorker</h2><div class="big">1,284,550</div><p>Sal says: “Alright. You can stay.”</p><button class="btn">Run it back</button></div><div class="checker"></div></div>', "Card (title / end screen)", "el-card")}
        ${fig('<div style="width:480px;position:relative;padding:8px 12px;border-radius:10px;color:#141414;background:#f2ead6;border:3px solid #000;box-shadow:4px 4px 0 #000"><div style="font-family:Bungee;font-size:15px">Ebbets Field <span style="background:#000;color:#f7b500;font-size:11px;padding:1px 6px;border-radius:4px;font-family:Oswald">GONE</span></div><div style="font:14px Oswald">Brooklyn · Demolished 1960 · you were 0.31 mi off (~6 blocks)</div><div style="font-family:Bungee;font-size:22px;color:#9b3b2a">+412,880</div></div>', "Result panel", "el-result")}
      </div>
      <h3>Palette</h3><div class="row">
        ${swatch("#f7b500", "Taxi yellow")}${swatch("#1d1e21", "Asphalt")}${swatch("#f2ead6", "Cream")}${swatch("#141414", "Ink")}${swatch("#9b3b2a", "Brick")}
        ${swatch(C.water, "Map water")}${swatch(C.land, "Map land")}${swatch(C.park, "Park")}${swatch(C.highway, "Highway")}${swatch(C.highwayEdge, "Highway edge")}${swatch(C.stream, "Creek")}
        ${swatch("#e0337a", "Player 2")}${swatch("#1f6fd1", "Player 3")}${swatch("#2a9d3f", "Player 4")}
      </div>
      <h3>Type</h3><div class="row">
        <figure><div style="font-family:Bungee;font-size:40px;color:#f7b500">YOU CALL YOURSELF</div><figcaption>Bungee — headings, buttons, numbers</figcaption></figure>
        <figure><div style="font-family:Oswald;font-size:30px">Sal the Rat's been under these streets</div><figcaption>Oswald — body text, Sal's lines</figcaption></figure>
        <figure><div style="font:700 26px Helvetica,Arial">Tap where you think it is</div><figcaption>Helvetica — map signage, chips</figcaption></figure>
      </div>`;
  });
  await sleep(1500);
  // whole sheet
  const kitEl = p.locator("#kit");
  await p.evaluate(() => { const k = document.getElementById("kit"); k.style.position = "absolute"; k.style.height = "auto"; k.style.overflow = "visible"; document.body.style.overflow = "visible"; document.documentElement.style.overflow = "visible"; });
  const H = await p.evaluate(() => document.getElementById("kit").scrollHeight + 60);
  await p.setViewportSize({ width: 1400, height: H });
  await sleep(500);
  await p.screenshot({ path: `${OUT}/sprite-sheet.png`, fullPage: true });
  // individual transparent pieces
  await p.evaluate(() => { document.getElementById("kit").style.background = "transparent"; document.body.style.background = "transparent"; document.documentElement.style.background = "transparent";
    for (const id of ["app", "stage", "titleScreen"]) { const e = document.getElementById(id); if (e) e.style.visibility = "hidden"; } });
  const ids = await p.$$eval("#kit .sp", els => els.map(e => e.id));
  for (const id of ids) await p.locator("#" + id).screenshot({ path: `${OUT}/elements/${id.replace(/^el-/, "")}.png`, omitBackground: true });
  console.log("elements:", ids.length);
  await p.close();
}

const LOG = [];
const log = (...a) => { console.log(...a); LOG.push(a.join(" ")); };
const browser = await chromium.launch();
for (const [name, fn] of [["kit", () => kit(browser)], ["phone", () => screens(browser, 390, 844, 3, "phone")], ["landscape", () => screens(browser, 1180, 820, 2, "landscape")]]) {
  try { await fn(); log("OK", name); } catch (e) { log("FAILED", name, e && e.stack || e); }
}
await browser.close();
fs.writeFileSync(OUT + "/log.txt", LOG.join("\n") + "\n");
