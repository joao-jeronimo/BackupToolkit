import os
from datetime import datetime
from rsync_calls import do_rsync
from zfs_calls import zfs_create_snapshot, zfs_mount_dataset, zfs_list_datasets, zfs_find_dataset_in_list, zfs_create_dataset
import bkexceptions, bkhelpers
import pdb

def check_dataset_registry(c):
    missing_datasets = [
        misspair
        for misspair in [
                ( miss['localspecs']['dest_path'], bkhelpers.path_to_datasetname(c, miss['localspecs']['dest_path']))
                for miss in c.BackupToolkit.PROFILES.values()   ]
        if (misspair[1] not in c.BackupToolkit.ZFS_DATASETS) and (misspair[1] not in c.BackupToolkit.ZFS_SKIP_LIST)
        ]
    if any(missing_datasets):
        raise bkexceptions.VerificationFailed("Following backup destinations don't have their respective ZFS dataset registered in ZFS_DATASETS nor ZFS_SKIP_LIST lists:\n   %s"
                % ( "\n   ".join( [ repr(p) for p in missing_datasets ] ) ))

def check_fix_zfs_mounts(c, force_mount_datasets=False):
    # Get all ZFS mounts:
    all_mounted_fss = bkhelpers.get_mounted_fss(c)
    zfs_mounteds = [ fss for fss in all_mounted_fss
        if fss['fs_vfstype']=='zfs' ]
    # Build list of ZFS datasets to see if they are mounted:
    full_zfs_list = ( [c.BackupToolkit.ZFS_ROOT_POOLNAME] + c.BackupToolkit.ZFS_DATASETS )
    # See and report if any is not mounted:
    not_mounted_zfss = [
        nmf for nmf
        in full_zfs_list
        if not any ( bkhelpers.find_mounted_fs(zfs_mounteds, nmf, bkhelpers.datasetname_to_path(c, nmf)) )
        ]
    if any(not_mounted_zfss):
        # See if any dataset does not exist in real:
        zfs_datasets = zfs_list_datasets(c)
        nonexistant_datasets = [
                neds for neds in not_mounted_zfss
                if len(zfs_find_dataset_in_list(zfs_datasets, neds, bkhelpers.datasetname_to_path(c, neds)))==0
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
        if c.BackupToolkit.AUTO_MOUNT_DATASETS or force_mount_datasets:
            for to_mount in not_mounted_zfss:
                # Mount will throw error if dataset does not exist.
                zfs_mount_dataset(c, to_mount, su_do=True)
        else:
            raise bkexceptions.VerificationFailed((
                        "The following ZFS datasets are not mounted:\n"
                        "   %s\n"
                        "To mount them, set AUTO_MOUNT_DATASETS config option to true (not recommended) or run manually:\n"
                        "   invoke check-fix-zfs-mounts --force-mount-datasets\n"
                        "Further errors may be thrown if some datasets don't exist."
                ) % ( "\n   ".join(not_mounted_zfss) ))
