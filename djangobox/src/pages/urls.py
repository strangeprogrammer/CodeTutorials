from django.contrib import admin
from django.urls import path, include
from . import views
from django.views.generic.base import TemplateView

urlpatterns = [
	# path('admin/',admin.site.urls),
	path('accounts/',include('django.contrib.auth.urls')),
	path('',views.index, name='index'),
	path('codecorral/',views.codecorral, name='codecorral'),
]