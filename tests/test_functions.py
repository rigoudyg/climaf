#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test the classes module.
"""
from __future__ import print_function, division, unicode_literals, absolute_import


import unittest

from tests.tools_for_tests import remove_dir_and_content
from env.environment import *
from climaf.cache import setNewUniqueCache, craz
from climaf.driver import cfile
from climaf.classes import ds
from climaf.functions import cscalar, apply_scale_offset, fmul, fdiv, fadd, fsub, iplot, getLevs, vertical_average, \
    implot, diff_regrid, diff_regridn, tableau, annual_cycle, clim_average, clim_average_fast, summary, projects, \
    lonlatvert_interpolation, zonmean_interpolation, zonmean, diff_zonmean, convert_list_to_string,\
    ts_plot, iplot_members


class CscalarTests(unittest.TestCase):

    @unittest.skipUnless(False, "Test not implemented")
    def test_cscalar(self):
        pass

    def tearDown(self):
        craz()


class ApplyScaleOffsetTests(unittest.TestCase):

    @unittest.skipUnless(False, "Test not implemented")
    def test_apply_scale_offset(self):
        # TODO: Implement the test
        pass

    def tearDown(self):
        craz()


class FmulTests(unittest.TestCase):

    @unittest.skipUnless(False, "Test not implemented")
    def test_fmul(self):
        # TODO: Implement the test
        pass

    def tearDown(self):
        craz()


class FdivTests(unittest.TestCase):

    @unittest.skipUnless(False, "Test not implemented")
    def test_fdiv(self):
        # TODO: Implement the test
        pass

    def tearDown(self):
        craz()


class FaddTests(unittest.TestCase):

    @unittest.skipUnless(False, "Test not implemented")
    def test_fadd(self):
        # TODO: Implement the test
        pass

    def tearDown(self):
        craz()


class FsubTests(unittest.TestCase):

    @unittest.skipUnless(False, "Test not implemented")
    def test_fsub(self):
        # TODO: Implement the test
        pass

    def tearDown(self):
        craz()


class IplotTests(unittest.TestCase):

    @unittest.skipUnless(False, "Test not implemented")
    def test_iplot(self):
        # TODO: Implement the test
        pass

    def tearDown(self):
        craz()


class GetLevsTests(unittest.TestCase):

    @unittest.skipUnless(False, "Test not implemented")
    def test_getLevs(self):
        # TODO: Implement the test
        pass

    def tearDown(self):
        craz()


class VerticalAverageTests(unittest.TestCase):

    @unittest.skipUnless(False, "Test not implemented")
    def test_vertical_average(self):
        # TODO: Implement the test
        pass

    def tearDown(self):
        craz()


class ImplotTests(unittest.TestCase):

    @unittest.skipUnless(False, "Test not implemented")
    def test_implot(self):
        # TODO: Implement the test
        pass

    def tearDown(self):
        craz()


class DiffRegridTests(unittest.TestCase):

    @unittest.skipUnless(False, "Test not implemented")
    def test_diff_regrid(self):
        # TODO: Implement the test
        pass

    def tearDown(self):
        craz()


class DiffRegridnTests(unittest.TestCase):

    @unittest.skipUnless(False, "Test not implemented")
    def test_diff_regridn(self):
        # TODO: Implement the test
        pass

    def tearDown(self):
        craz()


class TableauTests(unittest.TestCase):

    def setUp(self):
        def my_table_test_function(table, ncol, nlin):
            test = len(table) == nlin
            if test:
                list_table_ncol = [len(lin) for lin in table]
                test = min(list_table_ncol) == max(list_table_ncol) and list_table_ncol[0] == ncol
            if test:
                list_value_is_none = list()
                for lin in table:
                    list_value_is_none += [val is None for val in lin]
                test = not(False in list_value_is_none)
            return test
        self.my_table_test_function = my_table_test_function

    def test_tableau(self):
        my_table = tableau()
        self.assertTrue(self.my_table_test_function(my_table, 1, 1))
        my_table = tableau(n_lin=5)
        self.assertTrue(self.my_table_test_function(my_table, 1, 5))
        my_table = tableau(n_col=5)
        self.assertTrue(self.my_table_test_function(my_table, 5, 1))
        my_table = tableau(8, 2)
        self.assertTrue(self.my_table_test_function(my_table, 2, 8))

    def tearDown(self):
        craz()


class AnnualCycleTests(unittest.TestCase):

    @unittest.skipUnless(False, "Test not implemented")
    def test_annual_cycle(self):
        # TODO: Implement the test
        pass

    def tearDown(self):
        craz()


class ClimAverageTests(unittest.TestCase):

    @unittest.skipUnless(False, "Test not implemented")
    def test_clim_average(self):
        # TODO: Implement the test
        pass

    def tearDown(self):
        craz()


class ClimAverageFastTests(unittest.TestCase):

    @unittest.skipUnless(False, "Test not implemented")
    def test_clim_average_fast(self):
        # TODO: Implement the test
        pass

    def tearDown(self):
        craz()


class SummaryTests(unittest.TestCase):

    @unittest.skipUnless(False, "Test not implemented")
    def test_summary(self):
        # TODO: Implement the test
        pass

    def tearDown(self):
        craz()


class ProjectsTests(unittest.TestCase):

    @unittest.skipUnless(False, "Test not implemented")
    def test_projects(self):
        # TODO: Implement the test
        pass

    def tearDown(self):
        craz()


class lonlatvertInterpolationTests(unittest.TestCase):

    @unittest.skipUnless(False, "Test not implemented")
    def test_lonlatvert_interpolation(self):
        # TODO: Implement the test
        pass

    def tearDown(self):
        craz()


class ZonmeanInterpolationTests(unittest.TestCase):

    @unittest.skipUnless(False, "Test not implemented")
    def test_zonmean_interpolation(self):
        # TODO: Implement the test
        pass

    def tearDown(self):
        craz()


class ZonmeanTests(unittest.TestCase):

    @unittest.skipUnless(False, "Test not implemented")
    def test_zonmean(self):
        # TODO: Implement the test
        pass

    def tearDown(self):
        craz()


class DiffZonmeanTests(unittest.TestCase):

    @unittest.skipUnless(False, "Test not implemented")
    def test_diff_zonmean(self):
        # TODO: Implement the test
        pass

    def tearDown(self):
        craz()


class ConvertListToStringTests(unittest.TestCase):

    def setUp(self):
        def my_conversion_function(elt, separator1=",", separator2="|"):
            string = ""
            if isinstance(elt, list):
                new_elt = list()
                for in_elt in elt:
                    if isinstance(in_elt, list):
                        new_elt.append(separator2.join([str(inner_elt) for inner_elt in in_elt]))
                    else:
                        # TODO: Raise an exception if it is not a string
                        new_elt.append(str(in_elt))
                return separator1.join(new_elt)
            else:
                # TODO: Raise an exception if it is not a string
                return elt
        self.my_conversion_function = my_conversion_function

    @unittest.expectedFailure
    def test_convert_list_to_string(self):
        # TODO: Find out what this function should do...
        self.assertEqual(convert_list_to_string("toto"), self.my_conversion_function("toto"))
        my_list = ["toto", 1, dict(a_key="a_value", an_other_key=8), [("8", 6), "an_other_value"]]
        self.assertEqual(convert_list_to_string(my_list), self.my_conversion_function(my_list))

    def tearDown(self):
        craz()


class TsPlotTests(unittest.TestCase):

    @unittest.skipUnless(False, "Test not implemented")
    def test_ts_plot(self):
        # TODO: Implement the test
        pass

    def tearDown(self):
        craz()


class IplotMembersTests(unittest.TestCase):

    @unittest.skipUnless(False, "Test not implemented")
    def test_iplot_members(self):
        # TODO: Implement the test
        pass

    def tearDown(self):
        craz()


if __name__ == '__main__':
    # Jump into the test directory
    tmp_directory = "/".join([os.environ["HOME"], "tmp", "tests", "test_functions"])
    remove_dir_and_content(tmp_directory)
    if not os.path.isdir(tmp_directory):
        os.makedirs(tmp_directory)
    setNewUniqueCache(tmp_directory)
    os.chdir(tmp_directory)
    unittest.main()
