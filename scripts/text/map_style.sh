#!/bin/sh
BLUE='\033[0;44m'
NOCOLOR='\033[0m'

# Constants
INPUTFILE=/mnt/data/dataset/twitter/twitter_sentiment_dataset.csv
INPUTFILESIZE=1
TYPE=m
WORKLOAD=text
ITR=1

# RocksDB
DS=rd
for workers in 0 8 16 32
do
    WORKERS=$workers
    for rowsperkeysize in 1 128 256 512 1024
    do
        ROWSPERKEY=$rowsperkeysize
        WRITE=1
        for batchsize in 128 256 512 1024
        do
            BATCHSIZE=$batchsize
            OUTPUTFILE="../output/${DS}/${WORKLOAD}/i${INPUTFILESIZE}_w${WORKERS}_r${ROWSPERKEY}_t${TYPE}_b${BATCHSIZE}"
            
            echo "${BLUE} DS=${DS}, WORKLOAD=${WORKLOAD}, WORKERS=${WORKERS}, TYPE=${TYPE}, ROWSPERKEY=${ROWSPERKEY}, BATCHSIZE=${BATCHSIZE} ${NOCOLOR}"
            if [ $WRITE -eq 1 ]
            then
                python ../$WORKLOAD/main.py -ds $DS -input-file $INPUTFILE -num-workers $WORKERS -input-rows-per-key $ROWSPERKEY -type $TYPE -batch-size $BATCHSIZE > $OUTPUTFILE
                WRITE=0
            else 
                python ../$WORKLOAD/main.py -ds $DS -input-file $INPUTFILE -num-workers $WORKERS -input-rows-per-key $ROWSPERKEY -type $TYPE -batch-size $BATCHSIZE -skip-write True > $OUTPUTFILE
            fi
        done
    done
done

# TileDB
DS=td
ROWSPERKEY=1
WRITE=1
for workers in 0 8 16 32
do 
    WORKERS=$workers
    for batchsize in 128 256 512 1024
    do
        BATCHSIZE=$batchsize
        OUTPUTFILE="../output/${DS}/${WORKLOAD}/i${INPUTFILESIZE}_w${WORKERS}_r${ROWSPERKEY}_t${TYPE}_b${BATCHSIZE}"
        
        echo "${BLUE} DS=${DS}, WORKLOAD=${WORKLOAD}, WORKERS=${WORKERS}, TYPE=${TYPE}, ROWSPERKEY=${ROWSPERKEY}, BATCHSIZE=${BATCHSIZE} ${NOCOLOR}"
        if [$WRITE -eq 1 ]
        then
            python ../$WORKLOAD/main.py -ds $DS -input-file $INPUTFILE -num-workers $WORKERS -input-rows-per-key $ROWSPERKEY -type $TYPE -batch-size $BATCHSIZE > $OUTPUTFILE
            WRITE=0
        else 
            python ../$WORKLOAD/main.py -ds $DS -input-file $INPUTFILE -num-workers $WORKERS -input-rows-per-key $ROWSPERKEY -type $TYPE -batch-size $BATCHSIZE -skip-write True > $OUTPUTFILE
        fi
    done
done
    
# Tensorstore
DS=ts
ROWSPERKEY=1
WRITE=1
for workers in 0 8 16 32
do 
    WORKERS=$workers
    for batchsize in 128 256 512 1024
    do
        BATCHSIZE=$batchsize
        OUTPUTFILE="../output/${DS}/${WORKLOAD}/i${INPUTFILESIZE}_w${WORKERS}_r${ROWSPERKEY}_t${TYPE}_b${BATCHSIZE}"
        
        echo "${BLUE} DS=${DS}, WORKLOAD=${WORKLOAD}, WORKERS=${WORKERS}, TYPE=${TYPE}, ROWSPERKEY=${ROWSPERKEY}, BATCHSIZE=${BATCHSIZE} ${NOCOLOR}"
        if [ $WRITE -eq 1 ]
        then
            python ../$WORKLOAD/main.py -ds $DS -input-file $INPUTFILE -num-workers $WORKERS -input-rows-per-key $ROWSPERKEY -type $TYPE -batch-size $BATCHSIZE > $OUTPUTFILE
            WRITE=0
        else 
            python ../$WORKLOAD/main.py -ds $DS -input-file $INPUTFILE -num-workers $WORKERS -input-rows-per-key $ROWSPERKEY -type $TYPE -batch-size $BATCHSIZE -skip-write True > $OUTPUTFILE
        fi
    done
done

# Baseline
# DS=base
# ROWSPERKEY=1
# for workers in 0 8 16 32
# do 
#     WORKERS=$workers
#     for batchsize in 128 256 512 1024
#     do
#         BATCHSIZE=$batchsize
#         OUTPUTFILE="../output/${DS}/${WORKLOAD}/i${INPUTFILESIZE}_w${WORKERS}_r${ROWSPERKEY}_t${TYPE}_b${BATCHSIZE}"
        
#         echo "${BLUE} DS=${DS}, WORKLOAD=${WORKLOAD}, WORKERS=${WORKERS}, TYPE=${TYPE}, ROWSPERKEY=${ROWSPERKEY}, BATCHSIZE=${BATCHSIZE} ${NOCOLOR}"
#         python ../$WORKLOAD/baseline_map.py  -input-file $INPUTFILE -num-workers $WORKERS -input-rows-per-key $ROWSPERKEY -type $TYPE -batch-size $BATCHSIZE > $OUTPUTFILE
            
#     done
# done