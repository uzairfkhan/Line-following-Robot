const int motor1A = 19;
  const int motor1B = 18;
  const int motor2A = 17;
  const int motor2B = 5;
  const int RightMotor = 100/1.33;
  const int LeftMotor = 200/1.33;
  int IRSensorRight = 16;
  int IRSensorLeft = 2;
  int IRSensorMid = 4;
  int JDleft =21;
  int JDRight =22;
  int lastFunction = 0; 
  int JC = 0;
  int junction_count = 0;
    void setup() {
    pinMode(motor1A, OUTPUT);
    pinMode(motor1B, OUTPUT);
    pinMode(motor2A, OUTPUT);
    pinMode(motor2B, OUTPUT);
    Serial.begin(115200);
  pinMode(IRSensorMid, INPUT); // IR Sensor pin INPUT
  pinMode(IRSensorRight, INPUT); // IR Sensor pin INPUT
  pinMode(IRSensorLeft, INPUT); // IR Sensor pin INPUT
  pinMode(JDleft, INPUT); // IR Sensor pin INPUT
  pinMode(JDRight, INPUT); // IR Sensor pin INPUT

  }

  void moveForward(int speed1,int speed2) {
    analogWrite(motor1A, speed1);
    analogWrite(motor1B, LOW);
    analogWrite(motor2A, LOW);
    analogWrite(motor2B, speed2);
    //Serial.print("Moving Forward ");
    lastFunction = 1;
}
  void sharpRight(int speed1,int speed2) {
    analogWrite(motor1A, LOW);
    analogWrite(motor1B, speed1);
    analogWrite(motor2A, LOW);
    analogWrite(motor2B, speed2);
    lastFunction = 2;
}

  void sharpLeft(int speed1,int speed2) {
    analogWrite(motor1A, speed1);
    analogWrite(motor1B, LOW);
    analogWrite(motor2A, speed2);
    analogWrite(motor2B, LOW);
    lastFunction = 3;
}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.print(digitalRead(7));
      int LeftsensorStatus = digitalRead(IRSensorLeft); // Set the GPIO as Input
    Serial.print("LeftsensorStatus");
    Serial.print(LeftsensorStatus);
  
 int MidsensorStatus = digitalRead(IRSensorMid); // Set the GPIO as Input
    Serial.println("MidsensorStatus");
    Serial.println(MidsensorStatus);

    int RightsensorStatus = digitalRead(IRSensorRight); // Set the GPIO as Input
    Serial.println("RightsensorStatus");
    Serial.println(RightsensorStatus);

int JDL = digitalRead(JDleft); // Set the GPIO as Input
    Serial.println("JDL");
    Serial.println(JDL);
    
    //delay(1000);
int JDR = digitalRead(JDRight); // Set the GPIO as Input
    Serial.println("JDR");
    Serial.println(JDR);
//     if(!JDL && JDR){
//       moveForward(0,0);
//       delay(300);
//       sharpRight(RightMotor,LeftMotor);
//       delay(1000);
//       moveForward(RightMotor,LeftMotor);
//       delay(550);
//       turn1 = 1;
//       //JC++;
//     }
//     if(JDL && JDR){
//       moveForward(0,0);
//       delay(300);
//       sharpRight(RightMotor,LeftMotor);
//       delay(1000);
//       moveForward(RightMotor,LeftMotor);
//       delay(550);
//       //JC++;
//     }
//     if(JDL && !JDR && turn1 == 1){
//       moveForward(0,0);
//       delay(300);
//       sharpLeft(RightMotor,LeftMotor);
//       delay(1000);
//       moveForward(RightMotor,LeftMotor);
//       delay(550);
//     }
 if(!JDL && JDR )
 {
   moveForward(0,0);
   delay(300);
   do
   {
      sharpRight(RightMotor,LeftMotor); 
   }
   while(!digitalRead(IRSensorRight));
   moveForward(0,0);
   delay(200); 
   moveForward(RightMotor,LeftMotor);
   junction_count++;  
 }

if(JDL && !JDR && junction_count >= 2)
 {
   moveForward(0,0);
   delay(300);
   do
   {
      sharpLeft(RightMotor,LeftMotor); 
   }
   while(!digitalRead(IRSensorLeft));
   moveForward(0,0);
   delay(200); 
   moveForward(RightMotor,LeftMotor);  
 }
/*else if(JDL && !JDR)
 {
   moveForward(0,0);
   delay(300); 
   JDL = 0;
   do
   {
      sharpRight(RightMotor,LeftMotor);
      int LeftsensorStatus = digitalRead(IRSensorLeft); // Set the GPIO as Input
   }
   while(LeftsensorStatus == 0);
   moveForward(0,0);
   delay(200); 
   moveForward(RightMotor,LeftMotor);
   JDL = digitalRead(JDleft);
   JDR = digitalRead(JDRight);
   LeftsensorStatus = digitalRead(IRSensorLeft);
   MidsensorStatus = digitalRead(IRSensorMid);
   RightsensorStatus = digitalRead(IRSensorRight);
 }
else if(JDL && JDR)
 {
   moveForward(0,0);
   delay(300);
   moveForward(0,LeftMotor);
   delay(200);
   JDR = 0;
   do
   {
      sharpLeft(RightMotor,LeftMotor);
      int RightsensorStatus = digitalRead(IRSensorRight); // Set the GPIO as Input
   }
   while(RightsensorStatus == 0);
   moveForward(0,0);
   delay(200); 
   moveForward(RightMotor,LeftMotor);
   JDL = digitalRead(JDleft);
   JDR = digitalRead(JDRight);
   LeftsensorStatus = digitalRead(IRSensorLeft);
   MidsensorStatus = digitalRead(IRSensorMid);
   RightsensorStatus = digitalRead(IRSensorRight);
 }*/
if(!LeftsensorStatus && !RightsensorStatus && !MidsensorStatus)
{
   moveForward(RightMotor,LeftMotor);
}
else if(!LeftsensorStatus && !MidsensorStatus && RightsensorStatus)
{
   moveForward(RightMotor*0,LeftMotor);
}
else if(!LeftsensorStatus && MidsensorStatus && !RightsensorStatus)
{
   moveForward(RightMotor,LeftMotor);
}
else if(!LeftsensorStatus && MidsensorStatus && RightsensorStatus)
{
   moveForward(RightMotor/2,LeftMotor);
}
else if(LeftsensorStatus && !MidsensorStatus && !RightsensorStatus)
{
   moveForward(RightMotor,LeftMotor*0);
}
else if(LeftsensorStatus && !MidsensorStatus && RightsensorStatus)
{
   moveForward(RightMotor,LeftMotor);
}
else if(LeftsensorStatus && MidsensorStatus && !RightsensorStatus)
{
   moveForward(RightMotor,LeftMotor/2);
}
else if(LeftsensorStatus && MidsensorStatus && RightsensorStatus)
{
   moveForward(RightMotor,LeftMotor);
}

}