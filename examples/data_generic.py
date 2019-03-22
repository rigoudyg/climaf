#!/usr/bin/python
# -*- coding: utf-8 -*-

__doc__ = """
Example for CliMAF access to data organized in various ways, using the 
data organization called 'generic' :

- data according to CAMI atlas naming scheme at CNRM such as :
/cnrm/est/COMMON/cami/V1.8/climlinks/CAYAN/hfls_1m_194601_199803_CAYAN.nc

- data sample distributed with CliMAF

- data organized according to OCMIP5 on Ciclad such as in :
/prodigfs/OCMIP5/OUTPUT/IPSL/IPSL-CM4/CTL/mon/CACO3/CACO3_IPSL_IPSL-CM4_CTL_1860-1869.nc

- data organized according to OBS4MIPS data at CNRM such as :
/cnrm/amacs/DATA/Obs4MIPs/netcdf/monthly_mean/clt_MODIS_L3_C5_200003-201109.nc

"""

# S.Senesi - march 2015

# Load Climaf functions and site settings
# This sets logical flags 'onCiclad' and 'atCNRM'
from climaf.api import *

if atCNRM:
    # NOTE : THE PROJECT AND DATALOC DECLARATION BELOW ARE ACTUALLY BUILT-IN AND NOT NECESSARY
    # They show here as an example of CliMAF felxibility

    # First declare project 'CAMIOBS' - Default project attribute 'simulation' will be used to identify a data source
    # Some data sources have a "." in their name, hence must use another separator for this project
    cproject("CAMIOBS", separator="_")

    # Root directory for obs data organized 'a la CAMI' on CNRM's Lustre file system.
    CAMIOBS_root = "/cnrm/est/COMMON/cami/V1.8/climlinks/"

    # Pattern for matching CAMI obs data files and their directory.
    # We choose to use facet 'model' to carry the observation source
    CAMIOBS_pattern = "${simulation}/${variable}_1m_YYYYMM_YYYYMM_${simulation}.nc"

    # Declare the CAMIOBS pattern to be associated with a project we name OBS_CAMI
    dataloc(project="CAMIOBS", organization="generic",
            url=[CAMIOBS_root + CAMIOBS_pattern])

    # From here, you can define your dataset using these files.
    # You need only to define the facets useful w.r.t. the patterns
    # i.e. here : model and variable
    pr_gpcp = ds(project="CAMIOBS", simulation="GPCP2.5d", variable="pr", period="1979-1980")

    # Display the basic filenames involved in the dataset
    pr_gpcp.baseFiles()

    # Let CliMAF generate a file with the exact dataset in its disk cache
    # i.e. : select period and/or variables, aggregate files...
    my_file = cfile(pr_gpcp)
    print my_file

    # Check file size and content
    import os

    os.system("ls -al " + my_file)
    # os.system("ncdump -h "+my_file)

# ---------------------------------------------------------------
# Access example data files (see comments above)
# ---------------------------------------------------------------

# First declare project and its 'non-standard' attribute(s) 'frequency'
# NOTE : THE PROJECT AND DATALOC DECLARATION BELOW ARE ACTUALLY BUILT-IN AND NOT NECESSARY
# They show here as an example of CliMAF flexibility
cproject("example", "frequency")
data_pattern_L = cpath + "/../examples/data/${simulation}/L/${simulation}SFXYYYY.nc"
data_pattern_A = cpath + "/../examples/data/${simulation}/A/${simulation}PLYYYY.nc"
dataloc(project="example", organization="generic", url=[data_pattern_A, data_pattern_L])

# Access a dataset
rst = ds(project="example", simulation="AMIPV6ALB2G", variable="rst", period="1980")
l = rst.baseFiles()
my_file = cfile(rst)

# ---------------------------------------------------------------
# Access OCMIP5 data on Ciclad (see comments above)
# ---------------------------------------------------------------

if onCiclad:
    # These definitions are now built-in :
    # cproject("OCMIP5","model","frequency")
    # cfreqs('OCMIP5',{'monthly':'mon' })

    # dataloc(project="OCMIP5_Ciclad", organization="generic",
    #        url=['/prodigfs/OCMIP5/OUTPUT/*/${model}/${simulation}/${frequency}/'
    #             '${variable}/${variable}_*_${model}_${simulation}_YYYY-YYYY.nc'])

    cdef("model", "IPSL-CM4")
    cdef("frequency", "monthly")

    cactl = ds(project="OCMIP5", simulation="CTL", variable="CACO3", period="1860-1861")
    print cactl.baseFiles()

    my_file = cfile(cactl)
    print my_file

# ---------------------------------------------------------------
# Access OBS4MIPs data at CNRM (see comments above)
# ---------------------------------------------------------------

if atCNRM:
    cproject("OBS4MIPS", "frequency")

    pattern = "/cnrm/amacs/DATA/Obs4MIPs/netcdf/${frequency}/" + \
              "${variable}_${simulation}_*_YYYYMM-YYYYMM.nc"
    dataloc(project="OBS4MIPS", organization="generic", url=[pattern])

    pr_obs = ds(project="OBS4MIPS", variable="pr", frequency="monthly_mean",
                period="1979-1980", simulation="GPCP-SG")

    print pr_obs.baseFiles()
    my_file = cfile(pr_obs)
    print my_file

if my_file is None:
    exit(1)

# Managing fiexed fields : use specific dataloc and frequency='fx
###################################################################

# If you want to access fixed fields, you must describe them as attached to a given 'model',
# and using frequency 'fx' , and write it as indicated below

# define a pattern for accessing fixed fields (here we use a set of fixed fields from CMIP5,
# but this is not mandatory)
pattern_fx_CNRM_CM5 = "/cnrm/cmip/cnrm/ESG/CMIP5/output1/CNRM-CERFACS/" + \
                      "CNRM-CM5/piControl/fx/*/fx/r0i0p0/v20130826/${variable}/${variable}_fx_CNRM-CM5_*nc"

# Tell which model use that fixed fields
dataloc(model="CNRM-CM5", frequency="fx", organization="generic", url=[pattern_fx_CNRM_CM5])

# You may then use period='fx' for describing and accessing the data::
cdef("project", "CMIP5")
sftlf = ds(model="CNRM-CM5", variable="sftlf", frequency="fx")
if atCNRM:
    print sftlf.baseFiles()

# If a given experiment has modified fixed fields, you may write::
pattern_fx_CNRM_CM5_lgm = "/cnrm/cmip/cnrm/ESG/CMIP5/output1/CNRM-CERFACS/" + \
                          "CNRM-CM5/lgm/fx/*/fx/r0i0p0/v20130826/${variable}/${variable}_fx_CNRM-CM5_*nc"
dataloc(model="CNRM-CM5", simulation="LGM", frequency="fx", organization="generic",
        url=[pattern_fx_CNRM_CM5_lgm])

# if you have one set of fixed fields per simulation/experiment, you can even use
# URLs that include a pattern for the simulation name,

sftlf_lgm = ds(model="CNRM-CM5", variable="sftlf", frequency="fx", simulation="LGM")
if atCNRM:
    print sftlf_lgm.baseFiles()

# Note : access to fx fields for projects or experiments related to an
# organization=CMIP5_DRS is built-in: no additionnal dataloc() call; and version
# used is the last one; just use frequency='fx' as for other datasets

# If you need more functions related to fixed fields, please complain to 'climaf at meteo dot fr'
