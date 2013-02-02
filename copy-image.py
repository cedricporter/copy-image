#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Hua Liang[Stupid ET] <et@everet.org>
#
import os
import shutil
from hashlib import md5
from glob import glob
from collections import defaultdict

dir = '.'
output_dir = 'output'
trash_dir = '/tmp/image-trash'
MIN_SIZE = 30000                # 30KB


def prepare():
    try:
        os.mkdir(output_dir)
    except:
        pass


def trash(filename):
    try: os.mkdir(trash_dir)
    except: pass
    try:
        shutil.move(filename, trash_dir)
    except:
        pass


def filesize_filter(filename):
    '''Trash the file smaller than min_size'''
    size = os.path.getsize(filename)
    if size < MIN_SIZE:
        trash(filename)


def filter():
    for f in os.listdir(output_dir):
        filesize_filter(os.path.normpath(output_dir + os.sep + f))


def md5_file(name):
    m = md5()
    with open(name, 'rb') as f:
        m.update(f.read())
        f.close()
    return m.hexdigest()


def uniq_file():
    '''Remove duplicate files

    Note: it will save one file from duplicate list if the file is
          bigger than MIN_SIZE.
    '''
    name_dict = defaultdict(list)
    for f in glob(os.path.normpath(output_dir + os.sep + "*.jpg")):
        m = md5_file(f)
        name_dict[m].append(f)

    dup_list = [name_dict[m] for m in name_dict if len(name_dict[m]) > 1]

    for dup in dup_list:
        if os.path.getsize(dup[0]) < MIN_SIZE:
            trash[dup[0]]
        for f in dup[1:]:
            trash(f)

    return dup_list


def main():
    for root, dirs, files in os.walk(dir):
        if output_dir in root:
            print '[info]: skip output dir ', output_dir
            continue
        for file in files:
            if file.endswith('.jpg'):
                prefix = root.split("-")[0]  # take the part before '-'
                fullname = os.path.join(root, file)
                outfilename = output_dir + os.sep + prefix + file
                outfilename = os.path.normpath(outfilename)
                shutil.copy(fullname, outfilename)
                print '[info]: copy', fullname, ", outfilename:", outfilename
            else:
                print '[warning]: skip', file


if __name__ == '__main__':
    prepare()
    main()
    filter()
    uniq_file()
