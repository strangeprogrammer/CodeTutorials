#!/bin/bash

FOLDER=$1
IMAGENAME=$2

#Log container information
#echo $FOLDER $IMAGENAME >>./containerLog.txt

docker run --rm -u guest:guest -v $FOLDER:/home/guest:rw $IMAGENAME

exit $?
