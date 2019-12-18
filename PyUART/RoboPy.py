import csv
import numpy as np

def sigmoid(a):
    return 1.0/(1.0+np.exp(a))

def line(mtrx):
    return mtrx.reshape(1,mtrx.shape[0] * mtrx.shape[1])

def backpropagation(mtrx,layr,prdcn,ac,w_2,w_1,b_2,b_1,alpha,lambd,cl,temp):
    delta_error = (prdcn - ac) * prdcn * (1 - prdcn)
    delta_hidden = (line(delta_error).dot(w_2.T)) * line(layr) * (1 - line(layr))
    w_2 = w_2 - alpha * line(layr).T.dot(line(delta_error)) - lambd * w_2 - cl * w_2 * temp
    w_1 = w_1 - alpha * line(mtrx).T.dot(line(delta_hidden)) - lambd * w_1 - cl *w_1 * temp
    b_2 = b_2 - alpha * delta_error
    b_1 = b_1 - alpha * delta_hidden.reshape(b_1.shape) 
    return w_2,w_1,b_2,b_1

def zero_filter(mtrx,n):
    a = mtrx.shape[0] // n
    b = mtrx.shape[1] // n
    for i in range(n-1):
        for j in range(i+1,n):
            for k in range(a):
                for l in range(b):
                    mtrx[a*i+k][b*j+l] = 0  
    return mtrx

def correct(a,s):
    'gets real measurements & returns a which not fallen'
    a = a[:(a.shape[0]-1)]
    newrow = [0.25, 0.5, 0.5, 0.45, 0.5 ,0.5]
    for j in range(s-a.shape[0]):
        a = np.vstack([a,newrow])
    return a

def upscale_sensor_data(mtrx):
    mtrx[:,:3] = mtrx[:,:3] * 40.0 - 20.0
    mtrx[:,3:] = mtrx[:,3:] * 500.0 - 250.0
    return mtrx

def normalize_sensor_data(mtrx):
    mtrx[:,:3] = (mtrx[:,:3] + 20.0) / 40.0 
    mtrx[:,3:] = (mtrx[:,3:] + 250.0) / 500.0
    return mtrx

def normalize_executor_matrix(mtrx,r):
    for i in range(6):
        mtrx[:,i] =  (mtrx[:,i] - r[i,0]) / (r[i,1] - r[i,0])
    return mtrx

def upscale_executor_matrix(mtrx,r):
    for i in range(6):
        mtrx[:,i] = mtrx[:,i] * (r[i,1] - r[i,0]) + r[i,0]
    return mtrx
        
def forward_pass(mtrx,w,b):
     return sigmoid(line(mtrx).dot(w)+line(b)).reshape(b.shape)
    
def output(s):
    print(s)
    with open('historia.log', 'a') as myfile:
            myfile.write(s)
    
if __name__ == "__main__":
        matrix = np.loadtxt('matrix.csv', 'int', delimiter=',')
        sensor = np.loadtxt('sensor.csv', 'float', delimiter=',')
        temperature = np.loadtxt('temperature.txt', 'int', delimiter='|')
        restrictions = np.loadtxt('restrictions.txt', 'int', delimiter = '\t')
        
        #prediction net (supervisor:sensor)
        
        prediction = np.loadtxt('prediction.csv', 'float', delimiter=',')
        layer = np.loadtxt('layer.txt', 'float', delimiter='\t')
        weight_1 = np.loadtxt('weight_1.csv', 'float', delimiter=',')
        weight_2 = np.loadtxt('weight_2.csv', 'float', delimiter=',')
        bias_1 = np.loadtxt('bias_1.csv', 'float', delimiter=',')
        bias_2 = np.loadtxt('bias_2.csv', 'float', delimiter=',')
        
        matrix = normalize_executor_matrix(matrix,restrictions)
        sensor = normalize_sensor_data(sensor)
        prediction = normalize_sensor_data(prediction)
        learning_rate = 0.1
        hyper = 0.1
        cool = 0.2
        stf = sensor.shape[0]  
        steps = matrix.shape[0]
            
        J = np.sum((sensor-prediction[:stf])**2) + hyper*np.sum(weight_1**2) + hyper*np.sum(weight_2**2) + cool*np.sum((temperature*weight_2)**2) + cool*np.sum((temperature*weight_1)**2)
        output('Target function of prediction net:'+str(J)+'\nRunning backpropagation for prediction.\nSource of data: matrix for executor\nSupervisor: sensor')
        
        weight_2[:stf*layer.shape[1],:stf*prediction.shape[1]],weight_1[:stf*matrix.shape[1],:stf*layer.shape[1]],bias_2[:stf],bias_1[:stf] = backpropagation(matrix[:stf],layer[:stf],prediction[:stf],sensor,weight_2[:stf*layer.shape[1],:stf*prediction.shape[1]],weight_1[:stf*matrix.shape[1],:stf*layer.shape[1]],bias_2[:stf],bias_1[:stf],learning_rate,hyper,cool,temperature[:stf*6,:stf*6])
        weight_2 = zero_filter(weight_2,steps)
        weight_1 = zero_filter(weight_1,steps)
        
        np.savetxt('weight_2.csv',weight_2,fmt='%.2f',delimiter=',')
        np.savetxt('weight_1.csv',weight_1,fmt='%.2f',delimiter=',')
        np.savetxt('bias_2.csv',bias_2,fmt='%.2f',delimiter=',')
        np.savetxt('bias_1.csv',bias_1,fmt='%.2f',delimiter=',')
        output('[Upd]weight_2.scv\n[Upd]weight_1.csv\n[Upd]bias_2.csv\n[Upd]bias_1.csv\nUpdated matrixes of prediction according to backpropagation.')
        
        #reverse net (supervisor:matrix)
        
        rev_weight_1 = np.loadtxt('rev_weight_1.csv', 'float', delimiter=',')
        rev_weight_2 = np.loadtxt('rev_weight_2.csv', 'float', delimiter=',')
        rev_bias_1 = np.loadtxt('rev_bias_1.csv', 'float', delimiter=',')
        rev_bias_2 = np.loadtxt('rev_bias_2.csv', 'float', delimiter=',')
        
        output('Running reverse forward pass.')
        layer = forward_pass(sensor,rev_weight_2[:stf*6,:stf*6],rev_bias_2[:stf])
        reverse = forward_pass(layer,rev_weight_1[:stf*6,:stf*6],rev_bias_1[:stf])

        learning_rate = 0.1
        hyper = 0.2
        cool = 0.2
        J_rev = np.sum((reverse-matrix[:stf])**2) + np.sum(rev_weight_1**2) + np.sum(rev_weight_2**2) + cool*np.sum((temperature*rev_weight_2)**2) + cool*np.sum((temperature*rev_weight_1)**2)
        output('Target function of reverse net:'+str(J_rev)+'\nRunnning backpropagation for reverse.\nSource of data: sensor(acc&gyro)\nSupervisor: matrix')
        rev_weight_2[:stf*layer.shape[1],:stf*reverse.shape[1]],rev_weight_1[:stf*sensor.shape[1],:stf*layer.shape[1]],rev_bias_2[:stf],rev_bias_1[:stf] = backpropagation(sensor,layer,reverse,matrix[:stf],rev_weight_2[:stf*layer.shape[1],:stf*reverse.shape[1]],rev_weight_1[:stf*sensor.shape[1],:stf*layer.shape[1]],rev_bias_2[:stf],rev_bias_1[:stf],learning_rate,hyper,cool,temperature[:stf*6,:stf*6])
        rev_weight_2 = zero_filter(rev_weight_2,steps)
        rev_weight_1 = zero_filter(rev_weight_1,steps)
        
        np.savetxt('rev_weight_2.csv',rev_weight_2,fmt='%.2f',delimiter=',')
        np.savetxt('rev_weight_1.csv',rev_weight_1,fmt='%.2f',delimiter=',')
        np.savetxt('rev_bias_2.csv',rev_bias_2,fmt='%.2f',delimiter=',')
        np.savetxt('rev_bias_1.csv',rev_bias_1,fmt='%.2f',delimiter=',')
        output('[Upd]rev_weight_2.csv\n[Upd]rev_weight_1.csv\n[Upd]rev_bias_2.csv\n[Upd]rev_bias_1.csv\nUpdated matrixes of reverse according to backpropagation.')

        #correction
       
        sensor = upscale_sensor_data(correct(sensor,steps)) 
        
        #iteration
        
        output('Running forward pass for iteration.')
        layer = forward_pass(sensor,rev_weight_2,rev_bias_2)
        reverse = forward_pass(layer,rev_weight_1,rev_bias_1)     
        matrix = upscale_executor_matrix(reverse,restrictions)
        np.savetxt('matrix.csv',matrix,fmt='%d',delimiter=',')
        output('[Upd]matrix.csv\nUpdated matrix to be executed.\n')
        
        with open('J.csv', mode='a') as csv_file:
            J_file = csv.writer(csv_file, delimiter=',')
            J_file.writerow([J, J_rev,stf]) 
        
        

