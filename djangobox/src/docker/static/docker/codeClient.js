function makeForm(){
	var code = document.querySelector('#code');
	var STDIN = document.querySelector('#STDIN');
	var mode = document.querySelector('#mode');
	var form = new FormData();
	
	form.append('code', code.value);
	form.append('STDIN', STDIN.value);
	form.append('mode', mode.value);
	return form;
}

function sendForm(url, form, success, failure, timeout){
	var xhr = new XMLHttpRequest();
	xhr.open('POST', url, true);
	
	//Get csrf token when submitting form
	var csrf = document.querySelector('[name=csrfmiddlewaretoken]');
	xhr.setRequestHeader('X-CSRFToken', csrf.value);
	
	//5 * 1000 milliseconds
	xhr.timeout = 5 * 1000;
	
	xhr.onload = function(){
		//Good Response
		if(this.status === 200){
			success.call(JSON.parse(this.responseText));
		//Bad response
		}else{
			failure.call(this);
		}
	};
	
	xhr.ontimeout = function(){
		timeout.call(this);
	};
	
	xhr.send(form);
}

function registerFormSend(url){
	document.querySelector('#submitcode').addEventListener('click', function(){
		sendForm(url, makeForm(), function(){
			document.querySelector('#STDOUT').value = this.STDOUT;
			document.querySelector('#STDERR').value = this.STDERR;
			document.querySelector('#retval').value = this.retval;
		}, function(){
			document.querySelector('#STDOUT').value = '';
			document.querySelector('#STDERR').value = 'Server encountered an error...';
			document.querySelector('#retval').value = '';
		}, function(){
			document.querySelector('#STDOUT').value = '';
			document.querySelector('#STDERR').value = 'Server timed out...';
			document.querySelector('#retval').value = '';
		});
	});
}
