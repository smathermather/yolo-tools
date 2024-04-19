# cv-tools
Scripts to support various computer vision data management tasks.

## yolo

The scripts in this directory support processing of prepared datasets for use with YOLO.
At the time of development, the target is YOLOv7.  Scripts are adapted from: https://blog.paperspace.com/train-yolov7-custom-data/

`convert-pascal.py` 

This script converts CV training data annotations from PASCAL VOC XML format, to YOLOv5 (.txt) format.
Put your PASCAL VOC annotations (./xml) to be converted in `/in/annotations` directory.
The script will read and parse all .xml files, and create appropriate .txt files in the `/out` directory.  

`test-converted.py` 

Run this script after converting your annotations, as a test to visually check that the annotations are correct.
The script will load one random annotation with its associated image, so you can check that the bounding box and category 
are correct.  

First, run the pascal-to-yolov5 script to create your YOLO annotations.  Then put your test imagest in the `/in/images` directory
and run the test script.  This should launch an image viewer window with the random image and it's associated bounding box.

`partition.py` 

This script partitions a dataset and its converted annotations into training (80%), validation (10%) and test (10%) groups. 

Typical workflow:

    $ python convert-pascal.py
    $ python test-converted.py
    $ python partition.py

