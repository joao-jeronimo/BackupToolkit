# -*- coding: utf-8 -*-
# By João Jerónimo
from .celery import app
from datetime import datetime
# Imports for wrapping-arround the Invoke library:
import invoke
import BackupToolkit.invoke_tasks
###########################################
import pdb

def build_invoke_namespace():
    thens = invoke.Collection()
    thens.add_collection(BackupToolkit.invoke_tasks, "BackupToolkit")
    return thens
def build_invoke_executor():
    invoke_nmspc = build_invoke_namespace()
    invoke_config = invoke.Config(
        project_location = "/home/jj/TestBackups/BackupToolkit/",
        runtime_path = "/home/jj/TestBackups/BackupToolkit/DriveH.yaml",)
    return invoke.Executor(collection=invoke_nmspc, config=invoke_config)

@app.task
def check_dataset_registry():
    executor = build_invoke_executor()
    #pdb.set_trace()
    return executor.execute("BackupToolkit.check_dataset_registry")

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
