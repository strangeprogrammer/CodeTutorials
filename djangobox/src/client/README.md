# client
This app contains client-side resources that are likely to change. These include static files and templates that may be edited.

#### ./doc
Contains documentation for the files under **./static** and **./templates**.

#### ./static
Contains 'client/codeClient.js', which is the class 'CodeRunner' and other code to interact with URL '/docker/runPOST/'.

Alco contains 'client/boxSetup.js', which acts as a default/example layer over 'client/codeClient.js'.

#### ./templates
Contains 'CodeRunner.html', which is an includable file for forms that utilize 'CodeMirror' and the 'runPOST' interface (takes 'defaultlang' as an argument). 

You should probably use 'CodeBox.html', which contains slightly more code and has about as much flexibility (takes 'id' as an argument and acts as a block-extended template).

#### ./README.md
You're reading it right now.