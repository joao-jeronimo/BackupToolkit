#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# By João Jerónimo

# Dependencies installation:
#sudo -H pip3 install fabric
#sudo apt install rsync

from invoke import task
from rsync_calls import do_rsync
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
def update_backup_rsync(c):
    rsync_result = do_rsync(c, **{
            'portnr':           22,
            'orig_username':    "remotebackups",
            'orig_ip':          "192.168.100.105",
            'orig_path':        "/srv/storage/outras_drives_usl/h/",
            'dest_path':        "/home/jj/TestBackups/backups_tank/h_drive",
            })
    return "Correu bem!"
