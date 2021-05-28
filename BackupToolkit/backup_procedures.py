import os
from datetime import datetime
from .rsync_calls import do_rsync
from .zfs_calls import zfs_create_snapshot, zfs_mount_dataset, zfs_list_datasets, zfs_find_dataset_in_list, zfs_create_dataset
from . import bkexceptions, bkhelpers
import pdb

def create_zfs_assets(c, dry_run=False):
    # Find datasets that do not exist:
    zfs_datasets = zfs_list_datasets(c)
    nonexistant_datasets = [
            neds for neds in c.BackupToolkit.ZFS_DATASETS
            if len(zfs_find_dataset_in_list(zfs_datasets, neds, bkhelpers.datasetname_to_path(c, neds)))==0
            ]
    # Create them, or elsewise print them:
    for dstc in nonexistant_datasets:
        # Calculate related values:
        datasetname = dstc
        mountpoint = bkhelpers.datasetname_to_path(c, datasetname)
        # Verify if the folder is already there, and rmdir it if so:
        if os.path.isdir(mountpoint):
            # Is the empty folder cannot be deleted, then we can't do anything for you!
            os.rmdir(mountpoint)
        # Call dataset creation:
        zfs_create_dataset(c, datasetname, mountpoint, dry_run=dry_run)

def update_backup_rsync(c, backup_profile=""):
    the_profile = bkhelpers.get_backup_profile(c, backup_profile)
    # Do the update:
    print("== Updating backup named '%s'" % backup_profile)
    rsync_parms = {
        **the_profile['origspecs'],
        'dest_path': the_profile['localspecs']['dest_path'],
        }
    print(repr(rsync_parms))
    rsync_result = do_rsync(c, **rsync_parms)
    if rsync_result.failed:
        raise bkexceptions.VerificationFailed("Rsync failed for %s" % repr(rsync_parms))
    return "Correu bem!"

def update_backup_global(c, backup_profile=""):
    # Do the rsync part:
    if not backup_profile and len(c.BackupToolkit.PROFILES.keys())==1:
        backup_profile = tuple(c.BackupToolkit.PROFILES.keys())[0]
    update_backup_rsync(c, backup_profile)
    # Get important string and names:
    the_profile = bkhelpers.get_backup_profile(c, backup_profile)
    datasetname = bkhelpers.path_to_datasetname(c, the_profile['localspecs']['dest_path'])
    # Build a name for the snapshot:
    nowtime = datetime.now()
    snapshot_name = "Backup_%04d%02d%02d_%02d%02d%02d" % (
            nowtime.year,
            nowtime.month,
            nowtime.day,
            nowtime.hour,
            nowtime.minute,
            nowtime.second,
            )
    # Now, then, create the ZFS snapshot:
    zfs_create_snapshot(c, datasetname, snapshot_name)
