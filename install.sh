#!/bin/bash

echo "WARNING: THIS PROGRAM SHOULD ONLY BE RUN ON UBUNTU!!!"

# NOTE: THE DEFAULT WORKING DIRECTORY FOR THE REST OF THIS PROGRAM IS THE DIRECTORY THAT THIS PROGRAM WAS INVOKED IN (usually, '/var/www/html/CodeTutorials/'; you can get around this with 'pushd' and 'popd')

if [ "$1" = "-v" ]
then
	exec 3>&1
else
	exec 3>/dev/null
fi

# Exit on errors
set -e
set -o pipefail

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
echo 1>&3
echo "Setting up project configuration..."
set +e
set +o pipefail
rm ./.settings.sh &>/dev/null
source ./devtools.sh # TODO: PUT INFORMATION IN README FILE ABOUT THIS PART
set -e
set -o pipefail

# Change project permissions as appropriate
echo 1>&3
echo "Updating project permissions..."
openproj
if $DEVELOPMENT && $DEPLOYMENT
then
	devdeploy .
elif $DEVELOPMENT
then
	developer.
elif $DEPLOYMENT
then
	deployment .
fi

# Set up and activate virtual environment
echo 1>&3
echo "Creating virtual environment for python..."
virtualenv -p python3 ./djangobox/ 1>&3
pushd ./djangobox/ &>/dev/null
	source ./bin/activate
popd &>/dev/null

# Install python packages
echo 1>&3
echo "Installing Django and useful packages in virtual environment..."
pip3 install Django==2.1.7 djangocodemirror==2.1.0 django-bootstrap3==11.1.0 1>&3

# Add relevant users to group 'docker'
echo 1>&3
if $DEVELOPMENT
then
	echo "Adding '$DEV_USER' to group 'docker'..."
	sudo usermod -aG docker $DEV_USER
fi
if $DEPLOYMENT
then
	echo "Adding '$SERVER_USER' to group 'docker'..."
	sudo usermod -aG docker $SERVER_USER
fi

# Set up database
echo 1>&3
echo "Setting up database..."
pushd ./djangobox/src/ &>/dev/null
	./manage.py makemigrations 1>&3
	./manage.py migrate 1>&3
popd &>/dev/null

# Collect static files
echo 1>&3
echo "Collecting static files..."
pushd ./djangobox/src/ &>/dev/null
	./manage.py collectstatic <<<"yes" 1>&3
popd &>/dev/null

# Build Docker images
echo 1>&3
echo "Building docker images..."
pushd ./djangobox/src/docker/docker_wrapper/ &>/dev/null
	sudo systemctl start containerd.service docker.service docker.socket
	./buildimages.sh 1>&3 # This script uses 'sudo' on its own, but this simplifies things a bit
	sudo systemctl stop containerd.service docker.service docker.socket
popd &>/dev/null

# Potentially, symlink the static directory for Apache
if $DEPLOYMENT
then
	echo 1>&3
	echo "Symlinking static files directory for Apache..."
	pushd /var/www/html/ &>/dev/null
		sudo ln -s -T $OLDPWD/djangobox/src/static/ ./static
	popd &>/dev/null
fi

# Move the WSGI configuration file so that Apache can find it
if $DEPLOYMENT
then
	echo 1>&3
	echo "Copying WSGI configuration file..."
	sudo cp ./wsgi/wsgi_codetutorials.conf /etc/apache2/mods-enabled/wsgi_codetutorials.conf
	sudo cp ./wsgi/wsgi_codetutorials.load /etc/apache2/mods-enabled/wsgi_codetutorials.load
fi

# Cleanup
undevtools
deactivate
