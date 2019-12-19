#!/bin/sh
mv $CI_PROJECT_DIR/PyUART/*.py .
mv $CI_PROJECT_DIR/PyUART/*.txt .
python3 matrix_inpreter.py walk
python3 weight_matrix_creator.py