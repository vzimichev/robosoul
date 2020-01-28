import numpy as np
import RoboPy
import json
import time
import argparse

def correction(a,s):
    'gets real measurements & returns a which not fallen'
    a = a[:(a.shape[0]-1)]
    newrow = [0.25, 0.5, 0.5, 0.45, 0.5 ,0.5]
    for j in range(s-a.shape[0]):
        a = np.vstack([a,newrow])
    return a

if __name__ == "__main__":
    start_time = time.time()
    parser = argparse.ArgumentParser(description='String')
    parser.add_argument('--prefix','-p', type = str, help='Input prefix',default='')
    parser.add_argument('--correct','-c', type = bool, help='Input prefix',default=False)
    args = parser.parse_args()
    prefix = args.prefix
    correct = args.correct
    RoboPy.output('Launch python3 neuro_compiler.py --prefix '+prefix+' --correct '+str(correct),'start')
    if prefix != '': prefix = prefix + '_'
    
    with open("config.json", "r") as config_file: CONFIG = json.load(config_file)
    for i in CONFIG: 
        if i['prefix'] == prefix + 'net':           
            RoboPy.output('Found net with prefix:'+i['prefix']+' foresight:'+str(i['foresight'])+' strategy:'+i['strategy']+' target:'+i['target'],'start')
            matrix = np.loadtxt(i['source'], 'float',delimiter=',')
            if correct: matrix = correction(matrix,len(np.loadtxt(i['supervisor'], 'float',delimiter=',')))
            flag = "w"
            if matrix.shape[0]<i['foresight']: x = [[0,matrix.shape[0],0,matrix.shape[0]]]
            else: x = [[sp,sp + i['foresight'],sp * i['foresight'], (sp + 1) * i['foresight']] for sp in range(0,matrix.shape[0]-i['foresight']+1)]
            expand = prefix + 'e'+ i['source']
            for gap in x:
                layers = []
                layer = matrix[gap[0]:gap[1]]
                with open(expand,flag) as file: np.savetxt(file,layer,fmt='%.4f',delimiter=',')
                for j in range(i['layers']):
                    weight = np.loadtxt(i['weight names'][j], 'float',delimiter=',')[:(gap[1]-gap[0])*int(i['strategy'][j],36),:(gap[1]-gap[0])*int(i['strategy'][j+1],36)]
                    bias = np.loadtxt(i['bias names'][j], 'float', delimiter=',')[:gap[1]-gap[0]]
                    layer = RoboPy.forward_pass(layer,weight,bias) 
                    l_name = prefix + 'layer_' + str(j+1) + '.csv'
                    with open(l_name,flag) as file: np.savetxt(file,layer,fmt='%.4f',delimiter=',')
                    if flag=="w": RoboPy.output('[Upd]' +l_name)
                    layers.append(l_name)
                flag = "a"
            RoboPy.output('Updated layers of prediction.\n[Upd]config.json')
            with open("config.json", "w") as config_file:
                i.update({'expanded source':expand,'gap':x,'layer names':layers})   
                json.dump(CONFIG,config_file,indent=4)
            
            layer = np.loadtxt(i['layer names'][-1],'float',delimiter=',')
            prediction = np.vstack([layer[0:i['foresight']],layer[2*i['foresight']-1::i['foresight']]])
                              
            if correct: 
                np.savetxt(i['supervisor'],prediction,fmt='%.4f',delimiter=',')
                RoboPy.output('[Upd]'+i['supervisor']+'\nUpdated '+i['supervisor']+' with correction.\n') 
            else:
                np.savetxt(i['result'],prediction,fmt='%.4f',delimiter=',')
                RoboPy.output('[Upd]'+i['result']+'\nUpdated prediction of '+i['supervisor']+'\n') 
            if i['target'] == 'prediction':             
                stf = RoboPy.predict_stf(RoboPy.upscale_sensor_data(prediction))
                RoboPy.output('Neural Network predicted '+str(stf)+' steps to fall.','highlight')
    RoboPy.output('Session of neuro_compiler.py ended in ','time',time.time()-start_time)  
     

            
