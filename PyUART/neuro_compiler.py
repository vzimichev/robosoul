import numpy as np
import RoboPy
import json
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='String')
    parser.add_argument('--prefix','-p', type = str, help='Input prefix',default='')
    args = parser.parse_args()
    prefix = args.prefix
    RoboPy.output('Launch python3 neuro_compiler.py --prefix '+prefix,'start')
    if prefix != '': prefix = prefix + '_'
    
    with open("config.json", "r") as config_file: CONFIG = json.load(config_file)
    for i in CONFIG: 
        if i['prefix'] == prefix + 'net':           
            RoboPy.output('Found net with prefix:'+i['prefix']+' foresight:'+str(i['foresight'])+' strategy:'+str(i['strategy'])+' target:'+i['target'],'start')
            matrix = np.loadtxt(i['source'], 'float',delimiter=',')
            sp,stf,other,flag = 0,0,0,"w"
            while True:
                layers = []
                while sp + i['foresight'] > matrix.shape[0]: 
                    matrix = np.vstack([matrix,np.zeros(shape=(1,6))])
                    other += 1 
                
                layer = matrix[sp:sp + i['foresight']]
                
                for j in range(i['layers']):
                    weight = np.loadtxt(i['weight names'][j], 'float',delimiter=',')
                    bias = np.loadtxt(i['bias names'][j], 'float', delimiter=',')
                    layer = RoboPy.forward_pass(layer,weight,bias) 
                    l_name = prefix + 'layer_' + str(j+1) + '.csv'
                    with open(l_name,flag) as file: np.savetxt(file,layer[:i['foresight']-other],fmt='%.4f',delimiter=',')
                    if flag == "w": RoboPy.output('[Upd]' +l_name+ '\nUpdated hidden layer of prediction.\n')
                    layers.append(l_name)
                sp += i['foresight']
                flag = "a"
                if i['target'] == 'prediction': 
                    if sp == matrix.shape[0]: break
                if i['target'] == 'reverse': 
                    if sp == matrix.shape[0]: break
            
            with open("config.json", "w") as config_file:
                i.update({'layer names':layers})   
                json.dump(CONFIG,config_file,indent=4)

            layer = np.loadtxt(i['layer names'][-1],'float',delimiter=',')
            np.savetxt(i['result'],layer,fmt='%.4f',delimiter=',')
            RoboPy.output('[Upd]'+i['result']+'\nUpdated prediction of '+i['supervisor']+'\n')                   
            
            if i['target'] == 'prediction':             
                stf = RoboPy.predict_stf(RoboPy.upscale_sensor_data(layer))
                RoboPy.output('Neural Network predicted '+str(stf)+' steps to fall.','highlight')
            

            
