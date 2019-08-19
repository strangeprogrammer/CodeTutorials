from django.urls import path
from CodeTutorials.settings import UNITTEST

app_name = 'client'

if UNITTEST:
	from .views import (
		codeClient_unit,
		boxSetup_unit,
	)
	
	urlpatterns = [
		path('codeClient_unit/',	codeClient_unit),
		path('boxSetup_unit/',		boxSetup_unit),
	]
else:
	urlpatterns = []
