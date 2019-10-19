#!/bin/bash

# NOTE: THE DEFAULT WORKING DIRECTORY FOR THE REST OF THIS PROGRAM IS THE DIRECTORY THAT THIS PROGRAM WAS INVOKED IN (YOU CAN GET AROUND THIS WITH 'pushd' and 'popd')

# Exit on errors
set -e
set -o pipefail

# Install some prerequisite packages # FIXME
# sudo apt install python3 python3-pip virtualenv git

# Ask about project mode
echo -n "Would you like to install the project for 1) development only, 2) development of the deployment version, or 3) deployment only? "
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
	exit 1
	;;
esac

# Set up project configuration
source ./devtools.sh # TODO: PUT INFORMATION IN README FILE ABOUT THIS PART
sudo openproj
if $DEVELOPMENT && $DEPLOYMENT
then
	sudo devdeploy .
elif $DEVELOPMENT
then
	sudo developer.
elif $DEPLOYMENT
then
	sudo deployment .
fi

# Set up and activate virtual environment
virtualenv -p python3 ./djangobox/
pushd ./djangobox/
source ./bin/activate
popd

# Install python packages
pip3 install Django==2.1.7 djangocodemirror==2.1.0 django-bootstrap3==11.1.0

# Add relevant users to group 'docker'
if $DEVELOPMENT
then
	sudo usermod -aG docker $DEV_USER
fi
if $DEPLOYMENT
then
	sudo usermod -aG docker $SERVER_USER
fi

# Set up database, collect static files, and build Docker images
pushd ./djangobox/src/
./manage.py makemigrations
./manage.py migrate
./manage.py collectstatic <<<"yes"
pushd ./docker/docker_wrapper/
sudo systemctl start containerd.service docker.service docker.socket
sudo ./buildimages.sh # This script uses 'sudo' on its own, but this simplifies things a bit
sudo systemctl stop containerd.service docker.service docker.socket
popd
popd

# Potentially, symlink the static directory for Apache
pushd /var/www/html/
ln -s -T $OLDPWD/djangobox/src/static/ ./static/
popd

# Cleanup
undevtools
deactivate
