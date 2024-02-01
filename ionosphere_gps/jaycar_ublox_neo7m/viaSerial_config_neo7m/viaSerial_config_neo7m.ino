/*
  Test baud rate changes on serial, factory reset, and hard reset.
  By: Thorsten von Eicken
  Date: January 29rd, 2019
  License: MIT. See license file for more information but you can
  basically do whatever you want with this code.

  This example shows how to reset the U-Blox module to factory defaults over serial.

  Feel like supporting open source hardware?
  Buy a board from SparkFun!
  ZED-F9P RTK2: https://www.sparkfun.com/products/15136
  NEO-M8P RTK: https://www.sparkfun.com/products/15005
  SAM-M8Q: https://www.sparkfun.com/products/15106

  Hardware Connections:
  Connect the U-Blox serial port to Serial1
  If you're using a Uno or don't have a 2nd serial port (Serial1), use SoftwareSerial instead (see below)
  Open the serial monitor at 115200 baud to see the output
*/

#include <SparkFun_u-blox_GNSS_Arduino_Library.h> //http://librarymanager/All#SparkFun_u-blox_GNSS
SFE_UBLOX_GNSS myGNSS;

#include <SoftwareSerial.h>

//#define mySerial Serial1 // Uncomment this line to connect via Serial1
// - or -
SoftwareSerial mySerial(10, 11); // Uncomment this line to connect via SoftwareSerial(RX, TX). Connect pin 10 to GNSS TX pin.

#define defaultRate 9600 // Uncomment this line if you are using an M8 - which defaults to 9600 Baud on UART1
// - or -
//#define defaultRate 38400 // Uncomment this line if you are using an F9 - which defaults to 38400 Baud on UART1

int state = 0; // steps through auto-baud, reset, etc states

void setup()
{
  Serial.begin(115200);
  while (!Serial); //Wait for user to open terminal
  Serial.println("SparkFun u-blox Example");

    do {
    Serial.println("GNSS: trying 38400 baud");
    mySerial.begin(38400);
    if (myGNSS.begin(mySerial) == true) break;

    delay(100);
    Serial.println("GNSS: trying 9600 baud");
    mySerial.begin(9600);
    if (myGNSS.begin(mySerial) == true) {
        Serial.println("GNSS: connected at 9600 baud, switching to 38400");
        myGNSS.setSerialRate(38400);
        delay(100);
    } else {
        myGNSS.factoryReset();
        delay(2000); //Wait a bit before trying again to limit the Serial output
    }
  } while(1);

  Serial.println("GNSS serial connected");

  delay(5000);

  // myGNSS.enableNMEAMessage(UBX_NMEA_GBS, COM_PORT_UART1);
  // myGNSS.disableNMEAMessage(UBX_NMEA_GST, COM_PORT_UART1);
  // myGNSS.disableNMEAMessage(UBX_NMEA_GLL, COM_PORT_UART1);
  // myGNSS.disableNMEAMessage(UBX_NMEA_GSV, COM_PORT_UART1);
  // myGNSS.disableNMEAMessage(UBX_NMEA_GSA, COM_PORT_UART1);
  // myGNSS.disableNMEAMessage(UBX_NMEA_GGA, COM_PORT_UART1);
  // myGNSS.disableNMEAMessage(UBX_NMEA_VTG, COM_PORT_UART1);
  // myGNSS.disableNMEAMessage(UBX_NMEA_RMC, COM_PORT_UART1);
  // myGNSS.enableDebugging(); // Uncomment this line to enable helpful debug messages on Serial
}

void loop()
{
    while (mySerial.available() > 0)
    {
      Serial.write(mySerial.read());
      } 
}
