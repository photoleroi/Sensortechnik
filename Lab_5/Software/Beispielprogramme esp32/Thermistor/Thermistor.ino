/*
  Analog Input

  modified for ESP32 nodeMCU von AZ delivery
  to compute value of Thermistor
  still in progress: equation on https://cdn.shopify.com/s/files/1/1509/1638/files/KY-013_Thermistor_Sensor_Modul_Datenblatt.pdf?9800502722103794008 
  compared to https://42project.net/shop/sensoren/analoger-temperatur-sensor-thermistor-ntc-ky-013-modul-mit-10-k%CF%89-fuer-arduino/ 
  but not yet working properly (wrong offset, wrong direction)

  Demonstrates analog input by reading an analog sensor on ADC1_CH4 on pin G32 and
  turning on and off a light emitting diode(LED) connected to digital pin 13.
  The amount of time the LED will be on and off depends on the value obtained
  by analogRead().

  The circuit:
  - potentiometer
    center pin of the potentiometer to the G32
    one side pin (either one) to ground
    the other side pin to +3.3 V
  - LED
    built-in LED attached to pin 

  created by David Cuartielles
  modified 30 Aug 2011
  By Tom Igoe

  This example code is in the public domain.

  http://www.arduino.cc/en/Tutorial/AnalogInput
*/

#define LEDPIN 1
#define ANALOGPIN ADC1_CHANNEL_4

#include "driver/adc.h"
#include "math.h"

int sensorValue = 0;  // variable to store the value coming from the sensor


// Steinhart-Hart equation for precise temperature reading
double Thermistor(int rawadc) {
  double Temp;
  Temp = log(((10240000/rawadc) - 10000));
  Temp = 1 / (0.001129148 + (0.000234125 + (0.0000000876741 * Temp * Temp ))* Temp );
  Temp = Temp - 273.15;
  return Temp;
}

void setup() {
  // declare the ledPin as an OUTPUT:
  pinMode(LEDPIN, OUTPUT);
  adc1_config_width(ADC_WIDTH_BIT_10);
  adc1_config_channel_atten(ANALOGPIN, ADC_ATTEN_DB_11);
  Serial.begin(115200);
}

void loop() {
  // read the value from the sensor:
  sensorValue = adc1_get_raw(ANALOGPIN);
  Serial.println(Thermistor(sensorValue));
  // turn the ledPin on
  digitalWrite(LEDPIN, HIGH);
  // stop the program for <sensorValue> milliseconds:
  delay(sensorValue);
  // turn the ledPin off:
  digitalWrite(LEDPIN, LOW);
  // stop the program for for <sensorValue> milliseconds:
  delay(1024 - sensorValue);
}
