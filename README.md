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

Information to install docker can be found at the following URL:

[Docker Installation](https://docs.docker.com/install/)

You can find information specifically for Ubuntu installation here:

[Docker Installation Ubuntu](https://docs.docker.com/install/linux/docker-ce/ubuntu/#install-docker-ce)

Remember to install the **containerd.io**, **docker-ce-cli**, and **docker-ce** packages, in that order.

Installation of 'python3' and 'pip3' can be easily done through your package manager:

```bash
# For Linux distributions that use 'APT'
sudo apt install python3
sudo apt install python3-pip
```

Installation of 'virtualenv' is also easy once 'pip3' has been installed:

```bash
sudo pip3 install virtualenv
```

There are some other packages that need to be installed within the virtual environment that are listed in the **setup** section of this document.

## SETTING UP THE VIRTUAL ENVIRONMENT AND DJANGO

First, **git clone** the project repository into **/var/www/html/CodeTutorials/**. The following instructions assume that you (or the server user (apache)) will have been granted sufficient access to all of the rest of the files within the project.

You must also set up a python virtual environment (basically just allows you to keep a separate version of python and python packages on the system):

```bash
cd /var/www/html/CodeTutorials/
virtualenv -p python3 ./djangobox/
```

The following commands are what you should always use to anoint your command prompt with the virtual environment before performing development or package management:

```bash
cd ./djangobox
source ./bin/activate
```

The correct version of 'Django' can then be installed in the virtual environment along with 'Django-codemirror' and other neccesary packages:

```bash
pip3 install Django==2.1.7
pip3 install djangocodemirror
pip3 install django-summernote
pip3 install django-bootstrap3
```

The following command can then be used to exit the virtual environment:

```bash
deactivate
```

## PROPER PROJECT PERMISSIONING

In order for the server to be able to use docker, you must run the following command using the name of the owner of the project files (which is your own username for development purposes and 'www-data' for apache-related deployment purposes; it should be run one time each with either option for deployment development):

```bash
sudo usermod -aG docker [USER]
```

You must log-in again after running the previous command for the changes to take effect.

A tool named 'permutils.sh' has been provided to allow you greater control over permissions related to this project. Run the file with:

```bash
cd /var/www/html/CodeTutorials/
source ./permutils.sh
```

It will then provide you with some prompts. Once you have filled those out, the following functions (which require 'sudo' capabilities) will be available for you to use at the command line:

```bash
developer	[DIRECTORY]	# Changes all files under the given directory to the developer's owner and group
devdeploy	[DIRECTORY]	# Changes all files under the given directory to the developer's owner and the server's group
deployment	[DIRECTORY]	# Changes all files under the given directory to the server's owner and group
openaccess	[DIRECTORY]	# For all files under the given directory, grants file read and directory traversal permission to everyone
closeaccess	[DIRECTORY]	# For all files under the given directory, revokes all permissions from everyone except the owner
```

Depending on whether you are using the project solely for development, development of the deployment version, or deployment only, you should invoke the 'developer', 'devdeploy', or 'deployment' function (respectively). It only needs to be invoked upon the files that need to have their owner & group changed (this is almost exclusively 'CodeTutorials/djangobox/src' and files/directories within it, though you may have to run it every so often depending upon your 'umask' value).

Finally, you will have to give executable permissions to both the owner and group of the file 'CodeTutorials/djangobox/src/docker/docker_wrapper/runContainer.sh'.

To perform shell-level cleanup, the file 'unpermutils.sh' can be run like so:

```bash
cd /var/www/html/CodeTutorials/
source ./unpermutils.sh
```

## SETTING UP THE SERVER

To set up the database and statically hosted files, run:

```bash
cd /var/www/html/CodeTutorials/djangobox
source ./bin/activate
cd ./src
./manage.py makemigrations
./manage.py migrate
./manage.py collectstatic <<<"yes"
```

Next, refer to the invocation of **buildimages.sh** in **/var/www/html/CodeTutorials/djangobox/src/docker/docker_wrapper/README.md** for information on setting up the Docker containers.

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

The file **WSGI_Config.txt** contains the relevant lines that you'll want to put in your apache settings in order to run the project on an apache server (assuming the project is located at **/var/www/html/CodeTutorials**). You should be able to just start your apache server afterward and navigate to the relevant URLs of your choice.

The file **djangobox/src/CodeTutorials/urls.py** contains information about static URLs that MUST be heeded if putting the server into a deployment environment. If you're just developing, however, that shouldn't be a problem. Note that the following command (which is used to copy static files to the appropriate location before usage) will only work on apps listed under the **INSTALLED_APPS** variable in **djangobox/src/CodeTutorials/settings.py**:

```bash
./manage.py collectstatic
```

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
