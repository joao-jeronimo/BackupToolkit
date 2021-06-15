# -*- coding: utf-8 -*-
# By João Jerónimo
import os, invoke
from .celery import app
from datetime import datetime
from .backup_engine import BackupEngine
###########################################
import pdb

MAIN_CONF_FILENAME = "BackupToolkitConfig.yaml"

def build_engine():
    # Open and interpret user-level config file:
    homedir = os.path.expanduser("~")
    user_config_file_path = os.path.join(homedir, '.backup_toolkit.conf')
    with open(user_config_file_path, "r") as conf_file:
        user_config_dict = {}
        for lin in conf_file.readlines():
            lindata = lin.split("=")
            user_config_dict[lindata[0].strip()] = lindata[1].strip()
    # This file points to the main config directory:
    main_config_dir = user_config_dict["MAIN_CONFIG_DIR"]
    main_config_file_path = os.path.join(main_config_dir, MAIN_CONF_FILENAME)
    # Create an invoke context that is fit for using under the control of Celery:
    ictx = invoke.context.Context()
    ictx.config.run.hide = 'both'
    # This is a YAML config file that stores all needed information:
    be = BackupEngine(main_config_file_path, ictx)
    return be
def call_task_by_name(be, taskname, *args, **kwargs):
    be = build_engine()
    invokable = getattr(be, taskname)
    try:
        return invokable(*args, **kwargs)
    except BaseException as e:
        be.log("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
        be.log("!!!!!!!!!!!! Exception thrown by task '%s':\n%s" % (taskname, str(e)) )
        be.log("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")

@app.task
def check_dataset_registry():
    be = build_engine()
    return call_task_by_name(be, "check_dataset_registry")
@app.task
def check_fix_zfs_mounts(backup_profile="", force_mount_datasets=False):
    be = build_engine()
    return call_task_by_name(be, "check_fix_zfs_mounts",
            backup_profile,
            force_mount_datasets)


@app.task
def create_zfs_assets(backup_profile="", force_mount_datasets=False):
    be = build_engine()
    return call_task_by_name(be, "create_zfs_assets",
            backup_profile,
            force_mount_datasets)

@app.task
def update_backup_rsync(backup_profile=""):
    be = build_engine()
    return call_task_by_name(be, "update_backup_rsync",
            backup_profile)

@app.task
def update_backup_versioned(backup_profile=""):
    be = build_engine()
    return call_task_by_name(be, "update_backup_versioned",
            backup_profile)

###################################
### Heartbeats for testing: #######
###################################
@app.task
def fill_log_file():
    with open("logfile.log", "a") as toappend:
        nowtime = datetime.now()
        readable_timestamp = "Running async task as of: %04d-%02d-%02d %02d:%02d:%02d . . .\n" % (
                nowtime.year,
                nowtime.month,
                nowtime.day,
                nowtime.hour,
                nowtime.minute,
                nowtime.second,
                )
        toappend.write(readable_timestamp)
