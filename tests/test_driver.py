#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test the driver module.
"""
from __future__ import print_function, division, unicode_literals, absolute_import


import os
import unittest

from tests.tools_for_tests import remove_dir_and_content

from climaf.cache import setNewUniqueCache
from climaf.driver import capply, capply_script, maketree, capply_operator, ceval_for_cdataset, ceval_for_ctree, \
	ceval_operator, cstore, ceval_for_scriptChild, ceval_for_cpage, ceval_for_cpage_pdf, ceval_for_cens, \
	ceval_for_string, ceval, ceval_script, timePeriod, ceval_select, cread, cview, derive_variable, set_variable, \
	noselect, cfile, cshow, cMA, cvalue, cexport, cimport, get_fig_sizes, cfilePage, cfilePage_pdf, calias, CFlongname,\
	efile, Climaf_Driver_Error
from climaf.classes import ds
from climaf.period import Climaf_Period_Error, init_period
from env.environment import *
from env.site_settings import atCNRM, onCiclad


class CapplyTests(unittest.TestCase):

	@unittest.skipUnless(False, "Test not yet written")
	def test_capply(self):
		# TODO: Write the test
		pass


class CapplyScriptTests(unittest.TestCase):

	@unittest.skipUnless(False, "Test not yet written")
	def test_capply_script(self):
		# TODO: Write the test
		pass


class MaketreeTests(unittest.TestCase):

	@unittest.skipUnless(False, "Test not yet written")
	def test_maketree(self):
		# TODO: Write the test
		pass


class CapplyOperatorTests(unittest.TestCase):

	@unittest.skipUnless(False, "Test not yet written")
	def test_capply_operator(self):
		# TODO: Write the test
		pass


class CevalForCdatasetTests(unittest.TestCase):

	@unittest.skipUnless(False, "Test not yet written")
	def test_ceval_for_cdataset(self):
		# TODO: Write the test
		pass


class CevalForCtreeTests(unittest.TestCase):

	@unittest.skipUnless(False, "Test not yet written")
	def test_ceval_for_ctree(self):
		# TODO: Write the test
		pass


class CevalOperatorTests(unittest.TestCase):

	@unittest.skipUnless(False, "Test not yet written")
	def test_ceval_operator(self):
		# TODO: Write the test
		pass


class CstoreTests(unittest.TestCase):

	@unittest.skipUnless(False, "Test not yet written")
	def test_cstore(self):
		# TODO: Write the test
		pass


class CevalForScriptChildTests(unittest.TestCase):

	@unittest.skipUnless(False, "Test not yet written")
	def test_ceval_for_scriptChild(self):
		# TODO: Write the test
		pass


class CevalForCpageTests(unittest.TestCase):

	@unittest.skipUnless(False, "Test not yet written")
	def test_ceval_for_cpage(self):
		# TODO: Write the test
		pass


class CevalForCpagePdfTests(unittest.TestCase):

	@unittest.skipUnless(False, "Test not yet written")
	def test_ceval_for_cpage_pdf(self):
		# TODO: Write the test
		pass


class CevalForCensTests(unittest.TestCase):

	@unittest.skipUnless(False, "Test not yet written")
	def test_ceval_for_cens(self):
		# TODO: Write the test
		pass


class CevalForStringTests(unittest.TestCase):

	@unittest.skipUnless(False, "Test not yet written")
	def test_ceval_for_string(self):
		# TODO: Write the test
		pass


class CevalTests(unittest.TestCase):

	@unittest.skipUnless(False, "Test not yet written")
	def test_ceval(self):
		# TODO: Write the test
		pass


class CevalScriptTests(unittest.TestCase):

	@unittest.skipUnless(False, "Test not yet written")
	def test_ceval_script(self):
		# TODO: Write the test
		pass


class TimePeriodTests(unittest.TestCase):

	@unittest.skipUnless(False, "Test not yet written")
	def test_timePeriod(self):
		# TODO: Write the test
		pass


class CevalSelectTests(unittest.TestCase):

	@unittest.skipUnless(False, "Test not yet written")
	def test_ceval_select(self):
		# TODO: Write the test
		pass


class CreadTests(unittest.TestCase):

	@unittest.skipUnless(False, "Test not yet written")
	def test_cread(self):
		# TODO: Write the test
		pass


class CviewTests(unittest.TestCase):

	@unittest.skipUnless(False, "Test not yet written")
	def test_cview(self):
		# TODO: Write the test
		pass


class DeriveVariableTests(unittest.TestCase):

	@unittest.skipUnless(False, "Test not yet written")
	def test_derive_variable(self):
		# TODO: Write the test
		pass


class SetVariableTests(unittest.TestCase):

	@unittest.skipUnless(False, "Test not yet written")
	def test_set_variable(self):
		# TODO: Write the test
		pass


class NoselectTests(unittest.TestCase):

	@unittest.skipUnless(False, "Test not yet written")
	def test_noselect(self):
		# TODO: Write the test
		pass


class CfileTests(unittest.TestCase):

	@unittest.skipUnless(False, "Test not yet written")
	def test_cfile(self):
		# TODO: Write the test
		pass

	def test_cdataset_cfile_not_ambiguous(self):
		my_data_test = ds(project="example", variable="tas", period="*", simulation="AMIPV6ALB2G")
		dict_choices = my_data_test.explore("choices")
		self.assertDictEqual(dict_choices, {'period': [init_period("1980-1981")]})
		cfile(my_data_test)


class CshowTests(unittest.TestCase):

	@unittest.skipUnless(False, "Test not yet written")
	def test_cshow(self):
		# TODO: Write the test
		pass


class CMATests(unittest.TestCase):

	@unittest.skipUnless(False, "Test not yet written")
	def test_cMA(self):
		# TODO: Write the test
		pass


class CvalueTests(unittest.TestCase):

	@unittest.skipUnless(False, "Test not yet written")
	def test_cvalue(self):
		# TODO: Write the test
		pass


class CexportTests(unittest.TestCase):

	@unittest.skipUnless(False, "Test not yet written")
	def test_cexport(self):
		# TODO: Write the test
		pass


class CimportTests(unittest.TestCase):

	@unittest.skipUnless(False, "Test not yet written")
	def test_cimport(self):
		# TODO: Write the test
		pass


class GetFigSizesTests(unittest.TestCase):

	@unittest.skipUnless(False, "Test not yet written")
	def test_get_fig_sizes(self):
		# TODO: Write the test
		pass


class CfilePageTests(unittest.TestCase):

	@unittest.skipUnless(False, "Test not yet written")
	def test_cfilePage(self):
		# TODO: Write the test
		pass


class CfilePagePdfTests(unittest.TestCase):

	@unittest.skipUnless(False, "Test not yet written")
	def test_cfilePage_pdf(self):
		# TODO: Write the test
		pass


class CaliasTests(unittest.TestCase):

	@unittest.skipUnless(False, "Test not yet written")
	def test_calias(self):
		# TODO: Write the test
		pass


class CFlongnameTests(unittest.TestCase):

	@unittest.skipUnless(False, "Test not yet written")
	def test_CFlongname(self):
		# TODO: Write the test
		pass


class EfileTests(unittest.TestCase):

	@unittest.skipUnless(False, "Test not yet written")
	def test_efile(self):
		# TODO: Write the test
		pass


if __name__ == '__main__':
	# Jump into the test directory
	tmp_directory = "/".join([os.environ["HOME"], "tmp", "tests", "test_driver"])
	remove_dir_and_content(tmp_directory)
	if not os.path.isdir(tmp_directory):
		os.makedirs(tmp_directory)
	setNewUniqueCache(tmp_directory)
	os.chdir(tmp_directory)
	unittest.main()
	remove_dir_and_content(tmp_directory)
