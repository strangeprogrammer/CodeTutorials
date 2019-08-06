# DOCUMENTING ../templates/client/CodeBox.html

- Template 'CodeBox.html':
	- Environment Variables:
		- id: The HTML id associated with this editor
	- Blocks:
		- preamble: HTML associated with the editor that comes before everything else
		- presetcode: Code loaded into the editor when the page loads
		- presetSTDIN: STDIN loaded into the editor when the page loads
		- codelang: The programming language to be used
		- postamble: HTML associated with the editor that comes after everything else
	- Notes:
		- Since the CSRF token is rendered here, it needn't be rendered in the including file (though it wouldn't cause anything bad to happen if it was).