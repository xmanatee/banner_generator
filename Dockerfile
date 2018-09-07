FROM ubuntu:14.04
MAINTAINER Steve Mayne <steve.mayne@gmail.com>

RUN apt-get update -y \
    && apt-get install -q -y \
	    make \
	    "g++" \
	    git-core \
	    libqt4-webkit \
	    libqt4-dev \
	    libgl1-mesa-dri \
	    python-imaging \
	    qt4-qmake \
	    x11-xkb-utils \
	    xfonts-75dpi \xfonts-100dpi \
	    xfonts-cyrillic \
	    xfonts-scalable \
	    xserver-xorg-core \
	    xvfb \
    && apt-get update -y \
    && apt-get install -y \
        python3-pip \
    && pip3 install flask

RUN git clone https://github.com/marazmiki/CutyCapt.git /tmp/CutyCapt

WORKDIR /tmp/CutyCapt
RUN qmake && make

RUN cp /tmp/CutyCapt/CutyCapt /usr/bin/cutycapt

RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

WORKDIR /home

COPY server.py server.py
COPY renderer.py renderer.py
COPY web web
COPY templates /mnt/templates

CMD if [ -z "$PORT" ] ; then export PORT=8080; echo "Running in debug mode"; else echo "Running in prod with PORT=$PORT" ; fi && python3 server.py --port=$PORT
