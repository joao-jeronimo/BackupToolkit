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
from . import backup_guards, backup_procedures

@task
def check_dataset_registry(c):
    return backup_guards.check_dataset_registry(c)

@task
def check_fix_zfs_mounts(c, force_mount_datasets=False):
    backup_guards.check_dataset_registry(c)
    return backup_guards.check_fix_zfs_mounts(c, force_mount_datasets)

@task
def create_zfs_assets(c, dry_run=False):
    backup_guards.check_dataset_registry(c)
    return backup_procedures.create_zfs_assets(c, dry_run)

@task
def update_backup_rsync(c, backup_profile=""):
    backup_guards.check_fix_zfs_mounts(c)
    return backup_procedures.update_backup_rsync(c, backup_profile)

@task
def update_backup_global(c, backup_profile=""):
    backup_guards.check_fix_zfs_mounts(c)
    return backup_procedures.update_backup_global(c, backup_profile)