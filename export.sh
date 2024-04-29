#!/bin/bash

# NUM_EPOCHS=3
# TRAIN_DATA=data/poland1.yaml
# IMG_SIZE=1280
# #IMG_SIZE=640
# #TRAIN_CFG=yolov7.yaml
# TRAIN_CFG=yolov7-tiny.yaml
# TRAIN_WTS=yolov7_training.pt
# RUN_NAME=poland1b_det

echo "running model export to ONNX"

#python train.py --img-size $IMG_SIZE --cfg cfg/training/$TRAIN_CFG --hyp data/hyp.scratch.custom.yaml --batch 8 --epochs $NUM_EPOCHS --data $TRAIN_DATA --weights $TRAIN_WTS --workers 24 --name $RUN_NAME

python export.py --weights runs/train/poland1b_det2/weights/best.pt --grid --end2end --simplify --topk-all 100 --iou-thres 0.65 --conf-thres 0.35 --img-size 640 640 --max-wh 640

echo "done"
exit 0
