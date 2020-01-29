import time,serial,argparse
import numpy as np
from RoboPy import output,fall_check,upscale_executor_matrix,normalize_sensor_data

def servoin(a=90,b=90,c=90,d=90,e=90,f=90,delay=3):
    '''waits end of previous act. and send angles to arduino returns acc-array     
    '''
    while ser.read()!=b'>':pass
    acc = [float(e) for e in ser.readline().split(b'\t')]
    output('accelerometer: '+str(acc)+'\n')
    if fall_check(*acc)==False:
        data='in'
        for i in a,b,c,d,e,f,delay:
            try: 
                data+=str(hex(i))[2]+str(hex(i))[3]
            except IndexError:
                data+='0'+str(hex(i))[2]
        ser.write(data.encode())
        output('servo in: '+str([a,b,c,d,e,f,delay])+'\n')
    else:
         1/0
    return acc
    
def serial_begin(port):
    ser = serial.Serial(port, 19200, bytesize=8, parity='N', stopbits=1, timeout=2)
    time.sleep(2)
    output(time.ctime()+'\nconnected to: '+ ser.portstr,'highlight')
    ser.write('in5a5a5a5a5a5a03'.encode())
    return ser,np.array([[90,90,90,90,90,90]])

def executor(ser,prt,mtrx):
    k = 0
    acc = []
    try:#fall detection script            
        while k == 0:
            for i in mtrx: 
                acc.append(servoin(*i))
                k += 1
    except ZeroDivisionError:
        output('I have fallen.\n','error')
        output('Steps to fall:'+str(stf)+'\n','highlight')
        if len(acc) != 0: 
            sensor_data = normalize_sensor_data(np.array(acc))
            np.savetxt('sensor.csv',sensor_data,fmt='%.4f',delimiter=',')
            output('[Upd]sensor.csv\nSensor data recieved.\n')   
        else: output('No sensor data recieved.\n','warning') 
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
    start_time = time.time()
    parser = argparse.ArgumentParser(description='String')
    parser.add_argument('--prefix','-p', type = str, help='Input prefix',default='')
    args = parser.parse_args()
    prefix = args.prefix
    output('Launch python3 executor.py --prefix '+prefix,'start')
    if prefix != '': prefix = prefix + '_'    
    
    port = '/dev/ttyACM0'
    ser,matrix = serial_begin(port)
    matrix = np.loadtxt('matrix.csv', 'float', delimiter = ',')
    restrictions = np.loadtxt('restrictions.txt', 'int', delimiter = '\t')       
    matrix = upscale_executor_matrix(matrix,restrictions)
    
    ser,stf,sensor_data = executor(ser,port,matrix.astype(int))
    
    ser.close()
    output('Session of executor.py ended in ','time',time.time()-start_time)  
