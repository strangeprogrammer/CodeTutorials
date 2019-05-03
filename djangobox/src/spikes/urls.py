from django.urls import path
from django.views.generic.base import TemplateView

from .views import (
	uptest,
	editorPush,
	requestSpike,
	pathSpike,
	formPush,
	JSONDialog,
	editorJSON,
	
	#Deprecated
	#codePush,
	#codeDialog,
	editorRequest,
	editor,
	BasicSampleFormView,
)

from docker.views import runPOST

app_name = 'spikes'

urlpatterns = [
	path('uptest/',		uptest,								name = 'Django is up and running!'),
	path('editorPush/',	editorPush),
	path('requestSpike/',	requestSpike,	name = 'requestSpike'),
	path('pathSpike/',	pathSpike,	name = 'pathSpike'),
	path('formPush/',	formPush,	name = 'formPush'),
	path('JSONDialog/',	JSONDialog,	name = 'JSONDialog'),
	path('editorJSON/',	editorJSON,	name = 'editorJSON'),
	path('editorRequest/',	editorRequest,	name = 'editorRequest'),
	path('editor/',		TemplateView.as_view(template_name = "editor.html"),		name = 'editor'),
	path('form/',		BasicSampleFormView.as_view(template_name = "form.html"),	name = 'codemirror-form'),

	#Deprecated
	#path('codePush/',	codePush,	name = 'codePush'),
	#path('codeDialog/',	codeDialog,	name = 'codeDialog'),

]
