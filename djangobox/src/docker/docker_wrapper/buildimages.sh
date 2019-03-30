#!/bin/bash

buildimages() {
	docker build -t gccbox -f ./Dockerfile.c .
	docker build -t rbox -f ./Dockerfile.R .
	docker build -t pythonbox -f ./Dockerfile.py .
}

#Silent version
buildimages &>/dev/null

#Non-silent version (for debugging if required)
#buildimages
