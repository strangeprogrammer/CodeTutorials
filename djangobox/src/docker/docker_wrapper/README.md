# docker_wrapper
Contains docker build files and houses dynamically-created directories for users.

#### ./Dockerfile.c
Contains the docker build image for gcc.

#### ./Dockerfile.py
Contains the docker build image for python.

#### ./Dockerfile.R
Contains the docker build image for R.

#### ./buildimages.sh
Automatically builds docker images when run.
Invocation:

	sudo ./buildimages.sh

Notes:
The containers generated are called 'gccbox', 'pythonbox', and 'rbox'.
The UID and GID of the user 'guest' within the generated containers will be '1001'.

#### ./runContainer.sh
Runs the code in the given folder with the given image.

#### ./c_spike
A simple spike to make sure that C code can be run properly in docker.

#### ./py_spike
A simple spike to make sure that python code can be run properly in docker.

#### ./r_spike
A simple spike to make sure that R code can be run properly in docker.

#### ./README.md
You're reading it right now.