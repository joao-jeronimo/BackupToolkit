
begin_nonreentrancy() {
    local PIDFILE=$1
    ### Non-reentrancy - Init:
    if [[ -f $PIDFILE ]]
    then
        echo "Already running."
        exit -1
    fi
    echo $$ > $PIDFILE
}

end_nonreentrancy() {
    local PIDFILE=$1
    ### Non-reentrancy - Cleanup:
    rm $PIDFILE
}
