FROM r-base:3.5.3
RUN mkdir /home/guest
RUN useradd -d /home/guest guest
RUN chown -R guest:guest /home/guest
USER guest
WORKDIR /home/guest
VOLUME /home/guest
CMD R --vanilla -f ./code <./STDIN >./STDOUT
