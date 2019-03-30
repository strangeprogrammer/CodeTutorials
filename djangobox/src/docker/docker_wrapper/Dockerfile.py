FROM python:3.8.0a3-stretch
RUN mkdir /home/guest
RUN useradd -d /home/guest guest
RUN chown -R guest:guest /home/guest
USER guest
WORKDIR /home/guest
VOLUME /home/guest
CMD python ./code <./STDIN >./STDOUT
