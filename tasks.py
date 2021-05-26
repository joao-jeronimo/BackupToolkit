#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# By João Jerónimo

# Dependencies installation:
#   sudo -H pip3 install fabric
#   sudo apt install rsync
# Exemple task invocation:
#   invoke --config=DriveH.yaml update-backup-global --backup-profile=h_drive
# Configurations:
#   sudo /sbin/zfs allow jj snapshot,mount backupstank

from invoke import task
from datetime import datetime
from rsync_calls import do_rsync
from zfs_calls import zfs_create_snapshot, zfs_mount_dataset
import bkexceptions, bkconfigs, bkhelpers
import pdb

@task
def check_dataset_existence(c):
    missing_datasets = [
        misspair
        for misspair in [   ( miss['localspecs']['dest_path'], bkhelpers.path_to_datasetname(c, miss['localspecs']['dest_path']))
                for miss in c.BackupToolkit.PROFILES.values()   ]
        if (misspair[1] not in bkconfigs.ZFS_DATASETS) and (misspair[1] not in bkconfigs.ZFS_SKIP_LIST)
        ]
    if any(missing_datasets):
        raise bkexceptions.VerificationFailed("Following backup destinations don't have their respective ZFS dataset registered in ZFS_DATASETS nor ZFS_SKIP_LIST lists:\n   %s"
                % ( "\n   ".join( [ repr(p) for p in missing_datasets ] ) ))

@task(check_dataset_existence)
def check_fix_zfs_mounts(c, force_mount_datasets=False):
    # Get all ZFS mounts:
    all_mounted_fss = bkhelpers.get_mounted_fss(c)
    zfs_mounteds = [ fss for fss in all_mounted_fss
        if fss['fs_vfstype']=='zfs' ]
    # Build list of ZFS datasets to see if they are mounted:
    full_zfs_list = ( [c.BackupToolkit.ZFS_ROOT_POOLNAME] + bkconfigs.ZFS_DATASETS )
    # See ant report if any is not mounted:
    not_mounted_zfss = [
        nmf for nmf
        in full_zfs_list
        if not any ( bkhelpers.find_mounted_fs(zfs_mounteds, nmf, bkhelpers.datasetname_to_path(c, nmf)) )
        ]
    if any(not_mounted_zfss):
        if bkconfigs.AUTO_MOUNT_DATASETS or force_mount_datasets:
            for to_mount in not_mounted_zfss:
                zfs_mount_dataset(c, to_mount, su_do=True)
        else:
            raise bkexceptions.VerificationFailed((
                        "The following ZFS datasets are not mounted:\n"
                        "   %s\n"
                        "To mount them, set AUTO_MOUNT_DATASETS config option to true (not recommended) or run manually:\n"
                        "   invoke check-fix-zfs-mounts --force-mount-datasets\n"
                        "Further errors may be thrown if some datasets don't exist."
                ) % ( "\n   ".join(not_mounted_zfss) ))

@task(pre=[check_fix_zfs_mounts])
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

@task(pre=[check_fix_zfs_mounts])
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
    












