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
int sonar_trig_left = 3;
int sonar_echo_left = 9;

int sonar_trig_right = 10;
int sonar_echo_right = 11;

#define eye_left A0
#define eye_right A1

int range = 30;
NewPing sonar_left (sonar_trig_left, sonar_echo_left, range);
NewPing sonar_right (sonar_trig_right, sonar_echo_right, range);

int motorspeed = 140;
int threshold = 60;

// // Hardware Room
// float eye_gain_left = 0;
// float eye_gain_right= 250;

// my office
float eye_gain_left = 0;
float eye_gain_right= 250;

RedBotMotors motors;
RedBotAccel accel;


void setup() {
  Serial.begin(9600);
  delay(2000);
  randomSeed(analogRead(A1));
  robot_state = S_DRIVE;
}

void loop() {
  // The default state for the robot is always to drive forward. THis is changed depending on circumstances. 
  robot_state = S_DRIVE;

  // // Fall thru the possible tests to change robot state.
  // robot_state = doublePhoto(robot_state); // Low priority
  // robot_state = singlePhoto(robot_state); //     |
  robot_state = doubleEcho(robot_state);  //     |
  // // robot_state = singleEcho(robot_state);  //     V
  antiStuck();
  // robot_state = drunkWalk(robot_state);   // High priority
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
// int doublePhoto(int state_value)
// {
//   int state = state_value;
  
//   int iters = 40;
//   float lefty = 0;
//   float righty = 0;
//   for (int i = 0; i <= iters; i++)
//   {
//     lefty = lefty + analogRead(eye_left);
//     righty = righty + analogRead(eye_right);
//     }
    
//   float left_value = (lefty / iters) - eye_gain_left;
//   float right_value = (righty / iters) - eye_gain_right;
//   float diff = (left_value - right_value);
//   diff = diff * diff;
//   diff = sqrt(diff);

//   // Serial.print(left_value);
//   // Serial.print(" ");
//   // Serial.println(right_value);
  
//   if (right_value > left_value && diff > threshold)
//   {
//     state = S_RIGHT;
//     }

//   if (left_value > right_value && diff > threshold)
//   {
//     state = S_LEFT;
//     }
  
//   return state;
//   }

// If a photosensor is broken, we have to work differently. Without knowing which one is dead, we have to
// guide the robot to the light source. 
// int singlePhoto(int state_value)
// {
//   return state_value;
//   }

int doubleEcho(int state_value)
{
  // int echo_threshold = 5;
  int sensor_return = state_value;

  int left = sonar_left.ping_cm();
  delay(50);
  int right = sonar_right.ping_cm();

  // Serial.print(left);
  // Serial.print(" ");
  // Serial.println(right);

 if (left > right)
 {
  if (right ==0)
  {
    sensor_return = S_RIGHT;
  }
  // else
  // {
  //   sensor_return = S_LEFT;
  // }
 }

 if (right > left)
 {
    if(left == 0)
    {
      sensor_return = S_LEFT;
    }
    // else
    // {
    //   sensor_return = S_RIGHT;
    // }
 }
  // Serial.println(sensor_return);
  return sensor_return;
}
// // If an echosensor is broken, we have to work differently. Without knowing which one is dead, we have to
// // guide the robot away from obstacles. 
// int singleEcho(int state_value)
// {
//   return state_value;
//   }

// // All sensors are dead, or we can't verify their accuracy. We will implement purely ballistic behaviours
// // that _eventually_ would guide our robot somewhere!
// int drunkWalk(int state_value)
// {
//   return state_value;
//   }

// Ballistic behaviour to back up the robot if it seems to be stopped against something
void antiStuck()
{
  float j;
  float k;
  
  for (int i = 0; i <=1; i++)
  {
    accel.read();
    j = accel.x;
    delay(10);
    accel.read();
    k = accel.x;
  }
  float m = (j - k);
  m = m * m;
  m = sqrt(m);
  // Serial.print(m);
  if (m < 100)
  {
    // Ballistic behaviour
    Serial.println("Antistuck Behaviour firing.");
    motors_reverse();
    delay(2000);
    motors_right();
    delay(666);
    }

  }

// *****************************************************************
// Motor Methods
// *****************************************************************
void motors_drive()
{
  motors.stop();
  motors.drive(motorspeed);
  tone(buzzer, 1000); 
  }

void motors_left()
{
  motors.stop();
  motors.leftMotor(motorspeed + 20);  
  }

void motors_right()
{
  motors.stop();
  motors.rightMotor(-1 * motorspeed + 20);
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
