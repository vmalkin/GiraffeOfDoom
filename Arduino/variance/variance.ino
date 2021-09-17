#include <Wire.h> //Needed for I2C to GNSS

#include <SparkFun_u-blox_GNSS_Arduino_Library.h> //http://librarymanager/All#SparkFun_u-blox_GNSS
SFE_UBLOX_GNSS myGNSS;

long lastTime = 0; //Simple local timer. Limits amount if I2C traffic to u-blox module.

void setup()
{
  Serial.begin(115200); //Increase serial speed to maximize
  while (!Serial)
    ; //Wait for user to open terminal
  Wire.begin();
  Wire.setClock(300000); // Increase I2C clock speed to 400kHz

  //myGNSS.enableDebugging(); //Uncomment this line to enable debug messages over Serial

  if (myGNSS.begin() == false) //Connect to the u-blox module using Wire port
  {
    Serial.println(F("u-blox GNSS not detected at default I2C address. Please check wiring. Freezing."));
    while (1)
      ;
  }

  myGNSS.setI2COutput(COM_TYPE_UBX); //Set the I2C port to output UBX only (turn off NMEA noise)

  // Note: not all u-blox modules can output solutions at 10Hz - or not while tracking all satellite constellations
  // If the rate drops back to 1Hz, you're asking too much of your module
  myGNSS.setNavigationFrequency(5);           //Set output to 10 times a second
  //myGNSS.saveConfiguration(); //Optional: Save the current settings to flash and BBR
}

long latitudeOld = 0;
long longitudeOld = 0;
    
void loop()
{
  // Calling getPVT returns true if there actually is a fresh navigation solution available.
  if (myGNSS.getPVT())
  {
    long latitude = myGNSS.getLatitude();
    long longitude = myGNSS.getLongitude();
    
    long dLat = latitude - latitudeOld;
    latitudeOld = latitude;
    long dLong = longitude - longitudeOld;
    longitudeOld = longitude;
    Serial.print(dLat);
    Serial.print(",");
    Serial.println(dLong);
  }
}
