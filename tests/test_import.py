#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test the import of all modules.
"""

import os
import unittest
import importlib

from tests.tools_for_tests import remove_dir_and_content


testmodules = [
    "climaf",
    "climaf.api",
    "climaf.anynetcdf",
    "climaf.cache",
    "climaf.classes",
    "climaf.clogging",
    "climaf.cmacro",
    "climaf.dataloc",
    "climaf.driver",
    "climaf.easyCMIP_functions",
    "climaf.functions",
    "climaf.html",
    "climaf.netcdfbasics",
    "climaf.operators",
    "climaf.period",
    "climaf.site_settings",
    "climaf.standard_operators"
]


class ImportTests(unittest.TestCase):

    def test_imports(self):
        for modname in testmodules:
            self.assertTrue(importlib.import_module(modname))


if __name__ == '__main__':
    # Jump into the test directory
    tmp_directory = "/".join([os.environ["HOME"], "tmp", "tests", "test_import"])
    remove_dir_and_content(tmp_directory)
    if not os.path.isdir(tmp_directory):
        os.makedirs(tmp_directory)
    os.chdir(tmp_directory)
    unittest.main()
    remove_dir_and_content(tmp_directory)
