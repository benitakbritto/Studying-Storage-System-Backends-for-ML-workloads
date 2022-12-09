#!/bin/sh
BLUE='\033[0;44m'
NOCOLOR='\033[0m'

# Constants
INPUTFILE=/mnt/data/dataset/twitter/twitter_sentiment_dataset.csv
ITR=1
WORKLOAD=TEXT
WRITE=1
TYPE=m
DS=base
ROWSPERKEY=1

# Map style
for workers in 0 8 16 32
do 
    WORKERS=$workers
    for batchsize in 128 256 512 1024
    do
        BATCHSIZE=$batchsize
        OUTPUTFILE="../output/${DS}/${WORKLOAD}/i${INPUTFILESIZE}_w${WORKERS}_r${ROWSPERKEY}_t${TYPE}_b${BATCHSIZE}"
        
        echo "${BLUE} DS=${DS}, WORKLOAD=${WORKLOAD}, WORKERS=${WORKERS}, TYPE=${TYPE}, ROWSPERKEY=${ROWSPERKEY}, BATCHSIZE=${BATCHSIZE} ${NOCOLOR}"
        python ../$WORKLOAD/baseline_map.py  -input-file $INPUTFILE -num-workers $WORKERS -batch-size $BATCHSIZE > $OUTPUTFILE
        
    done
done

#TODO Remove this file, use it only to run baseline tests separately

    
# Iterable
TYPE=i
WORKERS=0
ROWSPERKEY=1

for batchsize in 128 256 512 1024
    do
        BATCHSIZE=$batchsize
        OUTPUTFILE="../output/${DS}/${WORKLOAD}/i${INPUTFILESIZE}_w${WORKERS}_r${ROWSPERKEY}_t${TYPE}_b${BATCHSIZE}"
        
        echo "${BLUE} DS=${DS}, WORKLOAD=${WORKLOAD}, WORKERS=${WORKERS}, TYPE=${TYPE}, ROWSPERKEY=${ROWSPERKEY}, BATCHSIZE=${BATCHSIZE} ${NOCOLOR}"
        
        python ../$WORKLOAD/baseline_iterable.py -ds $DS -input-file $INPUTFILE -type $TYPE -batch-size $BATCHSIZE  > $OUTPUTFILE
            
    done