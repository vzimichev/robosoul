#!/bin/sh
set -e
echo "Launch #0. (executor only)"
python3 executor.py

for value in $(seq 25)
do
 echo "Launch #${value}."
 python3 executor.py &
 chmod -c 444 sensor.csv
 python3 neuro_compiler.py -t prediction 
 python3 RoboPy.py -t prediction
 python3 neuro_compiler.py -p rev
 python3 RoboPy.py -p rev --learning 0.05 --hyper 0.03 --cool 0.1
 python3 neuro_compiler.py -c True -p rev
 chmod -c 644 sensor.csv
 wait
done

