#!/bin/bash

# Note: comment all instances of '&>/dev/null' for debugging

### Setup

# Die if things go unexpectedly wrong
# https://stackoverflow.com/a/19469570
set -e
set -E
set -o pipefail

# Environment Variables
# CONT_RUNOPTS
# CONT_GRACE
# CONT_TIMEOUT


# Get input arguments
FOLDER=$1
IMAGENAME=$2
CONTNAME=$3

# Optionally, log invocation information
# echo $FOLDER $IMAGENAME $CONTNAME >>./containerLog.txt

# Set to "true" or "false" as you desire
DEBUG="false"

MYNAME="$(basename $0):$$:"


### Important subroutines

function createCont(){ # Explicitly create the container
	if $DEBUG; then echo "$MYNAME Creating container"; fi
	docker create $CONT_RUNOPTS --name $CONTNAME $IMAGENAME
}

function toCont(){ # Copy the code and STDIN into the container
	if $DEBUG; then echo "$MYNAME Copying files to container"; fi
	docker cp $FOLDER/code $CONTNAME:/home/guest/code	&
	docker cp $FOLDER/STDIN $CONTNAME:/home/guest/STDIN	&
	wait
}

function runCont(){ # Start the container AND WAIT FOR IT TO STOP (otherwise race conditions are formed when copying files out of the container)
	if $DEBUG; then echo "$MYNAME Running container"; fi
	docker start $CONTNAME
	{	sleep $CONT_GRACE
		docker stop -t $CONT_TIMEOUT $CONTNAME
	} &
	
	{	( return $(docker wait $CONTNAME) ) && kill -SIGTERM $! && wait
	} || {	echo "$MYNAME Container timed out"
		false
	}
}

function fromCont(){ # Copy the STDOUT, STDERR, and return value out of the container
	if $DEBUG; then echo "$MYNAME Copying files from container"; fi
	docker cp $CONTNAME:/home/guest/STDOUT $FOLDER/STDOUT	&
	docker cp $CONTNAME:/home/guest/STDERR $FOLDER/STDERR	&
	docker cp $CONTNAME:/home/guest/retval $FOLDER/retval	&
	wait
}

function rmCont(){ # Remove the container since it's no longer needed
	if $DEBUG; then echo "$MYNAME Removing container"; fi
	docker rm -f $CONTNAME || true
}


### Register handler to remove container in case there's an unexpected error

# Make a backup STDERR
exec 3>&2

function errRmCont(){
	wait
	echo "$MYNAME AN UNEXPECTED ERROR OCCURED; Removing dangling container '$CONTNAME'" 1>&3
	rmCont
	exit -1
}
trap errRmCont ERR


### Main

function main(){
	createCont
	toCont
	runCont
	fromCont
	rmCont
}

# START ZE PROGRAM!!!
if $DEBUG; then
	echo "$MYNAME Invocation options: $CONT_RUNOPTS"
	main
	echo "$MYNAME Done with container management"
else
	main &>/dev/null
fi
