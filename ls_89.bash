#!/bin/env bash
set -e -x
# System vars:
IDIR=$(dirname $0)
# Libs:
source $IDIR/lib.bash
# Other vars:
source ~/.backupbot_params
PIDFILE=$IDIR/run/ls_89.pid
# The program:
begin_nonreentrancy $PIDFILE
##################################################################################

rclone ls "$REMOTE_NAME"

##################################################################################
end_nonreentrancy $PIDFILE
