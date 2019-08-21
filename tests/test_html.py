#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Test the html module.
"""

import os
import unittest

from tests.tools_for_tests import remove_dir_and_content

from climaf.cache import setNewUniqueCache
from climaf.html import header, trailer, vspace, section, open_table, close_table, open_line, close_line, link,\
    link_on_its_own_line, cell, line, flines, fline, cinstantiate, compareCompanion, start_line, safe_mode_cfile_plot, \
    Climaf_Html_Error


class HeaderTests(unittest.TestCase):

    @unittest.skipUnless(False, "Not implemented")
    def test_header(self):
        # TODO: Implement the tests
        pass


class TrailerTests(unittest.TestCase):

    @unittest.skipUnless(False, "Not implemented")
    def test_trailer(self):
        # TODO: Implement the tests
        pass


class VspaceTests(unittest.TestCase):

    @unittest.skipUnless(False, "Not implemented")
    def test_vspace(self):
        # TODO: Implement the tests
        pass


class SectionTests(unittest.TestCase):

    @unittest.skipUnless(False, "Not implemented")
    def test_section(self):
        # TODO: Implement the tests
        pass


class OpenTableTests(unittest.TestCase):

    @unittest.skipUnless(False, "Not implemented")
    def test_open_table(self):
        # TODO: Implement the tests
        pass


class CloseTableTests(unittest.TestCase):

    @unittest.skipUnless(False, "Not implemented")
    def test_close_table(self):
        # TODO: Implement the tests
        pass


class OpenLineTests(unittest.TestCase):

    @unittest.skipUnless(False, "Not implemented")
    def test_open_line(self):
        # TODO: Implement the tests
        pass


class CloseLineTests(unittest.TestCase):

    @unittest.skipUnless(False, "Not implemented")
    def test_close_line(self):
        # TODO: Implement the tests
        pass


class LinkTests(unittest.TestCase):

    @unittest.skipUnless(False, "Not implemented")
    def test_link(self):
        # TODO: Implement the tests
        pass


class LinkOnItsOwnLineTests(unittest.TestCase):

    @unittest.skipUnless(False, "Not implemented")
    def test_link_on_its_own_line(self):
        # TODO: Implement the tests
        pass


class CellTests(unittest.TestCase):

    @unittest.skipUnless(False, "Not implemented")
    def test_cell(self):
        # TODO: Implement the tests
        pass


class LineTests(unittest.TestCase):

    @unittest.skipUnless(False, "Not implemented")
    def test_line(self):
        # TODO: Implement the tests
        pass


class FlineTests(unittest.TestCase):

    @unittest.skipUnless(False, "Not implemented")
    def test_fline(self):
        # TODO: Implement the tests
        pass


class FlinesTests(unittest.TestCase):

    @unittest.skipUnless(False, "Not implemented")
    def test_flines(self):
        # TODO: Implement the tests
        pass


class CinstantiateTests(unittest.TestCase):

    @unittest.skipUnless(False, "Not implemented")
    def test_cinstantiate(self):
        # TODO: Implement the tests
        pass


class CompareCompanionTests(unittest.TestCase):

    @unittest.skipUnless(False, "Not implemented")
    def test_compareCompanion(self):
        # TODO: Implement the tests
        pass


class StartLineTests(unittest.TestCase):

    @unittest.skipUnless(False, "Not implemented")
    def test_start_line(self):
        # TODO: Implement the tests
        pass


class SafeModeCfilePlotTests(unittest.TestCase):

    @unittest.skipUnless(False, "Not implemented")
    def test_safe_mode_cfile_plot(self):
        # TODO: Implement the tests
        pass


if __name__ == '__main__':
    # Jump into the test directory
    tmp_directory = "/".join([os.environ["HOME"], "tmp", "tests", "test_macro"])
    remove_dir_and_content(tmp_directory)
    if not os.path.isdir(tmp_directory):
        os.makedirs(tmp_directory)
    setNewUniqueCache(tmp_directory)
    os.chdir(tmp_directory)
    unittest.main()
    remove_dir_and_content(tmp_directory)
