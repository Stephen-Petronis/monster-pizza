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
# Google's own ID first, then the other ad buyers from Google's AdMob iOS setup guide (they let those buyers bid on our ads)
i=0
for id in cstr6suwn9 4fzdc2evr5 2fnua5tdw4 ydx93a7ass p78axxw29g v72qych5uu ludvb6z3bs cp8zw746q7 3sh42y64q3 c6k4g5qg8m \
  s39g8k73mm wg4vff78zm 3qy4746246 f38h382jlk hs6bdukanm mlmmfzh3r3 v4nxqhlyqp wzmmz9fp6w su67r6k2v3 yclnxrl5pm \
  t38b2kh725 7ug5zh24hu gta9lk7p23 vutu7akeur y5ghdn5j9k v9wttpbfk9 n38lu8286q 47vhws6wlr kbd757ywx3 9t245vhmpl \
  a2p9lx4jpn 22mmun2rn5 44jx6755aq k674qkevps 4468km3ulz 2u9pt9hc89 8s468mfl3y klf5c3l5u5 ppxm28t8ap kbmxgpxpgc \
  uw77j35x4d 578prtvx9j 4dzt52r2t5 tl55sbb4fm c3frkrj4fj e5fvkxwrpn 8c4e2ghe7u 3rd42ekr43 97r2b46745 3qcr597p9d; do
  /usr/libexec/PlistBuddy -c "Add :SKAdNetworkItems:$i dict" "$PL"
  /usr/libexec/PlistBuddy -c "Add :SKAdNetworkItems:$i:SKAdNetworkIdentifier string $id.skadnetwork" "$PL"
  i=$((i+1))
done
echo "Info.plist updated (AdMob app ID: $APPID)."
