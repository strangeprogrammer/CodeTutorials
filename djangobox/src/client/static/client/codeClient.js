/* Constructor 'CodeRunner':
 * 
 * Arguments:
 * url:		The URL to which code should be forwarded to
 * region:	A CSS selector that should contain elements from which data is read/written by AJAX
 * timeout:	How long the AJAX server request should wait before timing out
 * 
 * Notes:
 * The 'region' selector's corresponding HTML element should have children HTML elements with the following classes:
 * 'presetcode':	OPTIONAL: Should contain the preset code (and be hidden)
 * 'presetSTDIN':	OPTIONAL: Should contain the preset STDIN (and be hidden)
 * 'code':		From where program code is taken
 * 'STDIN':		From where standard input for the program is taken
 * 'language':		From where the language of the program code is taken
 * 'submitcode':	An element that can act as a submit button
 * 'resetcode':		An element that can act as a reset button
 * 'STDOUT':		To where the standard output of the program is put
 * 'STDERR':		To where the standard error of the program is put
 * 'retval':		To where the return value of the program is put
 * 
 * Returns:
 * A new 'CodeRunner' object
 */
function CodeRunner(url, region, timeout = 10000){//10 * 1000 milliseconds = 10 seconds
	//Get relevant fields
	this.url	= url;
	this.region	= document.getElementById(region);
	this.timeout	= timeout;
	
	//Get necessary HTML elements
	this.code	= this.region.querySelector('.code');
	this.STDIN	= this.region.querySelector('.STDIN');
	this.mode	= this.region.querySelector('.codelang');
	this.STDOUT	= this.region.querySelector('.STDOUT');
	this.STDERR	= this.region.querySelector('.STDERR');
	this.retval	= this.region.querySelector('.retval');
	this.submit	= this.region.querySelector('.submitcode');
	this.reset	= this.region.querySelector('.resetcode');
	
	//Get optional HTML elements
	var x = this.region.querySelector('.presetcode');
	this.pcode = "";
	if(x !== null){
		this.pcode = CodeRunner.cleancode(x.value);
		x.hidden = 'hidden';
	}
	var y = this.region.querySelector('.presetSTDIN');
	this.pSTDIN = "";
	if(y !== null){
		this.pSTDIN = y.value;
		y.hidden = 'hidden';
	}
	
	//Get csrf token for form submission
	this.csrf	= this.region.querySelector('[name=csrfmiddlewaretoken]').value;
};

//Returns a POST form object using the relevant HTML elements
CodeRunner.prototype.makeForm = function(){
	var form = new FormData();
	form.append('code', this.code.value);
	form.append('STDIN', this.STDIN.value);
	form.append('mode', this.mode.value);
	return form;
};

/* Function 'CodeRunner.prototype.sendForm':
 * 
 * Arguments:
 * form:	A form object to submit to the internal URL
 * success:	A callback that takes the JSON object from the server
 * failure:	A callback called when the form can't be submitted
 * timeout:	A callback for when the wait time's been exceeded
 * 
 * Notes:
 * Sends the given form and takes callbacks for some different end status conditions
 * 
 * No Return Value
 */
CodeRunner.prototype.sendForm = function(form, success, failure, timeout){
	var xhr = new XMLHttpRequest();
	xhr.open('POST', this.url, true);
	
	xhr.setRequestHeader('X-CSRFToken', this.csrf);
	xhr.timeout = this.timeout;
	
	xhr.onload = function(){
		//Good Response
		if(this.status === 200){
			success(JSON.parse(this.responseText));
		//Bad response
		}else{
			failure();
		};
	};
	
	xhr.ontimeout = function(){
		timeout();
	};
	
	xhr.send(form);
};

/* Function 'CodeRunner.prototype.registerFormSend':
 * 
 * Arguments:
 * obj:
 * 	presubmit:	A callback that is called before the AJAX form is created
 * 	success:	A callback that is called after the AJAX request returns successfully
 * 	failure:	A callback that is called after the AJAX request returns unsuccessfully
 * 	timemout:	A callback that is called after the AJAX request times out
 * 
 * Notes:
 * Invoking this function more than once upon the same 'CodeRunner' object will overwrite any previous event handlers for the submit button
 * 
 * No Return Value
 */
CodeRunner.prototype.registerFormSend = function({presubmit = function(){},
success = function(kwargs){},
failure = function(){},
timeout = function(){}} = {}){ // https://stackoverflow.com/a/894877
	var self = this; //JavaScript quirk work-around
	
	//Set up 'onclick' event handler for the 'submit' button
	this.submit.onclick = function(){
		presubmit();
		self.sendForm(self.makeForm(), function(kwargs){ //On success, update the contents of the 'STDOUT', 'STDERR', and 'retval' elements
			self.STDOUT.value = kwargs.STDOUT;
			self.STDERR.value = kwargs.STDERR;
			self.retval.value = kwargs.retval;
			success(kwargs); //Use the response object, potentially
		}, function(){ //On failure, clean up and notify the user
			self.STDOUT.value = '';
			self.STDERR.value = 'Form couldn\'t be submitted properly...';
			self.retval.value = '';
			failure(); //Callback on failure, potentially
		}, function(){ //On timeout, clean up and notify the user
			self.STDOUT.value = '';
			self.STDERR.value = 'Server timed out...';
			self.retval.value = '';
			timeout(); //Callback on timeout, potentially
		});
	};
};

//Call this whenever 'this' object is ready to be used or reset
CodeRunner.prototype.preset = function(){
	this.code.value		= this.pcode;
	this.STDIN.value	= this.pSTDIN;
	this.STDOUT.value	= '';
	this.STDERR.value	= '';
	this.retval.value	= '';
	this.onreset(); //Call the callback on reset/preset
};

/* Function 'CodeRunner.prototype.registerReset':
 * 
 * Arguments:
 * onreset: a callback triggered whenever 'this' object is (p)reset
 * 
 * Notes:
 * Invoking this function more than once upon the same 'CodeRunner' object will overwrite any previous event handlers for the reset button
 * 
 * No Return Value
 */
CodeRunner.prototype.registerReset = function(onreset = function(){}){
	this.onreset	= onreset;
	var self	= this; //JavaScript quirk work-around
	
	this.reset.onclick = function(){
		self.preset();
	};
};

//Returns true if the line (string) contains only whitespace and false otherwise
CodeRunner.iswhite = function(line){
	if(line.trim().length === 0){
		return true;
	};
	return false;
};

/* Function 'CodeRunner.cleancode':
 * 
 * Arguments:
 * code: A snippet of code
 * 
 * Description:
 * Removes excess indentation of the code block
 * 
 * Notes & Extras:
 * Removes trailing whitespace and leading blank lines
 * Ignores blank lines when performing the computation of how much indentation to remove, but still removes all acceptable indentation from them
 * Please do not use mixed indenation (both spaces and tabs)
 * 
 * Returns:
 * The code with excess whitespace removed
 */
CodeRunner.cleancode = function(code){
	//Remove all trailing whitespace and split up the result into individual lines
	var lines = code.trimEnd().split('\n');
	
	//Remove all leading lines that contain only whitespace
	var start = 0;
	for(; start < lines.length && CodeRunner.iswhite(lines[start]); start++);
	lines = lines.slice(start, lines.length);
	
	//Find the minimum amount of whitespace that can be removed safely
	var minimum = Infinity;
	for(i in lines){
		diff = lines[i].length - lines[i].trimStart().length;
		if(diff < minimum && ! CodeRunner.iswhite(lines[i])){
			minimum = diff;
		};
	};
	
	//Remove all the whitespace, concatenate the results, and return the answer
	return lines.map(function(x){
		return x.slice(minimum, x.length);
	}).join('\n');
};
