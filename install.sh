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

# Initialize project settings
echo 1>&3
echo "Initializing project settings..."
rm ./.settings.sh &>/dev/null || true
source ./devtools.sh --installation

# Change project permissions as appropriate
echo 1>&3
echo "Updating project permissions..."
openproj
if $DEVELOPMENT && $DEPLOYMENT
then
	function fixperms {
		devdeploy "$@"
		openaccess "$@"
	}
elif $DEVELOPMENT
then
	function fixperms {
		developer "$@"
		openaccess "$@"
	}
elif $DEPLOYMENT
then
	function fixperms {
		deployment "$@"
		openaccess "$@"
	}
fi
fixperms .

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
pip3 install Django==2.1.7 djangocodemirror==2.1.0 django-bootstrap3==11.1.0 django-generate-secret-key==1.0.2 1>&3

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

# Generate a secret key for Django
echo 1>&3
echo "Generating a secret key for Django..."
pushd ./djangobox/src/ &>/dev/null
	./manage.py generate_secret_key --replace
	fixperms $SRC_DIR/secretkey.txt
	closeaccess $SRC_DIR/secretkey.txt
popd &>/dev/null

# Set up database
echo 1>&3
echo "Setting up database..."
pushd ./djangobox/src/ &>/dev/null
	./manage.py makemigrations 1>&3
	./manage.py migrate 1>&3
	fixperms $SRC_DIR/db.sqlite3
popd &>/dev/null

# Collect static files
echo 1>&3
echo "Collecting static files..."
pushd ./djangobox/src/ &>/dev/null
	./manage.py collectstatic <<<"yes" 1>&3
	fixperms $SRC_DIR/static/
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
	cat ./mods-enabled/wsgi.conf | sudo tee -a /etc/apache2/mods-enabled/wsgi.conf &>/dev/null
fi

# Cleanup
unset -f fixperms
undevtools
deactivate
