# convert-weinstein.py
#
# For converting bbox annotations in Weinstein et al to YOLOv5 format.
# Weinstein training data bbox annotations are all in one file.  This 
# script creates one file per image, as expected by YOLOv5.
#
# Paper: https://www.biorxiv.org/content/10.1101/2021.08.05.455311v1.full
# Data: https://zenodo.org/records/5033174 

import csv
import os
from tqdm import tqdm

# Function to get the data from XML Annotation
# def extract_info_from_xml(xml_file):
#     root = ET.parse(xml_file).getroot()
    
#     # Initialise the info dict 
#     info_dict = {}
#     info_dict['bboxes'] = []

#     # Parse the XML Tree
#     for elem in root:
#         # Get the file name 
#         if elem.tag == "filename":
#             info_dict['filename'] = elem.text
            
#         # Get the image size
#         elif elem.tag == "size":
#             image_size = []
#             for subelem in elem:
#                 image_size.append(int(subelem.text))
            
#             info_dict['image_size'] = tuple(image_size)
        
#         # Get details of the bounding box 
#         elif elem.tag == "object":
#             bbox = {}
#             for subelem in elem:
#                 if subelem.tag == "name":
#                     bbox["class"] = subelem.text
                    
#                 elif subelem.tag == "bndbox":
#                     for subsubelem in subelem:
#                         bbox[subsubelem.tag] = int(subsubelem.text)            
#             info_dict['bboxes'].append(bbox)
    
#     return info_dict

# Dictionary that maps class names to IDs
# class_name_to_id_mapping = {"trafficlight": 0,
#                            "stop": 1,
#                            "speedlimit": 2,
#                            "crosswalk": 3}

# Convert the info dict to the required yolo format and write it to disk
# def convert_to_yolov5(info_dict):
#     print_buffer = []
    
#     # For each bounding box
#     for b in info_dict["bboxes"]:
#         try:
#             class_id = class_name_to_id_mapping[b["class"]]
#         except KeyError:
#             print("Invalid Class. Must be one from ", class_name_to_id_mapping.keys())
        
#         # Transform the bbox co-ordinates as per the format required by YOLO v5
#         b_center_x = (b["xmin"] + b["xmax"]) / 2 
#         b_center_y = (b["ymin"] + b["ymax"]) / 2
#         b_width    = (b["xmax"] - b["xmin"])
#         b_height   = (b["ymax"] - b["ymin"])
        
#         # Normalise the co-ordinates by the dimensions of the image
#         image_w, image_h, image_c = info_dict["image_size"]  
#         b_center_x /= image_w 
#         b_center_y /= image_h 
#         b_width    /= image_w 
#         b_height   /= image_h 
        
#         #Write the bbox details to the file 
#         print_buffer.append("{} {:.3f} {:.3f} {:.3f} {:.3f}".format(class_id, b_center_x, b_center_y, b_width, b_height))
        
#     # Name of the file which we have to save 
#     save_file_name = os.path.join("out/converted", info_dict["filename"].replace("png", "txt"))
    
#     # Save the annotation to disk
#     print("\n".join(print_buffer), file= open(save_file_name, "w"))


# Read input annotations
# annotations = [os.path.join('in/annotations', x) for x in os.listdir('in/annotations') if x[-3:] == "xml"]
# annotations.sort()

# Convert and save the annotations
# for ann in tqdm(annotations):
#     info_dict = extract_info_from_xml(ann)
#     convert_to_yolov5(info_dict)
# annotations = [os.path.join('out/converted', x) for x in os.listdir('out/converted') if x[-3:] == "txt"]



# Field definitions - select the list that matches the annotations input file
class_id = 0    # alway 0, as we will only have one class: "Bird"
field_image = 6
field_bbox_start = 2
header_row = 1  # 1 if there is a header row, 0 if no header row

#... add other field definitions for other input file arrangements



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
        #print(one_record)
        #print(one_record[field_image])
        #for one_field in one_record:
        #    print(one_field)
        file_name = one_record[field_image]
        if (last_file_name != file_name):
            files[file_name] = []
            last_file_name = file_name

        bbox = [class_id, one_record[0+field_bbox_start], one_record[1+field_bbox_start], one_record[2+field_bbox_start], one_record[3+field_bbox_start]]

        #... convert to yolo values

        files[file_name].append(bbox)

    #print(files)
    # print(len(files))

    return files

# Write the yolov5 format annotation files
def write_yolov5(file_dict):
    print("Writing files, total: ", len(file_dict))

    for one_record in file_dict:
        #print(file_dict[one_record])
        print_buffer = []
        rows = file_dict[one_record]
        for one_row in rows:
            #print_buffer.append("{} {:.3f} {:.3f} {:.3f} {:.3f}".format(class_id, b_center_x, b_center_y, b_width, b_height))
            #print_buffer.append("{} {:.3f} {:.3f} {:.3f} {:.3f}".format(one_row[0], one_row[1], one_row[2], one_row[3], one_row[4]))
            print_buffer.append("{} {} {} {} {}".format(one_row[0], one_row[1], one_row[2], one_row[3], one_row[4]))

        out_file_path = "out/converted/" + one_record.replace("png", "txt")
        print("\n".join(print_buffer), file= open(out_file_path, "w"))

        # with open(out_file_path, "wt", newline='') as fp:
        #     writer = csv.writer(fp, delimiter=",")
        #     # writer.writerow(["your", "header", "foo"])  # write header
        #     #writer.writerows(rows)
        
        
            


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