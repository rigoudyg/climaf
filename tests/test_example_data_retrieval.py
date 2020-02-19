#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Test based on examples/index_html.py
"""

import os
import unittest

from tests.tools_for_tests import remove_dir_and_content, compare_picture_files, skipUnless_CNRM_Lustre

from climaf.cache import setNewUniqueCache
from climaf import __path__ as cpath
from climaf.api import *
from climaf.period import init_period

if not isinstance(cpath, list):
    cpath = cpath.split(os.sep)


class DataRetrieval(unittest.TestCase):

    def setUp(self):
        craz()
        self.reference_directory = os.sep.join(cpath + ["..", "tests", "reference_data", "test_data_retrieval"])
        self.climaf_dir = os.sep.join(cpath[:-1])

    def test_retrieval_period(self):
        ta = ds(project='example', simulation="AMIPV6ALB2G", variable="ta", period="*")
        choices = ta.explore("choices")
        self.assertDictEqual(choices, {'period': [init_period("1980")]})
        self.assertEqual(ta.baseFiles(),
                         os.sep.join([self.climaf_dir, "examples/data/AMIPV6ALB2G/A/AMIPV6ALB2GPL1980.nc"]))
        ta_last = ds(project='example', simulation="AMIPV6ALB2G", variable="ta", period="last_1Y")
        choices_last = ta_last.explore("choices")
        self.assertDictEqual(choices_last, dict())
        self.assertEqual(ta_last.baseFiles(),
                         os.sep.join([self.climaf_dir, "examples/data/AMIPV6ALB2G/A/AMIPV6ALB2GPL1980.nc"]))

    def test_retrieval_subperiod(self):
        derive('*', 'rls', 'minus', 'rlds', 'rlus')
        g = ds(project='CMIP6', period='1850-1854', variable='rls', model='CNRM-CM6-1')
        climaf_ds = ccdo(ccdo(g, operator='fldmean'), operator='yearavg')
        self.assertEqual(str(climaf_ds),
                         "ccdo(ccdo(ds('CMIP6%%rls%1850-1854%global%/cnrm/cmip%CNRM-CM6-1%*%*%*%historical%r1i1p1f*%g*%"
                         "latest'),operator='fldmean'),operator='yearavg')")
        cMA(climaf_ds)

        g = ds(project='CMIP6', period='1852-1854', variable='rls', model='CNRM-CM6-1')
        climaf_ds = ccdo(ccdo(g, operator='fldmean'), operator='yearavg')
        self.assertEqual(str(climaf_ds),
                         "ccdo(ccdo(ds('CMIP6%%rls%1852-1854%global%/cnrm/cmip%CNRM-CM6-1%*%*%*%historical%r1i1p1f*%g*%"
                         "latest'),operator='fldmean'),operator='yearavg')")
        cMA(climaf_ds)


if __name__ == '__main__':
    # Jump into the test directory
    tmp_directory = "/".join([os.environ["HOME"], "tmp", "tests", "test_data_retrieval"])
    remove_dir_and_content(tmp_directory)
    if not os.path.isdir(tmp_directory):
        os.makedirs(tmp_directory)
    setNewUniqueCache(tmp_directory)
    os.chdir(tmp_directory)
    unittest.main()
    remove_dir_and_content(tmp_directory)
