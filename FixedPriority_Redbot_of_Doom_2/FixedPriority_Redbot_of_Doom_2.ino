// Fixed Priority ARbitration controller for Redbot using 2 echo sensors and 2 photoresistors
// Robot is a photovore with collision avoidance
// Control software accounts for failure of 1/4 sensors
// Includes random drive if all else fails
#include <RedBot.h>
#include <RedBotSoftwareSerial.h>
#include <NewPing.h>

// The states for the robot. These are considered primitive behaviours. 
enum states {S_DRIVE, S_LEFT, S_RIGHT, S_REVERSE, S_STOP};
enum states robot_state;

// Set up for sensors
#define sonar_trig_left 3
#define sonar_echo_left 9
#define sonar_trig_right 11
#define sonar_echo_right 10
#define eye_left A0
#define eye_right A1

#define range 30
NewPing sonar_left (sonar_trig_left, sonar_echo_left, range);
NewPing sonar_right (sonar_trig_right, sonar_echo_right, range);

int motorspeed = 140;
int eye_threshold = 50;

//// Hardware Room
//float eye_gain_left = 0;
//float eye_gain_right= 250;

// my office
float eye_gain_left = 0;
float eye_gain_right= 250;

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
  robot_state = doublePhoto(robot_state); 
  robot_state = doubleEcho(robot_state);
  robot_state = stuck(robot_state);

  do_action(robot_state);
  //  debugEyes();
  Serial.print(robot_state);
  Serial.println();
}


void debugEyes()
{
  Serial.print(readLeftEye());
  Serial.print(" ");
  Serial.print(readRightEye());
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
      
    case S_LEFT:
      motors_left();  
      break;
  
    case S_RIGHT:
      motors_right();  
      break; 

    case S_STOP:
      motors_stop();
      break;

    case S_REVERSE:
      motors_reverse();
      break;
    }
  }

// *****************************************************************
// Sensor tests to see if we can change state
// *****************************************************************
int doublePhoto(int state_value)
{
  int state = state_value;
  
  float left_value = readLeftEye();
  float right_value = readRightEye();
  float diff = (left_value - right_value);
  diff = diff * diff;
  diff = sqrt(diff);
  
  if (right_value > left_value && diff > eye_threshold)
  {
    state = S_RIGHT;
    }

  if (left_value > right_value && diff > eye_threshold)
  {
    state = S_LEFT;
    }
    
//  if (diff < eye_threshold)
//  {
//    state = S_DRIVE;
//    }
  return state;
  } 


int doubleEcho(int state_value)
{
  int sensor_return = state_value;

  int left = readLeftEcho();
  delay(50);
  int right = readRightEcho();

  // Object on Left, turn right
  if (left > right )
  {
    sensor_return = S_RIGHT;
    }
    
  // Object on Right, turn left
  if (right > left)
  {
    sensor_return = S_LEFT;
    }

//  if (right == left && left == 0)
//  {
//    sensor_return = S_DRIVE;
//    }

  return sensor_return;
  }

int stuck(int state)
{
  int currentstate = state;
  accel.read();

  return currentstate;
  }


float readLeftEye()
{
  int iters = 40;
  float lefty = 0;
  for (int i = 0; i <= iters; i++)
  {
    lefty = lefty + analogRead(eye_left);
    }    
  float left_value = (lefty / iters) - eye_gain_left;
  return left_value;
  }

float readRightEye()
{
  int iters = 40;
  float righty = 0;
  for (int i = 0; i <= iters; i++)
  {
    righty = righty + analogRead(eye_right);
    }
  float right_value = (righty / iters) - eye_gain_right;
  return right_value;
  }

int readLeftEcho()
{
  int left = sonar_left.ping_cm();
  return left;
  }

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
