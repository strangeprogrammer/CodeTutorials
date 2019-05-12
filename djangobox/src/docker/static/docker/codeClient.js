/* Class 'CodeRunner':
 * url:		The URL to which code should be forwarded to
 * region:	A CSS selector that should contain elements from which data is read/written by AJAX
 * 
 * Note: The 'region' selector's corresponding HTML element should have children HTML elements with the following classes:
 * 'presetcode':	Should contain the preset code and be hidden
 * 'presetSTDIN':	Should contain the preset STDIN and be hidden
 * 'code':		From where program code is taken
 * 'STDIN':		From where standard input for the program is taken
 * 'language':		From where the language of the program code is taken
 * 'submitcode':	An element that can act as a submit button
 * 'resetcode':		An element that can act as a reset button
 * 'STDOUT':		To where the standard output of the program is put
 * 'STDERR':		To where the standard error of the program is put
 * 'retval':		To where the return value of the program is put
 */
function CodeRunner(url, region, timeout = 5000){
	//Get global variables
	this.url	= url;
	this.region	= region;
	this.timeout	= timeout; //5 * 1000 milliseconds = 5 seconds
	
	//Get relevant HTML elements
	this.pcode	= document.querySelector(region + ' .presetcode');
	this.pSTDIN	= document.querySelector(region + ' .presetSTDIN');
	this.code	= document.querySelector(region + ' .code');
	this.STDIN	= document.querySelector(region + ' .STDIN');
	this.mode	= document.querySelector(region + ' .codelang');
	this.submit	= document.querySelector(region + ' .submitcode');
	this.reset	= document.querySelector(region + ' .resetcode');
	this.STDOUT	= document.querySelector(region + ' .STDOUT');
	this.STDERR	= document.querySelector(region + ' .STDERR');
	this.retval	= document.querySelector(region + ' .retval');
	
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
	
	//Get csrf token when submitting form
	var csrf = document.querySelector('[name=csrfmiddlewaretoken]');
	xhr.setRequestHeader('X-CSRFToken', csrf.value);
	
	xhr.timeout = this.timeout;
	
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
	this.code.value		= this.pcode.value;
	this.STDIN.value	= this.pSTDIN.value;
	this.STDOUT.value	= '';
	this.STDERR.value	= '';
	this.retval.value	= '';
};
