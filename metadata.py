# ---------------------------------------------
# metadata.py
#
# For setting metadata on an ONNX model, 
# used by the Deepness plugin.
# ---------------------------------------------

import json
import onnx
import os
import argparse
import sys

# Ensures parameters entered meet the count necessary to assign all fields
if __name__ == "__main__":
    #Describes the program's usage and gives an example of usage
    parser = argparse.ArgumentParser(description="This program intakes information from the assigned input path, processes it, assigning class names, and sends it to the output path.")
    parser.add_argument('-input', '--input-model-path', type=str, required=True, help="Accepts the Input Path")
    parser.add_argument('-output', '--output-path', type=str, required=True, help= "Accepts the Output Path")
    parser.add_argument('-class', '--class-names', type=str, nargs= '*', required=True, help="Takes in class names separated by commas. IE. term,new_term,third_term")
    args = parser.parse_args()

    # Assigns params entered into the terminal to the variables used in the program
    input_model_path = args.input_model_path
    output_path = args.output_path
    class_inputs = ''.join(args.class_names).split(',') # creates a list of the individual elements given in the --class_names input 

    # Prints a confirmation message of the params entered
    print('Input Path is:', input_model_path + '\nOutput Path is:', output_path +'\nClass Names are:', class_inputs)
    


#model_path = "runs/train/poland1b_det2/weights/best.onnx"
#model = onnx.load('deeplabv3_landcover_4c.onnx')
#model_path = "runs/train/poland1-100_det/weights/best.onnx"
#model = onnx.load(model_path)
model = onnx.load(input_model_path)

# Builds a class_names dictionary using Key, Value pairs of the index for each element in class_inputs and the list element itself
class_names = {}
for index, element in enumerate(class_inputs):
    class_names[index] = element

# Prints a confirmation of the class_names dictionary
print ('Class Dictionary:', class_names)


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
