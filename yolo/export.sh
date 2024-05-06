#!/bin/bash
# ---------------------------------------------------------------------------
# export.sh
#
# For exporting a trained yolov7 model to ONNX format, and applying
# metadata necessary for use in QGIS Deepness plugin.
# ---------------------------------------------------------------------------

#INPUT_WEIGHTS=runs/train/poland1-100_det/weights/best.pt
INPUT_WEIGHTS=runs/train/mekellar-1_3ep_det/weights/best.pt
#TRAIN_DATA=data/mckellar-1.yaml
# poland 1216(1200) / mckellar-1 896(900)
#IMG_SIZE=1280
#IMG_SIZE=640
IMG_SIZE=896
#TRAIN_CFG=yolov7.yaml
TRAIN_CFG=yolov7-tiny.yaml
TRAIN_WTS=yolov7_training.pt
RUN_NAME=mekellar-1_3ep_det

echo "Exporting model"
python export.py --weights $INPUT_WEIGHTS --grid --simplify --img-size $IMG_SIZE $IMG_SIZE

#echo "Setting metadata"
python metadata.py runs/train/mekellar-1_3ep_det/weights/best.onnx runs/train/mekellar-1_3ep_det/weights/mckellar1_3ep_detection_yolo7_ITCVD_deepness.onnx

echo "done"
exit 0
