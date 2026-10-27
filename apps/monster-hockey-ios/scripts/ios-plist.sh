#!/bin/bash
# App settings in ios/App/App/Info.plist: full screen, no status bar, and what Google AdMob needs.
set -e
cd "$(dirname "$0")/.."
PL=ios/App/App/Info.plist
[ -f "$PL" ] || exit 0
setp(){ /usr/libexec/PlistBuddy -c "Set :$1 $3" "$PL" 2>/dev/null || /usr/libexec/PlistBuddy -c "Add :$1 $2 $3" "$PL"; }
setp UIStatusBarHidden bool true
setp UIViewControllerBasedStatusBarAppearance bool false
setp UIRequiresFullScreen bool true
setp ITSAppUsesNonExemptEncryption bool false
setp CFBundleDisplayName string "Monster Hockey"
# AdMob: the app ID (from admob.json) and Google's ad network ID
APPID=$(node -e "console.log(require('./admob.json').iosAppId)")
setp GADApplicationIdentifier string "$APPID"
/usr/libexec/PlistBuddy -c "Delete :SKAdNetworkItems" "$PL" 2>/dev/null || true
/usr/libexec/PlistBuddy -c "Add :SKAdNetworkItems array" "$PL"
/usr/libexec/PlistBuddy -c "Add :SKAdNetworkItems:0 dict" "$PL"
/usr/libexec/PlistBuddy -c "Add :SKAdNetworkItems:0:SKAdNetworkIdentifier string cstr6suwn9.skadnetwork" "$PL"
echo "Info.plist updated (AdMob app ID: $APPID)."
