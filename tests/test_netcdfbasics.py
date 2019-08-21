#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Test the netcdfbasics module.
"""

import os
import unittest

from tests.tools_for_tests import remove_dir_and_content

from climaf.netcdfbasics import varOfFile, varsOfFile, fileHasVar, fileHasDim, dimsOfFile, \
    model_id, timeLimits
from climaf.period import init_period
from climaf.cache import setNewUniqueCache
from climaf import __path__ as rootpath


class VarsOfFileTests(unittest.TestCase):

    def test_vars(self):
        my_file = "/".join([rootpath[0], "..", "examples", "data", "NPv3.1ada_SE_1982_1991_1M_ua_pres.nc"])
        self.assertEqual(varsOfFile(my_file), ["ua", "pres"])
        my_file = "/".join(
            [rootpath[0], "..", "examples", "data", "tas_Amon_CNRM-CM5_historical_r1i1p1_185001-185212.nc"])
        self.assertEqual(varsOfFile(my_file), ["tas", ])


class VarOfFileTests(unittest.TestCase):

    def test_var(self):
        my_file = "/".join([rootpath[0], "..", "examples", "data", "NPv3.1ada_SE_1982_1991_1M_ua_pres.nc"])
        self.assertIsNone(varOfFile(my_file))
        my_file = "/".join(
            [rootpath[0], "..", "examples", "data", "tas_Amon_CNRM-CM5_historical_r1i1p1_185001-185212.nc"])
        self.assertEqual(varOfFile(my_file), "tas")


class FileHasVarTests(unittest.TestCase):

    def test_var(self):
        my_file = "/".join([rootpath[0], "..", "examples", "data", "NPv3.1ada_SE_1982_1991_1M_ua_pres.nc"])
        self.assertTrue(fileHasVar(my_file, "ua"))
        self.assertFalse(fileHasVar(my_file, "tas"))
        my_file = "/".join(
            [rootpath[0], "..", "examples", "data", "tas_Amon_CNRM-CM5_historical_r1i1p1_185001-185212.nc"])
        self.assertFalse(fileHasVar(my_file, "ua"))
        self.assertTrue(fileHasVar(my_file, "tas"))


class DimsOfFileTests(unittest.TestCase):

    def test_dims(self):
        my_file = "/".join([rootpath[0], "..", "examples", "data", "NPv3.1ada_SE_1982_1991_1M_ua_pres.nc"])
        self.assertEqual(dimsOfFile(my_file), ["lat", "presnivs", "time_counter", "lon"])
        my_file = "/".join(
            [rootpath[0], "..", "examples", "data", "tas_Amon_CNRM-CM5_historical_r1i1p1_185001-185212.nc"])
        self.assertEqual(dimsOfFile(my_file), ["lat", "nb2", "lon", "time"])


class FileHasDimTests(unittest.TestCase):

    def test_dim(self):
        my_file = "/".join([rootpath[0], "..", "examples", "data", "NPv3.1ada_SE_1982_1991_1M_ua_pres.nc"])
        self.assertTrue(fileHasDim(my_file, "lat"))
        self.assertFalse(fileHasDim(my_file, "nav_lon"))
        my_file = "/".join(
            [rootpath[0], "..", "examples", "data", "tas_Amon_CNRM-CM5_historical_r1i1p1_185001-185212.nc"])
        self.assertFalse(fileHasDim(my_file, "time_bounds"))
        self.assertTrue(fileHasDim(my_file, "lon"))


class ModelIdTests(unittest.TestCase):

    def test_model_id(self):
        my_file = "/".join([rootpath[0], "..", "examples", "data", "NPv3.1ada_SE_1982_1991_1M_ua_pres.nc"])
        self.assertEqual(model_id(my_file), "no_model")
        my_file = "/".join(
            [rootpath[0], "..", "examples", "data", "tas_Amon_CNRM-CM5_historical_r1i1p1_185001-185212.nc"])
        self.assertEqual(model_id(my_file), "CNRM-CM5")


class TimeLimitesTests(unittest.TestCase):

    def test_time_limites(self):
        my_file = "/".join([rootpath[0], "..", "examples", "data", "NPv3.1ada_SE_1982_1991_1M_ua_pres.nc"])
        self.assertIsNone(timeLimits(my_file))
        my_file = "/".join(
            [rootpath[0], "..", "examples", "data", "tas_Amon_CNRM-CM5_historical_r1i1p1_185001-185212.nc"])
        self.assertEqual(repr(timeLimits(my_file)), repr(init_period("1850-1852")))


if __name__ == '__main__':
    # Jump into the test directory
    tmp_directory = "/".join([os.environ["HOME"], "tmp", "tests", "test_netcdfbasics"])
    remove_dir_and_content(tmp_directory)
    if not os.path.isdir(tmp_directory):
        os.makedirs(tmp_directory)
    os.chdir(tmp_directory)
    setNewUniqueCache(tmp_directory)
    unittest.main()
    remove_dir_and_content(tmp_directory)
