#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test the cache module.
"""

from __future__ import print_function, division, unicode_literals, absolute_import


import os
import shutil
import unittest

from tests.tools_for_tests import remove_dir_and_content

from climaf import __path__ as rootpath
from climaf.cmacro import crewrite
from env.environment import *

from climaf.cache import setNewUniqueCache, generateUniqueFileName, hash_to_path,\
    register, getCRS, rename,  hasExactObject, \
    cdrop, cprotect, csync, craz, cdump, clist, cls, crm, cdu, cwc, \
    Climaf_Cache_Error


class SetNewUniqueCacheTests(unittest.TestCase):

    def test_setNewUniqueCache(self):
        # TODO: Change this test to check that new files put in cache will be put into the new one and that
        #       call to craz works
        new_tmp_directory = tmp_directory + "/tmp"
        setNewUniqueCache(new_tmp_directory)
        from climaf.cache import cachedirs, currentCache, cacheIndexFileName
        self.assertEqual(cachedirs, [new_tmp_directory])
        self.assertEqual(currentCache, new_tmp_directory)
        self.assertEqual(cacheIndexFileName, new_tmp_directory + "/index")
        setNewUniqueCache(tmp_directory, raz=False)
        from climaf.cache import cachedirs, currentCache, cacheIndexFileName
        self.assertEqual(cachedirs, [tmp_directory])
        self.assertEqual(currentCache, tmp_directory)
        self.assertEqual(cacheIndexFileName, tmp_directory + "/index")


class GenerateUniqueFileNameTests(unittest.TestCase):

    def test_generateUniqueFileName(self):
        my_crs = "ds('CMIP6%%tas%0185-1900%global%/cnrm/cmip%CNRM-CM6-1%CNRM-CERFACS%CMIP%Amon%piControl%r1i1p1f2%gr%" \
                 "latest')"
        my_basedir = os.path.sep.join([tmp_directory,
                                       '7f'])
        self.assertEqual(generateUniqueFileName(my_crs),
                         os.path.sep.join([my_basedir, '19fc8b622fd648549cfe53a9a57875a0b86e35ae4ae118212c6251.nc']))
        self.assertTrue(os.path.exists(my_basedir))
        self.assertEqual(generateUniqueFileName(my_crs, format=None), "")

        shutil.copy(os.sep.join([rootpath[0], "..", "examples", "data", "NPv3.1ada_SE_1982_1991_1M_ua_pres.nc"]),
                    os.sep.join(['7f/19fc8b622fd648549cfe53a9a57875a0b86e35ae4ae118212c6251.nc']))
        # TODO: Go on to test the usecases of the generateUniqueFileName function


class RegisterTests(unittest.TestCase):

    @unittest.skipUnless(False, "The test is not written")
    def test_register(self):
        # TODO: Implement the tests for this function
        pass


class GetCRSTests(unittest.TestCase):

    @unittest.skipUnless(False, "The test is not written")
    def test_getCRS(self):
        # TODO: Implement the tests for this function
        pass


class RenameTests(unittest.TestCase):

    @unittest.skipUnless(False, "The test is not written")
    def test_rename(self):
        # TODO: Implement the tests for this function
        pass


class HasExactObjectTests(unittest.TestCase):

    @unittest.skipUnless(False, "The test is not written")
    def test_hasExactObject(self):
        # TODO: Implement the tests for this function
        pass


class CdropTests(unittest.TestCase):

    @unittest.skipUnless(False, "The test is not written")
    def test_cdrop(self):
        # TODO: Implement the tests for this function
        pass


class CprotectTests(unittest.TestCase):

    @unittest.skipUnless(False, "The test is not written")
    def test_cprotect(self):
        # TODO: Implement the tests for this function
        pass


class CsyncTests(unittest.TestCase):

    @unittest.skipUnless(False, "The test is not written")
    def test_csync(self):
        # TODO: Implement the tests for this function
        pass


class CrazTests(unittest.TestCase):

    @unittest.skipUnless(False, "The test is not written")
    def test_craz(self):
        # TODO: Implement the tests for this function
        pass


class CdumpTests(unittest.TestCase):

    @unittest.skipUnless(False, "The test is not written")
    def test_cdump(self):
        # TODO: Implement the tests for this function
        pass



class ClsTests(unittest.TestCase):

    @unittest.skipUnless(False, "The test is not written")
    def test_cls(self):
        # TODO: Implement the tests for this function
        pass


class CrmTests(unittest.TestCase):

    @unittest.skipUnless(False, "The test is not written")
    def test_crm(self):
        # TODO: Implement the tests for this function
        pass


class CduTests(unittest.TestCase):

    @unittest.skipUnless(False, "The test is not written")
    def test_cdu(self):
        # TODO: Implement the tests for this function
        pass


class CwcTests(unittest.TestCase):

    @unittest.skipUnless(False, "The test is not written")
    def test_cwc(self):
        # TODO: Implement the tests for this function
        pass


if __name__ == '__main__':
    # Jump into the test directory
    tmp_directory = "/".join([os.environ["HOME"], "tmp", "tests", "test_cache"])
    remove_dir_and_content(tmp_directory)
    if not os.path.isdir(tmp_directory):
        os.makedirs(tmp_directory)
    setNewUniqueCache(tmp_directory)
    os.chdir(tmp_directory)
    unittest.main()
    remove_dir_and_content(tmp_directory)
