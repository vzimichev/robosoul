import numpy as np
import time
import json
import pandas as pd
from RoboPy import output

if __name__ == "__main__":
    start_time = time.time()
    params = ['strategy','foresight','learning rate','hyper','cool']
    executor_report = 'executor_report.xls'
    data = {'executor': [*['' for k in params],*list(np.loadtxt(executor_report, 'int'))]}
    target = {}

    with open("config.json", "r") as config_file: CONFIG = json.load(config_file)
    for i in CONFIG: 
        if i['target'] == 'prediction':
            data.update({i['prefix'] :   [*[i[k] for k in params],*list(np.loadtxt(i['report'], 'int', delimiter=',')[:,0])]})
            target.update({i['prefix'] : [*[i[k] for k in params],*list(np.loadtxt(i['report'], 'float', delimiter=',')[:,1])]})
    index = [*params,*[i for i in range(1,len(data['executor'])-len(params)+1)]]
    df = pd.DataFrame(data,index=index)
    df.to_excel('steps_ev.xlsx')
    tf = pd.DataFrame(target, index=index)
    tf.to_excel('target_ev.xlsx')
    
    print('Steps to fall\n',df)
    print('Target function\n',tf)
    
    output('Session of viewer.py ended in ','time',time.time()-start_time)  
