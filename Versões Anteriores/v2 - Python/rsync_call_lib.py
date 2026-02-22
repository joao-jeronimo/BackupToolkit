#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess, re

class Endpoint:
    def __init__(self, conndata, path):
        """
        Represents a rsync source or destination.
         * conndata - A dictionary with at least "proto" key. Other keys
                are protocol dependent. "proto" may be "local", meaning a
                local file or directory.
         * path - A local or remote path.
        """
        self.conndata = conndata
        self.path = path
    
    def parseSpec(endpoint_spec):
        if   endpoint_spec.startswith("file://"):
            return Endpoint(conndata={'proto': 'local'}, path=endpoint_spec[len("file://"):])
        elif ':' not in endpoint_spec:
            return Endpoint(conndata={'proto': 'local'}, path=endpoint_spec)
        elif ':' in endpoint_spec:
            speccomps = re.findall("([a-zA-Z0-9]+@)?([a-zA-Z0-9_.-]+:)([0-9]+:)?(.+)", endpoint_spec)
            speckeys = {
                'username':     (speccomps[0] or '@')[:-1],
                'hostname':     (speccomps[1] or ':')[:-1],
                'port':         (speccomps[3] or ':')[:-1],
                'path':         speccomps[4],
                }
            if   not speckeys['hostname']:
                print ("Hostname not provided for endpoint '%s'."%endpoint_spec)
                exit(-1)
            elif not speckeys['username']:
                speckeys['username'] = 'jj'
            elif not speckeys['port']:
                speckeys['port'] = '22'
            elif not speckeys['path']:
                speckeys['path'] = '/home/jj'
            return Endpoint(conndata={
                        'proto': 'ssh',
                        'host': speckeys['hostname'],
                        'port': speckeys['port'],
                        'username': speckeys['username'],
                    }, path=speckeys['path'])
    
    def build_endpoint_spec(self):
        if self.conndata['proto'] == 'local':
            return [self.path]
        elif self.conndata['proto'] == 'ssh':
            port = self.conndata['port']
            username = self.conndata['username']
            host = self.conndata['host']
            return ['--port='+str(port), username+'@'+host+':'+self.path]
        else:
            raise BaseException("Unknown protocol "+self.conndata['proto'])
    
    def __repr__(self):
        return "Endpoint(conndata=%s, path=%s)" % (repr(self.conndata), repr(self.path,))
        #reprdict = dict()
        #for k in ('conndata', 'path',):
        #    reprdict[k] = repr( getattr(self, k) )
        #return "type('Endpoint', (object,), %s)" % repr(reprdict)
    
    def __src__(self):
        return "Endpoint(conndata=%s, path=%s)" % (self.conndata, self.path,)

class Rsync:
    rsync_args = []
    
    def __init__(self, source, destination):
        if source.conndata['proto'] != 'local' and destination.conndata['proto'] != 'local':
            raise BaseException("For rsync to work, either source or destination (or both)"+
                                " must be local. Can't rsync between two remote hosts.")
        self.source = source
        self.destination = destination
    
    def add_args(self, additionals):
        self.rsync_args += additionals
    
    #def gauge(self):
    #    """
    #    Tries to gauge the size of a rsync proccess. This may be somewhat
    #    blind, not taking into account file sizes or the amount of data
    #    that actually needs to be synched.
    #    Returns a RsyncProccess.
    #    """
    #    return RsyncProccess(None)
    
    def run(self):
        """
        Actually runs rsync between source and destination.
        Returns a RsyncProccess.
        """
        command = (["rsync"]
            + self.rsync_args
            + self.source.build_endpoint_spec()
            + self.destination.build_endpoint_spec() )
        print("Command to run: "+str(command))
        
        theproc = subprocess.Popen(command,
                stdin=subprocess.DEVNULL,
                stdout=None,
                stderr=subprocess.STDOUT)
        return RsyncProccess(theproc)

class RsyncProccess:
    """
    Represents a rsync proccess and can be used to kill, pause, monitor, or
    elsehow control, it. Proccesses are not necessarily persistent from the
    point of view of this library.
    """
    def __init__(self, proc):
        self.proc = proc
