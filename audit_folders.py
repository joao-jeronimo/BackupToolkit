#!/bin/env python3
# -*- coding: utf-8 -*-
import sys, os
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

for folpath in scanfolders(folder = sys.argv[1]):
    file_status = 'OK'
    ### Verify the file basename:
    file_basename = os.path.basename(folpath)
    # Sensitive extensions:
    if file_status == 'OK':
        for extension in ['.key', '.ppk', '.pem', '.p12', ]:
            if file_basename.lower().endswith(extension):
                file_status = f"!!! Sensitive extension '{extension[1:]}'."
    # Sensitive name fragments:
    if file_status == 'OK':
        for fragment in ['id_rsa', 'id_ed25519', 'mountpoint', 'key', 'colornote', 'marta', 'sofia', 'mulher', ]:
            if fragment in file_basename.lower():
                file_status = f"!!! Sensitive name fragment '{fragment}'."
    print("%-66s %s" % (folpath, file_status, ))
