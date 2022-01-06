#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test the cache module.
"""

from __future__ import print_function, division, unicode_literals, absolute_import


import shutil
import unittest

from env.environment import *
from tests.tools_for_tests import remove_dir_and_content
from climaf.cache import setNewUniqueCache, craz
from climaf.dataloc import dataloc, getlocs, isLocal, selectFiles, \
	remote_to_local_filename, selectEmFiles, periodOfEmFile, selectExampleFiles, selectCmip5DrsFiles


class DatalocTest(unittest.TestCase):
	@unittest.skipUnless(False, "The test is not written")
	def test_init(self):
		# TODO: Implement the tests
		pass

	@unittest.skipUnless(False, "The test is not written")
	def test_eq(self):
		# TODO: Implement the tests
		pass

	@unittest.skipUnless(False, "The test is not written")
	def test_ne(self):
		# TODO: Implement the tests
		pass

	@unittest.skipUnless(False, "The test is not written")
	def test_str(self):
		# TODO: Implement the tests
		pass

	@unittest.skipUnless(False, "The test is not written")
	def test_pr(self):
		# TODO: Implement the tests
		pass

	def tearDown(self):
		craz()


class getlocsTest(unittest.TestCase):
	@unittest.skipUnless(False, "The test is not written")
	def test_getlocs(self):
		# TODO: Implement the tests
		pass

	def tearDown(self):
		craz()


class isLocalTest(unittest.TestCase):
	@unittest.skipUnless(False, "The test is not written")
	def test_isLocal(self):
		# TODO: Implement the tests
		pass

	def tearDown(self):
		craz()


class selectFilesTest(unittest.TestCase):
	@unittest.skipUnless(False, "The test is not written")
	def test_selectFiles(self):
		# TODO: Implement the tests
		pass

	def tearDown(self):
		craz()


class remote_to_local_filenameTest(unittest.TestCase):
	@unittest.skipUnless(False, "The test is not written")
	def test_remote_to_local_filename(self):
		# TODO: Implement the tests
		pass

	def tearDown(self):
		craz()


class selectEmFilesTest(unittest.TestCase):
	@unittest.skipUnless(False, "The test is not written")
	def test_selectEmFiles(self):
		# TODO: Implement the tests
		pass

	def tearDown(self):
		craz()


class periodOfEmFileTest(unittest.TestCase):
	@unittest.skipUnless(False, "The test is not written")
	def test_periodOfEmFile(self):
		# TODO: Implement the tests
		pass


	def tearDown(self):
		craz()

class selectExampleFilesTest(unittest.TestCase):
	@unittest.skipUnless(False, "The test is not written")
	def test_selectExampleFiles(self):
		# TODO: Implement the tests
		pass


	def tearDown(self):
		craz()

class selectCmip5DrsFilesTest(unittest.TestCase):
	@unittest.skipUnless(False, "The test is not written")
	def test_selectCmip5DrsFiles(self):
		# TODO: Implement the tests
		pass


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
