#!/bin/env bash
rotname=$1

set -x
case $rotname in
  test_scripts)
    for i in ./test_*
    do  $i
    done
    ;;
    
  *)
    set +x
    echo Unknown routine name.
    echo Valid names would be:
    cat $0 | sed -n -e '/case/,/esac/ p' | grep '^ *[^*]\+)$' | grep -o '[^ )]\+' | sed -e 's/^/ - /'
    exit -1
    ;;
esac