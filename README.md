# CodeTutorials

## MINIMUM SYSTEM REQUIREMENTS & PRE-INSTALLATION STEPS

All commands referenced throughout this document should be run in the context of a system using **python3** via **BASH** or some similar shell running on **Linux**/**UNIX** (though **Ubuntu** is recommended since the commands listed here integrate easily with it).

This is a list of software and their minimum versions required on the host in order to use the code provided by this project:

	# Docker packages
	containerd.io v.1.2.4
	docker-ce-cli v.18.09.3
	docker-ce v.18.09.3
	
	# Python packages
	python3 v.3.5.3
	pip3 v.9.0.1
	virtualenv v.15.1.0
	
	# Misc
	git (any version compatible with github, prefer latest)

Information to install docker can be found at the following URL:

[Docker Installation](https://docs.docker.com/install/)

You can find information specifically for Ubuntu installation here:

[Docker Installation Ubuntu](https://docs.docker.com/install/linux/docker-ce/ubuntu/#install-docker-ce)

Remember to install the **containerd.io**, **docker-ce-cli**, and **docker-ce** packages, in that order.

Installation of **python3**, **pip3**, **virtualenv**, and **git** can be easily done through your package manager:

```bash
# For Linux distributions that use 'APT'
sudo apt install python3 python3-pip virtualenv git
```

There are some other packages that need to be installed within the virtual environment that are listed in **SETTING UP THE VIRTUAL ENVIRONMENT AND DJANGO**.

## SETTING UP THE VIRTUAL ENVIRONMENT AND DJANGO

The following instructions assume that you (or the server user (apache)) will have been granted sufficient access to all of the rest of the files within the project. As a result, you may want to give your own user sufficient permissions as necessary to do what is required.

First, if the directory **/var/www/html/** does not exist, you may create it now in order to clone the repository properly:

```bash
# '1777' is an example directory mode which comes in useful for development
sudo mkdir -p -m 1777 /var/www/html/
```

Next, **git clone** the project repository into **/var/www/html/CodeTutorials/**:

```bash
git clone https://github.com/strangeprogrammer/CodeTutorials /var/www/html/CodeTutorials/
```

You must also set up a python virtual environment (used to get around python version conflicts easily):

```bash
cd /var/www/html/CodeTutorials/
virtualenv -p python3 ./djangobox/
```

The following commands are what you should always use to anoint your command prompt with the virtual environment before performing development or package management:

```bash
cd ./djangobox
source ./bin/activate
```

The correct version of **Django** can then be installed in the virtual environment along with **Django-codemirror** and other neccesary packages:

```bash
pip3 install Django==2.1.7 djangocodemirror django-bootstrap3
```

The following command can then be used to exit the virtual environment:

```bash
deactivate
```

## PROPER PROJECT PERMISSIONING

In order for the server to be able to use docker, you must run the following command using the name of the owner of the project files (which is your own username for development purposes and **www-data** for apache-related deployment purposes; it should be run one time each with either option for deployment development):

```bash
sudo usermod -aG docker [USER]
```

You must log-in again after running the previous command for the changes to take effect.

A tool named **devtools.sh** has been provided to allow you greater control over permissions related to this project. Run the file with:

```bash
cd /var/www/html/CodeTutorials/
source ./devtools.sh
```

It will then provide you with some prompts to fill out, after which the following functions (which may require **sudo** capabilities) will be available for you to use at the command line:

```bash
developer	[DIRECTORY]	# Changes all files under the given directory to the developer's owner and group
devdeploy	[DIRECTORY]	# Changes all files under the given directory to the developer's owner and the server's group
deployment	[DIRECTORY]	# Changes all files under the given directory to the server's owner and group
openaccess	[DIRECTORY]	# For all files under the given directory, grants file read and directory traversal permission to everyone
closeaccess	[DIRECTORY]	# For all files under the given directory, revokes all permissions from everyone except the owner
openproj				# Calls 'openaccess' upon 'CodeTutorials/djangobox/src/' and deals with a pesky file's permissions
closeproj				# Calls 'closeaccess' upon 'CodeTutorials/djangobox/src/' and deals with a pesky file's permissions
```

Depending on whether you are using the project solely for development, development of the deployment version, or deployment only, you should invoke the **developer**, **devdeploy**, or **deployment** function (respectively). It only needs to be invoked upon the files that need to have their owner & group changed (this is almost exclusively **CodeTutorials/djangobox/src** and files/directories within it, though you may have to run it every so often on a different directory depending upon your **umask** value).

Finally, As part of the installation process, you should run **openbox** at least once in order to change some permissions.

To deactivate the developer tools, simply run the following:

```bash
undevtools
```

## SETUP

To set up the database and statically hosted files, run:

```bash
cd /var/www/html/CodeTutorials/djangobox
source ./bin/activate
cd ./src
./manage.py makemigrations
./manage.py migrate
./manage.py collectstatic <<<"yes"
```

Next, refer to the invocation of **buildimages.sh** in **CodeTutorials/djangobox/src/docker/docker_wrapper/README.md** for information on setting up the Docker containers.

## CREATING A TUTORIAL

Refer to the file **djangobox/src/tutorials/HOWTO.md** to create a coding tutorial.

## STARTING THE SERVER

Make sure that you start the **docker.service** and **docker.socket** services:

```bash
# For Ubuntu and other systems that use 'systemd'
sudo systemctl start docker.service docker.socket
```

Once all the above instructions have been completed, you can run the following for development:

```bash
./manage.py runserver
```

## INFORMATION ON APACHE AND DEPLOYMENT USAGE

In order to allow Apache to use the docker containers, refer to the 1st paragraph of **PROPER PROJECT PERMISSIONING**.

The file **WSGI_Config.txt** contains the relevant lines that you'll want to put in your apache settings in order to run the project on an apache server (assuming the project is located at **/var/www/html/CodeTutorials/**). You must read some notes at the beginning of said file about proper filesystem paths if you are not using the default ones.  Otherwise, you should be able to just start your apache server and navigate to the relevant URLs of your choice.

The file **djangobox/src/CodeTutorials/urls.py** contains information about static URLs that MUST be heeded if putting the server into a deployment environment. If you're just developing, however, that shouldn't be a problem. Note that the following command (which is used to copy static files to the appropriate location before usage) will only work on apps listed under the **INSTALLED_APPS** variable in **djangobox/src/CodeTutorials/settings.py**:

```bash
./manage.py collectstatic
```

If you plan to deploy static files on the same server as Django, then, by default, the static files collected should be copied into (or their containing directory symlinked to) **/var/www/html/static/**.

Some values in the file **djangobox/src/CodeTutorials/settings.py** must be changed before putting the project into deployment. You will need to change:

- **DEBUG** to **False**
- **SECRET_KEY** to something else
- **ALLOWED_HOSTS** to include the hostnames that you will be serving from

## ADDITIONAL INFORMATION

If necessary, remove the database with:

```bash
rm ./db.sqlite3
```

To create a super user to help manage the server and model contents, run:

```bash
./manage.py createsuperuser
```

This will allow you to access **localhost:8000/admin/** (though the port will be different if you're running the development server (8000) versus apache (80)).