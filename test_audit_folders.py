#!/bin/env python3
# -*- coding: utf-8 -*-
import unittest, subprocess

class TestAuditFolders(unittest.TestCase):
    """
    Tests the audit_folders.py script.
    """
    
    def test_audit_folders_lists_everything(self):
        """
        The audit_folders.py script lists every file found.
        """
        self.assertTrue(False)
        subprocess

if __name__ == '__main__':
    unittest.main(verbosity=2)