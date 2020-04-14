from utils import *
import serial

def listen(ser):
    while ser.read()!=b'>':pass
    acc = [float(e) for e in ser.readline().split(b'\t')]
    output('accelerometer: '+str(acc))
    return acc

def servoin(ser,a=90,b=90,c=90,d=90,e=90,f=90,delay=3):
    data='in'
    for i in a,b,c,d,e,f,delay:
        try: 
            data+=str(hex(i))[2]+str(hex(i))[3]
        except IndexError:
            data+='0'+str(hex(i))[2]
    ser.write(data.encode())
    output('servo in: '+str([a,b,c,d,e,f,delay]))       
    
def serial_begin(port):
    ser = serial.Serial(port, 19200, bytesize=8, parity='N', stopbits=1, timeout=2)
    time.sleep(2)
    output(time.ctime()+'\nconnected to: '+ ser.portstr,'highlight')
    return ser

def bad_loop(data):
    while True:
        try:
            np.savetxt('sensor.csv',data,fmt='%.4f',delimiter=',')
            break
        except PermissionError:
            output('Ready to override sensor data. Waiting for permission...')
            time.sleep(1)
    output('[Upd]sensor.csv')
    output('Sensor data recieved.') 

def executor(ser,mtrx):
    while True: #am I standing?
        servoin(ser) 
        sensor = listen(ser)
        if ready(*sensor): break
        print('Master, lift me up, please...')
        time.sleep(1)
    k = 0 #ready to go!
    acc = []
    for i in mtrx: 
        servoin(ser,*i)
        sensor = listen(ser)
        acc.append(sensor)
        k += 1
        if not ready(*sensor): #finita la comedia
            output('I have fallen.','error')
            servoin(ser) 
            if len(acc) != 0: 
                sensor_data = normalize_sensor_data(np.array(acc))
                bad_loop(sensor_data)
            else: output('No sensor data recieved.','warning') 
            output('Steps to fall:'+str(k),'highlight')
            return k,False
    output('All matrix have been executed.')
    sensor_data = normalize_sensor_data(np.array(acc))
    bad_loop(sensor_data)
    output('Steps to fall:'+str(k),'highlight')
    return k,True
 
if __name__ == "__main__":
    start_time = time.time()
    parser = argparse.ArgumentParser(description='String')
    parser.add_argument('--prefix','-p', type = str, help='Input prefix of net. [default = ""]', default='')
    parser.add_argument('--online','-o', type = str2bool, help='Enable on-line learning. [default = False]', default=False)
    args = parser.parse_args()
    prefix = args.prefix
    online = args.online
    output('Launch python3 executor.py --prefix '+prefix+' --online '+str(online),'start')
    if prefix != '': prefix = prefix + '_'    
    
    port = '/dev/ttyS0'
    ser = serial_begin(port)
    matrix = np.loadtxt('matrix.csv', 'float', delimiter = ',')
    restrictions = np.loadtxt('restrictions.txt', 'int', delimiter = '\t')       
    matrix = upscale_executor_matrix(matrix,restrictions)
    
    if not online: stf = executor(ser,matrix.astype(int))[0]
    
    ser.close()
    filename = 'executor_report.xls'
    with open(filename, 'a') as myfile: myfile.write(str(stf)+'\n')
    output('[Upd]'+filename)
    output('Steps to fall recorded.')   
    output('Session of executor.py ended in ','time',time.time()-start_time)  
