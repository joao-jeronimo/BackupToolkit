#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# By João Jerónimo


import BackupToolkit.celery_tasks

BackupToolkit.celery_tasks.fill_log_file.delay()

