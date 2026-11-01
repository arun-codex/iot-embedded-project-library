# ESP32 BLE Scanner

**Status:** Built and verified  
**Difficulty:** Beginner  
**Board:** Espressif ESP32-DevKitC-32UE / ESP32-WROOM-32UE  
**Build verified:** 1 November 2026  
**Category:** Wireless and networking

## 1. Goal

Use the ESP32's Bluetooth Low Energy (BLE) radio to passively discover nearby devices that are advertising BLE packets. The sketch reports an advertised device name when present, RSSI, the number of advertised service UUIDs and the advertisement's connectability indication.

This project scans BLE advertisements only. It does not connect to discovered devices, pair with them, read private characteristics, collect payloads, or attempt to identify people.

## 2. Learning outcomes

- Distinguish Bluetooth Low Energy advertising from Bluetooth Classic discovery.
- Initialize the ESP32 BLE stack.
- Configure passive BLE scanning.
- Read advertised device names where provided.
- Measure RSSI and interpret its variation.
- Count service UUIDs included in advertisements.
- Understand the difference between an advertisement's connectability indication and a successful connection.
- Retrieve scan results after the scan completes and release their memory.

## 3. Prerequisites

- Basic Arduino C++: functions, pointers, loops, conditions and classes.
- Arduino IDE 2.3.10 or compatible Arduino IDE 2.x.
- ESP32 board package by Espressif Systems, version 3.3.12 for the recorded build.
- USB data cable.
- The external antenna connected to the ESP32-WROOM-32UE module.
- Nearby BLE devices that are actively advertising. Not every Bluetooth device advertises continuously.

## 4. Hardware and bill of materials

| Part | Qty | Required | Actual use | Incremental cost |
|---|---:|---|---|---:|
| ESP32-DevKitC-32UE | 1 | Yes | BLE scanning and serial output | ₹0; already owned |
| USB data cable | 1 | Yes | Power, upload and serial | ₹0; already owned |
| External antenna and pigtail for 32UE module | 1 | Yes | 2.4 GHz RF connection | ₹0; already owned |
| Breadboard and jumper wires | 1 set | No | Not used | ₹0 |

No additional purchases were needed.

**Antenna note:** ESP32-WROOM-32UE is the external-antenna module variant. Ensure the antenna is connected to its U.FL/IPEX connector before using the radio. Handle the miniature connector carefully.

## 5. Software and versions

| Item | Recorded value |
|---|---|
| Host OS | Fedora Linux |
| IDE | Arduino IDE 2.3.10 |
| Board package | esp32 by Espressif Systems 3.3.12 |
| Board profile | ESP32 Dev Module |
| Serial port | /dev/ttyUSB0 during recorded session; may change |
| Serial baud | 115200 |
| BLE implementation | BLE library bundled with Arduino-ESP32 core |
| Source headers | Arduino.h, BLEDevice.h, BLEUtils.h, BLEScan.h, BLEAdvertisedDevice.h |

No separate BLE library installation was required for the recorded build.

## 6. Wiring

No breadboard circuit or GPIO wiring is used.

1. Connect the ESP32 board to Fedora using the USB data cable.
2. Attach the external antenna to the ESP32-WROOM-32UE antenna connector.
3. Do not connect external voltage to GPIO pins.

## 7. Source code

Source file: [03-ble-scanner.ino](03-ble-scanner.ino)

The sketch follows this flow:

1. Start serial communication at 115200 baud.
2. Initialize BLE with an empty local device name.
3. Obtain the BLE scan object.
4. Configure passive scanning, interval 160 and window 80.
5. Run a synchronous five-second scan.
6. After the scan returns, iterate through stored scan results and print device name, RSSI, advertised service UUID count and connectability indication.
7. Clear stored results to release memory.
8. Wait ten seconds and begin another scan.

Printing results after the scan completes keeps serial output out of the BLE advertisement callback. This makes the output easier to inspect and avoids concurrent application-level Serial printing from that callback.

## 8. Build and upload

1. Open Arduino IDE.
2. Open this project's 03-ble-scanner.ino.
3. Select **ESP32 Dev Module**.
4. Select the ESP32 serial port. It was /dev/ttyUSB0 during the recorded session; the name may change.
5. Click **Verify**, then **Upload**.
6. Open **Tools → Serial Monitor**.
7. Set the baud rate to **115200**.
8. Allow several scan cycles to complete.

A bootloader diagnostic block after uploading or resetting the board is normal. It is separate from the BLE scan table.

## 9. Expected output

~~~text
================================
ESP32 BLE SCANNER
================================
BLE initialized successfully.

================================
Starting BLE scan...
================================
NO | DEVICE NAME | RSSI | SERVICES | CONNECTABLE
------------------------------------------------
01 | <advertised-name> | -52 dBm | 1 | Yes
02 | (name not advertised) | -49 dBm | 0 | No

Device records detected: 2
Scan completed.
Next scan in 10 seconds...
~~~

The example values are illustrative. Real results depend on devices advertising nearby, antenna orientation, distance, obstacles and radio conditions.

## 10. Actual test results

The user uploaded the sketch to the physical ESP32-DevKitC-32UE and supplied Serial Monitor screenshots and text output.

Observed results:

| Measurement | Observed value |
|---|---|
| BLE initialization | Successful |
| Records per scan | Approximately 2 to 4 in the supplied captures |
| RSSI range | -101 dBm to -43 dBm in the supplied text |
| Advertised service UUID count | 0 or 1 in the supplied rows |
| Connectability indication | Both Yes and No were observed |
| Repeated scanning | Multiple consecutive scan cycles completed |
| Serial baud | 115200 |
| Fresh output after firmware startup | Readable scan tables were shown in the screenshot and post-startup log |

Real nearby BLE device names are intentionally omitted from this public record to reduce disclosure of device identifiers. MAC addresses and raw advertising payloads were not collected by this sketch.

### Interpreting the fields

- **Device name:** A name carried in the advertisement, if one is present. Many BLE devices do not advertise a name.
- **RSSI:** Received signal strength in dBm. A value closer to zero is generally stronger; readings vary with location and antenna orientation.
- **Services:** Number of service UUIDs present in the advertisement data. This is not a count of every service the device supports or exposes after a connection.
- **Connectable:** The connectability indication inferred from the advertising packet. “Yes” does not prove that a connection or pairing would succeed.

The count is the number of scan-result records reported by the BLE scan API for that scan. It should not be treated as a guaranteed count of unique physical devices.

### Serial-output observation

The pasted capture contained a block of replacement/gibberish characters around a firmware/boot transition. After the ESP32 startup banner, repeated scan tables were readable in the supplied log and screenshot. The capture does not establish the cause of the characters before startup, so this record does not claim a root cause. The latest visible post-startup scan output was clean.

The bootloader text in the capture is recorded as startup output; by itself it does not establish an unexpected runtime crash.

## 11. Troubleshooting

### No BLE devices are detected

- Confirm the external antenna is connected to the ESP32-WROOM-32UE.
- Move near a device known to be advertising BLE.
- Remember that a phone or accessory may not advertise continuously.
- Keep the board still and try several scan cycles.

### Device names are missing

Many BLE advertisements do not include a local name. The sketch prints "(name not advertised)" in that case. This is normal and does not mean the scan failed.

### RSSI varies between scans

BLE devices may transmit intermittently and radio signals are affected by walls, reflections, distance and antenna orientation. Compare readings only under similar conditions.

### Service count is zero

The advertisement may not include service UUIDs. This does not prove that the device has no GATT services; the sketch does not connect to discover the complete GATT database.

### Serial Monitor output is garbled

- Confirm Serial Monitor is set to 115200 baud.
- Close and reopen Serial Monitor after uploading.
- Make sure no other application is using /dev/ttyUSB0.
- A bootloader message immediately after upload/reset is expected. Assess the scan table after the startup banner.
- If malformed characters continue during normal scan output, run the standalone serial diagnostic and capture a fresh log.

### Port not found or permission denied

Check ls -l /dev/ttyUSB*, confirm the cable supports data, and use the actual group shown on the device.

## 12. Limitations and safety

- This sketch discovers BLE advertisements only; it does not discover every Bluetooth Classic device.
- It does not connect, pair, read characteristics or retrieve protected device data.
- Service count is limited to UUIDs advertised in the packet; it is not a complete service inventory.
- The connectability field reflects advertising information and is not a connection test.
- Device names can expose personal or organizational information. Do not publish raw names, MAC addresses, location-tagged scans or raw advertising payloads without permission.
- Perform wireless observations only in compliance with local law and applicable permissions.

## 13. Improvements actually built

None recorded yet. Do not list future ideas as completed improvements.

## 14. References

- Espressif, [Arduino-ESP32 BLE API and scan example](https://docs.espressif.com/projects/arduino-esp32/en/latest/api/ble.html)
- Espressif, [ESP-IDF Bluetooth Low Energy documentation](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/bluetooth/index.html)
- Espressif, [ESP32 Series datasheet](https://www.espressif.com/sites/default/files/documentation/esp32_datasheet_en.pdf)
- Espressif, [ESP32-DevKitC user guide](https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32/esp32-devkitc/user_guide.html)

---

**Documentation rule:** This entry records the observed physical build. The replacement-character block around the firmware/boot transition is noted without claiming an unproven cause.
