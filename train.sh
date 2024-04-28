#!/bin/bash

NUM_EPOCHS=3
TRAIN_DATA=data/test2-data.yaml
TRAIN_CFG=yolov7.yaml
#TRAIN_CFG=yolov7-tiny.yaml
TRAIN_WTS=yolov7_training.pt
RUN_NAME=test2a_det

echo "running model training"

python train.py --img-size 640 --cfg cfg/training/$TRAIN_CFG --hyp data/hyp.scratch.custom.yaml --batch 8 --epochs $NUM_EPOCHS --data $TRAIN_DATA --weights $TRAIN_WTS --workers 24 --name $RUN_NAME

echo "done"
exit 0
