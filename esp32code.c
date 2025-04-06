#include "DHTesp.h"
#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>

// WiFi Credentials
const char* ssid = "Wokwi-GUEST";       
const char* password = ""; 

// Defined functions
void callbackMQTT(char *topic, byte *payload, unsigned int length);
void connectWiFi(void);
void connectMQTT(void);

// MQTT Broker Credentials, Topics and some Variables 
const char* mqtt_server = "broker.emqx.io";                 // Broker address
const int mqtt_port = 1883;                                 // Common non-secure MQTT port
const char* mqtt_user = "iot-broker";                       
const char* mqtt_password = "iot-broker";                   
const char* topic_publish = "/sensor-iot-unisinos-send";   
const char* topic_receive = "/sensor-iot-unisinos-receive";
int LDRresult = 0;

// Initialize DHT Sensor
const int DHT_PIN = 23;
DHTesp dhtSensor;

// Initialize LDR Sensor
const int LDR_PIN = 34;

// Initialize LEDs
const int LED_TEMPERATURE = 0;
const int LED_HUMIDITY = 2;
const int LED_BRIGHTNESS = 15;

// Initialize WiFi and MQTT
WiFiClient espClient;
PubSubClient client(espClient);

void connectWiFi() {
  Serial.print("Connecting to WiFi: ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("\nConnected to WiFi!");
}

void connectMQTT() {
  Serial.print("\nConnecting to MQTT broker... \n");
  client.setServer(mqtt_server, mqtt_port);

    // Receive data once any subscribed topic publish it
  client.setCallback(callbackMQTT);

  while (!client.connected()) {
    if (client.connect("ESP32Client-iot-unisinos-1", mqtt_user, mqtt_password)) {
        // subscribe in the received topic
      client.subscribe(topic_receive);
    } else {
      delay(4000); 
    }
  }
}

void callbackMQTT(char *topic, byte *payload, unsigned int length) {

  // Copy payload into a null-terminated string
  char message[length + 1];
  memcpy(message, payload, length);
  message[length] = '\0';
  
  Serial.printf("Data Received:");
  Serial.println(message);

  // Allocate JSON document (https://arduinojson.org/v6/assistant/)
  StaticJsonDocument<200> doc;

  // Parse JSON
  DeserializationError error = deserializeJson(doc, message);
  if (error)
    return;

  // Extract values
  bool tempIsOutRange = doc["tempIsOutRange"];
  bool umiIsOutRange = doc["umiIsOutRange"];
  bool brigIsOutRange = doc["brigIsOutRange"];

  // Turn ON/OFF the Leds
  if (tempIsOutRange)
    digitalWrite(LED_TEMPERATURE, HIGH);
  else
    digitalWrite(LED_TEMPERATURE, LOW);

  if (umiIsOutRange)
    digitalWrite(LED_HUMIDITY, HIGH);
  else
    digitalWrite(LED_HUMIDITY, LOW);

  if (brigIsOutRange)
    digitalWrite(LED_BRIGHTNESS, HIGH);
  else
    digitalWrite(LED_BRIGHTNESS, LOW);
}

void setup() {
  Serial.begin(115200);
  dhtSensor.setup(DHT_PIN, DHTesp::DHT22);
  
  connectWiFi();
  connectMQTT();

  pinMode(LED_TEMPERATURE, OUTPUT);
  pinMode(LED_HUMIDITY, OUTPUT);
  pinMode(LED_BRIGHTNESS, OUTPUT);
}

void loop() {

  if (!client.connected())
    connectMQTT();
  
  // Keep MQTT connection alive
  client.loop();
  
  TempAndHumidity data = dhtSensor.getTempAndHumidity();

  LDRresult = analogRead(LDR_PIN);

  const float GAMMA = 0.7;
  const float RL10 = 50;

  float voltage = float(LDRresult) / 4096. * 5.0;
  float resistance = 2000.0 * voltage / (1.0 - voltage / 5.0);
  float lux = pow(RL10 * 1e3 * pow(10.0, GAMMA) / resistance, (1.0 / GAMMA));

  // Send default value in case the brightness is not read (inf)
  if(!(isfinite(lux)))
    lux = 2000;

  // Convert sensor data to JSON
  String payload = "{";
  payload += "\"temperature\": " + String(data.temperature, 2) + ",";
  payload += "\"humidity\": " + String(data.humidity, 1) + ",";
  payload += "\"brightness\": " + String(lux);
  payload += "}";

  // Publish data to MQTT topic
  if (client.publish(topic_publish, payload.c_str()))
    Serial.println("Data Sent: " + payload);

  delay(4000);
}