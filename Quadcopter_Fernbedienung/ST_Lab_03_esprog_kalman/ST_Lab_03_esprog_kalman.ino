#include <Wire.h>
#include <Adafruit_BMP280.h>
#include <MPU6050_light.h>
#include <Kalman.h> // Source: https://github.com/TKJElectronics/KalmanFilter

#define RESTRICT_PITCH // Comment out to restrict roll to ±90deg instead - please read: http://www.freescale.com/files/sensors/doc/app_note/AN3461.pdf

Kalman kalmanX; // Create the Kalman instances
Kalman kalmanY;

double compAngleX, compAngleY; // Calculated angle using a complementary filter
double kalAngleX, kalAngleY; // Calculated angle using a Kalman filter


MPU6050 mpu(Wire);
Adafruit_BMP280 bmp;

const int joystickXPin = 32;
const int joystickYPin = 33;
const int joystickButtonPin = 25;
const int EbuttonPin = 26;

float temperature = 0.0;
float pressure = 0.0;
long timer = 0;
long print_timer =0;
float accX = 0.0;
float accY = 0.0;
float accZ = 0.0;
float gyroX = 0.0;
float gyroY = 0.0;
float gyroZ = 0.0;

void setup() {
  Serial.begin(115200);
  Wire.begin();
  if (!bmp.begin(0x77)) {
    //Serial.println("BMP280 Sensor error");
    while (1);
  }

  pinMode(joystickButtonPin, INPUT_PULLUP);
  pinMode(EbuttonPin, INPUT_PULLUP);
  analogReadResolution(10);  // 10-Bit-Auflösung für ADC
  
  byte status = mpu.begin();
  //Serial.print(F("MPU6050 status: "));
  //Serial.println(status);
  while(status!=0){ } // stop everything if could not connect to MPU6050
  
  //Serial.println(F("Calculating offsets, do not move MPU6050"));
  delay(1000);
  mpu.calcOffsets(true,true); // gyro and accelero
  delay(100);
  mpu.update();
  accX = mpu.getAccX();
  accY = mpu.getAccY();
  accZ = mpu.getAccZ();

  // Source: http://www.freescale.com/files/sensors/doc/app_note/AN3461.pdf eq. 25 and eq. 26
  // atan2 outputs the value of -π to π (radians) - see http://en.wikipedia.org/wiki/Atan2
  // It is then converted from radians to degrees
  double roll  = atan2(accY, accZ) * RAD_TO_DEG;
  double pitch = atan(-accX / sqrt(accY * accY + accZ * accZ)) * RAD_TO_DEG;
  
  kalmanX.setAngle(roll); // set start angle
  kalmanY.setAngle(pitch);
  compAngleX = roll; // initial values for complementary filter
  compAngleY = pitch;
  
  timer = micros();
}

void loop() {
  float temperature = bmp.readTemperature();
  float pressure = bmp.readPressure();
  mpu.update();
  accX = mpu.getAccX();
  accY = mpu.getAccY();
  accZ = mpu.getAccZ();
  gyroX = mpu.getGyroX();
  gyroY = mpu.getGyroY();
  gyroZ = mpu.getGyroZ();
  int joystickX = analogRead(joystickXPin);
  int joystickY = analogRead(joystickYPin);
  int joystickButton = digitalRead(joystickButtonPin);
  int emergencyButton = digitalRead(EbuttonPin);

  double dt = (double)(micros() - timer) / 1000000; // Calculate delta time
  timer = micros();

  // Source: http://www.freescale.com/files/sensors/doc/app_note/AN3461.pdf eq. 25 and eq. 26
  // atan2 outputs the value of -π to π (radians) - see http://en.wikipedia.org/wiki/Atan2
  // It is then converted from radians to degrees
  double roll  = atan2(accY, accZ) * RAD_TO_DEG;
  double pitch = atan(-accX / sqrt(accY * accY + accZ * accZ)) * RAD_TO_DEG;

  // Calculate roll angle
  if ((roll < -90 && kalAngleX > 90) || (roll > 90 && kalAngleX < -90)) {
    kalmanX.setAngle(roll);
    compAngleX = roll;
    kalAngleX = roll;
  } else {
    kalAngleX = kalmanX.getAngle(roll, gyroX, dt); // Calculate the angle using a Kalman filter
  }

  // Calculate pitch angle
  if (abs(kalAngleX) > 90){
    gyroY = -gyroY; // Invert rate, so it fits the restricted accelerometer reading
  }
  kalAngleY = kalmanY.getAngle(pitch, gyroY, dt);

  // Calculate the angles using a Complimentary filter
  compAngleX = 0.93 * (compAngleX + gyroX * dt) + 0.07 * roll; 
  compAngleY = 0.93 * (compAngleY + gyroY * dt) + 0.07 * pitch;


  if(millis() - print_timer >= 50.0){
    
    Serial.print(accX, 4);Serial.print(",");
    Serial.print(accY, 4);Serial.print(",");
    Serial.print(accZ, 4);Serial.print(",");
    Serial.print(gyroX, 4);Serial.print(",");
    Serial.print(gyroY, 4);Serial.print(",");
    Serial.print(gyroZ, 4);Serial.print(",");
    
    //unfiltered data calculated from accelerometer
    Serial.print(roll, 4);Serial.print(",");
    Serial.print(pitch, 4);Serial.print(",");
    //kalman filtered data
    Serial.print(kalAngleX, 4);Serial.print(",");
    Serial.print(kalAngleY, 4);Serial.print(",");
    //complementary filter data
    Serial.print(compAngleX, 4);Serial.print(",");
    Serial.print(compAngleY, 4);Serial.print(",");
    
    Serial.print(joystickX, 4);Serial.print(",");
    Serial.print(joystickY, 4);Serial.print(",");
    Serial.print(joystickButton, 4);Serial.print(",");
    Serial.print(emergencyButton, 4);Serial.println("");
    print_timer = millis();
  }

  delay(2);
}
