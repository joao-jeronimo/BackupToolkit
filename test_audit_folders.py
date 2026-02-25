#!/bin/env python3
# -*- coding: utf-8 -*-
import unittest, subprocess

def sorted_list(thelist):
    lll = thelist.copy()
    lll.sort()
    return lll

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
        sorted_stdout = sorted_list([
            li
            for li in str(prog_run.stdout, 'utf-8').split('\n')
            if len(li) > 0
            ])
        self.assertEqual(sorted_stdout, sorted_list([
            "./test_fixtures/test_audit_folders/folder1/file.key",
            "./test_fixtures/test_audit_folders/folder1/bababakeybobobo",
            "./test_fixtures/test_audit_folders/folder1/file.ppk",
            "./test_fixtures/test_audit_folders/folder1/file.pem",
            "./test_fixtures/test_audit_folders/folder1/id_ed25519",
            "./test_fixtures/test_audit_folders/folder1/Mountpoints.zip",
            "./test_fixtures/test_audit_folders/folder1/id_rsa",
            "./test_fixtures/test_audit_folders/folder2/folder4/as_martaes.txt",
            "./test_fixtures/test_audit_folders/folder2/folder4/as_sofiaes.txt",
            "./test_fixtures/test_audit_folders/folder2/folder4/as_mulheres.txt",
            "./test_fixtures/test_audit_folders/folder2/folder3/mps.zip",
            "./test_fixtures/test_audit_folders/folder2/file.p12",
            "./test_fixtures/test_audit_folders/folder2/backup_colornote_mybake",
            "./test_fixtures/test_audit_folders/folder2/containes_text",
            ]))

if __name__ == '__main__':
    unittest.main(verbosity=2)