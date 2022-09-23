#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test the period module.
"""
from __future__ import print_function, division, unicode_literals, absolute_import


import os
import unittest
from datetime import datetime, timedelta

from tests.tools_for_tests import remove_dir_and_content
from env.environment import *

from climaf.period import cperiod, Climaf_Period_Error, init_period, sort_periods_list, merge_periods, \
    intersect_periods_list, lastyears, firstyears

from climaf.cache import setNewUniqueCache, craz


class CreatePeriodDefinedTests(unittest.TestCase):

    def test_no_args(self):
        # Test that cperiod needs arguments
        with self.assertRaises(TypeError):
            cperiod()

    def test_fx(self):
        # Test that cperiod can be init with "fx"
        cperiod("fx")
        cperiod("fx", 1850)
        cperiod("fx", pattern="%4d")

    def test_no_datetime(self):
        # Test that cperiod need two datetime objects at least if not "fx"
        with self.assertRaises(Climaf_Period_Error):
            cperiod("1850")
        with self.assertRaises(Climaf_Period_Error):
            cperiod("1850", "1950")
        with self.assertRaises(Climaf_Period_Error):
            cperiod("1850-1950")
        with self.assertRaises(Climaf_Period_Error):
            cperiod(1850, 1950)

    def test_datetime(self):
        date_1 = datetime(1850, 1, 1, 0, 0)
        date_2 = datetime(1950, 12, 31, 23, 59)
        with self.assertRaises(Climaf_Period_Error):
            cperiod(date_1)
        cperiod(date_1, date_2)
        cperiod(datetime(1850, 1, 1, 0, 0), datetime(1950, 12, 31, 23, 59), pattern="%4d")

    def test_order(self):
        # TODO: Modify CliMAF in order to check that the period is in a logic order
        date_1 = datetime(1850, 1, 1, 0, 0)
        date_2 = datetime(1950, 12, 31, 23, 59)
        with self.assertRaises(Climaf_Period_Error):
            cperiod(date_2, date_1)

    def tearDown(self):
        craz()


class CreatePeriodFixedTests(unittest.TestCase):

    def setUp(self):
        self.my_period = cperiod("fx")
        self.my_test_date = datetime(1850, 1, 1, 0, 0)
        self.my_test_period = cperiod(datetime(1850, 1, 1, 0, 0), datetime(1950, 12, 31, 23, 59))

    def test_fx(self):
        self.assertTrue(self.my_period.fx)

    def test_pattern(self):
        self.assertEqual(self.my_period.pattern, "fx")

    def test_start(self):
        with self.assertRaises(AttributeError):
            self.my_period.start

    def test_end(self):
        with self.assertRaises(AttributeError):
            self.my_period.end

    def test_repr(self):
        self.assertEqual(repr(self.my_period), "fx")

    def test_iso(self):
        with self.assertRaises(Climaf_Period_Error):
            self.my_period.iso()

    def test_hasFullYear(self):
        with self.assertRaises(Climaf_Period_Error):
            self.my_period.hasFullYear(self.my_test_date)

    def test_start_with(self):
        self.assertFalse(self.my_period.start_with(self.my_test_period))

    def test_is_before(self):
        self.assertFalse(self.my_period.is_before(self.my_test_period))

    def test_includes(self):
        self.assertFalse(self.my_period.includes(self.my_test_period))

    def test_intersects(self):
        self.assertEqual(self.my_period.intersects(self.my_test_period), self.my_test_period)

    def tearDown(self):
        craz()


class CreatePeriodGenericTests(unittest.TestCase):

    def setUp(self):
        self.my_period = cperiod(datetime(1850, 1, 1, 0), datetime(1950, 12, 31, 23, 59))
        self.my_date_1 = datetime(1850, 1, 1)
        self.my_date_2 = datetime(1950, 12, 31, 23, 59)
        self.my_date_2_60 = self.my_date_2 - timedelta(0, 60)
        self.my_date_3 = datetime(1700, 5, 26)
        self.my_date_4 = datetime(2000, 6, 7)
        self.my_date_5 = datetime(1900, 9, 2)
        self.my_date_6 = datetime(1920, 1, 26, 11)
        self.my_date_7 = datetime(1920, 1, 26)
        self.my_period_1 = cperiod(self.my_date_1, self.my_date_2, pattern=None)

        def a_test_pattern():
            return "a test pattern"

        self.my_period_2 = cperiod(self.my_date_3, self.my_date_5, pattern=a_test_pattern())
        self.my_period_3 = cperiod(self.my_date_5, self.my_date_4)
        self.my_period_4 = cperiod(self.my_date_5, self.my_date_6)
        self.my_period_5 = cperiod(self.my_date_1, self.my_date_5)
        self.my_period_6 = cperiod(self.my_date_3, self.my_date_4)

    def test_fx(self):
        self.assertFalse(self.my_period.fx)

    def test_pattern(self):
        self.assertEqual(self.my_period.pattern, "1850010100-1950123123")
        self.assertEqual(self.my_period_2.pattern, "a test pattern")

    def test_start(self):
        self.assertEqual(self.my_period.start, self.my_date_1)

    def test_end(self):
        self.assertEqual(self.my_period.end, self.my_date_2)

    def test_eq(self):
        self.assertEqual(self.my_period, self.my_period_1)
        self.assertNotEqual(cperiod("fx"), self.my_period)
        self.assertNotEqual(self.my_period_3, self.my_period_4)
        self.assertNotEqual(self.my_period_3, self.my_period_6)

    def test_repr(self):
        self.assertEqual(repr(self.my_period), "1850010100-1950123123")
        self.assertEqual(repr(self.my_period_1), "1850010100-1950123123")
        self.assertEqual(repr(self.my_period_2), "17000526-19000901")

    def test_iso(self):
        self.assertEqual(self.my_period.iso(), ",".join([self.my_date_1.isoformat(), self.my_date_2_60.isoformat()]))

    def test_hasFullYear(self):
        self.assertTrue(self.my_period.hasFullYear(1900))
        self.assertFalse(self.my_period.hasFullYear("1700"))
        self.assertFalse(self.my_period.hasFullYear(2000))
        self.assertFalse(self.my_period.hasFullYear(1950))
        self.assertTrue(self.my_period.hasFullYear(1850))
        self.assertFalse(self.my_period_4.hasFullYear(1920))

    def test_start_with(self):
        self.assertFalse(self.my_period.start_with(self.my_period_2))
        self.assertTrue(self.my_period.start_with(self.my_period_5))
        self.assertTrue(self.my_period.start_with(self.my_period_1))

    def test_is_before(self):
        self.assertTrue(self.my_period_5.is_before(self.my_period_3))
        self.assertFalse(self.my_period.is_before(self.my_period_2))

    def test_includes(self):
        self.assertTrue(self.my_period.includes(self.my_period_1))
        self.assertTrue(self.my_period_6.includes(self.my_period))
        self.assertFalse(self.my_period.includes(self.my_period_6))
        self.assertFalse(self.my_period.includes(self.my_period_2))
        self.assertFalse(self.my_period.includes(self.my_period_3))

    def test_intersects(self):
        self.assertEqual(self.my_period_6.intersects(self.my_period_3), self.my_period_3)
        self.assertEqual(self.my_period.intersects(self.my_period_5), self.my_period_5)
        self.assertEqual(self.my_period_6.intersects(self.my_period), self.my_period)
        self.assertEqual(self.my_period_2.intersects(self.my_period), self.my_period_5)

    def tearDown(self):
        craz()


class InitPeriodTests(unittest.TestCase):

    def test_arg_types(self):
        with self.assertRaises(Climaf_Period_Error):
            init_period(1850)
        with self.assertRaises(TypeError):
            init_period(1850, 1950)
        init_period(cperiod(datetime(1850, 1, 2), datetime(1950, 5, 23)))
        init_period("1850")
        init_period("1500-2000")
        init_period("1500_2000")
        init_period("fx")
        # TODO: Make the null and negative years working well
        with self.assertRaises(Climaf_Period_Error):
            init_period("0000")
        with self.assertRaises(Climaf_Period_Error):
            init_period("-150")
        with self.assertRaises(Climaf_Period_Error):
            init_period("00toto")
        with self.assertRaises(Climaf_Period_Error):
            init_period("195001-185002")
        init_period("1850-19500201")
        with self.assertRaises(Climaf_Period_Error):
            init_period("1950-1850")

    def test_year(self):
        my_period = init_period("1")
        self.assertEqual(my_period.start, datetime(1, 1, 1))
        self.assertEqual(my_period.end, datetime(2, 1, 1))
        my_period = init_period("52")
        self.assertEqual(my_period.start, datetime(52, 1, 1))
        self.assertEqual(my_period.end, datetime(53, 1, 1))
        my_period = init_period("873")
        self.assertEqual(my_period.start, datetime(873, 1, 1))
        self.assertEqual(my_period.end, datetime(874, 1, 1))
        my_period = init_period("1745")
        self.assertEqual(my_period.start, datetime(1745, 1, 1))
        self.assertEqual(my_period.end, datetime(1746, 1, 1))
        my_period = init_period("17452")
        self.assertEqual(my_period.start, datetime(1745, 1, 1))
        self.assertEqual(my_period.end, datetime(1746, 1, 1))
        my_period = init_period("174512")
        self.assertEqual(my_period.start, datetime(1745, 12, 1))
        self.assertEqual(my_period.end, datetime(1746, 1, 1))
        my_period = init_period("1745125")
        self.assertEqual(my_period.start, datetime(1745, 12, 1))
        self.assertEqual(my_period.end, datetime(1746, 1, 1))
        my_period = init_period("17451225")
        self.assertEqual(my_period.start, datetime(1745, 12, 25))
        self.assertEqual(my_period.end, datetime(1745, 12, 26))
        my_period = init_period("174512253")
        self.assertEqual(my_period.start, datetime(1745, 12, 25))
        self.assertEqual(my_period.end, datetime(1745, 12, 26))
        my_period = init_period("1745122513")
        self.assertEqual(my_period.start, datetime(1745, 12, 25, 13))
        self.assertEqual(my_period.end, datetime(1745, 12, 25, 14))
        my_period = init_period("17451225132")
        self.assertEqual(my_period.start, datetime(1745, 12, 25, 13))
        self.assertEqual(my_period.end, datetime(1745, 12, 25, 14))
        my_period = init_period("174512251324")
        self.assertEqual(my_period.start, datetime(1745, 12, 25, 13, 24))
        self.assertEqual(my_period.end, datetime(1745, 12, 25, 13, 25))
        # TODO: Deal with longer strings than possible to treat...

    def test_period(self):
        my_period = init_period("1-6")
        self.assertEqual(my_period.start, datetime(1, 1, 1))
        self.assertEqual(my_period.end, datetime(7, 1, 1))
        my_period = init_period("52-68")
        self.assertEqual(my_period.start, datetime(52, 1, 1))
        self.assertEqual(my_period.end, datetime(69, 1, 1))
        my_period = init_period("873-999")
        self.assertEqual(my_period.start, datetime(873, 1, 1))
        self.assertEqual(my_period.end, datetime(1000, 1, 1))
        my_period = init_period("1745-1847")
        self.assertEqual(my_period.start, datetime(1745, 1, 1))
        self.assertEqual(my_period.end, datetime(1848, 1, 1))
        my_period = init_period("17452-18475")
        self.assertEqual(my_period.start, datetime(1745, 1, 1))
        self.assertEqual(my_period.end, datetime(1848, 1, 1))
        my_period = init_period("174512_184705")
        self.assertEqual(my_period.start, datetime(1745, 12, 1))
        self.assertEqual(my_period.end, datetime(1847, 6, 1))
        my_period = init_period("1745125_1847053")
        self.assertEqual(my_period.start, datetime(1745, 12, 1))
        self.assertEqual(my_period.end, datetime(1847, 6, 1))
        my_period = init_period("17451225-18470513")
        self.assertEqual(my_period.start, datetime(1745, 12, 25))
        self.assertEqual(my_period.end, datetime(1847, 5, 14))
        my_period = init_period("174512253-184705136")
        self.assertEqual(my_period.start, datetime(1745, 12, 25))
        self.assertEqual(my_period.end, datetime(1847, 5, 14))
        my_period = init_period("1745122513-1847051316")
        self.assertEqual(my_period.start, datetime(1745, 12, 25, 13))
        self.assertEqual(my_period.end, datetime(1847, 5, 13, 17))
        my_period = init_period("17451225132-18470513169")
        self.assertEqual(my_period.start, datetime(1745, 12, 25, 13))
        self.assertEqual(my_period.end, datetime(1847, 5, 13, 17))
        my_period = init_period("174512251324-184705131659")
        self.assertEqual(my_period.start, datetime(1745, 12, 25, 13, 24))
        self.assertEqual(my_period.end, datetime(1847, 5, 13, 17))
        my_period = init_period(cperiod(datetime(1850, 1, 2), datetime(1950, 5, 23)))
        self.assertEqual(my_period.start, datetime(1850, 1, 2))
        self.assertEqual(my_period.end, datetime(1950, 5, 23))
        my_period = init_period("174512251324-184705")
        self.assertEqual(my_period.start, datetime(1745, 12, 25, 13, 24))
        self.assertEqual(my_period.end, datetime(1847, 6, 1, 0, 0))

    def tearDown(self):
        craz()


class SortPeriodsListTests(unittest.TestCase):

    def test_args(self):
        sort_periods_list([cperiod(datetime(1850, 2, 1), datetime(1950, 6, 2)),
                           init_period("1560-18421230")])
        with self.assertRaises(Climaf_Period_Error):
            sort_periods_list(["1850-1950", "1520-1420"])
        with self.assertRaises(TypeError):
            sort_periods_list("1850-1950", "1520-1420")

    def test_sort(self):
        my_period_1 = cperiod(datetime(1850, 1, 2), datetime(1950, 3, 4))
        my_period_2 = cperiod(datetime(1740, 5, 6), datetime(1850, 1, 6, 14))
        my_period_3 = cperiod(datetime(1800, 5, 2), datetime(1847, 6, 3))
        my_period_4 = cperiod(datetime(2000, 5, 6), datetime(2061, 4, 9))
        self.assertEqual(sort_periods_list([my_period_1, my_period_2]), [my_period_2, my_period_1])
        ordered_list = [my_period_2, my_period_3, my_period_1, my_period_4]
        unordered_list = [my_period_1, my_period_4, my_period_1, my_period_3, my_period_2]
        self.assertEqual(sort_periods_list(unordered_list), ordered_list)

    def tearDown(self):
        craz()


class MergePeriodsTests(unittest.TestCase):

    def test_args(self):
        merge_periods([cperiod(datetime(1850, 2, 1), datetime(1950, 6, 2)),
                       init_period("1560-18421230")])
        with self.assertRaises(Climaf_Period_Error):
            merge_periods(["1850-1950", "1520-1420"])

    def test_merge(self):
        my_period_1 = cperiod(datetime(1850, 1, 2), datetime(1950, 3, 4))
        my_period_2 = cperiod(datetime(1740, 5, 6), datetime(1850, 1, 6, 14))
        my_period_3 = cperiod(datetime(1800, 5, 2), datetime(1847, 6, 3))
        my_period_4 = cperiod(datetime(2000, 5, 6), datetime(2061, 4, 9))
        unordered_list = [my_period_1, my_period_4, my_period_3, my_period_2]
        result_list = [cperiod(datetime(1740, 5, 6), datetime(1950, 3, 4)),
                       cperiod(datetime(2000, 5, 6), datetime(2061, 4, 9))]
        self.assertEqual(merge_periods(unordered_list), result_list)

    def tearDown(self):
        craz()


class IntersectPeriodsListsTests(unittest.TestCase):

    def test_args(self):
        intersect_periods_list(
            [cperiod(datetime(1850, 2, 1), datetime(1950, 6, 2)), init_period("1560-18421230")],
            [init_period("2050-2100"), init_period("1900-1960")]
        )
        with self.assertRaises(Climaf_Period_Error):
            merge_periods(["1850-1950", "1520-1420"], ["1900-1980", "1450-1520"])

    def test_intersect(self):
        my_period_1 = cperiod(datetime(1850, 1, 2), datetime(1950, 3, 4))
        my_period_2 = cperiod(datetime(1740, 5, 6), datetime(1850, 1, 6, 14))
        my_period_3 = cperiod(datetime(1800, 5, 2), datetime(1847, 6, 3))
        my_period_4 = cperiod(datetime(1900, 5, 6), datetime(2061, 4, 9))
        my_list_1 = [my_period_1, my_period_3]
        my_list_2 = [my_period_2, my_period_4]
        result_list = [cperiod(datetime(1800, 5, 2), datetime(1847, 6, 3)),
                       cperiod(datetime(1850, 1, 2), datetime(1850, 1, 6, 14)),
                       cperiod(datetime(1900, 5, 6), datetime(1950, 3, 4))]
        self.assertEqual(intersect_periods_list(my_list_1, my_list_2), result_list)

    def tearDown(self):
        craz()


class LastYearsTest(unittest.TestCase):

    def test_args(self):
        lastyears("1850-1950", 52)
        lastyears(cperiod(datetime(1850, 1, 1), datetime(1950, 2, 3)), 4)
        with self.assertRaises(Climaf_Period_Error):
            lastyears(1850, 5)
        with self.assertRaises(Climaf_Period_Error):
            lastyears("1850-1870", "toto")

    def test_last_years(self):
        my_period = cperiod(datetime(1850, 1, 1), datetime(1859, 5, 25))
        self.assertEqual(lastyears(my_period, 1), repr(cperiod(datetime(1858, 5, 25), datetime(1859, 5, 25))))
        self.assertEqual(lastyears(my_period, 15), repr(my_period))

    def tearDown(self):
        craz()


class FirstYearsTest(unittest.TestCase):

    def test_args(self):
        firstyears("1850-1950", 52)
        firstyears(cperiod(datetime(1850, 1, 1), datetime(1950, 2, 3)), 4)
        with self.assertRaises(Climaf_Period_Error):
            firstyears(1850, 5)
        with self.assertRaises(Climaf_Period_Error):
            firstyears("1850-1870", "toto")

    def test_last_years(self):
        my_period = cperiod(datetime(1850, 6, 23), datetime(1859, 1, 1))
        self.assertEqual(firstyears(my_period, 1), repr(init_period("18500623-18510622")))
        self.assertEqual(firstyears(my_period, 15), repr(my_period))

    def tearDown(self):
        craz()


if __name__ == '__main__':
    # Jump into the test directory
    tmp_directory = "/".join([os.environ["HOME"], "tmp", "tests", "test_period"])
    remove_dir_and_content(tmp_directory)
    if not os.path.isdir(tmp_directory):
        os.makedirs(tmp_directory)
    os.chdir(tmp_directory)
    setNewUniqueCache(tmp_directory)
    unittest.main()
