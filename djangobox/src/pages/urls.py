from django.urls import path, include
from . import views
from pages.views import index	#DMD


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

urlpatterns = [
	path('main/',		views.main,		name='main'),
	path('index/',		views.index,		name='index'),
	path('codecorral/',	views.codecorral,	name='codecorral'),
	path('',		views.redirect_view),
	path('summernote/',	include('django_summernote.urls')),
]

#If settings.DEBUG:
    #urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
