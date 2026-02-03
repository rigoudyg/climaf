#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test the html module.
"""
from __future__ import print_function, division, unicode_literals, absolute_import


import unittest
import string

from tests.tools_for_tests import remove_dir_and_content
from env.environment import *

from climaf.cache import setNewUniqueCache, craz
from climaf import __file__ as climaf_based_file
from climaf.classes import ds
from climaf.driver import cfile
from climaf.chtml import header, trailer, vspace, section, open_table, close_table, open_line, close_line, link,\
    link_on_its_own_line, cell, line, flines, fline, cinstantiate, compareCompanion, start_line, safe_mode_cfile_plot, \
    Climaf_Html_Error


class HeaderTests(unittest.TestCase):

    def test_header(self):
        template = """
    <?xml version="1.0" encoding="iso-8859-1"?>
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
    "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
    <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="fr">
    <head>
    <title>[ $TITLE ]</title>
    <style type="text/css" media=screen>$STYLE</style>
    </head>
    <body>
    <h1>$TITLE</h1>
    <a href="https://climaf.readthedocs.io/en/master/"><center>CliMAF documentation</center></a>
    <hr/> <!--- this draws a line --->
    """ + "\n"
        cami_css_file = os.path.sep.join(os.path.abspath(climaf_based_file).split(os.path.sep)[:-1] +
                                         ["..", "climaf", "cami_style_css"])
        with open(cami_css_file) as f:
            cami_css_style = f.read()
        cesmep_css_file = os.path.sep.join(os.path.abspath(climaf_based_file).split(os.path.sep)[:-1] +
                                           ["..", "climaf", "cesmep_style_css"])
        with open(cesmep_css_file) as f:
            cesmep_css_style = f.read()
        template = string.Template(template)
        with self.assertRaises(TypeError):
            header()
        with self.assertRaises(IOError):
            header("A title", "my_own_style_css")
        self.assertEqual(header("A header"), template.safe_substitute(STYLE=cami_css_style, TITLE="A header"))
        self.assertEqual(header("A header", style_file=cesmep_css_file),
                         template.safe_substitute(STYLE=cesmep_css_style, TITLE="A header"))

    def tearDown(self):
        craz()


class TrailerTests(unittest.TestCase):

    def test_trailer(self):
        self.assertEqual(trailer(), "</body>\n")

    def tearDown(self):
        craz()


class VspaceTests(unittest.TestCase):

    def test_vspace(self):
        self.assertEqual(vspace(), "<br>\n")
        self.assertEqual(vspace(1), "<br>\n")
        self.assertEqual(vspace(5), "<br>\n<br>\n<br>\n<br>\n<br>\n")

    def tearDown(self):
        craz()


class SectionTests(unittest.TestCase):

    def test_section(self):
        template = "<h$LEVEL><a name=$KEY></a>$TITLE</h$LEVEL>\n"
        template = string.Template(template)
        with self.assertRaises(TypeError):
            section()
        self.assertEqual(section("A title"), template.safe_substitute(TITLE="A title", LEVEL=1, KEY='"None"'))
        self.assertEqual(section("A title", level=5),
                         template.safe_substitute(TITLE="A title", LEVEL=5, KEY='"None"'))
        self.assertEqual(section("A title", key="a key"),
                         template.safe_substitute(TITLE="A title", LEVEL=1, KEY='"a key"'))
        self.assertEqual(section("A title", level=5, key="a key"),
                         template.safe_substitute(TITLE="A title", LEVEL=5, KEY='"a key"'))

    def tearDown(self):
        craz()


class OpenTableTests(unittest.TestCase):

    def test_open_table(self):
        template = "<TABLE CELLSPACING=$SPACING>\n <TR>\n <TH ALIGN=LEFT> $TITLE </TH> \n$COLUMNS</TR> \n"
        template = string.Template(template)
        template_columns = '<TD ALIGN=RIGHT>$LABEL</TD>\n'
        template_columns = string.Template(template_columns)
        self.assertEqual(open_table(), template.safe_substitute(SPACING=5, TITLE="", COLUMNS=""))
        self.assertEqual(open_table(title="A title"), template.safe_substitute(SPACING=5, TITLE="A title", COLUMNS=""))
        self.assertEqual(open_table(spacing=8), template.safe_substitute(SPACING=8, TITLE="", COLUMNS=""))
        self.assertEqual(open_table(columns=["a column", ]),
                         template.safe_substitute(SPACING=5, TITLE="",
                                                  COLUMNS=template_columns.safe_substitute(LABEL="a column")))
        self.assertEqual(open_table(columns=["a column", "an other one"]),
                         template.safe_substitute(SPACING=5, TITLE="",
                                                  COLUMNS="".join([template_columns.safe_substitute(LABEL=lab)
                                                                   for lab in ["a column", "an other one"]])))
        self.assertEqual(open_table(columns=["a column", "an other one"], title="A title", spacing=9),
                         template.safe_substitute(SPACING=9, TITLE="A title",
                                                  COLUMNS="".join([template_columns.safe_substitute(LABEL=lab)
                                                                   for lab in ["a column", "an other one"]])))

    def tearDown(self):
        craz()


class CloseTableTests(unittest.TestCase):

    def test_close_table(self):
        self.assertEqual(close_table(), "</TABLE>\n")

    def tearDown(self):
        craz()


class OpenLineTests(unittest.TestCase):

    def test_open_line(self):
        template = " <TR>\n <TH ALIGN=LEFT> <li>$TITLE</li> </TH> \n"
        template = string.Template(template)
        self.assertEqual(open_line(), template.safe_substitute(TITLE=""))
        self.assertEqual(open_line("A title"), template.safe_substitute(TITLE="A title"))

    def tearDown(self):
        craz()


class CloseLineTests(unittest.TestCase):

    def test_close_line(self):
        self.assertEqual(close_line(), ' </TR>\n')

    def tearDown(self):
        craz()


class LinkTests(unittest.TestCase):

    def test_not_run(self):
        with self.assertRaises(TypeError):
            link()
        with self.assertRaises(TypeError):
            link(thumbnail=60)
        with self.assertRaises(TypeError):
            link("a label")

    def test_link_filename_None(self):
        label = "A label"
        self.assertEqual(link(label, filename=None), label)
        self.assertEqual(link(label, filename=None, thumbnail=60), label)
        self.assertEqual(link(label, filename=None, hover="80*80"), label)

    def test_link_thumbnail_not_None_hover_False(self):
        template = '<A HREF="$FILENAME"><IMG HEIGHT=$THUMBNAIL_HEIGHT WIDTH=$THUMBNAIL_WIDTH SRC="$FILENAME"></a>'
        template = string.Template(template)
        self.assertEqual(link(label="A label", filename="A filename", thumbnail=80, hover=False),
                         template.safe_substitute(FILENAME="A filename", THUMBNAIL_WIDTH=80, THUMBNAIL_HEIGHT=80))
        self.assertEqual(link(label="A label", filename="A filename", thumbnail="100*300", hover=False),
                         template.safe_substitute(FILENAME="A filename", THUMBNAIL_WIDTH=100, THUMBNAIL_HEIGHT=300))
        self.assertEqual(link(label="A label", filename="A filename", thumbnail="100x300", hover=False),
                         template.safe_substitute(FILENAME="A filename", THUMBNAIL_WIDTH=100, THUMBNAIL_HEIGHT=300))
        self.assertEqual(link(label="A label", filename="A filename", thumbnail="100m300", hover=False),
                         template.safe_substitute(FILENAME="A filename", THUMBNAIL_WIDTH=None, THUMBNAIL_HEIGHT=None))

    def test_link_thumbnail_not_None_hover_not_False(self):
        template = '<A class="info" HREF="$FILENAME">' \
                   '<IMG HEIGHT=$THUMBNAIL_HEIGHT WIDTH=$THUMBNAIL_WIDTH SRC="$FILENAME">' \
                   '<span>' \
                   '<IMG HEIGHT=$HOVER_HEIGHT WIDTH=$HOVER_WIDTH SRC="$FILENAME"/>' \
                   '</span></a>'
        template = string.Template(template)
        self.assertEqual(link(label="A label", filename="A filename", thumbnail=80, hover=True),
                         template.safe_substitute(FILENAME="A filename", THUMBNAIL_WIDTH=80, THUMBNAIL_HEIGHT=80,
                                                  HOVER_WIDTH=240, HOVER_HEIGHT=240))
        self.assertEqual(link(label="A label", filename="A filename", thumbnail="100*150", hover=True),
                         template.safe_substitute(FILENAME="A filename", THUMBNAIL_WIDTH=100, THUMBNAIL_HEIGHT=150,
                                                  HOVER_WIDTH=300, HOVER_HEIGHT=450))
        with self.assertRaises(Climaf_Html_Error):
            link(label="A label", filename="A filename", thumbnail="100*150", hover="a hover")
        self.assertEqual(link(label="A label", filename="A filename", thumbnail="100*150", hover="200*300"),
                         template.safe_substitute(FILENAME="A filename", THUMBNAIL_WIDTH=100, THUMBNAIL_HEIGHT=150,
                                                  HOVER_WIDTH=200, HOVER_HEIGHT=300))
        self.assertEqual(link(label="A label", filename="A filename", thumbnail="100*150", hover="200x300"),
                         template.safe_substitute(FILENAME="A filename", THUMBNAIL_WIDTH=100, THUMBNAIL_HEIGHT=150,
                                                  HOVER_WIDTH=200, HOVER_HEIGHT=300))
        with self.assertRaises(Climaf_Html_Error):
            link(label="A label", filename="A filename", thumbnail="100*150", hover="200m300")

    def test_link_thumbnail_None_hover_False(self):
        template = '<A HREF="$FILENAME">$LABEL</a>'
        template = string.Template(template)
        self.assertEqual(link(label="A label", filename="A filename", thumbnail=None, hover=False),
                         template.safe_substitute(FILENAME="A filename", LABEL="A label"))

    def test_link_thumbnail_None_hover_not_False(self):
        template = '<A class="info" HREF="$FILENAME">$LABEL<span>' \
                   '<IMG HEIGHT=$HOVER_HEIGHT WIDTH=$HOVER_WIDTH SRC="$FILENAME"/></span></a>'
        template = string.Template(template)
        self.assertEqual(link(label="A label", filename="A filename", thumbnail=None, hover=True),
                         template.safe_substitute(FILENAME="A filename", HOVER_WIDTH=200, HOVER_HEIGHT=200,
                                                  LABEL="A label"))
        self.assertEqual(link(label="A label", filename="A filename", thumbnail=None, hover="80"),
                         template.safe_substitute(FILENAME="A filename", HOVER_WIDTH=80, HOVER_HEIGHT=80,
                                                  LABEL="A label"))
        with self.assertRaises(Climaf_Html_Error):
            link(label="A label", filename="A filename", thumbnail=None, hover="a hover")
        self.assertEqual(link(label="A label", filename="A filename", thumbnail=None, hover="200*300"),
                         template.safe_substitute(FILENAME="A filename", HOVER_WIDTH=200, HOVER_HEIGHT=300,
                                                  LABEL="A label"))
        self.assertEqual(link(label="A label", filename="A filename", thumbnail=None, hover="200x300"),
                         template.safe_substitute(FILENAME="A filename", HOVER_WIDTH=200, HOVER_HEIGHT=300,
                                                  LABEL="A label"))
        with self.assertRaises(Climaf_Html_Error):
            link(label="A label", filename="A filename", thumbnail=None, hover="200m300")

    def tearDown(self):
        craz()


class LinkOnItsOwnLineTests(unittest.TestCase):

    def test_link_on_its_own_line(self):
        self.assertEqual(link_on_its_own_line("A label", "A filename"),
                         open_line() + link("A label", "A filename", thumbnail=None, hover=True) + close_line())
        self.assertEqual(link_on_its_own_line("A label", "A filename", thumbnail="800*500"),
                         open_line() + link("A label", "A filename", thumbnail="800x500", hover=True) + close_line())
        self.assertEqual(link_on_its_own_line("A label", "A filename", hover=80),
                         open_line() + link("A label", "A filename", thumbnail=None, hover=200) + close_line())
        self.assertEqual(link_on_its_own_line("A label", "A filename", thumbnail=150, hover=80),
                         open_line() + link("A label", "A filename", thumbnail=150, hover=80) + close_line())

    def tearDown(self):
        craz()


class CellTests(unittest.TestCase):

    def setUp(self):
        template = '<TD ALIGN=RIGHT>$LINK</TD>\n'
        template = string.Template(template)
        self.test_template = template
        my_dataset = ds(project="example", simulation="AMIPV6ALB2G", variable="tas", period="1980-1981")
        self.test_filename = cfile(my_dataset)
        from climaf import cachedir
        self.test_cachedir = cachedir
        self.test_altdir = "/home/common/tmp/cache/all/climaf"
        self.test_label = "A label"
        self.changed_filename = self.test_filename.replace(self.test_cachedir, self.test_altdir)
        self.test_dirname = os.sep.join([os.environ["HOME"], "tmp", "cache", "climaf"])

    def test_cell_not_work(self):
        with self.assertRaises(TypeError):
            cell()

    def test_cell_dirname_None(self):
        self.assertEqual(cell(self.test_label, filename=self.test_filename),
                         self.test_template.safe_substitute(
                             LINK=link(self.test_label, self.test_filename, None, True)))
        self.assertEqual(cell(self.test_label, filename=self.test_filename, altdir=self.test_altdir),
                         self.test_template.safe_substitute(
                             LINK=link(self.test_label, self.changed_filename, None, True)))

    def test_cell_dirname_not_None_filename_None(self):
        self.assertEqual(cell(self.test_label, filename=None, dirname=self.test_dirname),
                         self.test_template.safe_substitute(LINK=link(self.test_label, None, None, True)))
        self.assertTrue(os.path.exists(self.test_dirname) and os.path.isdir(self.test_dirname))

    @unittest.expectedFailure
    def test_cell_dirname_not_None_filename_not_None(self):
        # TODO : Correct this test or change CliMAF to have reproducibility (but is it what we want to?)
        self.assertEqual(cell(self.test_label, filename=self.test_filename, dirname=self.test_dirname),
                         self.test_template.safe_substitute(LINK=""))
        self.assertTrue(os.path.exists(self.test_dirname) and os.path.isdir(self.test_dirname))

    def tearDown(self):
        craz()


class LineTests(unittest.TestCase):

    def test_line(self):
        with self.assertRaises(TypeError):
            line([("a key", "a value"), "a value", ["some list", "of several objects"]], "A title")
        with self.assertRaises(TypeError):
            line([("a key", 8), "a value", ("some value", "with figure")], "A title")
        list_of_pairs = [("a key", "a value"), "a value", ("some value", "with figure")]
        rep = open_line() + "A title" + cell("a key", "a value") + cell("a value", None) + \
              cell("some value", "with figure") + close_line()
        self.assertEqual(line(list_of_pairs, "A title"), rep)

    def tearDown(self):
        craz()


class FlineTests(unittest.TestCase):

    def test_fline(self):
        def my_func(*args):
            print(args)
            return str(args)

        rep = fline(my_func, 'COD', ['EurNland', 'EurSland', 'AtlOce', 'MedSea'], title="Seasonal cycle (1)",
                    common_args=['AERmon', [{'id': 'MODIS',
                                             'name': 'MODIS',
                                             'ignore': ['EUC12', 'Scplains'],
                                             'period': '2003-2018',
                                             'var': 'Cloud_Optical_Thickness_Combined_Mean_Mean'}], True],
                    other_args={'EurNland': ['blue black black black black black black', '0 0 2 16 5 13 15', 0, 40],
                                'EurSland': ['blue black black black black black black', '0 0 2 16 5 13 15', 0, 40],
                                'AtlOce': ['blue black black black black black black', '0 0 2 16 5 13 15', 0, 40],
                                'MedSea': ['blue black black black black black black', '0 0 2 16 5 13 15', 0, 40]})
        reference_rep = " <TR>\n" \
                        " <TH ALIGN=LEFT> <li>Seasonal cycle (1)</li> </TH> \n" \
                        "<TD ALIGN=RIGHT>('COD', 'EurNland', 'AERmon', [{'id': 'MODIS', 'name': 'MODIS', 'ignore': " \
                        "['EUC12', 'Scplains'], 'period': '2003-2018', 'var': " \
                        "'Cloud_Optical_Thickness_Combined_Mean_Mean'}], True, " \
                        "'blue black black black black black black', '0 0 2 16 5 13 15', 0, 40)</TD>\n" \
                        "<TD ALIGN=RIGHT>('COD', 'EurSland', 'AERmon', [{'id': 'MODIS', 'name': 'MODIS', 'ignore': " \
                        "['EUC12', 'Scplains'], 'period': '2003-2018', 'var': " \
                        "'Cloud_Optical_Thickness_Combined_Mean_Mean'}], True, " \
                        "'blue black black black black black black', '0 0 2 16 5 13 15', 0, 40)</TD>\n" \
                        "<TD ALIGN=RIGHT>('COD', 'AtlOce', 'AERmon', [{'id': 'MODIS', 'name': 'MODIS', 'ignore': " \
                        "['EUC12', 'Scplains'], 'period': '2003-2018', 'var': " \
                        "'Cloud_Optical_Thickness_Combined_Mean_Mean'}], True, " \
                        "'blue black black black black black black', '0 0 2 16 5 13 15', 0, 40)</TD>\n" \
                        "<TD ALIGN=RIGHT>('COD', 'MedSea', 'AERmon', [{'id': 'MODIS', 'name': 'MODIS', 'ignore': " \
                        "['EUC12', 'Scplains'], 'period': '2003-2018', 'var': " \
                        "'Cloud_Optical_Thickness_Combined_Mean_Mean'}], True, " \
                        "'blue black black black black black black', '0 0 2 16 5 13 15', 0, 40)</TD>\n " \
                        "</TR>\n"
        self.assertEqual(rep, reference_rep)

    def tearDown(self):
        craz()


class FlinesTests(unittest.TestCase):

    @unittest.skipUnless(False, "Not implemented")
    def test_flines(self):
        # TODO: Implement the tests
        pass

    def tearDown(self):
        craz()


class CinstantiateTests(unittest.TestCase):

    @unittest.skipUnless(False, "Not implemented")
    def test_cinstantiate(self):
        # TODO: Implement the tests
        pass

    def tearDown(self):
        craz()


class CompareCompanionTests(unittest.TestCase):

    def test_compareCompanion(self):
        rep = ' <script type="text/javascript" ' \
              'src="https://cdnjs.cloudflare.com/ajax/libs/require.js/2.2.0/require.min.js">' \
              '</script>\n <script type="text/javascript" ' \
              'src="https://cdn.rawgit.com/PBrockmann/compareCompanion/master/compareCompanion.js"></script> \n'
        self.assertEqual(compareCompanion(), rep)

    def tearDown(self):
        craz()


class StartLineTests(unittest.TestCase):

    def test_start_line(self):
        with self.assertRaises(TypeError):
            start_line()
        self.assertEqual(start_line("A title"), open_table() + open_line("A title") + close_line() + close_table() +
                         open_table() + open_line())

    def tearDown(self):
        craz()


class SafeModeCfilePlotTests(unittest.TestCase):

    @unittest.skipUnless(False, "Not implemented")
    def test_safe_mode_cfile_plot(self):
        # TODO: Implement the tests
        pass

    def tearDown(self):
        craz()


if __name__ == '__main__':
    # Jump into the test directory
    tmp_directory = "/".join([os.environ["HOME"], "tmp", "tests", "test_html"])
    remove_dir_and_content(tmp_directory)
    if not os.path.isdir(tmp_directory):
        os.makedirs(tmp_directory)
    setNewUniqueCache(tmp_directory)
    os.chdir(tmp_directory)
    unittest.main()
