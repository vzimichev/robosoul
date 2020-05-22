#!/bin/sh
echo "Launching run_test.sh with folowing variables:"
echo "CI_NUMBER: $CI_NUMBER"

set -e
echo "Launch #0. (executor only)"
python executor.py

for series in $(seq $(($CI_NUMBER)))
do
    for value in $(seq 5)
    do
     echo "Launch #${value}. Series #${series}."
     chmod -c 444 sensor.csv
     python executor.py &
     python neuro_compiler.py -t prediction 
     python backprop.py -t prediction
     python neuro_compiler.py -p rev
     python backprop.py -p rev --learning 0.05 --hyper 0.03 --cool 0.1
     python neuro_compiler.py -c True -p rev
     chmod -c 644 sensor.csv
     wait
    done
    python matrix_inpreter.py walk -r False
done

