import pdb

def dikt_linez(comm_res, colnames=False, skiplines=False):
    # Basic preprocessing the source string:
    fss_table = [ ln.split() for ln in comm_res.split('\n') ]
    # Sensible default arguments:
    if not skiplines:
        if colnames:
            # If col names were provided by caller, then most likely is they are NOT in the file, so no lines to skip.
            skiplines = 0
        else:
            # Otherwise, they are most likely to be taken from file, so skip 1 line by default when parsing.
            skiplines = 1
    if not colnames:
        colnames = fss_table[0]
    # Conversion:
    list_of_dikts = [
            dict([ (colnames[idx], ln[idx]) for idx in range(len(colnames)) ])
        for ln in fss_table[skiplines:] if len(ln)==len(colnames) ]
    return list_of_dikts

def find_mounted_fs(fss, fs_spec, fs_file):
    matches = [ fs for fs in fss
        if fs['fs_spec']==fs_spec and fs['fs_file']==fs_file ]
    return matches


