#!/bin/sh
set -e
echo "Launch #0. (executor only)"
python3 executor.py
for series in $(seq 10)
do
    for value in $(seq 5)
    do
     echo "Launch #${value}. Series #${series}."
     python3 executor.py &
     chmod -c 444 sensor.csv
     python3 neuro_compiler.py -t prediction 
     python3 RoboPy.py -t prediction -c 0.05
     python3 neuro_compiler.py -p rev
     python3 RoboPy.py -p rev --learning 0.05 --hyper 0.03 --cool 0.1
     python3 neuro_compiler.py -c True -p rev
     chmod -c 644 sensor.csv
     wait
    done
    python3 matrix_inpreter.py walk -r False
done

