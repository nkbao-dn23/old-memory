FROM ubuntu:20.04
MAINTAINER peternguyen

RUN apt-get update
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get install xinetd clang cmake -y
RUN useradd -m notes

RUN chmod 774 /tmp
RUN chmod -R 774 /var/tmp
RUN chmod -R 774 /dev
RUN chmod -R 774 /run
RUN chmod 1733 /tmp /var/tmp /dev/shm

RUN mkdir /home/notes/src
ADD notes /home/notes/src
ADD flag.txt /home/notes
WORKDIR /home/notes
ENV CC=clang
RUN cmake ./src/
RUN cmake --build .
RUN strip note
RUN strip ./libzone/libzone.so

ADD notes.xinetd /etc/xinetd.d/notes
WORKDIR /home/notes

RUN chmod 660 /etc/xinetd.d/notes
RUN chown -R root:notes /home/notes/
RUN chmod -R 750 /home/notes/
RUN chmod 750 /home/notes/note
RUN chmod 440 /home/notes/flag.txt

#CMD ["/bin/bash"]
CMD ["/usr/sbin/xinetd", "-dontfork"]
