# Validation record — ESP32 Passive Wi-Fi Scanner

- **Date:** 2026-10-31
- **Status:** Passed — built and verified on physical hardware
- **Board:** ESP32-DevKitC-32UE / ESP32-WROOM-32UE
- **Detected chip (from prior bring-up):** ESP32-D0WD-V3, revision 3.1
- **Board profile:** ESP32 Dev Module
- **Arduino IDE:** 2.3.10
- **Arduino-ESP32 core:** 3.3.12
- **Serial port observed:** /dev/ttyUSB0
- **Serial baud:** 115200

## Checks completed

- [x] Sketch compiled and uploaded to the physical ESP32.
- [x] Scanner startup banner appeared.
- [x] Wi-Fi scans completed repeatedly.
- [x] One to five access points appeared in individual scans across the captured sessions.
- [x] SSID, RSSI, channel and advertised security columns were displayed.
- [x] RSSI values across the captured sessions ranged from -96 dBm to -35 dBm.
- [x] Channels 1, 2, 3, 8 and 11 appeared in captured results.
- [x] WPA2 and WPA2/WPA3 advertised modes appeared in captured results.
- [x] Standalone serial diagnostic ran cleanly at 115200 baud for 32 sequential messages, reaching 32524 ms uptime.
- [x] Fresh scanner retest showed multiple consecutive readable scan tables at 115200 baud.
- [x] No malformed serial characters appeared in the supplied fresh scanner retest.
- [x] The ESP32 boot log was explained by the user as following a manual EN reset / USB reconnect, not an unexpected runtime restart.

## Serial-noise investigation

The first scanner capture included occasional replacement/gibberish characters around startup and between some scan blocks. The standalone serial-only diagnostic subsequently produced clean output for 32 consecutive messages. A fresh Wi-Fi scanner retest also produced clean, readable output across repeated scan tables.

The earlier noise was therefore **not reproduced** in the diagnostic or fresh scanner retest. Its original cause was not conclusively identified, so this record does not claim a proven root cause. The manually initiated reset later produced the normal ESP32 bootloader log.

## Observed measurements

The user-provided scans showed between one and five networks per scan, with RSSI values ranging from -96 dBm to -35 dBm. Observed channels were 1, 2, 3, 8 and 11. WPA2 and WPA2/WPA3 were displayed.

Real nearby SSID names are intentionally omitted from this public record to protect network privacy. These are observational measurements, not a controlled RF benchmark.

## Scope notes (not build failures)

- The original ESP32 radio used here operates on 2.4 GHz Wi-Fi; it does not scan 5 GHz.
- Passive scans can miss weak or intermittent access-point beacons.
- Scan count and RSSI vary with location, antenna orientation and radio conditions.
- The external antenna is required for the ESP32-WROOM-32UE module's RF operation. The user owns the supplied antenna; its physical connector state was not separately photographed during this test.

## Evidence boundary

Validation is based on the user's supplied Arduino IDE upload information, Serial Monitor screenshots and pasted scan output in the build conversation. No automated test suite or independent second-board replication was performed.
