from django.test import TestCase

from unittest.mock import patch

from docker.views import writeOut

class mockfile:
	def __init__(self, expected):
		self.expected = expected
		self.opened = None
		self.rightwrite = False
	
	def __enter__(self):
		self.opened = True
		return self
	
	def __exit__(self, *args):
		self.close()
	
	def write(self, string):
		if self.expected == string:
			self.rightwrite = True
	
	def close(self):
		self.opened = False

class TestWrite(TestCase):
	def test_writeOut(self):
		# The mock function must patched against the tested module's version of the dependency function. More information at:
		# https://docs.python.org/3/library/unittest.mock.html#where-to-patch
		with patch('docker.views.open') as fakeopen:
			fakeopen.return_value = mf = mockfile('fakeoutput')
			
			writeOut('fakeoutput','fakepath')
			
			fakeopen.assert_called_with('fakepath', 'w')
			assert mf.opened != None, "File wasn't opened properly..."
			assert mf.opened == False, "File wasn't closed properly..."
			assert mf.rightwrite, "Wrong value was written to file..."
