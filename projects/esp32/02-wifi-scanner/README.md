# ESP32 Passive Wi-Fi Scanner

**Status:** Built with limitations (manual hardware test passed; intermittent serial-output noise remains unexplained)  
**Difficulty:** Beginner  
**Board:** Espressif ESP32-DevKitC-32UE / ESP32-WROOM-32UE  
**Build verified:** 31 October 2026  
**Category:** Wireless and networking

## 1. Goal

Use the ESP32's 2.4 GHz Wi-Fi radio to passively discover nearby access points and report their advertised SSID, received signal strength (RSSI), channel and authentication mode in Serial Monitor.

This sketch does not join a network, send probe requests, capture user traffic, collect credentials, or disrupt wireless communications. It is a local observation and learning exercise.

## 2. Learning outcomes

- Understand station mode without joining an access point.
- Perform a passive Wi-Fi scan with Arduino-ESP32.
- Read SSID, RSSI, channel and advertised authentication mode.
- Interpret RSSI and understand why weak access points may not appear in every scan.
- Repeat scans and release scan-result memory.

## 3. Prerequisites

- Basic Arduino C++: functions, variables, conditions, switch statements and loops.
- Arduino IDE 2.3.10 or compatible Arduino IDE 2.x.
- ESP32 board package by Espressif Systems, version 3.3.12 for the recorded build.
- USB data cable.
- A 2.4 GHz Wi-Fi environment to observe. Only perform wireless observations where you have permission.

## 4. Hardware and bill of materials

| Part | Qty | Required | Actual use | Incremental cost |
|---|---:|---|---|---:|
| ESP32-DevKitC-32UE | 1 | Yes | Wi-Fi scan and serial output | ₹0; already owned |
| USB data cable | 1 | Yes | Power, upload and serial | ₹0; already owned |
| External antenna and pigtail for 32UE module | 1 | Use external antenna connector | Connection state during captured scan was not separately recorded | ₹0; already owned |
| Breadboard and jumper wires | 1 set | No | Not used | ₹0 |

No additional purchases were needed. The breadboard is not required.

**Antenna note:** ESP32-WROOM-32UE is the external-antenna module variant. Attach the supplied antenna to its U.FL/IPEX connector carefully before future RF tests. The captured session did not independently document the connector state, so this guide does not claim antenna attachment was verified during that run.

## 5. Software and versions

| Item | Recorded value |
|---|---|
| Host OS | Fedora Linux |
| IDE | Arduino IDE 2.3.10 |
| Board package | esp32 by Espressif Systems 3.3.12 |
| Board profile | ESP32 Dev Module |
| Detected chip in prior board bring-up | ESP32-D0WD-V3, revision 3.1 |
| Serial port | /dev/ttyUSB0 during recorded session; may change |
| Serial baud | 115200 |
| Arduino library | WiFi.h, supplied by ESP32 Arduino core |

No separate library installation is required for WiFi.h.

## 6. Wiring

No breadboard circuit or GPIO wiring is used.

1. Connect the ESP32 board to Fedora using the USB data cable.
2. Attach the supplied external antenna to the module connector. Handle the tiny connector carefully.
3. Do not connect external voltage to GPIO pins.

## 7. Source code

Source: [src/wifi_scanner.ino](src/wifi_scanner.ino)

The sketch uses:
- WiFi.mode(WIFI_STA) to initialize station mode without network credentials.
- WiFi.disconnect() so the sketch does not intentionally connect to an access point.
- WiFi.scanNetworks(false, false, true, 300) for synchronous passive scanning, without requesting hidden SSIDs, with a 300 ms maximum per-channel dwell argument.
- WiFi.SSID(i), WiFi.RSSI(i), WiFi.channel(i) and WiFi.encryptionType(i) to read scan results.
- WiFi.scanDelete() to release stored scan results before the next scan.

The official Arduino-ESP32 Wi-Fi API documents the scan arguments and result-access methods. See References.

## 8. Build and upload

1. Open Arduino IDE and load src/wifi_scanner.ino.
2. Select **ESP32 Dev Module**.
3. Select the ESP32 serial port. It was /dev/ttyUSB0 in the recorded session; the name may change.
4. Click **Verify**, then **Upload**.
5. Open **Tools → Serial Monitor**.
6. Set Serial Monitor to **115200 baud**, matching Serial.begin(115200).
7. Observe repeated scan output. The sketch waits 15 seconds after each scan completes before starting another; start-to-start timing also includes scan duration.

### Fedora serial permission

Inspect the actual device group:

~~~bash
ls -l /dev/ttyUSB0
~~~

The recorded device belonged to group dialout. If your device also shows that group, add your user and start a fresh login session:

~~~bash
sudo usermod -aG dialout "$USER"
~~~

Do not use chmod 777 or run the IDE as root. If the device shows another group, use the actual group shown by ls -l.

## 9. Expected output

~~~text
ESP32 Wireless Recon Lab
Project 02: Wi-Fi Scanner

====================================
       ESP32 WI-FI SCANNER
====================================
Starting passive scan...

Networks found: <count>

NO | SSID | RSSI | CHANNEL | SECURITY
-----------------------------------------------
1 | <network-name> | <rssi> dBm | <channel> | <security>

Scan completed.
====================================
~~~

Network count and results vary with location, signal strength, beacon timing and radio environment. The sketch waits 15 seconds after a completed scan.

## 10. Actual test results

The user ran the sketch on the ESP32-DevKitC-32UE and supplied repeated Serial Monitor output.

| Measurement | Observed result |
|---|---|
| Access points per scan | 1 to 5 |
| RSSI range | -36 dBm to -96 dBm |
| Channels seen | 1, 2, 3 and 8 |
| Security shown in captured rows | WPA2 |
| Repeated scanning | Multiple consecutive scans completed |
| Serial baud | 115200 |
| Output | SSID, RSSI, channel and security columns were readable |

Nearby SSID names are intentionally omitted from this public record to avoid disclosing network identifiers. These measurements summarize the user's captured output; they are not a controlled RF benchmark.

### Interpreting RSSI

RSSI is reported in dBm. A value closer to zero is generally stronger: -36 dBm is stronger than -81 dBm. Readings vary with distance, obstacles, antenna orientation and radio conditions. A scan is a snapshot, not a measure of internet speed or overall network quality.

### Band limitation

The original ESP32 used by this board supports 2.4 GHz Wi-Fi. A network name containing text such as "5G" does not prove that the access point was detected on 5 GHz; SSIDs are user-defined labels. This scanner does not scan 5 GHz networks.

### Serial-output limitation

The supplied Serial Monitor text contained occasional replacement/gibberish characters around startup and between some scan blocks. The structured scan lines remained readable and repeated scanning was demonstrated. The cause was not isolated. Do not treat this issue as fixed; re-test with a fresh serial-monitor session and stable USB connection.

## 11. Troubleshooting

### Serial Monitor shows garbled text
- Confirm Serial Monitor is set to 115200 baud.
- Ensure no second application is using /dev/ttyUSB0.
- Close and reopen Serial Monitor, then press EN/RESET once.
- If noise persists between normal output blocks, capture a fresh log and investigate the USB cable, USB-UART connection and serial session. The original noise has not been diagnosed.

### Fewer networks appear than expected
Passive scanning waits for access-point beacons and can miss weak or intermittent networks. Check the external antenna connection, keep the board position fixed and repeat the scan. A missing result does not prove an access point is offline.

### RSSI changes significantly
Compare readings from the same location and antenna orientation. Obstacles, reflections, orientation and interference can change RSSI. Do not treat one reading as a stable property of an access point.

### Port not found or permission denied
Check ls -l /dev/ttyUSB*, confirm the cable supports data, and use the actual group shown on the device.

## 12. Limitations and safety

- Original ESP32 Wi-Fi is 2.4 GHz only; no 5 GHz scan.
- Passive scanning may miss weak or intermittent access points.
- Intermittent serial-output noise remains unexplained.
- Antenna connection state was not separately recorded for the captured scan.
- The sketch does not connect to discovered networks, capture payloads, collect passwords, send deauthentication frames or jam radio channels.
- Advertised authentication mode is descriptive scan information, not a security audit or proof that an access point is configured safely.
- Nearby SSIDs can identify people, homes or organizations. Avoid publishing raw SSIDs, BSSIDs or location-tagged scans without permission.
- Perform wireless observations only in compliance with local law and applicable permissions.

## 13. Improvements actually built

None recorded. Do not list future features until they have been implemented and tested.

## 14. References

- Espressif, [Arduino-ESP32 Wi-Fi API — WiFiScan](https://docs.espressif.com/projects/arduino-esp32/en/latest/api/wifi.html)
- Espressif, [ESP-IDF Wi-Fi scan types](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-guides/wifi.html)
- Espressif, [ESP32 Series datasheet](https://www.espressif.com/sites/default/files/documentation/esp32_datasheet_en.pdf)
- Espressif, [ESP32-DevKitC user guide](https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32/esp32-devkitc/user_guide.html)

---

**Documentation rule:** This entry records observed hardware behavior only. The serial noise and antenna-connection uncertainty remain explicit limitations until separately re-tested.
