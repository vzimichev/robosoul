#include <Servo.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_ADXL345_U.h>

Adafruit_ADXL345_Unified accel = Adafruit_ADXL345_Unified(12345);

String data;
Servo servo[6];
byte initial[7] = {8,4,0,10,3,7,0};
byte ang[7];
byte last[6];
byte pos[6];

//all the right moves proceed from last[] to ang[]

void setup() 
{
  Serial.begin(19200);
  servo[0].attach(9); //left hip - green
  servo[1].attach(11); //right hip - orange
  servo[2].attach(3);  //left knee - red
  servo[3].attach(10);  //right knee - black
  servo[4].attach(5);  //left foot - grey
  servo[5].attach(6);  //right foot - purple
  
//start position
  for (byte i = 0; i < 6; i++){
    ang[i]=90+initial[i];
    servo[i].write(ang[i]);
    last[i]=ang[i];
    pos[i]=ang[i];
    delay(10);}//for index      

 //accelerometer setup
  if(!accel.begin())
  {
    Serial.println("Ooops, no ADXL345 detected ... Check your wiring!");
    while(1);
  }
  accel.setRange(ADXL345_RANGE_4_G);
  sensors_event_t event; 
  accel.getEvent(&event);
  Serial.print(">"); Serial.print(event.acceleration.x); Serial.print("\t");Serial.print(event.acceleration.y); Serial.print("\t");Serial.println(event.acceleration.z);
}//void setup

void loop()
{
  if (Serial.available()>0)
  {
    if (Serial.find("in"))
    {
      data = Serial.readString();
      for (byte i = 0; i < 7; i++){
        ang[i] = strtol(&data.substring(2*i, 2*i+2)[0],NULL,16)+initial[i];        //getting ang[]
}//for reading

//movement from last[] to ang[]
     while(pos[0] != ang[0] || pos[1] != ang[1] || pos[2] != ang[2] || pos[3] != ang[3] || pos[4] != ang[4] || pos[5] != ang[5]){
      for (byte i = 0; i < 6; i++){
            int c = ((pos[i]-ang[i])/(last[i]-ang[i]));
            if (c == 0) continue;
            if (c > 0){
              if ((0.75 >= c > 0.25) && (c != 0.5)){
                pos[i]-= 2;}//if stop
              else{
                pos[i]-= 1;}
            }//if c > 0
            if (c < 0){
              if ((-0.75 <= c < -0.25) && (c != -0.5)){
                pos[i]+= 2;}//if stop
              else{
                pos[i]+= 1;}
            }//if c < 0
          servo[i].write(pos[i]);
          delay(ang[6]);
 }//for index      
 }//while stop

  sensors_event_t event; 
  accel.getEvent(&event);
  
  Serial.print(">"); Serial.print(event.acceleration.x); Serial.print("\t");Serial.print(event.acceleration.y); Serial.print("\t");Serial.println(event.acceleration.z);

 //Serial.println("end");
 }//if IN
 }//if avaliable
 }//void
