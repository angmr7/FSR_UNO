// Define FSR sensor pins
const int fsrPins[5] = {A0, A1, A2, A3, A4};
const int threshold = 100;

bool sensorState[5] = {false, false, false, false, false};

void setup() {
  Serial.begin(9600);  // Start Serial for communication with the host
  for (int i = 0; i < 5; i++) {
    pinMode(fsrPins[i], INPUT);
  }
}

void loop() {
  for (int i = 0; i < 5; i++) {
    int sensorValue = analogRead(fsrPins[i]);

    if (sensorValue > threshold) {
      // If sensor goes above threshold and wasn’t already active
      if (!sensorState[i]) {
        sensorState[i] = true;
        Serial.print("SENSOR_");
        Serial.print(i);
        Serial.println("_PRESSED");
      }
    }
    else {
      // If sensor falls below threshold and was active
      if (sensorState[i]) {
        sensorState[i] = false;
        Serial.print("SENSOR_");
        Serial.print(i);
        Serial.println("_RELEASED");
      }
    }
  }
  delay(50);  // Simple debounce delay
}
