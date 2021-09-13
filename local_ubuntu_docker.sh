#!/usr/bin/env bash

# Small utility to build/run  a docker container with values used 
# in the CI.

usage() { echo "Usage: $0 [-b  -r ]" 1>&2; exit 1; }

while getopts "br" o; do
    case "${o}" in
        b)
            docker build -t fossmerge .
            ;;
        r)
            docker run   -v $PWD:/build -it fossmerge  /bin/bash -c "cd /build && poetry install"
            docker run   -v $PWD:/build -it fossmerge  /bin/bash -c "cd /build && bash;"
            ;;
        *)
            usage
            ;;
    esac
done
#if [ -z "${cmd}" ] ; then
#    usage
#fi

#echo "s = ${cmd}"
#echo "p = ${cmd}"



