# Examples for some operators cdftools:
#
# - cdfmean =>
#    * cdfmean : computes the mean value of the field, 2D or 3D (output: excluded profile)
#    * cdfmean_profile : vertical profile of horizontal means for 3D fields (output: excluded mean value)
#    * cdfvar : compute the spatial variance, 2D or 3D (output: excluded mean value, profile and variance of profile)
#    * cdfvar_profile : vertical profile of spatial variance (output: excluded mean value, profile and variance)
#
# - cdfheatc (computes the heat content in the specified area)
#
# - cdfmxlheatc (computed the heat content in the mixed layer)
#
# - cdfstd =>
#    * cdfstd : compute the standard deviation of given variables
#    * cdfstdmoy : compute the mean value of the field, in addition to the standard deviation


from climaf.api import *
from climaf.operators import *
cdef("frequency","monthly") 
cdef("project","EM")

#-----------
#  cdfmean
#-----------
#
# CDFtools usage :
# cdfmean  IN-file IN-var T|U|V|F|W [imin imax jmin jmax kmin kmax]
#        ... [-full] [-var] [-zeromean] 
#
# CliMAF usage (cdfmean, cdfmean_profile, cdfvar, cdfvar_profile) :
#

# For example, define dataset with sea water velocity ("uo")
d1=ds(experiment="PRE6CPLCr2alb", variable="uo", period="199807", realm="O")

# How to get required files for cdfmean
fixed_fields('cdfmean',target=['/cnrm/aster/data3/aster/chevalli/Monitoring/MONITORING_v3.1/config/ORCA1_mesh_mask.nc','/cnrm/aster/data3/aster/chevalli/Monitoring/MONITORING_v3.1/config/ORCA1_mesh_hgr.nc','/cnrm/aster/data3/aster/chevalli/Monitoring/MONITORING_v3.1/config/ORCA1_mesh_zgr.nc'], link=['/cnrm/aster/data3/aster/vignonl/code/climaf/mask.nc','/cnrm/aster/data3/aster/vignonl/code/climaf/mesh_hgr.nc','/cnrm/aster/data3/aster/vignonl/code/climaf/mesh_zgr.nc'])

#fixed_fields('cdfmean',target=['/cnrm/aster/data3/aster/vignonl/${experiment}/ORCA1_mesh_mask.nc','/cnrm/aster/data3/aster/vignonl/${project}/ORCA1_mesh_hgr.nc', '/cnrm/aster/data3/aster/chevalli/Monitoring/MONITORING_v3.1/config/ORCA1_mesh_zgr.nc'], link=['/cnrm/aster/data3/aster/vignonl/climaf/mask.nc','/cnrm/aster/data3/aster/vignonl/climaf/mesh_hgr.nc','/cnrm/aster/data3/aster/vignonl/climaf/mesh_zgr.nc'])

# Compute some mean values
my_cdfmean=cdfmean(d1,pos_grid='U')
cfile(my_cdfmean)

my_cdfmean2=cdfmean(d1,pos_grid='U',opt='-full')
cfile(my_cdfmean2)

my_cdfmean3=cdfmean(d1,pos_grid='U',imin=100,imax=102,jmin=117,jmax=118,kmin=1,kmax=2)
cfile(my_cdfmean3)


# How to get required files for cdfmean_profile
fixed_fields('cdfmean_profile',target=['/cnrm/aster/data3/aster/chevalli/Monitoring/MONITORING_v3.1/config/ORCA1_mesh_mask.nc','/cnrm/aster/data3/aster/chevalli/Monitoring/MONITORING_v3.1/config/ORCA1_mesh_hgr.nc','/cnrm/aster/data3/aster/chevalli/Monitoring/MONITORING_v3.1/config/ORCA1_mesh_zgr.nc'], link=['/cnrm/aster/data3/aster/vignonl/code/climaf/mask.nc','/cnrm/aster/data3/aster/vignonl/code/climaf/mesh_hgr.nc','/cnrm/aster/data3/aster/vignonl/code/climaf/mesh_zgr.nc'])

# Compute vertical profile
my_cdfmean_prof=cdfmean_profile(d1,pos_grid='U')
cfile(my_cdfmean_prof)


# How to get required files for cdfvar
fixed_fields('cdfvar',target=['/cnrm/aster/data3/aster/chevalli/Monitoring/MONITORING_v3.1/config/ORCA1_mesh_mask.nc','/cnrm/aster/data3/aster/chevalli/Monitoring/MONITORING_v3.1/config/ORCA1_mesh_hgr.nc','/cnrm/aster/data3/aster/chevalli/Monitoring/MONITORING_v3.1/config/ORCA1_mesh_zgr.nc'], link=['/cnrm/aster/data3/aster/vignonl/code/climaf/mask.nc','/cnrm/aster/data3/aster/vignonl/code/climaf/mesh_hgr.nc','/cnrm/aster/data3/aster/vignonl/code/climaf/mesh_zgr.nc'])

# Compute spatial variance
my_cdfvar=cdfvar(d1,pos_grid='U')
cfile(my_cdfvar)


# How to get required files for cdfvar_profile
fixed_fields('cdfvar_profile',target=['/cnrm/aster/data3/aster/chevalli/Monitoring/MONITORING_v3.1/config/ORCA1_mesh_mask.nc','/cnrm/aster/data3/aster/chevalli/Monitoring/MONITORING_v3.1/config/ORCA1_mesh_hgr.nc','/cnrm/aster/data3/aster/chevalli/Monitoring/MONITORING_v3.1/config/ORCA1_mesh_zgr.nc'], link=['/cnrm/aster/data3/aster/vignonl/code/climaf/mask.nc','/cnrm/aster/data3/aster/vignonl/code/climaf/mesh_hgr.nc','/cnrm/aster/data3/aster/vignonl/code/climaf/mesh_zgr.nc'])

# Compute vertical profile of spatial variance
my_cdfvar_prof=cdfvar_profile(d1,pos_grid='U')
cfile(my_cdfvar_prof)


#-----------
# cdfheatc   
#-----------
#
# CDFtools usage :
# cdfheatc  T-file ...
#     ... [imin imax jmin jmax kmin kmax] [-full] 
#
# CliMAF usage :
#

# Define dataset with salinity ("so" in .nc <=> "vosaline" for cdftools)
# and temperature ("thetao" in .nc <=> "votemper" for cdftools) 
d2=ds(experiment="PRE6CPLCr2alb", variable="so", period="199807", realm="O")
d3=ds(experiment="PRE6CPLCr2alb", variable="thetao", period="199807", realm="O")

# How to get required files for cdfheatc
fixed_fields('cdfheatc',target=['/cnrm/aster/data3/aster/chevalli/Monitoring/MONITORING_v3.1/config/ORCA1_mesh_mask.nc','/cnrm/aster/data3/aster/chevalli/Monitoring/MONITORING_v3.1/config/ORCA1_mesh_hgr.nc','/cnrm/aster/data3/aster/chevalli/Monitoring/MONITORING_v3.1/config/ORCA1_mesh_zgr.nc'], link=['/cnrm/aster/data3/aster/vignonl/code/climaf/mask.nc','/cnrm/aster/data3/aster/vignonl/code/climaf/mesh_hgr.nc','/cnrm/aster/data3/aster/vignonl/code/climaf/mesh_zgr.nc'])

# Compute the heat content in the specified area
my_cdfheatc=cdfheatc(d2,d3,imin=100,imax=102,jmin=117,jmax=118,kmin=1,kmax=2)
cfile(my_cdfheatc)


#----------------
#  cdfmxlheatc
#----------------
#
# CDFtools usage :
# cdfmxlheatc T-file [-full]
#
# CliMAF usage :
#

# Define dataset with temperature ("thetao" in .nc <=> "votemper" for cdftools)
# and mld ("omlmax" in .nc <=> "somxlt02" for cdftools)
d4=ds(experiment="PRE6CPLCr2alb", variable="thetao", period="199807", realm="O")
d5=ds(experiment="PRE6CPLCr2alb", variable="omlmax", period="199807", realm="O")

# How to get required files for cdfmxlheatc
fixed_fields('cdfmxlheatc',target=['/cnrm/aster/data3/aster/chevalli/Monitoring/MONITORING_v3.1/config/ORCA1_mesh_mask.nc','/cnrm/aster/data3/aster/chevalli/Monitoring/MONITORING_v3.1/config/ORCA1_mesh_zgr.nc'], link=['/cnrm/aster/data3/aster/vignonl/code/climaf/mask.nc','/cnrm/aster/data3/aster/vignonl/code/climaf/mesh_zgr.nc'])

# Compute the heat content in the mixed layer
my_cdfmxlheatc=cdfmxlheatc(d4,d5)
cfile(my_cdfmxlheatc)


#-----------
#  cdfstd
#-----------
#
# CDFtools usage :
# cdfstd [-save] [-spval0] [-nomissincl] [-stdopt] list_of files
#
# CliMAF usage (cdfstd, cdfstdmoy) : **mono-variable**
#

# For example, define dataset with mld ("omlmax") for period "199807-199810"
d6=ds(experiment="PRE6CPLCr2alb", variable="omlmax", period="199807-199810", realm="O")

# Compute the standard deviation of variable "omlmax"
my_cdfstd=cdfstd(d6)
cfile(my_cdfstd)

# Compute the mean value and standard deviation of "uo" field (sea water velocity)
my_cdfstd_moy=cdfstdmoy(d1)
cfile(my_cdfstd_moy)

