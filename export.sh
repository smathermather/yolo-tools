#!/bin/bash
# ---------------------------------------------------------------------------
# export.sh
#
# For exporting a trained yolov7 model to ONNX format, and applying
# metadata necessary for use in QGIS Deepness plugin.
# ---------------------------------------------------------------------------

# Function to display usage/help message
usage() {
    echo "Usage: $0 -r <RUN_NAME> -s <IMG_SIZE> -c <CLASS_NAMES>"
    exit 1
}

# Check if help option is provided
if [[ "$*" == *"--help"* ]] || [[ "$*" == *"-h"* ]]; then
    usage
fi

SCRIPTS_DIR=$(dirname "$0")

# Loops through command line options and their arguments storing the arguments for later use.
while getopts ':r:s:c:' opt; do
	case $opt in
		r) RUN_NAME="$OPTARG"
		;;
		s) IMG_SIZE="$OPTARG"
		;;
		c) CLASS_NAMES="$OPTARG"
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
if [[ -z $RUN_NAME || -z $IMG_SIZE || -z $CLASS_NAMES ]]; then
    echo "Error: Missing required options."
    usage
fi

INPUT_WEIGHTS=runs/train/$RUN_NAME/weights/best.pt

# Prints confirmation lines to the terminal expressing the arguments that have been assigned
printf "Argument RUN_NAME is %s\n" "$RUN_NAME"
printf "Argument IMG_SIZE is %s\n" "$IMG_SIZE"
printf "Using INPUT_WEIGHTS: %s\n" "$INPUT_WEIGHTS"

echo "Exporting model"
python export.py --weights $INPUT_WEIGHTS --grid --simplify --img-size $IMG_SIZE $IMG_SIZE

echo "Setting metadata"
python $SCRIPTS_DIR/metadata.py -input runs/train/$RUN_NAME/weights/best.onnx -output runs/train/$RUN_NAME/weights/$RUN_NAME-yolo7-deepness.onnx -class $CLASS_NAMES

echo "done"
exit 0
