
// Generally, you should use "unsigned long" for variables that hold time
// The value will quickly become too large for an int to store
int sensorpin = A5;

// Variables to store current sensor data
int reading_seismo;
int reading_pressure;
int reading_temp;

//variables to store current interval times. 
unsigned long printout_millis = 0;
unsigned long weather_millis = 0;

// Constants
const int PRINTOUT_INTERVAL = 100;
const int WEATHER_INTERVAL = 1000;


void setup() {
  // Fast serial connection.
  Serial.begin(115200);
}

void loop() {
  unsigned long currentMillis = millis();

  if (currentMillis - weather_millis >= WEATHER_INTERVAL) {
    // Update interval timer
    weather_millis = currentMillis;
    // Update sensor values
    reading_temp = returnTemperature();
    reading_pressure = returnPressure()
  }

  // Output current data to serial port
  if (currentMillis - printout_millis >= PRINTOUT_INTERVAL) {
    // Update interval timer
    printout_millis = currentMillis;
    // Update sensor values AND output data thru serial port.
    reading_seismo = returnSeismo();
    Serial.print(reading_seismo);
    Serial.print(reading_temp);
    Serial.println(reading_pressure);
  }

  // A small delay
  delay(3);
}

int returnPressure()
{
  return 0;
}

int returnTemperature()
{
  return 0;
}

int returnSeismo()
{
  int data = Serial.println(analogRead(sensorpin));
  return data;
}