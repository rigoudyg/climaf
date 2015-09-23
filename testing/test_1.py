"""
Basic test for accessing data in CMIP5_DRS hierarchy. With unittest

Call it as : python -m unittest -b -v -f test_1

S.Senesi - dec 2014
"""

import unittest, os.path
from climaf.api import *


class A_basic(unittest.TestCase):
    def setUp(self) :
        climaf.cache.setNewUniqueCache(os.path.expanduser("~/tmp/climaf_tmp_cache_test_basic"))
        #dataloc(project="example", simulation="AMIPV6ALB2G", organization="example", url=[cpath+"/../examples/data/AMIPV6ALB2G"])
        cdef("frequency","monthly")
        self.dg=ds(project="example", simulation="AMIPV6ALB2G", variable="tas", period="1980-1981")
        self.dir=dict()

    def test_1_print_dataset(self):
        pdg=`self.dg`
        print pdg
        expected="ds('example.AMIPV6ALB2G.tas.1980-1981.global.monthly')"
        print expected
        self.assertEqual(pdg,expected, 
                         'Issue printing a very basic dataset')

    def test_2_declaring_and_applying_a_script(self):
        mean=climaf.driver.capply("mean_and_std",self.dg) # Main output is the return value of applying the script
        std=mean.sdev         # Secondary output 'std' is a 'property' of main output
        sd=`std`
        actual=sd
        print "actual=",sd
        expected="mean_and_std(ds('example.AMIPV6ALB2G.tas.1980-1981.global.monthly')).sdev"
        print "expected=",expected
        self.assertEqual(sd,expected,' Issue building a compound expression (apply script)')

    def test_3_evaluating_a_script(self):
        mean=climaf.driver.capply("mean_and_std",self.dg) # Main output is the return value of applying the script
        std=mean.sdev         # Secondary output 'std' is a 'property' of main output
        fil=cfile(std)
        expected=climaf.cache.currentCache+'/d1/a.nc'
        print "actual=",fil
        print "expected=",expected
        self.assertEqual(fil,expected,"Issue evaluating script application as a file")

    def test_4_plotting(self):
        mean=climaf.driver.capply("mean_and_std",self.dg) # Main output is the return value of applying the script
        std=mean.sdev         # Secondary output 'std' is a 'property' of main output
        plot1d=climaf.driver.capply("timeplot",std,title="tas standard deviation") 
        # Have the plot displayed (this will also actually launch the script,
        cshow(plot1d)
	os.system("sleep 3s")

    def tearDown(self):
        climaf.cache.craz(hideError=True)



def skipUnless_CNRM_Lustre():
    if os.path.exists('/cnrm/aster'):
        return lambda func: func
    return unittest.skip("because CNRM's Lustre not available")

@skipUnless_CNRM_Lustre()
#@unittest.skip("Not tested here")
class B_CMIP5_DRS_CNRM(unittest.TestCase):
    def setUp(self) :
        climaf.cache.setNewUniqueCache(os.path.expanduser("~/tmp/climaf_tmp_cache_test_cmip5_drs"))
        # Declare a list of root directories for CMIP5 data on CNRM's Lustre file system.
        urls_CMIP5_CNRM=["/cnrm/aster/data2/ESG/data1", "/cnrm/aster/data2/ESG/data2", "/cnrm/aster/data2/ESG/data5",
                         "/cnrm/aster/data4/ESG/data6", "/cnrm/aster/data4/ESG/data7", "/cnrm/aster/data4/ESG/data8"]
        dataloc(project="CMIP5", organization="CMIP5_DRS", url=urls_CMIP5_CNRM)
        cdef("frequency","monthly") ; cdef("model","CNRM-CM5") ; cdef("project","CMIP5")
        self.ds=ds(experiment="1pctCO2", variable="tas", period="1860-1861")

    def test_identifying_files(self):
        files=self.ds.baseFiles()
        self.assertEqual(files,"/cnrm/aster/data2/ESG/data1/CMIP5/output1/CNRM-CERFACS/CNRM-CM5/1pctCO2/mon/atmos/Amon/r1i1p1/v20110701/tas/tas_Amon_CNRM-CM5_1pctCO2_r1i1p1_185001-189912.nc", 'Issue accessing 1cptCO2 data files')

    def test_selecting_files(self):
        print `ds`
        my_file=cfile(self.ds); print "myfile = "+my_file
        expected=climaf.cache.currentCache+'/9e/2.nc'
        print "expected = "+expected
        self.assertEqual(my_file,expected,'Issue extracting 1pctCO2 data files')

    def tearDown(self):
        climaf.cache.craz(hideError=True)



def skipUnless_Ciclad():
    if os.path.exists('/prodigfs') or os.path.exists('/home/senesi/tmp/ciclad/prodigfs/esg/CMIP5'):
        return lambda func: func
    return unittest.skip("because not on Ciclad")

@skipUnless_Ciclad()
class B_CMIP5_DRS_Ciclad(unittest.TestCase):
    def setUp(self) :
        climaf.cache.setNewUniqueCache(os.path.expanduser("~/tmp/climaf_tmp_cache_test_cmip5_drs"))
        # Declare a list of root directories for CMIP5 data on CNRM's Lustre file system.
        urls_CMIP5=["/prodigfs/esg"]
        dataloc(organization="CMIP5_DRS", url=urls_CMIP5)
        cdef("frequency","monthly") ; cdef("model","CNRM-CM5") ; cdef("project","CMIP5")
        self.ds=ds(experiment="1pctCO2", variable="tas", period="1860-1861")

    def test_identifying_files(self):
        files=self.ds.baseFiles()
        expected="/prodigfs/esg/CMIP5/merge/CNRM-CERFACS/CNRM-CM5/1pctCO2/mon/atmos/Amon/r1i1p1/v20110701/tas/tas_Amon_CNRM-CM5_1pctCO2_r1i1p1_185001-189912.nc"
        print "actual="+files
        print "expected="+expected
        self.assertEqual(files,expected, 'Issue accessing 1cptCO2 data files')

    def test_selecting_files(self):
        my_file=cfile(self.ds)
        expected=climaf.cache.currentCache+'/1b/8.nc'
        print "actual="+my_file
        print "expected="+expected
        self.assertEqual(my_file,expected,'Issue extracting 1pctCO2 data files')

    def tearDown(self):
        climaf.cache.craz(hideError=True)




#@unittest.skip("Not tested here")
@skipUnless_Ciclad()
class C_OCMIP5_CIclad(unittest.TestCase):
    def setUp(self) :
        climaf.cache.setNewUniqueCache(os.path.expanduser("~/tmp/climaf_tmp_cache_drs_ocmip5_ciclad"))
        dataloc(project="OCMIP5", organization="generic",
                url=['/prodigfs/OCMIP5/OUTPUT/*/${model}/${experiment}/'
                     '${frequency}/${variable}/${variable}_*_${model}_'
                     '${experiment}_YYYY-YYYY.nc'])
        cdef("frequency","mon") ; cdef("project","OCMIP5")
        cactl=ds(experiment="CTL", model="IPSL-CM4", variable="CACO3", period="1860-1861")
        mfile=cfile(cactl)
        self.file=mfile

    def test_selecting_CACO3_for_IPSL_CM4(self):
        expected=climaf.cache.currentCache+'/f2/9.nc'
        print self.file
        print expected
        self.assertEqual(self.file,expected,'Issue')

    def tearDown(self):
        climaf.cache.craz(hideError=True)

## def suite():
##     suite = unittest.TestSuite()
##     suite.addTest(WidgetTestCase('test_default_size'))
##     suite.addTest(WidgetTestCase('test_resize'))
##     return suite

## def suite():
##     tests = ['test_identifying_files', 'test_selecting_files']
##     return unittest.TestSuite(map(WidgetTestCase, tests))

suite1 = unittest.TestLoader().loadTestsFromTestCase(A_basic)
suite2 = unittest.TestLoader().loadTestsFromTestCase(B_CMIP5_DRS_CNRM)
suite3 = unittest.TestLoader().loadTestsFromTestCase(C_OCMIP5_CIclad)
alltests = unittest.TestSuite([suite1, suite2,suite3])

if __name__ == '__main__':
    print "Testing some CliMAF basic operations"
    unittest.main()
