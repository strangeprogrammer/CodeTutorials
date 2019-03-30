from django.shortcuts import render

from django.http import HttpResponse
from docker.models import SessionNum
from CodeTutorials.settings import BASE_DIR
import subprocess
import os
import shutil

def writeOut(string, path):
	with open(path, 'w') as f:
		f.write(string)
		f.close()

def runContainer(path, mode):
	if mode == 'C':
		box = 'gccbox'
	elif mode == 'R':
		box = 'rbox'
	elif mode == 'python':
		box = 'pythonbox'
	else:
		raise Exception()
	return subprocess.call([os.path.join(BASE_DIR, 'docker', 'docker_wrapper', 'runContainer.sh'), path, box])

def readIn(path):
	with open(path, 'r') as f:
		retval = f.read() # Read everything
		f.close()
		return retval

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
	response = "Couldn't run code properly..."
	
	if request.method == 'POST':
		code = request.POST.get('code', default = None)
		STDIN = request.POST.get('STDIN', default = None)
		mode = request.POST.get('mode', default = None)
		
		if code and STDIN:
			try:
				with SessionWrapper() as UUID: # Automatically handle the UUID's creation and deletion
					path = os.path.join(BASE_DIR, "docker", "docker_wrapper", UUID.__str__())
					try:
						os.mkdir(path)
						
						try:
							writeOut(code, os.path.join(path, 'code'))
							writeOut(STDIN, os.path.join(path, 'STDIN'))
							runContainer(path, mode) # This function checks 'mode' on its own
							response = readIn(os.path.join(path,'STDOUT'))
						except Exception:
							pass
						
						shutil.rmtree(path)
					except Exception:
						# It's possible to have a dangling directory if 'shutil.rmtree' fails, though the correct output will still be displayed on the screen
						pass
			except Exception:
				pass
	
	return HttpResponse(response, content_type = 'text/plain')
