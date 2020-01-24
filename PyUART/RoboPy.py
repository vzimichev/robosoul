import argparse
import json
import numpy as np
from colorama import Fore, Style

def sigmoid(a):
    return 1.0/(1.0+np.exp(a))

def line(mtrx):
    return mtrx.reshape(1,mtrx.shape[0] * mtrx.shape[1])

def backpropagation(netinfo): 
    result = np.loadtxt(netinfo['result'], 'float', delimiter=',')
    supervisor = np.loadtxt(netinfo['supervisor'], 'float', delimiter=',')
    #layer shift -1
    netinfo['layer names'].insert(0,netinfo['expanded source'])  
    x = [y for y in netinfo['gap'] if y[1]<=min(supervisor.shape[0],result.shape[0])]
    if len(x) == 0: x = [[0,min(supervisor.shape[0],result.shape[0]),0,min(supervisor.shape[0],result.shape[0])]]
    flag = True
    for gap in x:
        #output layer 
        #error
        delta = (result[gap[0]:gap[1]] - supervisor[gap[0]:gap[1]]) * result[gap[0]:gap[1]] * (1 - result[gap[0]:gap[1]])
        full_weight = np.loadtxt(netinfo['weight names'][-1], 'float', delimiter=',')
        weight = full_weight[:(gap[1]-gap[0])*int(netinfo['strategy'][-2]),:(gap[1]-gap[0])*int(netinfo['strategy'][-1])]
        full_bias = np.loadtxt(netinfo['bias names'][-1], 'float', delimiter=',')
        bias = full_bias[:gap[1]-gap[0]]
        full_temperature = np.loadtxt(netinfo['temp names'][-1], 'int', delimiter='|')
        temperature = full_temperature[:(gap[1]-gap[0])*int(netinfo['strategy'][-2]),:(gap[1]-gap[0])*int(netinfo['strategy'][-1])]
        layer = np.loadtxt(netinfo['layer names'][-2], 'float', delimiter=',')[gap[2]:gap[3]]
        
        #backpropagation of output layer
        weight = weight - netinfo['learning rate'] * line(layer).T.dot(line(delta)) - netinfo['hyper'] * weight - netinfo['cool'] * weight * temperature   
        bias = bias - netinfo['learning rate'] * delta
        weight = zero_filter(weight,netinfo['foresight'])
        full_weight[:(gap[1]-gap[0])*int(netinfo['strategy'][-2]),:(gap[1]-gap[0])*int(netinfo['strategy'][-1])] = weight
        np.savetxt(netinfo['weight names'][-1],full_weight,fmt='%.4f',delimiter=',')
        full_bias[:gap[1]-gap[0]] = bias
        np.savetxt(netinfo['bias names'][-1],full_bias,fmt='%.4f',delimiter=',')  
        if flag: output('[Upd]' + netinfo['weight names'][-1] + '\n[Upd]' + netinfo['bias names'][-1])
        #target function    
        J = np.sum((supervisor[gap[0]:gap[1]]-result[gap[0]:gap[1]])**2) + netinfo['hyper']*np.sum(full_weight**2) + netinfo['cool']*np.sum((full_temperature*full_weight)**2)

        #backpropagation of hidden layers 
        for j in range(netinfo['layers'] - 2, -1, -1):
            delta = (line(delta).dot(weight.T)) * line(layer) * (1 - line(layer))
            
            full_weight = np.loadtxt(netinfo['weight names'][j], 'float', delimiter=',')
            weight = full_weight[:(gap[1]-gap[0])*int(netinfo['strategy'][j]),:(gap[1]-gap[0])*int(netinfo['strategy'][j+1])]
            full_bias = np.loadtxt(netinfo['bias names'][j], 'float', delimiter=',')
            bias = full_bias[:gap[1]-gap[0]]
            full_temperature = np.loadtxt(netinfo['temp names'][j], 'int', delimiter='|')
            temperature = full_temperature[:(gap[1]-gap[0])*int(netinfo['strategy'][j]),:(gap[1]-gap[0])*int(netinfo['strategy'][j+1])]
            full_layer = np.loadtxt(netinfo['layer names'][j], 'float', delimiter=',')
            layer = full_layer[gap[2]:gap[3]]
            
            weight = weight - netinfo['learning rate'] * line(layer).T.dot(line(delta)) - netinfo['hyper'] * weight - netinfo['cool'] * weight * temperature
            bias = bias - netinfo['learning rate'] * delta.reshape(bias.shape) 
            weight = zero_filter(weight,netinfo['foresight'])
            
            
            full_weight[:(gap[1]-gap[0])*int(netinfo['strategy'][j]),:(gap[1]-gap[0])*int(netinfo['strategy'][j+1])] = weight
            np.savetxt(netinfo['weight names'][j],full_weight,fmt='%.4f',delimiter=',')
            full_bias[:gap[1]-gap[0]] = bias
            np.savetxt(netinfo['bias names'][j],full_bias,fmt='%.4f',delimiter=',')  
            if flag: output('[Upd]' + netinfo['weight names'][j] + '\n[Upd]' + netinfo['bias names'][j])
                          
            J += netinfo['hyper']*np.sum(full_weight**2) + netinfo['cool']*np.sum((full_temperature*full_weight)**2)
        flag = False
    with open(netinfo['report'], 'a') as myfile: myfile.write(str(J)+'\n')
    output('Updated matrixes of prediction according to backpropagation.\n[Upd]'+netinfo['report']+'\nTarget function of '+netinfo['target']+' net: '+str(J))  
    
        
def zero_filter(mtrx,n):
    a = mtrx.shape[0] // n
    b = mtrx.shape[1] // n
    for i in range(n-1):
        for j in range(i+1,n):
            for k in range(a):
                for l in range(b):
                    mtrx[a*i+k][b*j+l] = 0  
    return mtrx

def correct(a,s):
    'gets real measurements & returns a which not fallen'
    a = a[:(a.shape[0]-1)]
    newrow = [0.25, 0.5, 0.5, 0.45, 0.5 ,0.5]
    for j in range(s-a.shape[0]):
        a = np.vstack([a,newrow])
    return a

def fall_check(accelx,accely,accelz,gx,gy,gz):
    '''gets measurement of accelerometer
        checks if Robo has fallen
        returns FALSE if Robo - NOT fallen
        returns TRUE if Robo - has fallen'''
    if (abs(accely)>5 or abs(accelz)>5) and abs(accelx)<7: return True
    else: return False

def predict_stf(prdctn):
    for i in range(len(prdctn)):
        if fall_check(*prdctn[i]): break 
    return i + 1

def upscale_sensor_data(mtrx):
    mtrx[:,:3] = mtrx[:,:3] * 40.0 - 20.0
    mtrx[:,3:] = mtrx[:,3:] * 500.0 - 250.0
    return mtrx

def normalize_sensor_data(mtrx):
    mtrx[:,:3] = (mtrx[:,:3] + 20.0) / 40.0 
    mtrx[:,3:] = (mtrx[:,3:] + 250.0) / 500.0
    return mtrx

def normalize_executor_matrix(mtrx,r):
    for i in range(6):
        mtrx[:,i] =  (mtrx[:,i] - r[i,0]) / (r[i,1] - r[i,0])
    return mtrx

def upscale_executor_matrix(mtrx,r):
    for i in range(6):
        mtrx[:,i] = np.round(mtrx[:,i] * (r[i,1] - r[i,0]) / r[i,2]) * r[i,2] + r[i,0]
    return mtrx
        
def forward_pass(mtrx,w,b):
     return sigmoid(line(mtrx).dot(w)+line(b)).reshape(b.shape)
    
def output(s, color = None):
    if color == 'error':
        print(Fore.RED + '{}'.format(s))
        print(Style.RESET_ALL)
    if color == 'warning':
        print(Fore.YELLOW + '{}'.format(s))
        print(Style.RESET_ALL)
    if color == 'highlight':
        print(Fore.GREEN + '{}'.format(s))
        print(Style.RESET_ALL) 
    if color == 'start':
        print(Fore.CYAN + '{}'.format(s))
        print(Style.RESET_ALL)
    if color == None:
        print(s)
    with open('historia.log', 'a') as myfile:
            myfile.write(s)
            
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='String')
    parser.add_argument('--prefix','-p', type = str, help='Input prefix',default='')
    parser.add_argument('--learning','-l', type = float, help='Learning rate of backpropagation',default=0.1)
    parser.add_argument('--hyper','-hp', type = float, help='L2 normalization parameter',default=0.1)
    parser.add_argument('--cool','-c', type = float, help='Cool parameter of non-Markov process',default=0.2)
    args = parser.parse_args()
    prefix = args.prefix
    learning = args.learning
    hyper = args.hyper
    cool = args.cool

    output('Launch python3 RoboPy.py --learning '+str(learning)+' --hyper '+str(hyper)+' --cool '+str(cool)+' --prefix '+prefix,'start')    
    if prefix != '': prefix = prefix + '_'
    
    with open("config.json", "r") as config_file: CONFIG = json.load(config_file)
    for i in CONFIG: 
        if i['prefix'] == prefix + 'net':      
            with open("config.json", "w") as config_file:
                i.update({'learning rate':learning,'hyper':hyper,'cool':cool})   
                json.dump(CONFIG,config_file,indent=4)
    
    with open("config.json", "r") as config_file: CONFIG = json.load(config_file)
    for i in CONFIG: 
        if i['prefix'] == prefix + 'net': backpropagation(netinfo=i)