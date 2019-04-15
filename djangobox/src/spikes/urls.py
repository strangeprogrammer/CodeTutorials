from django.urls import path

from .views import (
	uptest,
	editorPush,
	requestSpike,
	pathSpike,
	formPush,
	JSONDialog
	
	#Deprecated
	#codePush,
	#codeDialog,
)

app_name = 'spikes'

urlpatterns = [
	path('uptest/',		uptest,		name = 'Django is up and running!'),
	path('editorPush/',	editorPush),
	path('requestSpike/',	requestSpike,	name = 'requestSpike'),
	path('pathSpike/',	pathSpike,	name = 'pathSpike'),
	path('formPush/',	formPush,	name = 'formPush'),
	path('JSONDialog/',	JSONDialog,	name = 'JSONDialog'),
	
	#Deprecated
	#path('codePush/',	codePush,	name = 'codePush'),
	#path('codeDialog/',	codeDialog,	name = 'codeDialog'),
]
