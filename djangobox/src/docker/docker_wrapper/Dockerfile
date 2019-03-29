FROM gcc:4.9
RUN mkdir /home/guest
RUN useradd -d /home/guest guest
RUN chown -R guest:guest /home/guest
USER guest
WORKDIR /home/guest
VOLUME /home/guest
CMD gcc -std=c99 -Wpedantic -Wall -o ./program -x c ./code <./STDIN && ./program >./STDOUT
