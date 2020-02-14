from threading import Thread
from RoboPy import output
from sarge import run as system


if __name__ == "__main__":

    for j in range(1,26):        
        system('echo "Launch #'+str(j)+'"')
        
        #forward
        executor = Thread(target = system, args = ('python3 executor.py', ))
        neuro_compiler = Thread(target = system, args = ('python3 neuro_compiler.py -p pre', ))
        Robo_Py = Thread(target = system, args = ('python3 RoboPy.py -p pre', ))
        #reverse
        rev_neuro_compiler = Thread(target = system, args = ('python3 neuro_compiler.py -p rev', ))
        rev_RoboPy = Thread(target = system, args = ('python3 RoboPy.py -p rev', ))
        #iteration
        it_neuro_compiler = Thread(target = system, args = ('python3 neuro_compiler.py -c True -p rev', ))
        
        executor.start()

        neuro_compiler.start()

        neuro_compiler.join()

        executor.join()

        Robo_Py.start()

        Robo_Py.join()

        rev_neuro_compiler.start()

        rev_neuro_compiler.join()

        rev_RoboPy.start()

        rev_RoboPy.join()

        it_neuro_compiler.start()

        it_neuro_compiler.join()
