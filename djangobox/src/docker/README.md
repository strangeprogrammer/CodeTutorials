# docker
This app contains files related to the server-side backend components that interact with docker instances.

#### ./dockerBackend.py
Contains some wrapper code to interact with the docker containers.

#### ./docker_wrapper
A location where docker instances can interact with generated folders. It also contains some files used to build the docker images that should be used during installation.

#### ./migrations
This folder should remain here so that the contents of 'models.py' can be created and used properly when the project is first installed.

#### ./models.py
Contains the model for associating users with UUID's.

#### ./static
Contains 'docker/codeClient.js', which is the client-side code to interact with 'docker/runPOST'.

#### ./templates
Contains 'CodeRunner.html', which is an includable file for forms that utilize 'CodeMirror' and the 'runPOST' interface (takes 'defaultlang' as an argument).

#### ./tools.py
Contains some code used within 'dockerBackend.py' and 'views.py'.

#### ./urls.py
Adds the URL for the 'runPOST' function.

#### ./views.py
Contains IO functions to get code and STDIN from user, as well as provide STDOUT back.

#### ./README.md
You're reading it right now.