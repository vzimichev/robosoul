#!/bin/sh

for value in {1..5}
do
python3 executor.py
python3 neuro_compiler.py
python3 RoboPy.py
done
