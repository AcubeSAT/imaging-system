#include "DHT.h"

#define DHTPIN 4

DHT dht(DHTPIN, DHTTYPE);

void setup()
{
  Serial.begin(9600);
  Serial.println(F("DHTxx test!"));
  pinMode(7, OUTPUT);
  dht.begin();
}

void loop()
{
  delay(2000);
  float t = dht.readTemperature();
  Serial.print(t);
  if (t <= 31)
    digitalWrite(7, HIGH);
  if (t > 31)
    digitalWrite(7, LOW);
}
