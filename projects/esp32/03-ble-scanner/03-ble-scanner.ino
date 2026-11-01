#include <Arduino.h>
#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEScan.h>
#include <BLEAdvertisedDevice.h>

// ESP32 BLE Scanner
// Board: ESP32-DevKitC-32UE
// Arduino-ESP32 Core: 3.3.12

const uint32_t SCAN_TIME_SECONDS = 5;
const uint32_t SCAN_INTERVAL_MS = 10000;

BLEScan* bleScanner = nullptr;

void setup() {
  Serial.begin(115200);
  delay(1500);

  Serial.println();
  Serial.println("================================");
  Serial.println("ESP32 BLE SCANNER");
  Serial.println("================================");

  BLEDevice::init("");

  bleScanner = BLEDevice::getScan();

  // Passive scanning: do not request scan responses.
  bleScanner->setActiveScan(false);
  bleScanner->setInterval(160);
  bleScanner->setWindow(80);

  Serial.println("BLE initialized successfully.");
}

void loop() {
  Serial.println();
  Serial.println("================================");
  Serial.println("Starting BLE scan...");
  Serial.println("================================");

  Serial.println(
    "NO | DEVICE NAME | RSSI | SERVICES | CONNECTABLE"
  );

  Serial.println(
    "------------------------------------------------"
  );

  // Wait for the scan to finish before printing results.
  BLEScanResults* results =
    bleScanner->start(SCAN_TIME_SECONDS, false);

  if (results == nullptr) {
    Serial.println("BLE scan failed.");
    delay(SCAN_INTERVAL_MS);
    return;
  }

  int deviceCount = results->getCount();

  for (int i = 0; i < deviceCount; i++) {
    BLEAdvertisedDevice device = results->getDevice(i);

    String name = device.haveName()
      ? device.getName()
      : "(name not advertised)";

    Serial.printf(
      "%02d | %-25s | %4d dBm | %2d | %s\n",
      i + 1,
      name.c_str(),
      device.getRSSI(),
      device.getServiceUUIDCount(),
      device.isConnectable() ? "Yes" : "No"
    );
  }

  Serial.println();
  Serial.printf(
    "Device records detected: %d\n",
    deviceCount
  );

  // Release stored scan results before the next scan.
  bleScanner->clearResults();

  Serial.println("Scan completed.");
  Serial.println("Next scan in 10 seconds...");

  delay(SCAN_INTERVAL_MS);
}