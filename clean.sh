#!/bin/bash

SRC_DIR=~/work/datasets/road-signs
TRAIN_DIR=data/test2

echo "cleaning files"
mkdir $TRAIN_DIR
rm -rf $TRAIN_DIR/*

echo "copying files"
cp -pr $SRC_DIR/* $TRAIN_DIR/

exit 0
