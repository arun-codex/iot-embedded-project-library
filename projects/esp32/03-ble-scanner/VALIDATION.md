# Validation record — ESP32 BLE Scanner

- **Date:** 2026-11-01
- **Status:** Passed — built and verified on physical hardware
- **Board:** ESP32-DevKitC-32UE / ESP32-WROOM-32UE
- **Board profile:** ESP32 Dev Module
- **Arduino IDE:** 2.3.10
- **Arduino-ESP32 core:** 3.3.12
- **Serial port observed:** /dev/ttyUSB0
- **Serial baud:** 115200

## Checks supported by supplied evidence

- [x] Firmware compiled and uploaded to the physical ESP32.
- [x] BLE initialization message appeared.
- [x] Passive scan started and completed repeatedly.
- [x] Two to four BLE scan-result records appeared in the supplied scans.
- [x] Device name or "(name not advertised)" was displayed.
- [x] RSSI values were displayed; observed range was -101 dBm to -43 dBm.
- [x] Advertised service UUID counts of zero and one were observed.
- [x] Both connectable and non-connectable advertisement indications were observed.
- [x] Repeated scan cycles completed.
- [x] Readable scan tables appeared after the firmware startup banner in the supplied screenshot and log.

## Serial-output observation

A block of replacement/gibberish characters appeared around a firmware/boot transition in the pasted capture. After the ESP32 startup banner, multiple scan tables were readable in the supplied log and screenshot. The cause of the earlier characters was not established. The captured bootloader text alone does not establish an unexpected runtime reset.

## Privacy

Nearby BLE device names and addresses are omitted from this public validation record. The sketch reports advertised names but does not print MAC addresses or raw advertising payloads.

## Evidence boundary

Evidence is based on the user's supplied Arduino IDE screenshot and pasted BLE scan output. No automated test suite, pairing test, GATT connection test or independent second-board replication was performed.
