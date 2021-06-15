#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# By João Jerónimo


import BackupToolkit.celery_tasks

#BackupToolkit.celery_tasks.fill_log_file.delay()
#BackupToolkit.celery_tasks.check_dataset_registry.delay()
#BackupToolkit.celery_tasks.check_fix_zfs_mounts.delay("h_drive")
BackupToolkit.celery_tasks.update_backup_versioned.delay("h_drive")


