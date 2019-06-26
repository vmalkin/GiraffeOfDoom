// FGM-3 Fluxgate Sensor Sketch
#define FGM 8
unsigned long sensor_read_interval = 2000000;
unsigned long sensor_read_total;
unsigned long current_timer = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(FGM, INPUT_PULLUP);
  delay(5000);
}

void loop() {
  sensor_read_total = 0;
  while (sensor_read_total <= sensor_read_interval)
  {
    sensor_read_total = sensor_read_total + sensor_reading();
    }
  if (micros() > current_timer)
  {
    Serial.println(micros() - current_timer);
    current_timer = micros();
    }

}

int sensor_reading()
{
  int reading;
  reading = pulseIn(FGM, LOW);
  return reading;
  }
