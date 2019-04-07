from django.shortcuts import render
from django.http import HttpResponse
import os

def uptest(request, *args, **kwargs):
	return render(request, 'uptest.html', {})

def editorPush(request, *args, **kwargs):
	return render(request, 'editorpush.html', {})

def requestSpike(request, *args, **kwargs):
	context = { 'method': request.method or 'N/A', 'last': 'N/A', 'cookies': request.COOKIES }
	
	if request.method == 'POST':
		print(request.POST)
		context['last'] = request.POST.get('key', default=None) or 'N/A'
	else:
		print(request.GET)
		context['last'] = request.GET.get('key', default=None) or 'N/A'
	
	return render(request, 'requestSpike.html', context)

def pathSpike(request, *args, **kwargs):
	print(os.path.abspath("."))
	return HttpResponse("Check the console!", content_type = 'text/plain')

def formPush(request, *args, **kwargs):
	return render(request, "formPush.html", {})

#Deprecated
"""
def codePush(request, *args, **kwargs):
	return render(request, "codePush.html", {})
"""

def codeDialog(request, *args, **kwargs):
	return render(request, "codeDialog.html", {})
