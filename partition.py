# partition.py
#
# For splitting an image set with annotations into training (80%), validation (10%) and test (10%) groups.
# Most of this is sourced from Paperspace Blog - https://blog.paperspace.com/train-yolov7-custom-data/
#
# NOTE: this requires scikit-learn, which is not enabled by default in the YOLOv7 requirements.txt
# use 'pip install scikit-learn' if you receive error "ModuleNotFoundError: No module named 'sklearn'"

import os
import shutil
from sklearn.model_selection import train_test_split

# Read images and annotations
images = [os.path.join('in/images', x) for x in os.listdir('in/images')]
annotations = [os.path.join('out/converted', x) for x in os.listdir('out/converted') if x[-3:] == "txt"]

print("Sorting and splitting dataset, total images: {}".format(len(images)))
print("  Total annotation files: {}".format(len(annotations)))

images.sort()
annotations.sort()

# Check list sizes, remove any images with no annotations
if (len(images) != len(annotations)):
    orphan_count = 0
    orphan_list = []
    print("List sizes don't match.  Removing orphan images.")
    annotation_files = os.listdir('out/converted')
    for one_image in images:
        annotation_file_name = os.path.basename(one_image).replace("png", "txt")
        if annotation_file_name not in annotation_files:
            #print("not found: {}".format(annotation_file_name))
            #print("  remove: {}".format(one_image))
            orphan_count += 1
            orphan_list.append(one_image)
    print("removing {} orphans".format(orphan_count))
    for one_orphan in orphan_list:
        images.remove(one_orphan)
    print("total images is now: {}".format(len(images)))

# Split the dataset into train-valid-test splits 
train_images, val_images, train_annotations, val_annotations = train_test_split(images, annotations, test_size = 0.2, random_state = 1)
val_images, test_images, val_annotations, test_annotations = train_test_split(val_images, val_annotations, test_size = 0.5, random_state = 1)

new_dirs = ["out/partition", "out/partition/images", "out/partition/labels", "out/partition/images/train", 
            "out/partition/images/val", "out/partition/images/test", 
            "out/partition/labels/train", "out/partition/labels/val", "out/partition/labels/test"]
for one_dir in new_dirs:
    #print(one_dir)
    if not os.path.exists(one_dir):
        os.mkdir(one_dir)

#if not os.path.exists("out-images/train"):
#    os.mkdir("out-images/train")

#images/val images/test labels/train labels/val labels/test

#Utility function to move images 
def move_files_to_folder(list_of_files, destination_folder):
    for f in list_of_files:
        try:
            #shutil.move(f, destination_folder)
            shutil.copy(f, destination_folder)
        except:
            print(f)
            assert False

# Move the splits into their folders
move_files_to_folder(train_images, 'out/partition/images/train')
move_files_to_folder(val_images, 'out/partition/images/val/')
move_files_to_folder(test_images, 'out/partition/images/test/')
move_files_to_folder(train_annotations, 'out/partition/labels/train/')
move_files_to_folder(val_annotations, 'out/partition/labels/val/')
move_files_to_folder(test_annotations, 'out/partition/labels/test/')

print("Done")