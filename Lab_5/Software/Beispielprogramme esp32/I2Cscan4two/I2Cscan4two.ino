/* I2C scanner for ESP32

based on: Rui Santos
source: https://randomnerdtutorials.com/esp32-i2c-communication-arduino-ide/

and Albert Vu
https://www.az-delivery.de/blogs/azdelivery-blog-fur-arduino-und-raspberry-pi/esp32-beide-i-c-schnittstellen-verwenden

modified by: Joerg Dahlkemper, 2020-07-02

There are 2 available I2C busses
Typical configuration:
I2C1: connect SDA1 to G21 and SCL to G22
I2C2: connect SDA2 to G17 and SCL to G16
*/

#include <Wire.h>

#define SDA1 21
#define SCL1 22

#define SDA2 17
#define SCL2 16

TwoWire I2Cone = TwoWire(0);
TwoWire I2Ctwo = TwoWire(1);

void scan1(){
  byte error, address;
  int nDevices;
  Serial.println("Scanning I2C 1 ...");
  nDevices = 0;
  for(address = 1; address < 127; address++ ) {
    I2Cone.beginTransmission(address);
    error = I2Cone.endTransmission();
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

void scan2(){
  byte error, address;
  int nDevices;
  Serial.println("Scanning I2C 2 ...");
  nDevices = 0;
  for(address = 1; address < 127; address++ ) {
    I2Ctwo.beginTransmission(address);
    error = I2Ctwo.endTransmission();
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
  I2Cone.begin(SDA1, SCL1, 400000); // definition of HW setup
  I2Ctwo.begin(SDA2, SCL2, 400000); // definition of HW setup
}

void loop(){
scan1();
Serial.println();
delay(100);
scan2();
Serial.println();
delay(5000);
} 
