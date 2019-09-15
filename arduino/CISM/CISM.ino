#include "DHT.h"
#include <math.h>

/*
 *  Inputs
 */
#define NUM_INPUTS 10
int inputid[NUM_INPUTS] = {1, 2, 3, 4, 5, 11, 12, 13, 14, 15}; //inputid
unsigned long timelastinput[NUM_INPUTS] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0};

#define NUM_DHT 10
DHT dht_s0(2, DHT22); //DHT sensor 0
DHT dht_s1(3, DHT22); //DHT sensor 1
DHT dht_s2(4, DHT22); //DHT sensor 2
DHT dht_s3(5, DHT22); //DHT sensor 3
DHT dht_s4(6, DHT22); //DHT sensor 4
DHT dht_s5(7, DHT22); //DHT sensor 5
DHT dht_s6(8, DHT22); //DHT sensor 6
DHT dht_s7(9, DHT22); //DHT sensor 7
DHT dht_s8(10, DHT22); //DHT sensor 8
DHT dht_s9(11, DHT22); //DHT sensor 9
float h[NUM_DHT] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0}; //humidity
float t[NUM_DHT] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0}; //temperature


/*
 *  Outputs
 */
#define NUM_OUTPUTS 1
int output[NUM_OUTPUTS][4] = {{1, 13, 0, 1}}; //outputid, pin, PWM, value
unsigned long timelastoutput[NUM_OUTPUTS] = {0};

/*
 *  Rules
 */
float maxTemp = 80;



String comString;
boolean comComplete = false;
unsigned long now = 0;

void setup() {
  Serial.begin(115200);
  //while (!Serial) {
  //  ; // wait for serial port to connect. Needed for Leonardo only
  //} 
  Serial.println("{\"name\":\"CISM\",\"version\":\"0.02\"}");
  comString.reserve(10);
  
  /*
   *  Inputs
   */
  dht_s0.begin();
  dht_s1.begin();
  dht_s2.begin();
  dht_s3.begin();
  dht_s4.begin();
  dht_s5.begin();
  dht_s6.begin();
  dht_s7.begin();
  dht_s8.begin();
  dht_s9.begin();

  /*
   *  Outputs
   */
  for (int i=0; i<NUM_OUTPUTS; i++){
    pinMode(output[i][1], OUTPUT);
    if (output[i][2]==0){
      digitalWrite(output[i][1], output[i][3]);
    }else{
      analogWrite(output[i][1], output[i][3]);
    }
  }
  
}

void loop() {
  
  if (Serial.available() > 0) {
    char inChar = (char)Serial.read();
    if(inChar == '\n') {
      comComplete = true;
    }else{
      comString += inChar;
    }
  }
  if(comComplete) {
    //Serial.println(comString);
    
    if(comString=="getjson") {
      readSensors();
      outputJSON();
      
    } else if(comString.substring(0,9)=="setoutput") {
      comString = comString.substring(9);
      comString.trim();
      
      char c[10];
      
      comString.substring(0,comString.indexOf(' ')).toCharArray(c, 10);;
      int arg0 = atoi(c);
      
      comString.substring(comString.indexOf(' ')+1).toCharArray(c, 10);
      int arg1 = atoi(c);
      
      output[arg0][3] = arg1;
      
      //Serial.print("{\"output\":[{\"id\":");
      //Serial.print(output[0][0]);
      //Serial.print(",\"data\":");
      //Serial.print(output[0][3]);
      //Serial.println("}]}")
      
      
      Serial.print("{\"outputid\":");
      Serial.print(output[arg0][0]);
      Serial.println("}");
      
    } else {
      Serial.println("{\"!\":\"unknown command\"}");
    }
    comComplete = false;
    comString = "";
  }
  
  
  now = millis();
  for(byte i=0; i<NUM_INPUTS; i++){
    if((now - timelastinput[i]) > 5000){
      readSensors();  
    }
  }
  
  for(byte i=0; i<NUM_OUTPUTS; i++){
    if((now - timelastoutput[i]) > 10000){
      digitalWrite(output[i][1], output[i][3]);
      timelastoutput[i] = now;
    }
  }
}

void outputJSON() {
  // check if returns are valid, if they are NaN (not a number) then something went wrong!
  Serial.print("{\"input\":[");
  for(byte i=0; i<NUM_INPUTS; i++){
    if(i>0) {
      Serial.print(",");
    }
    Serial.print("{\"id\":");
    Serial.print(inputid[i]); //id
    
    Serial.print(",\"temperature\":");
    if (isnan(t[i]) || isnan(h[i])){
      Serial.print("\"nan\"");
    }else{
      Serial.print(t[i]);
    }
    Serial.print(",");
    Serial.print("\"humidity\":"); 
    if (isnan(t[i]) || isnan(h[i])){
      Serial.print("\"nan\"");
    }else{
      Serial.print(h[i]);
    }
    Serial.print("}");
  }
  Serial.print("],\"output\":[{\"id\":");
  Serial.print(output[0][0]);
  Serial.print(",\"data\":");
  Serial.print(output[0][3]);
  Serial.println("}]}");
}

void readSensors() {
  // Reading temperature or humidity takes about 250 milliseconds!
  // Sensor readings may also be up to 2 seconds 'old' (its a very slow sensor)
  h[0] = dht_s0.readHumidity();
  t[0] = dht_s0.readTemperature(true);
  h[1] = dht_s1.readHumidity();
  t[1] = dht_s1.readTemperature(true);
  h[2] = dht_s2.readHumidity();
  t[2] = dht_s2.readTemperature(true);
  h[3] = dht_s3.readHumidity();
  t[3] = dht_s3.readTemperature(true); 
  h[4] = dht_s4.readHumidity();
  t[4] = dht_s4.readTemperature(true);
  h[5] = dht_s5.readHumidity();
  t[5] = dht_s5.readTemperature(true);
  h[6] = dht_s6.readHumidity();
  t[6] = dht_s6.readTemperature(true);
  h[7] = dht_s7.readHumidity();
  t[7] = dht_s7.readTemperature(true);
  h[8] = dht_s8.readHumidity();
  t[8] = dht_s8.readTemperature(true); 
  h[9] = dht_s9.readHumidity();
  t[9] = dht_s9.readTemperature(true);
  
  //Evaluate Rules
  output[0][3] = 1;
  for(byte i=0; i<NUM_INPUTS; i++){
    if(t[i] >= maxTemp){
      output[0][3] = 0;
    }
  }
  
  for(byte i=0; i<NUM_INPUTS; i++){
    timelastinput[i] = millis();  
  }
}
