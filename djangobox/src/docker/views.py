from django.shortcuts import render
from django.shortcuts import HttpResponse

from .models import SessionNum
from CodeTutorials.settings import BASE_DIR

from .tools import (
	readIn,
	writeOut,
	fragile,
)

from .dockerBackend import (
	runContainer,
)

import os
import shutil
import json

class SessionWrapper:
	def __init__(self):
		self.subject = SessionNum.objects.create()
	
	def getSubject(self):
		return self.subject
	
	def __enter__(self):
		return self
	
	def __exit__(self, *args):
		self.subject.delete()
	
	def __str__(self):
		return self.subject.num.__str__()

def runPOST(request, *args, **kwargs):
	STDOUT = ''
	STDERR = 'Couldn\'t run code properly...'
	retval = ''
	
	if request.method == 'POST':
		code = request.POST.get('code', default = None)
		STDIN = request.POST.get('STDIN', default = '')
		mode = request.POST.get('mode', default = None)
		
		if code and mode:
			try:
				with fragile(SessionWrapper()) as UUID: # Automatically handle the UUID's creation and deletion
					path = os.path.join(BASE_DIR, 'docker', 'docker_wrapper', UUID.__str__())
					
					os.mkdir(path)
					
					writeOut(code, os.path.join(path, 'code'))
					writeOut(STDIN, os.path.join(path, 'STDIN'))
					
					if runContainer(path, mode, UUID.__str__()) != 0:
						STDERR = 'An unexpected error occured...'
						raise fragile.Break
					
					retval = readIn(os.path.join(path,'retval'))
					STDOUT = readIn(os.path.join(path,'STDOUT'))
					STDERR = readIn(os.path.join(path,'STDERR'))
			except Exception as e:
				print(e)
				pass
			finally:
				shutil.rmtree(path) # It's possible to have a dangling directory if 'shutil.rmtree' fails, though the correct output will still be displayed on the screen
	
	return HttpResponse(json.dumps({'STDOUT':STDOUT, 'STDERR':STDERR, 'retval':retval}), content_type = 'text/plain')
