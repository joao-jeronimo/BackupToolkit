#!/bin/env python3
# -*- coding: utf-8 -*-
import sys, os, zipfile, argparse
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

def main():
    ### Cmdline parsing:
    # Elementary:
    parser = argparse.ArgumentParser("Scans a directory for sensitive files")
    parser.add_argument("--noscan", type=str, help="Comma-separated list of scans to be skipped. For now only 'ok' is implemented.")
    parser.add_argument("rootfolder", type=str, help="The starting folder.")
    args = parser.parse_args()
    # Secundary:
    scantypes_to_skip = args.noscan.lower().split(',') if args.noscan else []
    ### Behaviour:
    for fullpath in scanfolders(folder = args.rootfolder):
        ### Preparation:
        file_basename = os.path.basename(fullpath)
        file_status = 'OK'
        ### Verify the file basename:
        if file_status == 'OK':
            file_status = audit_file_basename(file_basename)
        ### Report or scan inside file:
        if   file_status != 'OK':
            print("%-66s %s" % (fullpath, file_status))
        elif file_basename.lower().endswith('zip'):
            print("%-66s %s" % (fullpath, ">> Scanning inside zipfile ... >>"))
            thezip = zipfile.ZipFile(fullpath, mode='r')
            zipmembers = thezip.namelist()
            zipmembers.sort()
            for membpath in zipmembers:
                if membpath[-1] == '/':
                    continue
                subfile_status = audit_file_basename(os.path.basename(membpath))
                if ('ok' not in scantypes_to_skip) or (subfile_status != 'OK'):
                    print("    > %-64s %s" % (membpath, subfile_status))
        elif 'ok' not in scantypes_to_skip:
            print("%-66s %s" % (fullpath, file_status))

main()