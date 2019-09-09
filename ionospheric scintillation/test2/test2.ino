#include <Wire.h> //Needed for I2C to GPS
#include "SparkFun_Ublox_Arduino_Library.h" 
SFE_UBLOX_GPS gps;

String nmea_sentence = "";

void setup()
{
  Serial.begin(115200);
  Serial.println("SparkFun Ublox Example");

  Wire.begin();

  if (gps.begin() == false)
  {
    Serial.println(F("Ublox GPS not detected at default I2C address. Please check wiring. Freezing."));
    while (1);
  }
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
//  Serial.print(incoming);
  nmea_sentence = nmea_sentence + incoming;

  if (incoming == '\r')
  {
    if (nmea_sentence.charAt(5) == 'V')
    {
      Serial.print(nmea_sentence);
      nmea_sentence = "";
      }
    nmea_sentence = "";
    }
}
