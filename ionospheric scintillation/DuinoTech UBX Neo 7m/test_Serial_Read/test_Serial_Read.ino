#include <TinyGPS.h>
#include <SoftwareSerial.h>

static const int RXPin = 11, TXPin = 10;
static const uint32_t GPSBaud = 9600;

boolean newData = false;
const byte numChars = 79;
char receivedChars[numChars];

// The serial connection to the GPS device
SoftwareSerial ss(RXPin, TXPin);
TinyGPS gps;

void setup()
{
  Serial.begin(115200);
  ss.begin(GPSBaud);
}

void loop() {
    recvWithStartEndMarkers();
    showNewData();
}

void recvWithStartEndMarkers() {
    static boolean recvInProgress = false;
    static byte ndx = 0;
    char startMarker = '$';
    char endMarker = '\n';
    char rc;
 
    while (ss.available() > 0 && newData == false) {
        rc = ss.read();

        if (recvInProgress == true) {
            if (rc != endMarker) {
                receivedChars[ndx] = rc;
                ndx++;
                if (ndx >= numChars) {
                    ndx = numChars - 1;
                }
            }
            else {
                receivedChars[ndx] = '\0'; // terminate the string
                recvInProgress = false;
                ndx = 0;
                newData = true;
            }
        }

        else if (rc == startMarker) {
            recvInProgress = true;
        }
    }
}

void showNewData() {
    if (newData == true) {
      if (receivedChars[4] == 'V')
      {
        Serial.println(receivedChars); 
        }
    newData = false;
    }
}
