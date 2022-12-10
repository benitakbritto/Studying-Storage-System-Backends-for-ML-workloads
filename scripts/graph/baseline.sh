#!/bin/sh
BLUE='\033[0;44m'
NOCOLOR='\033[0m'

# Constants
INPUTFILE=/mnt/data/dataset/fb15k-237/train.txt
INPUTFILESIZE=1
TYPE=m
WORKLOAD=graph
ITR=1
DS=base
ROWSPERKEY=1
WORKERS=0

# Baseline iterable
TYPE=i
for batchsize in 128 256 512 1024
do
    BATCHSIZE=$batchsize
    OUTPUTFILE="../output/${DS}/${WORKLOAD}/i${INPUTFILESIZE}_w${WORKERS}_r${ROWSPERKEY}_t${TYPE}_b${BATCHSIZE}"
    
    echo "${BLUE} DS=${DS}, WORKLOAD=${WORKLOAD}, WORKERS=${WORKERS}, TYPE=${TYPE}, ROWSPERKEY=${ROWSPERKEY}, BATCHSIZE=${BATCHSIZE}, ${NOCOLOR}"
    python ../$WORKLOAD/main.py -ds $DS -input-file $INPUTFILE -type $TYPE -batch-size $BATCHSIZE > $OUTPUTFILE
done

# Baseline map
TYPE=m
for batchsize in 128 256 512 1024
do
    BATCHSIZE=$batchsize
    OUTPUTFILE="../output/${DS}/${WORKLOAD}/i${INPUTFILESIZE}_w${WORKERS}_r${ROWSPERKEY}_t${TYPE}_b${BATCHSIZE}"
    
    echo "${BLUE} DS=${DS}, WORKLOAD=${WORKLOAD}, WORKERS=${WORKERS}, TYPE=${TYPE}, ROWSPERKEY=${ROWSPERKEY}, BATCHSIZE=${BATCHSIZE} ${NOCOLOR}"
    python ../$WORKLOAD/main.py -ds $DS -input-file $INPUTFILE -type $TYPE -batch-size $BATCHSIZE > $OUTPUTFILE
done
