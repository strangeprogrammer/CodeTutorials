#!/bin/bash

# Comment all instances of '&>/dev/null' for debugging

# Die if things go unexpectedly wrong
# https://stackoverflow.com/a/19469570
set -e
set -E
set -o pipefail


FOLDER=$1
IMAGENAME=$2
CONTNAME=$3

# Optionally, log invocation information
# echo $FOLDER $IMAGENAME $CONTNAME >>./containerLog.txt


# Explicitly create the container
function spawnCont(){
	docker create --name $CONTNAME $IMAGENAME

}

# Copy the code and STDIN into the container
function toCont(){
	docker cp $FOLDER/code $CONTNAME:/home/guest/code	&
	docker cp $FOLDER/STDIN $CONTNAME:/home/guest/STDIN	&
	wait
}

# Start the container AND WAIT FOR IT TO STOP (otherwise race conditions are formed when copying files out of the container)
function runCont(){
	docker start $CONTNAME
	docker wait $CONTNAME
}

# Copy the STDOUT, STDERR, and return value out of the container
function fromCont(){
	docker cp $CONTNAME:/home/guest/STDOUT $FOLDER/STDOUT	&
	docker cp $CONTNAME:/home/guest/STDERR $FOLDER/STDERR	&
	docker cp $CONTNAME:/home/guest/retval $FOLDER/retval	&
	wait
}

# Remove the container since it's no longer needed
function rmCont(){
	docker rm -f $CONTNAME
}


# Register handler to remove container in case there's an unexpected error
function errRmCont(){
	wait
	echo "AN UNEXPECTED ERROR OCCURED; Removing dangling container '$CONTNAME'"
	rmCont # &>/dev/null
	exit -1
}
trap errRmCont ERR


function main(){
	spawnCont
	toCont
	runCont
	fromCont
	rmCont
}

# 'main' is invoked in a subshell so that STDOUT and STDERR are redirected properly
# START ZE PROGRAM!!!
( main ) # &>/dev/null )
