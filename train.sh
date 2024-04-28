#!/bin/bash

NUM_EPOCHS=3
TRAIN_DATA=data/poland1.yaml
IMG_SIZE=1280
#IMG_SIZE=640
#TRAIN_CFG=yolov7.yaml
TRAIN_CFG=yolov7-tiny.yaml
TRAIN_WTS=yolov7_training.pt
RUN_NAME=poland1b_det

echo "running model training"

python train.py --img-size $IMG_SIZE --cfg cfg/training/$TRAIN_CFG --hyp data/hyp.scratch.custom.yaml --batch 8 --epochs $NUM_EPOCHS --data $TRAIN_DATA --weights $TRAIN_WTS --workers 24 --name $RUN_NAME

echo "done"
exit 0
