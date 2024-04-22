#!/bin/bash

i=0;

for arg in "$@" 
do
    i=$((i + 1));
    if [ $i == 1 ]
    then
    	MODE=$arg
    fi
    if [ $i == 2 ]
    then
    	TEXT=$arg
    fi
done

python password_tool.py $MODE $TEXT