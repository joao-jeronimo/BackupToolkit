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
