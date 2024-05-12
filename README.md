# yolo-tools
This repo contains a collection of python and shell scripts to support various computer vision data management and model training tasks involving YOLO.

These scripts are provided as part of the open-source drone mapping and object counting workflow described here:  https://twomile.com/open-source-drone-mapping-and-object-counting/

Scripts were originally developed in 2024 for YOLOv7.

Several scripts are adapted from code published on the excellent Paperspace machine learning blog: https://blog.paperspace.com/train-yolov7-custom-data/

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

After converting and partitioning, go to your yolov7 data directory and copy over the config, images, and labels

    $ cd ~/yolov7/data
    $ mkdir test1
    $ cp ~/cv-tools/yolo/config/test1-data.yaml .
    $ cp -pr ~/cv-tools/yolo/out/partition/* test1/

Then go to the yolov7 directory and run the training.

    $ python train.py --img-size 640 --cfg cfg/training/yolov7.yaml --hyp data/hyp.scratch.custom.yaml --batch 8 --epochs 100 --data data/test1-data.yaml --weights yolov7_training.pt --workers 24 --name yolo_road_det


