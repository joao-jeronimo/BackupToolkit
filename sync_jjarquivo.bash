#!/bin/env bash
set -e -x
# System vars:
IDIR=$(dirname $0)
# Libs:
source $IDIR/lib.bash
# Other vars:
source ~/.backupbot_params
PIDFILE=$IDIR/run/sync_jjarquivo.pid
# The program:
begin_nonreentrancy $PIDFILE
##################################################################################

time rclone sync --progress --create-empty-src-dirs                 \
    "$JJARQUIVO_LOCAL" "$JJARQUIVO_REMOTE"

##################################################################################
end_nonreentrancy $PIDFILE
