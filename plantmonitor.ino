int plant1 = A2;
int plant2 = A4;

void setup() {
  
   Serial.begin(9600);  
   
}

void loop() {
  
  Serial.print("sensor:plant1:");
  Serial.println(analogRead(plant1));
  
  Serial.print("sensor:plant2:");
  Serial.println(analogRead(plant2));
  
  delay(1000);          
  
}