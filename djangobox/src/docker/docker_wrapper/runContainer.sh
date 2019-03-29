#!/bin/bash

IMAGENAME="testcomp"

exit $(docker run --rm -v $1:/home/guest $IMAGENAME)
