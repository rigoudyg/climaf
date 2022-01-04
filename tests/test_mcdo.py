#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test the mcdo.py module.
"""
from __future__ import print_function, division, unicode_literals, absolute_import


import os
import unittest

from tests.tools_for_tests import remove_dir_and_content, compare_netcdf_files, compare_text_files

from env.environment import *
from climaf.cache import setNewUniqueCache
from climaf import __path__ as rootpath

from scripts.mcdo import main as mcdo_main


class McdoTests(unittest.TestCase):
    # TODO: Tests specific files and long series (more than 10 files at once)

    def setUp(self):
        self.ref_dir = os.path.sep.join([rootpath[0], "..", "tests", "reference_data", "test_mcdo"])
        self.input_file_1 = os.path.sep.join([rootpath[0], "..", "examples", "data", "AMIPV6ALB2G", "A",
                                              "AMIPV6ALB2GPL1980.nc"])
        self.input_file_2 = os.path.sep.join([rootpath[0], "..", "tests", "test_data",
                                              "tas_Amon_CNRM-CM5_historical_r1i1p1_1850.nc"])
        self.input_file_3 = os.path.sep.join([rootpath[0], "..", "tests", "test_data",
                                              "tas_Amon_CNRM-CM5_historical_r1i1p1_1851.nc"])
        self.input_file_4 = os.path.sep.join([rootpath[0], "..", "tests", "test_data",
                                              "tas_Amon_CNRM-CM5_historical_r1i1p1_1852.nc"])

    def test_1(self):
        log = "test_1.txt"
        test_log = os.path.sep.join([tmp_directory, log])
        ref_log = os.path.sep.join([self.ref_dir, log])
        output_file = "test_1.nc"
        test_output_file = os.path.sep.join([tmp_directory, output_file])
        ref_output_file = os.path.sep.join([self.ref_dir, output_file])
        mcdo_main(input_files=[self.input_file_1], output_file=test_output_file,
                  variable="ta", alias=["taC", "ta", "1", "-273.15"], region=None, units=None, vm=None,
                  period=None, operator="sellevel,85000", apply_operator_after_merge=False, test=test_log,
                  running_climaf_tests=True)
        compare_text_files(test_log, ref_log, _CLIMAF_PATH_=rootpath[0], _TEST_PATH_=tmp_directory)
        compare_netcdf_files(test_output_file, ref_output_file)

    def test_2(self):
        log = "test_2.txt"
        test_log = os.path.sep.join([tmp_directory, log])
        ref_log = os.path.sep.join([self.ref_dir, log])
        output_file = "test_2.nc"
        test_output_file = os.path.sep.join([tmp_directory, output_file])
        ref_output_file = os.path.sep.join([self.ref_dir, output_file])
        mcdo_main(input_files=[self.input_file_2, self.input_file_3, self.input_file_4], output_file=test_output_file,
                  variable="tas", alias=None, region=["-20", "60", "10", "350"], units=None, vm=None,
                  period="1850-06-01T00:00:00,1852-04-03T00:00:00", operator="ymonavg", apply_operator_after_merge=True,
                  test=test_log, running_climaf_tests=True)
        compare_text_files(test_log, ref_log, _CLIMAF_PATH_=rootpath[0], _TEST_PATH_=tmp_directory)
        compare_netcdf_files(test_output_file, ref_output_file)


if __name__ == '__main__':
    # Jump into the test directory
    tmp_directory = "/".join([os.environ["HOME"], "tmp", "tests", "test_mcdo"])
    remove_dir_and_content(tmp_directory)
    if not os.path.isdir(tmp_directory):
        os.makedirs(tmp_directory)
    os.chdir(tmp_directory)
    setNewUniqueCache(tmp_directory)
    unittest.main(exit=False)
    remove_dir_and_content(tmp_directory)
