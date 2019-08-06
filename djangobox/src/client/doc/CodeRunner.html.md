# DOCUMENTING ../templates/client/CodeRunner.html

- Template 'CodeRunner.html':
	- Environment Variables:
		- defaultlang: The programming language to be used
	- No Blocks
	- Notes:
		- Since the CSRF token is rendered here, it needn't be rendered in the including file (though it wouldn't cause anything bad to happen if it was).