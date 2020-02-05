import numpy as np
import time
import argparse
import json
from RoboPy import output,line,ready,upscale_sensor_data

def sigmoid(a):
    return 1.0/(1.0+np.exp(a))

def forward_pass(mtrx,w,b):
    return sigmoid(line(mtrx).dot(w)+line(b)).reshape(b.shape)
 
def predict_stf(prdctn):
    for i in range(len(prdctn)):
        if not ready(*prdctn[i]): break 
    return i + 1

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
    parser.add_argument('--prefix','-p', type = str, help='Input prefix of net. [default = ""]',default='')
    parser.add_argument('--correct','-c', type = bool, help='Use of correction algorythm to improove solution before iteration. [default = False]',default=False)
    args = parser.parse_args()
    prefix = args.prefix
    correct = args.correct
    output('Launch python3 neuro_compiler.py --prefix '+prefix+' --correct '+str(correct),'start')
    if prefix != '': prefix = prefix + '_'
    
    with open("config.json", "r") as config_file: CONFIG = json.load(config_file)
    for i in CONFIG: 
        if i['prefix'] == prefix + 'net':           
            output('Found net with prefix:'+i['prefix']+' foresight:'+str(i['foresight'])+' strategy:'+i['strategy']+' target:'+i['target'],'start')
            matrix = np.loadtxt(i['source'], 'float',delimiter=',')
            if correct: matrix = correction(matrix,len(np.loadtxt(i['supervisor'], 'float',delimiter=',')))
            flag = "w"
            if matrix.shape[0]<i['foresight']: x = [[0,matrix.shape[0],0,matrix.shape[0]]]
            else: x = [[sp,sp + i['foresight'],sp * i['foresight'], (sp + 1) * i['foresight']] for sp in range(0,matrix.shape[0]-i['foresight']+1)]
            expand = prefix + 'e' + i['source']
            for gap in x:
                layers = []
                layer = matrix[gap[0]:gap[1]]
                with open(expand,flag) as file: np.savetxt(file,layer,fmt='%.4f',delimiter=',')
                for j in range(i['layers']):
                    weight = np.loadtxt(i['weight names'][j], 'float',delimiter=',')[:(gap[1]-gap[0])*int(i['strategy'][j],36),:(gap[1]-gap[0])*int(i['strategy'][j+1],36)]
                    bias = np.loadtxt(i['bias names'][j], 'float', delimiter=',')[:gap[1]-gap[0]]
                    layer = forward_pass(layer,weight,bias) 
                    l_name = prefix + 'layer_' + str(j+1) + '.csv'
                    with open(l_name,flag) as file: np.savetxt(file,layer,fmt='%.4f',delimiter=',')
                    if flag=="w": output('[Upd]' +l_name)
                    layers.append(l_name)
                flag = "a"
            output('Updated layers of prediction.\n[Upd]config.json')
            with open("config.json", "w") as config_file:
                i.update({'expanded source':expand,'gap':x,'layer names':layers})   
                json.dump(CONFIG,config_file,indent=4)
            
            layer = np.loadtxt(i['layer names'][-1],'float',delimiter=',')
            prediction = np.vstack([layer[0:i['foresight']],layer[2*i['foresight']-1::i['foresight']]])
                              
            if correct: 
                np.savetxt(i['supervisor'],prediction,fmt='%.4f',delimiter=',')
                output('[Upd]'+i['supervisor']+'\nUpdated '+i['supervisor']+' with correction.') 
            else:
                np.savetxt(i['result'],prediction,fmt='%.4f',delimiter=',')
                output('[Upd]'+i['result']+'\nUpdated prediction of '+i['supervisor']) 
            if i['target'] == 'prediction':             
                stf = predict_stf(upscale_sensor_data(prediction))
                output('Neural Network predicted '+str(stf)+' steps to fall.','highlight')
    output('Session of neuro_compiler.py ended in ','time',time.time()-start_time)  
     

            
