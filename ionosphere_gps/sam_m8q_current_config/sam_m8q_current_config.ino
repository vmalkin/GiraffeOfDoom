/*
  Read NMEA sentences over I2C using u-blox module SAM-M8Q, NEO-M8P, ZED-F9P, etc
  By: Nathan Seidle
  SparkFun Electronics
  Date: August 22nd, 2018
  License: MIT. See license file for more information but you can
  basically do whatever you want with this code.

  This example reads the NMEA setences from the u-blox module over I2c and outputs
  them to the serial port
  
  Feel like supporting open source hardware?
  Buy a board from SparkFun!
  ZED-F9P RTK2: https://www.sparkfun.com/products/15136
  NEO-M8P RTK: https://www.sparkfun.com/products/15005
  SAM-M8Q: https://www.sparkfun.com/products/15106

  Hardware Connections:
  Plug a Qwiic cable into the GNSS and a BlackBoard
  If you don't have a platform with a Qwiic connection use the SparkFun Qwiic Breadboard Jumper (https://www.sparkfun.com/products/14425)
  Open the serial monitor at 115200 baud to see the output
*/

#include <Wire.h> //Needed for I2C to GNSS

#include <SparkFun_u-blox_GNSS_Arduino_Library.h> //Click here to get the library: http://librarymanager/All#SparkFun_u-blox_GNSS
SFE_UBLOX_GNSS myGNSS;

void setup()
{
  Serial.begin(115200);
  Serial.println("SparkFun u-blox Example");

  Wire.begin();

  if (myGNSS.begin() == false)
  {
    Serial.println(F("u-blox GNSS not detected at default I2C address. Please check wiring. Freezing."));
    while (1);
  }

//Disable or enable various NMEA sentences over the I2C interface
  myGNSS.setI2COutput(COM_TYPE_NMEA | COM_TYPE_UBX); // Turn on both UBX and NMEA sentences on I2C. (Turn off RTCM and SPARTN)
  myGNSS.disableNMEAMessage(UBX_NMEA_GLL, COM_PORT_I2C);
  myGNSS.disableNMEAMessage(UBX_NMEA_GSA, COM_PORT_I2C);
  myGNSS.enableNMEAMessage(UBX_NMEA_GSV, COM_PORT_I2C);
  myGNSS.disableNMEAMessage(UBX_NMEA_RMC, COM_PORT_I2C);
  myGNSS.disableNMEAMessage(UBX_NMEA_VTG, COM_PORT_I2C);
  myGNSS.disableNMEAMessage(UBX_NMEA_GGA, COM_PORT_I2C);
  myGNSS.disableNMEAMessage(UBX_NMEA_ZDA, COM_PORT_I2C);

  // Set the Main Talker ID to "GP". Does not work for GSV
  myGNSS.setMainTalkerID(SFE_UBLOX_MAIN_TALKER_ID_GP);

  //This will pipe all NMEA sentences to the serial port so we can see them
  myGNSS.setNMEAOutputPort(Serial);
}

void loop()
{
  myGNSS.checkUblox(); //See if new data is available. Process bytes as they come in.

  delay(100); //Don't pound too hard on the I2C bus
}
