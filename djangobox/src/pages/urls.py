from django.contrib import admin
from django.urls import path, include
from . import views
from pages.views import index	#DMD
from django.views.generic.base import TemplateView

urlpatterns = [
	# path('admin/',admin.site.urls),
	path('accounts/',include('django.contrib.auth.urls')),
	path('accounts/', include('accounts.urls')),
	path('',views.home, name='home'),
	path('main/', views.main, name='main'),
	path('index/', views.index, name='index'),
	path('codecorral/',views.codecorral, name='codecorral'),
	path('signup/', views.signup, name='signup'),
]
