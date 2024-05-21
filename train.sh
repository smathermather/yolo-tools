#!/bin/bash

# Function to display usage/help message
usage() {
    echo "Usage: $0 -n <NUM_EPOCHS> -s <IMG_SIZE> -d <TRAIN_DATA> -c <TRAIN_CFG> -w <TRAIN_WTS> -r <RUN_NAME>"
    exit 1
}

# Check if help option is provided
if [[ "$*" == *"--help"* ]] || [[ "$*" == *"-h"* ]]; then
    usage
fi


while getopts ':n:s:d:c:w:r:' opt; do
	case $opt in
		n) NUM_EPOCHS="$OPTARG"
		;;
		s) IMG_SIZE="$OPTARG"
		;;
		d) TRAIN_DATA="$OPTARG"
		;;
		c) TRAIN_CFG="$OPTARG"
		;;
		w) TRAIN_WTS="$OPTARG"
		;;
		r) RUN_NAME="$OPTARG"
		;;
		\?) echo "Invalid Option at -$OPTARG" >&2
		exit 1
		;;
	esac
	case $OPTARG in
		-*) echo "$opt requires a valid argument"
		usage
		;;

	esac
done

# Check if required options are provided
if [[ -z $NUM_EPOCHS || -z $IMG_SIZE  || -z $TRAIN_DATA || -z $TRAIN_CFG || -z $TRAIN_WTS || -z $RUN_NAME ]]; then
    echo "Error: Missing required options."
    usage
fi

#NUM_EPOCHS=3
#NUM_EPOCHS=100
#TRAIN_DATA=data/neill-2.yaml
#TRAIN_DATA=data/test1.yaml
#IMG_SIZE=1280
#IMG_SIZE=640
#IMG_SIZE=896
#TRAIN_CFG=yolov7.yaml
#TRAIN_CFG=yolov7-tiny.yaml
#TRAIN_WTS=yolov7_training.pt
#RUN_NAME=test1_3ep_det

echo "running model training"

python train.py --img-size $IMG_SIZE --cfg cfg/training/$TRAIN_CFG --hyp data/hyp.scratch.custom.yaml --batch 8 --epochs $NUM_EPOCHS --data $TRAIN_DATA --weights $TRAIN_WTS --workers 24 --name $RUN_NAME

echo "done"
exit 0
