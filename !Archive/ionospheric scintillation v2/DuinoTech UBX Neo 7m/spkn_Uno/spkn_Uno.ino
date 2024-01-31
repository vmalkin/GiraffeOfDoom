
#include <SparkFun_u-blox_GNSS_Arduino_Library.h> //http://librarymanager/All#SparkFun_u-blox_GNSS
#include <avr/wdt.h>

SFE_UBLOX_GNSS myGNSS;

#include <SoftwareSerial.h>
SoftwareSerial mySerial(10, 11); // RX, TX. Pin 10 on Uno goes to TX pin on GNSS module.

// We want to reset the Arduino after 24 hours of running
unsigned long uptime;
unsigned long timeout = 86400000;

void setup()
{
  Serial.begin(115200);
  mySerial.begin(9600);
  delay(200);
  myGNSS.begin(mySerial);
  myGNSS.factoryReset();
  
//  while (!Serial); //Wait for user to open terminal
//  Serial.println("SparkFun u-blox Example");
//
//  //Assume that the U-Blox GNSS is running at 9600 baud (the default) or at 38400 baud.
//  //Loop until we're in sync and then ensure it's at 38400 baud.
//  do {
//    Serial.println("GNSS: trying 38400 baud");
//    mySerial.begin(38400);
//    if (myGNSS.begin(mySerial) == true) break;
//
//    delay(100);
//    Serial.println("GNSS: trying 9600 baud");
//    mySerial.begin(9600);
//    if (myGNSS.begin(mySerial) == true) {
//        Serial.println("GNSS: connected at 9600 baud, switching to 38400");
////        myGNSS.setSerialRate(38400);
//        delay(100);
//    } else {
//        myGNSS.factoryReset();
//        delay(2000); //Wait a bit before trying again to limit the Serial output
//    }
//  } while(1);
  
  Serial.println("GNSS serial connected");

  myGNSS.setUART1Output(COM_TYPE_NMEA); //Set the UART port to output UBX only
  myGNSS.setI2COutput(COM_TYPE_UBX); //Set the I2C port to output UBX only (turn off NMEA noise)
  myGNSS.disableNMEAMessage(UBX_NMEA_GLL, COM_PORT_UART1); //Several of these are on by default on ublox board so let's disable them
  myGNSS.disableNMEAMessage(UBX_NMEA_GSA, COM_PORT_UART1);
  myGNSS.enableNMEAMessage(UBX_NMEA_GSV, COM_PORT_UART1);
  myGNSS.disableNMEAMessage(UBX_NMEA_RMC, COM_PORT_UART1);
  myGNSS.disableNMEAMessage(UBX_NMEA_GGA, COM_PORT_UART1); //Only leaving GGA & VTG enabled at current navigation rate
  myGNSS.disableNMEAMessage(UBX_NMEA_VTG, COM_PORT_UART1);  
  myGNSS.setNavigationFrequency(1);

  wdt_enable(WDTO_500MS);
  
}

void loop() {
    wdt_reset();
    uptime = millis();

    // Test if the arduino has been online for 24 hours, if so, delay so the watchdog timer resets
    if (uptime > timeout)
    {
      delay(2000);
      }
    
    while (mySerial.available() > 0)
    {
      Serial.write(mySerial.read());
      }
}
