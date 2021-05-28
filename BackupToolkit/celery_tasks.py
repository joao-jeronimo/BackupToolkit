# -*- coding: utf-8 -*-
# By João Jerónimo

from .celery import app
from datetime import datetime
from . import backup_guards, backup_procedures

@app.task
def check_dataset_registry(c):
    return backup_guards.check_dataset_registry(c)



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
