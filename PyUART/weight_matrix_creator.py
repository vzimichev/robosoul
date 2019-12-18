#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import time,serial,random
import numpy as np

def zero_filter(mtrx,n):
    a = mtrx.shape[0] // n
    b = mtrx.shape[1] // n
    for i in range(n-1):
        for j in range(i+1,n):
            for k in range(a):
                for l in range(b):
                    mtrx[a*i+k][b*j+l] = 0  
    return mtrx

def temp_mask(mtrx,n):
    a = mtrx.shape[0] // n
    b = mtrx.shape[1] // n
    for i in range(n):
        for j in range(0,i):
            for k in range(a):
                for l in range(b):
                    mtrx[a*i+k][b*j+l] = i-j  
    return mtrx

def output(s):
    print(s)
    with open('historia.log', 'a') as myfile:
            myfile.write(s)

matrix = np.loadtxt('matrix.csv', 'int', delimiter = ',')
leng = matrix.shape[0]

weight_1 = np.random.randint(-50,50,size=(leng*6,leng*6)) / 50
weight_1 = zero_filter(weight_1,leng)
np.savetxt('weight_1.csv',weight_1,fmt='%.2f',delimiter=',')
output('[Upd]weight_1.csv\nCreated first weight matrix to prediction alg.\n')
        
bias_1 = np.zeros(shape=(leng,6))
np.savetxt('bias_1.csv',bias_1,fmt='%.2f',delimiter=',')
output('[Upd]bias_1.csv\nCreated first zero matrix of bias to prediction alg.\n')
        
weight_2 = np.random.randint(-50,50,size=(leng*6,leng*6)) / 50
weight_2 = zero_filter(weight_2,leng)
np.savetxt('weight_2.csv',weight_2,fmt='%.2f',delimiter=',')
output('[Upd]weight_2.csv\nCreated second weight matrix to prediction alg.\n')
        
bias_2 = np.zeros(shape=(leng,6))
np.savetxt('bias_2.csv',bias_2,fmt='%.2f',delimiter=',')
output('[Upd]bias_2.csv\nCreated second zero matrix of bias to prediction alg.\n')
        
rev_weight_1 = np.random.randint(-50,50,size=(leng*6,leng*6)) / 50
rev_weight_1 = zero_filter(rev_weight_1,leng)
np.savetxt('rev_weight_1.csv',rev_weight_1,fmt='%.2f',delimiter=',')
output('[Upd]rev_weight_1.csv\nCreated first weight matrix to reverse alg.\n')
        
rev_bias_1 = np.zeros(shape=(leng,6))
np.savetxt('rev_bias_1.csv',rev_bias_1,fmt='%.2f',delimiter=',')
output('[Upd]rev_bias_1.csv\nCreated first zero matrix of bias to reverse alg.\n')
        
rev_weight_2 = np.random.randint(-50,50,size=(leng*6,leng*6)) / 50
rev_weight_2 = zero_filter(rev_weight_2,leng)
np.savetxt('rev_weight_2.csv',rev_weight_2,fmt='%.2f',delimiter=',')
output('[Upd]rev_weight_2.csv\nCreated second weight matrix to reverse alg.\n')

rev_bias_2 = np.zeros(shape=(leng,6))
np.savetxt('rev_bias_2.csv',rev_bias_2,fmt='%.2f',delimiter=',')
output('[Upd]rev_bias_2.csv\nCreated second zero matrix of bias to reverse alg.\n')

temperature = np.zeros(shape=(leng*6,leng*6)) 
temperature = temp_mask(temperature,leng)
np.savetxt('temperature.txt',temperature,fmt='%d',delimiter='|')
output('[Upd]temperature.txt\nCreated temperature mask.\n')

