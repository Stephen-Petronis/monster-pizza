import Foundation
import UIKit
import Capacitor
import GameKit

/// Apple Game Center for Monster Hockey.
///
/// The game (a web page) calls:
///   GameCenter.findMatch()    -> shows Apple's matchmaking screen (invite friends / Messages / SharePlay, or automatch)
///   GameCenter.quickMatch()   -> automatch with NO Apple screen (the game shows its own searching screen)
///   GameCenter.cancelSearch() -> stops a quickMatch search
///   GameCenter.send({ d, fast }) -> sends one message (a JSON string) to the other player
///   GameCenter.disconnect()   -> leaves the match
/// and listens for these events:
///   "match"  { host: Bool, other: String }  both players are connected; host runs the game
///   "cancel" {}                             the player closed Apple's screen
///   "fail"   { msg: String }                couldn't sign in or make a match
///   "data"   { d: String }                  a message from the other player
///   "left"   {}                             the other player left / the connection dropped
/// Invites accepted from Messages or Game Center (even when the app wasn't open) also end in "match".
///
/// All plugin state is only touched on the main thread.
@objc(GameCenterPlugin)
public class GameCenterPlugin: CAPPlugin, CAPBridgedPlugin, GKMatchmakerViewControllerDelegate, GKMatchDelegate, GKLocalPlayerListener {
    public let identifier = "GameCenterPlugin"
    public let jsName = "GameCenter"
    public let pluginMethods: [CAPPluginMethod] = [
        CAPPluginMethod(name: "status", returnType: CAPPluginReturnPromise),
        CAPPluginMethod(name: "findMatch", returnType: CAPPluginReturnPromise),
        CAPPluginMethod(name: "quickMatch", returnType: CAPPluginReturnPromise),
        CAPPluginMethod(name: "cancelSearch", returnType: CAPPluginReturnPromise),
        CAPPluginMethod(name: "send", returnType: CAPPluginReturnPromise),
        CAPPluginMethod(name: "disconnect", returnType: CAPPluginReturnPromise)
    ]

    private var match: GKMatch?
    private var started = false
    private var signInScreen: UIViewController?
    private var matchScreen: GKMatchmakerViewController?   // Apple's matchmaking screen we put up (if any)
    private var listening = false
    private var wantsMatch = false   // tapped FIND A MATCH / QUICK MATCH before sign-in finished
    private var wantsQuick = false   // ...and it was QUICK MATCH (no Apple screen)
    private var searching = false    // QUICK MATCH is looking for someone
    private var searchGen = 0        // which QUICK MATCH tap the current search belongs to
    private var quickMisses = 0      // searches in a row that failed right away

    // MARK: sign in (quietly at launch; the sign-in screen only shows when they ask for a match)

    override public func load() {
        DispatchQueue.main.async { self.authenticate() }
    }

    private func authenticate() {
        GKLocalPlayer.local.authenticateHandler = { [weak self] viewController, _ in
            DispatchQueue.main.async {
                guard let self = self else { return }
                if let viewController = viewController {
                    self.signInScreen = viewController
                    if self.wantsMatch { self.show(viewController) }
                    return
                }
                self.signInScreen = nil
                if GKLocalPlayer.local.isAuthenticated {
                    if !self.listening {
                        self.listening = true
                        GKLocalPlayer.local.register(self)   // so invites reach us
                    }
                    if self.wantsMatch {
                        self.wantsMatch = false
                        if self.wantsQuick { self.startQuickMatch() } else { self.openMatchmaker() }
                    }
                } else if self.wantsMatch {
                    self.wantsMatch = false
                    self.notifyListeners("fail", data: ["msg": "SIGN IN TO GAME CENTER IN SETTINGS"])
                }
            }
        }
    }

    @objc func status(_ call: CAPPluginCall) {
        DispatchQueue.main.async {
            let me = GKLocalPlayer.local
            // alias = the Game Center nickname (displayName can be "Me" for the local player)
            call.resolve(["signedIn": me.isAuthenticated, "name": me.isAuthenticated ? me.alias : ""])
        }
    }

    // MARK: matchmaking

    @objc func findMatch(_ call: CAPPluginCall) {
        DispatchQueue.main.async {
            self.signInThen(quick: false)
            call.resolve()
        }
    }

    /// QUICK MATCH: Apple's automatch with no Apple screen; the game draws its own "searching" screen.
    @objc func quickMatch(_ call: CAPPluginCall) {
        DispatchQueue.main.async {
            self.signInThen(quick: true)
            call.resolve()
        }
    }

    @objc func cancelSearch(_ call: CAPPluginCall) {
        DispatchQueue.main.async {
            self.wantsMatch = false
            if self.searching {
                self.searching = false
                GKMatchmaker.shared().cancel()
            }
            call.resolve()
        }
    }

    /// Keeps searching until a match is found or they tap CANCEL: when Apple's search gives up
    /// with nobody found, a fresh one starts. Setup problems (sign-in, Game Center off) stop it with a message.
    private func startQuickMatch() {
        if searching { return }
        searching = true
        searchGen += 1
        quickMisses = 0
        searchOnce(gen: searchGen)
    }

    private func searchOnce(gen: Int) {
        let request = GKMatchRequest()
        request.minPlayers = 2
        request.maxPlayers = 2
        let began = Date()
        GKMatchmaker.shared().findMatch(for: request) { [weak self] found, error in
            DispatchQueue.main.async {
                guard let self = self else { return }
                guard self.searching, gen == self.searchGen else { found?.disconnect(); return }   // cancelled or replaced
                if let found = found {
                    self.searching = false
                    self.begin(found)
                    return
                }
                // A search that fails within a couple of seconds over and over means something's wrong (no internet).
                if Date().timeIntervalSince(began) < 2 { self.quickMisses += 1 } else { self.quickMisses = 0 }
                if self.keepLooking(error) && self.quickMisses < 5 {
                    DispatchQueue.main.asyncAfter(deadline: .now() + (self.quickMisses > 0 ? 2 : 0.3)) {
                        if self.searching && gen == self.searchGen { self.searchOnce(gen: gen) }
                    }
                } else {
                    self.searching = false
                    self.notifyListeners("fail", data: ["msg": self.failMessage(error)])
                }
            }
        }
    }

    private func keepLooking(_ error: Error?) -> Bool {
        guard let error = error else { return true }
        let ns = error as NSError
        guard ns.domain == GKErrorDomain, let code = GKError.Code(rawValue: ns.code) else { return true }
        switch code {
        case .gameUnrecognized, .notSupported, .apiNotAvailable, .notAuthenticated, .invalidCredentials,
             .authenticationInProgress, .underage, .parentalControlsBlocked, .notAuthorized, .cancelled, .matchRequestInvalid:
            return false
        default:
            return true
        }
    }

    private func signInThen(quick: Bool) {
        self.wantsQuick = quick
        if GKLocalPlayer.local.isAuthenticated {
            if quick { self.startQuickMatch() } else { self.openMatchmaker() }
        } else if let screen = self.signInScreen {
            self.wantsMatch = true
            self.show(screen)
        } else {
            // Apple stops offering the sign-in screen after the player cancels it; they have to use Settings.
            self.wantsMatch = true
            self.authenticate()
            DispatchQueue.main.asyncAfter(deadline: .now() + 4) {
                if self.wantsMatch && !GKLocalPlayer.local.isAuthenticated && self.signInScreen == nil {
                    self.wantsMatch = false
                    self.notifyListeners("fail", data: ["msg": "SIGN IN TO GAME CENTER IN SETTINGS"])
                }
            }
        }
    }

    private func openMatchmaker(recipients: [GKPlayer]? = nil) {
        // Already showing Apple's screen (double tap): leave it alone, unless this is a pick-friends request.
        if let current = matchScreen, current.presentingViewController != nil, recipients == nil { return }
        let request = GKMatchRequest()
        request.minPlayers = 2
        request.maxPlayers = 2
        if let recipients = recipients { request.recipients = recipients }
        guard let screen = GKMatchmakerViewController(matchRequest: request) else {
            notifyListeners("fail", data: ["msg": "GAME CENTER ISN'T READY"])
            return
        }
        present(matchmaker: screen)
    }

    /// Puts up a matchmaking screen, quietly replacing one that's already up (e.g. an invite arrives while browsing).
    private func present(matchmaker screen: GKMatchmakerViewController) {
        screen.matchmakerDelegate = self
        if let old = matchScreen, old !== screen, old.presentingViewController != nil {
            old.matchmakerDelegate = nil
            matchScreen = screen
            old.dismiss(animated: false) { self.show(screen) }
            return
        }
        matchScreen = screen
        show(screen)
    }

    private func closeMatchmaker(_ viewController: GKMatchmakerViewController) {
        if matchScreen === viewController { matchScreen = nil }
        viewController.matchmakerDelegate = nil
        viewController.dismiss(animated: true)
    }

    public func matchmakerViewControllerWasCancelled(_ viewController: GKMatchmakerViewController) {
        DispatchQueue.main.async {
            self.closeMatchmaker(viewController)
            self.notifyListeners("cancel", data: [:])
        }
    }

    public func matchmakerViewController(_ viewController: GKMatchmakerViewController, didFailWithError error: Error) {
        DispatchQueue.main.async {
            self.closeMatchmaker(viewController)
            self.notifyListeners("fail", data: ["msg": self.failMessage(error)])
        }
    }

    /// Says what went wrong in words a player can act on (the number helps us debug).
    private func failMessage(_ error: Error?) -> String {
        guard let error = error else { return "NO MONSTERS FOUND. TRY AGAIN!" }
        let ns = error as NSError
        if ns.domain == GKErrorDomain, let code = GKError.Code(rawValue: ns.code) {
            switch code {
            case .gameUnrecognized, .notSupported, .apiNotAvailable:
                return "GAME CENTER ISN'T SWITCHED ON FOR THIS APP YET (\(ns.code))"
            case .notAuthenticated, .invalidCredentials, .authenticationInProgress:
                return "SIGN IN TO GAME CENTER IN SETTINGS (\(ns.code))"
            case .underage, .parentalControlsBlocked, .notAuthorized:
                return "MULTIPLAYER IS TURNED OFF ON THIS PHONE (\(ns.code))"
            case .communicationsFailure, .connectionTimeout:
                return "NO MONSTERS FOUND. CHECK YOUR INTERNET (\(ns.code))"
            case .cancelled:
                return "SEARCH STOPPED"
            default:
                return "NO MONSTERS FOUND. TRY AGAIN! (\(ns.code))"
            }
        }
        return "NO MONSTERS FOUND. TRY AGAIN! (\(ns.code))"
    }

    public func matchmakerViewController(_ viewController: GKMatchmakerViewController, didFind match: GKMatch) {
        DispatchQueue.main.async {
            self.closeMatchmaker(viewController)
            self.begin(match)
        }
    }

    // Someone accepted an invite (Messages or Game Center), maybe launching the app to do it.
    public func player(_ player: GKPlayer, didAccept invite: GKInvite) {
        DispatchQueue.main.async {
            guard let screen = GKMatchmakerViewController(invite: invite) else { return }
            self.present(matchmaker: screen)
        }
    }

    // They picked friends to play from the Game Center app / dashboard.
    public func player(_ player: GKPlayer, didRequestMatchWithRecipients recipientPlayers: [GKPlayer]) {
        DispatchQueue.main.async { self.openMatchmaker(recipients: recipientPlayers) }
    }

    private func begin(_ newMatch: GKMatch) {
        if let old = match, old !== newMatch { old.delegate = nil; old.disconnect() }
        match = newMatch
        started = false
        newMatch.delegate = self
        startIfReady()
    }

    /// Both phones decide the host the same way (lowest player ID), so no extra messages are needed.
    private func startIfReady() {
        guard let m = match, !started, m.expectedPlayerCount == 0, let other = m.players.first else { return }
        started = true
        let mine = GKLocalPlayer.local.gamePlayerID
        let theirs = other.gamePlayerID
        // IDs should never match; if they somehow do, fall back to the names so exactly one side hosts.
        let host = mine != theirs ? mine < theirs : GKLocalPlayer.local.alias < other.alias
        // Kept until the page listens, so a match made from a cold-launch invite isn't lost.
        notifyListeners("match", data: ["host": host, "other": other.displayName], retainUntilConsumed: true)
    }

    /// Drops the current match. If it never got going, tell the page so it doesn't wait forever.
    private func endMatch(_ m: GKMatch) {
        guard m === match else { return }
        let wasStarted = started
        m.delegate = nil
        m.disconnect()
        match = nil
        started = false
        if wasStarted {
            notifyListeners("left", data: [:])
        } else {
            notifyListeners("fail", data: ["msg": "COULDN'T MAKE A MATCH"])
        }
    }

    // MARK: messages

    @objc func send(_ call: CAPPluginCall) {
        guard let text = call.getString("d"), let data = text.data(using: .utf8) else { call.resolve(); return }
        let fast = call.getBool("fast") ?? false
        DispatchQueue.main.async {
            if let m = self.match, self.started {
                // fast = position snapshots: fine to lose one now and then (Apple caps those at about 1000 bytes)
                try? m.sendData(toAllPlayers: data, with: (fast && data.count < 1000) ? .unreliable : .reliable)
            }
            call.resolve()
        }
    }

    public func match(_ match: GKMatch, didReceive data: Data, fromRemotePlayer player: GKPlayer) {
        guard let text = String(data: data, encoding: .utf8) else { return }
        DispatchQueue.main.async {
            guard match === self.match, self.started else { return }
            self.notifyListeners("data", data: ["d": text])
        }
    }

    public func match(_ match: GKMatch, player: GKPlayer, didChange state: GKPlayerConnectionState) {
        DispatchQueue.main.async {
            guard match === self.match else { return }
            if state == .connected {
                self.startIfReady()
            } else if state == .disconnected {
                self.endMatch(match)
            }
        }
    }

    public func match(_ match: GKMatch, didFailWithError error: Error?) {
        DispatchQueue.main.async { self.endMatch(match) }
    }

    @objc func disconnect(_ call: CAPPluginCall) {
        DispatchQueue.main.async {
            if let m = self.match { m.delegate = nil; m.disconnect() }
            self.match = nil
            self.started = false
            call.resolve()
        }
    }

    // MARK: helpers

    /// Presents on top of whatever is showing. If another screen is mid-animation (e.g. Apple's sign-in
    /// screen closing itself), or the window isn't up yet (cold launch from an invite), try again shortly.
    private func show(_ screen: UIViewController, tries: Int = 0) {
        if screen.presentingViewController != nil { return }   // already up
        guard let root = bridge?.viewController else { return }
        var top: UIViewController = root
        var busy = root.isBeingPresented || root.isBeingDismissed || root.view.window == nil
        while !busy, let next = top.presentedViewController {
            if next.isBeingPresented || next.isBeingDismissed { busy = true } else { top = next }
        }
        if busy {
            if tries < 40 {
                DispatchQueue.main.asyncAfter(deadline: .now() + 0.25) { self.show(screen, tries: tries + 1) }
            }
            return
        }
        top.present(screen, animated: true)
    }
}
