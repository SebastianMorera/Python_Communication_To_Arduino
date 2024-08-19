void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(9600); // Set baud rate
}

void loop() {
  if (Serial.available()) {
    char command = Serial.read();
    if (command == 'O') {
      digitalWrite(LED_BUILTIN, HIGH);
    } else if (command == 'F') {
      digitalWrite(LED_BUILTIN, LOW);
    }
  }
}