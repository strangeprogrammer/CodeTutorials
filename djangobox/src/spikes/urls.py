from django.urls import path
from .views import (
	uptest,
	editorPush,
	requestSpike,
    pathSpike,
    formPush,
    JSONDialog,
    editorJSON

	#Deprecated
	#codePush,
	#codeDialog,
)

from docker.views import runPOST

app_name = 'spikes'

urlpatterns = [
	path('uptest/',		uptest,		name = 'Django is up and running!'),
	path('editorPush/',	editorPush),
	path('requestSpike/',	requestSpike,	name = 'requestSpike'),
	path('pathSpike/',	pathSpike,	name = 'pathSpike'),
	path('formPush/',	formPush,	name = 'formPush'),
	path('JSONDialog/',	JSONDialog,	name = 'JSONDialog'),
    path('editorJSON/', editorJSON, name = 'editorJSON'),

	#Deprecated
	#path('codePush/',	codePush,	name = 'codePush'),
	#path('codeDialog/',	codeDialog,	name = 'codeDialog'),
]
