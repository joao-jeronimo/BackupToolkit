from .bkhelpers import dikt_linez
import pdb

def zfs_create_dataset(be, datasetname, mountpoint, dry_run=True):
    # Create:
    zfs_create_command = ('%(zfs_bin)s create %(datasetname)s' % {
                    'zfs_bin':          be.config.BackupToolkit.ZFS_BIN,
                    'datasetname':      datasetname,
                    'mountpoint':       mountpoint,
                    })
    print("zfs_create_command = %s" % zfs_create_command)
    # Set the mountpoint:
    zfs_setmountpoint_command = ('%(zfs_bin)s set mountpoint=%(mountpoint)s %(datasetname)s' % {
                    'zfs_bin':          be.config.BackupToolkit.ZFS_BIN,
                    'datasetname':      datasetname,
                    'mountpoint':       mountpoint,
                    })
    print("zfs_setmountpoint_command = %s" % zfs_setmountpoint_command)
    if not dry_run:
        be.ictx.run(zfs_create_command, warn=True)
        be.ictx.run(zfs_setmountpoint_command, warn=True)

def zfs_create_snapshot(be, datasetname, snapshotname):
    zfs_snapcreate_command = ('%(zfs_bin)s snapshot %(datasetname)s@%(snapshotname)s' % {
                    'zfs_bin':          be.config.BackupToolkit.ZFS_BIN,
                    'datasetname':      datasetname,
                    'snapshotname':     snapshotname,
                    })
    print("zfs_snapcreate_command = %s" % zfs_snapcreate_command)
    return be.ictx.run(zfs_snapcreate_command, warn=True)

def zfs_mount_dataset(be, datasetname, su_do=False):
    zfs_mount_command = ('%(zfs_bin)s mount %(datasetname)s' % {
                    'zfs_bin':          be.config.BackupToolkit.ZFS_BIN,
                    'datasetname':      datasetname,
                    })
    print("zfs_mount_command = %s" % zfs_mount_command)
    if su_do:
        return be.ictx.sudo(zfs_mount_command, warn=True)
    else:
        return be.ictx.run(zfs_mount_command, warn=True)

def zfs_list_datasets(be):
    # Build and run command:
    zfs_list_command = ('%(zfs_bin)s list' % {
                    'zfs_bin':          be.config.BackupToolkit.ZFS_BIN,
                    })
    print("zfs_list_command = %s" % zfs_list_command)
    zfs_list_res = be.ictx.run(zfs_list_command, warn=True)
    if zfs_list_res.failed:
        raise bkexceptions.VerificationFailed("Could not get list of mounted filesystems.")
    # Convert to list of lists:
    parsable_output = dikt_linez(zfs_list_res)
    return parsable_output

def zfs_find_dataset_in_list(thelist, datasetname, mountpoint):
    matches = [ ds for ds in thelist
        if ds['NAME']==datasetname and ds['MOUNTPOINT']==mountpoint ]
    return matches
