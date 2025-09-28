#include <Servo.h>

Servo bottomservo;  // create servo object to control a servo
Servo topservo;

// variables to store the servo positions/sensor value & pin
int bottompos = 90;    // 120 left, 60 right 90 d
int toppos = 55; // 20 top, 80 bottom 55 d
const int BOTTOM_ZERO = 90;
const int TOP_ZERO = 55;
const int MAX_SENSOR = 170; // 28"
const int MIN_SENSOR = 239; // 20"
int sensorValue = 0;
int sensorPin = A0;
bool runFlag = false;

void setup() {
  bottomservo.attach(11);  // attaches the servo on pin 9 to the servo object
  bottomservo.write(bottompos);
  topservo.attach(3);
  topservo.write(toppos);
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);
}

// 3D Scanning

void loop() {
  if (!runFlag) {
      String serial_string = Serial.readString();
      serial_string.trim();
      if (serial_string == "run") {
        runFlag = true;
        delay(200);
      }
  } else if (runFlag) {
    scan_sequence();
    delay(200);
    runFlag = false;
  }
}

void scan_sequence() {
  for (bottompos = 60; bottompos <= 120; bottompos += 1) {
    bottomservo.write(bottompos);
    delay(150);
    for (toppos = 20; toppos <= 80; toppos += 1) {
      topservo.write(toppos);
      delay(15);
      if (analogRead(sensorPin) >= MAX_SENSOR && analogRead(sensorPin) <= MIN_SENSOR) {
        Serial.print(analogRead(sensorPin));
        Serial.print(" ");
        Serial.print(toppos - TOP_ZERO);
        Serial.print(" ");
        Serial.println(bottompos - BOTTOM_ZERO);
        delay(2);
      }
    }
  }
  Serial.println("scan done");
}

// Calibration

// void loop() {
//   bottomservo.write(bottompos);
//   topservo.write(toppos);
//   Serial.println(analogRead(sensorPin));
// }
