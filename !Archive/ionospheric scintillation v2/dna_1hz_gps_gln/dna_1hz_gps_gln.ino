#include <Wire.h> //Needed for I2C to GNSS
#include <SparkFun_u-blox_GNSS_Arduino_Library.h> //Click here to get the library: http://librarymanager/All#SparkFun_u-blox_GNSS
SFE_UBLOX_GNSS myGNSS;

void setup()
{
  Serial.begin(115200);
  Serial.println("SparkFun u-blox Example");

  Wire.begin();
/*
  With Adafruit Ultimate GPS module, we needed the following
  Set internal Baud rate to 19200
  set GPS coms to 19200
  ouput GSV only
  set update speed to 10hz
*/
  if (myGNSS.begin() == false)
  {
    Serial.println(F("u-blox GNSS not detected at default I2C address. Please check wiring. Freezing."));
    while (1);
  }
//  myGNSS.factoryReset();
//  myGNSS.hardReset();
//  delay(7000);
//  Serial.println("Factory Reset Completed!");
  
  myGNSS.setI2COutput(COM_TYPE_NMEA); //Set the I2C port to output both NMEA and UBX messages
//  myGNSS.setI2COutput(COM_TYPE_UBX); //Set the I2C port to output both NMEA and UBX messages

//  // Set the speed for update and output
 myGNSS.setMeasurementRate(250);
 myGNSS.setI2CpollingWait(25); // Set i2cPollingWait to 25ms
  myGNSS.setNavigationFrequency(2);
  myGNSS.setDynamicModel(DYN_MODEL_STATIONARY);
  //Disable or enable various NMEA sentences over the UART1 interface
  myGNSS.disableNMEAMessage(UBX_NMEA_GLL, COM_PORT_I2C); //Several of these are on by default on ublox board so let's disable them
  myGNSS.disableNMEAMessage(UBX_NMEA_GSA, COM_PORT_I2C);
  myGNSS.enableNMEAMessage(UBX_NMEA_GSV, COM_PORT_I2C);
  myGNSS.disableNMEAMessage(UBX_NMEA_RMC, COM_PORT_I2C);
  myGNSS.disableNMEAMessage(UBX_NMEA_GGA, COM_PORT_I2C); //Only leaving GGA & VTG enabled at current navigation rate
  myGNSS.disableNMEAMessage(UBX_NMEA_VTG, COM_PORT_I2C);  
  myGNSS.configureMessage(UBX_CLASS_NAV, UBX_NAV_PVT, COM_PORT_I2C, 0); //Message Class, ID, and port we want to configure, sendRate of 0 (disable).
  
  
  myGNSS.setNMEAOutputPort(Serial);
  myGNSS.saveConfigSelective(VAL_CFG_SUBSEC_IOPORT); //Save (only) the communications port settings to flash and BBR
  delay(1000);
}

void loop()
{
  myGNSS.checkUblox(); //See if new data is available. Process bytes as they come in.

//  delay(250); //Don't pound too hard on the I2C bus
}
