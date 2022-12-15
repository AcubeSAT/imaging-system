#include <DHT.h>

#define DHTPIN 7 // What pin we're connected to.
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE, 6);

float temperature;
float humidity;

char dataStr[100] = "";
char buffer[7];

void setup()
{
  Serial.begin(9600);
  dht.begin();
}

void loop()
{
  dataStr[0] = 0;
  temperature = dht.readTemperature();

  ltoa((millis() / 1000) / 60, buffer, 10); // Convert long to charStr.

  strcat(dataStr, buffer);            // Add it to the end.
  strcat(dataStr, ", ");              // Append the delimiter.
  dtostrf(temperature, 5, 1, buffer); // 5 is minimum width, 1 is precision; float value is copied onto buffer.

  strcat(dataStr, buffer); // Append the converted float.
  strcat(dataStr, ", ");   // Append the delimiter.

  humidity = dht.readHumidity();
  dtostrf(humidity, 5, 1, buffer); // 5 is minimum width, 1 is precision; float value is copied onto buffer.
  strcat(dataStr, buffer);         // Append the converted float.
  strcat(dataStr, 0);              // Terminate correctly.

  Serial.println(dataStr);
  delay(30 * 1000);
  delay(30 * 1000);
}
