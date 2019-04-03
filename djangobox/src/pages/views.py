from django.shortcuts import render

# Create your views here.
def index(request, *args, **kwargs):
	return render(request, 'index.html', {})
# def uptest(request, *args, **kwargs):
# 	return render(request, 'uptest.html', {})
def codecorral(request, *args, **kwargs):
	return render(request, 'codecorral.html', {})

def home(request, *args, **kwargs):
	return render(request, 'home.html', {})

def main(request, *args, **kwargs):
	return render(request, 'main.html', {})

def signup(request, *args, **kwargs):
	return render(request, 'signup.html', {})
