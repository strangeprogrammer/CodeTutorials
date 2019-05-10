from CodeTutorials.settings import BASE_DIR

from .tools import (
	readIn,
	writeOut,
	fragile,
)

import subprocess
import os
import shutil

def boxType(mode):
	if mode == 'C':
		box = 'gccbox'
	elif mode == 'R':
		box = 'rbox'
	elif mode == 'python':
		box = 'pythonbox'
	else:
		raise Exception()
	return box

def writeProg(path, code, STDIN):
	writeOut(code, os.path.join(path, 'code'))
	writeOut(STDIN, os.path.join(path, 'STDIN'))

def readProg(path, defaults):
	defaults['retval'] = readIn(os.path.join(path,'retval'))
	defaults['STDOUT'] = readIn(os.path.join(path,'STDOUT'))
	defaults['STDERR'] = readIn(os.path.join(path,'STDERR'))
	return defaults

# Makes sure the value of 'mode' is valid and runs the program provided by the client
def runContainer(code, STDIN, mode, UUIDstr, defaults):
	try:
		path = os.path.join(BASE_DIR, 'docker', 'docker_wrapper', UUIDstr)
		os.mkdir(path)
		writeProg(path, code, STDIN)
		
		dockerPath = os.path.join(BASE_DIR, 'docker', 'docker_wrapper', 'runContainer.sh')
		if subprocess.call([dockerPath, path, boxType(mode), UUIDstr]) != 0:
			defaults['STDERR'] = 'An unexpected error occured...'
			raise fragile.Break
		
		defaults = readProg(path, defaults.copy())
	except fragile.Break:
		raise fragile.Break
	except Exception as e:
		print(e)
	finally:
		shutil.rmtree(path) # It's possible to have a dangling directory if 'shutil.rmtree' fails (unlikely), though the correct output will still be displayed on the screen
	
	return defaults
