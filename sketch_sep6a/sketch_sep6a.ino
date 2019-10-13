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
     while(last[0] != ang[0] || last[1] != ang[1] || last[2] != ang[2] || last[3] != ang[3] || last[4] != ang[4] || last[5] != ang[5]){
      for (byte i = 0; i<6;i++){
          byte pos = last[i];
          if (pos!=ang[i]){
            pos-=((pos-ang[i])/abs(pos-ang[i]));
            servo[i].write(pos);
            last[i]=pos;
            delay(ang[6]);}//if stop
 }//for index      
 }//while stop
  sensors_event_t event; 
  accel.getEvent(&event);
  
  Serial.print(">"); Serial.print(event.acceleration.x); Serial.print("\t");Serial.print(event.acceleration.y); Serial.print("\t");Serial.println(event.acceleration.z);

 //Serial.println("end");
 }//if IN
 }//if avaliable
 }//void
