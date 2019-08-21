#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Tools to deal with tests.
"""

from __future__ import unicode_literals, absolute_import, print_function, division

import os


def remove_dir_and_content(dirname):
    if os.path.isdir(dirname):
        # Deal with files
        listfiles = list()
        listdirs = list()
        for (d, subdirs, files) in os.walk(dirname):
            for name in files:
                listfiles.append(os.path.sep.join([d, name]))
            for subd in subdirs:
                listdirs.append(os.path.sep.join([d, subd]))
        for f in listfiles:
            os.remove(f)
        # Deal with subdirectories
        for d in sorted(listdirs, reverse=True):
            os.rmdir(d)
