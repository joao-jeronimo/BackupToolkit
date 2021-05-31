import os
from datetime import datetime
from .rsync_calls import do_rsync
from .zfs_calls import zfs_create_snapshot, zfs_mount_dataset, zfs_list_datasets, zfs_find_dataset_in_list, zfs_create_dataset
from . import bkexceptions, bkhelpers
import pdb


class BackupEngine:

    def __init__(self, ictx):
        self.ictx = ictx
    
    def check_dataset_registry(self):
        missing_datasets = [
            misspair
            for misspair in [
                    ( miss['localspecs']['dest_path'], bkhelpers.path_to_datasetname(self.ictx, miss['localspecs']['dest_path']))
                    for miss in self.ictx.BackupToolkit.PROFILES.values()   ]
            if (misspair[1] not in self.ictx.BackupToolkit.ZFS_DATASETS) and (misspair[1] not in self.ictx.BackupToolkit.ZFS_SKIP_LIST)
            ]
        if any(missing_datasets):
            raise bkexceptions.VerificationFailed("Following backup destinations don't have their respective ZFS dataset registered in ZFS_DATASETS nor ZFS_SKIP_LIST lists:\n   %s"
                    % ( "\n   ".join( [ repr(p) for p in missing_datasets ] ) ))

    def check_fix_zfs_mounts(self, force_mount_datasets=False):
        # Get all ZFS mounts:
        all_mounted_fss = bkhelpers.get_mounted_fss(self.ictx)
        zfs_mounteds = [ fss for fss in all_mounted_fss
            if fss['fs_vfstype']=='zfs' ]
        # Build list of ZFS datasets to see if they are mounted:
        full_zfs_list = ( [self.ictx.BackupToolkit.ZFS_ROOT_POOLNAME] + self.ictx.BackupToolkit.ZFS_DATASETS )
        # See and report if any is not mounted:
        not_mounted_zfss = [
            nmf for nmf
            in full_zfs_list
            if not any ( bkhelpers.find_mounted_fs(zfs_mounteds, nmf, bkhelpers.datasetname_to_path(self.ictx, nmf)) )
            ]
        if any(not_mounted_zfss):
            # See if any dataset does not exist in real:
            zfs_datasets = zfs_list_datasets(self.ictx)
            nonexistant_datasets = [
                    neds for neds in not_mounted_zfss
                    if len(zfs_find_dataset_in_list(zfs_datasets, neds, bkhelpers.datasetname_to_path(self.ictx, neds)))==0
                    ]
            if any(nonexistant_datasets):
                raise bkexceptions.VerificationFailed((
                            "The following datasets do not exist in ZFS namespace:\n"
                            "   %s\n"
                            "To create them, run the following command:\n"
                            "   invoke --config=ConfigFile.yaml create-zfs-assets --dry-run\n"
                            "   invoke --config=ConfigFile.yaml create-zfs-assets"
                    ) % ( "\n   ".join(not_mounted_zfss) ))
            # Mount may be forced by config flag, but is not recomended because may require root privileges:
            if self.ictx.BackupToolkit.AUTO_MOUNT_DATASETS or force_mount_datasets:
                for to_mount in not_mounted_zfss:
                    # Mount will throw error if dataset does not exist.
                    zfs_mount_dataset(self.ictx, to_mount, su_do=True)
            else:
                raise bkexceptions.VerificationFailed((
                            "The following ZFS datasets are not mounted:\n"
                            "   %s\n"
                            "To mount them, set AUTO_MOUNT_DATASETS config option to true (not recommended) or run manually:\n"
                            "   invoke check-fix-zfs-mounts --force-mount-datasets\n"
                            "Further errors may be thrown if some datasets don't exist."
                    ) % ( "\n   ".join(not_mounted_zfss) ))



    def create_zfs_assets(self, dry_run=False):
        # Find datasets that do not exist:
        zfs_datasets = zfs_list_datasets(self.ictx)
        nonexistant_datasets = [
                neds for neds in self.ictx.BackupToolkit.ZFS_DATASETS
                if len(zfs_find_dataset_in_list(zfs_datasets, neds, bkhelpers.datasetname_to_path(self.ictx, neds)))==0
                ]
        # Create them, or elsewise print them:
        for dstc in nonexistant_datasets:
            # Calculate related values:
            datasetname = dstc
            mountpoint = bkhelpers.datasetname_to_path(self.ictx, datasetname)
            # Verify if the folder is already there, and rmdir it if so:
            if os.path.isdir(mountpoint):
                # Is the empty folder cannot be deleted, then we can't do anything for you!
                os.rmdir(mountpoint)
            # Call dataset creation:
            zfs_create_dataset(self.ictx, datasetname, mountpoint, dry_run=dry_run)

    def update_backup_rsync(self, backup_profile=""):
        the_profile = bkhelpers.get_backup_profile(self.ictx, backup_profile)
        # Do the update:
        print("== Updating backup named '%s'" % backup_profile)
        rsync_parms = {
            **the_profile['origspecs'],
            'dest_path': the_profile['localspecs']['dest_path'],
            }
        print(repr(rsync_parms))
        rsync_result = do_rsync(self.ictx, **rsync_parms)
        if rsync_result.failed:
            raise bkexceptions.VerificationFailed("Rsync failed for %s" % repr(rsync_parms))
        return "Correu bem!"

    def update_backup_global(self, backup_profile=""):
        # Do the rsync part:
        if not backup_profile and len(self.ictx.BackupToolkit.PROFILES.keys())==1:
            backup_profile = tuple(self.ictx.BackupToolkit.PROFILES.keys())[0]
        self.update_backup_rsync(backup_profile)
        # Get important string and names:
        the_profile = bkhelpers.get_backup_profile(self.ictx, backup_profile)
        datasetname = bkhelpers.path_to_datasetname(self.ictx, the_profile['localspecs']['dest_path'])
        # Build a name for the snapshot:
        nowtime = datetime.now()
        snapshot_name = "Backup_%04d%02d%02d_%02d%02d%02d" % (
                nowtime.year,
                nowtime.month,
                nowtime.day,
                nowtime.hour,
                nowtime.minute,
                nowtime.second,
                )
        # Now, then, create the ZFS snapshot:
        zfs_create_snapshot(self.ictx, datasetname, snapshot_name)
