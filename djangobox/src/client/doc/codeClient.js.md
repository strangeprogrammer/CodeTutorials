# DOCUMENTING ../static/client/codeClient.js

- Constructor 'CodeRunner':
	- Arguments:
		- url: The URL to which code should be forwarded to
		- region: A CSS selector that should contain elements from which data is read/written by AJAX
		- timeout: How long the AJAX server request should wait before timing out
	- Notes:
 		- The 'region' selector's corresponding HTML element should have children HTML elements with the following classes:
		'presetcode': OPTIONAL: Should contain the preset code (and be hidden)
		'presetSTDIN': OPTIONAL: Should contain the preset STDIN (and be hidden)
		'code': From where program code is taken
		'STDIN': From where standard input for the program is taken
		'language': From where the language of the program code is taken
		'submitcode': An element that can act as a submit button
		'resetcode': An element that can act as a reset button
		'STDOUT': To where the standard output of the program is put
		'STDERR': To where the standard error of the program is put
		'retval': To where the return value of the program is put
	- Outline:
		- Get relevant fields
		- Get necessary HTML elements
		- Get optional HTML elements
		- Get csrf token for form submission
	- Returns:
		- A new 'CodeRunner' object

- Function 'CodeRunner.prototype.makeForm':
	- No Arguments
	- Returns:
		- A POST form object using the relevant HTML elements

- Function 'CodeRunner.prototype.sendForm'
	- Arguments:
		- form: A form object to submit to the internal URL
		- success: A callback that takes the JSON object from the server
		- failure: A callback called when the form can't be submitted
		- timeout: A callback for when the wait time's been exceeded
	- Notes:
		- Sends the given form and takes callbacks for some different end status conditions
	- No Return Value

- Function 'CodeRunner.prototype.registerFormSend':
	- Arguments:
		- obj:
			- presubmit: A callback that is called before the AJAX form is created
			- success: A callback that is called after the AJAX request returns successfully
			- failure: A callback that is called after the AJAX request returns unsuccessfully
			- timemout: A callback that is called after the AJAX request times out
	- Notes:
		- Invoking this function more than once upon the same 'CodeRunner' object will overwrite any previous event handlers for the submit button
	- Outline:
		- Set up 'onclick' event handler for the 'submit' button
		- On success, update the contents of the 'STDOUT', 'STDERR', and 'retval' elements
			- Use the response object, potentially
		- On failure, clean up and notify the user
			- Callback on failure, potentially
		- On timeout, clean up and notify the user
			- Callback on timeout, potentially
	- No Return Value

- Function 'CodeRunner.prototype.preset':
	- No Arguments
	- Notes:
		- Call this whenever 'this' object is ready to be used or reset
	- No Return Value

- Function 'CodeRunner.prototype.registerReset':
	- Arguments:
		- onreset: a callback triggered whenever 'this' object is (p)reset
	- Notes:
		- Invoking this function more than once upon the same 'CodeRunner' object will overwrite any previous event handlers for the reset button
	- No Return Value

- Function 'CodeRunner.iswhite':
	- Arguments:
		- line: a string ending in a newline
	- Returns:
		- True if the line (string) contains only whitespace and false otherwise

- Function 'CodeRunner.cleancode':
	- Arguments:
		- code: A snippet of code
	- Description:
		- Removes excess indentation of the code block
	- Notes & Extras:
		- Removes trailing whitespace and leading blank lines
		- Ignores blank lines when performing the computation of how much indentation to remove, but still removes all acceptable indentation from them
		- Please do not use mixed indenation (both spaces and tabs)
	- Outline:
		- Remove all trailing whitespace and split up the result into individual lines
		- Remove all leading lines that contain only whitespace
		- Find the minimum amount of whitespace that can be removed safely
		- Remove all the whitespace, concatenate the results, and return the answer
	- Returns:
		- The code with excess whitespace removed