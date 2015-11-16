/*

  M A G D U I N O   V E R S I O N   2
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

const int arraySize = 125; //size for running average arrays

// setup arrays to store sensor data
int xAvg[arraySize];
int yAvg[arraySize];
int zAvg[arraySize];

int xValue; // GLOBAL reported values
int yValue;
int zValue;

const int waitTimer = 15000; // wait timer for printing results to serial.  

void setup()
{
  Wire.begin();        // join i2c bus (address optional for master)
  Serial.begin(9600);  // start serial for output
  config();            // turn the MAG3110 on

  // send command to begin logging
  //Serial.println("#S|LOGMAGNETO|[]#");

  // fill arrays with zeros to init them.
  int i = 0;
  for (i = 0; i < arraySize; i++)
  {
    xAvg[i] = 0;
  }

  i = 0;
  for (i = 0; i < arraySize; i++)
  {
    yAvg[i] = 0;
  }

  i = 0;
  for (i = 0; i < arraySize; i++)
  {
    zAvg[i] = 0;
  }
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
  int iterations = 300;
  for(int i = 0; i < iterations; i++)
  {
    Smooth_Recording();
  }
}

/* #############################################################
 * S M O O T H I N G   C O D E
 * by Vaughn
 * #############################################################
 *
 */
void Smooth_Recording()
{
  // This function will use a running average to smooth out sensor data
  // We do this by creating an arrays to hold X, Y and Z values
  // populate the arrays
  // when arrays are full, ouput the average value contained in the arrays
  // then stack on a new value and drop off the oldest value
  // calculate a new average and report, repeat
  //
  // We are fiddling about with global variables, which is a bit yucky, so there's probably a more
  // "correct" way to do this...

  // FILL ARRAYS
  int i = 0;
  for (i = 0; i < arraySize; i++)//Starting at the beginning of the array
  {
    if (i == arraySize - 1) // IF we are at end of array, read the sensor
    {
      xAvg[i] = readx(); // Sensor value added to array
    }
    else
    {
      xAvg[i] = xAvg[i + 1]; // OTHERWISE grab the value from the next slot and pass it back one
    }
  }

  i = 0;
  for (i = 0; i < arraySize; i++)
  {
    if (i == arraySize - 1) // IF we are at end of array, read the sensor
    {
      yAvg[i] = ready();
    }
    else
    {
      yAvg[i] = yAvg[i + 1]; // grab the value from the next slot and pass it back one
    }
  }

  i = 0;
  for (i = 0; i < arraySize; i++)
  {
    if (i == arraySize - 1) // IF we are at end of array, read the sensor
    {
      zAvg[i] = readz();
    }
    else
    {
      zAvg[i] = zAvg[i + 1]; // grab the value from the next slot and pass it back one
    }
  }

  //Clear report values of old data
  xValue = 0;
  yValue = 0;
  zValue = 0;

  // calculate the average of the array contents and set new report values.
  i = 0;
  for (i = 0; i < arraySize; i++)
  {
    xValue = xValue + xAvg[i];
  }

  i = 0;
  for (i = 0; i < arraySize; i++)
  {
    yValue = yValue + yAvg[i];
  }

  i = 0;
  for (i = 0; i < arraySize; i++)
  {
    zValue = zValue + zAvg[i];
  }

  //Calculate the actual running average
  xValue = xValue / arraySize;
  yValue = yValue / arraySize;
  zValue = zValue / arraySize;
}

/* #############################################################
 * P R I N T   V A L U E S   C O D E
 * Adapted from Sparkfun by Vaughn
 * #############################################################
 *
 * Print values has to be a bit special.
 * We want the sensors constantly monitoring the environment, even if we are not reporting data constantly.
 * Reasons for this include, setting up the Uno to repsond to spikes in readings. If we dont I'm worried that
 * we might end up with lumpy or steplike blocks of data being reported, instead of a continuum.
 *
 * To that end, even tho the Uno is constantly looping thru recording and averaging, the report cycle happens
 * at intervals as defined by WaitCounter
 */
void print_values(void)
{       
    Serial.print(xValue);
    Serial.print(",");
    Serial.print(yValue);
    Serial.print(",");
    Serial.print(zValue);
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

