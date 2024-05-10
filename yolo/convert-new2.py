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

import argparse
import csv
import os
from tqdm import tqdm

# Field definitions - select the list that matches the annotations input file
class_id = 0    # always 0, as we will only have one class: "Bird"

# Creates an arguments parser allowing User flexiblity in entering variable data 
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='A program that converts image bounding box annotations into the YOLOv5 format')
    parser.add_argument('-height', '--image-height', type=int, default=800, help='Takes the height of the training image')
    parser.add_argument('-width', '--image-width', type=int, default=800, help='Takes the Width of the image')
    parser.add_argument('-image', '--field-image', type=int, default=7, help='CSV field containing the training image file name')
    parser.add_argument('-header', '--header-row', type=int, choices=[0,1], default=1, help='Denotes the presence or absence of a header row in CSV file')
    parser.add_argument('-xmin', '--field-xmin', type=int, default=2, help='CSV field containing the x-axis minimum value')
    parser.add_argument('-ymin', '--field-ymin', type=int, default=3, help='CSV field containing the y-axis minimum value')
    parser.add_argument('-xmax', '--field-xmax', type=int, default=4, help='CSV field containing the x-axis maximum value')
    parser.add_argument('-ymax', '--field-ymax', type=int, default=5, help='CSV field containing the y-axis maximum value')
    
    args = parser.parse_args()


    # Extracts necessary values from user input arguments
    image_height = args.image_height
    image_width = args.image_width
    field_image = args.field_image
    header_row = args.header_row
    field_xmin = args.field_xmin
    field_ymin = args.field_ymin
    field_xmax = args.field_xmax
    field_ymax = args.field_ymax

# -------------------- Examples
# Poland
# $ python convert-new2.py -height=1216 -width=1216 -image=6 -xmin=2 -ymin=5 -xmax=4 -ymax=3 -header=1
#
# McKellar
# $ python convert-new2.py -height=926 -width=926 -image=1 -header=1



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

