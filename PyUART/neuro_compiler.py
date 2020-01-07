import numpy as np
import RoboPy
import json
import argparse

if __name__ == "__main__":
    RoboPy.output('neuro_compiler.py launch','start')
    parser = argparse.ArgumentParser(description='String')
    parser.add_argument('--prefix','-p', type = str, help='Input prefix',default='')
    args = parser.parse_args()
    prefix = args.prefix

    if prefix != '': prefix = prefix + '_'
    
    with open("config.json", "r") as config_file: CONFIG = json.load(config_file)
    for i in CONFIG: 
        if i['prefix'] == prefix + 'net':           
            matrix = np.loadtxt(i['source'], 'float',delimiter=',')
            sp,pstf,flag = 0,0,"w"
            while sp == pstf:
                layers = []
                layer = matrix[sp:sp+i['foresight']]
                for j in range(i['layers']):
                    weight = np.loadtxt(i['weight names'][j], 'float',delimiter=',')
                    bias = np.loadtxt(i['bias names'][j], 'float', delimiter=',')
                    layer = RoboPy.forward_pass(layer,weight,bias) 
                    l_name = prefix + 'layer_' + str(j+1) + '.csv'
                    with open(l_name,flag) as file: np.savetxt(file,layer,fmt='%.4f',delimiter=',')
                    RoboPy.output('[Upd]' +l_name+ '\nUpdated hidden layer of prediction.\n')
                    layers.append(l_name)
                sp += i['foresight']
                flag = "a"
                if i['target'] == 'prediction': pstf = RoboPy.predict_stf(RoboPy.upscale_sensor_data(layer))
                if i['target'] == 'reverse': 
                    pstf = sp
                    if sp > 10: break


            with open("config.json", "w") as config_file:
                i.update({'layer names':layers})   
                json.dump(CONFIG,config_file,indent=4)

            np.savetxt(i['result'],np.loadtxt(i['layer names'][-1],'float',delimiter=','),fmt='%.4f',delimiter=',')
            RoboPy.output('[Upd]'+i['result']+'\nUpdated prediction of sensor data.\n')                   
                      
            RoboPy.output('Neural Network predicted '+str(pstf)+' steps to fall.','highlight')
            

            
