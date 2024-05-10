#!/bin/bash
# ---------------------------------------------------------------------------
# export.sh
#
# For exporting a trained yolov7 model to ONNX format, and applying
# metadata necessary for use in QGIS Deepness plugin.
# ---------------------------------------------------------------------------

SCRIPTS_DIR=$(dirname "$0")
#RUN_NAME=mckellar-1_100ep_det
RUN_NAME=poland1-100_det
INPUT_WEIGHTS=runs/train/$RUN_NAME/weights/best.pt
#INPUT_WEIGHTS=runs/train/poland1-100_det/weights/best.pt
# poland 1216(1200) / mckellar-1 896(900)
IMG_SIZE=1216
#IMG_SIZE=640
#IMG_SIZE=896

echo "Exporting model"
python export.py --weights $INPUT_WEIGHTS --grid --simplify --img-size $IMG_SIZE $IMG_SIZE

#echo "Setting metadata"
python $SCRIPTS_DIR/metadata.py runs/train/$RUN_NAME/weights/best.onnx runs/train/$RUN_NAME/weights/$RUN_NAME-yolo7-deepness.onnx

echo "done"
exit 0
