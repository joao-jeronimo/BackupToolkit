import bkconfigs

def do_rsync(c, portnr, orig_username, orig_ip, orig_path, dest_path):
    rsync_arguments = " ".join(
              [ "-rltv", "--delete" ]
            + [ "--exclude=\"%s\""%toexclude for toexclude in bkconfigs.RSYNC_EXCLUSIONS ]
        )
    # Build and print final command:
    rsync_command = ('%(rsync_bin)s %(rsync_arguments)s --port="%(portnr)d" "%(orig_username)s@%(orig_ip)s:%(orig_path)s" "%(dest_path)s"' % {
                    'rsync_bin':        bkconfigs.RSYNC_BIN,
                    'rsync_arguments':  rsync_arguments,
                    'portnr':           portnr,
                    'orig_username':    orig_username,
                    'orig_ip':          orig_ip,
                    'orig_path':        orig_path,
                    'dest_path':        dest_path,
                    })
    print("rsync_command = %s" % rsync_command)
    # Run the command:
    return c.run(rsync_command, warn=True)
