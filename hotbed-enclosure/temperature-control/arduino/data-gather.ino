#include <DHT.h>
#include <DHT_U.h>

#include <Adafruit_Sensor.h>

#include "DHT.h"

#define DHTPIN 4
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);
uint8_t actuate = HIGH;
int counter = 0;

void setup()
{
    Serial.begin(9600);
    Serial.println(F("DHTxx test!"));
    pinMode(7, OUTPUT);
    dht.begin();
}

void loop()
{
    delay(1000);
    counter++;
    float t = dht.readTemperature();

    if (counter > 10 * 60)
    {
        actuate = LOW;
    }
    digitalWrite(7, actuate);

    Serial.print(t);
    Serial.print(",");
    Serial.println(actuate);
}
