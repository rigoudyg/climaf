#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Test the operators module.
"""
from __future__ import print_function, division, unicode_literals, absolute_import


import os
import unittest

from tests.tools_for_tests import remove_dir_and_content
from env.environment import *

from climaf.cache import setNewUniqueCache
from climaf.operators import scriptFlags, cscript, fixed_fields, coperator
from climaf.operators_derive import derive, is_derived_variable, derived_variable, Climaf_Operator_Error


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


class IsDerivedVariableTest(unittest.TestCase):

    def setUp(self):
        derive("erai", 'ta', 'rescale', 't', scale=1., offset=0.)
        derive('*', 'rscre', 'minus', 'rs', 'rscs')

    def test_is_derived_variable(self):
        self.assertTrue(is_derived_variable("ta", "erai"))
        self.assertTrue(is_derived_variable("rscre", "erai"))
        self.assertFalse(is_derived_variable("ta", "CMIP6"))


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


if __name__ == '__main__':
    # Jump into the test directory
    tmp_directory = "/".join([os.environ["HOME"], "tmp", "tests", "test_operators"])
    remove_dir_and_content(tmp_directory)
    if not os.path.isdir(tmp_directory):
        os.makedirs(tmp_directory)
    setNewUniqueCache(tmp_directory)
    os.chdir(tmp_directory)
    unittest.main(exit=False)
    remove_dir_and_content(tmp_directory)
