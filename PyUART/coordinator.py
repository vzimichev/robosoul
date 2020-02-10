from threading import Thread
from RoboPy import output
import os

if __name__ == "__main__":
    for j in range(1,26):        
        #forward
        executor = Thread(target = os.system, args = ('python3 executor.py', ))
        neuro_compiler = Thread(target = os.system, args = ('python3 neuro_compiler.py -p pre', ))
        RoboPy = Thread(target = os.system, args = ('python3 RoboPy.py -p pre', ))
        #reverse
        rev_neuro_compiler = Thread(target = os.system, args = ('python3 neuro_compiler.py -p rev', ))
        rev_RoboPy = Thread(target = os.system, args = ('python3 RoboPy.py -p rev', ))
        #iteration
        it_neuro_compiler = Thread(target = os.system, args = ('python3 neuro_compiler.py -c True -p rev', ))
        #output
        print_output = Thread(target = output, args = ('Launch #'+str(j),))
                                                       
        print_output.start()
        print_output.join()
        executor.start()
        neuro_compiler.start()
        executor.join()
        neuro_compiler.join()
        RoboPy.start()
        rev_neuro_compiler.start()
        rev_neuro_compiler.join()
        rev_RoboPy.start()
        rev_RoboPy.join()
        it_neuro_compiler.start()
        it_neuro_compiler.join()
        RoboPy.join()