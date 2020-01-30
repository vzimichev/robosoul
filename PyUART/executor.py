import time,serial,argparse
import numpy as np
from RoboPy import output,ready,upscale_executor_matrix,normalize_sensor_data

def listen(ser):
    while ser.read()!=b'>':pass
    acc = [float(e) for e in ser.readline().split(b'\t')]
    output('accelerometer: '+str(acc)+'\n')
    return acc

def servoin(ser,a=90,b=90,c=90,d=90,e=90,f=90,delay=3):
    data='in'
    for i in a,b,c,d,e,f,delay:
        try: 
            data+=str(hex(i))[2]+str(hex(i))[3]
        except IndexError:
            data+='0'+str(hex(i))[2]
    ser.write(data.encode())
    output('servo in: '+str([a,b,c,d,e,f,delay])+'\n')       
    
def serial_begin(port):
    ser = serial.Serial(port, 19200, bytesize=8, parity='N', stopbits=1, timeout=2)
    time.sleep(2)
    output(time.ctime()+'\nconnected to: '+ ser.portstr,'highlight')
    return ser

def executor(ser,mtrx):
    while True: #am I standing?
        servoin(ser) 
        sensor = listen(ser)
        if ready(*sensor): break
    k = 0 #ready to go!
    acc = []
    for i in mtrx: 
        servoin(ser,*i)
        sensor = listen(ser)
        acc.append(sensor)
        k += 1
        if not ready(*sensor): #finita la comedia
            output('I have fallen.\n','error')
            if len(acc) != 0: 
                sensor_data = normalize_sensor_data(np.array(acc))
                np.savetxt('sensor.csv',sensor_data,fmt='%.4f',delimiter=',')
                output('[Upd]sensor.csv\nSensor data recieved.\n')   
            else: output('No sensor data recieved.\n','warning') 
            output('Steps to fall:'+str(k)+'\n','highlight')
            return False
    output('All matrix have been executed.\n')
    if len(acc) != 0: 
        sensor_data = normalize_sensor_data(np.array(acc))
        np.savetxt('sensor.csv',sensor_data,fmt='%.4f',delimiter=',')
        output('[Upd]sensor.csv\nSensor data recieved.\n')   
    else: output('No sensor data recieved.\n','warning') 
    output('Steps to fall:'+str(k)+'\n','highlight')
    return True
 
if __name__ == "__main__":
    start_time = time.time()
    parser = argparse.ArgumentParser(description='String')
    parser.add_argument('--prefix','-p', type = str, help='Input prefix',default='')
    args = parser.parse_args()
    prefix = args.prefix
    output('Launch python3 executor.py --prefix '+prefix,'start')
    if prefix != '': prefix = prefix + '_'    
    
    port = '/dev/ttyACM0'
    ser = serial_begin(port)
    matrix = np.loadtxt('matrix.csv', 'float', delimiter = ',')
    restrictions = np.loadtxt('restrictions.txt', 'int', delimiter = '\t')       
    matrix = upscale_executor_matrix(matrix,restrictions)
    
    if executor(ser,matrix.astype(int)) == False:
        while True: #am I standing?
            servoin(ser) 
            sensor = listen(ser)
            if ready(*sensor): break
            print('Master, lift me up, please...')
            time.sleep(1)
    
    ser.close()
    output('Session of executor.py ended in ','time',time.time()-start_time)  
