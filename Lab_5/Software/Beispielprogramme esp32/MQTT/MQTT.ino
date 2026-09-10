/*
 * Demonstration eines MQTT Clients
 * 
 * Verbindet sich mit MQTT Server
 * veroeffentlich Temperaturmessung des DHT22 unter dem Topic station1/temperature
 * 
 * Voraussetzung:
 * DHT22 an Pin 16
 * WIFI_SSID ist auf das eigene WLAN zu aendern
 * WIFI_CRED ist das WLAN-Kennwort, das hier im Klartext eingegeben wird
 * MQTT_BROKER ist an die IP-Adresse des Brokers anzupassen
 * 
 * Hinweis:
 * Diese Anwendung dient zur Demonstration und bietet signifikante Angriffsflaechen fuer Hacker.
 * Eine Angabe von Kennwoertern im Klartext ist zu vermeiden.
 * Hinweise zu Sicherheitsaspekten finden sich in 
 * https://www.heise.de/developer/artikel/Sichere-IoT-Kommunikation-mit-MQTT-Teil-1-Grundlagen-3645209.html 
 */

#define WIFI_SSID "myWLAN"
#define WIFI_CRED "vollgeheim"
#define MQTT_BROKER "192.168.178.1"
#define MQTT_CLIENT_ID "Station1"
#define TOPIC_TEMPERATURE "station1/temperature"

#include <DHT.h>
#include <WiFi.h>
#include <PubSubClient.h>

// Initialisierung WiFi und MQTT
WiFiClient espClient;
PubSubClient mqttClient(espClient);
long Timer = 0;
char result_buffer[50];



void read_dht22() {
  // Dummy statt echte Sensormessung
  float temperature = 20.0;
  
  String(temperature).toCharArray(result_buffer, 20);
  mqttClient.publish(TOPIC_TEMPERATURE, result_buffer);
  Serial.print("[i]Temperatur in Grad C published: ");
  Serial.println(temperature);
  }
}


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
  dht22.begin();
  delay(100);

  // WLAN verbinden
  Serial.print("[i] Verbinde mit WLAN ");
  Serial.print(WIFI_SSID);
  WiFi.begin(WIFI_SSID, WIFI_CRED);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.print(" OK. Eigene IP: ");
  Serial.println(WiFi.localIP());

  // MQTT verbinden
  mqttClient.setServer(MQTT_BROKER, 1883);
}

void loop() {
  if (!mqttClient.connected())
    reconnect();

  mqttClient.loop();

  if (millis() > Timer)
  {
    read_dht22();
    Timer = millis() + 2500;
  }

}
