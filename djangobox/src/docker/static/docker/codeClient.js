/* Class 'CodeRunner':
 * url:		The URL to which code should be forwarded to
 * region:	A CSS selector that should contain elements from which data is read/written by AJAX
 * timeout:	How long the AJAX server request should wait before timing out
 * 
 * Note: The 'region' selector's corresponding HTML element should have children HTML elements with the following classes:
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
 */
function CodeRunner(url, region, timeout = 5000){//5 * 1000 milliseconds = 5 seconds
	//Get global variables
	this.url	= url;
	this.region	= region;
	this.timeout	= timeout;
	
	//Get necessary HTML elements
	this.code	= document.querySelector(region + ' .code');
	this.STDIN	= document.querySelector(region + ' .STDIN');
	this.mode	= document.querySelector(region + ' .codelang');
	this.submit	= document.querySelector(region + ' .submitcode');
	this.reset	= document.querySelector(region + ' .resetcode');
	this.STDOUT	= document.querySelector(region + ' .STDOUT');
	this.STDERR	= document.querySelector(region + ' .STDERR');
	this.retval	= document.querySelector(region + ' .retval');
	
	//Get optional HTML elements
	var x = document.querySelector(region + ' .presetcode');
	this.pcode = "";
	if(x !== null){
		this.pcode = x.value;
		x.hidden = 'hidden';
	}
	var y = document.querySelector(region + ' .presetSTDIN');
	this.pSTDIN = "";
	if(y !== null){
		this.pSTDIN = y.value;
		y.hidden = 'hidden';
	}
	
	//Get csrf token for form submission
	this.csrf	= document.querySelector(region + ' [name=csrfmiddlewaretoken]').value;
	
	//Perform setup
	this.registerFormSend();
	this.registerReset();
	this.preset();
};

CodeRunner.prototype.makeForm = function(){
	var form = new FormData();
	form.append('code', this.code.value);
	form.append('STDIN', this.STDIN.value);
	form.append('mode', this.mode.value);
	return form;
};

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

CodeRunner.prototype.registerFormSend = function(){
	var self = this; //JavaScript quirk work-around
	
	this.submit.addEventListener('click', function(){
		self.sendForm(self.makeForm(), function(kwargs){
			self.STDOUT.value = kwargs.STDOUT;
			self.STDERR.value = kwargs.STDERR;
			self.retval.value = kwargs.retval;
		}, function(){
			self.STDOUT.value = '';
			self.STDERR.value = 'Server encountered an error...';
			self.retval.value = '';
		}, function(){
			self.STDOUT.value = '';
			self.STDERR.value = 'Server timed out...';
			self.retval.value = '';
		});
	});
};

CodeRunner.prototype.registerReset = function(){
	var self = this; //JavaScript quirk work-around
	
	this.reset.addEventListener('click', function(){
		self.preset();
	});
};

CodeRunner.prototype.preset = function(){
	this.code.value		= CodeRunner.cleancode(this.pcode);
	this.STDIN.value	= CodeRunner.cleancode(this.pSTDIN);
	this.STDOUT.value	= '';
	this.STDERR.value	= '';
	this.retval.value	= '';
};

//Returns true if the line (string) contains only whitespace and false otherwise
CodeRunner.iswhite = function(line){
	if(line.trim().length === 0){
		return true;
	};
	return false;
};

/* Argument:
 * code: A snippet of code
 * 
 * Description:
 * Removes excess indentation of the code block
 * 
 * Notes & Extras:
 * Removes trailing whitespace and leading blank lines
 * Ignores blank lines when performing the computation of how much indentation to remove, but still removes all acceptable indentation from them
 * Please do not use mixed indenation (both spaces and tabs)
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
