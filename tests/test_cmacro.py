#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test the cmacro module.
"""
from __future__ import print_function, division, unicode_literals, absolute_import


import os
import unittest

from tests.tools_for_tests import remove_dir_and_content
from env.environment import *
from climaf.cache import setNewUniqueCache
from climaf.api import *
from climaf.classes import ctree, cdummy, scriptChild
from climaf.cmacro import macro, crewrite, cmatch, read, write, show, instantiate, Climaf_Macro_Error


class MacroTests(unittest.TestCase):

    def test_unexisting_project(self):
        crstest = "plot(ccdo(llbox(ds('toto|AMIPV6ALB2G|ta|198001|global|monthly')," \
                  "latmax=60,latmin=40,lonmax=25,lonmin=-15),operator='zonmean'))"
        my_macro = macro("a_macro", crstest)
        self.assertIsNone(my_macro)

    def test_simple(self):
        january_ta = ds(project='example', simulation='AMIPV6ALB2G', variable='ta', frequency='monthly',
                        period='198001')
        ta_europe = llbox(january_ta, latmin=40,
                          latmax=60, lonmin=-15, lonmax=25)
        ta_ezm = ccdo(ta_europe, operator='zonmean')
        fig_ezm = plot(ta_ezm)
        my_macro = macro('eu_cross_section', fig_ezm)
        self.assertEqual(cmacros["eu_cross_section"].buildcrs(),
                         "plot(ccdo(llbox(ARG,latmax=60,latmin=40,lonmax=25,lonmin=-15),operator='zonmean'))")
        self.assertEqual(cmacros["eu_cross_section"].buildcrs().replace("ARG", january_ta.buildcrs()),
                         fig_ezm.buildcrs())
        self.assertIn("eu_cross_section", globals())
        import sys
        self.assertIn("eu_cross_section", sys.modules["__main__"].__dict__)
        self.assertTrue(isinstance(my_macro, ctree))
        self.assertEqual(my_macro.buildcrs(),
                         "plot(ccdo(llbox(ARG,latmax=60,latmin=40,lonmax=25,lonmin=-15),operator='zonmean'))")
        pr = ds(project='example', simulation='AMIPV6ALB2G',
                variable='pr', frequency='monthly', period='198001')
        pr_ezm = eu_cross_section(pr)
        self.assertEqual(cmacros["eu_cross_section"].buildcrs().replace(
            "ARG", pr.buildcrs()), pr_ezm.buildcrs())

    def test_lobjects(self):
        january_ta = ds(project='example', simulation='AMIPV6ALB2G', variable='ta', frequency='monthly',
                        period='198001')
        mean_january_ta = time_average(january_ta)
        my_bias = minus(january_ta, mean_january_ta)
        my_macro = macro("my_bias", my_bias, [mean_january_ta, ])
        self.assertTrue(isinstance(my_macro, ctree))
        self.assertEqual(my_macro.buildcrs(), 'minus(ARG,time_average(ARG))')

    def test_cdummy(self):
        my_object = cdummy()
        my_macro = macro("a_macro", my_object)
        self.assertTrue(isinstance(my_macro, cdummy))
        self.assertEqual(my_macro.buildcrs(), "ARG")

    def test_dataset(self):
        january_ta = ds(project='example', simulation='AMIPV6ALB2G', variable='ta', frequency='monthly',
                        period='198001')
        my_macro = macro("a_macro", january_ta)
        self.assertTrue(isinstance(my_macro, cdummy))
        self.assertEqual(my_macro.buildcrs(), "ARG")

    def test_none(self):
        my_object = None
        my_macro = macro("a_macro", my_object)
        self.assertIsNone(my_macro)

    def test_cscript(self):
        cscript('mycdo', 'cdo ${operator} ${in} ${out_1} ${out_2}')
        january_ta = ds(project='example', simulation='AMIPV6ALB2G', variable='ta', frequency='monthly',
                        period='198001')
        ta_ezm = mycdo(january_ta, operator='zonmean')
        my_macro = macro("a_macro", ta_ezm.outputs["2"])
        self.assertTrue(isinstance(my_macro, scriptChild))
        self.assertEqual(my_macro.buildcrs(),
                         "mycdo(ARG,operator='zonmean').2")

    def test_cpage(self):
        tas_ds = ds(project='example', simulation='AMIPV6ALB2G',
                    variable='tas', period='1980-1981')
        tas_avg = time_average(tas_ds)
        fig = plot(tas_avg, title='title')
        my_page = cpage([[None, fig], [fig, fig], [fig, fig]], widths=[0.2, 0.8],
                        heights=[0.33, 0.33, 0.33], fig_trim=False, page_trim=False,
                        format='pdf', title='Page title', x=10, y=20, ybox=45,
                        pt=20, font='DejaVu-Sans', gravity='South', background='grey90',
                        page_width=1600., page_height=2400.)
        my_macro = macro("a_macro", my_page)
        self.assertTrue(isinstance(my_macro, cpage))
        self.assertEqual(my_macro.buildcrs(),
                         "cpage([[None,plot(time_average(ARG),title='title')],[plot(time_average(ARG),title='title'),"
                         "plot(time_average(ARG),title='title')],[plot(time_average(ARG),title='title'),"
                         "plot(time_average(ARG),title='title')]],[0.2, 0.8],[0.33, 0.33, 0.33], fig_trim='True', "
                         "page_trim='True', format='png', page_width=1000, page_height=1500)")

    def test_cpage_pdf(self):
        # TODO: Modify CliMAF to allow macros built upon cpage_pdf
        tas_ds = ds(project='example', simulation='AMIPV6ALB2G',
                    variable='tas', period='1980-1981')
        tas_avg = time_average(tas_ds)
        fig = plot(tas_avg, title='title', format='pdf')
        crop_fig = cpdfcrop(fig)
        my_pdfpage = cpage_pdf([[crop_fig, crop_fig], [crop_fig, crop_fig], [crop_fig, crop_fig]],
                               widths=[0.2, 0.8], heights=[0.33, 0.33, 0.33], page_width=800., page_height=1200.,
                               scale=0.95, openright=True, title='Page title', x=-5, y=10, titlebox=True,
                               pt='huge', font='ptm', background='yellow')
        my_macro = macro("a_macro", my_pdfpage)
        self.assertIsNone(my_macro)
        # self.assertTrue(isinstance(my_macro, cpage_pdf))
        # self.assertEqual(my_macro.buildcrs(), "cpage([[None,plot(time_average(ARG),title='title')],
        #                 [plot(time_average(ARG),title='title'),plot(time_average(ARG),title='title')],
        #                 [plot(time_average(ARG),title='title'),plot(time_average(ARG),title='title')]],
        #                 [0.2, 0.8],[0.33, 0.33, 0.33], fig_trim='True', page_trim='True', format='png',
        #                 page_width=1000, page_height=1500)")

    def test_cens(self):
        cdef('project', 'example')
        cdef('simulation', "AMIPV6ALB2G")
        cdef('variable', 'tas')
        cdef('frequency', 'monthly')
        ds1980 = ds(period="1980")
        ds1981 = ds(period="1981")
        myens = cens({'1980': ds1980, '1981': ds1981})
        my_macro = macro("a_macro", myens)
        self.assertTrue(isinstance(my_macro, cens))
        self.assertEqual(my_macro.buildcrs(), "cens({'1980':ARG,'1981':ARG})")

    def tearDown(self):
        craz()


class CrewriteTests(unittest.TestCase):

    def test_crewrite(self):
        crstest_1 = "plot(ccdo(llbox(ds('toto|AMIPV6ALB2G|ta|198001|global|monthly'),latmax=60,latmin=40,lonmax=25," \
                    "lonmin=-15),operator='zonmean'))"
        new_crstest_1 = crewrite(crstest_1)
        self.assertEqual(new_crstest_1,
                         "plot(ccdo(llbox(latmax=60,latmin=40,lonmax=25,lonmin=-15),operator='zonmean'))")
        crstest_2 = "plot(ccdo(llbox(ds('example|AMIPV6ALB2G|ta|198001|global|monthly'),latmax=60,latmin=40," \
                    "lonmax=25,lonmin=-15),operator='zonmean'))"
        new_crstest_2 = crewrite(crstest_2)
        self.assertEqual(new_crstest_2,
                         "plot(ccdo(llbox(ds('example|AMIPV6ALB2G|ta|198001|global|monthly'),latmax=60,latmin=40,"
                         "lonmax=25,lonmin=-15),operator='zonmean'))")
        new_crstest_3 = crewrite(crstest_2, alsoAtTop=False)
        self.assertEqual(new_crstest_3,
                         "plot(ccdo(llbox(ds('example|AMIPV6ALB2G|ta|198001|global|monthly'),latmax=60,latmin=40,"
                         "lonmax=25,lonmin=-15),operator='zonmean'))")
        january_ta1 = ds(project='example', simulation='AMIPV6ALB2G', variable='ta', frequency='monthly',
                         period='198001')
        january_ta2 = ds(project='example', simulation='AMIPV6ALB2G', variable='ta', frequency='monthly',
                         period='19800101')
        january_ta = minus(january_ta1, january_ta2)
        ta_europe = llbox(january_ta, latmin=40,
                          latmax=60, lonmin=-15, lonmax=25)
        ta_ezm = ccdo(ta_europe, operator='zonmean')
        fig_ezm = plot(ta_ezm, format="eps")
        my_macro = macro('eu_cross_section', fig_ezm, [january_ta2, ])
        my_crewrite = crewrite(fig_ezm.buildcrs())
        self.assertEqual(my_crewrite,
                         "eu_cross_section(ds('example|AMIPV6ALB2G|ta|198001|global|monthly'),"
                         "ds('example|AMIPV6ALB2G|ta|19800101|global|monthly'))")

    def tearDown(self):
        craz()


class CmatchTests(unittest.TestCase):

    @unittest.expectedFailure
    def test_script_child(self):
        # TODO: Check where argslist comes from...
        cscript('mycdo', 'cdo ${operator} ${in} ${out_1} ${out_2}')
        january_ta = ds(project='example', simulation='AMIPV6ALB2G', variable='ta', frequency='monthly',
                        period='198001')
        ta_ezm = mycdo(january_ta, operator='zonmean')
        my_macro = macro("a_macro", ta_ezm.outputs["2"])
        cmatch_result = cmatch(my_macro, ta_ezm)
        self.assertEqual(cmatch_result, [])
        cmatch_result = cmatch(my_macro, ta_ezm.outputs["1"])
        self.assertEqual(cmatch_result, [])
        cmatch_result = cmatch(my_macro, ta_ezm.outputs["2"])
        self.assertEqual(cmatch_result, [])

    def test_ctree(self):
        january_ta1 = ds(project='example', simulation='AMIPV6ALB2G', variable='ta', frequency='monthly',
                         period='198001')
        january_ta2 = ds(project='example', simulation='AMIPV6ALB2G', variable='ta', frequency='monthly',
                         period='19800101')
        january_ta = minus(january_ta1, january_ta2)
        ta_europe = llbox(january_ta, latmin=40,
                          latmax=60, lonmin=-15, lonmax=25)
        ta_ezm = ccdo(ta_europe, operator='zonmean')
        fig_ezm = plot(ta_ezm, format="eps")
        my_macro = macro('eu_cross_section', fig_ezm, [january_ta2, ])
        cmatch_result = cmatch(my_macro, fig_ezm)
        self.assertEqual(cmatch_result, [january_ta1, january_ta2])
        cmatch_result = cmatch(my_macro, plot(ta_ezm, format="png"))
        self.assertEqual(cmatch_result, [])

    @unittest.expectedFailure
    def test_cpage(self):
        # TODO: Find out where orientation parameter comes from...
        tas_ds = ds(project='example', simulation='AMIPV6ALB2G',
                    variable='tas', period='1980-1981')
        tas_avg = time_average(tas_ds)
        fig = plot(tas_avg, title='title')
        my_page = cpage([[None, fig], [fig, fig], [fig, fig]], widths=[0.2, 0.8],
                        heights=[0.33, 0.33, 0.33], fig_trim=False, page_trim=False,
                        format='pdf', title='Page title', x=10, y=20, ybox=45,
                        pt=20, font='DejaVu-Sans', gravity='South', background='grey90',
                        page_width=1600., page_height=2400.)
        my_macro = macro("a_macro", my_page)
        cmatch_result = cmatch(my_macro, my_page)
        self.assertEqual(cmatch_result, [])

    def tearDown(self):
        craz()


class ReadWriteTests(unittest.TestCase):

    def setUp(self):
        january_ta = ds(project='example', simulation='AMIPV6ALB2G', variable='ta', frequency='monthly',
                        period='198001')
        mean_january_ta = time_average(january_ta)
        my_bias = minus(january_ta, mean_january_ta)
        my_macro = macro("my_bias", my_bias, [mean_january_ta, ])
        self.my_macro_file = os.path.sep.join(
            [tmp_directory, "my_macro_test.json"])
        write(self.my_macro_file)
        del cmacros["my_bias"]
        self.assertNotIn("my_bias", cmacros)

    def test_read(self):
        self.assertNotIn("my_bias", cmacros)
        read("my_macro.txt")
        self.assertNotIn("my_bias", cmacros)
        read(self.my_macro_file)
        self.assertIn("my_bias", cmacros)

    def test_write(self):
        write(self.my_macro_file)
        self.assertTrue(os.path.exists(self.my_macro_file))

    def tearDown(self):
        craz()


class ShowTests(unittest.TestCase):

    @unittest.skipUnless(False, "Improve this test")
    def test_show(self):
        from io import StringIO
        old_stdout = sys.stdout
        result = StringIO()
        sys.stdout = result
        show()
        show(interp=False)
        sys.stdout = old_stdout

    def tearDown(self):
        craz()


class InstantiateTests(unittest.TestCase):

    @unittest.skipUnless(False, "Not implemented")
    def test_instantiate(self):
        pass

    def tearDown(self):
        craz()


if __name__ == '__main__':
    # Jump into the test directory
    tmp_directory = "/".join([os.environ["HOME"],
                             "tmp", "tests", "test_macro"])
    remove_dir_and_content(tmp_directory)
    if not os.path.isdir(tmp_directory):
        os.makedirs(tmp_directory)
    setNewUniqueCache(tmp_directory)
    os.chdir(tmp_directory)
    unittest.main()
