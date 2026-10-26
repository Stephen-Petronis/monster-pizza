import Foundation
import UIKit
import Capacitor
import GameKit

/// Apple Game Center for Monster Hockey.
///
/// The game (a web page) calls:
///   GameCenter.findMatch()    -> shows Apple's matchmaking screen (random opponent, or invite friends / Messages)
///   GameCenter.send({ d, fast }) -> sends one message (a JSON string) to the other player
///   GameCenter.disconnect()   -> leaves the match
/// and listens for these events:
///   "match"  { host: Bool, other: String }  both players are connected; host runs the game
///   "cancel" {}                             the player closed Apple's screen
///   "fail"   { msg: String }                couldn't sign in or make a match
///   "data"   { d: String }                  a message from the other player
///   "left"   {}                             the other player left / the connection dropped
/// Invites accepted from Messages or Game Center (even when the app wasn't open) also end in "match".
@objc(GameCenterPlugin)
public class GameCenterPlugin: CAPPlugin, CAPBridgedPlugin, GKMatchmakerViewControllerDelegate, GKMatchDelegate, GKLocalPlayerListener {
    public let identifier = "GameCenterPlugin"
    public let jsName = "GameCenter"
    public let pluginMethods: [CAPPluginMethod] = [
        CAPPluginMethod(name: "status", returnType: CAPPluginReturnPromise),
        CAPPluginMethod(name: "findMatch", returnType: CAPPluginReturnPromise),
        CAPPluginMethod(name: "send", returnType: CAPPluginReturnPromise),
        CAPPluginMethod(name: "disconnect", returnType: CAPPluginReturnPromise)
    ]

    private var match: GKMatch?
    private var started = false
    private var signInScreen: UIViewController?
    private var listening = false
    private var wantsMatch = false   // tapped FIND A MATCH before sign-in finished

    // MARK: sign in (quietly at launch; the sign-in screen only shows when they ask for a match)

    override public func load() {
        DispatchQueue.main.async { self.authenticate() }
    }

    private func authenticate() {
        GKLocalPlayer.local.authenticateHandler = { [weak self] viewController, error in
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
                    self.openMatchmaker()
                }
            } else if self.wantsMatch {
                self.wantsMatch = false
                self.notifyListeners("fail", data: ["msg": "SIGN IN TO GAME CENTER IN SETTINGS"])
            }
        }
    }

    @objc func status(_ call: CAPPluginCall) {
        DispatchQueue.main.async {
            let me = GKLocalPlayer.local
            call.resolve(["signedIn": me.isAuthenticated, "name": me.isAuthenticated ? me.displayName : ""])
        }
    }

    // MARK: matchmaking

    @objc func findMatch(_ call: CAPPluginCall) {
        DispatchQueue.main.async {
            if GKLocalPlayer.local.isAuthenticated {
                self.openMatchmaker()
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
            call.resolve()
        }
    }

    private func openMatchmaker(recipients: [GKPlayer]? = nil) {
        let request = GKMatchRequest()
        request.minPlayers = 2
        request.maxPlayers = 2
        if let recipients = recipients { request.recipients = recipients }
        guard let screen = GKMatchmakerViewController(matchRequest: request) else {
            notifyListeners("fail", data: ["msg": "GAME CENTER ISN'T READY"])
            return
        }
        screen.matchmakerDelegate = self
        show(screen)
    }

    public func matchmakerViewControllerWasCancelled(_ viewController: GKMatchmakerViewController) {
        viewController.dismiss(animated: true)
        notifyListeners("cancel", data: [:])
    }

    public func matchmakerViewController(_ viewController: GKMatchmakerViewController, didFailWithError error: Error) {
        viewController.dismiss(animated: true)
        notifyListeners("fail", data: ["msg": "COULDN'T MAKE A MATCH"])
    }

    public func matchmakerViewController(_ viewController: GKMatchmakerViewController, didFind match: GKMatch) {
        viewController.dismiss(animated: true)
        begin(match)
    }

    // Someone accepted an invite (Messages or Game Center), maybe launching the app to do it.
    public func player(_ player: GKPlayer, didAccept invite: GKInvite) {
        DispatchQueue.main.async {
            guard let screen = GKMatchmakerViewController(invite: invite) else { return }
            screen.matchmakerDelegate = self
            self.show(screen)
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
        let host = GKLocalPlayer.local.gamePlayerID < other.gamePlayerID
        notifyListeners("match", data: ["host": host, "other": other.displayName], retainUntilConsumed: true)
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
        guard match === self.match, let text = String(data: data, encoding: .utf8) else { return }
        notifyListeners("data", data: ["d": text])
    }

    public func match(_ match: GKMatch, player: GKPlayer, didChange state: GKPlayerConnectionState) {
        guard match === self.match else { return }
        DispatchQueue.main.async {
            if state == .connected {
                self.startIfReady()
            } else if state == .disconnected && self.started {
                self.notifyListeners("left", data: [:])
            }
        }
    }

    public func match(_ match: GKMatch, didFailWithError error: Error?) {
        guard match === self.match else { return }
        DispatchQueue.main.async { if self.started { self.notifyListeners("left", data: [:]) } }
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

    private func show(_ screen: UIViewController) {
        guard let root = bridge?.viewController else { return }
        if screen.presentingViewController != nil { return }   // already up
        var top: UIViewController = root
        while let next = top.presentedViewController { top = next }
        top.present(screen, animated: true)
    }
}
