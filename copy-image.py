#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Hua Liang[Stupid ET] <et@everet.org>
#
import os
import shutil


dir = '.'
output_dir = 'output'
trash = '/tmp/image-trash'
MIN_SIZE = 30000                # 30KB


def prepare():
    try:
        os.mkdir(output_dir)
    except:
        pass


def filesize_filter(filename):
    try: os.mkdir(trash)
    except: pass
    size = os.path.getsize(filename)
    if size < MIN_SIZE:
        try:
            shutil.move(filename, trash)
        except:
            pass


def filter():
    for f in os.listdir(output_dir):
        filesize_filter(os.path.normpath(output_dir + os.sep + f))


def main():
    for root, dirs, files in os.walk(dir):
        for file in files:
            if file.endswith('.jpg'):
                prefix = root[:root.find('-')]  # take the part before '-'
                fullname = os.path.join(root, file)
                outfilename = output_dir + os.sep + prefix + file
                outfilename = os.path.normpath(outfilename)
                shutil.copy(fullname, outfilename)
                print '[info]: copy', fullname
            else:
                print '[warning]: skip', file


if __name__ == '__main__':
    prepare()
    main()
    filter()
