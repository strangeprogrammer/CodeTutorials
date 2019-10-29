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

from django.shortcuts import render

from django.views.generic.edit import FormView
from django.urls import reverse
from .forms import SampleForm
from django.http import HttpResponse
from .writeTofiles import (
    addView,
    addURL,
    importFromViews,
    addHtmlPage,
)

import os

from CodeTutorials.settings import (
    CONT_GRACE,
    CONT_TIMEOUT,
)

def uptest(request, *args, **kwargs):
    return render(request, 'uptest.html', {})

def editor(request, *args, **kwargs):		#DMD
    return render(request, 'editor.html', {})

def editorRequest(request, *args, **kwargs):
    context = { 'method': request.method or 'N/A', 'last': 'N/A', 'cookies': request.COOKIES }
    #print(request.POST)
    context['last'] = request.POST.get('key', default=None) or 'N/A'
    return render(request, 'editorRequest.html', context)


def quizUpload(request, *args, **kwargs):
    context = { 'method': request.method or 'N/A', 'last': 'N/A', 'cookies': request.COOKIES }
    print(request.POST)  #TEST
    context['htmlCode'] = request.POST.get('key', default=None) or 'N/A'
    context['page'] = request.POST.get('pageName', default=None) or 'N/A'
    if context['page'] != 'N/A':
        addHtmlPage(context['page'], context['htmlCode'])

    return render(request, 'quizUpload.html', context)


def editorJSON(request, *args, **kwargs):		#DMD
    return render(request, "editorJSON.html", {})

def quizTutorial(request, *args, **kwargs):        #DMD
    return render(request, "quizTutorial.html", {})

def pathSpike(request, *args, **kwargs):
    print(os.path.abspath("."))
    return HttpResponse("Check the console!", content_type = 'text/plain')

def formPush(request, *args, **kwargs):
    return render(request, "formPush.html", {})

def JSONDialogV2(request, *args, **kwargs):
    return render(request, "JSONDialogV2.html", {'timeout': (CONT_GRACE + CONT_TIMEOUT) * 1000})

def CSRFSpike(request, *args, **kwargs):
    return render(request, "CSRFSpike.html", {})


class BasicSampleFormView(FormView):
    template_name = 'form.html'
    form_class = SampleForm
    def get_success_url(self):
        return reverse('codemirror-form')


def editorPush(request, *args, **kwargs):
    return render(request, 'editorpush.html', {})

def editorTemplates(request, *args, **kwargs):
    return render(request, 'editorTemplates/main.html', {})


def requestSpike(request, *args, **kwargs):
    context = { 'method': request.method, 'last': '', 'cookies': request.COOKIES }

    if request.method == 'POST':
        context['last'] = request.POST.get('key', default=None) or ''
    elif request.method == 'GET':
        context['last'] = request.GET.get('key', default=None) or ''

    return render(request, 'requestSpike.html', context)
