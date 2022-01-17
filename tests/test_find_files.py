#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test the find files module.
"""

from __future__ import print_function, division, unicode_literals, absolute_import


import unittest
import os

from env.environment import *
from climaf.cache import setNewUniqueCache, craz
from tests.tools_for_tests import remove_dir_and_content
from climaf.find_files import selectGenericFiles, mysplit, build_facets_regexp, rreplace, store_wildcard_facet_values, \
	my_glob, extract_period, glob_remote_data, post_process_wildcard_facets_values


class selectGenericFilesTest(unittest.TestCase):
	@unittest.skipUnless(False, "The test is not written")
	def test_selectGenericFiles(self):
		# TODO: Implement the tests
		pass

	def tearDown(self):
		craz()


class mysplitTest(unittest.TestCase):
	@unittest.skipUnless(False, "The test is not written")
	def test_mysplit(self):
		# TODO: Implement the tests
		pass

	def tearDown(self):
		craz()


class build_facets_regexpTest(unittest.TestCase):
	@unittest.skipUnless(False, "The test is not written")
	def test_build_facets_regexp(self):
		# TODO: Implement the tests
		pass

	def tearDown(self):
		craz()


class rreplaceTest(unittest.TestCase):
	@unittest.skipUnless(False, "The test is not written")
	def test_rreplace(self):
		# TODO: Implement the tests
		pass

	def tearDown(self):
		craz()


class store_wildcard_facet_valuesTest(unittest.TestCase):
	@unittest.skipUnless(False, "The test is not written")
	def test_store_wildcard_facets_values(self):
		# TODO: Implement the tests
		pass

	def tearDown(self):
		craz()


class myglobTest(unittest.TestCase):
	@unittest.skipUnless(False, "The test is not written")
	def test_myglob(self):
		# TODO: Implement the tests
		pass

	def tearDown(self):
		craz()


class extract_periodTest(unittest.TestCase):
	@unittest.skipUnless(False, "The test is not written")
	def test_extract_period(self):
		# TODO: Implement the tests
		pass

	def tearDown(self):
		craz()


class glob_remote_dataTest(unittest.TestCase):
	@unittest.skipUnless(False, "The test is not written")
	def test_glob_remote_data(self):
		# TODO: Implement the tests
		pass

	def tearDown(self):
		craz()


class post_process_wildcard_facets_valuesTest(unittest.TestCase):
	@unittest.skipUnless(False, "The test is not written")
	def test_post_process_wildcard_facets_values(self):
		# TODO: Implement the tests
		pass

	def tearDown(self):
		craz()


if __name__ == '__main__':
	# Jump into the test directory
	tmp_directory = "/".join([os.environ["HOME"], "tmp", "tests", "test_find_files"])
	remove_dir_and_content(tmp_directory)
	if not os.path.isdir(tmp_directory):
		os.makedirs(tmp_directory)
	setNewUniqueCache(tmp_directory)
	os.chdir(tmp_directory)
	unittest.main()
