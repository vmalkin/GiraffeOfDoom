// FGM-3 Fluxgate Sensor Sketch
#define FGM 8

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(FGM, INPUT_PULLUP);
}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.println(pulseIn(FGM, LOW));
}
