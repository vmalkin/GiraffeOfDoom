
// Generally, you should use "unsigned long" for variables that hold time
// The value will quickly become too large for an int to store
unsigned long previousMillis = 0;        // will store last time LED was updated
int sensorpin = A5;

// 70 plus delay should give us plebty of read time
const long interval = 70;           

void setup() {
  // Fast serial connection.
  Serial.begin(115200);
}

void loop() {
  // here is where you'd put code that needs to be running all the time.

  // check to see if it's time to blink the LED; that is, if the difference
  // between the current time and last time you blinked the LED is bigger than
  // the interval at which you want to blink the LED.
  unsigned long currentMillis = millis();

  if (currentMillis - previousMillis >= interval) {
    Serial.println(analogRead(sensorpin));
    
    // save the last time you blinked the LED
    previousMillis = currentMillis;

    delay(30);
  }
}
