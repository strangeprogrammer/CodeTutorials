### BEGIN COPYRIGHT NOTICE

# Copyright 2019 Stephen Fedele <stephen.m.fedele@wmich.edu>, Daniel Darcy, Timothy Curry
# 
# This file is part of CodeTutorials.
# 
# CodeTutorials is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
# 
# CodeTutorials is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with CodeTutorials.  If not, see <https://www.gnu.org/licenses/>.

### END COPYRIGHT NOTICE

from CodeTutorials.settings import (
	BASE_DIR,
	CONT_TMP_PATH,
)

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
		path = os.path.join(CONT_TMP_PATH, UUIDstr)
		os.makedirs(path)
		writeProg(path, code, STDIN)
		
		dockerPath = os.path.join(BASE_DIR, 'docker', 'docker_wrapper', 'runContainer.sh')
		if subprocess.call([dockerPath, path, boxType(mode), UUIDstr]) != 0:
			defaults['STDERR'] = 'SERVER: An unexpected error occured...'
			raise fragile.Break
		
		defaults = readProg(path, defaults.copy())
	except fragile.Break:
		raise fragile.Break
	except Exception as e:
		print(e)
	finally:
		shutil.rmtree(path) # It's possible to have a dangling directory if 'shutil.rmtree' fails (unlikely), though the correct output may still be displayed on the screen
	
	return defaults
