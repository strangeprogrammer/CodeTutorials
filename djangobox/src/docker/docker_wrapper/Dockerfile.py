FROM python:3.8.0a3-stretch
ARG uid
ARG gid
RUN addgroup --disabled-password --gid $gid guest && adduser --disabled-password --home /home/guest --gecos "" --gid $gid --uid $uid guest
WORKDIR /home/guest
#CMD [ "bash", "-c", "
#	chown guest:guest ./code ./STDIN;
#	exec su guest -s /bin/bash -c '
#		python ./code 0<./STDIN 1>./STDOUT 2>./STDERR;
#		echo -n $? 1>./retval;
#	';" ]

# If all of the previous commented lines were condensed into a single line, it would be the next line

CMD [ "bash", "-c", "chown guest:guest ./code ./STDIN; exec su guest -s /bin/bash -c 'python ./code 0<./STDIN 1>./STDOUT 2>./STDERR; echo -n $? 1>./retval;';" ]
