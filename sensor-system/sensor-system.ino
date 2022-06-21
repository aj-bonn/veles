// Including necessary libraries
#include <OneWire.h>
#include <DallasTemperature.h>

// Defining necessary variables
#define ONE_WIRE_BUS 2
#define DEVICE_DISCONNECTED_C -255

OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature temp_sensor(&oneWire);
DeviceAddress insideThermometer;

//Plant Info
String name = "Hugo";
int pnum = 10;

// Prototypes
void print_Temp(DeviceAddress addy);


void setup() {
  temp_sensor.begin();
  Serial.begin(9600);
}

void loop() {
  // PLANT INFO
  Serial.print(name);
  Serial.print("\t");
  Serial.print(pnum);
  Serial.print("\t");
  // Take time using Python
  
  // SENSOR DATA
  Serial.print(analogRead(A0)); // Capacitance
  Serial.print("\t");
  Serial.print(analogRead(A1)); // Resistance
  Serial.print("\t");
  temp_sensor.requestTemperatures();
  Serial.print(temp_sensor.getTempCByIndex(0)); // Temperature in Celsius
  Serial.println((temp_sensor.getTempCByIndex(0) * 9.0) / 5.0 + 32.0); // Temperature in Fahrenheit
  
  // Takes data every 1/2 hour
  delay(1800000);
  // Question is should the delay be here or in the Python file??? Both? A: Here
  
  /* Prev. ver. 
  Serial.print("Capacitance: ");
  Serial.println(analogRead(A0));
  Serial.print("Resistance: ");
  Serial.println(analogRead(A1));
  temp_sensor.requestTemperatures();
  Serial.print("Temp C: ");
  Serial.print(temp_sensor.getTempCByIndex(0));
  Serial.print(" Temp F: ");
  Serial.println((temp_sensor.getTempCByIndex(0) * 9.0) / 5.0 + 32.0);
  delay(1800000);
  Serial.println("");
  */
}
