### BEGIN COPYRIGHT NOTICE

# Copyright 2019 Stephen Fedele <stephen.m.fedele@wmich.edu>, Daniel Darcy, Timothy Curry
# 
# This file is part of CodeTutorials.
# 
# CodeTutorials is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
# 
# CodeTutorials is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with CodeTutorials.  If not, see <https://www.gnu.org/licenses/>.

### END COPYRIGHT NOTICE

FROM gcc:8.3.0
ARG uid
ARG gid
RUN addgroup --disabled-password --gid $gid guest && adduser --disabled-password --home /home/guest --gecos "" --gid $gid --uid $uid guest
WORKDIR /home/guest
#CMD [ "bash", "-c", "
#	chown guest:guest ./code ./STDIN;
#	exec su guest -c '
#		gcc -std=c99 -Wpedantic -Wall -o ./program -x c ./code 1>./STDOUT 2>./STDERR;
#		echo \"gcc: $?\n\n\" 1>>./STDOUT;
#		./program 0<./STDIN 1>>./STDOUT 2>>./STDERR;
#		echo -n $? 1>./retval;
#	';" ]

# If all of the previous commented lines were condensed into a single line, it would be the next line

CMD [ "bash", "-c", "chown guest:guest ./code ./STDIN; exec su guest -c 'gcc -std=c99 -Wpedantic -Wall -o ./program -x c ./code 1>./STDOUT 2>./STDERR; echo -e \"gcc: $?\n\" 1>>./STDOUT; ./program 0<./STDIN 1>>./STDOUT 2>>./STDERR; echo -n $? 1>./retval;';" ]
