#!/usr/bin/env python3

# STD lib
import os

# External
import natsort

MUSIC_FILES = ['mp3', 'wav', 'ogg', 'flac']


def load_directory_content(directory, type_list=None):

    flist = []
    for root, dirlist, filelist in os.walk(directory):

        flist.extend([os.path.join(root, file) for file in filelist])

    return list(filter(lambda x: _is_file_of_type(x, type_list), flist)) if type_list else flist


def _files_are_same(file_path1, file_path2):
    f1stats = os.stat(file_path1)
    f2stats = os.stat(file_path2)

    return f1stats.st_size == f2stats.st_size


def _is_file_of_type(file_path, type_list):
    return list(os.path.splitext(file_path))[1].lstrip('.') in type_list


def _extract_file_name(path):
    return list(os.path.split(path))[1]


def _map_files(file_list):
    return list(map(
        lambda x: {_extract_file_name(x): x},
        file_list
    ))


def _reduce_files(file_list):

    seen = set()
    file_names = list(map(lambda x: list(x.keys())[0], file_list))

    seen_twice = set(x for x in file_names if x in seen or seen.add(x))

    return list(filter(lambda x: list(x.keys())[0] in seen_twice, file_list))


if __name__ == "__main__":

    rf = _reduce_files(_map_files(load_directory_content('r:\\music\\lp', MUSIC_FILES)))


    print('\n'.join([str(f) for f in natsort.natsorted(rf, key=lambda x: list(x.values())[0])]))

    print(len(rf))

    #print('\n'.join(fl))

