#!/bin/sh
cp $CI_PROJECT_DIR/PyUART/* .
python3 matrix_inpreter.py walk
python3 weight_matrix_creator.py --target prediction --strategy $CI_STRATEGY --foresight $CI_FORESIGHT --prefix pre3 --learning 0.3   --hyper $CI_HYPER --cool $CI_COOLDOWN
python3 weight_matrix_creator.py --target prediction --strategy $CI_STRATEGY --foresight $CI_FORESIGHT --prefix pre4 --learning 0.1   --hyper $CI_HYPER --cool $CI_COOLDOWN
python3 weight_matrix_creator.py --target prediction --strategy $CI_STRATEGY --foresight $CI_FORESIGHT --prefix pre5 --learning 0.05  --hyper $CI_HYPER --cool $CI_COOLDOWN
python3 weight_matrix_creator.py --target prediction --strategy $CI_STRATEGY --foresight $CI_FORESIGHT --prefix pre6 --learning 0.01  --hyper $CI_HYPER --cool $CI_COOLDOWN
python3 weight_matrix_creator.py --target prediction --strategy $CI_STRATEGY --foresight $CI_FORESIGHT --prefix pre7 --learning 0.005 --hyper $CI_HYPER --cool $CI_COOLDOWN
python3 weight_matrix_creator.py --target reverse --prefix rev --strategy 666 --foresight 8 