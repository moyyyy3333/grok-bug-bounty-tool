# IoT and Hardware Bug Bounty Targets on Bugcrowd

**Generated:** 2026-11-24  
**Scope:** Public Bugcrowd programs with IoT, firmware, or hardware in scope.  
**Methodology:** Open-source intelligence (OSINT) via web search and program pages. Conceptual application of reverse-engineering unified tool methodology (firmware extraction analysis, binary inspection, update channel review, interface enumeration). No exploitation, no submissions, no active testing performed.

**Scoring Criteria (1-10, higher = higher research interest / potential attack surface):**
- Exposed services (web UI, APIs, BLE, cloud endpoints)
- Default credentials (historical or documented)
- Unencrypted update channels (HTTP vs HTTPS, signing)
- Debug interfaces (UART, JTAG, SWD potential or documented)

Ranked by combined score, public firmware availability, program activity, and breadth of device models.

## Ranked Top 5 Targets

### 1. NETGEAR Cash Rewards (bugcrowd.com/netgear)
**Overall Score: 9.2/10**

- **Device Models:** Nighthawk Pro Gaming Routers/Switches, Nighthawk Routers/Switches, Orbi mesh systems, Insight Managed Smart Cloud Wireless APs, Meural Canvas/Frames, and related IoT.
- **Firmware Update URLs:** Official support pages (e.g., https://www.netgear.com/support/product/<model>/#download). Manual downloads available per model. Community knowledge base for update procedures (kb.netgear.com).
- **Public Firmware Images:** Yes — full public downloads of current and historical firmware for most models. Community archives and release notes widely available.
- **Evidence:** 1,343 vulnerabilities rewarded historically. High activity. Default credentials historically common (admin/password). Web management interfaces exposed on local network. Firmware often extractable for RE.
- **Conceptual RE Scoring:**
  - Exposed services: 9 (local web UI, apps, cloud API)
  - Default credentials: 8 (well-known defaults)
  - Unencrypted update channels: 6 (mixed; some HTTP legacy)
  - Debug interfaces: 7 (common UART on consumer routers)
- **Notes:** Ideal for static firmware analysis. Check for hardcoded keys, command injection in web UI, update signature bypasses.

### 2. AXIS OS Public Program (bugcrowd.com/engagements/axis-os-public)
**Overall Score: 8.7/10**

- **Device Models:** 400+ Axis-branded products (network cameras, intercoms, audio devices, sensors, body-worn systems) running AXIS OS (Linux-based).
- **Firmware Update URLs:** https://www.axis.com/support/device-software and product-specific support pages. FTP-style downloads (e.g., /ftp/pub/axis/software/.../*.bin).
- **Public Firmware Images:** Yes — direct public .bin downloads with checksums for active, LTS, and PSS tracks. Release notes and lifecycle guides public.
- **Evidence:** 91 vulnerabilities rewarded; average payout ~$6k; P1 up to $25k. Active as of Nov 2026. SSH access for researchers noted (non-root by default). Physical invasive access out of scope.
- **Conceptual RE Scoring:**
  - Exposed services: 9 (HTTPS web UI, VAPIX/ONVIF APIs, anonymous basic info)
  - Default credentials: 7 (factory defaults exist; hardening guide available)
  - Unencrypted update channels: 5 (HTTPS preferred; signed)
  - Debug interfaces: 8 (Linux, potential serial; SSH provided)
- **Notes:** Excellent for binary analysis of Linux firmware. Focus on privilege escalation (VAPIX to root), API auth bypasses. Reward reduction announced recently.

### 3. Wyze Bug Bounty (bugcrowd.com/engagements/wyze)
**Overall Score: 8.1/10**

- **Device Models:** Wyze Cam V3, Wyze Cam v4 (hardware testing in dedicated scope), plus web/API (auth.wyze.com, my.wyze.com, api.wyzecam.com).
- **Firmware Update URLs:** Support pages for manual flash (microSD recovery). Download links from Release Notes & Firmware (support.wyze.com). Example historical: download.wyzecam.com/firmware/v3/..., v4/....
- **Public Firmware Images:** Yes — official downloads for flashing; community GitHub mirrors (e.g., kohrar/Wyze-Firmwares) of older images.
- **Evidence:** Separate hardware reward tier for Cam V3/V4. ~57 vulns rewarded. Consumer cameras with known IoT patterns.
- **Conceptual RE Scoring:**
  - Exposed services: 8 (Wi-Fi, app, cloud, potential RTSP)
  - Default credentials: 6
  - Unencrypted update channels: 7 (manual flash common; OTA details limited)
  - Debug interfaces: 7 (setup button recovery, potential UART)
- **Notes:** Strong candidate for firmware dumping via SD and static analysis of camera binaries. Check for hardcoded keys, auth flaws in cloud APIs.

### 4. Arlo Cash Rewards (bugcrowd.com/arlo)
**Overall Score: 7.6/10**

- **Device Models:** Extensive hardware: Arlo Essential 2 & 3 (indoor/outdoor, doorbell), Pro 3/5S/6, Ultra 2, Go v2, Base Stations, SmartHubs, Chime 2, Floodlights, All-In-One Sensor, Safe Button, Wire-Free Siren, Home Security System components.
- **Firmware Update URLs:** Automatic OTA via Arlo Secure App or my.arlo.com. Manual check in app (Device Info > Firmware). No widely public raw image downloads.
- **Public Firmware Images:** Limited — primarily app-mediated OTA; community notes on versions but not full public binaries.
- **Evidence:** 558 vulnerabilities rewarded. Very high activity. Bonus rewards for certain series. EOS devices noted but core still in scope.
- **Conceptual RE Scoring:**
  - Exposed services: 8 (cloud APIs, apps, local if applicable, BLE possible)
  - Default credentials: 5
  - Unencrypted update channels: 4 (app/cloud controlled)
  - Debug interfaces: 6 (hardware present but less documented)
- **Notes:** More cloud/app focused. Research paths: mobile app RE, API auth, device pairing. Hardware testing allowed for listed models.

### 5. Cisco Networking / Meraki (tracked as Bugcrowd Cisco Networking)
**Overall Score: 7.4/10**

- **Device Models:** Cisco Meraki MR Access Points, MS Switches, MV Smart Cameras, MG Fixed Wireless, MX & Z Series Security Appliances (incl. vMX), Campus Gateways, Catalyst 9200L (cloud-managed), Systems Manager.
- **Firmware Update URLs:** Managed via Meraki Dashboard (Organization > Firmware upgrades). Cloud download (HTTPS). Limited public images (some vMX on Cisco software download, login required).
- **Public Firmware Images:** Partial — primarily cloud-distributed; some images available with account. Documentation public.
- **Evidence:** Hardware-heavy scope. Up to $10k rewards. Long-running (public since ~2018). Cloud management architecture.
- **Conceptual RE Scoring:**
  - Exposed services: 8 (local management, cloud, APIs)
  - Default credentials: 6 (cloud-centric)
  - Unencrypted update channels: 4 (HTTPS to dashboard)
  - Debug interfaces: 5 (enterprise hardening)
- **Notes:** Enterprise focus. Conceptual interest in firmware signing, local services, and cloud-to-device trust. Physical access may be needed for deeper RE.

## Additional Notes
- **iRobot** and **Motorola Mobility IoT** also have hardware/Android device scope but lower public firmware availability (app/OTA only). Motorola focuses on Android 13+ devices with root/bootloader focus.
- All analysis is conceptual and based on public information only. Always verify current scope and rules on official Bugcrowd program pages before any research.
- Sources: Bugcrowd program pages, manufacturer support sites, community knowledge bases, and public firmware repositories as of November 2026.

**Disclaimer:** This digest is for research prioritization only. No exploitation or submissions were attempted. Follow all program rules and applicable laws.