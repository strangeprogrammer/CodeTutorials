from django.shortcuts import render

def uptest(request, *args, **kwargs):
	return render(request, 'uptest.html', {})

def editorPush(request, *args, **kwargs):
	return render(request, 'editorpush.html', {})

def requestSpike(request, *args, **kwargs):
	context = { 'method': request.method or 'N/A', 'last': 'N/A', 'cookies': request.COOKIES }
	
	if request.method == 'POST':
		context['last'] = request.POST.get('key', default=None) or 'N/A'
	else:
		context['last'] = request.GET.get('key', default=None) or 'N/A'
	
	return render(request, 'requestSpike.html', context)
