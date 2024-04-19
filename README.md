# cv-tools
Scripts to support various computer vision data management tasks.

## pascal-to-yolov5.py
This script converts CV training data annotations from PASCAL VOC XML format, to YOLOv5 (.txt) format.
Credit: https://blog.paperspace.com/train-yolov7-custom-data/

Put your PASCAL VOC annotations (./xml) to be converted in `/in/` directory.

Run the script.

    $ python pascal-to-yolov5.py

The script will read and parse all .xml files, and create appropriate .txt files in the `/out/` directory.  

## yolo-annotation-test.py

Run this script after converting your annotations, as a test to visually check that the annotations are correct.
The script will load one random annotation with its associated image, so you can check that the bounding box and category 
are correct.  

First, run the pascal-to-yolov5 script to create your YOLO annotations.  Then put your test imagest in the `/images` directory
and run the test script.

    $ python yolo-annotation-test.py

This should launch an image viewer window with the random image and it's associated bounding box.
