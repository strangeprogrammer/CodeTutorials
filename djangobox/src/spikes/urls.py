from django.urls import path
from django.views.generic.base import TemplateView

from .views import (
	uptest,
	editorPush,
	editorTemplates,
	requestSpike,
	pathSpike,
	formPush,
    quizTutorial,
	CSRFSpike,
	quizUpload,
	editorRequest,
	editor,
	BasicSampleFormView,
	
	#Cannot be used without minor tweaks
	#JSONDialogV2,       #KEY = 58ufhd763
	#editorJSON,
)

app_name = 'spikes'

urlpatterns = [
	path('uptest/', uptest,	name = 'Django is up and running!'),
	path('editorPush/',	editorPush),
	path('editorTemplates/',	editorTemplates),
	path('requestSpike/', requestSpike,	name = 'requestSpike'),
	path('pathSpike/', pathSpike, name = 'pathSpike'),
	path('formPush/', formPush,	name = 'formPush'),
	path('CSRFSpike/', CSRFSpike, name = 'CSRFSpike'),
    path('quizTutorial/', quizTutorial, name = 'quizTutorial'),
	path('quizUpload/',	quizUpload,	name = 'quizUpload'),
	path('editorRequest/', editorRequest, name = 'editorRequest'),
	path('editor/', TemplateView.as_view(template_name = "editor.html"), name = 'editor'),
	path('form/', BasicSampleFormView.as_view(template_name = "form.html"),	name = 'codemirror-form'),
	
	#Cannot be used without minor tweaks
	#path('JSONDialogV2/', JSONDialogV2,	name = 'JSONDialogV2'),
	#path('editorJSON/', editorJSON,	name = 'editorJSON'),
]
