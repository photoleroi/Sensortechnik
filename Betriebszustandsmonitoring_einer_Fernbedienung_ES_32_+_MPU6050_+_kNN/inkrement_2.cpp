#define ANALOGPIN_1 ADC1_CHANNEL_4
#define ANALOGPIN_2 ADC1_CHANNEL_5
#define SWICHTPIN 25
#define NOTTASTER 15
#include "driver/adc.h"
#include <Adafruit_BMP280.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>


#define WIFI_SSID "TP-Link_C16C"
#define WIFI_CRED "08402769"
#define MQTT_BROKER "192.168.0.105"

#define MQTT_CLIENT_ID "Station1"
#define TEMPERATURE "station1/temperature"
#define PRESSURE "station1/pressure"
#define ALTITUDE "station1/altitude"
#define JOYSTICK_X "station1/joystick_x"
#define JOYSTICK_Y "station1/joystick_y"
#define JOYSTICK_SW "station1/joystick_SW"
#define NOT_TASTER "station1/nottaster"
#define ZUSTAND "station1/zustand"  // Neuer MQTT-Topic für den Zustand

// Initialisierung der WiFi und MQTT
WiFiClient espClient;
PubSubClient mqttClient(espClient);
long Timer = 0;
char result_temperature[50];
char result_pressure[50];
char result_altitude[50];
char result_joystick_x[50];
char result_joystick_y[50];
char result_joystick_sw[50];
char result_not_taster[50];
char result_zustand[50];  // Ergebnis für den Zustand

Adafruit_MPU6050 mpu;
Adafruit_BMP280 bmp280;
float temperature;
float pressure;
float altitude;
float geschwindigkeit_x;
float geschwindigkeit_y;
float geschwindigkeit_z;
float drehung_x;
float drehung_y;
float drehung_z;
int joystick_x = 0;
int joystick_y = 0;
String joystick_sw = "";
String not_taster = "";
String zustand = "";  // Variable für den Zustand

void reconnect()
{
  while (!mqttClient.connected())
  {
    Serial.print("[i] Verbinde mit MQTT ");
    if (!mqttClient.connect(MQTT_CLIENT_ID))
    {
      Serial.print("[!] MQTT-Client kann nicht verbunden werden: ");
      Serial.print(mqttClient.state());
      Serial.println("Neuer Versuch in 5 Sekunden ...");
      delay(5000);
    }
  }
}
  
void setup() {
  Serial.begin(115200);

  // WLAN-Verbindung
  Serial.print("[i] Verbinde mit WLAN ");
  Serial.print(WIFI_SSID);
  WiFi.begin(WIFI_SSID, WIFI_CRED);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.print(" OK. Eigene IP: ");
  Serial.println(WiFi.localIP());

  // MQTT-Server einrichten
  mqttClient.setServer(MQTT_BROKER, 1883);
  
  pinMode(SWICHTPIN, INPUT_PULLUP);
  pinMode(NOTTASTER, INPUT_PULLUP);
  
  Serial.println("Initialisiere BMP280 ...");
  if (!bmp280.begin(0x76)) {  
    Serial.println("BMP280 Sensor nicht gefunden. Sensor an I2C 0x76 erwartet. SD0 mit VCC verbunden?");
  } else {
    bmp280.setSampling(Adafruit_BMP280::MODE_NORMAL, Adafruit_BMP280::SAMPLING_X2,
                       Adafruit_BMP280::SAMPLING_X16, Adafruit_BMP280::FILTER_X16,
                       Adafruit_BMP280::STANDBY_MS_500);
  }

  adc1_config_width(ADC_WIDTH_BIT_10);
  adc1_config_channel_atten(ANALOGPIN_1, ADC_ATTEN_DB_11);  
  adc1_config_channel_atten(ANALOGPIN_2, ADC_ATTEN_DB_11);

  if (!mpu.begin(0x68)) {
    Serial.println("MPU6050 nicht gefunden!");
    while (1) { delay(500); }
  }
  mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
  mpu.setGyroRange(MPU6050_RANGE_500_DEG);
  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);
}

void loop() {
  if (!mqttClient.connected())
    reconnect();

  mqttClient.loop();
  
  if (millis() > Timer) {
    sensors_event_t a, g, temp;
    mpu.getEvent(&a, &g, &temp);

    joystick_x = adc1_get_raw(ANALOGPIN_1); 
    joystick_y = adc1_get_raw(ANALOGPIN_2);
    temperature = bmp280.readTemperature();
    pressure = bmp280.readPressure() / 100.0F;
    altitude = bmp280.readAltitude(1013.25);
    drehung_x = g.gyro.x;
    drehung_y = g.gyro.y;
    drehung_z = g.gyro.z;
    geschwindigkeit_x = a.acceleration.x;
    geschwindigkeit_y = a.acceleration.y;
    geschwindigkeit_z = a.acceleration.z;

    // Zustandserkennung
    if (abs(geschwindigkeit_x) < 0.2 && abs(geschwindigkeit_y) < 0.2 && abs(geschwindigkeit_z) < 0.2 &&
        abs(drehung_x) < 0.1 && abs(drehung_y) < 0.1 && abs(drehung_z) < 0.1) {
      zustand = "Ruhe";
    } else if (abs(geschwindigkeit_x) < 1 && abs(geschwindigkeit_y) < 1 && abs(geschwindigkeit_z) < 1) {
      zustand = "Transport";
    } else {
      zustand = "Betrieb";
    }

    if (digitalRead(SWICHTPIN) == 1) {
      joystick_sw = "false";
    } else {
      joystick_sw = "true";
    }
    if (digitalRead(NOTTASTER) == 1) {
      not_taster = "true";
    } else {
      not_taster = "false";
    }
  
    // Werte in Zeichenketten umwandeln
    String(temperature).toCharArray(result_temperature, 20);
    String(pressure).toCharArray(result_pressure, 20);
    String(altitude).toCharArray(result_altitude, 20);
    String(joystick_x).toCharArray(result_joystick_x, 20);
    String(joystick_y).toCharArray(result_joystick_y, 20);
    String(joystick_sw).toCharArray(result_joystick_sw, 20);
    String(not_taster).toCharArray(result_not_taster, 20);
    String(zustand).toCharArray(result_zustand, 20);

    // Daten an MQTT senden
    mqttClient.publish(TEMPERATURE, result_temperature);
    mqttClient.publish(PRESSURE, result_pressure);
    mqttClient.publish(ALTITUDE, result_altitude);
    mqttClient.publish(JOYSTICK_X, result_joystick_x);
    mqttClient.publish(JOYSTICK_Y, result_joystick_y);
    mqttClient.publish(JOYSTICK_SW, result_joystick_sw);
    mqttClient.publish(NOT_TASTER, result_not_taster);
    mqttClient.publish(ZUSTAND, result_zustand);  // Zustand veröffentlichen

    Serial.print("temp: "); Serial.println(temperature);
    Serial.print("druck: "); Serial.println(pressure);
    Serial.print("zustand: "); Serial.println(zustand);

    Timer = millis() + 500;
  }
}
