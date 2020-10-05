// Fixed Priority ARbitration controller for Redbot using 2 echo sensors and 2 photoresistors
// Robot is a photovore with collision avoidance
// Control software accounts for failure of 1/4 sensors
// Includes random drive if all else fails

#include <RedBot.h>
#include <RedBotSoftwareSerial.h>

// The states for the robot. These are considered primitive behaviours. 
#define S_DRIVE 0
#define S_LEFT 1
#define S_RIGHT 2
#define S_REVERSE 3
#define S_PAUSE 4

int robot_state
void setup() {
  // put your setup code here, to run once:
  robot_state = S_PAUSE;
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

// Sensor tests to see if we can change state

String pauseStart(int state)
{
  state = S_DRIVE;
  delay(2000);
  return state;
  }
  
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



// Motor Methods
void motors_drive()
{}

void motors_left()
{}

void motors_right()
{}

void motors_reverse()
{}

void motors_stop()
{}
