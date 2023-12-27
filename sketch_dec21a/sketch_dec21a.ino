    float voltage1 = 3.12;
  float voltage2 = 5.36;
  float voltage3 = 0.2;

void setup() {
  Serial.begin(9600); // Set the baud rate to match the serial monitor

}

void loop() {
  // Fixed voltage values for demonstration purposes


  int randomInt1 = random(3001);
  int randomInt2 = random(3001);
  int randomInt3 = random(3001);

  // Convert the random integer to a floating-point value between 0 and 3
  voltage1 = map(randomInt1, 0, 3000, 0.0, 3.0);
  voltage2 = map(randomInt2, 0, 3000, 0.0, 3.0);
  voltage3 = map(randomInt3, 0, 3000, 0.0, 3.0);

  // Send all three values on the same line, separated by spaces
  Serial.print(voltage1, 2); // Two decimal places for the first value
  Serial.print(" ");
  Serial.print(voltage2, 2); // Two decimal places for the second value
  Serial.print(" ");
  Serial.print(voltage3, 1); // One decimal place for the third value
  Serial.println(); // Move to the next line

  delay(0.01); // Adjust the delay as needed based on your application
}
