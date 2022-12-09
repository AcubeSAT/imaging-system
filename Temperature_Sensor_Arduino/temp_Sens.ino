#include <DHT.h>
#define DHTPIN 7     // what pin we're connected to
#define DHTTYPE DHT11   // DHT 11 
DHT dht(DHTPIN, DHTTYPE, 6);

float temperature;
float humidity;
char dataStr[100] = "";
char buffer[7];

void setup() {
  Serial.begin(9600);
  dht.begin();
}

void loop() {
  dataStr[0] = 0; 
  temperature = dht.readTemperature();
  ltoa((millis()/1000)/60,buffer,10); //convert long to charStr
  strcat(dataStr, buffer); //add it to the end
  strcat( dataStr, ", "); //append the delimiter
  dtostrf(temperature, 5, 1, buffer);  //5 is minimum width, 1 is precision; float value is copied onto buff
  strcat( dataStr, buffer); //append the converted float
  strcat( dataStr, ", "); //append the delimiter

  humidity = dht.readHumidity();
  dtostrf(humidity, 5, 1, buffer);  //5 is minimum width, 1 is precision; float value is copied onto buff
  strcat( dataStr, buffer); //append the converted float
  strcat( dataStr, 0); //terminate correctly
 
  Serial.println(dataStr);
  delay(30 * 1000);  
  delay(30 * 1000);  

}
