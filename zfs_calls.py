
def zfs_create_snapshot(c, datasetname, snapshotname):
    zfs_snapcreate_command = ('%(zfs_bin)s snapshot %(datasetname)s@%(snapshotname)s' % {
                    'zfs_bin':          c.BackupToolkit.ZFS_BIN,
                    'datasetname':      datasetname,
                    'snapshotname':     snapshotname,
                    })
    print("zfs_snapcreate_command = %s" % zfs_snapcreate_command)
    return c.run(zfs_snapcreate_command, warn=True)

def zfs_mount_dataset(c, datasetname, su_do=False):
    zfs_mount_command = ('%(zfs_bin)s mount %(datasetname)s' % {
                    'zfs_bin':          c.BackupToolkit.ZFS_BIN,
                    'datasetname':      datasetname,
                    })
    print("zfs_mount_command = %s" % zfs_mount_command)
    if su_do:
        return c.sudo(zfs_mount_command, warn=True)
    else:
        return c.run(zfs_mount_command, warn=True)
