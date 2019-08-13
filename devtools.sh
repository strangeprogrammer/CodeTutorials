#!/bin/sed -e 3q;d;

# Do not run this file directly - source it instead

### Startup

# Clear everything from a previous session

undevtools &>/dev/null

# Global and static variables

TOOLS_PROMPT="(devtools) "
TOOLS_DIR=$(realpath -m $(dirname "$PWD/$0"))
TOOLS_SETTINGS=$TOOLS_DIR"/devtools_settings.sh"
SRC_DIR=$TOOLS_DIR"/djangobox/src"
MANAGE_PY=$SRC_DIR"/manage.py"

# Useful aliases

alias thruargs='
if [ -n "$*" ]
then
	local INDEX
	for INDEX in "$@"
	do
'

alias unthruargs='
	done
else
	echo "Error: Missing parameter."
fi
'

# Initialize or load configuration file

if [ -f $TOOLS_SETTINGS ]
then
	source $TOOLS_SETTINGS
	echo "Settings loaded from file '$TOOLS_SETTINGS' (delete it to reset this dialog)."
else
	echo -n "Input developer username:  "
	read DEV_USER
	echo -n "Input developer groupname: "
	read DEV_GROUP
	echo -n "Input server username:     "
	read SERVER_USER
	echo -n "Input server groupname:    "
	read SERVER_GROUP
	
	
	DEPSERVER_START="sudo systemctl start apache2.service"
	echo -n "Input deployment server startup command (defaults to '$DEPSERVER_START'): "
	read
	if [ -n "$REPLY" ]
	then
		DEPSERVER_START=$REPLY
	fi
	
	DEPSERVER_STOP="sudo systemctl stop apache2.service"
	echo -n "Input deployment server shutdown command (defaults to '$DEPSERVER_STOP'): "
	read
	if [ -n "$REPLY" ]
	then
		DEPSERVER_STOP=$REPLY
	fi
	
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
	thruargs
		find $INDEX \( -type d -o -type f \) -execdir sudo chown $TO_WHOM \{\} +
		find $INDEX -type d -execdir sudo chmod u+rwx,g+rwx \{\} +
		find $INDEX -type f -execdir sudo chmod u+rw,g+rw \{\} +
	unthruargs
}


### User-end functions

function undevtools {
	PS1=${PS1#$TOOLS_PROMPT}
	
	unset -v TOOLS_PROMPT TOOLS_DIR TOOLS_SETTINGS SRC_DIR MANAGE_PY DEV_USER DEV_GROUP SERVER_USER SERVER_GROUP DEPSERVER_START DEPSERVER_STOP	1>/dev/null
	unset -f undevtools changeperms developer devdeploy deployment openaccess openbox closeaccess closebox depserver killdepserver			1>/dev/null
	
	unalias collectstatic
}

# Ownership tools

function developer {
	changeperms $DEV_USER:$DEV_GROUP "$@"
}

function devdeploy {
	changeperms $DEV_USER:$SERVER_GROUP "$@"
}

function deployment {
	changeperms $SERVER_USER:$SERVER_GROUP "$@"
}

# Permission tools

function openaccess {
	thruargs
		find $INDEX -type d -execdir sudo chmod a+rx,ug+w \{\} +
		find $INDEX -type f -execdir sudo chmod a+r,ug+w \{\} +
	unthruargs
}

function openbox {
	openaccess $SRC_DIR/
	sudo chmod ug+x $SRC_DIR"/docker/docker_wrapper/runContainer.sh"
}

function closeaccess {
	thruargs
		find $INDEX \( -type f -o -type d \) -execdir sudo chmod go-rwx \{\} +
	unthruargs
}

function closebox {
	closeaccess $SRC_DIR/
}

# Server tools

eval "
function depserver {
	$DEPSERVER_START
}

function killdepserver {
	$DEPSERVER_STOP
}
"

alias collectstatic="$MANAGE_PY collectstatic <<<'yes' 1>/dev/null"


### Cleanup

unalias thruargs unthruargs
