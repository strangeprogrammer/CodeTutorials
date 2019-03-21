from django.test import TestCase

from docker.models import SessionNum
from docker.views import SessionWrapper

class SessionWrapperTest(TestCase):
	def test_withable(self):
		"""Test that the wrapper class can be used with the keyword 'with'"""
		# Check that the query set has nothing in it to start with
		assert len(SessionNum.objects.all()) == 0, 'SessionNum object list is the wrong size...'
		
		with SessionWrapper() as dummy:
			# Check that the query set has 'dummy' in it
			assert dummy.subject in SessionNum.objects.all(), 'Couldn\'t find dummy in SessionNum object list...'
			# Check that the query set has 1 element in it
			assert len(SessionNum.objects.all()) == 1, 'SessionNum object list is the wrong size...'
		
		# Check that the query set has nothing in it to end with
		assert len(SessionNum.objects.all()) == 0, 'SessionNum object list is the wrong size...'
	
	def test_str(self):
		with SessionWrapper() as dummy:
			assert dummy.__str__() == dummy.subject.num.__str__()
