#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np

def forward_pass(mtrx,w,b):
     return sigmoid(line(mtrx).dot(w)+line(b)).reshape(b.shape)

def line(mtrx):
    return mtrx.reshape(1,mtrx.shape[0] * mtrx.shape[1])

def sigmoid(a):
    return 1.0/(1.0+np.exp(a))

def upscale_sensor_data(mtrx):
    mtrx[:,0:3] = mtrx[:,0:3] * 40.0 - 20.0
    mtrx[:,3:] = mtrx[:,3:] * 500.0 - 250.0
    return mtrx

def normalize_executor_matrix(mtrx,r):
    for i in range(6):
        mtrx[:,i] =  (mtrx[:,i] - r[i,0]) / (r[i,1] - r[i,0])
    return mtrx

def output(s):
    print(s)
    with open('historia.log', 'a') as myfile:
            myfile.write(s)
    
if __name__ == "__main__":
    matrix = np.loadtxt('matrix.csv', 'int', delimiter=',')
    weight_1 = np.loadtxt('weight_1.csv', 'float',delimiter=',')
    bias_1 = np.loadtxt('bias_1.csv', 'float', delimiter=',')
    weight_2 = np.loadtxt('weight_2.csv', 'float',delimiter=',')
    bias_2 = np.loadtxt('bias_2.csv', 'float', delimiter=',')
    restrictions = np.loadtxt('restrictions.txt', 'int', delimiter = '\t')
    
    matrix = normalize_executor_matrix(matrix,restrictions)
    layer = forward_pass(matrix,weight_1,bias_1)        
    np.savetxt('layer.txt',layer,fmt='%.10f',delimiter='\t')
    prediction = upscale_sensor_data(forward_pass(layer,weight_2,bias_2))
    np.savetxt('prediction.csv',prediction,fmt='%.10f',delimiter=',')
    output('[Upd]layer.txt\nUpdated hidden layer of prediction.\n[Upd]prediction.csv\nUpdated prediction of sensor data.\n')

