#include "BluetoothSerial.h"
/* Check if Bluetooth configurations are enabled in the SDK */
/* If not, then you have to recompile the SDK */

#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
#error Bluetooth is not enabled! Please run `make menuconfig` to and enable it
#endif
BluetoothSerial SerialBT;
int light36 = 0;
const int potPin36 = 36;
int light35 = 0;
const int potPin35 = 35;
int light34 = 0;
const int potPin34 = 26;
int light33 = 0;
const int potPin33 = 25;

const int ledPin22 = 22; // 730-740nm power led output (0-230 hertz)  ==> 30mA , 1.42 Volt
const int ledPin21 = 21; // 840-850nm power led output (0-230 hertz)  ==> 35mA , 1.27 Volt
const int freq = 5000;
const int ledChannel0 = 0; // for 730nm led channel 
const int ledChannel1 = 1;  // for 850nm led channel 
const int resolution = 8;
int ledChannel = 0;
const int MAX_HERTZ = 255;
const int MIN_HERTZ = 0;

void setup() {
  pinMode(potPin36, INPUT);
  pinMode(potPin35, INPUT);
  pinMode(potPin34, INPUT);
  pinMode(potPin33, INPUT);

  ledcSetup(ledChannel0, freq, resolution);
  ledcSetup(ledChannel1, freq, resolution);
  
  ledcAttachPin(ledPin21, ledChannel0);
  ledcAttachPin(ledPin22, ledChannel1);
  
  Serial.begin(115200);
  /* If no name is given, default 'ESP32' is applied */
  /* If you want to give your own name to ESP32 Bluetooth device, then */
  /* specify the name as an argument SerialBT.begin("myESP32Bluetooth"); */
  SerialBT.begin("myESP32Bluetooth");
  Serial.println("Bluetooth Started! Ready to pair...");
}

void loop() {

  //----------------------------------------------------
  light36 = 0.0;
  light36 += analogRead(potPin36);
  Serial.print("0 ");
  Serial.println(light36);
  SerialBT.println(light36);
  //--------------------------------------------------
  light35 = 0.0;
  light35 += analogRead(potPin35);
  Serial.print("1 ");
  Serial.println(light35);
  SerialBT.println(light35);
//  -------------------------------------------------
  light34 = 0.0;
  light34 += analogRead(potPin34);
  Serial.print("2 ");
  Serial.println(light34);
  SerialBT.println(light34);
//  ------------------------------------------
  light33 = 0.0;
  light33 += analogRead(potPin33);
  Serial.print("3 ");
  Serial.println(light33);
  SerialBT.println(light33);
//  -------------------------------------
    if(ledChannel==0){
      ledcWrite(ledChannel, MAX_HERTZ);
      ledChannel = 1;
      ledcWrite(ledChannel,MIN_HERTZ);
    }
    else if(ledChannel == 1){
      ledcWrite(ledChannel, MAX_HERTZ);
      ledChannel = 0;
      ledcWrite(ledChannel,MIN_HERTZ);
    }
    else {
      exit(0); 
    }
//      ledcWrite(ledChannel, MAX_HERTZ);
  delay(500);
}
