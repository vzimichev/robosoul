#!/bin/sh
mv $CI_PROJECT_DIR/PyUART/*.py .
mv $CI_PROJECT_DIR/PyUART/*.txt .
python3 matrix_inpreter.py walk
python3 weight_matrix_creator.py --target prediction --strategy 68786 --foresight 3 --prefix pre
python3 weight_matrix_creator.py --target prediction --strategy 666 --foresight 8 --prefix longview
python3 weight_matrix_creator.py --target prediction --strategy 6z6 --foresight 3 --prefix wide
python3 weight_matrix_creator.py --target reverse --prefix rev --strategy 666 --foresight 8