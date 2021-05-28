#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# By João Jerónimo

# Commands for production:
#celery start w1 -A BackupToolkit worker --loglevel=INFO      
# Commands for simple devel testing:
#celery -A BackupToolkit worker -B --loglevel=INFO            # With beat support...

from celery import Celery

app = Celery('´LivingBackupToolkit',
             #broker='amqp://',
             broker='pyamqp://guest@localhost//',
             backend='rpc://',
             include=['.celery_tasks'])

## Optional configuration, see the application user guide.
#app.conf.update(
#    result_expires=3600,
#)



if __name__ == '__main__':
    app.start()