// Fixed Priority ARbitration controller for Redbot using 1 bump sensor
// Robot is a photovore with collision avoidance
// Control software accounts for failure of 1/4 sensors
// Includes random drive if all else fails
#include <RedBot.h>
#include <RedBotSoftwareSerial.h>

// The states for the robot. These are considered primitive behaviours. 
enum states {S_DRIVE, S_STUCK};
enum states robot_state;

int motorspeed = 140;
float accel_reading;

RedBotMotors motors;
RedBotAccel accel;

void setup() {
  Serial.begin(9600);
  randomSeed(analogRead(A1));
  Serial.println("Starting robot in 5 seconds...");
  delay(5000);
  robot_state = S_DRIVE;
}

void loop() {
  // Fall thru the possible tests for robot state.
  robot_state = S_DRIVE;
  robot_state = stuck(robot_state);
}

// *****************************************************************
// Do the things...
// *****************************************************************
void do_action(int state)
{
  switch(state)
  {
    case S_DRIVE:
      motors_drive();
      break;
      
    case S_STUCK:
      motors_stuck();  
      break;
    }
  }

// *****************************************************************
// Sensor tests to see if we can change state
// *****************************************************************
int stuck(int state)
{
  int currentstate = state;
  accel.read();
  float k = 0.95;
  int threshold = 100;
  float accel_prev = accel_reading;
  accel_reading = (k * accel.x) + ((1-k) * accel_prev);
  float testvalue = accel_reading - accel_prev;
  testvalue = sqrt(testvalue * testvalue);
  Serial.println(testvalue);
  if (testvalue < threshold)
  {
  currentstate = S_STUCK;
    }
  return currentstate;
  }


// *****************************************************************
// Motor Methods
// *****************************************************************
void motors_stuck()
{
  motors_reverse();
  delay(1000);
  motors_left();
  delay(500);
  }

void motors_drive()
{
  motors.stop();
  motors.drive(motorspeed);
  }

void motors_left()
{
  motors.stop();
//  motors.leftMotor(motorspeed);  
  motors.rightMotor(motorspeed);
  }

void motors_right()
{
  motors.stop();
  motors.leftMotor(-1 * motorspeed);  
//  motors.rightMotor(-1 * motorspeed);
  }

void motors_reverse()
{
  motors.stop();
  motors.drive(motorspeed * -1);
  }

void motors_stop()
{
  motors.stop();
  }
