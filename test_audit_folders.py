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
        prog_run = subprocess.run([ './audit_folders.py', './test_fixtures' ],
            check=True, stdout=subprocess.PIPE)
        self.assertEqual(str(prog_run.stdout, 'utf-8'), (
            "./test_fixtures/test_audit_folders/folder1/file.keys\n"
            "./test_fixtures/test_audit_folders/folder1/bababakeybobobo\n"
            "./test_fixtures/test_audit_folders/folder1/file.ppk\n"
            "./test_fixtures/test_audit_folders/folder1/file.pem\n"
            "./test_fixtures/test_audit_folders/folder1/id_ed25519\n"
            "./test_fixtures/test_audit_folders/folder1/Mountpoints.zip\n"
            "./test_fixtures/test_audit_folders/folder1/id_rsa\n"
            "./test_fixtures/test_audit_folders/folder2/folder4/as_martaes.txt\n"
            "./test_fixtures/test_audit_folders/folder2/folder4/as_sofiaes.txt\n"
            "./test_fixtures/test_audit_folders/folder2/folder4/as_mulheres.txt\n"
            "./test_fixtures/test_audit_folders/folder2/folder3/mps.zip\n"
            "./test_fixtures/test_audit_folders/folder2/file.p12\n"
            "./test_fixtures/test_audit_folders/folder2/backup_colornote_mybake\n"
            "./test_fixtures/test_audit_folders/folder2/containes_text\n"
            ))

if __name__ == '__main__':
    unittest.main(verbosity=2)