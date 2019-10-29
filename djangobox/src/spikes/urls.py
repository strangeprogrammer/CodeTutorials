### BEGIN COPYRIGHT NOTICE

# Copyright 2019 Stephen Fedele <stephen.m.fedele@wmich.edu>, Daniel Darcy, Timothy Curry
# 
# This file is part of CodeTutorials.
# 
# CodeTutorials is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
# 
# CodeTutorials is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with CodeTutorials.  If not, see <https://www.gnu.org/licenses/>.

### END COPYRIGHT NOTICE

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
