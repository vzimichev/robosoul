#!/bin/sh

for (i = 0; i < 10; i++)
{
python3 executor.py &
python3 RoboPy.py
wait
}