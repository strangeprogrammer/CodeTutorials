from django.shortcuts import render

from django.http import HttpResponse
from docker.models import SessionNum
import os
import shutil

def writeOut(string, path):
	with open(path, 'w') as f:
		f.write(string)
		f.close()

# TODO: Implement me
def runContainer(path):
	pass

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
		
		if code and STDIN:
			with SessionWrapper() as UUID: # Automatically handle the UUID's creation and deletion
				path = UUID.__str__()
				try:
					os.mkdir(path)
					
					try:
						writeOut(code, os.path.join(path, 'code'))
						writeOut(STDIN, os.path.join(path, 'STDIN'))
						runContainer(path)
						response = readIn(os.path.join(path,'STDOUT'))
					except Exception:
						pass
					
					shutil.rmtree(path)
				except Exception:
					# It's possible to have a dangling directory if 'shutil.rmtree' fails, though the correct output will still be displayed on the screen
					pass
	
	return HttpResponse(response, content_type = 'text/plain')
