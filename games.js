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
      title: "Nothin' But Net",
      blurb: "Off the bleachers, off the rim. Copy the trick shot or get a letter.",
      url: "https://stephen-petronis.github.io/NothinButNet/",
      marquee: "games/nothin-but-net/marquee.png",
      screen: "games/nothin-but-net/screen.gif",
      color: "#7b4bc4",
    },
    {
      id: "hoofbeat-hills",
      title: "Hoofbeat Hills",
      blurb: "Race a unicorn or a pegasus over the pastel hills. There's a secret third horse.",
      url: "https://stephen-petronis.github.io/hoofbeat-hills/",
      marquee: "games/hoofbeat-hills/marquee.png",
      screen: "games/hoofbeat-hills/screen.gif",
      color: "#e2608f",
    },
    {
      id: "shark-attack",
      title: "Shark Attack",
      blurb: "Point, click, take your turn, don't get eaten. Play with friends.",
      url: "https://stephen-petronis.github.io/sharkattack/",
      marquee: "games/shark-attack/marquee.png",
      screen: "games/shark-attack/screen.gif",
      color: "#1f9a8e",
    },
    {
      id: "cpm",
      title: "Chris the Project Manager",
      blurb: "Survive the commute, the office brawl and the pudding run.",
      url: "https://stephen-petronis.github.io/CPM/",
      marquee: "games/cpm/marquee.png",
      screen: "games/cpm/screen.gif",
      color: "#3c9a4e",
    },
  ],
};
