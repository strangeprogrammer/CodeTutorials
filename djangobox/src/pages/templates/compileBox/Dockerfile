FROM gcc:4.9
COPY . /usr/src/ctest
WORKDIR /usr/src/ctest
RUN gcc -o ctest Payload/main.c
CMD ["./ctest"]