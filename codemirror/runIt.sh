 #!/bin/sh
touch temp/useroutput.txt
chmod 777 temp/useroutput.txt
docker build -t dockerbox .		#uses main.c automatically (compilation)
docker run -it --rm --name my-running-app dockerbox >> temp/useroutput.txt
#rm Payload/main.c
#rm useroutput.txt
#Writes output to useroutput.txt ctest is reponame? (execution)

#Echo userouput.txt to webpage

#rm ctest.txt				//userinput in this scenario
#rm useroutput.txt		//Remove file which was users output
#rm main.c			//Remove file which was users output
#Remove docker containers everytime?
