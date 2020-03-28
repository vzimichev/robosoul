#!/bin/sh
cp $CI_PROJECT_DIR/PyUART/* .
python3 matrix_inpreter.py walk
python3 weight_matrix_creator.py --target prediction --strategy $CI_STRATEGY --foresight $CI_FORESIGHT --prefix pre1  --learning 1 --hyper 0.0 --cool 0.1
python3 weight_matrix_creator.py --target prediction --strategy $CI_STRATEGY --foresight $CI_FORESIGHT --prefix pre2 --learning 0.7 --hyper 0.0 --cool 0.1
python3 weight_matrix_creator.py --target prediction --strategy $CI_STRATEGY --foresight $CI_FORESIGHT --prefix pre3 --learning 0.3 --hyper 0.0 --cool 0.1
python3 weight_matrix_creator.py --target prediction --strategy $CI_STRATEGY --foresight $CI_FORESIGHT --prefix pre4  --learning 0.1 --hyper 0.0 --cool 0.1
python3 weight_matrix_creator.py --target prediction --strategy $CI_STRATEGY --foresight $CI_FORESIGHT --prefix pre5  --learning 0.05 --hyper 0.0 --cool 0.1
python3 weight_matrix_creator.py --target prediction --strategy $CI_STRATEGY --foresight $CI_FORESIGHT --prefix pre6  --learning 0.01 --hyper 0.0 --cool 0.1
python3 weight_matrix_creator.py --target prediction --strategy $CI_STRATEGY --foresight $CI_FORESIGHT --prefix pre7  --learning 0.005 --hyper 0.0 --cool 0.1
python3 weight_matrix_creator.py --target prediction --strategy $CI_STRATEGY --foresight $CI_FORESIGHT --prefix pre8  --learning 0.001 --hyper 0.0 --cool 0.1
python3 weight_matrix_creator.py --target prediction --strategy $CI_STRATEGY --foresight $CI_FORESIGHT --prefix pre9  --learning 0.0005 --hyper 0.0 --cool 0.1
python3 weight_matrix_creator.py --target reverse --prefix rev --strategy 666 --foresight 8 