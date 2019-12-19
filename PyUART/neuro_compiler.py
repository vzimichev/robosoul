import numpy as np
import RoboPy

if __name__ == "__main__":
    matrix = np.loadtxt('matrix.csv', 'int', delimiter=',')
    weight_1 = np.loadtxt('weight_1.csv', 'float',delimiter=',')
    bias_1 = np.loadtxt('bias_1.csv', 'float', delimiter=',')
    weight_2 = np.loadtxt('weight_2.csv', 'float',delimiter=',')
    bias_2 = np.loadtxt('bias_2.csv', 'float', delimiter=',')
    restrictions = np.loadtxt('restrictions.txt', 'int', delimiter = '\t')
    
    matrix = RoboPy.normalize_executor_matrix(matrix,restrictions)
    layer = RoboPy.forward_pass(matrix,weight_1,bias_1)        
    np.savetxt('layer.txt',layer,fmt='%.10f',delimiter='\t')
    prediction = RoboPy.upscale_sensor_data(RoboPy.forward_pass(layer,weight_2,bias_2))
    predicted_stf = RoboPy.predict_stf(prediction)
    RoboPy.output('Neural Network predicted '+str(predicted_stf)+' steps to fall.','highlight')
    np.savetxt('prediction.csv',prediction,fmt='%.10f',delimiter=',')
    RoboPy.output('[Upd]layer.txt\nUpdated hidden layer of prediction.\n[Upd]prediction.csv\nUpdated prediction of sensor data.\n')