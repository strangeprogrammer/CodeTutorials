FROM python:3.8.0a3-stretch
ARG uid
ARG gid
RUN addgroup --disabled-password --gid $gid guest && adduser --disabled-password --home /home/guest --gecos "" --gid $gid --uid $uid guest
WORKDIR /home/guest
VOLUME /home/guest
USER guest:guest
CMD python ./code <./STDIN >./STDOUT
