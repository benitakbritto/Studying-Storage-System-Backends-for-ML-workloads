#!/bin/bash
VAR=1

for i in 1 2 3
do
    if [[ $VAR -eq 1 ]]
    then
        echo "var is 1"
        VAR=0
    else
        echo "var is 0"
    fi
done