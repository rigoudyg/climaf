#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Test based on examples/index_html.py
"""

import os
import shutil
import unittest

from tests.tools_for_tests import remove_dir_and_content, compare_html_files

from climaf.cache import setNewUniqueCache
from climaf import __path__ as cpath
from climaf.api import ccdo, select, time_average, plot, cfile, ds, craz
from climaf.html import header, section, vspace, link_on_its_own_line, line, open_table, close_table, open_line, \
    close_line, cell, fline, flines, trailer
from climaf import cachedir


if not isinstance(cpath, list):
    cpath = cpath.split(os.sep)

exp = 'AMIPV6ALB2G'
period = "1980"


def my_slice(var, season):
    dats = ds(project='example', simulation=exp, variable=var, frequency='monthly', period=period)
    zonal_mean = ccdo(dats, operator="zonmean")
    if season != "ANN":
        months = {"DJF": "12,1,2", "MAM": "3,4,5", "JJA": "6,7,8", "SON": "9,10,11"}
        dat_season = select(zonal_mean, operator="selmon," + months[season])
    else:
        dat_season = zonal_mean
    toplot = time_average(dat_season)
    return cfile(plot(toplot, title=var + " " + exp + " " + period + " " + season))


class HtmlIndexCreation(unittest.TestCase):

    def setUp(self):
        self.reference_directory = os.sep.join(cpath + ["..", "tests", "reference_data", "test_index_html"])
        self.reference_index_1 = os.sep.join([self.reference_directory, "index_1.html"])
        self.reference_index_2 = os.sep.join([self.reference_directory, "index_2.html"])

    def test_html_index_1(self):
        # Start the index
        #######################
        # index is a string which will accumulate the content of the html index
        # and will be written to some file at the end
        index = header("CliMAF ATLAS of " + exp + " for " + period)
        index += section("Example of Section level 3 header ", level=3)
        index += section("Meridional profiles (level 4)", level=4, key="Slice")
        index += vspace(2)
        # Basics : Create a line of links to pre-existing figure files
        ################################################################
        # Very basic : create a link to a some figure file
        my_figure = cpath[0] + '/../doc/Logo-CliMAF-compact.png'
        index += link_on_its_own_line("A simple link, here to CliMAF logo ", my_figure)
        # Next, create a line of links to figures
        index += line([("link_label1", my_figure),
                       ("link_label2", "fig2.ps"),
                       "Here, a text with no link"],
                      title="The text of 1st column     ")
        index += vspace(3)
        # Define a first table : only two lines, for two variables, with seasons as columns
        #################################################################################
        index += open_table()
        # First method for creating a line : by calling 'cell' function which creates
        # several cells with the same structure. We also illustrate here various ways
        # to control the size of a thumbnail (fixed) image, and of the image which shows
        # when the mouse passes over the link label or thumbnail
        index += open_line('Surface temperature') + \
                 cell('DJF', my_slice('tas', 'DJF'), thumbnail=60) + \
                 cell('MAM', my_slice('tas', 'MAM'), thumbnail="60*60", hover=True) + \
                 cell('JJA', my_slice('tas', 'JJA'), thumbnail="60x60", hover="200x200") + \
                 close_line()
        # Second way to create the line of html links ; using climaf.html.fline() with three args:
        #  - the function (here 'my_slice') called for each column
        #  - a common value for first arg to my_slice,
        #  - and a list of values for second arg (one for each column)
        index += fline(my_slice, 'rst', ['ANN', 'DJF', 'JJA'], title="Surface temperature",
                       thumbnail=40)
        index += close_table()
        index += vspace(3)
        # Power user : iterate automatically with variables as lines, seasons as columns
        #################################################################################
        # For creating a table , with a line showing column titles, and iterating
        # over lines changing values of first arg to the function (here: the variable name),
        # use function 'flines', which loops on the list provided as second arg (it can also be a
        # dict with similar keys and which values are line titles)
        seasons = {'Year': 'ANN', 'Winter': 'DJF'}
        index += open_table(title='variable/season', columns=seasons.keys(), spacing=5)
        lvars = {
            "rst": "short wave at top ",
            "ta": " upper air temp"}
        index += flines(my_slice, lvars, seasons.values(), thumbnail=60)
        # (Argument thumbnail allows to control the size of the small image displayed
        # instead of a labelled link)
        index += close_table()
        # Close the index
        index += trailer()
        # Write it to some file. Launch firefox to display it
        out = "./index_example_1.html"
        absout = os.path.abspath(os.path.expanduser(out))
        with open(absout, "w") as filout:
            filout.write(index)
        # Check that the result corresponds to what is expected
        ########################################################
        self.assertTrue(compare_html_files(absout, self.reference_index_1))

    def test_html_index_2(self):
        ###################################################################################
        # Next : if we want a transportable atlas, figure files must be
        # created or copied at some place outside CliMAF cache. So, all thos
        # functions in package html which refer to figures allow for an
        # optional argument 'dirname'. The programmer must also take care of
        # writing the index in the same directory An example shows below
        ###################################################################################
        atlas_dir = os.path.expanduser(cachedir + '/../atlas')
        index = header("CliMAF ATLAS of " + exp + " for " + period)
        index += open_table(title='variable/season', columns=['DJF', 'MAM', 'JJA'], spacing=5)
        index += fline(my_slice, 'tas', ['DJF', 'MAM', 'JJA'], title="Surface temperature",
                       thumbnail=60, hover=200, dirname=atlas_dir)
        index += close_table()
        index += trailer()
        out = atlas_dir + "/index_example_2.html"
        with open(out, "w") as filout:
            filout.write(index)
        # Check that the result corresponds to what is expected
        ########################################################
        self.assertTrue(compare_html_files(out, self.reference_index_2))

    def tearDown(self):
        craz()


if __name__ == '__main__':
    # Jump into the test directory
    tmp_directory = "/".join([os.environ["HOME"], "tmp", "tests", "test_index_html"])
    remove_dir_and_content(tmp_directory)
    if not os.path.isdir(tmp_directory):
        os.makedirs(tmp_directory)
    setNewUniqueCache(tmp_directory)
    os.chdir(tmp_directory)
    unittest.main()
    remove_dir_and_content(tmp_directory)
