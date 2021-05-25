
ZFS_ROOT_POOLNAME   = "backupstank"
ZFS_ROOT_MOUNTPOINT = "/home/jj/TestBackups/backups_tank"

BACKUP_PROFILES = {
    'h_drive': {
        'origspecs': {
            'portnr':           22,
            'orig_username':    "remotebackups",
            'orig_ip':          "192.168.100.105",
            'orig_path':        "/srv/storage/outras_drives_usl/h/"
            },
        'localspecs': {
            'dest_path':        "/home/jj/TestBackups/backups_tank/h_drive",
            }
        },
    #'outro_backup': {}
    }
