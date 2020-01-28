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
    matrix = np.loadtxt('matrix.csv', 'int', delimiter=',')
    parser = argparse.ArgumentParser(description='String')
    parser.add_argument('--foresight','-f', type = int, help='Foresight is the value of steps can be processed by one pass of net. [default = len(matrix)] ',default=matrix.shape[0])
    parser.add_argument('--prefix','-p', type = str, help='Input prefix of net. [default = ""]',default='')
    parser.add_argument('--target','-t', type = str, help='Choosing target you define combination of {source,prediction,supervisor}. Available:prediction,reverse. [default = prediction]',default='prediction')
    parser.add_argument('--strategy','-s', type = str, help='Architecture of layers. [default = 666]', default='666')
    args = parser.parse_args()
    leng = args.foresight
    prefix = args.prefix
    strategy = args.strategy
    target = args.target
    output('Launch python3 weight_matrix_creator.py  --foresight '+str(leng)+' --target '+target+' --strategy '+strategy+' --prefix '+prefix,'start')
       
    if prefix != '': prefix = prefix + '_'
    
    weights,biases,temperatures = [],[],[]
    
    for j in range(len(strategy)-1):
        a,b = int(strategy[j],36),int(strategy[j+1],36)
        weight = np.random.randint(-50,50,size=(leng*a,leng*b)) / 50
        weight = zero_filter(weight,leng)
        w_name = prefix+'weight_'+str(j+1)+'.csv'
        np.savetxt(w_name,weight,fmt='%.4f',delimiter=',')
        output('[Upd]' + w_name + '\nCreated random weight matrix with shape: ['+str(leng*a)+'x'+str(leng*b)+'].\n')
            
        bias = np.zeros(shape=(leng,b))
        b_name = prefix+'bias_'+str(j+1)+'.csv'
        np.savetxt(b_name,bias,fmt='%.4f',delimiter=',')
        output('[Upd]' + b_name + '\nCreated zero matrix of bias with shape: ['+str(leng)+'x'+str(b)+'].\n')
                      
        temperature = np.zeros(shape=(leng*a,leng*b)) 
        temperature = temp_mask(temperature,leng)
        t_name = prefix+'temperature_'+str(j+1)+'.txt'
        np.savetxt(t_name,temperature,fmt='%d',delimiter='|')
        output('[Upd]' + t_name + '\nCreated temperature mask with shape: ['+str(leng*a)+'x'+str(leng*b)+'].\n')
        
        weights.append(w_name)
        biases.append(b_name)
        temperatures.append(t_name)

    with open("config.json", "r") as config_file: CONFIG = json.load(config_file)
    for tmp in CONFIG: 
        if prefix+'net' == tmp['prefix']: output('WARNING: identical prefix detected\n','warning')
    with open("config.json", "w") as config_file:
        CONFIG.append({'prefix':prefix+'net','target':target,'strategy':strategy,'foresight':leng,'layers':len(strategy)-1,'report':prefix+'report.xls','weight names':weights,'bias names':biases,'temp names':temperatures})
        if target=='prediction': CONFIG[-1].update({'source':'matrix.csv','result':prefix+'prediction.csv','supervisor':'sensor.csv'})
        if target=='reverse': CONFIG[-1].update({'source':'sensor.csv','result':prefix+'matrix.csv','supervisor':'matrix.csv'})        
        json.dump(CONFIG,config_file,indent=4) 

    output('[Upd]config.json\nAdded new configurations.\n')
