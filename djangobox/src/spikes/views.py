from django.shortcuts import render

def uptest(request, *args, **kwargs):
	return render(request, "uptest.html", {})
