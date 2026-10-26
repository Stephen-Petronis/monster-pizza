# Monster Hockey: Ice Scream! — iPhone & iPad app

This folder turns the Monster Hockey web game into a real iOS app with **Capacitor**. The game itself is the same `index.html` as on Monster Pizza, bundled inside the app with the songs, so it plays offline. High scores and online play still work when there's internet.

## One-time setup on your Mac
1. Install **Xcode** from the Mac App Store and open it once (let it install its extras).
2. Install **Node.js** from https://nodejs.org (the LTS button).
3. Get this repo onto the Mac (GitHub Desktop, or `git clone https://github.com/Stephen-Petronis/monster-pizza`).
4. Open **Terminal**, go to this folder and run the setup:
   ```
   cd monster-pizza/apps/monster-hockey-ios
   npm run setup
   ```
   It installs Capacitor, makes the Xcode project (`ios/`), builds the icon and launch screen from `assets/`, sets full screen / no status bar, and opens Xcode.

## Run it on your iPhone or iPad
1. In Xcode: **Xcode > Settings > Accounts**, add your Apple ID (the one with the Developer Program).
2. Click **App** in the left sidebar > **Signing & Capabilities** > pick your **Team**. Bundle Identifier is `com.stephenpetronis.monsterhockey` (change it if Xcode says it's taken).
3. Plug in the device, pick it at the top of the Xcode window, press **Play**. (First time: on the device, Settings > Privacy & Security > **Developer Mode** on.)

## Put it on the App Store
1. Go to https://appstoreconnect.apple.com > **Apps > +  > New App**: iOS, name (e.g. *Monster Hockey: Ice Scream!* — must be unique on the store), the bundle ID above, SKU anything (`monsterhockey1`).
2. In Xcode: pick **Any iOS Device (arm64)** at the top, then **Product > Archive**. When it finishes: **Distribute App > App Store Connect > Upload**.
3. Back in App Store Connect fill in:
   - **Screenshots**: iPhone 6.9" and iPad 13" (Claude can make these).
   - **Description, keywords, support URL** (`https://stephen-petronis.github.io/monster-pizza/`).
   - **Privacy Policy URL**: `https://stephen-petronis.github.io/monster-pizza/privacy.html`
   - **App Privacy**: no data linked to the player; no tracking. (High scores store 3-letter initials + score.)
   - **Age rating**: cartoon/fantasy violence (the fights) — answer "infrequent/mild".
   - Pick the uploaded build, then **Submit for Review**. Usually a day or two.
4. Try it first with **TestFlight** (same upload) if you want friends to playtest before release.

## Updating the game later
When the web game changes on Monster Pizza, run `git pull` and then `npm run update-game` here (it copies the game in, bundles the font and builds the songs into the page so they play inside the app), then in Xcode bump the **Version/Build** number and Archive again.

## Swapping the icon
Replace `assets/icon-only.png` (1024×1024, no transparency) and `assets/splash.png` (2732×2732) with your own art, then run `npx capacitor-assets generate --ios`.

## Game Center (Apple matchmaking)
In the app, **PLAY ONLINE > FIND A MATCH** opens Apple's Game Center matchmaking screen: play a random opponent, or invite friends (Game Center friends or Messages). Invites open the app and drop both players into the game. Room codes are still there for playing someone on the website.

The native code is a small local plugin in `plugins/game-center` (Swift, `GameCenterPlugin.swift`); `npm run update-game` installs it and syncs it into Xcode.

One-time switches:
1. **Xcode:** click **App** > **Signing & Capabilities** > **+ Capability** > **Game Center**.
2. **App Store Connect:** your app > the version you're submitting > scroll to **Game Center** and turn it on (if it isn't already).
3. To test, you need **two real iPhones/iPads signed into different Apple IDs** with Game Center on (Settings > Game Center). The Simulator can't do matchmaking.
