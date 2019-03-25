#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Testing Pre-requisites for CliMAF

Run it as : python -m unittest -v test_req

S.Senesi - jan 2015
"""

from __future__ import print_function, division, unicode_literals, absolute_import

import unittest
import os


class A_externals(unittest.TestCase):
    def setUp(self):
        pass

    def test_1_convert(self):
        bin = "convert"
        self.assertEqual(os.system("type %s > /dev/null 2>&1" % bin), 0, "Cannot execute %s" % bin)

    def test_2_identify(self):
        bin = "identify"
        self.assertEqual(os.system("type %s > /dev/null 2>&1" % bin), 0, "Cannot execute %s" % bin)

    def test_3_ncatted(self):
        bin = "ncatted"
        self.assertEqual(os.system("type %s > /dev/null 2>&1" % bin), 0, "Cannot execute %s" % bin)

    def test_4_ncdump(self):
        bin = "ncdump"
        self.assertEqual(os.system("type %s > /dev/null 2>&1" % bin), 0, "Cannot execute %s" % bin)

    def test_5_ncwa(self):
        bin = "convert"
        self.assertEqual(os.system("type %s > /dev/null 2>&1" % bin), 0, "Cannot execute %s" % bin)

    def test_6_ncrcat(self):
        bin = "ncrcat"
        self.assertEqual(os.system("type %s > /dev/null 2>&1" % bin), 0, "Cannot execute %s" % bin)

    def test_7_cdo(self):
        bin = "cdo"
        self.assertEqual(os.system("type %s > /dev/null 2>&1" % bin), 0, "Cannot execute %s" % bin)

    @unittest.expectedFailure
    def test_9_cdo(self):
        bin = "ncview"
        self.assertEqual(os.system("type %s > /dev/null 2>&1" % bin), 0, "You may have troubles without %s" % bin)

    @unittest.expectedFailure
    def test_ncl(self):
        bin = "ncl"
        self.assertEqual(os.system("type %s > /dev/null 2>&1" % bin), 0, "You may have troubles without %s" % bin)

    def tearDown(self):
        pass


if __name__ == '__main__':
    print("Testing CliMAF pre-requisites")
    unittest.main()
