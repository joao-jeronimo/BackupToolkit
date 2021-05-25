
def get_mounted_fss(c):
    df_res = c.run("LC_ALL=C df -h")
    if df_res.failed:
        raise bkexceptions.VerificationFailed("Could not verify if ZFS is mounted.")
    ### Process df output to see of the ZFS pool is there:
    # First metadata:
    df_lines = [ ln.strip() for ln in df_res.stdout.split('\n') ]
    df_header_line = df_lines[0]
    df_fs_lines = df_lines[0]
    # Now, normal output:
    return [{
        
        } for oneline in df_fs_lines]
    
    
    
