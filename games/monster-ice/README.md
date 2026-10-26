# Monster Hockey: "Ice Scream!"

(Folder and repo name: monster-ice.)

NES-style 3-on-3 hockey with classic monsters. Spun off from Rec Center Hockey in Super Sullivan. Part of the Monster Pizza arcade.

**1 PLAYER:** choose **EASY**, **HARD** or **NIGHTMARE**, pick 3 monsters (repeats allowed), face a random CPU team. EASY slows the whole game way down (the clock still runs in real time) so a younger kid can follow it; the CPU skates slower, shoots softer and less often, steals and hits less, and its goalie is slower, while you steal more and your shots sneak in more. HARD is full speed. **NIGHTMARE** is a step past HARD: the CPU skates faster, shoots harder and more often, steals and body checks more, and fills its specials faster; its goalie is quicker and yours a bit slower (wins show " NM" on the high score board). Special meters fill slower on NIGHTMARE (yours to 55%, the CPU's to 90%, fight specials to 60%), so pick your moment. Tune all three in `CFG.difficulty`. **PLAY ONLINE:** two devices, see below. **2P ON IPAD:** pick EASY (slow) or HARD (full speed); in 2-player it only changes the game speed. One iPad lying flat, Player 1 at the bottom, Player 2 at the top (their controls face them). **ZOMBONI:** offered as a 15-second break between periods (it's no longer on the title screen).

Games are **3 one-minute periods**. Tied after the third? **Sudden death:** the next goal wins.

**Turn your phone sideways** and the game switches to a controller layout: stick on the left, buttons and special on the right, rink in the middle. (2-player stays portrait.)

## Play online (2 devices)
**PLAY ONLINE** on the title screen. One player taps **HOST A GAME** and gets a 4-letter room code; the other taps **JOIN A GAME** and types it. The host picks the game speed, you each pick 3 monsters on your own device, a VS screen counts down 3-2-1, and you're on. The host is P1 (bottom net, shooting up), the guest is P2 (top net, shooting down). Specials, finishers and the fight all work; after the game, **PLAY AGAIN** keeps you connected and goes back to picking teams. If someone leaves mid-game, the CPU takes over their team.

How it works (all free): the two devices connect straight to each other (WebRTC). The `monster-pizza` Firebase project only passes the hello messages under the room code (collection `mi_rooms`; it stores nothing else). The host's device runs the game; the guest's sends its stick and buttons and draws the ~20-a-second snapshots the host sends back, sounds included.
- **Switch it on once:** paste `firestore.rules` into Firebase console > Firestore Database > Rules and Publish (it adds `mi_rooms`). Until then HOST says "ONLINE ISN'T SWITCHED ON YET".
- **Wi-Fi works best.** Some cell networks block direct connections; when that happens JOIN says it couldn't connect. Fixing that for every network needs a paid relay (TURN) server, or Apple's Game Center in an App Store version.
- Testing on one computer: open the game in two tabs with `#netlocal` at the end of the address (the hello goes through the browser instead of Firebase).

## Controls
| Touch | Keyboard (1 player) | Controller | What it does |
|---|---|---|---|
| Drag left side | WASD (or arrows) | Stick or d-pad | Skate (the red ring and yellow arrow show who you are) |
| A | SHIFT (or Z) | A | Pass (with the puck) / swap player |
| B | SPACE | B or X | Shoot. Double-tap = slap shot. **Hold to charge**; let go at **MAX** for a monster FINISHER |
| B as a pass reaches you | SPACE | B | **One-timer.** Tap when the ring around you flashes gold for a PERFECT shot |
| B (defending) | SPACE | B | Poke check: steals the puck |
| B B (double-tap, defending) | SPACE SPACE | B B | Body check: knocks them flat (bounce off someone bigger and *you* go down) |
| Special bar | E (or C) | Y or a bumper | Fire the special when the bar is full |

Menus: arrows + Enter/Space (controller: d-pad + A or START). As soon as you press a key, the on-screen buttons show the key names.

**2 players on one computer:** P1 = WASD + **F** pass, **G** shoot, **H** special. P2 = Arrows + **J** pass, **K** shoot, **L** special. Or plug in two controllers (first one is P1).

**Passing back to your goalie:** he catches it, holds it a beat, then fires it out to your most open teammate. Opponents' shots still bounce off him.

## The monsters
**MONSTERS** on the title screen (or **INFO** on the team pick) opens a player card for each monster: stats, what the special does, the finisher, the fight style, how long a bite lasts, pros and cons, plus a HOW TO WIN card with the hidden rules (blue line, finishers, one-timers, body checks, fights). Swipe or tap the arrows to flip. The card text lives in `CARDS` and `TIPS`.

| Monster | SPD | CHK | SHT | PAS | Special |
|---|---|---|---|---|---|
| Vampire | 3 | 3 | 3 | 4 | **Bite** – turns into a bat, flies to a foe (the puck carrier if close) and bites. That player joins your team for a while, depending on who got bitten: Frankenstein 8 seconds, Mummy 12, Werewolf and Creature 15, another Vampire only 5 (`CFG.special.biteTimes`). |
| Werewolf | 5 | 2 | 2 | 2 | **Frenzy** – rips out of his jersey and grows. 5 seconds of super speed; stays your player (even after a pass) until you hit SWAP; can't be checked, and anyone he touches goes flying (and loses the puck). |
| Creature | 4 | 2 | 4 | 3 | **Dive** – swims under the ice. With the puck: pops up in the slot in front of the goal. Without: pops up under the puck carrier and steals it. |
| Mummy | 2 | 4 | 3 | 2 | **Wrap** – throws bandages at the carrier (or nearest foe); they're stuck for ~3 seconds and drop the puck. |
| Frankenstein | 1 | 5 | 5 | 1 | **Stomp** – lightning strike + shockwave knocks down everyone nearby; for 5 seconds after, his shots are lightning shots that go through the goalie. |

**Frankenstein is a wall:** only another Frankenstein can knock him down: body checks, a frenzied Werewolf, stomps and finishers from anyone else leave him standing ("TOO BIG!"). You can still steal the puck from him, and anyone but a Frankenstein or a frenzied Werewolf who body checks him bounces off and goes down. A frenzied Werewolf can't be checked by anyone and hits wildly: bigger launches, longer knockdowns. Two frenzied Werewolves cancel each other out, and if they touch they go straight into a fight (even if there's already been one this game).

Stats work like NES Ice Hockey: high CHK strips the puck more easily and is harder to knock off it; Frankenstein is big and slow, the Werewolf is fast and easy to knock over. Every skater's special meter fills over time (~20s) and gets a boost from good checks. The CPU uses its specials too.

## No cheap goals
A shot (or a pass) taken from before your attacking blue line can't score: if it reaches the net, the goalie always turns it away ("TOO FAR!"), even a lightning shot. Get past the blue line first. The CPU follows the same rule and only shoots once it's past the line.

## Finishers
Hold SHOOT for 1 second without getting the puck stolen (you skate slowly while charging) and release at MAX **in the attacking zone** (past the blue line, in front of the net). Anywhere else a full charge is a hard power shot and the meter says GET CLOSER. Everyone freezes, your monster winds up, and the shot scores, knocking the goalie out and the net over:
- **Frankenstein – Thunder Slam:** lightning strike, then a stomp that knocks *everybody* down.
- **Vampire – Blood Moon:** a ring of bats, the puck flies in as a bat, the goalie is drained pale.
- **Creature – Tidal Wave:** a geyser under him, then a wall of spray that washes the goalie away.
- **Werewolf – Howl Spin:** pops the puck in the air, spins like a top and blasts it on fire.
- **Mummy – Tomb Shot:** bandages whirl around him and the goalie ends up wrapped.

PAS (passing) makes passes faster, more accurate and better led into your teammate's stride, and a good passer makes the one-timer window bigger.

## The Zomboni
A zombie Zamboni after Stephen's design (`art/zamboni-sheet.png`), hand-pixeled in code (`buildZomboni()`) so it stays crisp at game size: a side view with turning wheels (flipped for going left), the back going up the rink and the front coming down. The rink it cleans is trashed after a night of monster hockey: snow, skate grooves, blood splats and smears, skulls, eyeballs, pumpkin guts. The towel at the back lays down fresh glassy ice.
- **Between periods (optional):** when a period ends you get a **ZOMBONI BREAK?** card. Pick **DRIVE 15 SEC** to clean as much as you can in 15 seconds (CLEAN % and a rating at the end), then tap to play on: same game, next period. **SKIP** (or wait 8 seconds) goes straight on. The game song keeps playing. Turn the offer off with `CFG.zamboni.offer = false`.
- **From the title:** removed from the menu (the code is still there: `zamboniScene()`). It used to be the same 15-second run. At the end, tap the bar (or C) to go **AGAIN** with a fresh mess, or tap anywhere else to go back to the menu. Get it 97% clean before time's up for **SPOTLESS!**
- Drag (or arrows) to drive. **A / Z = HONK** (BRAAAINS!). **B / SPACE = BOOST** (backfire, flames). Find the lost things on the ice. **3 ghosts** drift around saying BOO. Drive into one and you're **SPOOKED!**: chilled to under half speed for 1.5 seconds (it also kills a turbo or boost). Honk to scare nearby ghosts off first. (`ghosts`, `slowTime`, `slowMult` in `CFG.zamboni`.)
- **Stephen's Zomboni panel:** the controls are Stephen's painted ZOMBONI art: zombie driver, icy title, the CLEAN bar and painted HONK / BOOST buttons. The game keeps the bar live (CLEAN % and lit segments; TAP: AGAIN at the end), flashes a button when it's pressed and shades BOOST while it recharges. Art: `art/zomboni-panel.png` in the source folder.
- **TURBOS:** 3 green bolt orbs sit on the ice, one in each third of the rink. Drive over one for 3 seconds of 1.8x speed (turning speeds up too). The machine is smaller (`size: 0.7`) with a 13px towel, and it cleans right up to the boards. 100% is possible but only with a clean line AND all 3 turbos: our test robot gets about 75% with no turbos and about 90% with all three.
- Speed, turning, boost, size, towel width, turbos, the timer and the offer time are in `CFG.zamboni`.

## Fight!
The fight switches to 16-bit fighters: bigger, shaded monsters in full gear (numbered jerseys, gloves, breezers, striped socks, skates).

Once per game, the gloves come off: after 3 knockdowns (or the first one in the last 40 seconds), the next big hit starts a fight between the hitter and the one who got hit.
- **B = PUNCH.** Big monsters hit harder, fast ones punch quicker.
- **Hold A = BLOCK.** Blocked punches barely hurt.
- **STAMINA** (the blue bar under health): every punch costs some, holding block drains it, and each punch you block chips at it. Rest and it refills. Too tired = no punch (TIRED!); if blocking runs it dry your guard breaks and you're dazed for a moment. No spamming.
- **Every monster fights differently:**
  - Frankenstein, *Heavy Hitter*: huge punches that crush a guard, but he tires fast.
  - Werewolf, *Flurry*: fast punches and the most stamina, but a weak guard and he takes extra damage.
  - Mummy, *Iron Guard*: blocking barely costs him anything, and he's tough to hurt.
  - Vampire, *Bloodsucker*: every punch that lands heals him a little.
  - Creature, *Slippery*: a bigger counter window and a faster special meter.
  The styles are in `FSTYLE` in the fight code (stamina, punch cost, block drain, damage...).
- **SPECIAL** (bar fills as you land and take hits): Thunder Punch, Bat Bite, Water Cannon, Claw Fury, Bandage Lash. It winds up for a second; in the last half second a ring appears on the defender with one blip and shrinks fast. **Tap BLOCK at the exact moment it turns gold (a ~0.06s window) to COUNTER** and the special hits the attacker instead. Just holding block cuts the damage.
- The winner finishes the loser monster-style: Frankenstein zaps him to an x-ray and a pile of ash, the Vampire drains him into a cloud of bats, the Creature drags him under the ice, the Werewolf spin-launches him into the stars, the Mummy wraps him up and slams a sarcophagus on him.
- The loser's team plays a man down for 3 seconds, then he skates back in.
- Any Vampire bites on the two fighters end when the fight starts, so you never fight (or send off) your own monster.

## The rink
Stephen's rink art (`art/rink-original.png`), with the ice markings faded way down so the play stands out, the crowd bobbing on 3 cheering frames, and the monster crowd, torches, skull banners and the scoreboard, which shows the real score, clock and period (HOME = you / P1, AWAY = CPU / P2). The art's nets were painted out so the game draws its own a little off the end boards. The game's boards and rounded corners line up with the art (the puck banks off them). The nets sit out from the end boards so you can skate behind them, and they're solid: the puck only goes in through the front.

## Music
Stephen's songs, looped, from files in the same folder as `index.html`:
- `halloween-arcade-run.mp3`: plays during hockey games (starts from the top each game).
- `fight-fight-fight.mp3`: when the gloves come off (the game song picks back up where it left off after the KO).
- `brains.mp3`: the Zomboni ("Brains"). The game song picks back up where it left off after the break.
- `skating-groove.mp3` (optional): menus and the Zamboni. Until it's added, the game song plays there too. The built-in chiptune only plays if no song file loads.

Sound cues: in the **last 5 seconds** of every period the music dips and the clock beeps each second (the last beep is higher), and every **goal** sets off a Bride-of-Frankenstein scream siren (a rising, wobbling wail over a siren, ending in her hiss) while the music dips under it. Online, the guest hears all of it too.

File names are in `CFG.music.tracks`; game-time volume is `CFG.music.gameVolume`.

## Tuning
All the knobs are in the `CFG` block at the top of the script: number and length of periods (`periods`, `periodMinutes`), skater size on the rink (`playerScale`), speeds, CPU difficulty, meter fill rate, every special's duration/size, the one-timer timing windows and goalie odds (`onetimer`), how long body-checked players stay down (`knockdown`), and how often the CPU body checks you (`cpuBodyCheck`), the power shot charge time and finisher scoring chance (`powerShot`), and everything about fights (`fight`: how many knockdowns start one, penalty time, special damage, counter timing window, CPU aggression).

## Head art
Stephen's monster heads (`art/monster-heads-sheet.png`) are cut into two atlases built into `index.html` (copies in `art/heads-16.png` and `art/heads-28.png`). Each row is one monster; columns 0–2 face right, 3–5 face left, 6–8 yell (shooting, specials, punching), 9–11 are mouth-wide-open (knocked down, stunned, getting hit), and column 12 is the big portrait (pick screen). Skaters switch heads based on which way they're skating and what's happening to them.

## Adding a monster
Copy an entry in `ROSTER`, add a row of heads to the head atlases (or draw a 7×7 fallback head), set stats, and either reuse an existing special in `power` (e.g. a Zombie that also uses `'mummy'`) or add a new `case` in `special()` (and a matching line in `aiSpecial()` so the CPU knows when to use it).

## High scores: Best Zomboni Drivers
The high score board is the Zomboni: after a 1-player Zomboni break between periods, your CLEAN % (to one decimal; the rink is measured on a fine 2px grid) goes on a top-5 board with arcade initials. 2-player and online games don't count. Saved on the device and shared through the `monster-pizza` Firebase project in the `mi_zomboni` collection; publish `firestore.rules` from this folder once so the shared board works (until then it stays on each device). Hockey wins no longer go on a board.
