/*  Example to read IMU 9250 or 6050 */
#include <Wire.h>

#define IMU_ADDRESS 0x68 // Device address
#define ACCEL_XOUT_H 0x3B // high byte of x acc see register map 6050/9250, low byte follows

uint8_t xHigh, xLow;
int16_t xAcc;

void setup() {
  Wire.begin(); // Initiate the Wire library
  Serial.begin(115200);
  delay(100);
}

void loop() {
  Wire.beginTransmission(IMU_ADDRESS); // Begin transmission to the Sensor 
  
  //Ask the particular registers for data
  Wire.write(ACCEL_XOUT_H);  // just the first register address must be sent
  Wire.endTransmission(); // Ends the transmission and transmits the data from the two registers
  Wire.requestFrom(IMU_ADDRESS, 2); // Request the high byte + the next byte which is the low byte
  
  if(Wire.available()<=2) {  // check that 2 bytes are found
    xHigh = Wire.read(); // Reads the high byte as 2 complement from register
    xLow = Wire.read(); // Reads the low byte as 2 complement from register
  }

  xAcc = (int16_t)(xHigh << 8) + (int16_t)xLow;  // cast required to convert into 16 bit value
  
  Serial.print("xHigh: ");
  Serial.print(xHigh);
  Serial.print("   xLow: ");
  Serial.print(xLow);
  Serial.print("   xAcc: ");
  Serial.println(xAcc);
  delay(1000);
}
