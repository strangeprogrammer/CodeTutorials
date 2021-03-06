#!/bin/sed -e 3q;d;

### BEGIN COPYRIGHT NOTICE

# Copyright 2019 Stephen Fedele <stephen.m.fedele@wmich.edu>
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

# Do not run this file directly - source it instead

### Startup

# Clear everything from a previous session

unsettings &>/dev/null || true

# Global variables

PROJECT_ROOT=$(realpath -m $(dirname "$PWD/$0"))
SETTINGS_FILE=$PROJECT_ROOT/.settings.sh

# Initialize or load configuration file

if [ -f $SETTINGS_FILE ]
then
	source $SETTINGS_FILE
	echo "Settings loaded from file '$SETTINGS_FILE' (delete it to reset this dialog)."
else
	# Ask about project mode
	echo -n "Will this project be used for 1) development only, 2) development of the deployment version, or 3) deployment only? "
	read
	case "$REPLY" in
	"1")
		DEVELOPMENT="true"
		DEPLOYMENT="false"
		;;
	"2")
		DEVELOPMENT="true"
		DEPLOYMENT="true"
		;;
	"3")
		DEVELOPMENT="false"
		DEPLOYMENT="true"
		;;
	*)
		echo "Error: Invalid question response..."
		return 1
		;;
	esac
	
	
	# Configure developer user and group
	DEV_USER="$(id -un)"
	cat <<- EOF
		Input developer username (login name)
		(default if empty: '$DEV_USER'):
	EOF
	read
	if [ -n "$REPLY" ]
	then
		DEV_USER=$REPLY
	fi
	echo
	
	DEV_GROUP="$(id -gn)"
	cat <<- EOF
		Input developer groupname
		(default if empty: '$DEV_GROUP'):
	EOF
	read
	if [ -n "$REPLY" ]
	then
		DEV_GROUP=$REPLY
	fi
	echo
	
	
	# Configure server user and group
	SERVER_USER="www-data"
	cat <<- EOF
		Input server username
		(if not applicable, input: 'nobody')
		(default if empty (uses Apache): '$SERVER_USER'):
	EOF
	read
	if [ -n "$REPLY" ]
	then
		SERVER_USER=$REPLY
	fi
	echo
	
	SERVER_GROUP="www-data"
	cat <<- EOF
		Input server groupname
		(if not applicable, input: 'nogroup')
		(default if empty (uses Apache): '$SERVER_GROUP'):
	EOF
	read
	if [ -n "$REPLY" ]
	then
		SERVER_GROUP=$REPLY
	fi
	echo
	
	
	# Configure deployment server commands
	if $DEPLOYMENT
	then
		SERVER_START="sudo systemctl start apache2.service containerd.service docker.service docker.socket"
	else
		SERVER_START="sudo systemctl start containerd.service docker.service docker.socket && $PROJECT_ROOT/djangobox/src/manage.py runserver"
	fi
	cat <<- EOF
		Input server startup command
		(default if empty: '$SERVER_START'):
	EOF
	read
	if [ -n "$REPLY" ]
	then
		SERVER_START=$REPLY
	fi
	echo
	
	if $DEPLOYMENT
	then
		SERVER_STOP="sudo systemctl stop apache2.service containerd.service docker.service docker.socket"
	else
		SERVER_STOP="sudo systemctl stop containerd.service docker.service docker.socket && echo 'Please remember to kill the Django process if it is running in the background!'"
	fi
	cat <<- EOF
		Input server shutdown command
		(default if empty: '$SERVER_STOP'):
	EOF
	read
	if [ -n "$REPLY" ]
	then
		SERVER_STOP=$REPLY
	fi
	echo
	
	
	# Save settings
	cat >$SETTINGS_FILE <<- EOF
	#!/bin/false
	DEVELOPMENT="$DEVELOPMENT"
	DEPLOYMENT="$DEPLOYMENT"
	DEV_USER="$DEV_USER"
	DEV_GROUP="$DEV_GROUP"
	SERVER_USER="$SERVER_USER"
	SERVER_GROUP="$SERVER_GROUP"
	SERVER_START="$SERVER_START"
	SERVER_STOP="$SERVER_STOP"
	EOF
	echo "Settings saved to file '$SETTINGS_FILE' (delete it to reset this dialog)."
fi

### Cleanup

function unsettings {
	unset -v PROJECT_ROOT SETTINGS_FILE DEVELOPMENT DEPLOYMENT DEV_USER DEV_GROUP SERVER_USER SERVER_GROUP SERVER_START SERVER_STOP 1>/dev/null
	unset -f unsettings 1>/dev/null
}
