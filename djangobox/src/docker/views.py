from django.shortcuts import render
from django.shortcuts import HttpResponse

from CodeTutorials.settings import BASE_DIR

from .tools import (
	fragile,
	SessionWrapper,
)

from .dockerBackend import runContainer

import json

def runPOST(request, *args, **kwargs):
	output = {	'STDOUT':'',
			'STDERR':'SERVER: Couldn\'t run code properly...',
			'retval':'',
	}
	if request.method == 'POST':
		code	= request.POST.get('code', default = '')
		STDIN	= request.POST.get('STDIN', default = '')
		mode	= request.POST.get('mode', default = None)
		
		if code and mode:
			with fragile(SessionWrapper()) as UUID: # Automatically handle the UUID's creation and deletion
				output = runContainer(code, STDIN, mode, UUID.__str__(), output)
	
	return HttpResponse(json.dumps(output), content_type = 'text/plain')
