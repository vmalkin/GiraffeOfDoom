#include <SparkFun_u-blox_GNSS_Arduino_Library.h>
#include <u-blox_config_keys.h>
#include <u-blox_structs.h>

#include <Wire.h> //Needed for I2C to GPS
SFE_UBLOX_GPS gps;

//char nmea_sentence[90];
//int input_index = 0;

String nmea_sentence;

void setup()
{
  Serial.begin(115200);
  //Serial.println("SparkFun Ublox Example");

  Wire.begin();

  if (gps.begin() == false)
  {
    //Serial.println(F("Ublox GPS not detected at default I2C address. Please check wiring. Freezing."));
    Serial.println(F("GPS_FAULT"));
    while (1);
  }
  //gps.setNavigationFrequency(1);
}

void loop()
{
  gps.checkUblox(); //See if new data is available. Process bytes as they come in.
  delay(1000); //Don't pound too hard on the I2C bus
}


//This function gets called from the SparkFun Ublox Arduino Library
//As each NMEA character comes in you can specify what to do with it
void SFE_UBLOX_GPS::processNMEA(char incoming)
{
  if (incoming != '\r')
  {
    nmea_sentence = nmea_sentence + incoming;
    }
  else
  {
    if (nmea_sentence[6] == 'V')
    {
      Serial.print(nmea_sentence);
      }
    nmea_sentence = "";
    }
  }
