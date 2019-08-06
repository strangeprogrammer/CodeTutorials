# DOCUMENTING ../static/client/boxSetup.js

#### Depends upon static file 'client/codeClient.js'

- Constructor 'boxSetup':
	- Arguments:
		- url: The URL to send the request to
		- id: The HTML id of the box to utilize (similar to a POST form, uses POST request mecahnnism)
		- obj:
			- options: Additional options to pass to the relevant codemirror object when it's created
			- onreset:A callback that is called when the reset button is pushed
			- onformsend: A callback that is called when the form is sent (when code is pushed to the server)
	- Notes:
		- This file contains code for the default setup of the codemirror/docker interface in JavaScript
		- This code may better serve example than practical use
	- Outline:
		- Use overwritable default options (recursive destructuring doesn't work)
		- Get relevant HTML element, set up code runner, and bind editor
		- Set up code reset protocol and perform initial reset
		- Set up presubmit hook
		- Clean up the code language value from HTML
	- Returns:
		- A new 'boxSetup' object

- Function 'cbox':
	- Arguments:
		- url:
		- id:
	- Notes:
		- Thin wrapper around 'boxSetup' for the 'C' language

- Function 'pybox':
	- Arguments:
		- url:
		- id:
	- Notes:
		- Thin wrapper around 'boxSetup' for the 'python' language

- Function 'rbox':
	- Arguments:
		- url:
		- id:
	- Notes:
		- Thin wrapper around 'boxSetup' for the 'R' language