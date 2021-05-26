import bkconfigs
import pdb

def get_mounted_fss(c):
    df_res = c.run("LC_ALL=C cat /proc/mounts")
    if df_res.failed:
        raise bkexceptions.VerificationFailed("Could not get list of mounted filesystems.")
    # First metadata:
    fss_table = [ ln.split() for ln in df_res.stdout.split('\n') ]
    MOUNTS_COLNAMES = [
        'fs_spec',
        'fs_file',
        'fs_vfstype',
        'fs_mntops',
        'fs_freq',
        'fs_passno',    ]
    fss_dictionaries = [
            dict([ (MOUNTS_COLNAMES[idx], ln[idx]) for idx in range(len(MOUNTS_COLNAMES)) ])
        for ln in fss_table if len(ln)==len(MOUNTS_COLNAMES) ]
    return fss_dictionaries

def datasetname_to_path(dataset_name):
    return dataset_name.replace(bkconfigs.ZFS_ROOT_POOLNAME, bkconfigs.ZFS_ROOT_MOUNTPOINT)
def path_to_datasetname(path_name):
    return path_name.replace(bkconfigs.ZFS_ROOT_MOUNTPOINT, bkconfigs.ZFS_ROOT_POOLNAME)

def get_backup_profile(profilename):
    # Verify args:
    if profilename=='':
        raise bkexceptions.VerificationFailed("No backup profile specified. Available profiles are: %s" % (', '.join(bkconfigs.BACKUP_PROFILES.keys())))
    # Get and return the profile:
    return bkconfigs.BACKUP_PROFILES[profilename]
