import Foundation
import Capacitor
import StoreKit

/// In-app purchases for Monster Hockey (Apple StoreKit 2).
///
/// The game calls:
///   Store.products({ ids: [...] }) -> { items: [{ id, price }] }   price is Apple's local price text, e.g. "$1.99"
///   Store.buy({ id })               -> { ok: Bool, pending?: Bool }
///   Store.owned()                   -> { ids: [...] }                what this Apple ID has bought (works offline from Apple's cache)
///   Store.restore()                 -> { ids: [...] }                asks Apple to sync, then same as owned()
/// and hears "owned" { ids } whenever a purchase arrives from outside the app (Ask to Buy approved, another device, refund).
@objc(StorePlugin)
public class StorePlugin: CAPPlugin, CAPBridgedPlugin {
    public let identifier = "StorePlugin"
    public let jsName = "Store"
    public let pluginMethods: [CAPPluginMethod] = [
        CAPPluginMethod(name: "products", returnType: CAPPluginReturnPromise),
        CAPPluginMethod(name: "buy", returnType: CAPPluginReturnPromise),
        CAPPluginMethod(name: "owned", returnType: CAPPluginReturnPromise),
        CAPPluginMethod(name: "restore", returnType: CAPPluginReturnPromise)
    ]

    // Everything below runs on the main thread (Task { @MainActor ... }), so `cache` is never touched from two threads at once
    // and notifyListeners / call.resolve always happen on main.
    private var cache: [String: Product] = [:]
    private var updates: Task<Void, Never>?

    override public func load() {
        // Purchases that finish outside buy(): Ask to Buy approvals, purchases on another device, refunds/revocations,
        // and any purchase left unfinished last time (StoreKit replays those here right after launch).
        updates = Task { @MainActor [weak self] in
            for await result in Transaction.updates {
                if case .verified(let t) = result { await t.finish() }
                let ids = await StorePlugin.ownedIds()
                guard let self = self else { return }
                self.notifyListeners("owned", data: ["ids": ids], retainUntilConsumed: true)
            }
        }
    }

    deinit { updates?.cancel() }

    private static func ownedIds() async -> [String] {
        var ids: [String] = []
        for await result in Transaction.currentEntitlements {
            if case .verified(let t) = result, t.revocationDate == nil { ids.append(t.productID) }
        }
        return ids
    }

    @MainActor private func product(_ id: String) async throws -> Product? {
        if let p = cache[id] { return p }
        let list = try await Product.products(for: [id])
        for p in list { cache[p.id] = p }
        return cache[id]
    }

    @objc func products(_ call: CAPPluginCall) {
        let ids = call.getArray("ids", String.self) ?? []
        Task { @MainActor in
            do {
                let list = try await Product.products(for: ids)
                for p in list { cache[p.id] = p }
                call.resolve(["items": list.map { ["id": $0.id, "price": $0.displayPrice] }])
            } catch {
                call.resolve(["items": []])
            }
        }
    }

    @objc func buy(_ call: CAPPluginCall) {
        guard let id = call.getString("id") else { call.resolve(["ok": false]); return }
        Task { @MainActor in
            do {
                guard let p = try await product(id) else { call.resolve(["ok": false, "msg": "NOT FOUND"]); return }
                let result = try await p.purchase()
                switch result {
                case .success(let verification):
                    if case .verified(let t) = verification {
                        await t.finish()
                        call.resolve(["ok": true])
                    } else {
                        call.resolve(["ok": false, "msg": "COULDN'T VERIFY"])
                    }
                case .pending:
                    call.resolve(["ok": false, "pending": true])   // Ask to Buy: arrives later through "owned"
                case .userCancelled:
                    call.resolve(["ok": false])
                @unknown default:
                    call.resolve(["ok": false])
                }
            } catch {
                call.resolve(["ok": false, "msg": "STORE TROUBLE"])
            }
        }
    }

    @objc func owned(_ call: CAPPluginCall) {
        Task { @MainActor in
            let ids = await StorePlugin.ownedIds()
            call.resolve(["ids": ids])
        }
    }

    @objc func restore(_ call: CAPPluginCall) {
        Task { @MainActor in
            try? await AppStore.sync()   // may ask them to sign in to their Apple ID
            let ids = await StorePlugin.ownedIds()
            call.resolve(["ids": ids])
        }
    }
}
