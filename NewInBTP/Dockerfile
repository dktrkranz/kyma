FROM debian:latest
RUN apt-get update ; apt-get -y install python3 python3-requests python3-webpy
ADD NewInBTP.py /usr/local/bin/NewInBTP.py
ENTRYPOINT python3 /usr/local/bin/NewInBTP.py
