# Monster Pizza

The arcade for all of Stephen's games. Outside: the Monster Pizza shop on a busy street.
Inside: one long hallway of arcade cabinets you scroll sideways through. Click a cabinet to play.

## Files

```
index.html          the whole site (street, hallway, menu, game player)
games.js            THE LIST — edit this to add/remove games and walls
walls/              your hand-drawn wall tiles (optional)
games/<id>/         art for each cabinet
    marquee.png     the lit sign across the top of the cabinet
    screen.gif      what plays on the screen (GIF, PNG or JPG)
```

Missing art never breaks anything: no marquee → the title is written on the sign;
no screen GIF → the screen shows the title and a blinking PRESS START;
no walls → the built-in doodle walls are used.

## Add a game

1. Open `games.js` and copy one `{ ... }` block.
2. Change `id`, `title`, `blurb`, `url`, `color`.
3. Drop `marquee.png` and `screen.gif` into `games/<id>/`.
4. `git add . && git commit -m "add <game>" && git push`

The hallway grows by one wall per game. Order in the list = order on the wall.
Link straight to a game with `.../#<id>` (e.g. `#worst-commute`). `#arcade` skips the street.

Games open inside the site (with a "Back to the arcade" button) when it runs on github.io
or locally; anywhere else they open in a new tab. Force it either way with
`openInPage: true/false` at the top of `games.js`.

## The wall grid (for your drawings)

Every wall tile is one segment of hallway, **4:3** — draw at **1200 × 900 px** (or 1600 × 1200).
It stretches to the screen height, so keep everything in proportion, not pixel-exact.
Measurements below are % of the height (900px → 1% = 9px).

```
  0% ┌────────────────────────────────────────────────────────┐
     │ ceiling band                                           │
  8% ├────────────────────────────────────────────────────────┤  string of lights hangs to ~15%
     │ upper wall          ┌──────────┐                       │
     │  ┌─────────┐        │          │   ┌────────┐          │
     │  │ picture │        │ CABINET  │   │  NOTE  │ 24%–55%  │
     │  │  zone   │        │  ZONE    │   │  ZONE  │          │
 57% ├──┴─────────┴────────┤ keep     ├───┴────────┴──────────┤  chair rail
     │ lower wall          │  clear   │                       │
 81% ├─────────────────────┤          ├───────────────────────┤  baseboard
 83% │ floor               └──────────┘                       │  cabinet stands on ~84%
100% └────────────────────────────────────────────────────────┘
          cabinet zone: centered, 38% of height wide (x ≈ 429–771 px at 1200 wide), 15%–84% tall
          note zone:    starts 23% of height right of center, 22% wide
```

- **Edges must tile.** The left and right edges of every wall should line up with each other
  (ceiling line, chair rail, baseboard, floor) so any wall can sit next to any other.
- **Keep the cabinet zone plain** — the cabinet covers it.
- Put the fun stuff (frames, cracks, stains, posters) in the picture zone, lower wall, ceiling and floor.
- Add files to `walls/` and list them in `games.js` → `walls: [...]`. They cycle 1, 2, 3, 1, 2, 3...
- End pieces (`leftCap` exit door, `rightCap` "coming soon") are the same height and 60% as wide (540 × 900).

## Deploy

New GitHub repo (e.g. `monster-pizza`) → push these files → Settings → Pages → deploy from `main`.
Because your games live on the same `stephen-petronis.github.io` address, they play inside the site.
