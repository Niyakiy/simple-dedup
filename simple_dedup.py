#!/usr/bin/env python

import logging
from os import (walk, stat)
from os.path import (
    join as os_join,
    exists)
from difflib import SequenceMatcher


class Directory:
    def __init__(self, abs_path):
        self.file_list = []
        self.file_count = 0
        self.path = ""


def load_directory(dir_path):
    for dir, subdirs, files in walk(dir_path):
        print(dir, subdirs, files)


def simple_file_compare(file1, file2):
    """
    Compares file name, size and last modification time
    to guess if files are the same
    :param file1: absolute path to file1
    :param file2: absolute path to file2
    :return: bool
    """

    # checking file names usign difflib
    matcher = SequenceMatcher(a=file1, b=file2)
    print(matcher.ratio())

    f1stats = stat(file1) if exists(file1) else None
    f2stats = stat(file2) if exists(file2) else None

    if not f1stats:
        logging.warning("File {} doesn't exist!".format(file1))
        return False
    if not f2stats:
        logging.warning("File {} doesn't exist!".format(file2))
        return False

    # checking size
    if f1stats.st_size == f2stats.st_size:
        return True

    return False

def main():
    print("")

if __name__ == "__main__":
    load_directory("d:\\backup")