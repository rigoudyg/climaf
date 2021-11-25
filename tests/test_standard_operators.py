#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test the standard operators module.
"""
from __future__ import print_function, division, unicode_literals, absolute_import


import os
import unittest

from tests.tools_for_tests import remove_dir_and_content
from env.environment import *

from climaf.cache import setNewUniqueCache
from climaf.standard_operators import load_standard_operators


class StandardOperatorsTests(unittest.TestCase):

    def test_load_standard_operator(self):
        load_standard_operators()
        import sys
        list_of_objects_in_main = sys.modules["__main__"].__dict__
        for script in cscripts:
            self.assertIn(script, globals())
            self.assertIn(script, list_of_objects_in_main)


if __name__ == '__main__':
    # Jump into the test directory
    tmp_directory = "/".join([os.environ["HOME"], "tmp", "tests", "test_standard_operators"])
    remove_dir_and_content(tmp_directory)
    if not os.path.isdir(tmp_directory):
        os.makedirs(tmp_directory)
    setNewUniqueCache(tmp_directory)
    os.chdir(tmp_directory)
    unittest.main()
    remove_dir_and_content(tmp_directory)
