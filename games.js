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

  // Where the exit door goes. Paste the Sylli Town itch.io link here.
  // Leave it empty and the door goes back out to the Monster Pizza street.
  exitUrl: "https://stephen-petronis.itch.io/syllitown",
  exitLabel: "SYLLI TOWN",

  // The gift shop window at the end of the hallway. The first 3 items show up in the window.
  // For each item: a picture, a price, and the link to buy it (Etsy, Shopify, Printful, etc.).
  // soon: true shows it as COMING SOON and doesn't link anywhere.
  shop: {
    storeUrl: "",            // link to the whole store, shown at the top of the shop
    items: [
      { name: "Monster Pizza Tee",        image: "art/logo.webp",                      price: "", url: "", soon: true },
      { name: "Hoofbeat Hills Sticker",   image: "games/hoofbeat-hills/cabinet.webp",  price: "", url: "", soon: true },
      { name: "Whack-A-Ghost Poster",     image: "games/whack-a-ghost/cabinet.webp",   price: "", url: "", soon: true },
      { name: "Nothing But Net Sticker",  image: "games/nothin-but-net/cabinet.webp",  price: "", url: "", soon: true },
      { name: "Worst Commute Mug",        image: "games/worst-commute/cabinet.webp",   price: "", url: "", soon: true },
      { name: "Shuck Shack Sticker",      image: "games/shuck-shack/cabinet.webp",     price: "", url: "", soon: true },
    ],
  },
  rightCap: "",  // the "more games coming" end

  games: [
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
    {
      id: "worst-commute",                 // short name, used for links like monsterpizza/#worst-commute
      title: "The Worst Commute",
      blurb: "Get Jason from Borough Hall to the office in one piece.",
      url: "https://stephen-petronis.github.io/worst-commute/",
      cabinet: "games/worst-commute/cabinet.webp",  // drawn cabinet, cut out on transparent
      screen: "games/worst-commute/screen.gif",     // gameplay GIF that plays on the drawn glass
      screenBox: [17.5, 24.4, 65, 23],              // left, top, width, height of the glass, in % of the cabinet art
      color: "#2f7fd0",                              // cabinet paint
    },
    {
      id: "nothin-but-net",
      title: "Nothing But Net",
      blurb: "Off the bleachers, off the rafters. 8 courts, 8 snacks, 1 legend.",
      url: "https://stephen-petronis.github.io/NothinButNet/",
      cabinet: "games/nothin-but-net/cabinet.webp",
      screen: "games/nothin-but-net/screen.gif",
      screenBox: [23.5, 25.2, 53, 21],
      color: "#7b4bc4",
    },
    {
      id: "hoofbeat-hills",
      title: "Hoofbeat Hills",
      blurb: "Race horses through 19 wild worlds, befriend the bosses with a dance party, and hit STAR TURBO.",
      url: "https://stephen-petronis.github.io/hoofbeat-hills/",
      // A full drawn cabinet replaces the built-in one. Cut out on a transparent background.
      cabinet: "games/hoofbeat-hills/cabinet.webp",
      screen: "games/hoofbeat-hills/screen.gif",
      screenBox: [22, 24.6, 56, 22],
      color: "#e2608f",
    },
    {
      id: "cpm",
      title: "Chris the Project Manager",
      blurb: "Survive the commute, the office brawl and the pudding run.",
      url: "https://stephen-petronis.github.io/CPM/",
      cabinet: "games/cpm/cabinet.webp",
      screen: "games/cpm/screen.gif",
      screenBox: [22, 24, 56, 22.5],
      color: "#3c9a4e",
    },
    {
      id: "shuck-shack",
      title: "Shuck Shack",
      blurb: "Trace the shell, pop the top, fill the order. Watch your fingers.",
      url: "https://stephen-petronis.github.io/shuck-shack/",
      cabinet: "games/shuck-shack/cabinet.webp",
      screen: "games/shuck-shack/screen.gif",
      screenBox: [22.6, 25.2, 54.7, 21],
      color: "#d9862b",
    },
    {
      id: "super-sullivan",
      title: "Super Sullivan",
      blurb: "Blow out the candles, pop the cake goblins, backflip the dirt bike, and win the big game.",
      url: "https://stephen-petronis.github.io/super-sullivan/",
      cabinet: "games/super-sullivan/cabinet.webp",
      screen: "games/super-sullivan/screen.gif",
      screenBox: [20.3, 25.9, 59.4, 25.5],
      color: "#1d4fd8",
    },
    {
      id: "fairy-garden",
      title: "Fairy Garden",
      blurb: "Fly out for seeds, grow a magic garden, brew potions and make bug friends.",
      url: "games/fairy-garden/index.html",           // lives inside this repo
      screen: "games/fairy-garden/screen.gif",        // no drawn cabinet yet: uses the built-in one
      color: "#ff6fae",
    },
  ],
};
