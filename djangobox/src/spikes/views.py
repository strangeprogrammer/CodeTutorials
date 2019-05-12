from django.shortcuts import render

from django.views.generic.edit import FormView
from django.urls import reverse
from .forms import SampleForm
from django.http import HttpResponse

import os

def uptest(request, *args, **kwargs):
	return render(request, 'uptest.html', {})

def editor(request, *args, **kwargs):		#DMD
	return render(request, 'editor.html', {})

def editorRequest(request, *args, **kwargs):		
	context = { 'method': request.method or 'N/A', 'last': 'N/A', 'cookies': request.COOKIES }
	print(request.POST)
	context['last'] = request.POST.get('key', default=None) or 'N/A'
	
	return render(request, 'editorRequest.html', context)

def editorJSON(request, *args, **kwargs):		#DMD
	return render(request, "editorJSON.html", {})

def pathSpike(request, *args, **kwargs):
	print(os.path.abspath("."))
	return HttpResponse("Check the console!", content_type = 'text/plain')

def formPush(request, *args, **kwargs):
	return render(request, "formPush.html", {})

# Deprecated
# def JSONDialog(request, *args, **kwargs):
#	return render(request, "JSONDialog.html", {})

def JSONDialogV2(request, *args, **kwargs):
	return render(request, "JSONDialogV2.html", {})



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
