#include <SPI.h>
#include <RF24.h>

// ce, csn pins
RF24 radio(9,10);

void setup() {
  // put your setup code here, to run once:
  radio.begin();
  radio.setPALevel(RF24_PA_MAX);
  radio.setChannel(0x76);
  radio.openWritingPipe(0xF0F0F0F0E1LL);
  radio.enableDynamicPayloads();
  radio.powerUp();
  
}

void loop() {
  // put your main code here, to run repeatedly:
  const char text[] = "Hello World!";
  radio.write(&text, sizeof(text));
  delay(1000);
  
}
