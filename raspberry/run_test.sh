#!/bin/sh
set -e
for value in $(seq 25)
do
 python3 executor.py -p rev &
 python3 neuro_compiler.py
 wait
 python3 RoboPy.py &
 python3 neuro_compiler.py -p rev
 wait
 python3 RoboPy.py -p rev
 for i in *.csv
 do
  cp -n ./$i results/${value}_${i}
 done
done
