#!/bin/false

# Do not run this file directly - source it instead

### Internal components - DO NOT TOUCH (please)

UTILS_DIR_BKP=$(realpath -m $(dirname "$PWD/$0"))

source $UTILS_DIR_BKP"/unpermutils.sh"

UTILS_DIR=$UTILS_DIR_BKP
unset -v UTILS_DIR_BKP

UTILS_SETTINGS=$UTILS_DIR"/permutils_settings.sh"

function changeperms {
	if [ -n "$2" ]
	then
		find $2 -type d -o -type f -execdir sudo chown $1 \{\} +
		find $2 -type d -execdir sudo chmod u+rwx,g+rwx \{\} +
		find $2 -type f -execdir sudo chmod u+rw,g+rw \{\} +
	else
		echo "Error: Missing parameter"
	fi
}


### User-end functions

function developer {
	changeperms $DEV_USER:$DEV_GROUP $1
}

function devdeploy {
	changeperms $DEV_USER:$SERVER_GROUP $1
}

function deployment {
	changeperms $SERVER_USER:$SERVER_GROUP $1
}

function openaccess {
	if [ -n "$1" ]
	then
		find $1 -type d -execdir sudo chmod a+rx \{\} +
		find $1 -type f -execdir sudo chmod a+r \{\} +
	else
		echo "Error: Missing parameter"
	fi
}

function closeaccess {
	if [ -n "$1" ]
	then
		find $1 -execdir sudo chmod go-rwx \{\} +
	else
		echo "Error: Missing parameter"
	fi
}


### Startup and settings file initial configuration

if [ -f $UTILS_SETTINGS ]
then
	source $UTILS_SETTINGS
else
	echo -n "Input developer username:  "
	read DEV_USER
	echo -n "Input developer groupname: "
	read DEV_GROUP
	echo -n "Input apache username:     "
	read SERVER_USER
	echo -n "Input apache groupname:    "
	read SERVER_GROUP
	
	echo -n "Would you like to save these settings? "
	read YN
	if [[ "$YN" =~ ^[Yy]([Ee][Ss])?$ ]]
	then
		cat >$UTILS_SETTINGS <<- EOF
		#!/bin/false
		DEV_USER=$DEV_USER
		DEV_GROUP=$DEV_GROUP
		SERVER_USER=$SERVER_USER
		SERVER_GROUP=$SERVER_GROUP
		EOF
		echo "Settings saved to file '$UTILS_SETTINGS' (delete it to reset this dialog)."
	fi
fi

echo "Some commands in this suite invoke 'sudo'. Use them at your own risk!"
echo "You can deactivate this suite at any time by running '$UTILS_DIR/unpermutils.sh'."

PS1="(permutils) "$PS1
