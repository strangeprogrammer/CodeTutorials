from django.urls import path, include
from . import views

urlpatterns = [
	path('main/', views.main, name='main'),
	path('index/', views.index, name='index'),
	path('codecorral/',	views.codecorral, name='codecorral'),
	path('', views.redirect_view),
	path('summernote/',	include('django_summernote.urls')),
]

#If settings.DEBUG:
    #urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
