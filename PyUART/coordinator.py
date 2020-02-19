from threading import Thread
from sarge import run as system


if __name__ == "__main__":
    #forward
    executor = Thread(target = system, args = ('python3 executor.py', ))
    neuro_compiler = Thread(target = system, args = ('python3 neuro_compiler.py -t prediction', ))
    
    executor.start()
    neuro_compiler.start()
    neuro_compiler.join()
    executor.join()
    
    for j in range(1,26):        
        system('echo "Launch #'+str(j)+'"')
               
        executor = Thread(target = system, args = ('python3 executor.py', ))
        neuro_compiler = Thread(target = system, args = ('python3 neuro_compiler.py -t prediction', ))
        Robo_Py = Thread(target = system, args = ('python3 RoboPy.py -t prediction', ))
        #reverse
        rev_neuro_compiler = Thread(target = system, args = ('python3 neuro_compiler.py -p rev', ))
        rev_RoboPy = Thread(target = system, args = ('python3 RoboPy.py -p rev', ))
        #iteration
        it_neuro_compiler = Thread(target = system, args = ('python3 neuro_compiler.py -c True -p rev', ))
        
        executor.start()
        
        Robo_Py.start()
        Robo_Py.join()

        rev_neuro_compiler.start()
        rev_neuro_compiler.join()

        rev_RoboPy.start()
        rev_RoboPy.join()

        it_neuro_compiler.start()
        it_neuro_compiler.join()
        
        neuro_compiler.start()
        neuro_compiler.join()
        
        executor.join()
    
    Robo_Py = Thread(target = system, args = ('python3 RoboPy.py -t prediction', ))
    #reverse
    rev_neuro_compiler = Thread(target = system, args = ('python3 neuro_compiler.py -p rev', ))
    rev_RoboPy = Thread(target = system, args = ('python3 RoboPy.py -p rev', ))
    #iteration
    it_neuro_compiler = Thread(target = system, args = ('python3 neuro_compiler.py -c True -p rev', ))
    
    Robo_Py.start()
    Robo_Py.join()

    rev_neuro_compiler.start()
    rev_neuro_compiler.join()

    rev_RoboPy.start()
    rev_RoboPy.join()

    it_neuro_compiler.start()
    it_neuro_compiler.join()
        