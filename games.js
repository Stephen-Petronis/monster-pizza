// =====================================================================
//  MONSTER PIZZA — the arcade list
//  Add a game = add one block to `games`. The hallway grows by one wall.
//  Remove a game = delete its block. Order here = order on the wall.
// =====================================================================

window.MONSTER_PIZZA = {

  // Leave this out and games open inside the site on github.io, in a new tab elsewhere.
  // openInPage: true,

  // Your hand-drawn wall tiles. They're laid side by side behind the whole hallway,
  // picked at random. Higher weight = shows up more often. Two "special" walls
  // never land next to each other. Any width works; all should be the same height.
  // Leave the list empty to use the built-in doodle walls.
  walls: [
    { src: "walls/wall-plain.jpg",   weight: 6 },   // the everyday wall
    { src: "walls/wall-peeling.jpg", weight: 1 },
    { src: "walls/wall-frames.jpg",  weight: 1 },
  ],

  // One straight-on floor tile that repeats under everything, and how far down
  // (in % of the wall height) your floor starts in the wall art.
  floor: "walls/floor.jpg",
  floorTop: 84,

  // Optional art for the two ends of the hallway (same height as a wall,
  // 60/100 as wide — e.g. 540x900). Leave blank for the built-in doodles.
  leftCap: "",   // the exit door back outside
  rightCap: "",  // the "more games coming" end

  games: [
    {
      id: "worst-commute",                 // short name, used for links like monsterpizza/#worst-commute
      title: "The Worst Commute",
      blurb: "Get Jason from Borough Hall to the office in one piece.",
      url: "https://stephen-petronis.github.io/worst-commute/",
      marquee: "games/worst-commute/marquee.png",   // art across the top of the cabinet
      screen: "games/worst-commute/screen.gif",     // GIF (or PNG/JPG) that plays on the screen
      color: "#2f7fd0",                              // cabinet paint
    },
    {
      id: "nothin-but-net",
      title: "Nothing But Net",
      blurb: "Off the bleachers, off the rafters. 8 courts, 8 snacks, 1 legend.",
      url: "https://stephen-petronis.github.io/NothinButNet/",
      cabinet: "games/nothin-but-net/cabinet.webp",
      // screen: "games/nothin-but-net/screen.gif",
      // screenBox: [27, 25.5, 46, 20],
      color: "#7b4bc4",
    },
    {
      id: "hoofbeat-hills",
      title: "Hoofbeat Hills",
      blurb: "Race horses through 19 wild worlds, befriend the bosses with a dance party, and hit STAR TURBO.",
      url: "https://stephen-petronis.github.io/hoofbeat-hills/",
      // A full drawn cabinet replaces the built-in one. Cut out on a transparent background.
      cabinet: "games/hoofbeat-hills/cabinet.webp",
      // Want a GIF playing on the drawn screen? Add it and uncomment both lines.
      // screen: "games/hoofbeat-hills/screen.gif",
      // screenBox: [22, 24.6, 56, 22],   // left, top, width, height of the glass, in % of the cabinet art
      color: "#e2608f",
    },
    {
      id: "cpm",
      title: "Chris the Project Manager",
      blurb: "Survive the commute, the office brawl and the pudding run.",
      url: "https://stephen-petronis.github.io/CPM/",
      cabinet: "games/cpm/cabinet.webp",
      // screen: "games/cpm/screen.gif",
      // screenBox: [22, 24, 56, 22.5],   // left, top, width, height of the glass, in % of the cabinet art
      color: "#3c9a4e",
    },
    {
      id: "shuck-shack",
      title: "Shuck Shack",
      blurb: "Trace the shell, pop the top, fill the order. Watch your fingers.",
      url: "https://stephen-petronis.github.io/shuck-shack/",
      cabinet: "games/shuck-shack/cabinet.webp",
      // The gameplay is painted on the glass. To play a GIF there instead, add it and uncomment:
      // screen: "games/shuck-shack/screen.gif",
      // screenBox: [22.5, 25.4, 54.8, 21.2],
      color: "#d9862b",
    },
    {
      id: "whack-a-ghost",
      title: "Whack-A-Ghost",
      blurb: "Pop the ghosts, spare the kitties, grab the hearts. Boss every 3 rounds.",
      url: "games/whack-a-ghost/index.html",          // lives inside this repo
      cabinet: "games/whack-a-ghost/cabinet.webp",
      screen: "games/whack-a-ghost/screen.gif",       // plays on the drawn glass
      screenBox: [24.5, 25.6, 51, 20],
      color: "#7a5a40",
    },
  ],
};
