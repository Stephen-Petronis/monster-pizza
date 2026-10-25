# Monster Ice

NES-style 3-on-3 hockey with classic monsters. Spun off from Rec Center Hockey in Super Sullivan. Part of the Monster Pizza arcade.

**1 PLAYER:** choose **EASY** or **HARD**, pick 3 monsters (repeats allowed), face a random CPU team. EASY slows the whole game way down (the clock still runs in real time) so a younger kid can follow it; the CPU skates slower, shoots softer and less often, steals and hits less, and its goalie is slower, while you steal more and your shots sneak in more. HARD is full speed. Tune both in `CFG.difficulty` (a MEDIUM can be added there later). **2 PLAYERS (iPad only for now):** pick EASY (slow) or HARD (full speed); in 2-player it only changes the game speed. One iPad lying flat, Player 1 at the bottom, Player 2 at the top (their controls face them). **ZAMBONI:** just drive.

Games are **3 one-minute periods**. Tied after the third? **Sudden death:** the next goal wins.

**Turn your phone sideways** and the game switches to a controller layout: stick on the left, buttons and special on the right, rink in the middle. (2-player stays portrait.)

## Controls
| Touch | Keyboard (1 player) | Controller | What it does |
|---|---|---|---|
| Drag left side | Arrows or WASD | Stick or d-pad | Skate (the red ring and yellow arrow show who you are) |
| A | Z or Shift | A | Pass (with the puck) / swap player |
| B | SPACE | B or X | Shoot. Double-tap = slap shot. **Hold to charge**; let go at **MAX** for a monster FINISHER |
| B as a pass reaches you | SPACE | B | **One-timer.** Tap when the ring around you flashes gold for a PERFECT shot |
| B (defending) | SPACE | B | Poke check: steals the puck |
| B B (double-tap, defending) | SPACE SPACE | B B | Body check: knocks them flat (bounce off someone bigger and *you* go down) |
| Special bar | C | Y or a bumper | Fire the special when the bar is full |

Menus: arrows + Enter/Space (controller: d-pad + A or START). As soon as you press a key, the on-screen buttons show the key names.

**2 players on one computer:** P1 = WASD + **F** pass, **G** shoot, **H** special. P2 = Arrows + **J** pass, **K** shoot, **L** special. Or plug in two controllers (first one is P1).

**Passing back to your goalie:** he catches it, holds it a beat, then fires it out to your most open teammate. Opponents' shots still bounce off him.

## The monsters
| Monster | SPD | CHK | SHT | PAS | Special |
|---|---|---|---|---|---|
| Vampire | 3 | 3 | 3 | 4 | **Bite** – turns into a bat, flies to a foe (the puck carrier if close) and bites. That player joins your team for 15 seconds. |
| Werewolf | 5 | 2 | 2 | 2 | **Frenzy** – rips out of his jersey and grows. 5 seconds of super speed; stays your player (even after a pass) until you hit SWAP; can't be checked, and anyone he touches goes flying (and loses the puck). |
| Creature | 4 | 2 | 4 | 3 | **Dive** – swims under the ice. With the puck: pops up in the slot in front of the goal. Without: pops up under the puck carrier and steals it. |
| Mummy | 2 | 4 | 3 | 2 | **Wrap** – throws bandages at the carrier (or nearest foe); they're stuck for ~3 seconds and drop the puck. |
| Frankenstein | 1 | 5 | 5 | 1 | **Stomp** – lightning strike + shockwave knocks down everyone nearby; for 5 seconds after, his shots are lightning shots that go through the goalie. |

**Frankenstein is a wall:** he can only be checked by another Frankenstein or a Werewolf in frenzy (anyone else bounces off and goes down). A frenzied Werewolf can't be checked by anyone and hits wildly: bigger launches, longer knockdowns. Two frenzied Werewolves cancel each other out, and if they touch they go straight into a fight (even if there's already been one this game).

Stats work like NES Ice Hockey: high CHK strips the puck more easily and is harder to knock off it; Frankenstein is big and slow, the Werewolf is fast and easy to knock over. Every skater's special meter fills over time (~20s) and gets a boost from good checks. The CPU uses its specials too.

## Finishers
Hold SHOOT for 1 second without getting the puck stolen (you skate slowly while charging) and release at MAX **in the attacking zone** (past the blue line, in front of the net). Anywhere else a full charge is a hard power shot and the meter says GET CLOSER. Everyone freezes, your monster winds up, and the shot scores, knocking the goalie out and the net over:
- **Frankenstein – Thunder Slam:** lightning strike, then a stomp that knocks *everybody* down.
- **Vampire – Blood Moon:** a ring of bats, the puck flies in as a bat, the goalie is drained pale.
- **Creature – Tidal Wave:** a geyser under him, then a wall of spray that washes the goalie away.
- **Werewolf – Howl Spin:** pops the puck in the air, spins like a top and blasts it on fire.
- **Mummy – Tomb Shot:** bandages whirl around him and the goalie ends up wrapped.

PAS (passing) makes passes faster, more accurate and better led into your teammate's stride, and a good passer makes the one-timer window bigger.

## Drive the Zamboni
A no-pressure mode: cruise **the Rat Rod** (a rusty, flame-painted hot-rod Zamboni with a chrome blower and a little rat hood ornament) around a rink trashed after a night of monster hockey: snow, skate grooves, pumpkin guts, goo. The towel at the back lays down fresh glassy ice.
- Drag (or arrows) to drive; it turns gently toward where you point. **A / Z = HONK** (each monster has its own: AWOOOO!, BLEH BLEH!, BLUB BLUB!...). **B / SPACE = BOOST** (backfire, flames). **C** or tap the bar = swap driver.
- Tap the driver bar to swap which monster drives. Find the 4 lost things on the ice (an eyeball, a stinky sock...). A ghost drifts around saying BOO; honk to scare it off.
- Get it 97% clean for **SPOTLESS!**, then tap the bar to mess it up again.

## Fight!
The fight switches to 16-bit fighters: bigger, shaded monsters in full gear (numbered jerseys, gloves, breezers, striped socks, skates).

Once per game, the gloves come off: after 3 knockdowns (or the first one in the last 40 seconds), the next big hit starts a fight between the hitter and the one who got hit.
- **B = PUNCH.** Big monsters hit harder, fast ones punch quicker.
- **Hold A = BLOCK.** Blocked punches barely hurt.
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
- `skating-groove.mp3` (optional): menus and the Zamboni. Until it's added, the game song plays there too. The built-in chiptune only plays if no song file loads.

File names are in `CFG.music.tracks`; game-time volume is `CFG.music.gameVolume`.

## Tuning
All the knobs are in the `CFG` block at the top of the script: number and length of periods (`periods`, `periodMinutes`), skater size on the rink (`playerScale`), speeds, CPU difficulty, meter fill rate, every special's duration/size, the one-timer timing windows and goalie odds (`onetimer`), how long body-checked players stay down (`knockdown`), and how often the CPU body checks you (`cpuBodyCheck`), the power shot charge time and finisher scoring chance (`powerShot`), and everything about fights (`fight`: how many knockdowns start one, penalty time, special damage, counter timing window, CPU aggression).

## Head art
Stephen's monster heads (`art/monster-heads-sheet.png`) are cut into two atlases built into `index.html` (copies in `art/heads-16.png` and `art/heads-28.png`). Each row is one monster; columns 0–2 face right, 3–5 face left, 6–8 yell (shooting, specials, punching), 9–11 are mouth-wide-open (knocked down, stunned, getting hit), and column 12 is the big portrait (pick screen). Skaters switch heads based on which way they're skating and what's happening to them.

## Adding a monster
Copy an entry in `ROSTER`, add a row of heads to the head atlases (or draw a 7×7 fallback head), set stats, and either reuse an existing special in `power` (e.g. a Zombie that also uses `'mummy'`) or add a new `case` in `special()` (and a matching line in `aiSpecial()` so the CPU knows when to use it).

## High scores
Wins go on a top-5 board with arcade initials, saved on the device and shared through the `monster-pizza` Firebase project in the `mi_hockey` collection. The current Firestore rules only allow Super Sullivan's boards, so publish `firestore.rules` from this folder (it keeps Super Sullivan's boards and adds this one). Until then the board just stays on each device.
