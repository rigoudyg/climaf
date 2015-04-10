__doc__="""
Example for CliMAF access to data organized in various ways, using the 
data organization called 'generic' :

- data according to CAMI atlas naming scheme at CNRM such as :
/cnrm/aster/data1/UTILS/cami/V1.7/climlinks/CAYAN/hfls_1m_194601_199803_CAYAN.nc

- data sample distributed with CliMAF

- data organized according to OCMIP5 on Ciclad such as in :
/prodigfs/OCMIP5/OUTPUT/IPSL/IPSL-CM4/CTL/mon/CACO3/CACO3_IPSL_IPSL-CM4_CTL_1860-1869.nc

- data organized according to OBS4MIPS data at CNRM such as :
/cnrm/vdr/DATA/Obs4MIPs/netcdf/monthly_mean/clt_MODIS_L3_C5_200003-201109.nc

"""

# S.Senesi - march 2015

# Load Climaf functions and site settings
# This sets logical flags 'onCiclad' and 'atCNRM'
from climaf.api import *

if atCNRM :
    # First declare project OBS_CAMI 
    cproject("CAMI_OBS")
    
    # Root directory for obs data organized 'a la CAMI' on CNRM's Lustre file system.
    CAMI_OBS_root="/cnrm/aster/data1/UTILS/cami/V1.7/climlinks/"
    
    # Pattern for matching CAMI obs data files and their directory. 
    # We choose to use facet 'model' to carry the observation source
    CAMI_OBS_pattern="${model}/${variable}_1m_YYYYMM_YYYYMM_${model}.nc"
    
    # Declare the CAMI_OBS pattern to be associated with a project we name OBS_CAMI
    dataloc(project="CAMI_OBS", organization="generic", 
            url=[CAMI_OBS_root+CAMI_OBS_pattern])
    
    # From here, you can define your dataset using these files. 
    # You need only to define the facets useful w.r.t. the patterns
    # i.e. here : model and variable
    pr_gpcp=ds(project="CAMI_OBS", model="GPCP2.5d", variable="pr", period="1979-1980")
    
    # Display the basic filenames involved in the dataset 
    pr_gpcp.baseFiles()
    
    # Let CliMAF generate a file with the exact dataset in its disk cache 
    # i.e. : select period and/or variables, aggregate files...
    my_file=cfile(pr_gpcp)
    print my_file
    
    # Check file size and content
    import os
    os.system("ls -al "+my_file)
    #os.system("ncdump -h "+my_file)


#---------------------------------------------------------------
# Access example data files (see comments above)
#---------------------------------------------------------------

# First declare project and its 'non-standard' attribute(s) 'frequency'
cproject("example","frequency")
data_pattern_L=cpath+"/../examples/data/${experiment}/L/${experiment}SFXYYYY.nc"
data_pattern_A=cpath+"/../examples/data/${experiment}/A/${experiment}PLYYYY.nc"
dataloc(project="example",organization="generic",url=[data_pattern_A,data_pattern_L])
rst=ds(project="example", experiment="AMIPV6ALB2G", variable="rst", period="1980-1981")
l=rst.baseFiles()
rst_file=cfile(rst)


#---------------------------------------------------------------
# Access OCMIP5 data on Ciclad (see comments above)
#---------------------------------------------------------------

if onCiclad :
    cproject("OCMIP5_Ciclad","frequency")
    
    dataloc(project="OCMIP5_Ciclad", organization="generic",
            url=['/prodigfs/OCMIP5/OUTPUT/*/${model}/${experiment}/${frequency}/${variable}/${variable}_*_${model}_${experiment}_YYYY-YYYY.nc'])
    
    cdef("model","IPSL-CM4") 
    cdef("frequency","mon") # Must use the right shortcut for the project, not "monthly"
    
    cactl=ds(project="OCMIP5_Ciclad", experiment="CTL", 
             variable="CACO3", period="1860-1861")
    print cactl.baseFiles()

    my_file=cfile(cactl)
    print my_file


#---------------------------------------------------------------
# Access OBS4MIPs data at CNRM (see comments above)
#---------------------------------------------------------------

if atCNRM :
    
    cproject("OBS4MIPS","frequency")

    pattern="/cnrm/vdr/DATA/Obs4MIPs/netcdf/${frequency}/"+
            "${variable}_${experiment}_*_YYYYMM-YYYYMM.nc"
    dataloc(project="OBS4MIPS", organization="generic", url=[pattern])

    pr_obs=ds(project="OBS4MIPS", variable="pr", frequency="monthly_mean"
              period="1979-1980", experiment="GPCP")

    print pr_obs.baseFiles()
    my_file=cfile(pr_obs)
    print my_file

if (my_file is None) : exit(1)

# Managing fiexed fields : use specific dataloc and frequency='fx
###################################################################

# If you want to access fixed fields, you must describe them as attached to a given 'model', 
# and using frequency 'fx' , and write it as indicated below

# define a pattern for accessing fixed fields (here we use a set of fixed fields from CMIP5,
# but this is not mandatory)
pattern_fx_CNRM_CM5="/cnrm/aster/data*/ESG/data*/CMIP5/output1/CNRM-CERFACS/CNRM-CM5/piControl/fx/*/fx/r0i0p0/v20130826/${variable}/${variable}_fx_CNRM-CM5_*nc"

# Tell which model use that fixed fields
dataloc(model="CNRM-CM5",frequency="fx",organization="generic", url=[pattern_fx_CNRM_CM5])

# You may then use period='fx' for describing and accessing the data::
sftlf=ds(model="CNRM-CM5", variable="sftlf", frequency="fx")
if atCNRM: print sftlf.baseFiles()

# If a given experiment has modified fixed fields, you may write::
pattern_fx_CNRM_CM5_lgm="/cnrm/aster/data*/ESG/data*/CMIP5/output1/CNRM-CERFACS/CNRM-CM5/lgm/fx/*/fx/r0i0p0/v20130826/${variable}/${variable}_fx_CNRM-CM5_*nc"
dataloc(model="CNRM-CM5",experiment="LGM", frequency="fx",organization="generic",
        url=[pattern_fx_CNRM_CM5_lgm])

# You can also use URLs that include a pattern for the experiment name, if you have one set of
# fixed fields per experiment

sftlf_lgm=ds(model="CNRM-CM5", variable="sftlf", frequency="fx", experiment="LGM")
if atCNRM: print sftlf_lgm.baseFiles()

# Note : access to fx fields for projects or experiments related to an 
# organization=CMIP5_DRS is built-in: no additionnal dataloc() call; and version
# used is the last one; just use frequency='fx' as for other datasets

# If you need more functions related to fixed fields, please complain to 'climaf at meteo dot fr'


if (rstfile is None) : exit(1)
