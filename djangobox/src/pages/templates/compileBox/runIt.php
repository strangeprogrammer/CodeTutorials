

<!doctype HTML>
<html>
<head>
	<title>CodeMirror: HTML completion demo</title>
	<meta charset="utf-8">
	<link rel="stylesheet" href="../doc/docs.css">
	<link rel="stylesheet" href="../lib/codemirror.css">
	<link rel="stylesheet" href="../addon/hint/show-hint.css">
	<script src="../compileBox.js"></script>
	<script src="../lib/codemirror.js"></script>
	<script src="../addon/hint/show-hint.js"></script>
	<script src="../addon/hint/xml-hint.js"></script>
	<script src="../addon/hint/html-hint.js"></script>
	<script src="../mode/xml/xml.js"></script>
	<script src="../mode/javascript/javascript.js"></script>
	<script src="../mode/css/css.js"></script>
	<script src="../mode/htmlmixed/htmlmixed.js"></script>
	<script src="../mode/clike/clike.js"></script>
	<style>
	.CodeMirror {border-top: 1px solid #888; border-bottom: 1px solid #888;}
	</style>
</head>

<body>
	<div id="nav">
		<a href="https://codemirror.net"><h1>CodeMirror</h1><img id="logo" src="../doc/logo.png"></a>

		<ul>
			<li><a href="../index.html">Home</a>
			</li><li><a href="../doc/manual.html">Manual</a>
			</li><li><a href="https://github.com/codemirror/codemirror">Code</a>
			</li></ul>
			<ul>
				<li><a class="active" href="#">HTML completion</a>
				</li></ul>
			</div>

			<article>
				<h2>HTML completion demo</h2>

				<p>Shows the <a href="xmlcomplete.html">XML completer</a>
					parameterized with information about the tags in HTML.
					Press <strong>ctrl-space</strong> to activate completion.</p>

					<div id="code"></div>

					<script>
					window.onload = function() {
						editor = CodeMirror(document.getElementById("code"), {
							mode: "clike",
							extraKeys: {"Ctrl-Space": "autocomplete"},
							value: "#include <stdio.h> \n\nint main(int argc, char * argv[]) { \n\n\n\tprintf(\"Hello World!\");\n\n\n}"
						});
					};
					</script>

					<?php

					$fileWrite = '';
					$myFile = "Payload/main.c";
					if(isset($_POST['fileWrite']) && !empty($_POST['fileWrite'])) {
						$fileWrite = $_POST['fileWrite'].PHP_EOL;
						shell_exec("../../../runIt.sh");		#  "docker commands not found!!!!!"
						//echo "yoooo";		//test
					}
					if($fileWrite) {
						$fh = fopen($myFile, 'a') or die("can't open file"); //Make sure you have permission
						fwrite($fh, $fileWrite);
						fclose($fh);	//erase/create needed after this is done for each iteration (need random names probably)
					}
					?>

					<form id="some" name="someName" method="post">
						<input type="hidden" id="codeToWrite" value="" name="fileWrite"/>
						<script>

						</script>
						<input type="submit" value="runCode" onclick="document.getElementById('codeToWrite').value = showCode();" />
					</form>

				</article>

			</body>
			</html>
