import bkconfigs

def zfs_create_snapshot(c, datasetname, snapshotname):
    zfs_snapcreate_command = ('%(zfs_bin)s snapshot %(datasetname)s@%(snapshotname)s' % {
                    'zfs_bin':        bkconfigs.ZFS_BIN,
                    'datasetname':      datasetname,
                    'snapshotname':     snapshotname,
                    })
    print("zfs_snapcreate_command = %s" % zfs_snapcreate_command)
    return c.run(zfs_snapcreate_command, warn=True)
