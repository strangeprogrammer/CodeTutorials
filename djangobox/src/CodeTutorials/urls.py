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
from django.urls import path

from spikes.views import (
	uptest,
	editorpush,
)

urlpatterns = [
	path('admin/', admin.site.urls),
	path('spikes/uptest/', uptest, name="Django is up and running!"),
	path('spikes/editorpush/', editorpush),
]

# When not putting the project into production, leave the following 3 lines uncommented (more information at the URL given afterward)
from django.conf import settings
from django.conf.urls.static import static
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# https://docs.djangoproject.com/en/2.1/howto/static-files/#serving-static-files-during-development

# FIXME: Update the note on the next line
# When putting the project into production, modify apache's configuration file to allow for static access to 'djangobox/src/static' using the information provided at the following URL:
# https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/modwsgi/#serving-files
