// swift-tools-version: 5.9
import PackageDescription

let package = Package(
    name: "MonsterGameCenter",
    platforms: [.iOS(.v15)],
    products: [
        .library(name: "MonsterGameCenter", targets: ["GameCenterPlugin"])
    ],
    dependencies: [
        .package(url: "https://github.com/ionic-team/capacitor-swift-pm.git", "8.0.0"..<"10.0.0")
    ],
    targets: [
        .target(
            name: "GameCenterPlugin",
            dependencies: [
                .product(name: "Capacitor", package: "capacitor-swift-pm"),
                .product(name: "Cordova", package: "capacitor-swift-pm")
            ],
            path: "ios/Sources/GameCenterPlugin",
            linkerSettings: [.linkedFramework("GameKit")]
        )
    ]
)
