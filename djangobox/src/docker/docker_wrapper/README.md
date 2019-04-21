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

	./buildimages.sh <UID> <GID>

Keep in mind that docker's bind-mount mechanism preserves UID and GID values through the mount. This means that if the files within a client directory are created with UID and GID '1234' then, inside the container, whichever user has UID '1234' and whichever group has GID '1234' will have access to the files.

The most secure option is to use the UID and GID of the server account during production, so as to give away as little user information as possible to the client, and so as to contain any maliciously uploaded code to affecting other server files instead of the whole system.

For development, it may be simplest to use the UID and GID of your own user account (though ultimately you should know enough about your own machine to make a wiser decision if necessary).

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