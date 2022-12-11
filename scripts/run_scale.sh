#!/bin/sh
BLUE='\033[0;44m'
NOCOLOR='\033[0m'

INPUT_TWITTER=/mnt/data/dataset/twitter/twitter_sentiment_dataset.csv
INPUT_FB15K=/mnt/data/dataset/fb15k-237/train.txt
OUTPUT_TWITTER_PREFIX=/mnt/data/dataset/twitter/twitter_sentiment_dataset
OUTPUT_FB15K_PREFIX=/mnt/data/dataset/fb15k-237/train

# ------------------- TEXT ------------------- 
for size in 2 1 10
do
    INPUT_SIZE=$size
    echo "${BLUE} START INPUTSIZE=${INPUT_SIZE} FOR TEXT ${NOCOLOR}"

    echo "${BLUE} Cleanup ${NOCOLOR}"
    chmod 777 cleanup.sh
    ./cleanup.sh

    echo "${BLUE} Augment dataset ${NOCOLOR}"
    AUG_FILE="${OUTPUT_TWITTER_PREFIX}_${INPUT_SIZE}.csv"
    python ../util/cat_dataset.py  --iterations $size --input-file $INPUT_TWITTER --output-file $AUG_FILE

    # Baseline
    echo "${BLUE} START INPUTSIZE=${INPUT_SIZE} FOR TEXT-Baseline ${NOCOLOR}"
    python ../text/main.py -input-file $AUG_FILE -ds base -num-workers 0 -batch-size 1024 
    # RD
    echo "${BLUE} START INPUTSIZE=${INPUT_SIZE} FOR TEXT-RD ${NOCOLOR}"
    python ../text/main.py -input-file $AUG_FILE -ds rd -type m -input-rows-per-key 1024 -batch-size 1024 -num-workers 32
    # TD - freeze issue
    # echo "${BLUE} START INPUTSIZE=${INPUT_SIZE} FOR TEXT-TD ${NOCOLOR}"
    # python ../text/main.py -input-file $AUG_FILE -ds td -type i -batch-size 1024 -num-workers 16 -pf 1024
    # TS
    echo "${BLUE} START INPUTSIZE=${INPUT_SIZE} FOR TEXT-TS ${NOCOLOR}"
    python ../text/main.py -input-file $AUG_FILE -ds ts -type m -batch-size 1024 -num-workers 32
    echo "${BLUE} COMPLETED INPUTSIZE=${INPUT_SIZE} FOR TEXT ${NOCOLOR}"
done

# ------------------- GRAPH ------------------- 
for size in 2 1 10
do
    INPUT_SIZE=$size
    echo "${BLUE} START INPUTSIZE=${INPUT_SIZE} FOR GRAPH ${NOCOLOR}"

    echo "${BLUE} Cleanup ${NOCOLOR}"
    chmod 777 cleanup.sh
    ./cleanup.sh

    echo "${BLUE} Augment dataset ${NOCOLOR}"
    AUG_FILE="${OUTPUT_TWITTER_PREFIX}_${INPUT_SIZE}.txt"
    python ../util/cat_dataset.py  --iterations $size --input-file $INPUT_FB15K --output-file $AUG_FILE

    # Baseline
    echo "${BLUE} START INPUTSIZE=${INPUT_SIZE} FOR GRAPH-Baseline ${NOCOLOR}"
    python ../graph/main.py -input-file $AUG_FILE -num-workers 0 -batch-size 512 -type i 
    # RD
    echo "${BLUE} START INPUTSIZE=${INPUT_SIZE} FOR GRAPH-RD ${NOCOLOR}"
    python ../graph/main.py -input-file $AUG_FILE -ds rd -type m -input-rows-per-key 1024 -batch-size 1024 -num-workers 16
    # TD - freeze issue
    # echo "${BLUE} START INPUTSIZE=${INPUT_SIZE} FOR GRAPH-TD ${NOCOLOR}"
    # python ../graph/main.py -input-file $AUG_FILE -ds td -type i -batch-size 512 -num-workers 16 -pf 1024
    # TS
    echo "${BLUE} START INPUTSIZE=${INPUT_SIZE} FOR GRAPH-TS ${NOCOLOR}"
    python ../graph/main.py -input-file $AUG_FILE -ds ts -type m -batch-size 1024 -num-workers 8
    echo "${BLUE} COMPLETED INPUTSIZE=${INPUT_SIZE} FOR GRAPH ${NOCOLOR}"
done
