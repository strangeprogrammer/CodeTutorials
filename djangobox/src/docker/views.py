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
