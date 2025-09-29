#include <Wire.h>
#include <SPI.h>
#include <Adafruit_BMP280.h>

Adafruit_BMP280 bmp; // I2C

const long intervalReporting = 100;
const long intervalBmpReading = 1000;

unsigned long previousReportingMillis = 0;
unsigned long previousBMPMillis = 0;
float currentSeismo = 0;
float currentTemp = 0;
float currentPress = 0;

void setup() {
  Serial.begin(57600);
  bmp.begin(BMP280_ADDRESS_ALT, BMP280_CHIPID);
  /* Default settings from datasheet. */
  bmp.setSampling(Adafruit_BMP280::MODE_NORMAL,     /* Operating Mode. */
                  Adafruit_BMP280::SAMPLING_X2,     /* Temp. oversampling */
                  Adafruit_BMP280::SAMPLING_X16,    /* Pressure oversampling */
                  Adafruit_BMP280::FILTER_X16,      /* Filtering. */
                  Adafruit_BMP280::STANDBY_MS_500); /* Standby time. */
}

void loop() {
  unsigned long currentMillis = millis();

  // Longer interval for reading the pressure sensor
  if (currentMillis - previousBMPMillis >= intervalBmpReading)
  {
    currentPress = readPressure();
    currentTemp = readTemperature();
    previousBMPMillis = currentMillis;
  }
  
  // The default reporting interval
  if (currentMillis - previousReportingMillis >= intervalReporting)
  {
    currentSeismo = readHallSensor();
    Serial.print(currentSeismo);
    Serial.print(",");
    Serial.print(currentPress);
    Serial.print(",");
    Serial.print(currentTemp);
    Serial.println();
    previousReportingMillis = currentMillis;
  }
}

float readTemperature()
{
  return bmp.readTemperature();
}

float readPressure()
{
  return bmp.readPressure();
}

float readHallSensor()
{
  return analogRead(A0);
}

