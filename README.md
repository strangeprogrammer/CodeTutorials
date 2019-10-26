# CodeTutorials

#### MINIMUM SYSTEM REQUIREMENTS
---

All commands referenced throughout this document should be run in the context of a system using **python3** via **BASH** or some similar shell running on **Ubuntu** (preferably, within a virtual machine).

This is a list of software and their minimum versions required on the host in order to use the code provided by this project:

```
# Docker packages
containerd.io v.1.2.4
docker-ce-cli v.18.09.3
docker-ce v.18.09.3

# Python packages
python3 v.3.5.3
pip3 (python3-pip) v.9.0.1
virtualenv v.15.1.0

# For development-deployment and deployment only installations
apache2 v.2.4.29
libapache2-mod-wsgi-py3 v.4.5.17

# Misc
git v.2.17.1
```

Information to install Docker can be found at the following URL:

[Docker Installation](https://docs.docker.com/install/)

You can find information specifically for an Ubuntu installation of Docker here:

[Docker Installation Ubuntu](https://docs.docker.com/install/linux/docker-ce/ubuntu/#install-docker-ce)

Remember to install the **containerd.io**, **docker-ce-cli**, and **docker-ce** packages, in that order.

Installation of **python3**, **pip3 (python3-pip)**, **virtualenv**, **apache2**, **libapache2-mod-wsgi-py3**, and **git** can be easily done through your package manager:

```bash
sudo apt install python3 python3-pip virtualenv apache2 libapache2-mod-wsgi-py3 git
```

#### PRE-INSTALLATION
---

First, if the directory **/var/www/html/** does not exist, you may create it now in order to clone the project properly:

```bash
sudo mkdir -p /var/www/html/
sudo chmod 1777 /var/www/html/ # '1777' is an example directory mode which comes in useful for the next step
cd /var/www/html/
```

Next, `git clone` the project repository into **CodeTutorials/**:

```bash
git clone https://github.com/strangeprogrammer/CodeTutorials ./CodeTutorials/
```

#### INFORMATION ON APACHE AND DEPLOYMENT MODE
---

NOTE: The information within this section is specific to projects that use either the development deployment or deployment mode.

If you will not be installing the project at **/var/www/html/CodeTutorials/** or if you will not be using the path **/var/www/html/static/** for static files then you must read some notes at the beginning of **CodeTutorials/wsgi/wsgi_codetutorials.conf** about proper paths for this project (and if the latter point is the case, you will also need to edit **install.sh** slightly).

Some values in the file **CodeTutorials/djangobox/src/CodeTutorials/settings.py** must be changed as well. You will need to change:

- **DEBUG** to **False**
- **ALLOWED_HOSTS** to include the hostnames that you will be serving from

#### INSTALLATION
---

`cd` into the project directory and run the installer program:

```bash
cd ./CodeTutorials/
./install.sh # Use '-v' for verbose output
```

You will then be provided with some prompts from 'devtools.sh' to fill out (more on this later), after which the installation process will proceed normally. In order to use Docker properly once the installation is finished, you may need to log out and then back in.

The automatic installation process consists of the following steps:

1. Determine whether the project is for development, development of the deployment version, or deployment
2. Initialize **devtools.sh** settings
3. Update project permissions and ownership according to the type of installation from step '1'
4. Set up virtual environment
5. Install python packages in virtual environment
6. Add developer to group 'docker' and/or add server user to group 'docker' according to the type of installation from step '1'
7. Generate a secret key for Django
8. Set up database for Django
9. Update files in Django's static directory
10. Build Docker images 'gccbox', 'rbox', and 'pythonbox'
11. If the installation type from step '1' is either development deployment or deployment, symlink Django's static directory so that Apache can find it
12. If the installation type from step '1' is either development deployment or deployment, copy some WSGI configuration files so that Apache can find them

#### DEVELOPMENT TOOLS
---

A toolbox named **devtools.sh** has been provided to give you some shortcuts for oft-used commands related to this project. To use these shortcuts in your shell, run:

```bash
cd /var/www/html/CodeTutorials/
source ./devtools.sh
```

If this is the first time you are using **devtools.sh**, it will then provide you with some prompts to fill out in order to properly configure some parameters for the following shortcuts (which may require `sudo` capabilities):

```bash
developer	[DIRECTORY]	# Changes all files under the given directory to the developer's owner and group
devdeploy	[DIRECTORY]	# Changes all files under the given directory to the developer's owner and the server's group
deployment	[DIRECTORY]	# Changes all files under the given directory to the server's owner and group
openaccess	[DIRECTORY]	# For all files under the given directory, grants file read and directory traversal permission to everyone
closeaccess	[DIRECTORY]	# For all files under the given directory, revokes all permissions from everyone except the owner
openproj				# Calls 'openaccess' upon 'CodeTutorials/djangobox/src/' and deals with a pesky file's permissions
closeproj				# Calls 'closeaccess' upon 'CodeTutorials/djangobox/src/' and deals with a pesky file's permissions
startserver				# Starts the server
stopserver				# Stops the server
collectstatic			# Updates files in Django's 'static' directory
```

Sometimes, if you are developing the deployment version of this project, Apache will be unable to read a necessary file or open a necessary directory due to permission issues. In that case, simply running `devdeploy` and `openaccess` upon the file or directory should clear the problem. This is unlikely to ever happen with the development or deployment only project modes, though, if it does, you can take similar steps using `developer` and `deployment`. This issue is primarily caused by your 'umask' value.

To deactivate the developer tools, simply run the following:

```bash
undevtools
```

#### DJANGO'S VIRTUAL ENVIRONMENT
---

The following commands are what you should always use to anoint your command prompt with the virtual environment before performing development or python package management:

```bash
cd /var/www/html/CodeTutorials/djangobox/
source ./bin/activate
```

This is because **CodeTutorials/djangobox/src/manage.py** relies upon the virtual environment being active in order to work properly.

The following command can be used to exit the virtual environment:

```bash
deactivate
```

#### CREATING A TUTORIAL
---

Refer to the file **CodeTutorials/djangobox/src/tutorials/HOWTO.md** to create a coding tutorial.

#### ADDITIONAL INFORMATION
---

If necessary, remove the database with:

```bash
rm ./db.sqlite3
```

To create a super user to help manage the server and model contents, run:

```bash
./manage.py createsuperuser
```

This will allow you to access **localhost:8000/admin/** (though the port will be different if you're running the development server (8000) versus apache (80)).