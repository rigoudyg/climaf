#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Test the operators module.
"""
from __future__ import print_function, division, unicode_literals, absolute_import


import os
import unittest

from tests.tools_for_tests import remove_dir_and_content
from env.environment import *

from climaf.cache import setNewUniqueCache, craz
from climaf.operators import scriptFlags, cscript, fixed_fields, coperator
from climaf.operators_derive import derive, is_derived_variable, derived_variable, Climaf_Operator_Error
from climaf.classes import calias, ds
from climaf.driver import cfile


class DeriveTest(unittest.TestCase):

    def test_derive_from_script(self):
        derive("erai", 'ta', 'rescale', 't', scale=1., offset=0.)
        derive('*', dict(out='rscre'), 'minus', 'rs', 'rscs')
        self.assertIsNone(derive("erai", "ta2", "minus", "t", "ta", "rscre"))
        self.assertEqual(derived_variables["erai"]["ta"], ('rescale', 'ta', ['t'], {'scale': 1.0, 'offset': 0.0}))
        self.assertEqual(derived_variables["*"]["rscre"], ('minus', 'rscre', ['rs', 'rscs'], {}))
        self.assertNotIn("ta2", derived_variables["erai"])
        with self.assertRaises(Climaf_Operator_Error):
            derive("CMIP5", dict(my_out_name='ta2'), 'rescale', 't', scale=2., offset=-154.3)

    @unittest.skipUnless(False, "Not implemented")
    def test_derive_from_operator(self):
        # TODO: Implement this test
        pass

    @unittest.skipUnless(False, "Not implemented")
    def test_derive_from_sth_else(self):
        # TODO: Implement this test and modify CliMAF in this scope
        pass

    def tearDown(self):
        craz()


class IsDerivedVariableTest(unittest.TestCase):

    def setUp(self):
        derive("erai", 'ta', 'rescale', 't', scale=1., offset=0.)
        derive('*', 'rscre', 'minus', 'rs', 'rscs')

    def test_is_derived_variable(self):
        self.assertTrue(is_derived_variable("ta", "erai"))
        self.assertTrue(is_derived_variable("rscre", "erai"))
        self.assertFalse(is_derived_variable("ta", "CMIP6"))

    def tearDown(self):
        craz()


class DerivedVariableTest(unittest.TestCase):

    def setUp(self):
        derive("erai", 'ta', 'rescale', 't', scale=1., offset=0.)
        derive('*', 'rscre', 'minus', 'rs', 'rscs')

    def test_derived_variable(self):
        self.assertIsNone(derived_variable("my_variable", "my_project"))
        self.assertIsNone(derived_variable("my_variable", "CMIP6"))
        self.assertIsNone(derived_variable("ta", "CMIP6"))
        self.assertEqual(derived_variable("rscre", "erai"), ("minus", "rscre", ["rs", "rscs"], {}))
        self.assertEqual(derived_variable("ta", "erai"), ('rescale', 'ta', ['t'], {'scale': 1.0, 'offset': 0.0}))

    def tearDown(self):
        craz()


class DeriveAndAliasTests(unittest.TestCase):

    def setUp(self):
        calias("example", 'tas_degC', 'tas', scale=1., offset=-273.15, units="degC")
        derive('example', 'tas_degC_mul', 'ccdo', 'tas_degC', operator="mulc,5")
        calias("example", "tas_K_mul", "tas_degC_mul", offset=273.15, units="K")

    @unittest.expectedFailure
    def test_derived_variable(self):
        tas = ds(project='example', simulation="AMIPV6ALB2G", variable="tas_K_mul", frequency='monthly', period="198001")
        self.assertEqual(str(tas), "ds('example|AMIPV6ALB2G|tas_K_mul|198001|global|monthly')")
        cfile(tas)

    def tearDown(self):
        craz()


if __name__ == '__main__':
    # Jump into the test directory
    tmp_directory = "/".join([os.environ["HOME"], "tmp", "tests", "test_operators"])
    remove_dir_and_content(tmp_directory)
    if not os.path.isdir(tmp_directory):
        os.makedirs(tmp_directory)
    setNewUniqueCache(tmp_directory)
    os.chdir(tmp_directory)
    unittest.main()
