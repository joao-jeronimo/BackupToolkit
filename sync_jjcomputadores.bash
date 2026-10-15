#!/bin/env bash
set -e -x
# System vars:
IDIR=$(dirname $0)
# Libs:
source $IDIR/lib.bash
# Other vars:
source ~/.backupbot_params
PIDFILE=$IDIR/run/sync_jjcomputadores.pid
# The program:
begin_nonreentrancy $PIDFILE
##################################################################################

time rclone sync --progress --create-empty-src-dirs                 \
    "$JJCOMPUTADORES_LOCAL" "$JJCOMPUTADORES_REMOTE"
time rclone ls "$JJCOMPUTADORES_REMOTE"

##################################################################################
end_nonreentrancy $PIDFILE
