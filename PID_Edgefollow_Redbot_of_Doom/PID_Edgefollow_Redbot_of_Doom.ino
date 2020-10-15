#include <PID_v1.h>
#include <RedBot.h>
#include <RedBotSoftwareSerial.h>
#include <NewPing.h>

// Set up for sensors
#define sonar_trig_right 11
#define sonar_echo_right 10
#define range 100

int motorspeed = 120;
double Setpoint, Input, Output;
double Kp=4, Ki=0.3, Kd=0;

RedBotMotors motors;
NewPing sonar_right (sonar_trig_right, sonar_echo_right, range);
PID myPID(&Input, &Output, &Setpoint, Kp, Ki, Kd, DIRECT);

void setup() {
  Serial.begin(9600);
  Input = readRightEcho();
  Setpoint = 30;
  myPID.SetOutputLimits(-20, 20);
  myPID.SetMode(AUTOMATIC);
}

void loop(){
  Input = readRightEcho();
  myPID.Compute();
  Serial.println(Output);
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
