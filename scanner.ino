#include <Servo.h>

Servo bottomservo;  // create servo object to control a servo
Servo topservo;

// variables to store the servo positions/sensor value & pin
int bottompos = 90;    // 100 left, 60 right 90 d
int toppos = 55; // 20 top, 80 bottom 55 d
int sensorValue = 0;
int sensorPin = A0;

void setup() {
  bottomservo.attach(11);  // attaches the servo on pin 9 to the servo object
  bottomservo.write(bottompos);
  topservo.attach(3);
  topservo.write(toppos);
  Serial.begin(9600);
}

// 3D Scanning

// void loop() {
//   for (bottompos = 60; bottompos <= 100; bottompos += 1) {
//     bottomservo.write(bottompos);
//     delay(150);
//     for (toppos = 20; toppos <= 80; toppos += 1){
//       topservo.write(toppos);
//       delay(15);
//       // if (analogRead(sensorPin))
//       // Serial.println(analogRead(sensorPin));
//       delay(2);
//     }
//   }
//   while(1) {
//   //do nothing in here
// }
// }

// Calibration

void loop() {
  bottomservo.write(bottompos);
  topservo.write(toppos);
  Serial.println(analogRead(sensorPin));
}
