# CodeTutorials

# SETTING UP THE VIRTUAL ENVIRONMENT AND DJANGO

In order to be able to use this project, you will have to set up a python virtual environment (basically just allows you to keep a separate version of python and python packages on the system). This can be done with the following commands on Linux (which should all be done in the context of a system using 'python3'):

# At least this version of 'virtualenv' should be used
pip3 install virtualenv==16.4.1
cd /var/www/html/CodeTutorials
virtualenv -p python3 ./djangobox

The following commands are what you should always use to anoint your command prompt with the virtual environment before performing development or package management:

cd ./djangobox
source ./bin/activate

The correct version of 'Django' can then be installed in the virtual environment:

pip install Django==2.1.7

The following command can then be used to exit the virtual environment:

deactivate

# INFORMATION ON APACHE USAGE

The file 'WSGI_Config.txt' contains the relevant lines that you'll want to put in your apache settings in order to run the project on an apache server (assuming it's located at '/var/www/html/CodeTutorials'). You should be able to just start your apache server afterward and navigate to the relevant URLs of your choice.  
