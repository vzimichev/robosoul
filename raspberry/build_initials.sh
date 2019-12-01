#!/bin/sh

alias ipython='python3 -m IPython'
ipython nbconvert --to script ../PyUART/*.ipynb
mv ../PyUART/*.py .
python3 matrix_inpreter.py
python3 weight_matrix_creator.py