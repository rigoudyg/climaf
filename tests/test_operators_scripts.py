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

from climaf.cache import setNewUniqueCache, craz
from climaf.operators import scriptFlags


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
