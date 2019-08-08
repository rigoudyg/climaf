#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Test the cache module.
"""

import os
import shutil
import unittest

from climaf import __path__ as rootpath

from climaf.cache import setNewUniqueCache, generateUniqueFileName, generateUniqueFileName_unsafe, \
    generateUniqueFileName_safe, stringToPath, searchFile, register, getCRS, rename, hasMatchingObject, \
    hasIncludingObject, hasBeginObject, hasExactObject, complement, cdrop, cprotect, csync, cload, cload_for_project, \
    craz, cdump, list_cache, clist, cls, crm, cdu, cwc, rebuild, Climaf_Cache_Error


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

    def test_generateUniqueFileName_unsafe(self):
        my_crs="ds('CMIP6%%tas%0185-1900%global%/cnrm/cmip%CNRM-CM6-1%CNRM-CERFACS%CMIP%Amon%piControl%r1i1p1f2%gr%latest')"
        self.assertEqual(generateUniqueFileName_unsafe(my_crs), '/home/rigoudyg/tmp/tests/test_cache/7f19f/c8b62/2fd64/8549c/fe53a/9a578/75a0b/86e35/ae4ae/11821/2c625/1.nc')
        self.assertTrue(os.path.exists('/home/rigoudyg/tmp/tests/test_cache/7f19f/c8b62/2fd64/8549c/fe53a/9a578/75a0b/86e35/ae4ae/11821/2c625/'))
        self.assertEqual(generateUniqueFileName_unsafe(my_crs, format=None), "")

    def test_generateUniqueFileName_safe(self):
        my_crs="ds('CMIP6%%tas%0185-1900%global%/cnrm/cmip%CNRM-CM6-1%CNRM-CERFACS%CMIP%Amon%piControl%r1i1p1f2%gr%latest')"
        self.assertEqual(generateUniqueFileName_safe(my_crs), '/home/rigoudyg/tmp/tests/test_cache/7f19f/c8b62/2fd64/8549c/fe53a/9a578/75a0b/86e35/ae4ae/11821/2c625/1.nc')
        self.assertTrue(os.path.exists('/home/rigoudyg/tmp/tests/test_cache/7f19f/c8b62/2fd64/8549c/fe53a/9a578/75a0b/86e35/ae4ae/11821/2c625/'))
        self.assertEqual(generateUniqueFileName_safe(my_crs, format=None), "")

        def my_operator(expr):
            return expr[-5:-1]

        def my_other_operator(expr):
            return None

        self.assertEqual(generateUniqueFileName_safe(my_crs, operator=my_operator), "/home/rigoudyg/tmp/tests/test_cache/est'/7f19f/c8b62/2fd64/8549c/fe53a/9a578/75a0b/86e35/ae4ae/11821/2c625/1.nc")
        self.assertEqual(generateUniqueFileName_safe(my_crs, operator=my_other_operator), "/home/rigoudyg/tmp/tests/test_cache/7f19f/c8b62/2fd64/8549c/fe53a/9a578/75a0b/86e35/ae4ae/11821/2c625/1.nc")
        shutil.copy("/".join([rootpath[0], "..", "examples", "data", "NPv3.1ada_SE_1982_1991_1M_ua_pres.nc"]), '/home/rigoudyg/tmp/tests/test_cache/7f19f/c8b62/2fd64/8549c/fe53a/9a578/75a0b/86e35/ae4ae/11821/2c625/1.nc')
        with self.assertRaises(Climaf_Cache_Error):
            generateUniqueFileName_safe(my_crs)
        # TODO: Go on to test the usecases of the generateUniqueFileName_safe function


class StringToPathTests(unittest.TestCase):

    def test_stringToPath(self):
        name = "7f19fc8b622fd648549cfe53a9a57875a0b86e35ae4ae118212c6251"
        lenngth = 5
        self.assertEqual(stringToPath(name, lenngth), "7f19f/c8b62/2fd64/8549c/fe53a/9a578/75a0b/86e35/ae4ae/11821/2c625/1")


class SearchFileTests(unittest.TestCase):

    def test_searchFile(self):
        my_path_1 = "7f19f/c8b62/2fd64/8549c/fe53a/9a578/75a0b/86e35/ae4ae/11821/2c625/1.nc"
        my_path_2 = "7f19f/c8b62/2fd64/8549c/fe53a/9a578/75a0b/86e35/ae4ae/11821/2c625/2.nc"
        my_path_3 = "7f19f/c8b62/2fd64/8549c/fe53a/9a578/75a0b/86e35/ae4ae/11821/2c625/3.nc"
        os.symlink(my_path_2, my_path_3)
        self.assertEqual(searchFile(my_path_1), "/".join([tmp_directory, my_path_1]))
        self.assertEqual(searchFile(my_path_3), None)


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


class HasMatchingObjectTests(unittest.TestCase):

    @unittest.skipUnless(False, "The test is not written")
    def test_hasMatchingObject(self):
        # TODO: Implement the tests for this function
        pass


class HasIncludingObjectTests(unittest.TestCase):

    @unittest.skipUnless(False, "The test is not written")
    def test_hasIncludingObject(self):
        # TODO: Implement the tests for this function
        pass


class HasBeginObjectTests(unittest.TestCase):

    @unittest.skipUnless(False, "The test is not written")
    def test_hasbeginObject(self):
        # TODO: Implement the tests for this function
        pass


class HasExactObjectTests(unittest.TestCase):

    @unittest.skipUnless(False, "The test is not written")
    def test_hasExactObject(self):
        # TODO: Implement the tests for this function
        pass


class ComplementTests(unittest.TestCase):

    @unittest.skipUnless(False, "The test is not written")
    def test_complement(self):
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


class CloadTests(unittest.TestCase):

    @unittest.skipUnless(False, "The test is not written")
    def test_cload(self):
        # TODO: Implement the tests for this function
        pass


class CloadForProjectTests(unittest.TestCase):

    @unittest.skipUnless(False, "The test is not written")
    def test_cload_for_project(self):
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


class ListCacheTests(unittest.TestCase):

    @unittest.skipUnless(False, "The test is not written")
    def test_list_cache(self):
        # TODO: Implement the tests for this function
        pass


class ClistTests(unittest.TestCase):

    @unittest.skipUnless(False, "The test is not written")
    def test_clist(self):
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


class RebuildTests(unittest.TestCase):

    @unittest.skipUnless(False, "The test is not written")
    def test_rebuild(self):
        # TODO: Implement the tests for this function
        pass


if __name__ == '__main__':
    # Jump into the test directory
    tmp_directory = "/".join([os.environ["HOME"], "tmp", "tests", "test_cache"])
    if not os.path.isdir(tmp_directory):
        os.makedirs(tmp_directory)
    setNewUniqueCache(tmp_directory)
    os.chdir(tmp_directory)
    unittest.main()
