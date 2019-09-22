#!/bin/bash

# Die if things go unexpectedly wrong
# https://stackoverflow.com/a/19469570
set -e
set -o pipefail

BUILDUID=1001
BUILDGID=1001

buildimages() {
	sudo docker build --build-arg uid=$BUILDUID --build-arg gid=$BUILDGID -t gccbox -f ./Dockerfile.c .
	sudo docker build --build-arg uid=$BUILDUID --build-arg gid=$BUILDGID -t rbox -f ./Dockerfile.R .
	sudo docker build --build-arg uid=$BUILDUID --build-arg gid=$BUILDGID -t pythonbox -f ./Dockerfile.py .
}

buildimages
