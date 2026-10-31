#include <WiFi.h>

// ESP32 Passive Wi-Fi Scanner
// Board: ESP32-DevKitC-32UE
// Arduino-ESP32 Core: 3.3.12

const unsigned long SCAN_INTERVAL = 15000;

void printEncryption(wifi_auth_mode_t security) {
  switch (security) {
    case WIFI_AUTH_OPEN:
      Serial.print("OPEN");
      break;
    case WIFI_AUTH_WEP:
      Serial.print("WEP");
      break;
    case WIFI_AUTH_WPA_PSK:
      Serial.print("WPA");
      break;
    case WIFI_AUTH_WPA2_PSK:
      Serial.print("WPA2");
      break;
    case WIFI_AUTH_WPA_WPA2_PSK:
      Serial.print("WPA/WPA2");
      break;
    case WIFI_AUTH_WPA2_ENTERPRISE:
      Serial.print("WPA2-ENTERPRISE");
      break;
    case WIFI_AUTH_WPA3_PSK:
      Serial.print("WPA3");
      break;
    case WIFI_AUTH_WPA2_WPA3_PSK:
      Serial.print("WPA2/WPA3");
      break;
    case WIFI_AUTH_WAPI_PSK:
      Serial.print("WAPI");
      break;
    default:
      Serial.print("OTHER/UNKNOWN");
      break;
  }
}

void scanWiFi() {
  Serial.println("\n====================================");
  Serial.println("       ESP32 WI-FI SCANNER");
  Serial.println("====================================");
  Serial.println("Starting passive scan...");

  // false = synchronous, false = do not request hidden SSIDs,
  // true = passive scan, 300 = maximum dwell argument per channel in ms.
  int16_t networks = WiFi.scanNetworks(false, false, true, 300);

  if (networks < 0) {
    Serial.print("Scan failed. Error: ");
    Serial.println(networks);
    WiFi.scanDelete();
    return;
  }

  if (networks == 0) {
    Serial.println("No networks found.");
  } else {
    Serial.print("\nNetworks found: ");
    Serial.println(networks);
    Serial.println("\nNO | SSID | RSSI | CHANNEL | SECURITY");
    Serial.println("-----------------------------------------------");

    for (int i = 0; i < networks; i++) {
      Serial.print(i + 1);
      Serial.print(" | ");
      Serial.print(WiFi.SSID(i));
      Serial.print(" | ");
      Serial.print(WiFi.RSSI(i));
      Serial.print(" dBm | ");
      Serial.print(WiFi.channel(i));
      Serial.print(" | ");
      printEncryption(WiFi.encryptionType(i));
      Serial.println();
      delay(10);
    }
  }

  WiFi.scanDelete();
  Serial.println("\nScan completed.");
  Serial.println("====================================");
}

void setup() {
  Serial.begin(115200);
  delay(1000);

  // Station mode is used for scanning; no credentials are supplied.
  WiFi.mode(WIFI_STA);
  WiFi.disconnect();
  delay(100);

  Serial.println("\nESP32 Wireless Recon Lab");
  Serial.println("Project 02: Wi-Fi Scanner");
}

void loop() {
  scanWiFi();
  Serial.println("\nNext scan in 15 seconds...");
  delay(SCAN_INTERVAL);
}