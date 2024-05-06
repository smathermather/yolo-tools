# ---------------------------------------------
# metadata.py
#
# For setting metadata on an ONNX model, 
# used by the Deepness plugin.
# ---------------------------------------------

import json
import onnx
import os
import sys

# Ensures parameters entered meet the count necessary to assign all fields and none are of type 'str'
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print ("\nParameter Count Does Not Meet Requirements: \n")
        print ("Usage: metadata.py <input_model_path> <output_path>\n")
        sys.exit(1)

# params to be entered in the command line and converted to integers for use in functions
input_model_path = sys.argv[1]
output_path = sys.argv[2]

#model_path = "runs/train/poland1b_det2/weights/best.onnx"
#model = onnx.load('deeplabv3_landcover_4c.onnx')
#model_path = "runs/train/poland1-100_det/weights/best.onnx"
#model = onnx.load(model_path)
model = onnx.load(input_model_path)

class_names = {
    0: 'bird'
}

m1 = model.metadata_props.add()
m1.key = 'model_type'
m1.value = json.dumps('Detector')

m2 = model.metadata_props.add()
m2.key = 'class_names'
m2.value = json.dumps(class_names)

m3 = model.metadata_props.add()
m3.key = 'resolution'
m3.value = json.dumps(10)

m4 = model.metadata_props.add()
m4.key = 'tiles_overlap'
m4.value = json.dumps(10)

m5 = model.metadata_props.add()
m5.key = 'det_conf'
m5.value = json.dumps(0.3)

m6 = model.metadata_props.add()
m6.key = 'det_iou_thresh'
m6.value = json.dumps(0.7)

#export_path = os.path.abspath("runs/train/poland1-100_det/weights/poland1-100_detection_yolo7_ITCVD_deepness.onnx")
export_path = os.path.abspath(output_path)
onnx.save(model, export_path)

print("Done, your ONNX model with metadata is at: ", export_path)