from utils import *

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
        weight = full_weight[:(gap[1]-gap[0])*int(netinfo['strategy'][-2],36),:(gap[1]-gap[0])*int(netinfo['strategy'][-1],36)]
        full_bias = np.loadtxt(netinfo['bias names'][-1], 'float', delimiter=',')
        bias = full_bias[:gap[1]-gap[0]]
        full_temperature = np.loadtxt(netinfo['temp names'][-1], 'int', delimiter='|')
        temperature = full_temperature[:(gap[1]-gap[0])*int(netinfo['strategy'][-2],36),:(gap[1]-gap[0])*int(netinfo['strategy'][-1],36)]
        layer = np.loadtxt(netinfo['layer names'][-2], 'float', delimiter=',')[gap[2]:gap[3]]
        
        #backpropagation of output layer
        weight = weight - netinfo['learning rate'] * line(layer).T.dot(line(delta)) - netinfo['hyper'] * weight - netinfo['cool'] * weight * temperature   
        bias = bias - netinfo['learning rate'] * delta
        weight = zero_filter(weight,netinfo['foresight'])
        full_weight[:(gap[1]-gap[0])*int(netinfo['strategy'][-2],36),:(gap[1]-gap[0])*int(netinfo['strategy'][-1],36)] = weight
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
            weight = full_weight[:(gap[1]-gap[0])*int(netinfo['strategy'][j],36),:(gap[1]-gap[0])*int(netinfo['strategy'][j+1],36)]
            full_bias = np.loadtxt(netinfo['bias names'][j], 'float', delimiter=',')
            bias = full_bias[:gap[1]-gap[0]]
            full_temperature = np.loadtxt(netinfo['temp names'][j], 'int', delimiter='|')
            temperature = full_temperature[:(gap[1]-gap[0])*int(netinfo['strategy'][j],36),:(gap[1]-gap[0])*int(netinfo['strategy'][j+1],36)]
            full_layer = np.loadtxt(netinfo['layer names'][j], 'float', delimiter=',')
            layer = full_layer[gap[2]:gap[3]]
            
            weight = weight - netinfo['learning rate'] * line(layer).T.dot(line(delta)) - netinfo['hyper'] * weight - netinfo['cool'] * weight * temperature
            bias = bias - netinfo['learning rate'] * delta.reshape(bias.shape) 
            weight = zero_filter(weight,netinfo['foresight'])
            
            
            full_weight[:(gap[1]-gap[0])*int(netinfo['strategy'][j],36),:(gap[1]-gap[0])*int(netinfo['strategy'][j+1],36)] = weight
            np.savetxt(netinfo['weight names'][j],full_weight,fmt='%.4f',delimiter=',')
            full_bias[:gap[1]-gap[0]] = bias
            np.savetxt(netinfo['bias names'][j],full_bias,fmt='%.4f',delimiter=',')  
            if flag: output('[Upd]' + netinfo['weight names'][j] + '\n[Upd]' + netinfo['bias names'][j])
                          
            J += netinfo['hyper']*np.sum(full_weight**2) + netinfo['cool']*np.sum((full_temperature*full_weight)**2)
        flag = False
    with open(netinfo['report'], 'a') as myfile: myfile.write('{:.4f}'.format(J)+'\n')
    output('Updated matrixes of prediction according to backpropagation.\n[Upd]'+netinfo['report']+'\nTarget function of '+netinfo['target']+' net: '+ '{:.4f}'.format(J))  
    
        
if __name__ == "__main__":
    start_time = time.time()
    parser = argparse.ArgumentParser(description='String')
    parser.add_argument('--prefix','-p', type = str, help='Input prefix of net. [default = ""]',default='')
    parser.add_argument('--target','-t', type = str, help='Input target of nets to be backpropagated. [default = ""]',default='')
    parser.add_argument('--learning','-l', type = float, help='Learning rate of backpropagation. [default = 0.1]',default=0.1)
    parser.add_argument('--hyper','-hp', type = float, help='L2 normalization parameter. [default = 0]',default=0.0)
    parser.add_argument('--cool','-c', type = float, help='Cool parameter of non-Markov process. [default = 0.1]',default=0.1)
    args = parser.parse_args()
    prefix = args.prefix
    target = args.target
    learning = args.learning
    hyper = args.hyper
    cool = args.cool

    output('Launch python3 RoboPy.py --learning '+str(learning)+' --hyper '+str(hyper)+' --cool '+str(cool)+' --prefix '+prefix,'start')    
    if prefix != '': prefix = prefix + '_'
    
    with open("config.json", "r") as config_file: CONFIG = json.load(config_file)
    for i in CONFIG: 
        if i['prefix'] == prefix + 'net' or i['target'] == target: 
            output('Found net with prefix:'+i['prefix']+' foresight:'+str(i['foresight'])+' strategy:'+i['strategy']+' target:'+i['target'],'start')
            if (cool * i['foresight'] > 0.9): output('Influence of cool parameter is very strong','warning')
            with open("config.json", "w") as config_file:
                i.update({'learning rate':learning,'hyper':hyper,'cool':cool})   
                json.dump(CONFIG,config_file,indent=4)
    
    with open("config.json", "r") as config_file: CONFIG = json.load(config_file)
    for i in CONFIG: 
        if i['prefix'] == prefix + 'net' or i['target'] == target: backpropagation(netinfo=i)
    output('Session of RoboPy.py ended in ','time',time.time()-start_time) 