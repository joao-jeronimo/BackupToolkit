#!/bin/env python3
# -*- coding: utf-8 -*-
import sys, os
from pathlib import Path

def scanfolders(folder):
    """
    Emulates the effect of the «find -type f» command.
        folder  The starting folder.
    """
    gen = Path(folder).rglob("*")
    for fol in gen:
        # Skip directories:
        if fol.is_dir():
            continue
        # Yield this path:
        if not fol.is_absolute():
            fol = os.path.join(os.path.curdir, fol)
        yield fol

for folpath in scanfolders(folder = sys.argv[1]):
    file_status = 'OK'
    # Verify the file basename:
    file_basename = os.path.basename(folpath)
    for extension in ['.key', '.ppk', '.pem', '.p12', ]:
        if file_basename.endswith(extension):
            file_status = f"!!! Sensitive extension '{extension[1:]}'."
    print("%-66s %s" % (folpath, file_status, ))
