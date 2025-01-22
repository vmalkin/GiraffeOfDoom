/***************************************************************************
  This is a library for the BMP280 humidity, temperature & pressure sensor
  This example shows how to take Sensor Events instead of direct readings
  
  Designed specifically to work with the Adafruit BMP280 Breakout
  ----> http://www.adafruit.com/products/2651

  These sensors use I2C or SPI to communicate, 2 or 4 pins are required
  to interface.

  Adafruit invests time and resources providing this open source code,
  please support Adafruit and open-source hardware by purchasing products
  from Adafruit!

  Written by Limor Fried & Kevin Townsend for Adafruit Industries.
  BSD license, all text above must be included in any redistribution
 ***************************************************************************/

#include <Wire.h>
#include <SPI.h>
#include <Adafruit_BMP280.h>
#define BMP280_ADDRESS 0x76

Adafruit_BMP280 bmp; // use I2C interface
Adafruit_Sensor *bmp_temp = bmp.getTemperatureSensor();
Adafruit_Sensor *bmp_pressure = bmp.getPressureSensor();

void setup() {
  Serial.begin(9600);
  while ( !Serial ) delay(100);   // wait for native usb
  // Serial.println(F("BMP280 Sensor event test"));

  unsigned status;
  //status = bmp.begin(BMP280_ADDRESS_ALT, BMP280_CHIPID);
  status = bmp.begin(BMP280_ADDRESS);
  // if (!status) {
  //   Serial.println(F("Could not find a valid BMP280 sensor, check wiring or "
  //                     "try a different address!"));
  //   Serial.print("SensorID was: 0x"); Serial.println(bmp.sensorID(),16);
  //   Serial.print("        ID of 0xFF probably means a bad address, a BMP 180 or BMP 085\n");
  //   Serial.print("   ID of 0x56-0x58 represents a BMP 280,\n");
  //   Serial.print("        ID of 0x60 represents a BME 280.\n");
  //   Serial.print("        ID of 0x61 represents a BME 680.\n");
  //   while (1) delay(10);
  // }

  /* Default settings from datasheet. */
  // bmp.setSampling(Adafruit_BMP280::MODE_NORMAL,     /* Operating Mode. */
  //                 Adafruit_BMP280::SAMPLING_X2,     /* Temp. oversampling */
  //                 Adafruit_BMP280::SAMPLING_X16,    /* Pressure oversampling */
  //                 Adafruit_BMP280::FILTER_X16,      /* Filtering. */
  //                 Adafruit_BMP280::STANDBY_MS_500); /* Standby time. */
  /* Default settings from datasheet. */

  // Settings for weather station incl disbale filter, so sensitive to pressure events!
  bmp.setSampling(Adafruit_BMP280::MODE_NORMAL,     /* Operating Mode. */
                  Adafruit_BMP280::SAMPLING_X2,     /* Temp. oversampling */
                  Adafruit_BMP280::SAMPLING_X16,    /* Pressure oversampling */
                  Adafruit_BMP280::FILTER_OFF,      /* Filtering. */
                  Adafruit_BMP280::STANDBY_MS_500); /* Standby time. */

  // bmp_temp->printSensorDetails();
}

void loop() {

  float reading = bmp.readPressure();
  
  if (reading < 110000)
  {
    Serial.print(bmp.readTemperature());
    Serial.print(",");
    Serial.println(reading);    
  }
  
  // Serial.print(",");
  // Serial.println(bmp.readTemperature());
  // Serial.println(" hPa");

  // Serial.println();
  delay(1000);
}
