# partition.py
#
# For splitting an image set with annotations into training (80%), validation (10%) and test (10%) groups.
# Most of this is sourced from Paperspace Blog - https://blog.paperspace.com/train-yolov7-custom-data/
#
# NOTE: this requires scikit-learn, which is not enabled by default in the YOLOv7 requirements.txt
# use 'pip install scikit-learn' if you receive error "ModuleNotFoundError: No module named 'sklearn'"

import os
from sklearn.model_selection import train_test_split

# Read images and annotations
images = [os.path.join('in/images', x) for x in os.listdir('in/images')]
annotations = [os.path.join('out', x) for x in os.listdir('out') if x[-3:] == "txt"]

print("Sorting and splitting dataset, total images: {}".format(len(images)))

images.sort()
annotations.sort()

# Split the dataset into train-valid-test splits 
train_images, val_images, train_annotations, val_annotations = train_test_split(images, annotations, test_size = 0.2, random_state = 1)
val_images, test_images, val_annotations, test_annotations = train_test_split(val_images, val_annotations, test_size = 0.5, random_state = 1)

new_dirs = ["out/partition", "out/partition/images", "out/partition/labels", "out/partition/images/train", 
            "out/partition/images/validate", "out/partition/images/test", 
            "out/partition/labels/train", "out/partition/labels/validate", "out/partition/labels/test"]
for one_dir in new_dirs:
    #print(one_dir)
    if not os.path.exists(one_dir):
        os.mkdir(one_dir)

#if not os.path.exists("out-images/train"):
#    os.mkdir("out-images/train")

#images/val images/test labels/train labels/val labels/test



print("Done")