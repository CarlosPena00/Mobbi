int i = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  if(i<10){
    Serial.println("111 1");
  }else{
    Serial.println("30 4D E7 87");
    i = 0;  
  }
  i++;
}
