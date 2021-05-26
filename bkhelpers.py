import pdb

def dikt_linez(df_res, colnames=False, skiplines=False):
    # Basic preprocessing the source string:
    fss_table = [ ln.split() for ln in df_res.stdout.split('\n') ]
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

def get_mounted_fss(c):
    df_res = c.run("LC_ALL=C cat /proc/mounts")
    if df_res.failed:
        raise bkexceptions.VerificationFailed("Could not get list of mounted filesystems.")
    # First metadata:
    fss_dictionaries = dikt_linez(df_res, [
            'fs_spec',
            'fs_file',
            'fs_vfstype',
            'fs_mntops',
            'fs_freq',
            'fs_passno',    ])
    return fss_dictionaries

def find_mounted_fs(fss, fs_spec, fs_file):
    matches = [ fs for fs in fss
        if fs['fs_spec']==fs_spec and fs['fs_file']==fs_file ]
    return matches

def datasetname_to_path(c, dataset_name):
    return dataset_name.replace(c.BackupToolkit.ZFS_ROOT_POOLNAME, c.BackupToolkit.ZFS_ROOT_MOUNTPOINT)
def path_to_datasetname(c, path_name):
    return path_name.replace(c.BackupToolkit.ZFS_ROOT_MOUNTPOINT, c.BackupToolkit.ZFS_ROOT_POOLNAME)

def get_backup_profile(c, profilename):
    # Verify args:
    if profilename=='':
        raise bkexceptions.VerificationFailed("No backup profile specified. Available profiles are: %s" % (', '.join(c.BackupToolkit.PROFILES.keys())))
    # Get and return the profile:
    return c.BackupToolkit.PROFILES[profilename]
