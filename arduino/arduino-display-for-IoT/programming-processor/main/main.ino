/*
 * Descripción -> Uso de la pantalla nextion para la operación de relay, 
 *                motor DC, servomotor y lectura de LM35
 * Placa -> Aruino Nano
 * Shield -> Kaanbal V1.0
 * Display -> NX3224T024
*/
#include <Wire.h> 
#include <Servo.h>
#include "chimalli.h"


bool flagRelay1 = false;
bool flagMotorA = false;
String valueSensor;
Servo servoMotor;

Motor motorA = Motor(A0, A1);
Relay relay1 = Relay(4);
TemperatureSensor  sensorTemp1 = TemperatureSensor(A6);


void setup(){
  Serial.begin(9600);
  servoMotor.attach(8);
}

void loop(){
  //Array of bytes [ff, 45, ...]
  byte displayResponse[9];
  while (Serial.available() > 0){   
    for (int i = 1 ; i < 16; i++){
      displayResponse[i] =  Serial.read();
      delay(20);                 
    }
    displayResponse[9] = '\0';
    defineAction(displayResponse);
  }
}
