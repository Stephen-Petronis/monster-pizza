// =====================================================================
//  MONSTER PIZZA — the arcade list
//  Add a game = add one block to `games`. The hallway grows by one wall.
//  Remove a game = delete its block. Order here = order on the wall.
// =====================================================================

window.MONSTER_PIZZA = {

  // Leave this out and games open inside the site on github.io, in a new tab elsewhere.
  // openInPage: true,

  // Your hand-drawn wall tiles. Leave empty to use the built-in doodle walls.
  // Each image should follow the wall grid in README.md (4:3, e.g. 1200x900).
  // They cycle: game 1 gets wall 1, game 2 gets wall 2 ... then it repeats.
  walls: [
    // "walls/wall-01.png",
    // "walls/wall-02.png",
    // "walls/wall-03.png",
  ],

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
