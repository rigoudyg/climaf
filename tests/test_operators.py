#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test the operators module.
"""

import os
import unittest

from tests.tools_for_tests import remove_dir_and_content

from climaf.cache import setNewUniqueCache
from climaf.operators import scriptFlags, cscript, fixed_fields, coperator, derive, is_derived_variable, \
    derived_variable, Climaf_Operator_Error


class ScriptFlagsTests(unittest.TestCase):

    def test_scriptFlags_noargs(self):
        my_script_flag = scriptFlags()
        self.assertFalse(my_script_flag.canOpendap)
        self.assertFalse(my_script_flag.canSelectVar)
        self.assertFalse(my_script_flag.canSelectTime)
        self.assertFalse(my_script_flag.canSelectDomain)
        self.assertFalse(my_script_flag.canAggregateTime)
        self.assertFalse(my_script_flag.canAlias)
        self.assertFalse(my_script_flag.canMissing)
        self.assertTrue(my_script_flag.commuteWithEnsemble)
        self.assertFalse(my_script_flag.commuteWithTimeConcatenation)
        self.assertFalse(my_script_flag.commuteWithSpaceConcatenation)

    def test_scriptFlags_args(self):
        my_script_flag = scriptFlags(canSelectVar=True, commuteWithSpaceConcatenation=True, canMissing=True)
        self.assertFalse(my_script_flag.canOpendap)
        self.assertTrue(my_script_flag.canSelectVar)
        self.assertFalse(my_script_flag.canSelectTime)
        self.assertFalse(my_script_flag.canSelectDomain)
        self.assertFalse(my_script_flag.canAggregateTime)
        self.assertFalse(my_script_flag.canAlias)
        self.assertTrue(my_script_flag.canMissing)
        self.assertTrue(my_script_flag.commuteWithEnsemble)
        self.assertFalse(my_script_flag.commuteWithTimeConcatenation)
        self.assertTrue(my_script_flag.commuteWithSpaceConcatenation)
        my_script_flag.unset_selectors()
        self.assertFalse(my_script_flag.canOpendap)
        self.assertFalse(my_script_flag.canSelectVar)
        self.assertFalse(my_script_flag.canSelectTime)
        self.assertFalse(my_script_flag.canSelectDomain)
        self.assertFalse(my_script_flag.canAggregateTime)
        self.assertFalse(my_script_flag.canAlias)
        self.assertFalse(my_script_flag.canMissing)
        self.assertTrue(my_script_flag.commuteWithEnsemble)
        self.assertFalse(my_script_flag.commuteWithTimeConcatenation)
        self.assertTrue(my_script_flag.commuteWithSpaceConcatenation)

    def test_equality(self):
        self.assertTrue(scriptFlags() == scriptFlags(canOpendap=False))
        self.assertFalse(scriptFlags() == scriptFlags(commuteWithEnsemble=False))


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
            my_script = cscript('mycdo','mycdo ${operator} ${in} ${out}')

    def test_simple_cscript(self):
        my_script = cscript('mycdo','(cdo ${operator} ${in} ${out})')
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
        my_script = cscript('mycdo2','(cdo ${operator} ${in_1} ${in_2} ${period} ${var} ${alias} ${missing} ${domain} ${out_tas})', format="txt")
        self.assertDictEqual(my_script.inputs, {1: ('in_1', False, False), 2: ('in_2', False, False)})
        self.assertDictEqual(my_script.outputs, {'tas': '%s'})
        self.assertEqual(my_script.name, "mycdo2")
        self.assertEqual(my_script.command, '(cdo ${operator} ${in_1} ${in_2} ${period} ${var} ${alias} ${missing} ${domain} ${out_tas})')
        self.assertIsNone(my_script.fixedfields)
        self.assertEqual(my_script.flags, scriptFlags(canSelectVar=True, canSelectTime=True, canSelectDomain=True,
                                                      canAlias=True, canMissing=True))
        self.assertEqual(my_script.outputFormat, "txt")
        self.assertTrue("mycdo2" in globals())
        import sys
        self.assertTrue("mycdo2" in sys.modules["__main__"].__dict__)

    def test_duplicate_entry(self):
        my_script = cscript('mycdo3','(cdo ${operator} ${in_1} ${in_1} ${out})')
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
            cscript('mycdo2','(cdo ${operator} ${in_1} ${mmin_2} ${out})')
        with self.assertRaises(Climaf_Operator_Error):
            cscript('mycdo2','(cdo ${operator} ${in_1} ${mmins_2} ${out})')
        with self.assertRaises(Climaf_Operator_Error):
            cscript('mycdo2','(cdo ${operator} ${out})')
        with self.assertRaises(Climaf_Operator_Error):
            cscript('mycdo2','(cdo ${operator} ${mmins} ${out})')
        with self.assertRaises(Climaf_Operator_Error):
            cscript('mycdo2','(cdo ${operator} ${in_3} ${in_5} ${out})')
        with self.assertRaises(Climaf_Operator_Error):
            cscript('mycdo2','(cdo ${operator} ${in} ${out})', format="fa")

    def test_repr(self):
        my_script = cscript('mycdo','(cdo ${operator} ${in} ${out})')
        self.assertEqual(repr(my_script), "CliMAF operator : mycdo")


class FixedFieldsTest(unittest.TestCase):

    def test_fixed_fields(self):
        fixed_fields('minus', ('mesh_hgr.nc','/data/climaf/${project}/${model}/ORCA1_mesh_hgr.nc'),
                     ('mesh_zgr.nc','/data/climaf/${project}/${model}/ORCA1_mesh_zgr.nc'))
        fixed_fields(['plot', ],
                     ('coordinates.nc','/cnrm/ioga/Users/chevallier/chevalli/Partage/NEMO/eORCA_R025_coordinates_v1.0.nc'))
        from climaf.operators import scripts
        self.assertEqual(scripts["minus"].fixedfields,
                         (('mesh_hgr.nc','/data/climaf/${project}/${model}/ORCA1_mesh_hgr.nc'),
                          ('mesh_zgr.nc','/data/climaf/${project}/${model}/ORCA1_mesh_zgr.nc')))
        self.assertEqual(scripts["plot"].fixedfields,
                         (('coordinates.nc','/cnrm/ioga/Users/chevallier/chevalli/Partage/NEMO/eORCA_R025_coordinates_v1.0.nc'), ))


class CoperatorTest(unittest.TestCase):

    @unittest.skipUnless(False, "Not implemented")
    def test_coperator(self):
        # TODO: Implement this test
        pass


class DeriveTest(unittest.TestCase):

    def test_derive_from_script(self):
        derive("erai", 'ta','rescale', 't', scale=1., offset=0.)
        derive('*', dict(out='rscre'),'minus','rs','rscs')
        self.assertIsNone(derive("erai", "ta2", "minus", "t", "ta", "rscre"))
        from climaf.operators import derived_variables
        self.assertEqual(derived_variables["erai"]["ta"], ('rescale', 'ta', ['t'], {'scale': 1.0, 'offset': 0.0}))
        self.assertEqual(derived_variables["*"]["rscre"], ('minus', 'rscre', ['rs', 'rscs'], {}))
        self.assertNotIn("ta2", derived_variables["erai"])
        with self.assertRaises(Climaf_Operator_Error):
            derive("CMIP5", dict(my_out_name='ta2'),'rescale', 't', scale=2., offset=-154.3)

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
        derive("erai", 'ta','rescale', 't', scale=1., offset=0.)
        derive('*', 'rscre','minus','rs','rscs')

    def test_is_derived_variable(self):
        self.assertTrue(is_derived_variable("ta", "erai"))
        self.assertTrue(is_derived_variable("rscre", "erai"))
        self.assertFalse(is_derived_variable("ta", "CMIP6"))


class DerivedVariableTest(unittest.TestCase):

    def setUp(self):
        derive("erai", 'ta','rescale', 't', scale=1., offset=0.)
        derive('*', 'rscre','minus','rs','rscs')

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
    unittest.main()
    remove_dir_and_content(tmp_directory)
