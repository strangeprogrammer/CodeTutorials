//Depends upon static file 'client/codeClient.js'

/* Constructor 'boxSetup':
 * 
 * Arguments:
 * url:		The URL to send the request to
 * id:		The HTML id of the box to utilize (similar to a POST form, uses POST request mecahnnism)
 * obj:
 * 	options:	Additional options to pass to the relevant codemirror object when it's created
 * 	onreset:	A callback that is called when the reset button is pushed
 * 	onformsend:	A callback that is called when the form is sent (when code is pushed to the server)
 * 
 * Notes:
 * This file contains code for the default setup of the codemirror/docker interface in JavaScript
 * This code may better serve example than practical use
 * 
 * Returns:
 * A new 'boxSetup' object
 */
function boxSetup(url, id,
{options = {},
onreset = function(){},
onformsend = function(){}} = {}){
	//Use overwritable default options (recursive destructuring doesn't work)
	var options = {mode:"null", extraKeys:{"Ctrl-Space": "autocomplete"}, ...options};
	
	//Get relevant HTML element, set up code runner, and bind editor
	this.box = document.getElementById(id);
	this.runner = new CodeRunner(url, id);
	this.editor = CodeMirror.fromTextArea(this.box.querySelector(".code"), options);
	
	var self = this; //JavaScript quirk work-around
	
	//Set up code reset protocol and perform initial reset
	this.runner.registerReset(function(){
		self.editor.setValue(CodeRunner.cleancode(self.runner.pcode));
		onreset();
	});
	this.runner.preset();
	
	//Set up presubmit hook
	this.runner.registerFormSend({presubmit:function(){
		self.editor.save();
		self.box.querySelector(".STDOUT").value = "Processing...";
		onformsend();
	}});
	
	//Clean up the code language value from HTML
	var codelang = this.box.querySelector(".codelang");
	codelang.value = codelang.value.trim();
}

//Thin wrapper around 'boxSetup' for the 'C' language
function cbox(url, id){
	return boxSetup.apply(this, [url, id, {options:{
		mode:"clike"
	}}]);
}

//Thin wrapper around 'boxSetup' for the 'python' language
function pybox(url, id){
	return boxSetup.apply(this, [url, id, {options:{
		mode:"python",
		version:3,
		singleLineStringErrors:true
	}}]);
}

//Thin wrapper around 'boxSetup' for the 'R' language
function rbox(url, id){
	return boxSetup.apply(this, [url, id, {options:{
		mode:"r"
	}}]);
}
