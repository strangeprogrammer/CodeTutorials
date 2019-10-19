#!/bin/sed -e 3q;d;

# Do not run this file directly - source it instead

### Startup

# Clear everything from a previous session

unsettings &>/dev/null

# Global variables

SETTINGS_DIR=$(realpath -m $(dirname "$PWD/$0"))
SETTINGS_FILE=$SETTINGS_DIR/.settings.sh

# Initialize or load configuration file

if [ -f $SETTINGS_FILE ]
then
	source $SETTINGS_FILE
	echo "Settings loaded from file '$SETTINGS_FILE' (delete it to reset this dialog)."
else
	# Configure developer user and group
	echo -n	"Input developer username:  "
	read DEV_USER
	echo -n	"Input developer groupname: "
	read DEV_GROUP
	
	# Configure server user and group
	SERVER_USER="www-data"
	echo	"Input server username:"
	echo	"(if not applicable: 'nobody'):"
	echo -n	"(default: '$SERVER_USER'):     "
	read
	if [ -n "$REPLY" ]
	then
		SERVER_USER=$REPLY
	fi
	
	SERVER_GROUP="www-data"
	echo	"Input server groupname:"
	echo 	"(if not applicable: 'nogroup'):"
	echo -n	"(default: '$SERVER_GROUP'):    "
	read
	if [ -n "$REPLY" ]
	then
		SERVER_GROUP=$REPLY
	fi
	
	# Configure deployment server commands
	SERVER_START="sudo systemctl start apache2.service containerd.service docker.service docker.socket"
	echo	"Input deployment server startup command:"
	echo 	"(if not applicable: 'true'):"
	echo -n	"(default: '$SERVER_START'): "
	read
	if [ -n "$REPLY" ]
	then
		SERVER_START=$REPLY
	fi
	
	SERVER_STOP="sudo systemctl stop apache2.service containerd.service docker.service docker.socket"
	echo	"Input deployment server shutdown command:"
	echo 	"(if not applicable: 'true'):"
	echo -n	"(default: '$SERVER_STOP'): "
	read
	if [ -n "$REPLY" ]
	then
		SERVER_STOP=$REPLY
	fi
	
	
	# Save settings
	cat >$SETTINGS_FILE <<- EOF
	#!/bin/false
	DEV_USER="$DEV_USER"
	DEV_GROUP="$DEV_GROUP"
	SERVER_USER="$SERVER_USER"
	SERVER_GROUP="$SERVER_GROUP"
	SERVER_START="$SERVER_START"
	SERVER_STOP="$SERVER_STOP"
	EOF
	echo
	echo "Settings saved to file '$SETTINGS_FILE' (delete it to reset this dialog)."
fi

### Cleanup

function unsettings {
	unset -v SETTINGS_DIR SETTINGS_FILE DEV_USER DEV_GROUP SERVER_USER SERVER_GROUP SERVER_START SERVER_STOP 1>/dev/null
}
