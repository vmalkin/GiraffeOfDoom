// Arduino code for tiltmeter using a photo-interrupt to measure fine motion of the vertical pendulum.
// BMP280 or similar is used for pressure and temperature readings.
#include <Wire.h>
#include <SPI.h>
#include <Adafruit_BMP280.h>

Adafruit_BMP280 bmp; // I2C
int sensorpin = A1;

// Variables to store current sensor data
int reading_seismo = 0;
float reading_temp = 0;
float reading_pressure = 0;

//variables to store current interval times. 
// Generally, you should use "unsigned long" for variables that hold time
// The value will quickly become too large for an int to store
unsigned long printout_millis = 0;
unsigned long weather_millis = 0;

// Constants
const int PRINTOUT_INTERVAL = 100;
const int WEATHER_INTERVAL = 1000;
#define BMP280_ADDRESS 0x76


void setup() {
  // Fast serial connection.
  Serial.begin(115200);
  unsigned status = bmp.begin(BMP280_ADDRESS);
}

void loop() {
  unsigned long currentMillis = millis();
  
  if (currentMillis - weather_millis >= WEATHER_INTERVAL) {
    // Update interval timer
    weather_millis = currentMillis;
    // Update sensor values
    reading_temp = returnTemperature();
    reading_pressure = returnPressure();
  }

  // Output current data to serial port
  if (currentMillis - printout_millis >= PRINTOUT_INTERVAL) {
    // Update interval timer
    printout_millis = currentMillis;
    // Update sensor values AND output data thru serial port.
    reading_seismo = returnSeismo();
    Serial.print(reading_seismo);
    Serial.print(',');
    Serial.print(reading_temp);
    Serial.print(',');
    Serial.println(reading_pressure);
  }

  // A small delay
  delay(3);
}

float returnTemperature()
{
  return bmp.readTemperature();
}

float returnPressure()
{
  return bmp.readPressure();
}

int returnSeismo()
{
  int seiz = analogRead(sensorpin);
  return seiz;
}
