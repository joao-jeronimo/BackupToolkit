#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# By João Jerónimo

# Dependencies installation:
#   sudo -H pip3 install fabric
#   sudo apt install rsync
# Exemple task invocation:
#   invoke update-backup-rsync --backup-profile=h_drive

from invoke import task
from datetime import datetime
from rsync_calls import do_rsync
from zfs_calls import zfs_create_snapshot
import bkexceptions, bkconfigs, bkhelpers
import pdb

@task
def mount_zfs_root(c):
    all_mounted_fss = bkhelpers.get_mounted_fss(c)
    zfs_mounteds = [ fss for fss in all_mounted_fss
        if fss['fs_vfstype']=='zfs' ]
    matching_mounteds = [ zfss for zfss in zfs_mounteds
        if zfss['fs_spec']==bkconfigs.ZFS_ROOT_POOLNAME and zfss['fs_file']==bkconfigs.ZFS_ROOT_MOUNTPOINT ]
    if len(matching_mounteds)>0:
        print("ZFS root pool mounted ok. Matching mount entries:")
        for matching in matching_mounteds:
            print("== Matching ZFS root pool:")
            print(matching)
    else:
        raise bkexceptions.VerificationFailed("Looks like ZFS root vol (%s, %s) is not mounted." % ( bkconfigs.ZFS_ROOT_POOLNAME, bkconfigs.ZFS_ROOT_MOUNTPOINT ))

@task(pre=[mount_zfs_root])
def update_backup_rsync(c, backup_profile=""):
    the_profile = bkhelpers.get_backup_profile(backup_profile)
    # Do the update:
    print("== Updating backup named '%s'" % backup_profile)
    rsync_parms = {
        **the_profile['origspecs'],
        'dest_path': the_profile['localspecs']['dest_path'],
        }
    print(repr(rsync_parms))
    rsync_result = do_rsync(c, **rsync_parms)
    return "Correu bem!"

@task(pre=[mount_zfs_root])
def update_backup_global(c, backup_profile=""):
    # Do the rsync part:
    update_backup_rsync(c, backup_profile)
    # Get important string and names:
    the_profile = bkhelpers.get_backup_profile(backup_profile)
    datasetname = bkhelpers.path_to_datasetname(the_profile['localspecs']['dest_path'])
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
    












