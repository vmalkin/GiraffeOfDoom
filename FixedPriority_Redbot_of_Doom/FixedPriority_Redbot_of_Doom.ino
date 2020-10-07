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

int motorspeed = 110;
int eye_gain_left = 0;
int eye_gain_right= 0;

RedBotMotors motors;
RedBotAccel accel;

void setup() {
  Serial.begin(9600);
  delay(2000);
  calibrateEyes();
  robot_state = S_DRIVE;
}

void loop() {
  robot_state = S_DRIVE;
  // Fall thru the possible tests for robot state.
  robot_state = doublePhoto(robot_state); // Low priority
//  robot_state = singlePhoto(robot_state); //     |
//
//  robot_state = doubleEcho(robot_state);  //     |
//  robot_state = singleEcho(robot_state);  //     V
//  robot_state = bumpDetect(robot_state);
//  robot_state = drunkWalk(robot_state);   // High priority

  // Perform action for current state.
  do_action(robot_state);

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
  int threshold = 20;
  
  int iters = 20;
  int lefty = 0;
  int righty = 0;
  for (int i = 0; i <= iters; i++)
  {
    lefty = lefty + analogRead(eye_left);
    righty = righty + analogRead(eye_right);
    }
    
  int left_value = lefty / iters;
  int right_value = righty / iters;
  
  int eye_reading = (right_value - eye_gain_right) - (left_value - eye_gain_left);
//  Serial.println(eye_reading);
  
//  if ((eye_reading < threshold) && (eye_reading > 0 - threshold))
//  {
//    state = S_DRIVE;
//    }
    
  if (eye_reading > threshold)
  {
    state = S_RIGHT;
    }

  if (eye_reading < (-1 * threshold))
  {
    state = S_LEFT;
    }
  return state;
  }

// If a photosensor is broken, we have to work differently. Without knowing which one is dead, we have to
// guide the robot to the light source. 
int singlePhoto(int state_value)
{
  return state_value;
  }

int doubleEcho(int state_value)
{
//  int threshold = 5;
  int sensor_return = state_value;

  int left = 100 - sonar_left.ping_cm();
  delay(50);
  int right = 100 - sonar_right.ping_cm();

  int sensedata = left - right;
//  int threshold_test = sqrt((sensedata)^2);

  // Object on Left, turn right
  if (sensedata < 0)
  {
    sensor_return = S_RIGHT;
//    sensor_return = S_LEFT;
    }
    
  // Object on Right, turn left
  if (sensedata > 0)
  {
    sensor_return = S_LEFT;
    }
    
  return sensor_return;
  }

// If an echosensor is broken, we have to work differently. Without knowing which one is dead, we have to
// guide the robot away from obstacles. 
int singleEcho(int state_value)
{
  return state_value;
  }

// All sensors are dead, or we can't verify their accuracy. We will implement purely ballistic behaviours
// that _eventually_ would guide our robot somewhere!
int drunkWalk(int state_value)
{
  return state_value;
  }

int antiStuck(int state_value)
{
  int newstate = state_value;
  
  accel.read();
  int h = sqrt((accel.x ^ 2) + (accel.y ^2));
  Serial.println(h);
  
  // Ballistic behaviour
  motors_reverse();
  delay(2000);
  motors_right();
  delay(666);
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
  motors.leftMotor(motorspeed);  
  }

void motors_right()
{
  motors.stop();
  motors.rightMotor(-1 * motorspeed);
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

// **********************************************************************
// Calibrate the robot eyes
// **********************************************************************
void calibrateEyes()
{
  Serial.println("Calibrating eyes...");
  float lefty = 0;
  float righty = 0;
  int i;
  for (i = 0; i < 100; i++)
  {
    lefty = lefty + analogRead(eye_left);
    righty = righty + analogRead(eye_right);
    }
  eye_gain_left = lefty / i;
  eye_gain_right = righty / i;

//  Serial.print(eye_gain_left);
//  Serial.print(" ");
//  Serial.println(analogRead(eye_left));
//  
//  Serial.println(eye_gain_right);
//  Serial.print(" ");
//  Serial.println(analogRead(eye_right));
  }
