
ZFS_BIN = "/sbin/zfs"
ZFS_ROOT_POOLNAME   = "backupstank"
ZFS_ROOT_MOUNTPOINT = "/home/jj/TestBackups/backups_tank"

RSYNC_BIN = "/usr/bin/rsync"
RSYNC_EXCLUSIONS = [ ".recycle", ".zfs", ]

ZFS_DATASETS = [
    "backupstank/h_drive"
    ]
ZFS_SKIP_LIST = [
    "backupstank/f_drive"
    ]

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

### Advanced options:
# Forces ZFS datasets be auto-mounted if they are unmounted at backup time. This is not recomended
# because mount may require root priviledges.
# If you want to make sure that everything is mounted, run the following command manually or as root via cron:
#  invoke check-fix-zfs-mounts --force-mount-datasets
AUTO_MOUNT_DATASETS = False
