#!/bin/bash

### BEGIN COPYRIGHT NOTICE

# Copyright 2019 Stephen Fedele <stephen.m.fedele@wmich.edu>, Daniel Darcy, Timothy Curry
# 
# This file is part of CodeTutorials.
# 
# CodeTutorials is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
# 
# CodeTutorials is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with CodeTutorials.  If not, see <https://www.gnu.org/licenses/>.

### END COPYRIGHT NOTICE

### Environment Variables

# CONT_RUNOPTS
# CONT_GRACE
# CONT_TIMEOUT


### Admin configurables

# NOTE: comment all instances of '&>/dev/null' for debugging

# Set the next line to "true" or "false" as you desire
DEBUG="false"

PID=$$
MYNAME="$(basename $0):$PID"

# Comment out the next line if you don't want to use logging
# LOGFILE="/var/www/html/CodeTutorials/djangobox/src/docker_requests.log"


### Setup

# Die if things go unexpectedly wrong
# https://stackoverflow.com/a/19469570
set -e
set -E
set -o pipefail

# Get input arguments
FOLDER=$1
IMAGENAME=$2
CONTNAME=$3


### More boilerplate

# Don't log if there is no logfile
if [ -n "$LOGFILE" ]
then
	function loginvoke(){
		{	flock 1
			echo "PID:            "$PID
			echo "Folder:         "$FOLDER
			echo "Image:          "$IMAGENAME
			echo "Container Name: "$CONTNAME
			if [ "$DEBUG" = "true" ]
			then
				echo "UID:            "$(id -ru)
				echo "EUID:           "$(id -u)
				echo "GID:            "$(id -rg)
				echo "EGID:           "$(id -g)
			fi
			echo ""
		} >>$LOGFILE
		return 0
	}
	
	function logstatus(){
		{	flock 1
			echo "PID:            "$PID
			echo "STATUS:         "$1
			echo ""
		} >>$LOGFILE
		return 0
	}
else
	function loginvoke(){
		return 0
	}
	
	function logstatus(){
		return 0
	}
fi

loginvoke


### Important subroutines

function createCont(){ # Explicitly create the container
	if [ "$DEBUG" = "true" ]; then echo "$MYNAME Creating container"; fi
	docker create $CONT_RUNOPTS --name $CONTNAME $IMAGENAME
}

function toCont(){ # Copy the code and STDIN into the container
	if [ "$DEBUG" = "true" ]; then echo "$MYNAME Copying files to container"; fi
	docker cp $FOLDER/code $CONTNAME:/home/guest/code	&
	docker cp $FOLDER/STDIN $CONTNAME:/home/guest/STDIN	&
	wait
}

function runCont(){ # Start the container AND WAIT FOR IT TO STOP (otherwise race conditions are formed when copying files out of the container)
	if [ "$DEBUG" = "true" ]; then echo "$MYNAME Running container"; fi
	docker start $CONTNAME
	{	# Wait to kill the container at the designated time
		sleep $CONT_GRACE
		echo "$MYNAME: Container timed out" >&3
		logstatus "timed out"
		docker stop -t $CONT_TIMEOUT $CONTNAME
	} &
	
	{	# If the container finishes successfully in time, kill the reaper
		( return $(docker wait $CONTNAME) ) && kill -SIGKILL $! && wait && logstatus "success"
	} || {	echo "$MYNAME: Container failed" >&3
		logstatus "failure"
		false
	}
}

function fromCont(){ # Copy the STDOUT, STDERR, and return value out of the container
	if [ "$DEBUG" = "true" ]; then echo "$MYNAME Copying files from container"; fi
	docker cp $CONTNAME:/home/guest/STDOUT $FOLDER/STDOUT	&
	docker cp $CONTNAME:/home/guest/STDERR $FOLDER/STDERR	&
	docker cp $CONTNAME:/home/guest/retval $FOLDER/retval	&
	wait
}

function rmCont(){ # Remove the container since it's no longer needed
	if [ "$DEBUG" = "true" ]; then echo "$MYNAME Removing container"; fi
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
if [ "$DEBUG" = "true" ]; then
	echo "$MYNAME Invocation options: $CONT_RUNOPTS"
	echo "$MYNAME Invocation options: $CONT_RUNOPTS" 1>&3
	main
	echo "$MYNAME Done with container management"
	echo "$MYNAME Done with container management" 1>&3
else
	main &>/dev/null
fi
