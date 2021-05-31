import os, yaml
from addict import Dict
from datetime import datetime
from .rsync_calls import do_rsync
from .zfs_calls import zfs_create_snapshot, zfs_mount_dataset, zfs_list_datasets, zfs_find_dataset_in_list, zfs_create_dataset
from . import bkexceptions, bkhelpers
import pdb


class BackupEngine:

    def __init__(self, ictx):
        self.ictx = ictx
        # Find and lioad config file:
        with open( self.find_config_file_path() ) as file:
            loaded_config = yaml.load(file, Loader=yaml.FullLoader)
            self.config = Dict(loaded_config)
    
    def find_config_file_path(self):
        return "./BackupToolkitConfig.yaml"
    
    def _check_dataset_registry(self):
        missing_datasets = [
            misspair
            for misspair in [
                    ( miss['localspecs']['dest_path'], self.path_to_datasetname(miss['localspecs']['dest_path']))
                    for miss in self.config.BackupToolkit.PROFILES.values()   ]
            if (misspair[1] not in self.config.BackupToolkit.ZFS_DATASETS) and (misspair[1] not in self.config.BackupToolkit.ZFS_SKIP_LIST)
            ]
        if any(missing_datasets):
            raise bkexceptions.VerificationFailed("Following backup destinations don't have their respective ZFS dataset registered in ZFS_DATASETS nor ZFS_SKIP_LIST lists:\n   %s"
                    % ( "\n   ".join( [ repr(p) for p in missing_datasets ] ) ))

    def _check_fix_zfs_mounts(self, backup_profile="", force_mount_datasets=False):
        # Get all ZFS mounts:
        all_mounted_fss = self.get_mounted_fss()
        zfs_mounteds = [ fss for fss in all_mounted_fss
            if fss['fs_vfstype']=='zfs' ]
        # Build list of ZFS datasets to see if they are mounted:
        full_zfs_list = [self.config.BackupToolkit.ZFS_ROOT_POOLNAME]
        if backup_profile:
            profile_obj = self.config.BackupToolkit.PROFILES[backup_profile]
            profile_mp = profile_obj.localspecs.dest_path
            datasets_to_add = [ self.path_to_datasetname(profile_mp) ]
            full_zfs_list += datasets_to_add
        else:
            full_zfs_list += self.config.BackupToolkit.ZFS_DATASETS
        # See and report if any is not mounted:
        not_mounted_zfss = [
            nmf for nmf
            in full_zfs_list
            if not any ( bkhelpers.find_mounted_fs(zfs_mounteds, nmf, self.datasetname_to_path(nmf)) )
            ]
        if any(not_mounted_zfss):
            # See if any dataset does not exist in real:
            zfs_datasets = zfs_list_datasets(self)
            nonexistant_datasets = [
                    neds for neds in not_mounted_zfss
                    if len(zfs_find_dataset_in_list(zfs_datasets, neds, self.datasetname_to_path(neds)))==0
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
            if self.config.BackupToolkit.AUTO_MOUNT_DATASETS or force_mount_datasets:
                for to_mount in not_mounted_zfss:
                    # Mount will throw error if dataset does not exist.
                    zfs_mount_dataset(self, to_mount, su_do=True)
            else:
                raise bkexceptions.VerificationFailed((
                            "The following ZFS datasets are not mounted:\n"
                            "   %s\n"
                            "To mount them, set AUTO_MOUNT_DATASETS config option to true (not recommended) or run manually:\n"
                            "   invoke check-fix-zfs-mounts --force-mount-datasets\n"
                            "Further errors may be thrown if some datasets don't exist."
                    ) % ( "\n   ".join(not_mounted_zfss) ))



    def _create_zfs_assets(self, dry_run=False):
        # Find datasets that do not exist:
        zfs_datasets = zfs_list_datasets(self)
        nonexistant_datasets = [
                neds for neds in self.config.BackupToolkit.ZFS_DATASETS
                if len(zfs_find_dataset_in_list(zfs_datasets, neds, self.datasetname_to_path(neds)))==0
                ]
        # Create them, or elsewise print them:
        for dstc in nonexistant_datasets:
            # Calculate related values:
            datasetname = dstc
            mountpoint = self.datasetname_to_path(datasetname)
            # Verify if the folder is already there, and rmdir it if so:
            if os.path.isdir(mountpoint):
                # Is the empty folder cannot be deleted, then we can't do anything for you!
                os.rmdir(mountpoint)
            # Call dataset creation:
            zfs_create_dataset(self, datasetname, mountpoint, dry_run=dry_run)

    def _update_backup_rsync(self, backup_profile=""):
        the_profile = self.get_backup_profile(backup_profile)
        # Do the update:
        print("== Updating backup named '%s'" % backup_profile)
        rsync_parms = {
            **the_profile['origspecs'],
            'dest_path': the_profile['localspecs']['dest_path'],
            }
        print(repr(rsync_parms))
        rsync_result = do_rsync(self, **rsync_parms)
        if rsync_result.failed:
            raise bkexceptions.VerificationFailed("Rsync failed for %s" % repr(rsync_parms))
        return "Correu bem!"

    def _update_backup_global(self, backup_profile=""):
        # Do the rsync part:
        if not backup_profile and len(self.config.BackupToolkit.PROFILES.keys())==1:
            backup_profile = tuple(self.config.BackupToolkit.PROFILES.keys())[0]
        self._update_backup_rsync(backup_profile)
        # Get important string and names:
        the_profile = self.get_backup_profile(backup_profile)
        datasetname = self.path_to_datasetname(the_profile['localspecs']['dest_path'])
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
        zfs_create_snapshot(self, datasetname, snapshot_name)
    
    # Too call from outside - only do checks once:
    def check_dataset_registry(self):
        return self._check_dataset_registry()
    def check_fix_zfs_mounts(self, backup_profile="", force_mount_datasets=False):
        self._check_dataset_registry()
        return self._check_fix_zfs_mounts(backup_profile, force_mount_datasets)
    def create_zfs_assets(self, dry_run=False):
        self._check_dataset_registry()
        return self._create_zfs_assets(dry_run)
    def update_backup_rsync(self, backup_profile=""):
        self._check_fix_zfs_mounts(backup_profile)
        return self._update_backup_rsync(backup_profile)
    def update_backup_global(self, backup_profile=""):
        self._check_fix_zfs_mounts(backup_profile)
        return self._update_backup_global(backup_profile)

    # Helper methods:
    def get_mounted_fss(self):
        df_res = self.ictx.run("LC_ALL=C cat /proc/mounts")
        if df_res.failed:
            raise bkexceptions.VerificationFailed("Could not get list of mounted filesystems.")
        # First metadata:
        fss_dictionaries = bkhelpers.dikt_linez(df_res.stdout, [
                'fs_spec',
                'fs_file',
                'fs_vfstype',
                'fs_mntops',
                'fs_freq',
                'fs_passno',    ])
        return fss_dictionaries
    
    def datasetname_to_path(self, dataset_name):
        return dataset_name.replace(self.config.BackupToolkit.ZFS_ROOT_POOLNAME, self.config.BackupToolkit.ZFS_ROOT_MOUNTPOINT)
    def path_to_datasetname(self, path_name):
        return path_name.replace(self.config.BackupToolkit.ZFS_ROOT_MOUNTPOINT, self.config.BackupToolkit.ZFS_ROOT_POOLNAME)

    def get_backup_profile(self, profilename):
        # Verify args:
        if profilename=='':
            raise bkexceptions.VerificationFailed("No backup profile specified. Available profiles are: %s" % (', '.join(self.config.BackupToolkit.PROFILES.keys())))
        # Get and return the profile:
        return self.config.BackupToolkit.PROFILES[profilename]

