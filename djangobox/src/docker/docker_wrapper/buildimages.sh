#!/bin/bash

# Die if things go unexpectedly wrong
# https://stackoverflow.com/a/19469570
set -e
set -o pipefail


buildimages() {
	docker build --build-arg uid=$1 --build-arg gid=$2 -t gccbox -f ./Dockerfile.c .
	docker build --build-arg uid=$1 --build-arg gid=$2 -t rbox -f ./Dockerfile.R .
	docker build --build-arg uid=$1 --build-arg gid=$2 -t pythonbox -f ./Dockerfile.py .
}

sudo buildimages $1 $2
