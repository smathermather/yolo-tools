#!/bin/bash

NUM_EPOCHS=3
#NUM_EPOCHS=100
#TRAIN_DATA=data/neill-2.yaml
TRAIN_DATA=data/test1.yaml
#IMG_SIZE=1280
#IMG_SIZE=640
IMG_SIZE=896
#TRAIN_CFG=yolov7.yaml
TRAIN_CFG=yolov7-tiny.yaml
TRAIN_WTS=yolov7_training.pt
RUN_NAME=test1_3ep_det

echo "running model training"

python train.py --img-size $IMG_SIZE --cfg cfg/training/$TRAIN_CFG --hyp data/hyp.scratch.custom.yaml --batch 8 --epochs $NUM_EPOCHS --data $TRAIN_DATA --weights $TRAIN_WTS --workers 24 --name $RUN_NAME

echo "done"
exit 0
