#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# By João Jerónimo

from invoke import Collection
import BackupToolkit.invoke_tasks

ns = Collection()
ns.add_collection(BackupToolkit.invoke_tasks, "BackupToolkit")
