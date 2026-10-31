# Board support and verification matrix

A board family being selected for the library is not the same as having a tested project for it.

| Board family | Current status | Verified model |
|---|---|---|
| ESP32 | Two projects built and verified: serial bring-up and passive Wi-Fi scanning | ESP32-DevKitC-32UE / ESP32-WROOM-32UE |
| ESP8266 | Selected; no completed project yet | Not yet tested |
| Arduino | Selected; no completed project yet | Not yet tested; exact model TBD |
| Raspberry Pi Pico | Selected; no completed project yet | Not yet tested; Pico vs Pico W TBD |

## Verified ESP32 details

The owner identified the board as ESP32-DevKitC-32UE. The official Espressif DevKitC documentation lists the 32UE variant as using an ESP32-WROOM-32UE module, with 4 MB flash and an external antenna connector. The serial bring-up build log identified the chip as ESP32-D0WD-V3 revision 3.1.

The ESP32 Dev Module profile was used successfully in Arduino IDE 2.3.10 with Arduino-ESP32 core 3.3.12.

The second project used the same board and software configuration for passive 2.4 GHz Wi-Fi scanning. Repeated scan output was observed with readable SSID, RSSI, channel and advertised-security columns. A standalone serial-only diagnostic also ran cleanly for 32 messages, and the fresh scanner retest did not reproduce the earlier malformed serial output. The original noise cause was not conclusively identified; see the scanner project's validation record.

These records document the working configuration; they are not a claim that every board setting or every DevKitC revision is identical.

## Adding a new board family

Before adding a board to a project's metadata, record its exact model, MCU/module, board package or SDK version, upload interface, voltage limits, pinout reference and verified test result. Avoid using only a marketing family name where variants differ materially.
