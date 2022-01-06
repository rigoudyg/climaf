#!/usr/bin/env python
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
from climaf.operators import scriptFlags, cscript, fixed_fields, coperator, Climaf_Operator_Error


class CscriptTest(unittest.TestCase):

    def test_existing_function(self):
        # TODO: Modify cscript to avoid creating an instance of the script if not possible
        import sys
        a = sys.modules["__main__"].__dict__["tmp_directory"]
        my_script = cscript("tmp_directory", "cdo ${operator} ${in} ${out}")
        self.assertEqual(sys.modules["__main__"].__dict__["tmp_directory"], a)

    @unittest.expectedFailure
    def test_unexisting_function(self):
        with self.assertRaises(Climaf_Operator_Error):
            my_script = cscript('mycdo', 'mycdo ${operator} ${in} ${out}')

    def test_simple_cscript(self):
        my_script = cscript('mycdo', '(cdo ${operator} ${in} ${out})')
        self.assertTrue(isinstance(my_script, cscript))
        self.assertDictEqual(my_script.inputs, {0: ('in', False, False)})
        self.assertDictEqual(my_script.outputs, {None: '%s', '': '%s'})
        self.assertEqual(my_script.name, "mycdo")
        self.assertEqual(my_script.command, '(cdo ${operator} ${in} ${out})')
        self.assertIsNone(my_script.fixedfields)
        self.assertEqual(my_script.flags, scriptFlags())
        self.assertEqual(my_script.outputFormat, "nc")
        self.assertTrue("mycdo" in globals())
        import sys
        self.assertTrue("mycdo" in sys.modules["__main__"].__dict__)
        my_ds1 = ds(project="example", simulation="AMIPV6ALB2G", variable="tas", period="1980-1981")
        mycdo(my_ds1, operator="timavg")
        help(mycdo)

    def test_complex_cscript(self):
        my_script = cscript('mycdo2',
                            '(cdo ${operator} ${in_1} ${in_2} ${period} ${var} ${alias} ${missing} ${domain} '
                            '${out_tas})', format="txt")
        self.assertDictEqual(my_script.inputs, {1: ('in_1', False, False), 2: ('in_2', False, False)})
        self.assertDictEqual(my_script.outputs, {'tas': '%s'})
        self.assertEqual(my_script.name, "mycdo2")
        self.assertEqual(my_script.command,
                         '(cdo ${operator} ${in_1} ${in_2} ${period} ${var} ${alias} ${missing} ${domain} ${out_tas})')
        self.assertIsNone(my_script.fixedfields)
        self.assertEqual(my_script.flags, scriptFlags(canSelectVar=True, canSelectTime=True, canSelectDomain=True,
                                                      canAlias=True, canMissing=True))
        self.assertEqual(my_script.outputFormat, "txt")
        self.assertTrue("mycdo2" in globals())
        import sys
        self.assertTrue("mycdo2" in sys.modules["__main__"].__dict__)

    def test_duplicate_entry(self):
        my_script = cscript('mycdo3', '(cdo ${operator} ${in_1} ${in_1} ${out})')
        self.assertDictEqual(my_script.inputs, {1: ('in_1', False, False)})
        self.assertDictEqual(my_script.outputs, {'': '%s', None: '%s'})
        self.assertEqual(my_script.name, "mycdo3")
        self.assertEqual(my_script.command, '(cdo ${operator} ${in_1} ${in_1} ${out})')
        self.assertIsNone(my_script.fixedfields)
        self.assertEqual(my_script.flags, scriptFlags())
        self.assertEqual(my_script.outputFormat, "nc")
        self.assertTrue("mycdo3" in globals())
        import sys
        self.assertTrue("mycdo3" in sys.modules["__main__"].__dict__)

    def test_errors(self):
        with self.assertRaises(Climaf_Operator_Error):
            cscript('mycdo2', '(cdo ${operator} ${in_1} ${mmins_2} ${out})')
        with self.assertRaises(Climaf_Operator_Error):
            cscript('mycdo2', '(cdo ${operator} ${out})')
        with self.assertRaises(Climaf_Operator_Error):
            cscript('mycdo2', '(cdo ${operator} ${mmins} ${out})')
        with self.assertRaises(Climaf_Operator_Error):
            cscript('mycdo2', '(cdo ${operator} ${in_3} ${in_5} ${out})')
        with self.assertRaises(Climaf_Operator_Error):
            cscript('mycdo2', '(cdo ${operator} ${in} ${out})', format="fa")

    def test_repr(self):
        my_script = cscript('mycdo', '(cdo ${operator} ${in} ${out})')
        self.assertEqual(repr(my_script), "CliMAF operator : mycdo")

    def tearDown(self):
        craz()


class FixedFieldsTest(unittest.TestCase):

    def test_fixed_fields(self):
        fixed_fields('minus', ('mesh_hgr.nc', '/data/climaf/${project}/${model}/ORCA1_mesh_hgr.nc'),
                     ('mesh_zgr.nc', '/data/climaf/${project}/${model}/ORCA1_mesh_zgr.nc'))
        fixed_fields(['plot', ],
                     ('coordinates.nc',
                      '/cnrm/ioga/Users/chevallier/chevalli/Partage/NEMO/eORCA_R025_coordinates_v1.0.nc'))
        self.assertEqual(cscripts["minus"].fixedfields,
                         (('mesh_hgr.nc', '/data/climaf/${project}/${model}/ORCA1_mesh_hgr.nc'),
                          ('mesh_zgr.nc', '/data/climaf/${project}/${model}/ORCA1_mesh_zgr.nc')))
        self.assertEqual(cscripts["plot"].fixedfields,
                         (('coordinates.nc',
                           '/cnrm/ioga/Users/chevallier/chevalli/Partage/NEMO/eORCA_R025_coordinates_v1.0.nc'), ))

    def tearDown(self):
        craz()


class CoperatorTest(unittest.TestCase):

    @unittest.skipUnless(False, "Not implemented")
    def test_coperator(self):
        # TODO: Implement this test
        pass

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
