//Depends upon static file 'docker/codeClient.js'

/* Arguments:
 * presubmit:	A callback that is called before the AJAX form is created
 * success:	A callback that is called after the AJAX request returns successfully
 * failure:	A callback that is called after the AJAX request returns unsuccessfully
 * timemout:	A callback that is called after the AJAX request times out
 * 
 * Notes:
 * This file contains code for the default setup of the codemirror/docker interface in JavaScript
 * This code may better serve example than practical use
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
	
	//Clean up the code language value
	var codelang = this.box.querySelector(".codelang");
	codelang.value = codelang.value.trim();
}

//Use this as a constructor
function cbox(url, id){
	return boxSetup.apply(this, [url, id, {options:{
		mode:"clike"
	}}]);
}

//Use this as a constructor
function pybox(url, id){
	return boxSetup.apply(this, [url, id, {options:{
		mode:"python",
		version:3,
		singleLineStringErrors:true
	}}]);
}

//Use this as a constructor
function rbox(url, id){
	return boxSetup.apply(this, [url, id, {options:{
		mode:"r"
	}}]);
}
