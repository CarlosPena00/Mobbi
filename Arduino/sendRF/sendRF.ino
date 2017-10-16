#include <SPI.h>
#include <RF24.h>
#include "printf.h"

// ce, csn pins
RF24 radio(9, 10);

char rxBuff[15];
int state = 3;

char ID[3], quant[3], temp[3], sound[3], vel[3];


int StrToHex(char str[])
{
  return (int) strtol(str, 0, 16);
}

uint16_t hex2int(char *hex) {
    uint16_t val = 0;
    for(int i = 0 ; i < 3 ; i++)
    {
        // get current character then increment
        uint8_t bte = hex[i]; 
        uint8_t var = 0;
        if (bte >= '0' && bte <= '9') 
        {
          var = bte - '0';
        }
        else if (bte >= 'a' && bte <='f')
        {
          var  = bte - 'a' + 10;
        }
        else if (bte >= 'A' && bte <='F')
        {
          var = bte - 'A' + 10;    
        }
        val = (val << 4) | var ;
    }
    return val;
}

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
    radio.read(rxBuff, 15);
    for (int i = 0 ; i < 15 ; i ++)
    {
      Serial.print(rxBuff[i]);
      if (i % 3 == 2)Serial.print(" ");
    }
    int j = 0;
    for (int i = 0 ; i < 3 ; i ++)
    {
      ID[i] = rxBuff[j];
      j++;
    }    
    for (int i = 0 ; i < 3 ; i ++)
    {
      quant[i] = rxBuff[j];
      j++;
    }
    for (int i = 0 ; i < 3 ; i ++)
    {
      temp[i] = rxBuff[j];
      j++;
    }    
    for (int i = 0 ; i < 3 ; i ++)
    {
      sound[i] = rxBuff[j];
      j++;
    }
        for (int i = 0 ; i < 3 ; i ++)
    {
      vel[i] = rxBuff[j];
      j++;
    }

  
        
    
    Serial.println(" ");
    
    
    
    Serial.println(hex2int(ID));
    Serial.println(hex2int(quant));
    Serial.println(hex2int(temp));
    Serial.println(hex2int(sound));
    Serial.println(hex2int(vel));
    
    
    if (rxBuff[0] == '*')
    {
      Serial.print("Send Back: ");
      Serial.println(rxBuff[1]);
      radio.stopListening();
      radio.write(&rxBuff[1], 1);
      radio.startListening();
    }
    else {
      Serial.println("Verify Byte Error");
    }

  }
}

void loop() {
  ForceSendID();
  delay(100);
}
