#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test the driver module.
"""
from __future__ import print_function, division, unicode_literals, absolute_import

import os
import unittest

from tests.tools_for_tests import remove_dir_and_content
from env.environment import *
from env.site_settings import atCNRM, onCiclad
from climaf.cache import setNewUniqueCache, craz
from climaf.api import cproject, dataloc
from climaf.driver import capply, capply_script, maketree, capply_operator, ceval_for_cdataset, ceval_for_ctree, \
	ceval_operator, cstore, ceval_for_scriptChild, ceval_for_cpage, ceval_for_cpage_pdf, ceval_for_cens, \
	ceval_for_string, ceval, ceval_script, timePeriod, ceval_select, cread, cview, derive_variable, set_variable, \
	noselect, cfile, cshow, cMA, cvalue, cexport, cimport, get_fig_sizes, cfilePage, cfilePage_pdf, calias, CFlongname, \
	efile
from climaf.utils import Climaf_Driver_Error
from climaf.classes import ds
from climaf.period import Climaf_Period_Error, init_period


class CapplyTests(unittest.TestCase):

	@unittest.skipUnless(False, "Test not yet written")
	def test_capply(self):
		# TODO: Write the test
		pass

	def tearDown(self):
		craz()


class CapplyScriptTests(unittest.TestCase):

	@unittest.skipUnless(False, "Test not yet written")
	def test_capply_script(self):
		# TODO: Write the test
		pass

	def tearDown(self):
		craz()


class MaketreeTests(unittest.TestCase):

	@unittest.skipUnless(False, "Test not yet written")
	def test_maketree(self):
		# TODO: Write the test
		pass

	def tearDown(self):
		craz()


class CapplyOperatorTests(unittest.TestCase):

	@unittest.skipUnless(False, "Test not yet written")
	def test_capply_operator(self):
		# TODO: Write the test
		pass

	def tearDown(self):
		craz()


class CevalForCdatasetTests(unittest.TestCase):

	@unittest.skipUnless(False, "Test not yet written")
	def test_ceval_for_cdataset(self):
		# TODO: Write the test
		pass

	def tearDown(self):
		craz()


class CevalForCtreeTests(unittest.TestCase):

	@unittest.skipUnless(False, "Test not yet written")
	def test_ceval_for_ctree(self):
		# TODO: Write the test
		pass

	def tearDown(self):
		craz()


class CevalOperatorTests(unittest.TestCase):

	@unittest.skipUnless(False, "Test not yet written")
	def test_ceval_operator(self):
		# TODO: Write the test
		pass

	def tearDown(self):
		craz()


class CstoreTests(unittest.TestCase):

	@unittest.skipUnless(False, "Test not yet written")
	def test_cstore(self):
		# TODO: Write the test
		pass

	def tearDown(self):
		craz()


class CevalForScriptChildTests(unittest.TestCase):

	@unittest.skipUnless(False, "Test not yet written")
	def test_ceval_for_scriptChild(self):
		# TODO: Write the test
		pass

	def tearDown(self):
		craz()


class CevalForCpageTests(unittest.TestCase):

	@unittest.skipUnless(False, "Test not yet written")
	def test_ceval_for_cpage(self):
		# TODO: Write the test
		pass

	def tearDown(self):
		craz()


class CevalForCpagePdfTests(unittest.TestCase):

	@unittest.skipUnless(False, "Test not yet written")
	def test_ceval_for_cpage_pdf(self):
		# TODO: Write the test
		pass

	def tearDown(self):
		craz()


class CevalForCensTests(unittest.TestCase):

	@unittest.skipUnless(False, "Test not yet written")
	def test_ceval_for_cens(self):
		# TODO: Write the test
		pass

	def tearDown(self):
		craz()


class CevalForStringTests(unittest.TestCase):

	@unittest.skipUnless(False, "Test not yet written")
	def test_ceval_for_string(self):
		# TODO: Write the test
		pass

	def tearDown(self):
		craz()


class CevalTests(unittest.TestCase):

	@unittest.skipUnless(False, "Test not yet written")
	def test_ceval(self):
		# TODO: Write the test
		pass

	def tearDown(self):
		craz()


class CevalScriptTests(unittest.TestCase):

	@unittest.skipUnless(False, "Test not yet written")
	def test_ceval_script(self):
		# TODO: Write the test
		pass

	def tearDown(self):
		craz()


class TimePeriodTests(unittest.TestCase):

	@unittest.skipUnless(False, "Test not yet written")
	def test_timePeriod(self):
		# TODO: Write the test
		pass

	def tearDown(self):
		craz()


class CevalSelectTests(unittest.TestCase):

	@unittest.skipUnless(False, "Test not yet written")
	def test_ceval_select(self):
		# TODO: Write the test
		pass

	def tearDown(self):
		craz()


class CreadTests(unittest.TestCase):

	@unittest.skipUnless(False, "Test not yet written")
	def test_cread(self):
		# TODO: Write the test
		pass

	def tearDown(self):
		craz()


class CviewTests(unittest.TestCase):

	@unittest.skipUnless(False, "Test not yet written")
	def test_cview(self):
		# TODO: Write the test
		pass

	def tearDown(self):
		craz()


class DeriveVariableTests(unittest.TestCase):

	@unittest.skipUnless(False, "Test not yet written")
	def test_derive_variable(self):
		# TODO: Write the test
		pass

	def tearDown(self):
		craz()


class SetVariableTests(unittest.TestCase):

	@unittest.skipUnless(False, "Test not yet written")
	def test_set_variable(self):
		# TODO: Write the test
		pass

	def tearDown(self):
		craz()


class NoselectTests(unittest.TestCase):

	@unittest.skipUnless(False, "Test not yet written")
	def test_noselect(self):
		# TODO: Write the test
		pass

	def tearDown(self):
		craz()


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

	def tearDown(self):
		craz()


class CshowTests(unittest.TestCase):

	@unittest.skipUnless(False, "Test not yet written")
	def test_cshow(self):
		# TODO: Write the test
		pass

	def tearDown(self):
		craz()


class CMATests(unittest.TestCase):

	@unittest.skipUnless(False, "Test not yet written")
	def test_cMA(self):
		# TODO: Write the test
		pass

	def tearDown(self):
		craz()


class CvalueTests(unittest.TestCase):

	@unittest.skipUnless(False, "Test not yet written")
	def test_cvalue(self):
		# TODO: Write the test
		pass

	def tearDown(self):
		craz()


class CexportTests(unittest.TestCase):

	@unittest.skipUnless(False, "Test not yet written")
	def test_cexport(self):
		# TODO: Write the test
		pass

	def tearDown(self):
		craz()


class CimportTests(unittest.TestCase):

	@unittest.skipUnless(False, "Test not yet written")
	def test_cimport(self):
		# TODO: Write the test
		pass

	def tearDown(self):
		craz()


class GetFigSizesTests(unittest.TestCase):

	@unittest.skipUnless(False, "Test not yet written")
	def test_get_fig_sizes(self):
		# TODO: Write the test
		pass

	def tearDown(self):
		craz()


class CfilePageTests(unittest.TestCase):

	@unittest.skipUnless(False, "Test not yet written")
	def test_cfilePage(self):
		# TODO: Write the test
		pass

	def tearDown(self):
		craz()


class CfilePagePdfTests(unittest.TestCase):

	@unittest.skipUnless(False, "Test not yet written")
	def test_cfilePage_pdf(self):
		# TODO: Write the test
		pass

	def tearDown(self):
		craz()


class CaliasTests(unittest.TestCase):

	def setUp(self):
		cproject('data_CNRM')
		root = "/cnrm/est/COMMON/climaf/test_data/${simulation}/O/"
		suffix = "${simulation}_1m_YYYYMMDD_YYYYMMDD_${variable}.nc"
		data_url = root + suffix
		dataloc(project='data_CNRM', organization='generic', url=data_url)

	def test_calias(self):
		# TODO: Write the test
		if "data_CNRM" in aliases or "data_CNRM" in derived_variables:
			raise KeyError("Should not have aliases for 'data_CNRM' at this stage")
		calias("data_CNRM", "tos,thetao", filenameVar="grid_T_table2.2")
		calias("data_CNRM", "uo", filenameVar="grid_U_table2.3")
		self.assertDictEqual(aliases["data_CNRM"],
		                     {'tos,thetao': ('tos,thetao', 1.0, 0.0, None, 'grid_T_table2.2', None, None),
		                      'tos': ('tos', 1.0, 0.0, None, 'grid_T_table2.2', None, None),
		                      'thetao': ('thetao', 1.0, 0.0, None, 'grid_T_table2.2', None, None),
		                      'uo': ('uo', 1.0, 0.0, None, 'grid_U_table2.3', None, None)
		                      })
		self.assertDictEqual(derived_variables["data_CNRM"],
		                     {'tos': ('ccdo', 'tos', ['tos,thetao'], {'operator': 'selname,tos'}),
		                      'thetao': ('ccdo', 'thetao', ['tos,thetao'], {'operator': 'selname,thetao'})
		                      })

	def tearDown(self):
		craz()


class CFlongnameTests(unittest.TestCase):

	@unittest.skipUnless(False, "Test not yet written")
	def test_CFlongname(self):
		# TODO: Write the test
		pass

	def tearDown(self):
		craz()


class EfileTests(unittest.TestCase):

	@unittest.skipUnless(False, "Test not yet written")
	def test_efile(self):
		# TODO: Write the test
		pass

	def tearDown(self):
		craz()


if __name__ == '__main__':
	# Jump into the test directory
	tmp_directory = "/".join([os.environ["HOME"], "tmp", "tests", "test_driver"])
	remove_dir_and_content(tmp_directory)
	if not os.path.isdir(tmp_directory):
		os.makedirs(tmp_directory)
	setNewUniqueCache(tmp_directory)
	os.chdir(tmp_directory)
	unittest.main()
