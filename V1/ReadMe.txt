================================================
===== How to use: ==============================
================================================

# Dependencies installation:
#   sudo -H pip3 install invoke pyyaml addict
#   sudo apt install rsync
# Example task invocation (DEPRECATED COMMANDS!):
#   invoke --config=DriveH.yaml update-backup-global
#   invoke --config=DriveH.yaml update-backup-global --backup-profile=h_drive
# Example task invocation:
#   invoke update-backup-global
#   invoke update-backup-global --backup-profile=h_drive
# Configurations:
#   sudo /sbin/zfs allow jj create,snapshot,mount backupstank