import numpy as np
import time
import sys
import json
import argparse
from colorama import Fore, Style

slash = '/' if 'linux' in sys.platform.lower() else '\\'

def line(mtrx):
    return mtrx.reshape(1,mtrx.shape[0] * mtrx.shape[1])

def upscale_sensor_data(mtrx):
    mtrx[:,:3] = mtrx[:,:3] * 40.0 - 20.0
    mtrx[:,3:] = mtrx[:,3:] * 500.0 - 250.0
    return mtrx

def normalize_sensor_data(mtrx):
    mtrx[:,:3] = (mtrx[:,:3] + 20.0) / 40.0 
    mtrx[:,3:] = (mtrx[:,3:] + 250.0) / 500.0
    return mtrx

def normalize_executor_matrix(mtrx,r):
    for i in range(7):
        mtrx[:,i] =  (mtrx[:,i] - r[i,0]) / (r[i,1] - r[i,0])
    return mtrx

def upscale_executor_matrix(mtrx,r):
    for i in range(7):
        mtrx[:,i] = np.round(mtrx[:,i] * (r[i,1] - r[i,0]) / r[i,2]) * r[i,2] + r[i,0]
    return mtrx

def output(s, color = None, time = None):
    if color == 'error':
        print(Fore.RED + '{}'.format(s))
        print(Style.RESET_ALL)
    if color == 'warning':
        print(Fore.YELLOW + '{}'.format(s))
        print(Style.RESET_ALL)
    if color == 'highlight':
        print(Fore.GREEN + '{}'.format(s))
        print(Style.RESET_ALL) 
    if color == 'start':
        print(Fore.CYAN + '{}'.format(s))
        print(Style.RESET_ALL)
    if color == 'time':
        print(Fore.BLUE + '{}'.format(s) + '{:.3f}'.format(time) + ' seconds.')
        print(Style.RESET_ALL)
    if color == None:
        if '[Upd]' in s:
            print("\033[90m{}\033[00m".format(s))
            print(Style.RESET_ALL) 
        else: print(s)
    with open('historia.log', 'a') as myfile: myfile.write(s+'\n')

def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1','on'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0','off'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')
        
def ready(accelx,accely,accelz,gx,gy,gz):
    if ((abs(accely)>5 or abs(accelz)>5) and abs(accelx)<7) or abs(gx)>200 or abs(gy)>200 or abs(gz)>200: return False
    else: return True
    
def zero_filter(mtrx,n):
    a = mtrx.shape[0] // n
    b = mtrx.shape[1] // n
    for i in range(n-1):
        for j in range(i+1,n):
            for k in range(a):
                for l in range(b):
                    mtrx[a*i+k][b*j+l] = 0  
    return mtrx

def high_pass_filter(mtrx):
    a = mtrx.shape[0]
    b = mtrx.shape[1]
    m = mtrx.max()
    for i in range(a):
        for j in range(b):
            if abs(mtrx[i][j]) < m * 0.005:
                mtrx[i][j] = 0
    return mtrx
