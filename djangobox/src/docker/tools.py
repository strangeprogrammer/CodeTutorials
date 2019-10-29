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

from .models import SessionNum
from CodeTutorials.settings import (
	CONT_MAXINPUT,
	CONT_MAXOUTPUT,
)
from contextlib import closing

# Read in a whole file and return it
def readIn(path):
	try:
		with closing(open(path, 'r')) as f:
			retval = f.read(CONT_MAXOUTPUT) # Read everything
			return retval
	except Exception:
		return ''

# Write out a whole string to a file
def writeOut(string, path):
	with closing(open(path, 'w')) as f:
		f.write(string[0:CONT_MAXINPUT])

#Best way I've seen around skip-ahead goto's in a high-level language so far:
#https://stackoverflow.com/a/23665658
class fragile:
	class Break(Exception):
		"""Break out of the 'with' statement"""
	
	def __init__(self, value):
		self.value = value
	
	def __enter__(self):
		return self.value.__enter__()
	
	def __exit__(self, etype, value, traceback):
		error = self.value.__exit__(etype, value, traceback)
		if etype == self.Break:
			return True
		return error

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
