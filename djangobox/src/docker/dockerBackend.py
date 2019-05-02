from CodeTutorials.settings import BASE_DIR

import subprocess
import os

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

# Makes sure the value of 'mode' is valid and runs the program provided by the client
def runContainer(path, mode, contname):
	return subprocess.call([os.path.join(BASE_DIR, 'docker', 'docker_wrapper', 'runContainer.sh'), path, boxType(mode), contname])
