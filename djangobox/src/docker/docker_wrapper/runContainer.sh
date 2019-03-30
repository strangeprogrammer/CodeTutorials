#!/bin/bash

FOLDER=$1
IMAGENAME=$2

docker run --rm -v $FOLDER:/home/guest $IMAGENAME
