#!/bin/sh
set -e
for value in $(seq 25)
do
 echo "Launch #${value}."
 python3 neuro_compiler.py -p pre
 python3 executor.py
 python3 RoboPy.py -p pre
 python3 neuro_compiler.py -p rev
 python3 RoboPy.py -p rev
 for i in *.csv
 do
  cp -n ./$i results/${value}_${i}
 done
done
