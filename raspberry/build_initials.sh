#!/bin/sh
mv $CI_PROJECT_DIR/PyUART/*.py .
mv $CI_PROJECT_DIR/PyUART/*.txt .
python3 matrix_inpreter.py walk
python3 weight_matrix_creator.py --target prediction --strategy 68786 --foresight 3 --prefix pre1
python3 weight_matrix_creator.py --target prediction --strategy 68786 --foresight 3 --prefix pre2
python3 weight_matrix_creator.py --target prediction --strategy 68786 --foresight 3 --prefix pre3
python3 weight_matrix_creator.py --target prediction --strategy 666 --foresight 8 --prefix longview1
python3 weight_matrix_creator.py --target prediction --strategy 666 --foresight 8 --prefix longview2
python3 weight_matrix_creator.py --target prediction --strategy 666 --foresight 8 --prefix longview3
python3 weight_matrix_creator.py --target prediction --strategy 6z6 --foresight 3 --prefix wide1
python3 weight_matrix_creator.py --target prediction --strategy 6z6 --foresight 3 --prefix wide2
python3 weight_matrix_creator.py --target prediction --strategy 6z6 --foresight 3 --prefix wide3
python3 weight_matrix_creator.py --target reverse --prefix rev --strategy 666 --foresight 8