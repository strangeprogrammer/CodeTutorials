from django.shortcuts import render
from CodeTutorials.settings import UNITTEST

if UNITTEST:
	def codeClient_unit(request, *args, **kwargs):
		return render(request, "tests/codeClient_unit.html", {})
	
	def boxSetup_unit(request, *args, **kwargs):
		return render(request, "tests/boxSetup_unit.html", {})
