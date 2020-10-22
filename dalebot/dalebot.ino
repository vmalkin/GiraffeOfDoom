// FSM robot - DaleBot
// single echo sensor
#include <NewPing.h>

// The states for the robot. These are considered primitive behaviours. 
enum states {S_DRIVE, S_PIVOT, S_REVERSE, S_STOP};
enum states robot_state;

// Set up for sensors
#define sonar_trig 3
#define sonar_echo 5 
#define range 400
NewPing sonar_left (sonar_trig, sonar_echo, range);

// Set up H-Bridge and motors
int motorSpeed;
const int AIN1 = 13;           //control pin 1 on the motor driver for the right motor
const int AIN2 = 12;            //control pin 2 on the motor driver for the right motor
const int PWMA = 11;            //speed control pin on the motor driver for the right motor

const int PWMB = 10;           //speed control pin on the motor driver for the left motor
const int BIN2 = 9;           //control pin 2 on the motor driver for the left motor
const int BIN1 = 8;           //control pin 1 on the motor driver for the left moto

void setup() {
  //set the motor control pins as outputs
  pinMode(AIN1, OUTPUT);
  pinMode(AIN2, OUTPUT);
  pinMode(PWMA, OUTPUT);
  pinMode(BIN1, OUTPUT);
  pinMode(BIN2, OUTPUT);
  pinMode(PWMB, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  robot_state = testState();
  doAction(robot_state);
}

// ---------------------------------------------------------------------------------
// Test state 
// ---------------------------------------------------------------------------------
int testState(int state)
{
  int currentstate = state;
  switch (currentstate)
  {
    case S_DRIVE
    }
  return currentstate;
  }

// ---------------------------------------------------------------------------------
// perform action for state. 
// ---------------------------------------------------------------------------------
void doAction(int state)
{
  
  }

// ---------------------------------------------------------------------------------
// Read echo sensor 
// ---------------------------------------------------------------------------------
int readEcho()
{
  delay(50);
  int distance = sonar.ping_cm();
  return distance
  }

// ---------------------------------------------------------------------------------
// Motor Methods. 
// ---------------------------------------------------------------------------------
void motors_drive()
{
  
  }

void motors_pivot()
{
  
  }

void motors_reverse()
{
  
  }

void motors_stop()
{
  
  }
