FROM gcc:8.3.0
ARG uid
ARG gid
RUN addgroup --disabled-password --gid $gid guest && adduser --disabled-password --home /home/guest --gecos "" --gid $gid --uid $uid guest
WORKDIR /home/guest
USER guest:guest
CMD gcc -std=c99 -Wpedantic -Wall -o ./program -x c ./code && ./program 0<./STDIN 1>./STDOUT 2>./STDERR; echo -n $? 1>./retval
