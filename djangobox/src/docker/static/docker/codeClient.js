/* Class 'CodeRunner':
 * url:		The URL to which code should be forwarded to
 * region:	A CSS selector that should contain elements from which data is read/written by AJAX
 * 
 * Note: The 'region' selector's corresponding HTML element should have children HTML elements with the following classes:
 * 'code':		From where program code is taken
 * 'STDIN':		From where standard input for the program is taken
 * 'language':		From where the language of the program code is taken
 * 'submitcode':	An element that can act as a button (since the code will be run when it is pressed)
 * 'STDOUT':		To where the standard output of the program is put
 * 'STDERR':		To where the standard error of the program is put
 * 'retval':		To where the return value of the program is put
 */
function CodeRunner(url, region){
	this.url	= url;
	this.region	= region;
	
	this.code	= document.querySelector(region + " .code");
	this.STDIN	= document.querySelector(region + " .STDIN");
	this.mode	= document.querySelector(region + " .language");
	this.submit	= document.querySelector(region + " .submitcode");
	this.STDOUT	= document.querySelector(region + " .STDOUT");
	this.STDERR	= document.querySelector(region + " .STDERR");
	this.retval	= document.querySelector(region + " .retval");
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
	
	//Get csrf token when submitting form
	var csrf = document.querySelector('[name=csrfmiddlewaretoken]');
	xhr.setRequestHeader('X-CSRFToken', csrf.value);
	
	//5 * 1000 milliseconds
	xhr.timeout = 5 * 1000;
	
	xhr.onload = function(){
		//Good Response
		if(this.status === 200){
			success(JSON.parse(this.responseText));
		//Bad response
		}else{
			failure();
		}
	};
	
	xhr.ontimeout = function(){
		timeout();
	};
	
	xhr.send(form);
};

CodeRunner.prototype.registerFormSend = function(){
	//JavaScript quirk work-around
	var self = this;
	
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
