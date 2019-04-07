FROM r-base:3.5.3
ARG uid
ARG gid
RUN deluser --remove-all-files docker
RUN addgroup --disabled-password --gid $gid guest && adduser --disabled-password --home /home/guest --gecos "" --gid $gid --uid $uid guest
WORKDIR /home/guest
VOLUME /home/guest
USER guest:guest
CMD R --vanilla --slave -f ./code 0<./STDIN 1>./STDOUT 2>./STDERR; echo -n $? 1>./retval
