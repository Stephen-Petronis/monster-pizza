#!/bin/bash
# One-time setup on the Mac: installs Capacitor, makes the Xcode project, icons and launch screen, opens Xcode.
set -e
cd "$(dirname "$0")/.."
command -v node >/dev/null || { echo "First install Node.js: https://nodejs.org (the LTS button), then run this again."; exit 1; }
xcode-select -p >/dev/null 2>&1 || { echo "First install Xcode from the Mac App Store and open it once, then run this again."; exit 1; }
echo "== Installing Capacitor =="
npm install
echo "== Bundling the pixel font =="
node scripts/localize-font.js
node scripts/pack-songs.js
echo "== Making the Xcode project =="
[ -d ios ] || npx cap add ios
echo "== Icons + launch screen (from the assets folder) =="
npx capacitor-assets generate --ios --iconBackgroundColor '#120a22' --iconBackgroundColorDark '#120a22' --splashBackgroundColor '#120a22' --splashBackgroundColorDark '#120a22'
echo "== App settings: full screen, no status bar =="
PL=ios/App/App/Info.plist
setp(){ /usr/libexec/PlistBuddy -c "Set :$1 $3" "$PL" 2>/dev/null || /usr/libexec/PlistBuddy -c "Add :$1 $2 $3" "$PL"; }
setp UIStatusBarHidden bool true
setp UIViewControllerBasedStatusBarAppearance bool false
setp UIRequiresFullScreen bool true
setp ITSAppUsesNonExemptEncryption bool false
setp CFBundleDisplayName string "Monster Hockey"
npx cap sync ios
echo "== Opening Xcode =="
npx cap open ios
