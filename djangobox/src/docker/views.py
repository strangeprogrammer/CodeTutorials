from django.shortcuts import render
from django.shortcuts import HttpResponse

from .models import SessionNum
from CodeTutorials.settings import BASE_DIR
import subprocess
import os
import shutil
import json

def writeOut(string, path):
	with open(path, 'w') as f:
		f.write(string)
		f.close()

# Makes sure the value of 'mode' is valid and runs the program provided by the client
def runContainer(path, mode, contname):
	if mode == 'C':
		box = 'gccbox'
	elif mode == 'R':
		box = 'rbox'
	elif mode == 'python':
		box = 'pythonbox'
	else:
		raise Exception()
	return subprocess.call([os.path.join(BASE_DIR, 'docker', 'docker_wrapper', 'runContainer.sh'), path, box, contname])

def readIn(path):
	try:
		with open(path, 'r') as f:
			retval = f.read() # Read everything
			f.close()
			return retval
	except Exception:
		return ''

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

#Best way I've seen around skip-ahead goto's in a high-level language so far:
#https://stackoverflow.com/a/23665658
class fragile:
	class Break(Exception):
		"""Break out of the with statement"""
	
	def __init__(self, value):
		self.value = value
	
	def __enter__(self):
		return self.value.__enter__()
	
	def __exit__(self, etype, value, traceback):
		error = self.value.__exit__(etype, value, traceback)
		if etype == self.Break:
			return True
		return error

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
