// Test code for Adafruit GPS modules using MTK3329/MTK3339 driver
//
// This code shows how to listen to the GPS module in an interrupt
// which allows the program to have more 'freedom' - just parse
// when a new NMEA sentence is available! Then access data when
// desired.
//
// Tested and works great with the Adafruit Ultimate GPS module
// using MTK33x9 chipset
//    ------> http://www.adafruit.com/products/746
// Pick one up today at the Adafruit electronics shop
// and help support open source hardware & software! -ada

#include <Adafruit_GPS.h>
#include <SoftwareSerial.h>

// Connect the GPS Power pin to 5V
// Connect the GPS Ground pin to ground
// Connect the GPS TX (transmit) pin to Digital 8
// Connect the GPS RX (receive) pin to Digital 7

// you can change the pin numbers to match your wiring:
SoftwareSerial mySerial(8, 7);
Adafruit_GPS GPS(&mySerial);

// Set GPSECHO to 'false' to turn off echoing the GPS data to the Serial console
// Set to 'true' if you want to debug and listen to the raw GPS sentences
#define GPSECHO  true
#define PGCMD_ANTENNA "$PGCMD,33,1*6C" // request for updates on antenna status
#define PGCMD_NOANTENNA "$PGCMD,33,0*6D"
#define FACTORY_RESET "$PMTK104*37"
#define PMTK_SET_BAUD_38400 "$PMTK251,38400*27"

String nmeaSentence;
void setup()
{
  // connect at 115200 so we can read the GPS fast enough and echo without dropping chars
  Serial.begin(115200);
  delay(100);
  Serial.println("DunedinAurora.NZ - Scintillation Monitor");
//  GPS.sendCommand(FACTORY_RESET);


// Default speed is 9600.
  GPS.begin(9600);
//  GPS.sendCommand(PMTK_SET_BAUD_9600);

  GPS.sendCommand(PGCMD_NOANTENNA); // OFF
  GPS.sendCommand(PMTK_SET_NMEA_OUTPUT_GSVONLY);  // GPGSV messages only
  GPS.sendCommand(PMTK_SET_NMEA_UPDATE_1HZ);
}
int i = 0;
void loop()                    
{
  char c = GPS.read();
  // if a sentence is received, we can check the checksum, parse it...
  
////    if (c != '\r')
//    if (c != '$')
//    {    
//       nmeaSentence = nmeaSentence + c;
//      }
//    else
//    {
//      Serial.print(nmeaSentence);
//      nmeaSentence = "";
//      }
      
  if (GPS.newNMEAreceived())
  {
    if (GPS.lastNMEA()[3] == 'G')
    {
      if (GPS.lastNMEA()[4] == 'S')
      {
        if (GPS.lastNMEA()[5] == 'V')
        {
          Serial.print(GPS.lastNMEA());
//          Serial.println(i++);
        }
      }
    }
  }
    
    if (!GPS.parse(GPS.lastNMEA()))   // this also sets the newNMEAreceived() flag to false
      return;  // we can fail to parse a sentence in which case we should just wait for another
}