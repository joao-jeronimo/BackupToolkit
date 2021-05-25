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
    all_mounted_fss = mkhelpers.get_mounted_fss(c)
    #
    pdb.set_trace()

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
