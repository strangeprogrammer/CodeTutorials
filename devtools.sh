#!/bin/sed -e 3q;d;

# Do not run this file directly - source it instead

### Startup

# Clear everything from a previous session

undevtools &>/dev/null

# Global and static variables

TOOLS_PROMPT="(devtools) "
TOOLS_DIR=$(realpath -m $(dirname "$PWD/$0"))
TOOLS_SETTINGS=$TOOLS_DIR/devtools_settings.sh
SRC_DIR=$TOOLS_DIR/djangobox/src
MANAGE_PY=$SRC_DIR/manage.py

# Initialize or load configuration file

if [ -f $TOOLS_SETTINGS ]
then
	source $TOOLS_SETTINGS
	echo "Settings loaded from file '$TOOLS_SETTINGS' (delete it to reset this dialog)."
else
	# Configure developer user and group
	echo -n "Input developer username:  "
	read DEV_USER
	echo -n "Input developer groupname: "
	read DEV_GROUP
	
	# Configure server user and group
	SERVER_USER="nobody"
	echo "Input server username:     "
	echo -n "(default: '$SERVER_USER'):       "
	read
	if [ -n "$REPLY" ]
	then
		SERVER_USER=$REPLY
	fi
	
	SERVER_GROUP="nogroup"
	echo "Input server groupname:    "
	echo -n "(default: '$SERVER_GROUP'):      "
	read
	if [ -n "$REPLY" ]
	then
		SERVER_GROUP=$REPLY
	fi
	
	# Configure deployment server commands
	DEPSERVER_START="true"
	echo "Input deployment server startup command:"
	echo "(recommended: 'sudo systemctl start apache2.service containerd.service docker.service docker.socket'):"
	echo -n "(default: '$DEPSERVER_START'):         "
	read
	if [ -n "$REPLY" ]
	then
		DEPSERVER_START=$REPLY
	fi
	
	DEPSERVER_STOP="true"
	echo "Input deployment server shutdown command:"
	echo "(recommended: 'sudo systemctl stop apache2.service containerd.service docker.service docker.socket'):"
	echo -n "(default: '$DEPSERVER_STOP'):         "
	read
	if [ -n "$REPLY" ]
	then
		DEPSERVER_STOP=$REPLY
	fi
	
	
	# Possibly, save settings
	echo -n "Would you like to save these settings? "
	read YN
	echo
	if [[ "$YN" =~ ^[Yy]([Ee][Ss])?$ ]]
	then
		cat >$TOOLS_SETTINGS <<- EOF
		#!/bin/false
		DEV_USER="$DEV_USER"
		DEV_GROUP="$DEV_GROUP"
		SERVER_USER="$SERVER_USER"
		SERVER_GROUP="$SERVER_GROUP"
		DEPSERVER_START="$DEPSERVER_START"
		DEPSERVER_STOP="$DEPSERVER_STOP"
		EOF
		echo "Settings saved to file '$TOOLS_SETTINGS' (delete it to reset this dialog)."
	fi
fi

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
	
	unset -v TOOLS_PROMPT TOOLS_DIR TOOLS_SETTINGS SRC_DIR MANAGE_PY DEV_USER DEV_GROUP SERVER_USER SERVER_GROUP DEPSERVER_START DEPSERVER_STOP	1>/dev/null
	unset -f undevtools changeperms developer devdeploy deployment openaccess openproj closeaccess closeproj depserver killdepserver		1>/dev/null
	
	unalias collectstatic
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
function depserver {
	$DEPSERVER_START
}

# Stops the deployment server
function killdepserver {
	$DEPSERVER_STOP
}
"

# Convenience for updating static files
alias collectstatic="$MANAGE_PY collectstatic <<<'yes' 1>/dev/null"
