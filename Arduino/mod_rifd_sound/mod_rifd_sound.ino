
#include <MFRC522.h> 
#include <SPI.h>

#define SS_PIN 10
#define RST_PIN 9

#define LIMIT 10

// Definicoes pino modulo RC522
MFRC522 mfrc522(SS_PIN, RST_PIN); 

//Led para liberacao do rfid
int led_rfid = 5;

//Led para debug de ruido
int led_sound_sensor = 4;

//Definicao dos pinos do sensor de ruido
int pino_analogico = A5;
int pino_digital = 7;

int valor_A0 = 0;
int valor_D = 0;

int control_sound_sensor = 0;

int op = 0;

void getSoundSensor(){
	if(control_sound_sensor > LIMIT){
		op = 1;
		return;
	}
	// put your main code here, to run repeatedly:
  	valor_A0 = analogRead(pino_analogico);
 	valor_D = digitalRead(pino_digital);
 	Serial.print(valor_A0);
 	Serial.print(" ");
 	Serial.println(valor_D);
 	control_sound_sensor++;

  digitalWrite(led_sound_sensor, HIGH);
  delay(10);
  digitalWrite(led_sound_sensor, LOW);
  delay(10);
}

void getRFID(){
	//Reset sound sensor
	op = 0;
	control_sound_sensor = 0;

	// Aguarda a aproximacao do cartao
  	if ( ! mfrc522.PICC_IsNewCardPresent()) 
  	{
   	 	return;
  	}
  	// Seleciona um dos cartoes
  	if ( ! mfrc522.PICC_ReadCardSerial()) 
  	{
   	 	return;
  	}

  	String conteudo = "";
  	byte letra;

  	for (byte i = 0; i < mfrc522.uid.size; i++) 
  	{
     	conteudo.concat(String(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " "));
     	conteudo.concat(String(mfrc522.uid.uidByte[i], HEX));
  	}

  	conteudo.toUpperCase();
  	//Enviar conteudo.substring(1) via serial
  	Serial.println(conteudo.substring(1));
  	
  	digitalWrite(led_rfid, HIGH);
  	delay(200);
  	digitalWrite(led_rfid, LOW);
  	delay(200);
}

void setup(){
	// Inicia a serial
  	Serial.begin(9600);
  	//Led rifd sensor
     SPI.begin();
	  pinMode(led_rfid, OUTPUT);
	//Led sound sensor
//	pinMode(led_sound_sensor, OUTPUT);
  	//inicia RFID
  	mfrc522.PCD_Init();
  	//Define pinos sensor como entrada
  	pinMode(pino_analogico, INPUT);
  	pinMode(pino_digital, INPUT);
}

void loop(){
	switch(op){
		case 0:
			getSoundSensor();
			break;
		case 1:
			getRFID();
			break;
	}
}
