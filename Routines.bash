#!/bin/env bash
rotname=$1

set -x
case $rotname in
  ola)
    echo Que seja "'olá'" como tu dizes.
    ;;
    
  *)
    set +x
    echo Unknown routine name.
    echo Valid names would be:
    cat $0 | sed -n -e '/case/,/esac/ p' | grep '^ *[^*]\+)$' | grep -o '[^ )]\+' | sed -e 's/^/ - /'
    exit -1
    ;;
esac