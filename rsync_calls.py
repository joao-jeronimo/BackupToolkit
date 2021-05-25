
def do_rsync(c, portnr, orig_username, orig_ip, orig_path, dest_path):
    rsync_command = ('rsync -rlt --delete --exclude=".recycle" -v --port="%(portnr)d" "%(orig_username)s@%(orig_ip)s:%(orig_path)s" "%(dest_path)s"' % {
                    'portnr':           portnr,
                    'orig_username':    orig_username,
                    'orig_ip':          orig_ip,
                    'orig_path':        orig_path,
                    'dest_path':        dest_path,
                    })
    return c.run(rsync_command, warn=True)
