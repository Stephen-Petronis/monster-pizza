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

## Walls

Wall tiles are laid side by side behind the whole hallway, picked at random by `weight`
in `games.js` (plain wall 6, special walls 1 each, so about 3 in 4 are plain). Two special
walls never sit next to each other, and the hallway always starts on a plain one.

Rules for new wall art:
- **Same height as the others** (current tiles are 972 x 1619). Width can be anything.
- **Left and right edges match**: ceiling beam, wallpaper top, red rail, baseboard all at the same heights.
- **Floor starts at 84%** down. The floor in the wall art is covered by `walls/floor.jpg`,
  a straight-on strip cut from your floor so it repeats without seams.
- Cabinets stand in the middle of the screen from ~15% to 84% tall and cover whatever is behind them,
  so detailed walls get partly hidden sometimes. That's fine.

Drop a new file in `walls/` and add a line to `walls: [...]`.

`templates/` has the original grid guides (made for the old 4:3 layout; the heights still apply).

## Deploy

New GitHub repo (e.g. `monster-pizza`) → push these files → Settings → Pages → deploy from `main`.
Because your games live on the same `stephen-petronis.github.io` address, they play inside the site.
