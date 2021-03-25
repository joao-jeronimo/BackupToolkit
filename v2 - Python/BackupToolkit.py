#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys, datetime
from os.path import expanduser
from berkeleydb import db as bdb
import rsync_call_lib as rsynccall
from git import Repo

import pdb



class PythonBDB(object):
    def __init__(self, evalenv):
        self.evalenv = evalenv
        self.innerDB = bdb.DB()
    
    def __getattr__(self, attrnm):
        return getattr(self.innerDB, attrnm)
    
    def gput(self, key, data):
        return self.put( bytes(repr(key), 'utf-8'), bytes(repr(data), 'utf-8') )
    def gget(self, key):
        returnt = self.get( bytes(repr(key), 'utf-8') )
        if returnt is None: return None
        else:               return eval(returnt, {}, self.evalenv)

KEY_BACKUPS = 'Backups'

class BackupToolkit:
    rsync_args = ['-rlt', '--delete', '--exclude=.recycle', '--exclude=.git', '-v']
    
    def get_backup(self, backupname):
        the_backup = self.config_db.gget(backupname)
        if the_backup is None:
            print("No backup named %s!"%backupname)
            exit(-1)
        return the_backup
    
    def do_rsync(self, the_backup):
        # Update backup using Rsync:
        rsync = rsynccall.Rsync( the_backup['srcendpoint'], the_backup['dstendpoint'] )
        rsync.add_args(self.rsync_args)
        rsync.run()
    
    def do_gitstatus(self, repo, the_backup):
        # Adding new files one by one:
        return repo.untracked_files
    
    def do_gitadd(self, repo, toadd):
        # Adding new files one by one:
        # TODO: Do a "find" on that path before adding files (to avoid adding big dirs).
        for item_toadd in toadd:
            print("Adding file: %s"%(item_toadd,))
            repo.index.add([item_toadd])
    
    def do_gitcommit(self, repo):
        commit_message = "Backup update at: %s"%( print(datetime.datetime.now()), )
        repo.index.commit(commit_message)

class CliBackupToolkit(BackupToolkit):
    
    def command_list(self):
        allbackups = self.config_db.gget(KEY_BACKUPS)
        for backupname in allbackups:
            print("Backup: %s"%backupname)
    
    def command_create(self, backupname, srcspec, dstspec):
        allbackups = self.config_db.gget(KEY_BACKUPS)
        if backupname in allbackups:
            print("Backup %s already exists."%backupname)
            exit(-1)
        # Init the backup:
        srcendpoint = rsynccall.Endpoint.parseSpec(srcspec)
        dstendpoint = rsynccall.Endpoint.parseSpec(dstspec)
        # Sanity check:
        if dstendpoint.conndata['proto'] != 'local':
            raise NotImplementedError("Backup destination must be a local endpoint, and «%s» is not local." % (dstspec,))
        # Init dst as a git repo:
        newRepo = Repo.init(dstendpoint.path)
        ### Update on DB:
        # Add to backup index on DB:
        allbackups.append(backupname)
        self.config_db.gput(KEY_BACKUPS, allbackups)
        # Add key for this backup:
        self.config_db.gput(backupname, {
            'srcendpoint': srcendpoint,
            'dstendpoint': dstendpoint,
            })
    
    def command_details(self, backupname):
        the_backup = self.get_backup(backupname)
        print("Details for backup %s:\n %s"%(backupname, str(the_backup)))
    
    def command_update_rsync(self, backupname):
        the_backup = self.get_backup(backupname)
        print("Updating backup with rsync %s:\n %s"%(backupname, str(the_backup)))
        self.do_rsync(the_backup)
    
    def command_update_git(self, backupname):
        the_backup = self.get_backup(backupname)
        print("Adding new files to repository of backup %s:\n %s"%(backupname, str(the_backup)))
        repo = Repo(the_backup['dstendpoint'].path)
        toadd = self.do_gitstatus(repo, the_backup)
        print("Files to add:\n%s"%(','.join(toadd),))
        self.do_gitadd(repo, toadd)
        self.do_gitcommit(repo)
        
    
    
    def command_hardremove(self, backupname):
        raise NotImplementedError
    def command_unlink(self, backupname):
        raise NotImplementedError


    def main(self):
        # Initialize config database:
        #homedir = os.getenv('HOME')
        self.homedir = expanduser("~")
        self.config_db = PythonBDB({
            'Endpoint':   rsynccall.Endpoint,
            })
        self.config_db.open(os.path.join(self.homedir, '.backup_toolkit_config.db'), dbtype=bdb.DB_HASH, flags=bdb.DB_CREATE)
        if self.config_db.gget(KEY_BACKUPS)==None:
            self.config_db.gput(KEY_BACKUPS, [])
        # Cmdline arguments:
        if len(sys.argv)<2:
            print("Syntax: %s command arguments"%(sys.argv[0],))
            exit(-1)
        thecommand = sys.argv[1]
        getattr(self, "command_"+thecommand)(*sys.argv[2:])

if __name__ == "__main__": CliBackupToolkit().main()


################
# Chamadas para teste:
#  ./BackupToolkit.py create xptotry3 /home/jj/Trab/jjComputadores/Explicações /home/jj/Desktop/backuptry
################


"""
https://www.jcea.es/programacion/pybsddb.htm
https://flylib.com/books/en/2.9.1.166/1/
"""
## See if some values are there:
#stored_data = config_db.gget('Backups')
#if stored_data is None:
#    print("Putting velue in DB.")
#    config_db.gput('Backups', ['Drive F', 'Drive G', 'Drive H', ])
#else:
#    print("Got the following value from DB: "+str(stored_data))
#return
#
## Do it:
#rsync = rsynccall.Rsync(
#    rsynccall.Endpoint(conndata={'proto': 'local'}, path="/home/jj/Trab/jjComputadores/Explicações"),
#    rsynccall.Endpoint(conndata={'proto': 'local'}, path="/home/jj/Desktop/backuptry") )
#rsync.add_args(RSYNC_ARGS)
#rsync.run()
