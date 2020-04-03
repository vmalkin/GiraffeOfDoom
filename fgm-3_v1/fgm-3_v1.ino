// FGM-3 Fluxgate Sensor Sketch
// FGM sensor is powered off Arduino 5V. Output pin from FGM to pin 8 on Uno.
#include <avr/wdt.h>
#define FGM 8
unsigned long sensor_read_interval = 1000000;  // Approx 200000 per second
unsigned long current_timer = 0;

void setup() {
  // put your setup code here, to run once:
  wdt_enable(WDTO_8S);
  Serial.begin(9600);
  pinMode(FGM, INPUT_PULLUP);
  
}

void loop() {
  wdt_reset();
  sensor_freq();
  Serial.println(sensor_freq());
  delay(2000);
}

// This method counts pulses from the FGM for an interval of time and returns the frequency
float sensor_freq()
{
  int sensor_read_total = 0;
  float sensor_freq;
  while (sensor_read_total <= sensor_read_interval)
  {
    sensor_read_total = sensor_read_total + sensor_reading();
    }
  
  if (micros() > current_timer)
  {
    sensor_freq = sensor_read_total / (micros() - current_timer);
    // Serial.println(sensor_freq)
    current_timer = micros();
    }
  else
  {
    current_timer = 0;
    }
  return sensor_freq;
  }

int sensor_reading()
{
  int reading;
  reading = pulseIn(FGM, LOW);
  return reading;
  }
