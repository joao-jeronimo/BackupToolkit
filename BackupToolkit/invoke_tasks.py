#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# By João Jerónimo

# Dependencies installation:
#   sudo -H pip3 install fabric
#   sudo apt install rsync
# Exemple task invocation:
#   invoke --config=DriveH.yaml update-backup-global
#   invoke --config=DriveH.yaml update-backup-global --backup-profile=h_drive
# Configurations:
#   sudo /sbin/zfs allow jj create,snapshot,mount backupstank

from invoke import task
from . import backup_engine
from .backup_engine import BackupEngine
import pdb

@task
def check_dataset_registry(c):
    be = BackupEngine(c)
    return be.check_dataset_registry()

@task
def check_fix_zfs_mounts(c, force_mount_datasets=False):
    be = BackupEngine(c)
    be.check_dataset_registry()
    return be.check_fix_zfs_mounts(force_mount_datasets)

@task
def create_zfs_assets(c, dry_run=False):
    be = BackupEngine(c)
    be.check_dataset_registry()
    return be.create_zfs_assets(dry_run)

@task
def update_backup_rsync(c, backup_profile=""):
    be = BackupEngine(c)
    be.check_fix_zfs_mounts()
    return be.update_backup_rsync(backup_profile)

@task
def update_backup_global(c, backup_profile=""):
    be = BackupEngine(c)
    be.check_fix_zfs_mounts()
    return be.update_backup_global(backup_profile)
