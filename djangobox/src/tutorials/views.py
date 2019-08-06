from django.shortcuts import render

def renderTutorial(request, *args, **kwargs):
	return render(request, "tutorials/" + str(kwargs["tutorialname"]) + "/main.html", {})
