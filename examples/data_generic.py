__doc__="""
Example for CliMAF access to data organized in various ways, using the 
'generic' organization

- data according to CAMI atlas naming scheme such as :
[/cnrm/aster/data1/UTILS/cami/V1.7/climlinks]/CAYAN/hfls_1m_194601_199803_CAYAN.nc

- data sample distributed with CliMAF

"""
# S.Senesi - feb 2015

# Load Climaf functions
from climaf.api import *
# Load default settings for IPSL and CNRM. This sets logcial flags 'onCiclad' and 'atCNRM'
from climaf.site_settings import *

if atCNRM :
    # Root directory for obs data organized 'a la CAMI' on CNRM's Lustre file system.
    CAMI_OBS_root="/cnrm/aster/data1/UTILS/cami/V1.7/climlinks/"

    # Pattern for matching CAMI obs data files and their directory. 
    # We choose to use facet 'model' to carry the observation source
    CAMI_OBS_pattern="${model}/${variable}_1m_YYYYMM_YYYYMM_${model}.nc"
    
    # Declare the CAMI_OBS pattern to be associated with a project we name OBS_CAMI
    dataloc(project="OBS_CAMI", organization="generic", url=[CAMI_OBS_root+CAMI_OBS_pattern])

    # From here, you can define your dataset using these files. 
    # You need only to define the facets useful w.r.t. the patterns, i.e. here : model and variable
    pr_gpcp=ds(project="OBS_CAMI", model="GPCP2.5d", variable="pr", period="1979-1980")

    # Display the basic filenames involved in the dataset 
    pr_gpcp.baseFiles()

    # Let CliMAF generate a file with the exact dataset in its disk cache 
    # i.e. : select period and/or variables, aggregate files...
    my_file=cfile(pr_gpcp)
    print my_file
    
    # Check file size and content
    import os
    os.system("ls -al "+my_file)
    #os.system("type ncdump && ncdump -h "+my_file)


# Access example data files , using the same steps as above

data_pattern_L=cpath+"/../examples/data/${experiment}/L/${experiment}SFXYYYY.nc"
data_pattern_A=cpath+"/../examples/data/${experiment}/A/${experiment}PLYYYY.nc"
dataloc(project="example",organization="generic",url=[data_pattern_A,data_pattern_L])
rst=ds(project="example", experiment="AMIPV6ALB2G", variable="rst", period="1980-1981")
l=rst.baseFiles()
rst_file=cfile(rst)


if (rstfile is None) : exit(1)
