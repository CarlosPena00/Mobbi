#include <SPI.h>
#include <RF24.h>
#include "printf.h"

// ce, csn pins
RF24 radio(9, 10);

byte ID[4];
char rxBuff[14];
int state = 3;


void setup() {
  Serial.begin(9600);
  // put your setup code here, to run once:
  radio.begin();
  radio.setPALevel(RF24_PA_MAX);
  radio.setChannel(0x76);
  radio.openWritingPipe(0xE8E8F0F0E2LL);
  radio.openReadingPipe(1, 0xE8E8F0F0E1LL);
  radio.enableDynamicPayloads();
  radio.setAutoAck(true);
  radio.powerUp();
  radio.printDetails();
  
  radio.startListening();

}

void ForceSendID()
{

  if (radio.available())
  {
    radio.read(rxBuff, 14);
    for (int i = 0 ; i < 14 ; i ++)

    Serial.print(rxBuff[i]);
    Serial.println(" ");
    if (rxBuff[0] == '*')
    {
      Serial.print("Send Back: ");
      Serial.println(rxBuff[1]);
      radio.stopListening();
      radio.write(&rxBuff[1], 1);  
      radio.startListening();
    }
    else{
      Serial.println("Verify Byte Error");
    }

  }
}

void loop() {
  ForceSendID();
  delay(100);
}
