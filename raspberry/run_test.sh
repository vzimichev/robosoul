#!/bin/sh
set -e
python3 executor.py &
python3 neuro_compiler.py -t prediction
wait

for value in $(seq 250)
do
 echo "Launch #${value}."
 python3 executor.py &
 python3 neuro_compiler.py -t prediction 

 python3 RoboPy.py -p pre1 --learning 0.1 --hyper 0.0 --cool 0.1
 python3 RoboPy.py -p pre2 --learning 0.05 --hyper 0.0 --cool 0.1
 python3 RoboPy.py -p pre3 --learning 0.05 --hyper 0.0 --cool 0.05
 python3 RoboPy.py -p longview1 --learning 0.1 --hyper 0.0 --cool 0.1
 python3 RoboPy.py -p longview2 --learning 0.05 --hyper 0.0 --cool 0.1
 python3 RoboPy.py -p longview3 --learning 0.05 --hyper 0.0 --cool 0.05
 python3 RoboPy.py -p wide1 --learning 0.1 --hyper 0.0 --cool 0.1
 python3 RoboPy.py -p wide2 --learning 0.05 --hyper 0.0 --cool 0.1
 python3 RoboPy.py -p wide3 --learning 0.05 --hyper 0.0 --cool 0.05

 python3 neuro_compiler.py -p rev
 python3 RoboPy.py -p rev
 python3 neuro_compiler.py -c True -p rev
 
 wait
done

