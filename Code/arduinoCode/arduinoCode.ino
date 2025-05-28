#include <Servo.h>
#define numOfValsRec 5
#define digitsPerValRec 1

Servo servoThumb;
Servo servoIndex;
Servo servoMiddle;
Servo servoRing;
Servo servoPinky;


int valsRec [numOfValsRec];
int stringLength = numOfValsRec * digitsPerValRec + 1; //$00000
int counter = 0;
bool counterStart = false;
String receivedString;
void setup() {
  Serial.begin(9600);
   servoThumb.attach(11);
   servoIndex.attach(10);
   servoMiddle.attach(9);
   servoRing.attach(6);
   servoPinky.attach(5);

}



void receieveData () { 
  while (Serial.available())
  { 
    
    char c = Serial.read();
    if (c=='$') { 
      counterStart = true;
    }
    if (counterStart) {
      if (counterStart < stringLength) {
         receivedString = String (receivedString + c);
         counter ++;
      }
      if (counter >= stringLength) {
        for (int i = 0; i< numOfValsRec; i++) {

         int num = (i * digitsPerValRec) + 1;
          valsRec [i] = receivedString.substring(num,num + digitsPerValRec).toInt();
        }
        receivedString = "";
        counter = 0;
        counterStart = false;
      }
    }

  }
}


void loop() {
  receieveData();
  if(valsRec[0] == 1) {servoThumb.write(135);}else{servoThumb.write(40);}
  if(valsRec[1] == 1) {servoIndex.write(135);}else{servoIndex.write(45);}
  if(valsRec[2] == 1) {servoMiddle.write(135);}else{servoMiddle.write(40);}
  if(valsRec[3] == 1) {servoRing.write(135);}else{servoRing.write(40);}
  if(valsRec[4] == 1) {servoPinky.write(135);}else{servoPinky.write(40);}

  

}
