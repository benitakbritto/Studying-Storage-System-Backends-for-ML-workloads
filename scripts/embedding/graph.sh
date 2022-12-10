BLUE='\033[0;44m'
NOCOLOR='\033[0m'

# Constants
WORKLOAD=graph
DS=td
INPUT_FILE=/mnt/data/embeddings/graph.txt
TYPE=power
DS_SIZE=1024
DS_SIZE_LIMIT=2048
EMBED_SIZE_LIMIT=400
BATCH_SIZE_LIMIT=1024

while [ $DS_SIZE -le $DS_SIZE_LIMIT ]
do 
    EMBED_SIZE=100
    while [ $EMBED_SIZE -le $EMBED_SIZE_LIMIT ]
    do
        BATCH_SIZE=128
        while [ $BATCH_SIZE -le $BATCH_SIZE_LIMIT ]
        do
            OUTPUTFILE="./output/${WORKLOAD}/d${DS_SIZE}_e${EMBED_SIZE}_b${BATCH_SIZE}"
            echo "${BLUE} WORKLOAD=${WORKLOAD}, ds_size=${DS_SIZE}, EMBED_SIZE=${EMBED_SIZE}, BATCH_SIZE=${BATCH_SIZE} ${NOCOLOR}"
            python ../../embedding/main.py -ds-size $DS_SIZE -ds $DS -batch-size $BATCH_SIZE -embed-size $EMBED_SIZE -input-file $INPUT_FILE -type $TYPE > $OUTPUTFILE
        BATCH_SIZE=$((BATCH_SIZE * 2))
        done
    EMBED_SIZE=$((EMBED_SIZE + 100))
    done
    DS_SIZE=$((DS_SIZE * 2))
done