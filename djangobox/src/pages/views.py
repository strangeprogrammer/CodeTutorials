from django.shortcuts import render

# Create your views here.
def index(request, *args, **kwargs):
	return render(request, 'index.html', {})
# def uptest(request, *args, **kwargs):
# 	return render(request, 'uptest.html', {})
def codecorral(request, *args, **kwargs):
	return render(request, 'codecorral.html', {})