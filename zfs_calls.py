from bkhelpers import dikt_linez
import pdb

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

def zfs_list_datasets(c):
    # Build and run command:
    zfs_list_command = ('%(zfs_bin)s list' % {
                    'zfs_bin':          c.BackupToolkit.ZFS_BIN,
                    })
    print("zfs_list_command = %s" % zfs_list_command)
    zfs_list_res = c.run(zfs_list_command, warn=True)
    if zfs_list_res.failed:
        raise bkexceptions.VerificationFailed("Could not get list of mounted filesystems.")
    # Convert to list of lists:
    parsable_output = dikt_linez(zfs_list_res)
    return parsable_output

def zfs_find_dataset_in_list(thelist, datasetname, mountpoint):
    matches = [ ds for ds in thelist
        if ds['NAME']==datasetname and ds['MOUNTPOINT']==mountpoint ]
    return matches
