"""CodeTutorials URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
	1. Add an import:  from my_app import views
	2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
	1. Add an import:  from other_app.views import Home
	2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
	1. Import the include() function: from django.urls import include, path
	2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
	path('admin/',		admin.site.urls),
	path('spikes/',		include('spikes.urls')),
	path('docker/',		include('docker.urls')),
	path('tutorials/',	include('tutorials.urls')),
	path('client/',		include('client.urls')),
]

# When putting the project into production, comment the following 4 lines (more information at the URL given afterward)
from CodeTutorials.settings import DEBUG
if DEBUG == True:
	from django.contrib.staticfiles.urls import staticfiles_urlpatterns
	urlpatterns += staticfiles_urlpatterns()
# https://docs.djangoproject.com/en/2.1/howto/static-files/#serving-static-files-during-development

# When putting the project into production, modify apache's configuration file to allow for static access to 'djangobox/src/static' using the information provided at the following URL (note, the relevant modifications are provided in '<project_root>/WSGI_Config.txt'):
# https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/modwsgi/#serving-files
