#!/bin/bash

SRC_DIR=~/work/datasets/ready-for-training/weinstein-poland-1
TRAIN_DIR=data/poland1

echo "cleaning files"
mkdir $TRAIN_DIR
rm -rf $TRAIN_DIR/*

echo "copying files"
cp -pr $SRC_DIR/* $TRAIN_DIR/

exit 0
