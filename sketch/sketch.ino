#include <Servo.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_ADXL345_U.h>
#include <BMI160Gen.h>

Adafruit_ADXL345_Unified accel = Adafruit_ADXL345_Unified(12345);

String data;
Servo servo[6];
byte initial[7] = {8,4,0,10,3,7,0};
byte ang[7];
byte last[6];
byte pos[6];

float convertRawGyro(int gRaw) {
  // since we are using 250 degrees/seconds range
  // -250 maps to a raw value of -32768
  // +250 maps to a raw value of 32767

  float g = (gRaw * 250.0) / 32768.0;

  return g;
}
//all the right moves proceed from last[] to ang[]

void setup() 
{
  Serial.begin(38400);
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
    pos[i]=last[i];
    delay(10);}//for index      

 //accelerometer setup
  if(!accel.begin())
  {
    Serial.println("Ooops, no ADXL345 detected ... Check your wiring!");
    while(1);
  }
  accel.setRange(ADXL345_RANGE_2_G);
  sensors_event_t event; 
  accel.getEvent(&event);

  BMI160.begin(BMI160GenClass::I2C_MODE);
  uint8_t dev_id = BMI160.getDeviceID();
  BMI160.setGyroRange(250);

  int gxRaw, gyRaw, gzRaw;         // raw gyro values
  float gx, gy, gz;

  // read raw gyro measurements from device
  BMI160.readGyro(gxRaw, gyRaw, gzRaw);

  // convert the raw gyro data to degrees/second
  gx = convertRawGyro(gxRaw);
  gy = convertRawGyro(gyRaw);
  gz = convertRawGyro(gzRaw);
  
  Serial.print(">"); Serial.print(event.acceleration.x); Serial.print("\t");Serial.print(event.acceleration.y); Serial.print("\t");Serial.print(event.acceleration.z);Serial.print("\t");Serial.print(gx); Serial.print("\t");Serial.print(gy); Serial.print("\t");Serial.println(gz);
}//void setup

void loop()
{
  if (Serial.available()>0) {
  if (Serial.find("in")) {
      data = Serial.readString();
      if (data.length() != 15) {
          Serial.println("[WARNING]Inappropriate length.");
          return;
      }
      for (byte i = 0; i<16; i++)  {
          if (static_cast<int>(data[i]) > 103) {
              Serial.println("[WARNING]Inappropriate symbol found.");
              return;
          }
      }
      for (byte i = 0; i < 7; i++) {
          ang[i] = strtol(&data.substring(2*i, 2*i+2)[0],NULL,16)+initial[i];        //getting ang[]
      }//for reading
      for (byte i = 0; i < 7; i++) {
          Serial.print("input[");Serial.print(i);Serial.print("]:\t");Serial.println(ang[i]);
      }
//moving from last[] to ang[]
      while(pos[0] != ang[0] || pos[1] != ang[1] || pos[2] != ang[2] || pos[3] != ang[3] || pos[4] != ang[4] || pos[5] != ang[5]) {
      for (byte i = 0; i<6;i++) {
          if (last[i] == ang[i]) continue;
          if (pos[i] == ang[i]) continue;
          int c = 100*(pos[i]-ang[i])/abs(last[i]-ang[i]);
          if (c > 0) {
            if ((25 < c) && (c < 75) && (c != 50)) pos[i]-=2;
            else pos[i]-=1;
          }
          else{
            if ((-25 > c) && (c > -75) && (c != -50)) pos[i]+=2;
            else pos[i]+=1;
          }
          servo[i].write(pos[i]);
          delay(ang[6]);
      }//for index      
      }//while stop
      
//getting sensor data      
      for (byte i = 0; i < 6; i++) last[i]=pos[i];
      sensors_event_t event; 
      accel.getEvent(&event);
      
      int gxRaw, gyRaw, gzRaw;
      float gx, gy, gz;  
      BMI160.readGyro(gxRaw, gyRaw, gzRaw);
      gx = convertRawGyro(gxRaw);
      gy = convertRawGyro(gyRaw);
      gz = convertRawGyro(gzRaw);
      
      Serial.print(">"); Serial.print(event.acceleration.x); Serial.print("\t");Serial.print(event.acceleration.y); Serial.print("\t");Serial.print(event.acceleration.z);Serial.print("\t");Serial.print(gx); Serial.print("\t");Serial.print(gy); Serial.print("\t");Serial.println(gz);
      }//if IN
}//if available
}//void
