#!/bin/env python3
# -*- coding: utf-8 -*-
import sys, os, zipfile, mmap
from pathlib import Path

def scanfolders(folder):
    """
    Emulates the effect of the «find -type f» command.
        folder  The starting folder.
    """
    here_subs = os.listdir(folder)
    here_subs.sort()
    for subfolder in here_subs:
        subpath = os.path.join(folder, subfolder)
        if os.path.isdir(subpath):
            for subsub in scanfolders(subpath):
                yield subsub
        else:
            yield subpath

def audit_file_basename(flbn):
    """
    Audits a file basename (i.e. file name and extension without it's path),
    returning a human-readable findingm or OK if no finding.
        flbn    The file name to audit.
    """
    file_status = 'OK'
    # Sensitive extensions:
    if file_status == 'OK':
        for extension in ['.key', '.ppk', '.pem', '.p12', ]:
            if flbn.lower().endswith(extension):
                file_status = f"!!! Sensitive extension '{extension[1:]}'."
    # Sensitive name fragments:
    if file_status == 'OK':
        for fragment in ['id_rsa', 'id_ed25519', 'mountpoint', 'key', 'colornote', 'marta', 'sofia', 'mulher', ]:
            if fragment in flbn.lower():
                file_status = f"!!! Sensitive name fragment '{fragment}'."
    return file_status

def audit_file_contents(flpath):
    """
    Audits file contents using mmap().
        flpath  The path of the file to audit.
    """
    ### Memory-map the file:
    with open(flpath, "rb") as fl:
        mmap.mmap(  fl.fileno(), length=0, flags=MAP_SHARED,
                    prot=PROT_WRITE | PROT_READ, access=ACCESS_DEFAULT,
                    offset=0, trackfd=True)
    
    return 'OK'

def main():
    for fullpath in scanfolders(folder = sys.argv[1]):
        # Preparation:
        file_basename = os.path.basename(fullpath)
        file_status = 'OK'
        ### Verify the file basename:
        if file_status == 'OK':
            file_status = audit_file_basename(file_basename)
        ### Verify file contents:
        if file_status == 'OK':
            file_status = audit_file_contents(fullpath)
        ### Print file status:
        print("%-66s %s" % (fullpath, file_status, ))
        ### Inspect zip files:
        if file_status == 'OK' and file_basename.lower().endswith('zip'):
            thezip = zipfile.ZipFile(fullpath, mode='r')
            zipmembers = thezip.namelist()
            zipmembers.sort()
            for membpath in zipmembers:
                if membpath[-1] == '/':
                    continue
                subfile_status = audit_file_basename(os.path.basename(membpath))
                #if subfile_status != 'OK':
                #    file_status = '>>> Sensitive contents inside ZIP file:'
                print("    > %-64s %s" % (membpath, subfile_status))
main()