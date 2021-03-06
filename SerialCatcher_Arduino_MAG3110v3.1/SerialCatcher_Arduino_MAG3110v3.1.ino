/*

  M A G D U I N O   V E R S I O N   3
  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  Editor/Author: Vaughn Malkin.
  Last Edited: 2015-04-06
  
  This code explores the capabilities of the MAG3110 sensor. We're looking to see if we can make a low-cost
  magneotometer to be part of a swarm of devices to detect geomagnetic disturbances
  
  The bulk of this sketch was adapted from the Mag3110 breakout code by Aaron Weiss

*/


/*
  MAG3110 Breakout Example Code

 by: Aaron Weiss, aaron at sparkfun dot com
 SparkFun Electronics 2011
 date: 9/6/11
 license: beerware, if you use this code and happen to meet me, you
 can by me a beer

 The code reads the raw 16-bit x, y, and z values and prints them
 out. This sketch does not use the INT1 pin, nor does it poll for
 new data.

 Arduino uno: A4 (SDA), A5 (SCL)
 Arduino mega: 20 (SDA), 21 (SCL)
 Leonardo: 2 (SDA), 3 (SCL)
 Arduino due: Due: 20 (SDA), 21 (SCL), SDA1, SCL1

 */

#include <Wire.h>

#define MAG_ADDR  0x0E //7-bit address for the MAG3110, doesn't change#

const float AvgCount = 5700; //size for running average arrays

float xValue; // GLOBAL reported values
float yValue;
float zValue;

const int waitTimer = 1; // wait timer for printing results to serial.  

void setup()
{
  Wire.begin();        // join i2c bus (address optional for master)
  Serial.begin(9600);  // start serial for output
  config();            // turn the MAG3110 on
}

/*
 ##################
 M A I N   L O O P 
 ##################
*/
void loop()
{
  // Set delay
  delay(waitTimer);
  
  // Perform sensor read
  MakeRecording();

  // Ouput data to serial Port
  print_values();
}

void config(void)
{
  // set up magnetometer
  Wire.beginTransmission(MAG_ADDR); // transmit to device 0x0E
  Wire.write(0x11);              // cntrl register2
  Wire.write(0x80);              // send 0x80, enable auto resets
  Wire.endTransmission();       // stop transmitting

  delay(15);

  Wire.beginTransmission(MAG_ADDR); // transmit to device 0x0E
  Wire.write(0x10);              // cntrl register1
  Wire.write(1);                 // send 0x01, active mode
  Wire.endTransmission();       // stop transmitting
}

/*  ***************************
    M A K E   R E C O R D I N G
    ***************************
*/
void MakeRecording()
{
    Smooth_Recording();
}

/* #############################################################
 * S M O O T H I N G   C O D E
 * by Vaughn
 * #############################################################
 *
 */
void Smooth_Recording()
{
  //Clear report values of old data
  xValue = 0;
  yValue = 0;
  zValue = 0;

  // calculate the average and set new report values.
  int i = 0;
  for (i = 0; i < AvgCount; i++)
  {
    xValue = xValue + readx();
    yValue = yValue + ready();
    zValue = zValue + readz();
  }

  //Calculate the actual running average
  xValue = xValue / AvgCount;
  yValue = yValue / AvgCount;
  zValue = zValue / AvgCount;
}

/* #############################################################
 * P R I N T   V A L U E S   C O D E
 * Adapted from Sparkfun by Vaughn
 * #############################################################
 *
 */
void print_values(void)
{       
    Serial.print(xValue,3);
    Serial.print(",");
    Serial.print(yValue,3);
    Serial.print(",");
    Serial.print(zValue,3);
    Serial.print("\r\n");
}

/* #############################################################
 * M A G N E T O M E T E R   S E N S O R   R E A D   C O D E
 * by Sparkfun
 * #############################################################
 *
 */
int readx(void)
{
  int xl, xh;  //define the MSB and LSB

  Wire.beginTransmission(MAG_ADDR); // transmit to device 0x0E
  Wire.write(0x01);              // x MSB reg
  Wire.endTransmission();       // stop transmitting

  delayMicroseconds(2); //needs at least 1.3us free time between start and stop

  Wire.requestFrom(MAG_ADDR, 1); // request 1 byte
  while (Wire.available())   // slave may send less than requested
  {
    xh = Wire.read(); // receive the byte
  }

  delayMicroseconds(2); //needs at least 1.3us free time between start and stop

  Wire.beginTransmission(MAG_ADDR); // transmit to device 0x0E
  Wire.write(0x02);              // x LSB reg
  Wire.endTransmission();       // stop transmitting

  delayMicroseconds(2); //needs at least 1.3us free time between start and stop

  Wire.requestFrom(MAG_ADDR, 1); // request 1 byte
  while (Wire.available())   // slave may send less than requested
  {
    xl = Wire.read(); // receive the byte
  }

  int xout = (xl | (xh << 8)); //concatenate the MSB and LSB
  return xout;
}

int ready(void)
{
  int yl, yh;  //define the MSB and LSB

  Wire.beginTransmission(MAG_ADDR); // transmit to device 0x0E
  Wire.write(0x03);              // y MSB reg
  Wire.endTransmission();       // stop transmitting

  delayMicroseconds(2); //needs at least 1.3us free time between start and stop

  Wire.requestFrom(MAG_ADDR, 1); // request 1 byte
  while (Wire.available())   // slave may send less than requested
  {
    yh = Wire.read(); // receive the byte
  }

  delayMicroseconds(2); //needs at least 1.3us free time between start and stop

  Wire.beginTransmission(MAG_ADDR); // transmit to device 0x0E
  Wire.write(0x04);              // y LSB reg
  Wire.endTransmission();       // stop transmitting

  delayMicroseconds(2); //needs at least 1.3us free time between start and stop

  Wire.requestFrom(MAG_ADDR, 1); // request 1 byte
  while (Wire.available())   // slave may send less than requested
  {
    yl = Wire.read(); // receive the byte
  }

  int yout = (yl | (yh << 8)); //concatenate the MSB and LSB
  return yout;
}

int readz(void)
{
  int zl, zh;  //define the MSB and LSB

  Wire.beginTransmission(MAG_ADDR); // transmit to device 0x0E
  Wire.write(0x05);              // z MSB reg
  Wire.endTransmission();       // stop transmitting

  delayMicroseconds(2); //needs at least 1.3us free time between start and stop

  Wire.requestFrom(MAG_ADDR, 1); // request 1 byte
  while (Wire.available())   // slave may send less than requested
  {
    zh = Wire.read(); // receive the byte
  }

  delayMicroseconds(2); //needs at least 1.3us free time between start and stop

  Wire.beginTransmission(MAG_ADDR); // transmit to device 0x0E
  Wire.write(0x06);              // z LSB reg
  Wire.endTransmission();       // stop transmitting

  delayMicroseconds(2); //needs at least 1.3us free time between start and stop

  Wire.requestFrom(MAG_ADDR, 1); // request 1 byte
  while (Wire.available())   // slave may send less than requested
  {
    zl = Wire.read(); // receive the byte
  }

  int zout = (zl | (zh << 8)); //concatenate the MSB and LSB
  return zout;
}

