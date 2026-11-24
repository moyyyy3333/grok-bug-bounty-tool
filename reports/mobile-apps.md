# Ranked Digest: Top 5 Active Public Bugcrowd Mobile App Programs

**Date**: 24 November 2026  
**Scope**: Public programs with iOS or Android targets. No exploitation, binary analysis, or submissions performed.  
**Methodology**: Conceptual reverse-engineering (static metadata + brief review) scored on jailbreak/root detection bypass potential, certificate pinning, hardcoded secrets, and exported components (1–10 scale; higher = more promising based on public evidence).

## Ranked Targets

| Rank | Program | Primary Focus | JB/Root | Pinning | Secrets | Exported | Overall |
|------|---------|---------------|---------|---------|---------|----------|---------|
| 1 | BitGo Mobile Apps | Institutional crypto approvals (React Native) | 8 | 7 | 8 | 6 | 7.3 |
| 2 | Ultra Mobile / Mint | Telecom account & SIM management | 7 | 6 | 7 | 7 | 6.8 |
| 3 | iRobot (Roomba Home) | IoT robot control + cloud APIs | 6 | 7 | 6 | 5 | 6.0 |
| 4 | Vinted | Marketplace (listings, orders, messages) | 5 | 4 | 6 | 6 | 5.3 |
| 5 | Carrefour UAE (MAF) | E-commerce + payments | 6 | 6 | 7 | 5 | 6.0 |

## Detailed Evidence

### 1. BitGo Mobile Apps Bug Bounty Engagement
- **URL**: https://bugcrowd.com/engagements/bitgo-mobileapps-mbb-og
- **Status**: Active / In progress (started Sep 2025)
- **Rewards**: P1 $3500–$4500
- **App Store Links**:
  - Android Verify: https://play.google.com/store/apps/details?id=com.bitgo.verify
  - Android Platform: https://play.google.com/store/apps/details?id=com.bitgo.mobileapp
  - iOS Verify: https://apps.apple.com/us/app/bitgo-verify/id1608937235
  - iOS Platform: https://apps.apple.com/us/app/bitgo/id6739010408
- **Bundle IDs**: `com.bitgo.verify`, `com.bitgo.mobileapp`
- **Minimum OS**: iOS 15.1+; Android ~7.0+
- **Brief Hints**: React Native / TypeScript; production; focus on pending approval workflows (transactions, policy updates, user management). Region restrictions apply for some testing.
- **RE Notes**: High-value crypto surface. Secrets likely in RN bundles or native modules. Pinning expected. JB detection common but often bypassable on test devices. Moderate exported components via RN bridges.

### 2. Ultra Mobile Mobile Apps Bug Bounty Engagement
- **URL**: https://bugcrowd.com/engagements/ultramobile-mobile-apps
- **Status**: Active / Ongoing
- **Rewards**: P1 $3500–$4500
- **App Store Links**:
  - Android: https://play.google.com/store/apps/details?id=com.uvnv.mintsim
  - iOS: https://apps.apple.com/us/app/mint-mobile/id1295303441
- **Bundle IDs**: `com.uvnv.mintsim` (Android)
- **Minimum OS**: iOS 16.6+; Android variants from 6.0+
- **Brief Hints**: Kotlin + Swift; mobile APIs; focus on sensitive information disclosure and free-service manipulation beyond trial. Self-signup available.
- **RE Notes**: Client-side trial/abuse logic common. Moderate pinning. Deep links and exported components typical for telecom account apps.

### 3. iRobot
- **URL**: https://bugcrowd.com/engagements/irobot
- **Status**: Active / Ongoing (large scope)
- **Rewards**: Mobile P1 $2500–$3000
- **App Store Links**:
  - iOS: https://apps.apple.com/us/app/roomba-home/id6504274697
  - Android: https://play.google.com/store/apps/details?id=com.irobot.home.prime
- **Bundle IDs**: `com.irobot.home.prime`
- **Minimum OS**: Android 11+ (API 30)
- **Brief Hints**: Swift/Objective-C + Kotlin/Java; focus on auth bypass impacting other users’ robots/accounts. Manual testing preferred.
- **RE Notes**: IoT command paths and session handling. Pinning present in modern builds. Variable JB detection. Pairing-related exported components.

### 4. Vinted Bug Bounty
- **URL**: https://bugcrowd.com/engagements/vinted-uab-mbb
- **Status**: Active / Public
- **Rewards**: P1 up to $8000
- **App Store Links**:
  - iOS: https://apps.apple.com/us/app/vinted-pre-loved-marketplace/id632064380
  - Android: https://play.google.com/store/apps/details?id=fr.vinted
- **Bundle IDs**: `fr.vinted`
- **Minimum OS**: iOS ~15.8–16+; Android 7.0–10+
- **Brief Hints**: Explicit out-of-scope for absence of certificate pinning, lack of jailbreak/root detection, clipboard leaks, path disclosure, anti-debug. Focus on business logic.
- **RE Notes**: Classic mobile RE findings largely OOS. Strong for IDOR and marketplace logic. Secrets possible in client configuration.

### 5. Majid Al Futtaim Retail (Carrefour UAE)
- **URL**: https://bugcrowd.com/engagements/carrefour
- **Status**: Active / Ongoing
- **Rewards**: P1 $3000–$4000
- **App Store Links**:
  - iOS: https://itunes.apple.com/app/carrefour-uae/id626805470
  - Android: https://play.google.com/store/apps/details?id=com.aswat.carrefouruae
- **Bundle IDs**: `com.aswat.carrefouruae`
- **Minimum OS**: Android 7.0+
- **Brief Hints**: Production mobile + APIs; focus on payment cycle manipulation, reward points, PCI data. Geo-blocked (VPN in brief).
- **RE Notes**: Payment validation and client-side checks. Moderate pinning. Deep-link and payment callback exported components.

## Disclaimer
All information derived from publicly available Bugcrowd engagement briefs and app store / APKMirror metadata. No binaries were downloaded or analyzed. Verify current scope, rules, and status before any authorized research. Programs and rewards change frequently.
