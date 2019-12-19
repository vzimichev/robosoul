import time,serial
import numpy as np
from RoboPy import output,fall_check

def servoin(a=90,b=90,c=90,d=90,e=90,f=90,delay=3):
    '''waits end of previous act. and send angles to arduino returns acc-array     
    '''
    while ser.read()!=b'>':pass
    acc = [float(e) for e in ser.readline().split(b'\t')]
    print(acc)
    with open('historia.log', 'a') as myfile:
            myfile.write('Accelerometer:'+str(acc)+'\n')
    if fall_check(*acc)==False:
        data='in'
        for i in a,b,c,d,e,f,delay:
            try: 
                data+=str(hex(i))[2]+str(hex(i))[3]
            except IndexError:
                data+='0'+str(hex(i))[2]
        ser.write(data.encode())
        print('servo in: ',a,b,c,d,e,f,delay)
        with open('historia.log', 'a') as myfile:
            myfile.write('Servo in:'+str([a,b,c,d,e,f,delay])+'\n')
    else:
         1/0
    return acc
    
def serial_begin(port):
    ser = serial.Serial(port, 19200, bytesize=8, parity='N', stopbits=1, timeout=2)
    time.sleep(2)
    output(time.ctime()+'\nconnected to: '+ ser.portstr)
    ser.write('in5a5a5a5a5a5a03'.encode())
    return ser,np.array([[90,90,90,90,90,90]])

def executor(ser,prt,mtrx):
    k = 0
    acc = []
    try:#fall detection script            
        for i in mtrx: 
            acc.append(servoin(*i))
            k += 1
    except ZeroDivisionError:
        output('I have fallen.\n')
        stand_up([90,90,90,90,90,90])
    return ser,k,acc

def stand_up(old):
    """TRUE when ready"""
    try:
        data='in'
        for i in old:
            try: 
                data+=str(hex(i))[2]+str(hex(i))[3]
            except IndexError:
                data+='0'+str(hex(i))[2]
        data+='03'
        ser.write(data.encode())
        servoin(*old)
    except ZeroDivisionError:
        print('Master, lift me up, please...')
        stand_up(old)

if __name__ == "__main__":
    port = '/dev/ttyACM0'
    ser,matrix = serial_begin(port)
    matrix = np.loadtxt('matrix.csv', 'int', delimiter = ',')
    
    ser,stf,sensor_data = executor(ser,port,matrix)
    
    output('Steps to fall:'+str(stf)+'\n')
    np.savetxt('sensor.csv',sensor_data,fmt='%.2f',delimiter=',')
    output('[Upd]sensor.csv\nSensor data recieved.\n')    
    ser.close()          

