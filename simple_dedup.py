#!/usr/bin/env python3

"""
Simple duplicate files searching script

Usage:
  simple_dedup.py <DIR> [options]

Options:
  --help                       Show help
  --verbose                    Add some debugging noise
  --exclude-extentions=<EXTs>  CSV extensions to remove from dudup
  --show-same-size-only
"""

import collections
import logging
from os import (walk, path)
from docopt import docopt

LOGGER = logging.getLogger(__name__)


def filter_by_extensions(path, excluded_extensions):
    """
    Filter if path's file extension isn't in excluded_extensions

    :param path:
    :param excluded_extensions:
    :return:
    """
    for ext in excluded_extensions:
        if path.endswith(ext):
            return False

    return True


class DedupDirectoryProcessor:
    """
    Class to locate duplicated files
    """

    def __init__(self, abs_path, excluded_extensions=None, same_size_only=False):
        """
        Init

        :param abs_path:
        """
        self.file_list = []
        self.file_count = 0
        self.path = abs_path
        self.excluded_extensions = list(excluded_extensions) if excluded_extensions else []
        self.same_size_only = same_size_only
        self.duplicate_with_counts = {}

    def load_directory(self):
        """
        Load directory content

        :return:
        """
        for directory, subdirectories, files in walk(self.path):
            LOGGER.warning('Processing dir %s', directory)
            if self.excluded_extensions:
                self.file_list.extend(
                    [(directory, file) for file in files if filter_by_extensions(
                        file, self.excluded_extensions)]
                )
            else:
                self.file_list.extend(
                    [(directory, file) for file in files]
                )
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
            all_files_info = list(sorted(
                map(
                    lambda x: (x, path.getsize(x)),
                    [f"{file_info[0]}/{file_info[1]}" for file_info in filter(
                        lambda x: x[1] == count_info[0],
                        self.file_list
                    )]
                ),
                key=lambda x: x[1],
                reverse=True
            ))

            if self.same_size_only:
                same_sizes_counter = list(map(
                    lambda x: x[0],
                    filter(
                        lambda x: x[1] > 1,
                        collections.Counter([
                            file_info[1] for file_info in all_files_info
                        ]).items()
                    )
                ))

                same_sizes_files = list(filter(
                    lambda x: x[1] in same_sizes_counter,
                    all_files_info
                ))

                if same_sizes_files:
                    print('\n'.join([f"{file_info[0]} (size: {file_info[1]})" for file_info in same_sizes_files]))
            else:
                # Simply print all found files
                print('\n'.join([f"{file_info[0]} (size: {file_info[1]})" for file_info in all_files_info]))


if __name__ == "__main__":
    arguments = docopt(__doc__)
    if arguments['--verbose']:
        print("Script's arguments: ", arguments)
    exclusions = []
    if arguments['--exclude-extentions']:
        exclusions = arguments['--exclude-extentions'].split(',')
    d = DedupDirectoryProcessor(
        arguments['<DIR>'],
        excluded_extensions=exclusions,
        same_size_only=arguments['--show-same-size-only']
    )
    d.load_directory()
    d.search_same_name()
    d.make_duplicates_list()

