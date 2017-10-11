#include <Wire.h> //I2C Arduino Library

#define addr 0x1E //I2C Address for The HMC5883

int x,y,z; //triple axis data;
float final_x, final_y, final_z;
int counter = 0;
#define output_delay 2000
#define station_name "Ruru Observatory rapid-run No2"

void setup(){
  
  Serial.begin(9600);
  Serial.println(station_name);
  
  Wire.begin();
  Wire.beginTransmission(addr); //start talking
  Wire.write(0x02); // Set the Register
  Wire.write(0x00); // Tell the HMC5883 to Continuously Measure
  Wire.endTransmission();
}


void loop(){
  //Tell the HMC what regist to begin writing data into
  Wire.beginTransmission(addr);
  Wire.write(0x03); //start with register 3.
  Wire.endTransmission();
  
 
 //Read the data.. 2 bytes for each axis.. 6 total bytes
  Wire.requestFrom(addr, 6);
  
  if(6<=Wire.available()){
    x = Wire.read()<<8; //MSB  x 
    x |= Wire.read(); //LSB  x
    z = Wire.read()<<8; //MSB  z
    z |= Wire.read(); //LSB z
    y = Wire.read()<<8; //MSB y
    y |= Wire.read(); //LSB y
  }

  final_x = final_x + x;
  final_y = final_y + y;
  final_z = final_z + z;
  counter = counter + 1;

  if (counter >= output_delay)
  {
    final_x = final_x / counter;
    final_y = final_y / counter;
    final_z = final_z / counter;
    
    // Show Values
    Serial.print(final_x,3);
    Serial.print(",");
    Serial.print(final_y,3);
    Serial.print(",");
    Serial.println(final_z,3);

    x = 0;
    y = 0;
    z = 0;
    
    final_x = 0;
    final_y = 0;
    final_z = 0;
    counter =0;
    }
}


