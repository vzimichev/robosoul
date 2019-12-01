#!/bin/sh

for i in range(10):
{
python3 executor.py &
python3 RoboPy.py
wait
}