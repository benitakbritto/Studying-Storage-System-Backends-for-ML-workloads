#!/bin/bash

# ./run.sh <WORKLOAD> <DATASTORE>
TEXT_DATASET_PATH='/mnt/data/dataset/twitter/twitter_sentiment_dataset.csv'
IMAGE_DATASET_PATH='/mnt/data/dataset/cifar/'
GRAPH_DATASET_PATH='/mnt/data/dataset/fb15k-237/train.txt'

WORKLOAD=$1
DS=$2

# ------------------- TEXT ------------------- 
if [ "$WORKLOAD" == "TEXT" ]
then 
    echo "TEXT WORKLOAD"
    # Baseline
    if [ "$DS" == "BASE" ]
    then 
        echo "BASE DATASTORE"
        for itr in $(seq 1 1 20)
        do
            python ../text/main.py -input-file $TEXT_DATASET_PATH -ds base -type i -num-workers 0 -batch-size 1024 -skip-write True
        done 
    # RD
    elif [ "$DS" == "RD" ]
    then 
        echo "RD DATASTORE"
        for itr in $(seq 1 1 20)
        do
            python ../text/main.py -input-file $TEXT_DATASET_PATH -ds rd -type m -input-rows-per-key 1024 -batch-size 1024 -num-workers 32 -skip-write True
        done 

    # TD
    elif [ "$DS" == "TD" ]
    then 
        echo "TD DATASTORE"
        for itr in $(seq 1 1 20)
        do 
            python ../text/main.py -input-file $TEXT_DATASET_PATH -ds td -type i -batch-size 1024 -num-workers 16 -pf 1024 -skip-write True
        done

    # TS
    elif [ "$DS" == "TS" ]
    then 
        echo "TS DATASTORE"
        for itr in $(seq 1 1 20)
        do
            python ../text/main.py -input-file $TEXT_DATASET_PATH -ds ts -type m -batch-size 1024 -num-workers 32
        done
    fi

# ------------------- IMAGE -------------------
elif [ "$WORKLOAD" == "IMAGE" ]
then 
    echo "IMAGE WORKLOAD"
    # Baseline
    if [ "$DS" == "BASE" ]
    then 
        echo "BASE DATASTORE"
        for itr in $(seq 1 1 20)
        do
            python ../image/main.py -input-file $IMAGE_DATASET_PATH -ds base -type m -batch-size 256 -num-workers 32 -skip-write True
        done 

    # RD
    elif [ "$DS" == "RD" ]
    then 
        echo "RD DATASTORE"
        for itr in $(seq 1 1 20)
        do
            python ../image/main.py -input-file $IMAGE_DATASET_PATH -ds rd -type m -batch-size 1024 -num-workers 16 -input-rows-per-key 128 -skip-write True
        done 

    # TD
    elif [ "$DS" == "TD" ]
    then 
        echo "TD DATASTORE"
        for itr in $(seq 1 1 20)
        do 
            python ../image/main.py -input-file $IMAGE_DATASET_PATH -ds td -type i -batch-size 512 -num-workers 32 -pf 512 -skip-write True
        done

    # TS
    elif [ "$DS" == "TS" ]
    then 
        echo "TS DATASTORE"
        for itr in $(seq 1 1 20)
        do
            python ../image/main.py -input-file $IMAGE_DATASET_PATH -ds ts -type i -batch-size 512 -num-workers 16 -pf 1024
        done
    fi

# ------------------- GRAPH -------------------
elif [ "$WORKLOAD" == "GRAPH" ]
then 
    echo "GRAPH WORKLOAD"
    # Baseline
    if [ "$DS" == "BASE" ]
    then 
        echo "BASE DATASTORE"
        for itr in $(seq 1 1 20)
        do
            python ../graph/main.py -input-file $GRAPH_DATASET_PATH -ds base -type i -batch-size 512 -num-workers 0 -skip-write True
        done 

    # RD
    elif [ "$DS" == "RD" ]
    then 
        echo "RD DATASTORE"
        for itr in $(seq 1 1 20)
        do
            python ../graph/main.py -input-file $GRAPH_DATASET_PATH -ds rd -type m -batch-size 1024 -num-workers 16 -input-rows-per-key 1024 -skip-write True
        done 

    # TD
    elif [ "$DS" == "TD" ]
    then 
        echo "TD DATASTORE"
        for itr in $(seq 1 1 20)
        do 
            python ../graph/main.py -input-file $GRAPH_DATASET_PATH -ds td -type i -batch-size 512 -num-workers 16 -pf 1024 -skip-write True
        done

    # TS
    elif [ "$DS" == "TS" ]
    then 
        echo "TS DATASTORE"
        for itr in $(seq 1 1 20)
        do
            python ../graph/main.py -input-file $GRAPH_DATASET_PATH -ds ts -type m -batch-size 1024 -num-workers 8
        done
    fi
fi