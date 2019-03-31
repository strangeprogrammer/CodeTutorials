#!/bin/bash

buildimages() {
	docker build --build-arg uid=$1 --build-arg gid=$2 -t gccbox -f ./Dockerfile.c .
	docker build --build-arg uid=$1 --build-arg gid=$2 -t rbox -f ./Dockerfile.R .
	docker build --build-arg uid=$1 --build-arg gid=$2 -t pythonbox -f ./Dockerfile.py .
}

buildimages $1 $2
