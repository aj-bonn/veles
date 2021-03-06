// Including necessary libraries
#include <OneWire.h>
#include <DallasTemperature.h>
#include <Arduino.h>

// Defining necessary variables
#define ONE_WIRE_BUS 2
#define DEVICE_DISCONNECTED_C -255

OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature temp_sensor(&oneWire);
DeviceAddress insideThermometer;

//Plant Info
String name = "Halle"; //change for each plant
int pnum = 10;
bool printemp = false;

//Recurring variables
int cap, res;

//Constants
int AIR_VAL = 600;
int WATER_VAL = 350;

// Prototypes
void print_Temp(DeviceAddress addy);


void setup() {
  temp_sensor.begin();
  Serial.begin(9600);
}

void loop() {
  if (printemp == true) {
      /* PLANT INFO */
      Serial.print(name);
      Serial.print("\t");
      Serial.print(pnum);
      Serial.print("\t");

      /* SENSOR DATA */
      // Moisture Sensor //
      // capacitance...
      cap = analogRead(A0);
      cap -= 35;
      Serial.print(cap);
      Serial.print("\t");

      // percent of water...
      int percMois = map(cap, AIR_VAL, WATER_VAL, 0, 100);
      Serial.print(percMois); //need to do a calculation
      Serial.print("\t");

      // soil moisture status...
      if (cap > 430) {
        Serial.print("Dry");
        }
      else if (cap > 350) {
        Serial.print("Wet");
        }
      else {
        Serial.print("Water");
        }
      Serial.print("\t");

      // Light Sensor //
      // resistance...
      res = analogRead(A1);
      res += 37;
      Serial.print(res);
      Serial.print("\t");

      // lux...
      float lux = 500.0/res;
      Serial.print(lux); //need to do a calculation
      Serial.print("\t");

      // Temperature Sensor //
      temp_sensor.requestTemperatures();
      Serial.print(temp_sensor.getTempCByIndex(0) + 1.2); // Temperature in Celsius
      Serial.print("\t");
      Serial.println(((temp_sensor.getTempCByIndex(0) + 1.2) * 9.0) / 5.0 + 32.0); // Temperature in Fahrenheit

      /* DATA SENT OUT EVERY MINUTE */
      delay(5000);
      //delay(60000); // so that in the future python script can be used to pull real-time data
    }
   else { // Fixes issue where data is not taken from temperature sensor at first run
      delay(500);
      printemp = true;
    }

}
