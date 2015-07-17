# Example for cdftransport operator of cdftools:
# - compute the transport accross a section

#----------------
#  cdftransport
#----------------
#
# CDFtools usage :
# cdftransport [-test  u v ] [-noheat ] [-plus_minus ] [-obc]...
#                   ... [VT-file] U-file V-file [-full] |-time jt] ...
#                   ... [-time jt ] [-zlimit limits of level]
#
# CliMAF usage :
#

from climaf.api import *
from climaf.operators import *
cdef("frequency","monthly")

# Use "NEMO" project, where VT-files (netcdf file with mean values of vt, vs, ut, us
# for heat and salt transport) are defined
cdef("project","NEMO")

# Define dataset with uo ("uo" in .nc <=> "vozocrtx" for cdftools),
# vo ("vo" in .nc <=> "vomecrty" for cdftools), vt (:=vomevt), vs (:=vomevs),
# ut (:=vozout), us (:=vozous) for heat and salt transport
d1=ds(experiment="PRE6CPLCr2alb", variable="uo", period="199807",grid='grid_U',table='table2.3')
d2=ds(experiment="PRE6CPLCr2alb", variable="vo", period="199807",grid='grid_V',table='table2.3')
d3=ds(experiment="PRE6CPLCr2alb", variable="vomevt", period="199807",grid='VT')
d4=ds(experiment="PRE6CPLCr2alb", variable="vomevs", period="199807",grid='VT')
d5=ds(experiment="PRE6CPLCr2alb", variable="vozout", period="199807",grid='VT')
d6=ds(experiment="PRE6CPLCr2alb", variable="vozous", period="199807",grid='VT')

# How to get required files for cdftransport
fixed_fields('cdftransport',target=['/cnrm/aster/data3/aster/chevalli/Monitoring/MONITORING_v3.1/config/ORCA1_mesh_hgr.nc','/cnrm/aster/data3/aster/chevalli/Monitoring/MONITORING_v3.1/config/ORCA1_mesh_zgr.nc'], link=['/cnrm/aster/data3/aster/vignonl/code/climaf/mesh_hgr.nc','/cnrm/aster/data3/aster/vignonl/code/climaf/mesh_zgr.nc'])

# Compute the transport accross specified section
my_cdftransport=cdftransport(d3,d4,d5,d6,d1,d2,imin=117,imax=117,jmin=145,jmax=147,opt2='-full')
cfile(my_cdftransport)
