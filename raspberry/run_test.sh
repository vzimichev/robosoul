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
 python3 RoboPy.py -t prediction
 python3 neuro_compiler.py -p rev
 python3 RoboPy.py -p rev --learning 0.05 --hyper 0.03 --cool 0.1
 python3 neuro_compiler.py -c True -p rev
 
 wait
done

