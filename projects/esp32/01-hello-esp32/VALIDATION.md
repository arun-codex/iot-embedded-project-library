# Validation record — Hello, ESP32! serial bring-up

- **Date:** 2026-10-31
- **Status:** Passed (manual hardware test)
- **Board profile:** ESP32 Dev Module
- **Board/module stated by owner:** ESP32-DevKitC-32UE / ESP32-WROOM-32UE
- **Detected chip:** ESP32-D0WD-V3, revision 3.1
- **USB serial port observed:** `/dev/ttyUSB0`
- **Arduino IDE:** 2.3.10
- **Arduino-ESP32 core:** 3.3.12
- **esptool:** 5.3.1
- **Serial baud:** 115200

## Checks recorded

- [x] Sketch compiled.
- [x] Device connected to the uploader.
- [x] Firmware writing reached 100%.
- [x] Flash hash verification passed.
- [x] ESP32 reset after flashing.
- [x] Serial Monitor showed `Hello, ESP32!` and repeated `ESP32 is running!` at 115200 baud.

## Evidence boundary

These checks are based on the user's supplied Arduino IDE upload log and Serial Monitor screenshots in the build conversation. The raw screenshots and full terminal log are not included in this repository. No automated test suite was run. The project has not been independently reproduced by another person or on another board revision.
