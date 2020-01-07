import numpy as np
import json
import argparse
from RoboPy import output,zero_filter

def temp_mask(mtrx,n):
    a = mtrx.shape[0] // n
    b = mtrx.shape[1] // n
    for i in range(n):
        for j in range(0,i):
            for k in range(a):
                for l in range(b):
                    mtrx[a*i+k][b*j+l] = i-j  
    return mtrx


if __name__ == "__main__":
    output('weight_matrix_creator.py launch','start')
    matrix = np.loadtxt('matrix.csv', 'int', delimiter=',')
    
    parser = argparse.ArgumentParser(description='String')
    parser.add_argument('--foresight','-f', type = int, help='Input prefix',default=matrix.shape[0])
    parser.add_argument('--prefix','-p', type = str, help='Input prefix',default='')
    parser.add_argument('--target','-t', type = str, help='Input prefix',default='prediction')
    parser.add_argument('--strategy','-s', type = str, help='Strategy of layers', default='666')
    args = parser.parse_args()
    leng = args.foresight
    prefix = args.prefix
    strategy = args.strategy
    target = args.target
       
    if prefix != '': prefix = prefix + '_'
    
    weights,biases,temperatures = [],[],[]
    
    for j in range(len(strategy)-1):
        a,b = int(strategy[j]),int(strategy[j+1])
        weight = np.random.randint(-50,50,size=(leng*a,leng*b)) / 50
        weight = zero_filter(weight,leng)
        w_name = prefix+'weight_'+str(j+1)+'.csv'
        np.savetxt(w_name,weight,fmt='%.4f',delimiter=',')
        output('[Upd]' + w_name + '\nCreated weight matrix.\n')
            
        bias = np.zeros(shape=(leng,b))
        b_name = prefix+'bias_'+str(j+1)+'.csv'
        np.savetxt(b_name,bias,fmt='%.4f',delimiter=',')
        output('[Upd]' + b_name + '\nCreated zero matrix of bias.\n')
                      
        temperature = np.zeros(shape=(leng*a,leng*b)) 
        temperature = temp_mask(temperature,leng)
        t_name = prefix+'temperature_'+str(j+1)+'.txt'
        np.savetxt(t_name,temperature,fmt='%d',delimiter='|')
        output('[Upd]' + t_name + '\nCreated temperature mask.\n')
        
        weights.append(w_name)
        biases.append(b_name)
        temperatures.append(t_name)

    with open("config.json", "r") as config_file: CONFIG = json.load(config_file)
    with open("config.json", "w") as config_file:
        CONFIG.append({'prefix':prefix+'net','target':target,'strategy':strategy,'foresight':leng,'layers':len(strategy)-1,'weight names':weights,'bias names':biases,'temp names':temperatures})
        if target=='prediction': CONFIG[-1].update({'source':'matrix.csv','result':prefix+'prediction.csv','supervisor':prefix+'sensor.csv'})
        if target=='reverse': CONFIG[-1].update({'source':'sensor.csv','result':prefix+'matrix.csv','supervisor':'matrix.csv'})        
        json.dump(CONFIG,config_file,indent=4) 

    output('[Upd]config.json\nAdded new configurations.\n')
