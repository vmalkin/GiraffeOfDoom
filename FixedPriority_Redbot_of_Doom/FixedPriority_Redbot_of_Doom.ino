// Fixed Priority ARbitration controller for Redbot using 2 echo sensors and 2 photoresistors
// Robot is a photovore with collision avoidance
// Control software accounts for failure of 1/4 sensors
// Includes random drive if all else fails
#include <RedBot.h>
#include <RedBotSoftwareSerial.h>
#include <NewPing.h>

// The states for the robot. These are considered primitive behaviours. 
#define S_DRIVE 0
#define S_LEFT 1
#define S_RIGHT 2
#define S_REVERSE 3
#define S_PAUSE 4

// Set up for sensors
#define sonar_trig_left 3
#define sonar_echo_left 9
#define sonar_trig_right 10
#define sonar_echo_right 11
#define eye_left A2
#define eye_right A7

#define range 30
NewPing sonar_left (sonar_trig_left, sonar_echo_left, range);
NewPing sonar_right (sonar_trig_right, sonar_echo_right, range);

int robot_state;
int motorspeed = 180;
RedBotMotors motors;

void setup() {
  
  delay(2000);
  robot_state = S_DRIVE;
}

void loop() {
  // Fall thru the possible tests for robot state.
  robot_state = doublePhoto(robot_state); // Low priority
  robot_state = singlePhoto(robot_state); //     |
  robot_state = doubleEcho(robot_state);  //     |
  robot_state = singleEcho(robot_state);  //     V
  robot_state = drunkWalk(robot_state);   // High priority

  // Perform action for current state.
  do_action(state);
}

// *****************************************************************
// Do the things...
// *****************************************************************
void do_action(state)
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
 
String doublePhoto(int state)
{
  return state;
  }

String singlePhoto(int state)
{
  return state;
  }

String doubleEcho(int state)
{
  return state;
  }

String singleEcho(int state)
{
  return state;
  }

String drunkWalk(int state)
{
  return state;
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
  motors.rightStop();
  motors.leftMotor(motorspeed, motordelay);  
  }

void motors_right()
{
  motors.leftStop();
  motors.rightMotor(-1 * motorspeed, motordelay);
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
