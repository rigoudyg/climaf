#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test the classes module.
"""
from __future__ import print_function, division, unicode_literals, absolute_import


import os
import unittest

from tests.tools_for_tests import remove_dir_and_content

from climaf.cache import setNewUniqueCache
from climaf.classes import cproject, cdef, Climaf_Classes_Error, cobject, cdummy, processDatasetArgs, cdataset, calias
from climaf.period import Climaf_Period_Error, init_period
from env.environment import *
from env.site_settings import atCNRM, onCiclad


class CprojectTests(unittest.TestCase):

    def test_cproject_init(self):
        cproject("my_project", ("my_arg", "my_default"), "my_other_arg", separator="-",
                 ensemble=["my_first_ensemble_arg", "my_other_ensemble_arg"])
        self.assertIn("my_project", cprojects)
        a_project = cprojects["my_project"]
        self.assertEqual(a_project.project, "my_project")
        self.assertEqual(a_project.facets, ["project", "simulation", "variable", "period", "domain", "my_arg",
                                            "my_other_arg"])
        self.assertDictEqual(a_project.facet_defaults, dict(my_arg="my_default"))
        self.assertEqual(a_project.separator, "-")
        self.assertEqual(a_project.crs,
                         "${project}-${simulation}-${variable}-${period}-${domain}-${my_arg}-${my_other_arg}")
        self.assertEqual(a_project.attributes_for_ensemble,
                         ["simulation", "my_first_ensemble_arg", "my_other_ensemble_arg"])
        cproject("my_project", "my_other_arg", separator="-", sep=".")
        self.assertIn("my_project", cprojects)
        a_project = cprojects["my_project"]
        self.assertEqual(a_project.project, "my_project")
        self.assertEqual(a_project.facets, ["project", "simulation", "variable", "period", "domain", "my_other_arg"])
        self.assertDictEqual(a_project.facet_defaults, dict())
        self.assertEqual(a_project.separator, ".")
        self.assertEqual(a_project.crs, "${project}.${simulation}.${variable}.${period}.${domain}.${my_other_arg}")
        self.assertEqual(a_project.attributes_for_ensemble, ["simulation", ])
        with self.assertRaises(Climaf_Classes_Error):
            cproject("my_project", "my_other_arg", sep=",")
        del cprojects["my_project"]

    def test_cproject_repr(self):
        cproject("my_project", "my_other_arg", sep=".")
        self.assertEqual(repr(cprojects["my_project"]),
                         "${project}.${simulation}.${variable}.${period}.${domain}.${my_other_arg}")

    @unittest.skipUnless(False, "Test not yet written")
    def test_cproject_crs2ds(self):
        # TODO: Write the test
        pass


class CdefTests(unittest.TestCase):

    def test_cdef(self):
        a = cdef("project")
        self.assertEqual(a, "")
        a = cdef("model", project="CMIP6")
        self.assertEqual(a, "*")
        cdef("model", value="CNRM-CM6-1", project="CMIP6")
        self.assertEqual(cprojects["CMIP6"].facet_defaults["model"], "CNRM-CM6-1")
        with self.assertRaises(Climaf_Classes_Error):
            cdef("my_attribute", project="CMIP6")
        with self.assertRaises(Climaf_Classes_Error):
            cdef("my_attribute", project="my_project")
        with self.assertRaises(Climaf_Classes_Error):
            cdef("my_attribute", value="my_value", project="my_project")


class CobjectTests(unittest.TestCase):

    def setUp(self):
        self.my_object = cobject()
        self.my_other_object = cobject()

    def test_cobject_init(self):
        self.assertEqual(self.my_object.crs, "void")

    def test_cobject_str(self):
        self.assertEqual(str(self.my_object), "void")

    def test_cobject_repr(self):
        self.assertEqual(repr(self.my_object), "void")

    def test_cobject_equal(self):
        self.assertEqual(self.my_object, self.my_other_object)
        self.assertNotEqual(self.my_object, "test")
        self.assertNotEqual(self.my_object, cdummy())

    @unittest.expectedFailure
    def test_cobject_register(self):
        # TODO: Modify CliMAF to raise an exception
        with self.assertRaises(NotImplementedError):
            self.my_object.register()

    @unittest.expectedFailure
    def test_cobject_erase(self):
        # TODO: Modify CliMAF to raise an exception
        with self.assertRaises(NotImplementedError):
            self.my_object.erase()


class CdummyTests(unittest.TestCase):

    def test_cdummy_init(self):
        cdummy()

    def test_cdummy_buildcrs(self):
        my_dummy = cdummy()
        self.assertEqual(my_dummy.buildcrs(), "ARG")

    def test_cdummy_equal(self):
        my_dummy = cdummy()
        my_other_dummy = cdummy()
        self.assertEqual(my_dummy, my_other_dummy)
        self.assertNotEqual(my_dummy, cobject())
        self.assertNotEqual(my_dummy, "test")


class ProcessDatasetArgsTests(unittest.TestCase):

    def test_CMIP6(self):
        # TODO: Write the test
        with self.assertRaises(Climaf_Period_Error):
            # TODO: Explicit the error
            processDatasetArgs(project="CMIP6")
        with self.assertRaises(Climaf_Classes_Error):
            processDatasetArgs(project="CMIP6", simulation="my_simulation")
        processDatasetArgs(project="CMIP6", period="1850-2000", simulation="")
        with self.assertRaises(Climaf_Classes_Error):
            processDatasetArgs(project="CMIP6", simulation="r1%t2")
        a = processDatasetArgs(project="CMIP6", period="1850-2000")
        self.assertEqual(sorted(list(a)), sorted(["domain", "experiment", "grid", "institute", "mip", "model",
                                                  "realization", "root", "simulation", "table", "variable", "version",
                                                  "project", "period"]))
        self.assertEqual(a["domain"], "global")
        self.assertEqual(a["experiment"], "historical")
        self.assertEqual(a["grid"], "g*")
        self.assertEqual(a["institute"], "*")
        self.assertEqual(a["mip"], "*")
        # TODO: Test the place on which the test is launched before this test
        self.assertEqual(a["model"], "CNRM-CM6-1")
        self.assertEqual(a["realization"], "r1i1p1f*")
        # TODO: Test the place on which the test is launched before this test
        if atCNRM:
            self.assertEqual(a["root"], "/cnrm/cmip")
        elif onCiclad:
            self.assertEqual(a["root"], "/bdd")
        else:
            self.assertEqual(a["root"], "")
        self.assertEqual(a["simulation"], "")
        self.assertEqual(a["table"], "*")
        self.assertEqual(a["variable"], "")
        self.assertEqual(a["version"], "latest")
        self.assertEqual(a["period"], init_period("1850-2000"))
        self.assertEqual(a["project"], "CMIP6")
        a = processDatasetArgs(project="CMIP6", period="fx")
        self.assertEqual(a["period"], init_period("fx"))

    def test_CMIP5(self):
        with self.assertRaises(Climaf_Period_Error):
            # TODO: Explicit the error
            processDatasetArgs(project="CMIP5")
        a = processDatasetArgs(project="CMIP5", period="1850-2000")
        self.assertEqual(sorted(list(a)), sorted(["domain", "experiment", "model", "realization", "root", "simulation",
                                                  "table", "variable", "version", "project", "period", "realm",
                                                  "frequency"]))
        self.assertEqual(a["domain"], "global")
        self.assertEqual(a["experiment"], "historical")
        self.assertEqual(a["model"], "")
        self.assertEqual(a["realization"], "r1i1p1")
        # TODO: Test the place on which the test is launched before this test
        if atCNRM:
            self.assertEqual(a["root"], "/cnrm/cmip/cnrm/ESG")
        elif onCiclad:
            self.assertEqual(a["root"], "/bdd")
        else:
            self.assertEqual(a["root"], "")
        self.assertEqual(a["simulation"], "")
        self.assertEqual(a["table"], "*")
        self.assertEqual(a["variable"], "")
        if atCNRM:
            self.assertEqual(a["version"], "*")
        else:
            self.assertEqual(a["version"], "latest")
        self.assertEqual(a["period"], init_period("1850-2000"))
        self.assertEqual(a["project"], "CMIP5")
        self.assertEqual(a["realm"], "*")
        self.assertEqual(a["frequency"], "*")
        a = processDatasetArgs(project="CMIP5", period="1850-2000", member=None)
        self.assertEqual(sorted(list(a)), sorted(["domain", "experiment", "model", "realization", "root", "simulation",
                                                  "table", "variable", "version", "project", "period", "realm",
                                                  "frequency"]))
        self.assertEqual(a["simulation"], "")
        a = processDatasetArgs(project="CMIP5", period="1850-2000", member="")
        self.assertEqual(sorted(list(a)), sorted(["domain", "experiment", "model", "realization", "root", "simulation",
                                                  "table", "variable", "version", "project", "period", "realm",
                                                  "frequency"]))
        self.assertEqual(a["simulation"], "")
        a = processDatasetArgs(project="CMIP5", period="1850-2000", member="toto")
        self.assertEqual(sorted(list(a)), sorted(["domain", "experiment", "model", "realization", "root", "simulation",
                                                  "table", "variable", "version", "project", "period", "realm",
                                                  "frequency"]))
        self.assertEqual(a["simulation"], "toto")
        a = processDatasetArgs(project="CMIP5", period="1850-2000", table="fx")
        self.assertEqual(a["simulation"], "r0i0p0")
        self.assertEqual(a["table"], "fx")
        self.assertEqual(repr(a["period"]), "fx")
        self.assertEqual(a["frequency"], "fx")
        a = processDatasetArgs(project="CMIP5", period="fx")
        self.assertEqual(a["simulation"], "r0i0p0")
        self.assertEqual(a["table"], "fx")
        self.assertEqual(repr(a["period"]), "fx")
        self.assertEqual(a["frequency"], "fx")
        a = processDatasetArgs(project="CMIP5", period="1850-2000", frequency="fx")
        self.assertEqual(a["simulation"], "r0i0p0")
        self.assertEqual(a["table"], "fx")
        self.assertEqual(repr(a["period"]), "fx")
        self.assertEqual(a["frequency"], "fx")
        a = processDatasetArgs(project="CMIP5", period="1850-2000", simulation="r0i0p0")
        self.assertEqual(a["simulation"], "r0i0p0")
        self.assertEqual(a["table"], "fx")
        self.assertEqual(repr(a["period"]), "fx")
        self.assertEqual(a["frequency"], "fx")

    def test_unknown(self):
        with self.assertRaises(Climaf_Period_Error):
            # TODO: Explicit the error
            processDatasetArgs(project="my_project")

    def test_without(self):
        with self.assertRaises(Climaf_Classes_Error):
            processDatasetArgs()
        cdef("project", "CMIP5")
        with self.assertRaises(Climaf_Period_Error):
            # TODO: Explicit the error
            processDatasetArgs()
        # TODO: Try to find a project in which after facets retrieval, the value is None to pass in the exception


class CdatasetTests(unittest.TestCase):

    def setUp(self):
        # TODO: Write the test
        if atCNRM:
            self.root = "/cnrm/cmip/cnrm/ESG"
        elif onCiclad:
            self.root = "/bdd"
        else:
            self.root = ""
        self.my_dataset = cdataset(project='CMIP5', model='CNRM-CM5', experiment='historical', frequency='monthly',
                                   simulation='r2i3p9', domain=[40, 60, -10, 20], variable='tas', period='1980-1989',
                                   version='last')
        self.my_other_dataset = cdataset(project='CMIP5', model='CNRM-CM5', experiment='historical',
                                         frequency='annual_cycle', simulation='r2i3p9',
                                         variable='tas,tos', period='1980-1989', version='last')

    @unittest.expectedFailure
    def test_cdataset_init(self):
        self.assertEqual(self.my_dataset.project, "CMIP5")
        self.assertEqual(self.my_dataset.simulation, "r2i3p9")
        self.assertEqual(self.my_dataset.variable, "tas")
        self.assertEqual(self.my_dataset.period, init_period("1980-1989"))
        self.assertEqual(self.my_dataset.domain, [40, 60, -10, 20])
        self.assertEqual(self.my_dataset.model, "CNRM-CM5")
        self.assertEqual(self.my_dataset.frequency, "monthly")
        self.assertDictEqual(self.my_dataset.kvp,
                             processDatasetArgs(project='CMIP5', model='CNRM-CM5', experiment='historical',
                                                frequency='monthly', simulation='r2i3p9', domain=[40, 60, -10, 20],
                                                variable='tas', period='1980-1989', version='last'))
        self.assertFalse(self.my_dataset.alias)
        self.assertEqual(self.my_dataset.crs,
                         "ds('CMIP5%r2i3p9%tas%1980-1989%[40, 60, -10, 20]%/cnrm/cmip/cnrm/ESG%CNRM-CM5%*%historical%"
                         "r1i1p1%monthly%*%last')")
        self.assertIsNone(self.my_dataset.files)
        self.assertIsNone(self.my_dataset.local_copies_of_remote_files)
        #
        self.assertEqual(self.my_other_dataset.variable, "tas,tos")
        #
        calias("CMIP5", "tas", scale=0.5)
        calias("CMIP5", "tos", offset=-273.15)
        # Try to find a test for which there is a problem with alias and variables
        with self.assertRaises(Climaf_Classes_Error):
            cdataset(project='CMIP5', model='CNRM-CM5', experiment='historical', frequency='annual_cycle',
                     simulation='r2i3p9', domain=[40, 60, -10, 20], variable='tas,tos', period='1980-1989',
                     version='last')

    def test_cdataset_setperiod(self):
        period_old = init_period("1980-1989")
        period_new = init_period("1980-1999")
        self.assertEqual(self.my_dataset.period, period_old)
        self.assertEqual(self.my_dataset.kvp["period"], period_old)
        self.assertEqual(self.my_dataset.crs,
                         "ds('CMIP5%r2i3p9%tas%1980-1989%[40, 60, -10, 20]%{}%CNRM-CM5%*%historical%r1i1p1%monthly%*"
                         "%last')".format(self.root))
        self.my_dataset.setperiod(period_new)
        self.assertEqual(self.my_dataset.period, period_new)
        self.assertEqual(self.my_dataset.kvp["period"], period_new)
        self.assertEqual(self.my_dataset.crs,
                         "ds('CMIP5%r2i3p9%tas%1980-1999%[40, 60, -10, 20]%{}%CNRM-CM5%*%historical%r1i1p1%monthly%*"
                         "%last')".format(self.root))
        self.my_dataset.setperiod(period_old)

    def test_cdataset_buildcrs(self):
        self.assertEqual(self.my_dataset.buildcrs(),
                         "ds('CMIP5%r2i3p9%tas%1980-1989%[40, 60, -10, 20]%{}%CNRM-CM5%*%historical%r1i1p1%monthly%*"
                         "%last')".format(self.root))
        self.assertEqual(self.my_dataset.buildcrs(period=init_period("2000")),
                         "ds('CMIP5%r2i3p9%tas%2000%[40, 60, -10, 20]%{}%CNRM-CM5%*%historical%r1i1p1%monthly%*"
                         "%last')".format(self.root))
        # TODO: When this option will be implemented, write the associated test
        # self.assertEqual(self.my_dataset.buildcrs(crsrewrite=None), "")
        self.assertEqual(self.my_other_dataset.buildcrs(),
                         "ds('CMIP5%r2i3p9%tas,tos%fx%global%{}%CNRM-CM5%*%historical%r1i1p1%annual_cycle%*"
                         "%last')".format(self.root))
        self.assertEqual(self.my_other_dataset.buildcrs(period=init_period("2000")),
                         "ds('CMIP5%r2i3p9%tas,tos%2000%global%{}%CNRM-CM5%*%historical%r1i1p1%annual_cycle%*"
                         "%last')".format(self.root))
        # TODO: When this option will be implemented, write the associated test
        # self.assertEqual(self.my_other_dataset.buildcrs(crsrewrite=None), "")

    def test_cdataset_equal(self):
        self.assertNotEqual(self.my_dataset, "test")
        self.assertNotEqual(self.my_dataset, cobject())
        my_dataset = self.my_dataset.explore("resolve")
        self.assertEqual(self.my_dataset, my_dataset)

    @unittest.skipUnless(False, "Test not yet written")
    def test_cdataset_errata(self):
        # TODO: Write the test
        pass

    @unittest.skipUnless(False, "Test not yet written")
    def test_cdataset_isLocal(self):
        # TODO: Write the test
        pass

    @unittest.skipUnless(False, "Test not yet written")
    def test_cdataset_isCached(self):
        # TODO: Write the test
        pass

    @unittest.skipUnless(False, "Test not yet written")
    def test_cdataset_oneVarPerFile(self):
        # TODO: Write the test
        pass

    @unittest.skipUnless(False, "Test not yet written")
    def test_cdataset_periodIsFine(self):
        # TODO: Write the test
        pass

    @unittest.skipUnless(False, "Test not yet written")
    def test_cdataset_domainIsFine(self):
        # TODO: Write the test
        pass

    @unittest.skipUnless(False, "Test not yet written")
    def test_cdataset_periodHasOneFile(self):
        # TODO: Write the test
        pass

    @unittest.skipUnless(False, "Test not yet written")
    def test_cdataset_hasOneMember(self):
        # TODO: Write the test
        pass

    @unittest.skipUnless(False, "Test not yet written")
    def test_cdataset_hasExactVariable(self):
        # TODO: Write the test
        pass

    @unittest.skipUnless(False, "Test not yet written")
    def test_cdataset_missingIsOK(self):
        # TODO: Write the test
        pass

    @unittest.skipUnless(False, "Test not yet written")
    def test_cdataset_explore(self):
        # TODO: Write the test
        pass

    @unittest.skipUnless(False, "Test not yet written")
    def test_cdataset_baseFiles(self):
        # TODO: Write the test
        pass

    @unittest.skipUnless(False, "Test not yet written")
    def test_cdataset_listfiles(self):
        # TODO: Write the test
        pass

    @unittest.skipUnless(False, "Test not yet written")
    def test_cdataset_hasRawVariable(self):
        # TODO: Write the test
        pass

    @unittest.skipUnless(False, "Test not yet written")
    def test_cdataset_check(self):
        # TODO: Write the test
        pass


class CensTests(unittest.TestCase):

    @unittest.skipUnless(False, "Test not yet written")
    def test_cens_init(self):
        # TODO: Write the test
        pass

    @unittest.skipUnless(False, "Test not yet written")
    def test_cens_equal(self):
        # TODO: Write the test
        pass

    @unittest.skipUnless(False, "Test not yet written")
    def test_cens_set_order(self):
        # TODO: Write the test
        pass

    @unittest.skipUnless(False, "Test not yet written")
    def test_cens_setitem(self):
        # TODO: Write the test
        pass

    @unittest.skipUnless(False, "Test not yet written")
    def test_cens_items(self):
        # TODO: Write the test
        pass

    @unittest.skipUnless(False, "Test not yet written")
    def test_cens_copy(self):
        # TODO: Write the test
        pass

    @unittest.skipUnless(False, "Test not yet written")
    def test_cens_pop(self):
        # TODO: Write the test
        pass

    @unittest.skipUnless(False, "Test not yet written")
    def test_cens_clear(self):
        # TODO: Write the test
        pass

    @unittest.skipUnless(False, "Test not yet written")
    def test_cens_update(self):
        # TODO: Write the test
        pass

    @unittest.skipUnless(False, "Test not yet written")
    def test_cens_buildcrs(self):
        # TODO: Write the test
        pass

    @unittest.skipUnless(False, "Test not yet written")
    def test_cens_check(self):
        # TODO: Write the test
        pass


class EdsTests(unittest.TestCase):

    @unittest.skipUnless(False, "Test not yet written")
    def test_eds(self):
        # TODO: Write the test
        pass


class FdsTests(unittest.TestCase):

    @unittest.skipUnless(False, "Test not yet written")
    def test_fds(self):
        # TODO: Write the test
        pass


class CtreeTests(unittest.TestCase):

    @unittest.skipUnless(False, "Test not yet written")
    def test_ctree_init(self):
        # TODO: Write the test
        pass

    @unittest.skipUnless(False, "Test not yet written")
    def test_ctree_buildcrs(self):
        # TODO: Write the test
        pass

    @unittest.skipUnless(False, "Test not yet written")
    def test_ctree_setperiod(self):
        # TODO: Write the test
        pass


class ScriptChildTests(unittest.TestCase):

    @unittest.skipUnless(False, "Test not yet written")
    def test_scriptChild_init(self):
        # TODO: Write the test
        pass

    @unittest.skipUnless(False, "Test not yet written")
    def test_scriptChild_buildcrs(self):
        # TODO: Write the test
        pass

    @unittest.skipUnless(False, "Test not yet written")
    def test_scriptChild_setperiod(self):
        # TODO: Write the test
        pass


class CompareTreesTests(unittest.TestCase):

    @unittest.skipUnless(False, "Test not yet written")
    def test_compare_trees(self):
        # TODO: Write the test
        pass


class AllowErrorOnDsTests(unittest.TestCase):

    @unittest.skipUnless(False, "Test not yet written")
    def test_allow_error_on_ds(self):
        # TODO: Write the test
        pass


class SelectProjectsTests(unittest.TestCase):

    @unittest.skipUnless(False, "Test not yet written")
    def test_select_projects(self):
        # TODO: Write the test
        pass


class DsTests(unittest.TestCase):

    @unittest.skipUnless(False, "Test not yet written")
    def test_ds(self):
        # TODO: Write the test
        pass


class CfreqsTests(unittest.TestCase):

    @unittest.skipUnless(False, "Test not yet written")
    def test_cfreqs(self):
        # TODO: Write the test
        pass


class CrealmsTests(unittest.TestCase):

    @unittest.skipUnless(False, "Test not yet written")
    def test_crealms(self):
        # TODO: Write the test
        pass


class CaliasTests(unittest.TestCase):

    @unittest.skipUnless(False, "Test not yet written")
    def test_calias(self):
        # TODO: Write the test
        pass


class VarIsAliasedTests(unittest.TestCase):

    @unittest.skipUnless(False, "Test not yet written")
    def test_varIsAliased(self):
        # TODO: Write the test
        pass


class CmissingTests(unittest.TestCase):

    @unittest.skipUnless(False, "Test not yet written")
    def test_cmissing(self):
        # TODO: Write the test
        pass


class CpageTests(unittest.TestCase):

    @unittest.skipUnless(False, "Test not yet written")
    def test_cpage_init(self):
        # TODO: Write the test
        pass

    @unittest.skipUnless(False, "Test not yet written")
    def test_cpage_scatter_on_page(self):
        # TODO: Write the test
        pass

    @unittest.skipUnless(False, "Test not yet written")
    def test_cpage_buildcrs(self):
        # TODO: Write the test
        pass


class CpagePdfTests(unittest.TestCase):

    @unittest.skipUnless(False, "Test not yet written")
    def test_cpage_pdf_init(self):
        # TODO: Write the test
        pass

    @unittest.skipUnless(False, "Test not yet written")
    def test_cpage_pdf_buildcrs(self):
        # TODO: Write the test
        pass


class GuessProjectsTests(unittest.TestCase):

    @unittest.skipUnless(False, "Test not yet written")
    def test_guess_projects(self):
        # TODO: Write the test
        pass

    @unittest.skipUnless(False, "Test not yet written")
    def test_guess_project(self):
        # TODO: Write the test
        pass


class BrowseTreeTests(unittest.TestCase):

    @unittest.skipUnless(False, "Test not yet written")
    def test_browse_tree(self):
        # TODO: Write the test
        pass


class DomainOfTests(unittest.TestCase):

    @unittest.skipUnless(False, "Test not yet written")
    def test_domainOf(self):
        # TODO: Write the test
        pass


class VarOfTests(unittest.TestCase):

    @unittest.skipUnless(False, "Test not yet written")
    def test_varOf(self):
        # TODO: Write the test
        pass


class ModelOfTests(unittest.TestCase):

    @unittest.skipUnless(False, "Test not yet written")
    def test_modelOf(self):
        # TODO: Write the test
        pass


class SimulationOfTests(unittest.TestCase):

    @unittest.skipUnless(False, "Test not yet written")
    def test_simulationOf(self):
        # TODO: Write the test
        pass


class ProjectOfTests(unittest.TestCase):

    @unittest.skipUnless(False, "Test not yet written")
    def test_projectOf(self):
        # TODO: Write the test
        pass


class RealmOfTests(unittest.TestCase):

    @unittest.skipUnless(False, "Test not yet written")
    def test_realmOf(self):
        # TODO: Write the test
        pass


class GridOfTests(unittest.TestCase):

    @unittest.skipUnless(False, "Test not yet written")
    def test_gridOf(self):
        # TODO: Write the test
        pass


class AttributeOfTests(unittest.TestCase):

    @unittest.skipUnless(False, "Test not yet written")
    def test_attributeOf(self):
        # TODO: Write the test
        pass


class ResolveFirstOrLastYearsTests(unittest.TestCase):

    @unittest.skipUnless(False, "Test not yet written")
    def test_resolve_first_or_last_years(self):
        # TODO: Write the test
        pass


if __name__ == '__main__':
    # Jump into the test directory
    tmp_directory = "/".join([os.environ["HOME"], "tmp", "tests", "test_classes"])
    remove_dir_and_content(tmp_directory)
    if not os.path.isdir(tmp_directory):
        os.makedirs(tmp_directory)
    setNewUniqueCache(tmp_directory)
    os.chdir(tmp_directory)
    unittest.main()
    remove_dir_and_content(tmp_directory)
