
def create_snapshot(c, datasetname, snapshotname):
    zfs_snapcreate_command = ('zfs snapshot %(datasetname)s@%(snapshotname)s' % {
                    'datasetname':      datasetname,
                    'snapshotname':     snapshotname,
                    })
    print("zfs_snapcreate_command = %s" % zfs_snapcreate_command)
    return c.sudo(zfs_snapcreate_command, warn=True)
