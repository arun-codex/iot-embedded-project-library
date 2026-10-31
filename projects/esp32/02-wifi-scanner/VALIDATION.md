# Validation record — ESP32 Passive Wi-Fi Scanner

- **Date:** 2026-10-31
- **Status:** Built with limitations; primary scan behavior observed
- **Board:** ESP32-DevKitC-32UE / ESP32-WROOM-32UE
- **Board profile:** ESP32 Dev Module
- **Arduino IDE:** 2.3.10
- **Arduino-ESP32 core:** 3.3.12
- **Serial port observed:** /dev/ttyUSB0
- **Serial baud:** 115200

## Checks supported by supplied evidence

- [x] Scanner startup banner appeared.
- [x] Wi-Fi scan completed repeatedly.
- [x] One to five access points appeared in individual scans.
- [x] SSID, RSSI, channel and advertised security columns were displayed.
- [x] RSSI values varied from -36 dBm to -96 dBm in the captured session.
- [x] Channels 1, 2, 3 and 8 appeared in captured results.
- [x] WPA2 was displayed for the captured entries.
- [ ] Clean serial output with no malformed characters has not been confirmed.
- [ ] External antenna attachment during this exact scan session was not separately recorded.
- [ ] No automated test suite or independent second-board replication was performed.

## Evidence and privacy

Evidence is the user's supplied Serial Monitor text in the project build conversation. Real nearby SSID names were intentionally excluded from this public record. The listed measurements are an observational summary, not a controlled RF test.

## Follow-up validation

1. Confirm the external antenna is securely connected to the ESP32-WROOM-32UE antenna connector before the next scan.
2. Reopen Serial Monitor at 115200 baud and perform a fresh reset.
3. Record whether malformed characters recur between scan blocks.
4. Repeat the scan from one fixed location and orientation if comparing RSSI stability.
