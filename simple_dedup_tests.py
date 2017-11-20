#!/usr/bin/env python3

import unittest
from os.path import join as os_join
from simple_dedup import (simple_file_compare)


class TestSimpleDedup(unittest.TestCase):

    def setUp(self):
        self.test_folder_path = "test-resources"
        self.test_source_folder_path = os_join(self.test_folder_path, "source_dir")
        self.test_target_folder_path = os_join(self.test_folder_path, "target_dir")

    def test_simple_file_compare(self):
        self.assertTrue(
            simple_file_compare(os_join(self.test_source_folder_path, "test_file1.txt"),
                                os_join(self.test_target_folder_path, "test_file1.txt")
                                )
        )


if __name__ == '__main__':
    unittest.main()
