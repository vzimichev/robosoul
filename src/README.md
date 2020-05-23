**Python helper scripts**:

*backprop.py*
* description: backpropagation realisation
* inputs: prediction, result of action, matrixes of NN
* outputs: corrected weight&bias matrixes

*executor.py*
* description: action realisation
* inputs: normalized action algorythm
* outputs: normalized sensor data

*matrix_inpreter.py*
* description: interpretation of input action algorythm
* inputs: text string of algorythm
* outputs: normalized action algorythm

*neuro_compiler.py*
* description: forward pass realisation
* inputs: normalized action algorythm, weight&bias matrixes
* outputs: normalized layers, nomalized prediction of sensor data

*utils.py*
* description: common usage
* inputs: not specified
* outputs: normalization, outputs, filters

*viewer.py*
* description: graph plotter
* inputs: learning process reports
* outputs: main report with graphs

*weight_matrix_creator.py*
* description: weight matrix creator
* inputs: 
    nessesary - name,strategy,foresight
    optional - learning rate, hyper parameters
* outputs: weight&bias matrixes

**Other files out here**:

*gold.csv*
* description: sensor data example on success

*restrictions.txt*
* description: restrictions for servodrivers w/discretization step

 




