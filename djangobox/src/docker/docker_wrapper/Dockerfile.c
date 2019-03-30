FROM gcc:8.3.0
RUN mkdir /home/guest
RUN useradd -d /home/guest guest
RUN chown -R guest:guest /home/guest
USER guest
WORKDIR /home/guest
VOLUME /home/guest
CMD gcc -std=c99 -Wpedantic -Wall -o ./program -x c ./code && ./program <./STDIN >./STDOUT
