#!/usr/bin/env python3

"""
Simple duplicate files searching script

Usage:
  simple_dedup.py <DIR> [options]

Options:
  --help     Show help
  --verbose  Add some debugging noise
  --exclude-extentions=<>
"""

import collections
import logging
from os import (walk, path)
from docopt import docopt

LOGGER = logging.getLogger(__name__)


def load_directory_content(path):
    """
    Scan whole dir/subdirs and return files

    :param path:
    :return:
    """
    return_files = []
    for directory, subdirectories, files in walk(path):
        LOGGER.warning('Processing dir %s', directory)
        return_files.extend(
            [(directory, file) for file in files]
        )
    return return_files


class DedupDirectoryProcessor:
    """
    Class to locate duplicated files
    """

    def __init__(self, abs_path):
        """
        Init

        :param abs_path:
        """
        self.file_list = []
        self.file_count = 0
        self.path = abs_path
        self.duplicate_with_counts = {}

    def load_directory(self):
        """
        Load directory content

        :return:
        """
        self.file_list = load_directory_content(self.path)
        self.file_count = len(self.file_list)
        LOGGER.warning('Found %i files.' % self.file_count)

    def search_same_name(self):
        """
        Get file names with 2 and more occurences in different dirs

        :return:
        """
        counts = collections.Counter([item[1] for item in self.file_list]).most_common()
        self.duplicate_with_counts = list(filter(
            lambda x: x[1] > 1,
            counts
        ))

    def make_duplicates_list(self):
        """
        Print to stdout files with same name and their path/size

        :return:
        """
        for count_info in self.duplicate_with_counts:
            print('-'*30)
            print("File:", count_info[0])
            all_file_locations = [
                f"{file_info[0]}/{file_info[1]}" for file_info in filter(
                    lambda x: x[1] == count_info[0],
                    self.file_list
                )
            ]
            print('\n'.join([f"{file} (size:{path.getsize(file)})" for file in sorted(
                all_file_locations,
                key=path.getsize,
                reverse=True
            )]))


if __name__ == "__main__":
    arguments = docopt(__doc__)
    if arguments['--verbose']:
        print("Script's arguments: ", arguments)
    d = DedupDirectoryProcessor(arguments['<DIR>'])
    d.load_directory()
    d.search_same_name()
    d.make_duplicates_list()

