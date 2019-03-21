from django.test import TestCase

from unittest.mock import patch

from docker.views import readIn

class mockfile:
	def __init__(self, retval):
		self.retval = retval
		self.opened = None
		self.rightwrite = False
	
	def __enter__(self):
		self.opened = True
		return self
	
	def __exit__(self, *args):
		self.close()
	
	def read(self):
		return self.retval
	
	def close(self):
		self.opened = False

class TestRead(TestCase):
	def test_readIn(self):
		# The mock function must patched against the tested module's version of the dependency function. More information at:
		# https://docs.python.org/3/library/unittest.mock.html#where-to-patch
		with patch('docker.views.open') as fakeopen:
			fakeopen.return_value = mf = mockfile('fakeoutput')
			
			retval = readIn('fakepath')
			
			fakeopen.assert_called_with('fakepath', 'r')
			assert mf.opened != None, "File wasn't opened properly..."
			assert mf.opened == False, "File wasn't closed properly..."
			assert retval == 'fakeoutput', "Wrong value was read from file..."
