#!/bin/bash
# Copy the latest web version of the game (from the Monster Pizza site folder) into the app, then sync it into Xcode.
set -e
cd "$(dirname "$0")/.."
mkdir -p www && cp ../../games/monster-ice/index.html www/
cp ../../games/monster-ice/*.mp3 www/
node scripts/localize-font.js
node scripts/pack-songs.js
[ -d ios ] && npx capacitor-assets generate --ios --iconBackgroundColor '#120a22' --iconBackgroundColorDark '#120a22' --splashBackgroundColor '#120a22' --splashBackgroundColorDark '#120a22' >/dev/null && echo 'Icon + launch screen updated.'
npm install --no-audit --no-fund >/dev/null   # picks up the Game Center plugin (plugins/game-center)
[ -d ios ] && npx cap sync ios
echo "Game updated in the app. In Xcode, press Play (or Product > Archive for a new App Store build)."
