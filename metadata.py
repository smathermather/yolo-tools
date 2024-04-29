# ---------------------------------------------
# metadata.py
#
# For setting metadata on an ONNX model, 
# used by the Deepness plugin.
# ---------------------------------------------

import json
import onnx

model_path = "runs/train/poland1b_det2/weights/test.onnx"
#model = onnx.load('deeplabv3_landcover_4c.onnx')
model = onnx.load(model_path)

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
m3.value = json.dumps(50)

# optional, if you want to standarize input after normalisation
# m4 = model.metadata_props.add()
# m4.key = 'standardization_mean'
# m4.value = json.dumps([0.0, 0.0, 0.0])

# m5 = model.metadata_props.add()
# m5.key = 'standardization_std'
# m5.value = json.dumps([1.0, 1.0, 1.0])

onnx.save(model, model_path)

print("Done")