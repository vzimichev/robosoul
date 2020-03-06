#!/bin/sh
cp $CI_PROJECT_DIR/PyUART/* .
python3 matrix_inpreter.py walk
python3 weight_matrix_creator.py --target prediction --strategy 68786 --foresight 3 --prefix pre1  --learning 0.1 --hyper 0.0 --cool 0.1
python3 weight_matrix_creator.py --target prediction --strategy 68786 --foresight 3 --prefix pre2 --learning 0.05 --hyper 0.0 --cool 0.1
python3 weight_matrix_creator.py --target prediction --strategy 68786 --foresight 3 --prefix pre3 --learning 0.1 --hyper 0.0 --cool 0.05
python3 weight_matrix_creator.py --target prediction --strategy 666 --foresight 8 --prefix longview1  --learning 0.1 --hyper 0.0 --cool 0.1
python3 weight_matrix_creator.py --target prediction --strategy 666 --foresight 8 --prefix longview2 --learning 0.05 --hyper 0.0 --cool 0.1
python3 weight_matrix_creator.py --target prediction --strategy 666 --foresight 8 --prefix longview3 --learning 0.1 --hyper 0.0 --cool 0.05
python3 weight_matrix_creator.py --target prediction --strategy 6z6 --foresight 3 --prefix wide1  --learning 0.1 --hyper 0.0 --cool 0.1
python3 weight_matrix_creator.py --target prediction --strategy 6z6 --foresight 3 --prefix wide2 --learning 0.05 --hyper 0.0 --cool 0.1
python3 weight_matrix_creator.py --target prediction --strategy 6z6 --foresight 3 --prefix wide3 --learning 0.1 --hyper 0.0 --cool 0.05
python3 weight_matrix_creator.py --target reverse --prefix rev --strategy 666 --foresight 8 