# Read in a whole file and return it
def readIn(path):
	try:
		with open(path, 'r') as f:
			retval = f.read() # Read everything
			f.close()
			return retval
	except Exception:
		return ''

# Write out a whole string to a file
def writeOut(string, path):
	with open(path, 'w') as f:
		f.write(string)
		f.close()

#Best way I've seen around skip-ahead goto's in a high-level language so far:
#https://stackoverflow.com/a/23665658
class fragile:
	class Break(Exception):
		"""Break out of the with statement"""
	
	def __init__(self, value):
		self.value = value
	
	def __enter__(self):
		return self.value.__enter__()
	
	def __exit__(self, etype, value, traceback):
		error = self.value.__exit__(etype, value, traceback)
		if etype == self.Break:
			return True
		return error
