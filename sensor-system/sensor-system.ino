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
bool printemp = false;

// Prototypes
void print_Temp(DeviceAddress addy);


void setup() {
  temp_sensor.begin();
  Serial.begin(9600);
}

void loop() {
  if (printemp == true) {
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
      Serial.print("\t");
      Serial.println((temp_sensor.getTempCByIndex(0) * 9.0) / 5.0 + 32.0); // Temperature in Fahrenheit
      
      // Takes data every 1/2 hour
      delay(1800000);
    }
   else {
      delay(500);
      printemp = true;
    }
  
}
