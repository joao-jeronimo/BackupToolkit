import pdb

def do_rsync(c, portnr, orig_username, orig_ip, orig_path, dest_path):
    rsync_arguments = " ".join(
              [ "-rltv", "--delete" ]
            + [ "--exclude=\"%s\""%toexclude for toexclude in c.BackupToolkit.RSYNC_EXCLUSIONS ]
        )
    # Build and print final command:
    rsync_command = ('%(rsync_bin)s %(rsync_arguments)s --port="%(portnr)d" "%(orig_username)s@%(orig_ip)s:%(orig_path)s" "%(dest_path)s"' % {
                    'rsync_bin':        c.BackupToolkit.RSYNC_BIN,
                    'rsync_arguments':  rsync_arguments,
                    'portnr':           portnr,
                    'orig_username':    orig_username,
                    'orig_ip':          orig_ip,
                    'orig_path':        orig_path,
                    'dest_path':        dest_path,
                    })
    print("rsync_command = %s" % rsync_command)
    # Run the command:
    rsync_result = c.run(rsync_command, warn=True)
    return rsync_result
