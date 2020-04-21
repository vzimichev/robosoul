#!/bin/sh
echo "Launching learn_on_storage.sh with folowing variables:"
echo "CI_LOS:\t$CI_LOS"
echo "OUT_DIR:\t$OUT_DIR"

set -e
files=`ls $OUT_DIR | wc -l`

if [ "$files" -eq 0 ] 
then
    echo "Storage folder is empty."
else
    if [ "$CI_LOS" = "true" ]
    then 
        echo "Found $files files at storage folder."
        FILES=$OUT_DIR/*
        chmod -c 777 $OUT_DIR/* > chmod.log
        for filename in $FILES
        do
    	    tmp=`echo "$filename" | cut -d'.' -f1`
            if [ "$launch" = "$tmp" ]
            then
                continue
            else
        	    python3 changer.py --name $tmp
                python3 neuro_compiler.py -t prediction 
                python3 backprop.py -t prediction
                python3 neuro_compiler.py -p rev
                python3 backprop.py -p rev --learning 0.05 --hyper 0.03 --cool 0.1
            fi
        done
        python3 changer.py
    else 
    if [ "$CI_LOS" = "erase" ]
    then
        rm $OUT_DIR/*
        echo "Storage folder become empty."
    else
        continue
    fi
    fi
fi
