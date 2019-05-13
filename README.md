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

In order for the server to be able to use docker, you must run the following command using the name of the owner of the project files (which is your own username for development purposes, and 'apache' for production purposes):

```bash
sudo usermod -aG docker [USER]
```

You must log-in again after running the command for the changes to take effect.

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

## INFORMATION ON APACHE AND PRODUCTION LEVEL USAGE

The file **WSGI_Config.txt** contains the relevant lines that you'll want to put in your apache settings in order to run the project on an apache server (assuming the project is located at **/var/www/html/CodeTutorials**). You should be able to just start your apache server afterward and navigate to the relevant URLs of your choice.

The file **djangobox/src/CodeTutorials/urls.py** contains information about static URLs that MUST be heeded if putting the server into a production environment. If you're just developing, however, that shouldn't be a problem. Note that the following command (which is used to copy static files to the appropriate location before usage) will only work on apps listed under the **INSTALLED_APPS** variable in **djangobox/src/CodeTutorials/settings.py**:

```bash
./manage.py collectstatic
```

Finally, the value of **SECRET_KEY** in the file **djangobox/src/CodeTutorials/settings.py** must be changed before putting the project into production.

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