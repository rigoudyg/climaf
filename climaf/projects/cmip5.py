"""
This module declares locations for searching data for projects CMIP5 for all frequencies, and where the data is
at CNRM and on Ciclad

Attributes for CMIP5 datasets are : model, rip (called simulation), frequency, table, realm, version

Syntax for these attributes is described in `the CMIP5 DRS document <http://cmip-pcmdi.llnl.gov/cmip5/docs/cmip5_data_reference_syntax.pdf>`_

Example for a CMIP5 dataset declaration ::

 >>> tas1pc=ds(project='CMIP5', model='CNRM-CM5', experiment='1pctCO2', variable='tas', frequency='monthly', period='1860-1861')


"""

import os
from climaf.dataloc import dataloc
from climaf.classes import cproject, calias, cfreqs,cdef
from climaf.site_settings import atCNRM, onCiclad

p=cproject("CMIP5" ,"model","experiment", ("frequency","monthly"),
           ("table","*"),("realm","*"),("version","last"),
           ensemble=["model","simulation"])
cdef("simulation","r1i1p1",project="CMIP5")

# Frequency alias
cfreqs('CMIP5', {'monthly':'mon' , 'daily':'day' })

urls_CMIP5=None

if atCNRM :
    # Declare a list of root directories for CNRM-CM CMIP5 data on CNRM's Lustre file system.
    urls_CMIP5=["/cnrm/aster/data2/ESG/data1", "/cnrm/aster/data2/ESG/data2", 
                "/cnrm/aster/data2/ESG/data5", "/cnrm/aster/data4/ESG/data6", 
                "/cnrm/aster/data4/ESG/data7", "/cnrm/aster/data4/ESG/data8",
                "/cnrm/aster/data2/ESG/vdr"]
if onCiclad :
    # Declare a list of root directories for CMIP5 data on IPLS's Ciclad file system
    urls_CMIP5=["/prodigfs/esg","/prodigfs/project/"]

if urls_CMIP5 :
    # Next command will lead to explore all directories in 'url' 
    # for searching data for a CliMAF dataset (by function ds) except if 
    # a more specific dataloc entry matches the arguments to 'ds'
    dataloc(project="CMIP5", organization="CMIP5_DRS", url=urls_CMIP5)
