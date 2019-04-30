import subprocess
import os

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
