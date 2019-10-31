import time,serial,random
import numpy as np

def servoin(a=90,b=90,c=90,d=90,e=90,f=90,delay=1):
    '''waits end of previous act. and send angles to arduino returns acc-array     
    '''
    while ser.read()!=b'>':pass
    acc = [float(e) for e in ser.readline().split(b'\t')]
    print(acc)
    with open("historia.log", "a") as myfile:
            myfile.write('Accelerometer:'+str(acc)+'\n')
    if fall_check(*acc)==False:
        data='in'
        for i in a,b,c,d,e,f,delay:
            try: 
                data+=str(hex(i))[2]+str(hex(i))[3]
            except IndexError:
                data+='0'+str(hex(i))[2]
        ser.write(data.encode())
        print("servo in: ",a,b,c,d,e,f,delay)
        with open("historia.log", "a") as myfile:
            myfile.write('Servo in:'+str([a,b,c,d,e,f,delay])+'\n')
    else:
         1/0
    return acc
    
def fall_check(accelx,accely,accelz):
    '''gets measurement of accelerometer
        checks if Robo has fallen
        returns FALSE if Robo - NOT fallen
        returns TRUE if Robo - has fallen'''
    if (abs(accelx)<5 or abs(accelz-2)<5) and accely>7:return False
    else: return True
    
      
def serial_begin(port):
    ser = serial.Serial(port, 19200, bytesize=8, parity='N', stopbits=1, timeout=2)
    time.sleep(2)
    print("connected to: "+ ser.portstr)
    with open("historia.log", "a") as myfile:
            myfile.write('connected to:'+str(ser.portstr))
    return ser,np.array([[90,90,90,90,90,90,1]])

def executor(ser,prt,mtrx):
    k = 1
    try:#fall detection script            
        for i in mtrx: 
            servoin(*i)
            k += 1
    except ZeroDivisionError:
        print('I have fallen.')
        with open("historia.log", "a") as myfile:
            myfile.write('I have fallen')
        stand_up([90,90,90,90,90,90,1])
    return ser,k

def stand_up(old):
    """TRUE when ready"""
    try:
        data='in'
        for i in old:
            try: 
                data+=str(hex(i))[2]+str(hex(i))[3]
            except IndexError:
                data+='0'+str(hex(i))[2]
        ser.write(data.encode())
        servoin(*old)
        print('Back in service.')
        with open("historia.log", "a") as myfile:
            myfile.write('Back in service')
    except ZeroDivisionError:
        print('Master, lift me up, please...')
        stand_up(old)
        

def smart_sum(a,b):
    '''returns a sum of matrixes not crossed a borders'''
    borders=[[10,170],[10,170],[10,170],[10,170],[10,170],[10,170],[0,30]]
    c = np.array(a)
    for i in range(len(a)):
        for j in range(len(a[0])):
            if borders[j][1]>a[i][j]+b[i][j]>borders[j][0]:
                c[i][j] = a[i][j]+b[i][j]
    return c
    
if __name__ == "__main__":
    port = 'COM9'
    ser,matrix = serial_begin(port)
    matrix = np.loadtxt('matrix.txt', 'int')
    ser,stf = executor(ser,port,matrix)
    best = stf
    while True:
        matrix = np.loadtxt('matrix.txt', 'int')
        random_matrix = np.random.randint(-1,2,size=(matrix.shape))
        tmp = smart_sum(matrix, random_matrix)
        ser,stf = executor(ser,port,tmp)
        with open("historia.log", "a") as myfile:
            myfile.write(str(tmp)+'\nSteps to fall:'+str(stf)+'\tBest for now:'+str(best)+'\n')
        if stf>best:
            np.savetxt('matrix.txt',tmp,fmt='%s',delimiter='\t')
            best = stf 
            print('Found a better way.')
        stand_up([90,90,90,90,90,90,1])