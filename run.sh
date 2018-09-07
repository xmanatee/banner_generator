#!/bin/bash

docker build \
    -t "xmanatee/snapshooter" \
    --build-arg PORT=8080 \
    . \
&& docker run --rm -it \
    -p 8080:8080 \
    xmanatee/snapshooter

#    -v "$PWD/pngs":/mnt/pngs \
#    -v "$PWD/templates":/mnt/templates \
