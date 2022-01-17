#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test the cache module.
"""

from __future__ import print_function, division, unicode_literals, absolute_import


import shutil
import unittest

from tests.tools_for_tests import remove_dir_and_content

import env
from env.environment import *
from climaf import __path__ as rootpath
from climaf.cmacro import crewrite

from climaf.cache import setNewUniqueCache, generateUniqueFileName, hash_to_path, alternate_filename, stringToPath, \
    searchFile, register, getCRS, rename, hasMatchingObject, hasIncludingObject, hasBeginObject, hasExactObject, \
    complement, cdrop, cprotect, csync, cload, cload_for_project, craz, cdump, list_cache, clist, cls, crm, cdu, cwc, \
    rebuild, ccost, Climaf_Cache_Error
from climaf.driver import cfile


class SetNewUniqueCacheTests(unittest.TestCase):

    def test_setNewUniqueCache(self):
        # TODO: Change this test to check that new files put in cache will be put into the new one and that
        #       call to craz works
        new_tmp_directory = tmp_directory + "/tmp"
        setNewUniqueCache(new_tmp_directory)
        self.assertEqual(env.environment.cachedirs, [new_tmp_directory])
        self.assertEqual(env.environment.currentCache, new_tmp_directory)
        self.assertEqual(env.environment.cacheIndexFileName, new_tmp_directory + "/index")
        setNewUniqueCache(tmp_directory, raz=False)
        self.assertEqual(env.environment.cachedirs, [tmp_directory])
        self.assertEqual(env.environment.currentCache, tmp_directory)
        self.assertEqual(env.environment.cacheIndexFileName, tmp_directory + "/index")

    def tearDown(self):
        craz()


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

    def tearDown(self):
        craz()


class StringToPathTests(unittest.TestCase):

    def test_stringToPath(self):
        name = "7f19fc8b622fd648549cfe53a9a57875a0b86e35ae4ae118212c6251"
        length = 5
        self.assertEqual(stringToPath(name, length),
                         "7f19f/c8b62/2fd64/8549c/fe53a/9a578/75a0b/86e35/ae4ae/11821/2c625/1")

    def tearDown(self):
        craz()


class SearchFileTests(unittest.TestCase):

    def test_searchFile(self):
        my_path_1 = "7f/19fc8b622fd648549cfe53a9a57875a0b86e35ae4ae118212c6251.nc"
        my_path_2 = "7f/19fc8b622fd648549cfe53a9a57875a0b86e35ae4ae118212c6252.nc"
        my_path_3 = "7f/19fc8b622fd648549cfe53a9a57875a0b86e35ae4ae118212c6253.nc"
        os.symlink(my_path_2, my_path_3)
        self.assertEqual(searchFile(my_path_1), "/".join([tmp_directory, my_path_1]))
        self.assertEqual(searchFile(my_path_3), None)

    def tearDown(self):
        craz()


class RegisterTests(unittest.TestCase):

    @unittest.skipUnless(False, "The test is not written")
    def test_register(self):
        # TODO: Implement the tests for this function
        pass

    def tearDown(self):
        craz()


class GetCRSTests(unittest.TestCase):

    @unittest.skipUnless(False, "The test is not written")
    def test_getCRS(self):
        # TODO: Implement the tests for this function
        pass

    def tearDown(self):
        craz()


class RenameTests(unittest.TestCase):

    @unittest.skipUnless(False, "The test is not written")
    def test_rename(self):
        # TODO: Implement the tests for this function
        pass

    def tearDown(self):
        craz()


class HasMatchingObjectTests(unittest.TestCase):

    @unittest.skipUnless(False, "The test is not written")
    def test_hasMatchingObject(self):
        # TODO: Implement the tests for this function
        pass

    def tearDown(self):
        craz()


class HasIncludingObjectTests(unittest.TestCase):

    @unittest.skipUnless(False, "The test is not written")
    def test_hasIncludingObject(self):
        # TODO: Implement the tests for this function
        pass

    def tearDown(self):
        craz()


class HasBeginObjectTests(unittest.TestCase):

    @unittest.skipUnless(False, "The test is not written")
    def test_hasbeginObject(self):
        # TODO: Implement the tests for this function
        pass

    def tearDown(self):
        craz()


class HasExactObjectTests(unittest.TestCase):

    @unittest.skipUnless(False, "The test is not written")
    def test_hasExactObject(self):
        # TODO: Implement the tests for this function
        pass

    def tearDown(self):
        craz()


class ComplementTests(unittest.TestCase):

    @unittest.skipUnless(False, "The test is not written")
    def test_complement(self):
        # TODO: Implement the tests for this function
        pass

    def tearDown(self):
        craz()


class CdropTests(unittest.TestCase):

    @unittest.skipUnless(False, "The test is not written")
    def test_cdrop(self):
        # TODO: Implement the tests for this function
        pass

    def tearDown(self):
        craz()


class CprotectTests(unittest.TestCase):

    @unittest.skipUnless(False, "The test is not written")
    def test_cprotect(self):
        # TODO: Implement the tests for this function
        pass

    def tearDown(self):
        craz()


class CsyncTests(unittest.TestCase):

    @unittest.skipUnless(False, "The test is not written")
    def test_csync(self):
        # TODO: Implement the tests for this function
        pass

    def tearDown(self):
        craz()


class CloadTests(unittest.TestCase):

    @unittest.skipUnless(False, "The test is not written")
    def test_cload(self):
        # TODO: Implement the tests for this function
        pass

    def tearDown(self):
        craz()


class CloadForProjectTests(unittest.TestCase):

    @unittest.skipUnless(False, "The test is not written")
    def test_cload_for_project(self):
        # TODO: Implement the tests for this function
        pass

    def tearDown(self):
        craz()


class CrazTests(unittest.TestCase):

    @unittest.skipUnless(False, "The test is not written")
    def test_craz(self):
        # TODO: Implement the tests for this function
        pass

    def tearDown(self):
        craz()


class CdumpTests(unittest.TestCase):

    @unittest.skipUnless(False, "The test is not written")
    def test_cdump(self):
        # TODO: Implement the tests for this function
        pass

    def tearDown(self):
        craz()


class ListCacheTests(unittest.TestCase):

    def test_list_cache(self):
        list_ref = list()
        for cachedir in env.environment.cachedirs:
            for (d, subd, files) in os.walk(cachedir):
                for f in files:
                    if any([f.endswith(term) for term in [".png", ".nc", ".pdf", ".eps"]]):
                        list_ref.append(os.path.sep.join([d, f]))
        self.assertEqual(list_cache(), list_ref)

    def tearDown(self):
        craz()


class ClistTests(unittest.TestCase):

    @unittest.skipUnless(False, "The test is not written")
    def test_clist(self):
        # TODO: Implement the tests for this function
        from climaf.cache import cachedirs
        # TODO: Once implemented, deal with several cachedirs
        cachedir = cachedirs[0]

        def find_files(rep, size="", age="", access=0, pattern="", not_pattern="", usage=False, count=False,
                       remove=False, CRS=False, special=False):
            list_ref = list()
            dict_ref = dict()
            if usage:
                dict_usage = dict()
            for (d, subd, files) in os.walk(rep):
                for f in files:
                    fname = os.path.sep.join([d, f])
                    test = (True in [fname.endswith(term) for term in [".png", ".nc", ".pdf", ".eps"]])
                    fname_stats = os.stat(fname)
                    size = size.strip()
                    if test and size:
                        if size.endswith("k"):
                            size = int(size[:-1])*1024
                        elif size.endswith("M"):
                            size = int(size[:-1])*1024*1024
                        elif size.endswith("G"):
                            size = int(size[:-1])*1024*1024*1024
                        elif size.endswith("T"):
                            size = int(size[:-1])*1024*1024*1024*1024
                        else:
                            try:
                                size = int(size)
                            except ValueError:
                                raise Exception("Could not deal with value %s as a size for a file")
                        test = fname_stats.st_size > size
                    if test and age:
                        test = fname_stats.st_ctime > (age * 24 * 3600)
                    if test and access != 0:
                        test = fname_stats.st_atime > (access * 24 * 3600)
                    if test:
                        fcrs = getCRS(fname)
                        import re
                        test = re.search(pattern, crewrite(fcrs)) or re.search(pattern, fname)
                        if test:
                            test = (re.search(not_pattern, crewrite(fcrs)) is None) \
                                   and (re.search(not_pattern, fname) is None)
                        if test:
                            list_ref.append(fname)
                            dict_ref[fcrs] = fname
                            if usage:
                                dict_usage[fcrs] = size
            if usage:
                du_list_sort = dict_usage.items()
                from operator import itemgetter
                du_list_sort.sort(key=itemgetter(1), reverse=False)
                unit = ["K", "M", "G", "T"]
                for n, pair in enumerate(du_list_sort):
                    i = 0
                    flt = float(pair[1])
                    while flt >= 1024. and i < 4:
                        flt /= 1024.
                        i += 1
                    du_list_sort[n] = (du_list_sort[n][0], "%6.1f%s" % (flt, unit[i]))

    def tearDown(self):
        craz()


class ClsTests(unittest.TestCase):

    @unittest.skipUnless(False, "The test is not written")
    def test_cls(self):
        # TODO: Implement the tests for this function
        pass

    def tearDown(self):
        craz()


class CrmTests(unittest.TestCase):

    @unittest.skipUnless(False, "The test is not written")
    def test_crm(self):
        # TODO: Implement the tests for this function
        pass

    def tearDown(self):
        craz()


class CduTests(unittest.TestCase):

    @unittest.skipUnless(False, "The test is not written")
    def test_cdu(self):
        # TODO: Implement the tests for this function
        pass

    def tearDown(self):
        craz()


class CwcTests(unittest.TestCase):

    @unittest.skipUnless(False, "The test is not written")
    def test_cwc(self):
        # TODO: Implement the tests for this function
        pass

    def tearDown(self):
        craz()


class RebuildTests(unittest.TestCase):

    @unittest.skipUnless(False, "The test is not written")
    def test_rebuild(self):
        # TODO: Implement the tests for this function
        pass

    def tearDown(self):
        craz()


class CCostTest(unittest.TestCase):
    def test_ccost(self):
        rst = ds(project="example", simulation="AMIPV6ALB2G",
                 variable="rstcs", period="1980")
        cdrop(rst)
        cfile(rst)
        ccost(rst)

    def tearDown(self):
        craz()


if __name__ == '__main__':
    # Jump into the test directory
    tmp_directory = "/".join([os.environ["HOME"], "tmp", "tests", "test_cache"])
    remove_dir_and_content(tmp_directory)
    if not os.path.isdir(tmp_directory):
        os.makedirs(tmp_directory)
    setNewUniqueCache(tmp_directory)
    os.chdir(tmp_directory)
    unittest.main()
