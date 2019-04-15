from django.shortcuts import render
from django.http import HttpResponse
import os

from django.views.generic.edit import FormView
from django.urls import reverse
from .forms import SampleForm

import sys
import docker

from docker.views import (
	writeOut,
	runContainer,
	readIn,
	SessionWrapper,
	runPOST
)



def uptest(request, *args, **kwargs):
	return render(request, 'uptest.html', {})

def editor(request, *args, **kwargs):		#DMD
	return render(request, 'editor.html', {})

def spike1(request, *args, **kwargs):		#DMD
	context = { 'method': request.method or 'N/A', 'last': 'N/A', 'cookies': request.COOKIES }
	print(request.POST)
	context['last'] = request.POST.get('key', default=None) or 'N/A'
	writeOut(context['last'], 'spikes/temp/tempdoc.txt')
	return render(request, 'spike1.html', context)

class BasicSampleFormView(FormView):
    template_name = 'form.html'
    form_class = SampleForm
    def get_success_url(self):
    return reverse('codemirror-form')


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

def JSONDialog(request, *args, **kwargs):
	return render(request, "JSONDialog.html", {})

#Deprecated
"""
def codePush(request, *args, **kwargs):
	return render(request, "codePush.html", {})

def codeDialog(request, *args, **kwargs):
	return render(request, "codeDialog.html", {})
"""
