#!/bin/sh
set -e
echo "Launching build_initials.sh with folowing variables:"
echo "CI_STRATEGY: $CI_STRATEGY"
echo "CI_FORESIGHT: $CI_FORESIGHT"
echo "CI_HYPER: $CI_HYPER"
echo "CI_COOLDOWN: $CI_COOLDOWN"
chmod -R 777 * >chmod.log
cp PyUART/* .
python matrix_inpreter.py walk
python weight_matrix_creator.py --target prediction --strategy $CI_STRATEGY --foresight $CI_FORESIGHT --prefix pre3 --learning 0.3   --hyper $CI_HYPER --cool $CI_COOLDOWN
python weight_matrix_creator.py --target prediction --strategy $CI_STRATEGY --foresight $CI_FORESIGHT --prefix pre4 --learning 0.1   --hyper $CI_HYPER --cool $CI_COOLDOWN
python weight_matrix_creator.py --target prediction --strategy $CI_STRATEGY --foresight $CI_FORESIGHT --prefix pre5 --learning 0.05  --hyper $CI_HYPER --cool $CI_COOLDOWN
python weight_matrix_creator.py --target prediction --strategy $CI_STRATEGY --foresight $CI_FORESIGHT --prefix pre6 --learning 0.01  --hyper $CI_HYPER --cool $CI_COOLDOWN
python weight_matrix_creator.py --target prediction --strategy $CI_STRATEGY --foresight $CI_FORESIGHT --prefix pre7 --learning 0.005 --hyper $CI_HYPER --cool $CI_COOLDOWN
python weight_matrix_creator.py --target reverse --prefix rev --strategy 667 --foresight 8