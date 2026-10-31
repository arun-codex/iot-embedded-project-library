void setup() {
  Serial.begin(115200);
  Serial.println("Hello, ESP32!");
}

void loop() {
  Serial.println("ESP32 is running!");
  delay(1000);
}
