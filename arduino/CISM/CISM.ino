#include "DHT.h"
#include <math.h>

/*
 *  Inputs
 */
#define NUM_INPUTS 5
int inputid[NUM_INPUTS] = {1, 2, 3, 4, 5}; //inputid
unsigned long timelastinput[NUM_INPUTS] = {0, 0, 0, 0, 0};

#define NUM_DHT 5
DHT dht_s0(2, DHT22); //DHT sensor 0
DHT dht_s1(3, DHT22); //DHT sensor 1
DHT dht_s2(4, DHT22); //DHT sensor 2
DHT dht_s3(5, DHT22); //DHT sensor 3
DHT dht_s4(6, DHT22); //DHT sensor 4
float h[NUM_DHT] = {0, 0, 0, 0, 0}; //humidity
float t[NUM_DHT] = {0, 0, 0, 0, 0}; //temperature


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
      Serial.print("{\"outputid\":");
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
  for(byte i=0; i<5; i++){
    if(i>0) {
      Serial.print(",");
    }
    Serial.print("{\"id\":");
    Serial.print(i+1);
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
  Serial.print("}]}");
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
