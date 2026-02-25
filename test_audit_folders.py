#!/bin/env python3
# -*- coding: utf-8 -*-
import unittest, subprocess

class TestAuditFolders(unittest.TestCase):
    """
    Tests the audit_folders.py script.
    """
    maxDiff = None
    
    def test_audit_folders_lists_everything(self):
        """
        The audit_folders.py script lists every file found.
        """
        prog_run = subprocess.run([ './audit_folders.py', './test_fixtures/test_audit_folders' ],
            check=True, stdout=subprocess.PIPE)
        splotten_stdout = [ l for l in str(prog_run.stdout, 'utf-8').split('\n') if len(l)>0 ]
        self.assertEqual(splotten_stdout, [
            "./test_fixtures/test_audit_folders/folder1/Mountpoints.zip         !!! Sensitive name fragment 'mountpoint'.",
            "./test_fixtures/test_audit_folders/folder1/bababakeybobobo         !!! Sensitive name fragment 'key'.",
            "./test_fixtures/test_audit_folders/folder1/file.key                !!! Sensitive extension 'key'.",
            "./test_fixtures/test_audit_folders/folder1/file.pem                !!! Sensitive extension 'pem'.",
            "./test_fixtures/test_audit_folders/folder1/file.ppk                !!! Sensitive extension 'ppk'.",
            "./test_fixtures/test_audit_folders/folder1/id_ed25519              !!! Sensitive name fragment 'id_ed25519'.",
            "./test_fixtures/test_audit_folders/folder1/id_rsa                  !!! Sensitive name fragment 'id_rsa'.",
            "./test_fixtures/test_audit_folders/folder2/Innocent file.txt       OK",
            "./test_fixtures/test_audit_folders/folder2/backup_colornote_mybake !!! Sensitive name fragment 'colornote'.",
            "./test_fixtures/test_audit_folders/folder2/containes_text          OK",
            "./test_fixtures/test_audit_folders/folder2/file.p12                !!! Sensitive extension 'p12'.",
            "./test_fixtures/test_audit_folders/folder2/folder3/mps.zip         OK",
            "./test_fixtures/test_audit_folders/folder2/folder4/as_martaes.txt  !!! Sensitive name fragment 'marta'.",
            "./test_fixtures/test_audit_folders/folder2/folder4/as_mulheres.txt !!! Sensitive name fragment 'mulher'.",
            "./test_fixtures/test_audit_folders/folder2/folder4/as_sofiaes.txt  !!! Sensitive name fragment 'sofia'.",
            ])

if __name__ == '__main__':
    unittest.main(verbosity=2)