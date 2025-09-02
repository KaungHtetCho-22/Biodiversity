#!/bin/bash

NAME=biodiversity_docker

MAIN_DIR=$(realpath "`dirname $0`/../")

NETWORK="host"

CMD="/bin/bash"
WORKDIR="/home/work"

docker run -it --rm --gpus all \
    -e PLATFORM=$ENV_PLATFORM \
    -p 5000:5000 \
    --network $NETWORK \
    -v $MAIN_DIR:/home/work \
    --shm-size 16G \
    --workdir $WORKDIR \
    --name $NAME \
    $NAME \
    $CMD


