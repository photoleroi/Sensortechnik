/* Demonstration BMP280 */

#include <Wire.h>
#include <Adafruit_BMP280.h>

Adafruit_BMP280 bmp280;

  
void setup() {
  Serial.begin(115200);
  Serial.println("Initialisiere BMP280 ...");
  if (!bmp280.begin()) {  
     Serial.println("BMP280 Sensor nicht gefunden. Sensor an I2C 0x77 erwartet. SD0 mit VCC verbunden?");
  } else {
    Serial.println("BMP280 gestartet");
    /* Standardeinstellungen setzen. */
    bmp280.setSampling(Adafruit_BMP280::MODE_NORMAL,     /* Operating Mode. */
                       Adafruit_BMP280::SAMPLING_X2,     /* Temp. oversampling */
                       Adafruit_BMP280::SAMPLING_X16,    /* Pressure oversampling */
                       Adafruit_BMP280::FILTER_X16,      /* Filtering. */
                       Adafruit_BMP280::STANDBY_MS_500); /* Standby time. */
    Serial.println("BMP280 auf Standardbetriebsart gemaess Datenblatt eingestellt.");
  }
}
  
void loop() {
    Serial.print(bmp280.readTemperature());
    Serial.print(",");
    Serial.println(bmp280.readPressure());

    // Weitere nuetzliche Funktionen
    // Serial.println(bmp280.readAltitude(1013.25));   // Hoehe bei Normaldruck 1013.25 hPa ist anzupassen

    delay(1000);
}
