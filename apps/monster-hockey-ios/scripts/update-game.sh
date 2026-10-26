#!/bin/bash
# Copy the latest web version of the game (from the Monster Pizza site folder) into the app, then sync it into Xcode.
set -e
cd "$(dirname "$0")/.."
cp ../../games/monster-ice/index.html www/
cp ../../games/monster-ice/*.mp3 www/
node scripts/localize-font.js
node scripts/pack-songs.js
[ -d ios ] && npx cap sync ios
echo "Game updated in the app. In Xcode, press Play (or Product > Archive for a new App Store build)."
