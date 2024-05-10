# convert-new.py
#
# For converting bbox annotations in Weinstein et al to YOLOv5 format.
# Weinstein training data bbox annotations are all in one file.  This 
# script creates one file per image, as expected by YOLOv5.
#
# Paper: https://www.biorxiv.org/content/10.1101/2021.08.05.455311v1.full
# Data: https://zenodo.org/records/5033174 
#
# Some functions drawn from Paperspace Blog - https://blog.paperspace.com/train-yolov7-custom-data/

import csv
import os
import sys
from tqdm import tqdm

# Field definitions - select the list that matches the annotations input file
class_id = 0    # alway 0, as we will only have one class: "Bird"

# Ensures parameters entered meet the count necessary to assign all fields and none are of type 'str'
if __name__ == "__main__":
    if len(sys.argv) != 9:
        print ("\nParameter Count Does Not Meet Requirements: \n")
        print ("Usage: convert-new.py <image_height> <image_width> <field_image> <header_row> <field_xmin> <fiel_y_min> <field_xmax> <field_ymax>\n")
        sys.exit(1)
    elif any(isinstance(x, str) for x in sys.argv):
        print ("\nApplication Does Not Accept type 'str' Parameters. \n")

# params to be entered in the command line and converted to integers for use in functions
image_height = int(sys.argv[1])
image_width = int(sys.argv[2])
field_image = int(sys.argv[3])
header_row = int(sys.argv[4]) 
field_xmin = int(sys.argv[5])
field_ymin = int(sys.argv[6])
field_xmax = int(sys.argv[7])
field_ymax = int(sys.argv[8])


#TODO add other field definitions for other input files

# Read and parse annotations data
def extract_annotations(csv_file):
    print ("\nExtracting file: " + csv_file)

    with open(csv_file) as fp:
        reader = csv.reader(fp, delimiter=",", quotechar='"')
        if (header_row):
            next(reader, None)  # use this to skip the headers
        data_read = [row for row in reader]

    return data_read

# Convert items to per-image files
#
# Target format is one file per image, containing one or more bbox records (one line per bbox)
#
def convert_to_yolov5(info_dict):
    files = {}
    last_file_name = ""
    print("Converting records, total: ", len(info_dict))
    for one_record in info_dict:
        file_name = one_record[field_image]
        if (last_file_name != file_name):
            files[file_name] = []
            last_file_name = file_name

        # convert to yolo values
        b_center_x = (float(one_record[field_xmin]) + float(one_record[field_xmax])) / 2 
        b_center_y = (float(one_record[field_ymin]) + float(one_record[field_ymax])) / 2
        b_width    = (float(one_record[field_xmax]) - float(one_record[field_xmin]))
        b_height   = (float(one_record[field_ymax]) - float(one_record[field_ymin]))

        # normalize to dimensions of the image
        b_center_x /= image_width 
        b_center_y /= image_height 
        b_width    /= image_width 
        b_height   /= image_height 

        # add to data list
        bbox = [class_id, b_center_x, b_center_y, b_width, b_height]
        files[file_name].append(bbox)

    return files

# Write the yolov5 format annotation files
def write_yolov5(file_dict):
    print("Writing files, total: ", len(file_dict))

    for one_record in file_dict:
        print_buffer = []
        rows = file_dict[one_record]
        for one_row in rows:
            print_buffer.append("{} {:.3f} {:.3f} {:.3f} {:.3f}".format(one_row[0], one_row[1], one_row[2], one_row[3], one_row[4]))

        out_file_path = "out/converted/" + one_record.replace("png", "txt")
        print("\n".join(print_buffer), file= open(out_file_path, "w"))


# ------------------- Main Execution -------------------------------------------------------------


print("Converting annotations from Weinstein et al research data")

# Prepare output directory
if not os.path.exists('out/converted'):
    os.mkdir('out/converted')


# Read input annotations
annotations = [os.path.join('in/annotations', x) for x in os.listdir('in/annotations') if x[-3:] == "csv"]
annotations.sort()

# Convert and save each
for ann in tqdm(annotations):
    #print("  file: " + ann)
    info_dict = extract_annotations(ann)
    file_dict = convert_to_yolov5(info_dict)
    write_yolov5(file_dict)

print("Done")

