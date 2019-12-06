#!/bin/sh
alias ipython='python3 -m IPython'
ipython nbconvert --to script $CI_PROJECT_DIR/PyUART/*.ipynb
mv $CI_PROJECT_DIR/PyUART/*.py .
mv $CI_PROJECT_DIR/PyUART/*.txt .
python3 matrix_inpreter.py walk
python3 weight_matrix_creator.py