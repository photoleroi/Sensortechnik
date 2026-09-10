/* I2C scanner for ESP32

creation: Rui Santos
source: https://randomnerdtutorials.com/esp32-i2c-communication-arduino-ide/
modified: Joerg Dahlkemper, 2020-07-02

uses the first of 2 available I2C busses
connect SDA to G21 and SCL to G22

*/

#include <Wire.h>

void scan(){
  byte error, address;
  int nDevices;
  Serial.println("Scanning...");
  nDevices = 0;
  for(address = 1; address < 127; address++ ) {
    Wire.beginTransmission(address);
    error = Wire.endTransmission();
    if (error == 0) {
      Serial.print("I2C device found at address 0x");
      if (address<16) {
        Serial.print("0");
      }
      Serial.println(address,HEX);
      nDevices++;
    }
    else if (error==4) {
      Serial.print("Unknow error at address 0x");
      if (address<16) {
        Serial.print("0");
      }
      Serial.println(address,HEX);
    }    
  }
  if (nDevices == 0) {
    Serial.println("No I2C devices found\n");
  }
  else {
    Serial.println("done\n");
  }
  delay(5000);          
}

void setup(){
  Serial.begin(115200);
  Wire.begin();
}

void loop(){
scan();
Serial.println();
delay(5000);
} 
