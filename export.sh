#!/bin/bash
# ---------------------------------------------------------------------------
# export.sh
#
# For exporting a trained yolov7 model to ONNX format, and applying
# metadata necessary for use in QGIS Deepness plugin.
# ---------------------------------------------------------------------------

# Function to display usage/help message
usage() {
    echo "Usage: $0 -r <RUN_NAME> -w <INPUT_WEIGHTS> -s <IMG_SIZE>"
    exit 1
}

# Check if help option is provided
if [[ "$*" == *"--help"* ]] || [[ "$*" == *"-h"* ]]; then
    usage
fi

SCRIPTS_DIR=$(dirname "$0")

# Loops through command line options and their arguments storing the arguments for later use.
while getopts ':r:w:s:' opt; do
	case $opt in
		r) RUN_NAME="$OPTARG"
		;;
		w) INPUT_WEIGHTS="$OPTARG"
		;;
		s) IMG_SIZE="$OPTARG"
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
if [[ -z $RUN_NAME || -z $INPUT_WEIGHTS || -z $IMG_SIZE ]]; then
    echo "Error: Missing required options."
    usage
fi

# Prints confirmation lines to the terminal expressing the -r option, -w option, and -s option arguments that have been assigned
printf "Argument RUN_NAME is %s\n" "$RUN_NAME"
printf "Argument INPUT_WEIGHTS is %s\n" "$INPUT_WEIGHTS"
printf "Argument IMG_SIZE is %s\n" "$IMG_SIZE"

#RUN_NAME=mckellar-1_100ep_det
#RUN_NAME=poland1-100_det
#INPUT_WEIGHTS=runs/train/$RUN_NAME/weights/best.pt
#INPUT_WEIGHTS=runs/train/poland1-100_det/weights/best.pt
# poland 1216(1200) / mckellar-1 896(900)
#IMG_SIZE=1216
#IMG_SIZE=640
#IMG_SIZE=896

echo "Exporting model"

python export.py --weights $INPUT_WEIGHTS --grid --simplify --img-size $IMG_SIZE $IMG_SIZE

echo "Setting metadata"

python $SCRIPTS_DIR/metadata.py runs/train/$RUN_NAME/weights/best.onnx runs/train/$RUN_NAME/weights/$RUN_NAME-yolo7-deepness.onnx

echo "done"
exit 0
