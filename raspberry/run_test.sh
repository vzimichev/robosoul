#!/bin/sh
set -e
for value in $(seq 25)
do
 python3 executor.py &
 python3 neuro_compiler.py
 wait
 python3 RoboPy.py
 for i in *.csv
 do
  cp -n ./$i results/${value}_${i}
 done
done
rm results/*_J.csv