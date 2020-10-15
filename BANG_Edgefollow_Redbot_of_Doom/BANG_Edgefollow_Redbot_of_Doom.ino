// Fixed Priority ARbitration controller for Redbot using 2 echo sensors and 2 photoresistors
// Robot is a photovore with collision avoidance
// Control software accounts for failure of 1/4 sensors
// Includes random drive if all else fails
#include <RedBot.h>
#include <RedBotSoftwareSerial.h>
#include <NewPing.h>

#define sonar_trig_right 11
#define sonar_echo_right 10

NewPing sonar_right (sonar_trig_right, sonar_echo_right, 100);
RedBotMotors motors;
int motorspeed = 130;
int setpoint = 20;
int hysteresis = 5;


void setup() {
  Serial.begin(9600);
}

void loop() {
  if ((readRightEcho() > setpoint - hysteresis) && (readRightEcho() < setpoint + hysteresis))
  {
    motors.stop();
    motors.drive(motorspeed);
    }
  else if ((readRightEcho() > setpoint + hysteresis))
  {
    motors.stop();
    motors.leftDrive(motorspeed);
    motors.rightDrive(motorspeed*0.8);
    }
  else if ((readRightEcho() < setpoint - hysteresis))
  {
    motors.stop();
    motors.leftDrive(motorspeed*0.8);
    motors.rightDrive(motorspeed);
    }
   
}


// *****************************************************************
// Sensor Methods
// *****************************************************************
int readRightEcho()
{
  int right = sonar_right.ping_cm();
  return right;
  }

// *****************************************************************
// Motor Methods
// *****************************************************************
void motors_drive()
{
  motors.stop();
  motors.drive(motorspeed);
  }

void motors_left()
{
  motors.stop();
  motors.rightMotor(motorspeed);  
  }

void motors_right()
{
  motors.stop();
  motors.leftMotor(motorspeed);
  }
