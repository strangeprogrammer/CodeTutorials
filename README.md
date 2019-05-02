# CodeTutorials

##SETTING UP THE VIRTUAL ENVIRONMENT AND DJANGO

In order to be able to use this project, you will have to set up a python virtual environment (basically just allows you to keep a separate version of python and python packages on the system). This can be done with the following commands on Linux (which should all be done in the context of a system using 'python3'):

	# At least this version of 'virtualenv' should be used
	pip3 install virtualenv==16.4.1
	cd /var/www/html/CodeTutorials
	virtualenv -p python3 ./djangobox

The following commands are what you should always use to anoint your command prompt with the virtual environment before performing development or package management:

	cd ./djangobox
	source ./bin/activate

The correct version of 'Django' can then be installed in the virtual environment:

	pip3 install Django==2.1.7

Along with 'Django-codemirror' and other neccesary packages:

      pip install djangocodemirror
      pip install django-summernote
      pip install django-bootstrap3

The following command can then be used to exit the virtual environment:

	deactivate

## SETTING UP THE SERVER

To set up the database and statically hosted files, run:

	cd /var/www/html/CodeTutorials/djangobox
	source ./bin/activate
	cd ./src
	./manage.py makemigrations
	./manage.py migrate
	./manage.py collectstatic <<<"yes"

Next, refer to the invocation of **buildimages.sh** in **/var/www/html/CodeTutorials/djangobox/src/docker/docker_wrapper/README.md** for information on setting up the Docker containers.

Once all the above instructions have been completed, you can run the following for development:

	./manage.py runserver

## INFORMATION ON APACHE AND PRODUCTION LEVEL USAGE

The file **WSGI_Config.txt** contains the relevant lines that you'll want to put in your apache settings in order to run the project on an apache server (assuming the project is located at **/var/www/html/CodeTutorials**). You should be able to just start your apache server afterward and navigate to the relevant URLs of your choice.

The file **djangobox/src/CodeTutorials/urls.py** contains information about static URLs that MUST be heeded if putting the server into a production environment. If you're just developing, however, that shouldn't be a problem. Note that the following command (which is used to copy static files to the appropriate location before usage) will only work on apps listed under the **INSTALLED_APPS** variable in **djangobox/src/CodeTutorials/settings.py**.

	./manage.py collectstatic

Finally, the value of **SECRET_KEY** in the file **djangobox/src/CodeTutorials/settings.py** must be changed before putting the project into production.

## ADDITIONAL INFORMATION

If necessary, remove the database with

	rm ./db.squlite3

To create a super user to help manage the server and model contents, run

	./manage.py createsuperuser

This will allow you to access **localhost:8000/admin/** (though the port will be different if you're running the development server (8000) versus apache (80)).
