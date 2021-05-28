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

from invoke import Collection
import BackupToolkit.invoke_tasks

ns = Collection()
ns.add_collection(BackupToolkit.invoke_tasks, "BackupToolkit")
