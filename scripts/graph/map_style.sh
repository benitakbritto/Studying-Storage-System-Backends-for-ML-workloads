#!/bin/sh
BLUE='\033[0;44m'
NOCOLOR='\033[0m'

# Constants
INPUTFILE=/mnt/data/dataset/fb15k-237/train.txt
INPUTFILESIZE=1
TYPE=m
WORKLOAD=graph
ITR=1

# RocksDB
DS=rd

for workers in $(seq 0 8 32)
do
    WORKERS=$workers
    rowsperkeysize=1
    for i in $(seq 0 1 10)
    do
        ROWSPERKEY=$rowsperkeysize
        batchsize=1
        for j in $(seq 0 1 10)
        do
            BATCHSIZE=$batchsize
            OUTPUTFILE="../../output/${DS}/${WORKLOAD}/i${INPUTFILESIZE}_w${WORKERS}_r${ROWSPERKEY}_t${TYPE}_b${BATCHSIZE}"
            
            echo "${BLUE} DS=${DS}, WORKLOAD=${WORKLOAD}, WORKERS=${WORKERS}, TYPE=${TYPE}, ROWSPERKEY=${ROWSPERKEY}, BATCHSIZE=${BATCHSIZE} ${NOCOLOR}"
            python ../../$WORKLOAD/main.py -ds $DS -input-file $INPUTFILE -num-workers $WORKERS -input-rows-per-key $ROWSPERKEY -type $TYPE -batch-size $BATCHSIZE > $OUTPUTFILE
            
            # go to next batch size
            batchsize=$(( $batchsize*2 ))
        done

        # go to next rows per key size
        rowsperkeysize=$(( $rowsperkeysize*2 ))
    done
done

# TileDB
DS=td
ROWSPERKEY=1
for workers in $(seq 0 8 32)
do 
    WORKERS=$workers
    batchsize=1
    for i in $(seq 0 1 10)
    do
        BATCHSIZE=$batchsize
        OUTPUTFILE="../../output/${DS}/${WORKLOAD}/i${INPUTFILESIZE}_w${WORKERS}_r${ROWSPERKEY}_t${TYPE}_b${BATCHSIZE}"
        
        echo "${BLUE} DS=${DS}, WORKLOAD=${WORKLOAD}, WORKERS=${WORKERS}, TYPE=${TYPE}, ROWSPERKEY=${ROWSPERKEY}, BATCHSIZE=${BATCHSIZE} ${NOCOLOR}"
        python ../../$WORKLOAD/main.py -ds $DS -input-file $INPUTFILE -num-workers $WORKERS -input-rows-per-key $ROWSPERKEY -type $TYPE -batch-size $BATCHSIZE > $OUTPUTFILE
        
        # go to next batch size
        batchsize=$(( $batchsize*2 ))
    done
done
    
# Tensorstore
DS=td
ROWSPERKEY=1
for workers in $(seq 0 8 32)
do 
    WORKERS=$workers
    batchsize=1
    for i in $(seq 0 1 10)
    do
        BATCHSIZE=$batchsize
        OUTPUTFILE="../../output/${DS}/${WORKLOAD}/i${INPUTFILESIZE}_w${WORKERS}_r${ROWSPERKEY}_t${TYPE}_b${BATCHSIZE}"
        
        echo "${BLUE} DS=${DS}, WORKLOAD=${WORKLOAD}, WORKERS=${WORKERS}, TYPE=${TYPE}, ROWSPERKEY=${ROWSPERKEY}, BATCHSIZE=${BATCHSIZE} ${NOCOLOR}"
        python ../../$WORKLOAD/main.py -ds $DS -input-file $INPUTFILE -num-workers $WORKERS -input-rows-per-key $ROWSPERKEY -type $TYPE -batch-size $BATCHSIZE > $OUTPUTFILE
        
        # go to next batch size
        batchsize=$(( $batchsize*2 ))
    done
done