#!/bin/sed -e 3q;d;

# Do not run this file directly - source it instead

### Startup

# Clear everything from a previous session

undevtools &>/dev/null

# Global and static variables

source ./makesettings.sh

TOOLS_PROMPT="(devtools) "
SRC_DIR=$SETTINGS_DIR/djangobox/src
MANAGE_PY=$SRC_DIR/manage.py

echo "Some commands in this suite invoke 'sudo'. Use them at your own risk!"
echo "You can deactivate this suite at any time by running 'undevtools'."

PS1=$TOOLS_PROMPT$PS1


### Internal components - DO NOT TOUCH (please)

function changeperms {
	local TO_WHOM=$1
	shift
	if [ -n "$*" ]
	then
		local INDEX
		for INDEX in "$@"
		do
			find $INDEX \( -type d -o -type f \) -execdir sudo chown --no-dereference $TO_WHOM \{\} +
			find $INDEX -type d -execdir sudo chmod u+rwx,g+rwx \{\} +
			find $INDEX -type f -execdir sudo chmod u+rw,g+rw \{\} +
		done
	else
		echo "Error: Missing parameter."
	fi
}


### User-end functions

# Removes any functionality of this script from your terminal
function undevtools {
	PS1=${PS1#$TOOLS_PROMPT}
	
	unset -v TOOLS_PROMPT SRC_DIR MANAGE_PY 1>/dev/null
	unset -f undevtools changeperms developer devdeploy deployment openaccess openproj closeaccess closeproj startserver stopserver 1>/dev/null
	
	unalias collectstatic
	
	unsettings
}

# Ownership tools

# Changes ownership and group of the given directories to the developer
function developer {
	changeperms $DEV_USER:$DEV_GROUP "$@"
}

# Changes ownership of the given directories to the developer and group to the server
function devdeploy {
	changeperms $DEV_USER:$SERVER_GROUP "$@"
}

# Changes ownership and group of the given directories to the server
function deployment {
	changeperms $SERVER_USER:$SERVER_GROUP "$@"
}

# Permission tools

# Recursively adds reading permission for everyone upon the given directories
function openaccess {
	if [ -n "$*" ]
	then
		local INDEX
		for INDEX in "$@"
		do
			find $INDEX -type d -execdir sudo chmod a+rx,ug+w \{\} +
			find $INDEX -type f -execdir sudo chmod a+r,ug+w \{\} +
		done
	else
		echo "Error: Missing parameter."
	fi
}

# Recursively revokes all permissions for everyone except the owner upon the given directories
function closeaccess {
	if [ -n "$*" ]
	then
		local INDEX
		for INDEX in "$@"
		do
			find $INDEX \( -type f -o -type d \) -execdir sudo chmod go-rwx \{\} +
		done
	else
		echo "Error: Missing parameter."
	fi
}

# Makes the project's files accessible to everyone
function openproj {
	openaccess $SRC_DIR/
	sudo chmod ug+x $SRC_DIR/docker/docker_wrapper/runContainer.sh
	sudo chmod u+x $SRC_DIR/docker/docker_wrapper/buildimages.sh
}

# Makes the project's files inaccessible to everyone except the owner
function closeproj {
	sudo chmod g-x $SRC_DIR/docker/docker_wrapper/runContainer.sh
	closeaccess $SRC_DIR/
}

# Server tools

eval "
# Starts the deployment server
function startserver {
	$SERVER_START
}

# Stops the deployment server
function stopserver {
	$SERVER_STOP
}
"

# Convenience for updating static files
alias collectstatic="$MANAGE_PY collectstatic <<<'yes' 1>/dev/null"
