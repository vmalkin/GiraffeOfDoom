/*
High speed may only work on parsing a single constellation, not both
#define PMTK_SET_NMEA_UPDATE_1HZ "$PMTK220,1000*1F" ///<  1 Hz
#define PMTK_SET_NMEA_UPDATE_2HZ "$PMTK220,500*2B"  ///<  2 Hz
#define PMTK_SET_NMEA_UPDATE_5HZ "$PMTK220,200*2C"  ///<  5 Hz
#define PMTK_SET_NMEA_UPDATE_10HZ "$PMTK220,100*2F" ///< 10 Hz

#define PMTK_SET_NMEA_OUTPUT_GSVONLY                                           \
  "$PMTK314,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0*29" ///< turn on just the
                                                      ///< GPGSV


*/

#include <Wire.h> //Needed for I2C to GNSS

#include <SparkFun_u-blox_GNSS_Arduino_Library.h> //Click here to get the library: http://librarymanager/All#SparkFun_u-blox_GNSS
SFE_UBLOX_GNSS myGNSS;

void setup()
{
  Serial.begin(115200);
  Serial.println("SparkFun u-blox Example");

  Wire.begin();
//  Wire.setClock(100000);
  
  if (myGNSS.begin() == false)
  {
    Serial.println(F("u-blox GNSS not detected at default I2C address. Please check wiring. Freezing."));
    while (1);
  }

/*
  With Adafruit Ultimate GPS module, we needed the following
  Set internal Baud rate to 19200
  set GPS coms to 19200
  ouput GSV only
  set update speed to 10hz
*/

//  myGNSS.factoryReset();
//  delay(5000);
//  Serial.println("Factory Reset Completed!");
  
  myGNSS.setI2COutput(COM_TYPE_NMEA); //Set the I2C port to output both NMEA and UBX messages

//  // Set the speed for update and output
//  myGNSS.setMeasurementRate(250);
//  myGNSS.setI2CpollingWait(25); // Set i2cPollingWait to 25ms
//  myGNSS.setNavigationRate(2);
//  
  
  myGNSS.setDynamicModel(DYN_MODEL_STATIONARY);
  myGNSS.setProcessNMEAMask(SFE_UBLOX_FILTER_NMEA_GSV); // Or, we can be kind to MicroNMEA and _only_ pass the GGA messages to it
  myGNSS.setNMEAOutputPort(Serial);
  myGNSS.saveConfigSelective(VAL_CFG_SUBSEC_IOPORT); //Save (only) the communications port settings to flash and BBR
  delay(1000);
}

void loop()
{
  myGNSS.checkUblox(); //See if new data is available. Process bytes as they come in.

//  delay(250); //Don't pound too hard on the I2C bus
}
