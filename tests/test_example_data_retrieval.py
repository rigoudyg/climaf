#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test based on examples/index_html.py
"""
from __future__ import print_function, division, unicode_literals, absolute_import


import unittest

from tests.tools_for_tests import remove_dir_and_content, compare_picture_files, skipUnless_CNRM_Lustre
from env.environment import *

from climaf.cache import setNewUniqueCache, craz
from climaf import __path__ as cpath
from climaf.api import *
from climaf.period import init_period

if not isinstance(cpath, list):
    cpath = cpath.split(os.sep)


class DataRetrieval_1(unittest.TestCase):

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

    @skipUnless_CNRM_Lustre()
    def test_retrieval_subperiod_1(self):
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

    @skipUnless_CNRM_Lustre()
    def test_retrieval_cmip6_data(self):
        g = ds(project='CMIP6', period='2000-2001', variable='tos', table='Omon', grid='gn', model='CNRM-CM6-1',
               experiment='hist-nat', realization='r1i1p1f2')
        climaf_ds = ccdo(g, operator='fldmean')
        print(cfile(climaf_ds))

        g = ds(project='CMIP6', period='2000-2001', variable='tos', table='Omon', grid='gn', model='CNRM-CM6-1',
               experiment='omip2', realization='r1i1p1f2')
        climaf_ds = ccdo(g, operator='fldmean')
        print(cfile(climaf_ds))

    def tearDown(self):
        craz()


class DataRetrieval_2(unittest.TestCase):

    def setUp(self):
        craz()
        self.reference_directory = os.sep.join(cpath + ["..", "tests", "reference_data", "test_data_retrieval"])
        self.climaf_dir = os.sep.join(cpath[:-1])
        cproject("test_data", ('frequency', 'monthly'), "model", "table", "realization", separator="%")
        dataloc(project="test_data", organization="generic",
                url=[os.sep.join(cpath + ["..", "tests", "test_data",
                                          "${variable}_${table}_${model}_${simulation}_${realization}_${period}.nc"])])

    def test_retrieval_subperiod_2(self):
        derive("*", "tas2", "time_average", "tas")
        derive('*', 'tas3', 'minus', 'tas', 'tas2')
        g = ds(project='test_data', period='1850', variable='tas3', model='CNRM-CM5', simulation="historical",
               realization="r1i1p1", table="Amon")
        climaf_ds = ccdo(ccdo(g, operator='fldmean'), operator='yearavg')
        self.assertEqual(str(climaf_ds),
                         "ccdo(ccdo(ds('test_data%historical%tas3%1850%global%monthly%CNRM-CM5%Amon%r1i1p1'),"
                         "operator='fldmean'),operator='yearavg')")
        cMA(climaf_ds)

        g = ds(project='test_data', period='185004-185006', variable='tas3', model='CNRM-CM5', simulation="historical",
               realization="r1i1p1", table="Amon")
        climaf_ds = ccdo(ccdo(g, operator='fldmean'), operator='yearavg')
        self.assertEqual(str(climaf_ds),
                         "ccdo(ccdo(ds('test_data%historical%tas3%185004-185006%global%monthly%CNRM-CM5%Amon%r1i1p1'),"
                         "operator='fldmean'),operator='yearavg')")
        cMA(climaf_ds)

    def test_retrieval_subperiod_several_files(self):
        f = ds(project='test_data', period='185004-185104', variable='tas3', model='CNRM-CM5', simulation="historical",
               realization="r1i1p1", table="Amon")
        self.assertEqual(str(f), "ds('test_data%historical%tas3%185004-185104%global%monthly%CNRM-CM5%Amon%r1i1p1')")
        cfile(f)

    def tearDown(self):
        craz()


if __name__ == '__main__':
    # Jump into the test directory
    tmp_directory = "/".join([os.environ["HOME"], "tmp", "tests", "test_data_retrieval"])
    remove_dir_and_content(tmp_directory)
    if not os.path.isdir(tmp_directory):
        os.makedirs(tmp_directory)
    setNewUniqueCache(tmp_directory)
    os.chdir(tmp_directory)
    unittest.main()
